import numpy as np
from numba import njit

@njit
def min_vertical_seam_energy(energies):
    height, width = energies.shape
    seam_energies = np.zeros((height, width))
    back_pointers = np.zeros((height, width), dtype=np.int32)

    seam_energies[0] = energies[0]

    for y in range(1, height):
        for x in range(width):
            x_left = max(x - 1, 0)
            x_right = min(x + 1, width - 1)
            min_parent_x = x_left + np.argmin(seam_energies[y - 1, x_left:x_right + 1])

            seam_energies[y, x] = energies[y, x] + seam_energies[y - 1, min_parent_x]
            back_pointers[y, x] = min_parent_x

    min_energy = np.min(seam_energies[-1])
    return min_energy

@njit
def find_vertical_seam(energies):
    height, width = energies.shape
    seam_energies = np.zeros((height, width))
    back_pointers = np.zeros((height, width), dtype=np.int32)

    seam_energies[0] = energies[0]

    for y in range(1, height):
        for x in range(width):
            x_left = max(x - 1, 0)
            x_right = min(x + 1, width - 1)
            min_parent_x = x_left + np.argmin(seam_energies[y - 1, x_left:x_right + 1])

            seam_energies[y, x] = energies[y, x] + seam_energies[y - 1, min_parent_x]
            back_pointers[y, x] = min_parent_x

    min_seam_end_x = np.argmin(seam_energies[-1])
    seam = []

    seam_point_x = min_seam_end_x
    for y in range(height - 1, -1, -1):
        seam.append((seam_point_x, y))
        seam_point_x = back_pointers[y, seam_point_x]

    seam.reverse()
    return seam

def carve_seam(magnitude, phase, seam_path):
    height, width = magnitude.shape
    mask = np.ones((height, width), dtype=bool)
    for x, y in seam_path:
        mask[y, x] = False
    new_magnitude = magnitude[mask].reshape((height, width - 1))
    new_phase = phase[mask].reshape((height, width - 1))
    return new_magnitude, new_phase

def carve_audio(n_of_seams, magnitude, phase, is_vertical=True):
    original_height, original_width = magnitude.shape
    if is_vertical:
        for _ in range(n_of_seams):
            seam_path = find_vertical_seam(magnitude)
            magnitude, phase = carve_seam(magnitude, phase, seam_path)
    else:
        magnitude = np.rot90(magnitude, k=-1)
        phase = np.rot90(phase, k=-1)
        for _ in range(n_of_seams):
            seam_path = find_vertical_seam(magnitude)
            magnitude, phase = carve_seam(magnitude, phase, seam_path)
        magnitude = np.rot90(magnitude, k=1)
        phase = np.rot90(phase, k=1)

        new_height, new_width = magnitude.shape
        if new_height < original_height:
            pad_height = original_height - new_height
            magnitude = np.pad(magnitude, ((0, pad_height), (0, 0)), mode='constant')
            phase = np.pad(phase, ((0, pad_height), (0, 0)), mode='constant')

    return magnitude, phase