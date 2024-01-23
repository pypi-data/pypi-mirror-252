import numpy as np
from dtl_functions_rd import transpose2d, window1d, convolution2d


"""Examples of running Data Transformation Library dtl_functions_rd."""
"""Example for transpose2d function."""
my_array = transpose2d([[1.5, 2.5, 3.5],
                        [4.5, 5.5, 6.5]])
print(f"Result: {my_array}\n")


"""Example for window1d function."""
input_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]     # list
input_array_2 = np.array((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))     # np.ndarray
size = 3
shift = 3
stride = 1

result = window1d(input_array, size, shift, stride)
print("Result for a list: %s\n" % result)

result2 = window1d(input_array_2, size, shift, stride)
print("Result for an array: %s\n" % result2)


"""Example for convolution2d function."""
input_matrix = np.array([[0, 1, 2],
                         [3, 4, 5],
                         [6, 7, 8]])
kernel = np.array([[0, 1],
                   [2, 3]])
stride = 2
conv2d = convolution2d(input_matrix, kernel, stride)
print(f"Result for 2D convolution: {conv2d}\n")
