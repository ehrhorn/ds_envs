import numpy as np

arr1: np.ndarray[np.int64] = np.array([3, 7, 39, -3])  # OK
arr2: np.ndarray[np.int32] = np.array([3, 7, 39, -3])  # Type error
arr3: np.ndarray[np.int32] = np.array([3, 7, 39, -3], dtype=np.int32)  # OK
arr4: np.ndarray[float] = np.array(
    [3, 7, 39, -3], dtype=float
)  # Type error: the type of ndarray can not be just "float"
arr5: np.ndarray[np.float64] = np.array([3, 7, 39, -3], dtype=float)  # OK
