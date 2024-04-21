<center>

**HANDWRITTEN DIGIT RECOGNITION**

<img src="https://upload.wikimedia.org/wikipedia/commons/f/f7/MnistExamplesModified.png" width="500">

</center>

**🔍 Loading Data 🔍**

- The MNIST dataset consists of handwritten digits with a training set of 60,000 examples and a test set of 10,000 examples.
- We load the dataset using TensorFlow's MNIST module.

**🖼️ Visualising Data 🖼️**

- Display the first 9 images from the training set along with their respective labels.

**🔄 Preprocessing Data 🔄**

- Separate a portion of the test set for validation purposes.
- Normalise the pixel values of the images to the range [0, 1].
- Apply image data augmentation to the training set to improve generalisation.

**🛠️ Building the Model 🛠️**

- Construct a convolutional neural network (CNN) model for handwritten digit recognition.
- The model architecture includes convolutional layers, max-pooling layers, flattening layers, and dense layers.
- Employ early stopping and learning rate reduction as callbacks during training to prevent overfitting and improve convergence.

**🚀 Training the Model 🚀**

- Train the model on the augmented training data with validation on the separated validation set.
- Monitor the validation loss and accuracy during training.

**📊 Model Evaluation 📊**

- Evaluate the trained model on the test set to measure its performance.
- Display the test accuracy achieved by the model (Test accuracy:99.50%).

**🔮 Prediction Examples 🔮**

- Predict the class labels for a selection of images from the test set.
- Show the predicted class and the actual class for each image.

**💾 Model Export 💾**

- Save the trained model as 'model.h5' for future use.

**📱 GUI Application 📱**

- Additionally, a Graphical User Interface (GUI) application has been developed for easy interaction with the model.
