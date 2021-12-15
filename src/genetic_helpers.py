import numpy as np

"""
Helper Functions
"""


def bool_to_np(board):
    f = lambda x: 1 if x == True else 0
    return np.asarray([[f(j) for j in i] for i in board])


def get_peaks(area):
    #
    peaks = np.array([])
    for col in range(area.shape[1]):
        if 1 in area[:, col]:
            p = area.shape[0] - np.argmax(area[:, col], axis=0)
            peaks = np.append(peaks, p)
        else:
            peaks = np.append(peaks, 0)
    return peaks


def get_row_transition(area, highest_peak):
    sum = 0
    # From highest peak to bottom
    for row in range(int(area.shape[0] - highest_peak), area.shape[0]):
        for col in range(1, area.shape[1]):
            if area[row, col] != area[row, col - 1]:
                sum += 1
    return sum


def get_col_transition(area, peaks):
    sum = 0
    for col in range(area.shape[1]):
        if peaks[col] <= 1:
            continue
        for row in range(int(area.shape[0] - peaks[col]), area.shape[0] - 1):
            if area[row, col] != area[row + 1, col]:
                sum += 1
    return sum


def get_bumpiness(peaks):
    s = 0
    for i in range(9):
        s += np.abs(peaks[i] - peaks[i + 1])
    return s


def get_holes(peaks, area):
    # Count from peaks to bottom
    holes = []
    for col in range(area.shape[1]):
        start = -peaks[col]
        # If there's no holes i.e. no blocks on that column
        if start == 0:
            holes.append(0)
        else:
            holes.append(np.count_nonzero(area[int(start) :, col] == 0))
    return holes


def get_wells(peaks):
    wells = []
    for i in range(len(peaks)):
        if i == 0:
            w = peaks[1] - peaks[0]
            w = w if w > 0 else 0
            wells.append(w)
        elif i == len(peaks) - 1:
            w = peaks[-2] - peaks[-1]
            w = w if w > 0 else 0
            wells.append(w)
        else:
            w1 = peaks[i - 1] - peaks[i]
            w2 = peaks[i + 1] - peaks[i]
            w1 = w1 if w1 > 0 else 0
            w2 = w2 if w2 > 0 else 0
            w = w1 if w1 >= w2 else w2
            wells.append(w)
    return wells
