# Data Transformation Library

## About

This project is an exercise primarily focused on building Python libraries, publishing packages to PyPI and dependency management using Poetry.

The task is to implement three data transformation functions:
* **Transpose** - flipping of the input matrix diagonally, meaning that the row and column indices of a matrix are switched and a new matrix is produced.
* **Time Series Windowing** - producing lists or numpy arrays containing a subset of elements of the input list or numpy array. The size of the window is defined by passing size, stride and shift parameters. Time series windowing is used for making informed decisions in economics, climate, epidemiology and many other fields.
* **Cross-Correlation (Convolution)** - used in convolutional neural networks in machine learning libraries. Cross-correlation and convolution are both operations applied to images. Cross-correlation means sliding a kernel (filter) across an image. Convolution means sliding a flipped kernel across an image. In practice using one over the other does not change the result, just the resulting values are learned in a flipped orientation. 2D Convolutions are essential in the advancement of convolutional neural networks and various image processing filters such as blurring, sharpening, edge detection, and others.

Functions were built using Python and Numpy (as per requirements of this task). Having the knowledge of how to build such functions by yourself provides the flexibility in ones specific uses cases, as some times the already built functions in various libraries (PyTorch, cv2, etc.) have constraints and changing them can be difficult or even impossible and impractical.

For package management we were required to use Poetry.

## Libraries Used

For this project only Python's **standard library** as well as **Numpy** (were it was required) were used.


For package management **Poetry** was used.

## How to Use

As this project is an exercise on building Python libraries, the built library can be installed from PyPI, were it is being published.

To do so in the terminal window type `pip install dtl_functions_rd`. After the library is installed, open the `main.py` file that is located in the main project directory to see a few examples on how to use the functions of this data transformation library.


## Possible Future Improvements

* Version handling