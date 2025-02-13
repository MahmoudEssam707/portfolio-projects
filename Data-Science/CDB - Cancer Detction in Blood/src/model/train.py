import os
from sklearn.metrics import classification_report
import mlflow.tensorflow
import tensorflow as tf
import numpy as np
import random
import yaml
import pandas as pd
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import (Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D)
from tensorflow.keras.applications import VGG19
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Set seed for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# Load configuration
with open("/home/mahmoud/CDIB/config.yaml", "r") as file:
    config = yaml.safe_load(file)

PROCESSED_DATA_PATH = config["paths"]["processed_data"]
CHECKPOINTS_PATH = config["paths"].get("checkpoints", "checkpoints/")
IMAGE_SIZE = tuple(config["training"]["image_size"])
BATCH_SIZE = config["training"]["batch_size"]
EPOCHS = config["training"]["epochs"]
LEARNING_RATE = config["training"]["learning_rate"]

# Load dataset
train_df = pd.read_csv(os.path.join(PROCESSED_DATA_PATH, "train.csv"))
val_df = pd.read_csv(os.path.join(PROCESSED_DATA_PATH, "val.csv"))
test_df = pd.read_csv(os.path.join(PROCESSED_DATA_PATH, "test.csv"))

# Function to create data generators
def create_generators(df, is_train, color_mode):
    datagen = ImageDataGenerator(
        rescale=1./255,
        # rotation_range=20 if is_train else 0,
        # width_shift_range=0.2 if is_train else 0,
        # height_shift_range=0.2 if is_train else 0,
        zoom_range=0.3 if is_train else 0,
        horizontal_flip=is_train,
        fill_mode='nearest' if is_train else None
    )
    return datagen.flow_from_dataframe(
        df, x_col="Image", y_col="Target", target_size=IMAGE_SIZE, batch_size=BATCH_SIZE, 
        class_mode='categorical', color_mode=color_mode, seed=SEED, shuffle=is_train
    )

# Create separate generators for RGB
train_gen_rgb = create_generators(train_df, True, "rgb")
val_gen_rgb = create_generators(val_df, False, "rgb")
test_gen_rgb = create_generators(test_df, False, "rgb")

# CNN model function
def build_cnn(input_shape):
    inputs = Input(shape=input_shape)
    x = Conv2D(64, (3,3), activation='relu')(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2,2))(x)

    x = Conv2D(128, (3,3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2,2))(x)

    x = Conv2D(256, (3,3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2,2))(x)

    x = Flatten()(x)
    x = Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.00001))(x)
    x = Dropout(0.5)(x)
    outputs = Dense(len(train_gen_rgb.class_indices), activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE), 
                  loss='categorical_crossentropy', metrics=['accuracy'])

    return model

# Build models
models = {
    "CNN": build_cnn((IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),  
    "VGG19": build_cnn((IMAGE_SIZE[0], IMAGE_SIZE[1], 3))  
}

# Load pretrained VGG19 for RGB
base_model = VGG19(weights='imagenet', include_top=False, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
base_model.trainable = False
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
outputs = Dense(len(train_gen_rgb.class_indices), activation='softmax')(x)
models["VGG19"] = Model(base_model.input, outputs)
models["VGG19"].compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE), 
                            loss='categorical_crossentropy', metrics=['accuracy'])
mlflow.tensorflow.autolog(disable=True)  
results = {}

for name, model in models.items():
    print(f"Training {name}...")
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=12, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3),
        ModelCheckpoint(os.path.join(CHECKPOINTS_PATH, f"{name}_best.keras"), monitor='val_loss', save_best_only=True)
    ]

    train_gen, val_gen, test_gen = train_gen_rgb, val_gen_rgb, test_gen_rgb
    
    with mlflow.start_run(run_name=name):
        history = model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=callbacks)

        # Get best model
        best_model = load_model(os.path.join(CHECKPOINTS_PATH, f"{name}_best.keras"))
        test_loss, test_acc = best_model.evaluate(test_gen)

        # Compute Precision, Recall, F1-score
        y_true = test_gen.classes
        y_pred = np.argmax(best_model.predict(test_gen), axis=1)
    
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

        precision = report["macro avg"]["precision"]
        recall = report["macro avg"]["recall"]
        f1_score = report["macro avg"]["f1-score"]

        # Log only required metrics
        mlflow.log_metric("train_loss", history.history['loss'][-1])
        mlflow.log_metric("train_accuracy", history.history['accuracy'][-1])
        mlflow.log_metric("val_loss", history.history['val_loss'][-1])
        mlflow.log_metric("val_accuracy", history.history['val_accuracy'][-1])
        mlflow.log_metric("test_loss", test_loss)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1_score)
        # Log model
        mlflow.tensorflow.log_model(best_model, "model")
        results[name] = test_acc

# Register the best model
best_model_name = max(results, key=results.get)
best_model = load_model(os.path.join(CHECKPOINTS_PATH, f"{best_model_name}_best.keras"))
# mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", f"{best_model_name}_best")

print(f"Best model: {best_model_name} with accuracy {results[best_model_name]:.4f}")