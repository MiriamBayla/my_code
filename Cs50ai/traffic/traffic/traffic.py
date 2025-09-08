import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    # Lists of images and labels (0-42)
    images = []
    labels = []

    # For each sign (42 of them)
    for sign in range(NUM_CATEGORIES):
        # make this path the directory's path + this sign's path
        this_signs_path = os.path.join(data_dir, str(sign))

        # If no such path exists - continue
        if not os.path.isdir(this_signs_path):
            continue

        # For each pic of a given type of sign
        for sign_example in os.listdir(this_signs_path):
            # Make file path be the sign's path + this specific pic's path
            file_path = os.path.join(this_signs_path, sign_example)

            # This is the pic
            image = cv2.imread(file_path)

            if image is None:
                continue

            # Resize image to be correct size
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

            # Add the current image and label to the lists
            images.append(image)
            labels.append(sign)

    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = tf.keras.models.Sequential()

    # First convolutional layer
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu',
              input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))

    # First pooling layer
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Second convolutional layer
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))

    # Second pooling layer
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Third convolutional layer
    model.add(tf.keras.layers.Conv2D(128, (3, 3), activation='relu'))

    # Third pooling layer
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Flatten
    model.add(tf.keras.layers.Flatten())

    # Final connected layer
    model.add(tf.keras.layers.Dense(128, activation='relu'))

    # Dropout to prevent overfitting
    model.add(tf.keras.layers.Dropout(0.5))

    # Output layer with 43 categories with set probabilities (which add up to 1)
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax'))

    # Compile the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


if __name__ == "__main__":
    main()
