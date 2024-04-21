import customtkinter as ctk
from tkinter import filedialog
from PIL import Image,ImageTk
import numpy as np
import tensorflow as tf

# Load your trained model
model = tf.keras.models.load_model('model.h5')

# Create the tkinter app
app = ctk.CTk()
app.geometry("300x300")
app.title("Handwritten Digit Recognition")

# Create a canvas to display the image
canvas = ctk.CTkCanvas(app, width=280, height=280, bg="#242424")
canvas.pack()

# Create a label to display the predicted digit
label = ctk.CTkLabel(app, text="Prediction is: ")
label.pack()

# Function to handle the image selection
def select_image():
    # Open a file dialog to select an image
    file_path = filedialog.askopenfilename()

    if file_path:
        # Load the image using PIL
        image = Image.open(file_path)

        # Resize the image to fit the canvas
        image = image.resize((280, 280))

        # Clear previous content on the canvas
        canvas.delete("all")

        # Convert the image to grayscale
        image_gray = image.convert("L")

        # Resize the grayscale image to 28x28 pixels
        image_gray = image_gray.resize((28, 28))

        # Convert the grayscale image to a numpy array
        image_array = np.array(image_gray)

        # Normalize the image
        image_array = image_array / 255.0

        # Reshape the image array to match the input shape of the model
        image_array = np.reshape(image_array, (1, 28, 28, 1))

        # Make the prediction using the model
        prediction = model.predict(image_array)

        # Get the predicted digit
        digit = np.argmax(prediction)

        # Update the label with the predicted digit
        label.configure(text="Prediction is: " + str(digit))

        # Convert the PIL image to Tkinter format
        tk_image = ImageTk.PhotoImage(image)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor="nw", image=tk_image)

        # Prevent garbage collection of the image
        canvas.image = tk_image


# Create a button to select an image
button = ctk.CTkButton(app, text="Select Image", command=select_image)
button.pack()

# Run the tkinter event loop
app.mainloop()
