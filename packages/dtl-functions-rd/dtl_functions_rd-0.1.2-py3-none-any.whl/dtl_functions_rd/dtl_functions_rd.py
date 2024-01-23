import numpy as np


def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    Transposes the input matrix into a new matrix
    with the same dimensions as the input matrix
    but will make the column values into row values.

    :param input_matrix: input matrix as a list of a list of floats
    :return: transposed matrix as a list

    Example:
    my_array = ([[1.5, 2.5, 3.5], [4.5, 5.5, 6.5]])

    Result:
    [[1.5, 4.5], [2.5, 5.5], [3.5, 6.5]]

    For context:
    https://numpy.org/doc/stable/reference/generated/numpy.transpose.html
    """

    transposed_matrix = [[input_matrix[j][i] for j in range(len(input_matrix))]
                         for i in range(len(input_matrix[0]))]

    return transposed_matrix


def window1d(
        input_array: list | np.ndarray,
        size: int,
        shift: int = 1,
        stride: int = 1) -> list[list | np.ndarray]:
    """
    Returns a list of windows (1D arrays) of set parameters.

    :param input_array: a list of integers or 1D numpy arrays.
    :param size: determines the amount of elements of the input to be contained in the window.
    :param shift: the number of input elements to shift between the start of each window. Default is 1.
    :param stride: determines the stride (step) between input elements within a window
    :return: windows of input array

    Example:
    input_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]     # list
    input_array = np.array((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))     # np.ndarray
    size = 3
    shift = 3
    stride = 1

    Result:
    for a list: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for np.ndarray: [array([1, 2, 3]), array([4, 5, 6]), array([7, 8, 9])]

    For context:
    https://se.mathworks.com/help/econ/rolling-window-estimation-of-state-space-models.html
    https://www.tensorflow.org/api_docs/python/tf/data/Dataset#window
    https://www.techbeamers.com/python-range-function/
    """

    windows = []
    input_len = len(input_array)
    end_index = input_len - size + 1

    for i in range(0, end_index, shift):    # start, stop, step
        window = input_array[i:i + size:stride]
        windows.append(window)

    return windows


def convolution2d(input_matrix: np.ndarray,
                  kernel: np.ndarray,
                  stride: int = 1) -> np.ndarray:
    """
    Applies a 2D convolution over an input matrix composed of several input planes.

    :param input_matrix: an array of shape (x, y)
    :param kernel: a filtering array of shape (h, w)
    :param stride: the stride of the convolving kernel. Can be a single number or a tuple (sH, sW). Default: 1
    :return: 2D convoluted array

    Example:
    input_matrix = np.array([[0, 1, 2],
                             [3, 4, 5],
                             [6, 7, 8]])
    kernel = np.array([[0, 1],
                       [2, 3]])

    Result:
    [[19. 25.]
     [37. 43.]]

    For context:
    https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html
    https://www.deeplearningbook.org/contents/convnets.html
    https://pytorch.org/docs/stable/generated/torch.nn.functional.conv2d.html#torch.nn.functional.conv2d
    """

    h, w = kernel.shape
    y, x = input_matrix.shape

    if input_matrix.shape[0] < kernel.shape[0] or input_matrix.shape[1] < kernel.shape[1]:
        raise ValueError("Kernel size must be smaller than the input matrix.")

    x = int(((x - h + 1) / stride) + 1)
    y = int(((y - w + 1) / stride) + 1)
    out_image = np.zeros((x, y))

    for i in range(out_image.shape[0]):
        for j in range(out_image.shape[1]):
            out_image[i, j] = np.sum(input_matrix[i:i + h, j:j + w] * kernel)

    return out_image
