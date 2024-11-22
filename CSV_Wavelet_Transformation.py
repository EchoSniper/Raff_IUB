import pandas as pd
import numpy as np
import pywt
import matplotlib.pyplot as plt

# Load data from CSV files
# Assuming each CSV file contains a column of current data (e.g., for phase A, B, C, and G)
currentA = pd.read_csv('current1.csv', header=None).values.flatten()  # Data for Phase A
currentB = pd.read_csv('current2.csv', header=None).values.flatten()  # Data for Phase B
currentC = pd.read_csv('current3.csv', header=None).values.flatten()  # Data for Phase C
currentG = pd.read_csv('current4.csv', header=None).values.flatten()  # Data for Ground (G)

# Define wavelet transformation function
def apply_wavelet_transformation(data, wavelet='db4', level=1):
    # Apply the wavelet transformation
    coeffs = pywt.wavedec(data, wavelet, level=level)
    # Return only Level 1 coefficients (Detail coefficients, not approximation)
    return coeffs[1]

# Apply wavelet transformation for each phase (only Level 1 detail coefficients)
coeffsA = apply_wavelet_transformation(currentA)
coeffsB = apply_wavelet_transformation(currentB)
coeffsC = apply_wavelet_transformation(currentC)
coeffsG = apply_wavelet_transformation(currentG)

# Plot wavelet transformation results (Level 1 details only)
fig, axs = plt.subplots(4, 1, figsize=(10, 8))

# Wavelet coefficients for Level 1 (Detail Coefficients)
axs[0].plot(coeffsA)
axs[0].set_title("Level 1 Detail Coefficients for Phase A")
axs[1].plot(coeffsB)
axs[1].set_title("Level 1 Detail Coefficients for Phase B")
axs[2].plot(coeffsC)
axs[2].set_title("Level 1 Detail Coefficients for Phase C")
axs[3].plot(coeffsG)
axs[3].set_title("Level 1 Detail Coefficients for Ground (G)")

plt.tight_layout()
plt.show()

# Calculate the maximum values of the Level 1 coefficients
maxA = np.max(coeffsA)  # Maximum value of Phase A Level 1 coefficients
maxB = np.max(coeffsB)  # Maximum value of Phase B Level 1 coefficients
maxC = np.max(coeffsC)  # Maximum value of Phase C Level 1 coefficients
maxG = np.max(coeffsG)  # Maximum value of Ground Level 1 coefficients

# Print the maximum values of the Level 1 coefficients
print(f"The maximum value for Phase A Level 1 coefficients is: {maxA}")
print(f"The maximum value for Phase B Level 1 coefficients is: {maxB}")
print(f"The maximum value for Phase C Level 1 coefficients is: {maxC}")
print(f"The maximum value for Ground Level 1 coefficients is: {maxG}")

# Define threshold values for fault detection
constant = 200
neu = 0.5

# Fault detection based on the maximum values of the coefficients
if maxA > constant:
    if maxB > constant:
        if maxC > constant:
            if maxG > neu:
                print("Three Phase to Ground Fault is Detected")
        if maxG < neu:
            print("Three Phase Fault is Detected")
    elif maxB < constant:
        if maxC > constant:
            if maxG > neu:
                print("Double Line to Ground Fault (AC-G) is Detected")
        if maxG < neu:
            print("Line to Line Fault Between Phase A and C is Detected")
elif maxA < constant:
    if maxB > constant:
        if maxC > constant:
            if maxG > neu:
                print("Double Line to Ground Fault (BC-G) is Detected")
        if maxG < neu:
            print("Line to Line Fault Between Phase B and C is Detected")
    elif maxB < constant:
        if maxC < constant:
            if maxG < neu:
                print("No Fault is Detected. System is Normal")

# You can also print normalized coefficients for additional comparison if needed
normA = (coeffsA - np.min(coeffsA)) / (np.max(coeffsA) - np.min(coeffsA))
normB = (coeffsB - np.min(coeffsB)) / (np.max(coeffsB) - np.min(coeffsB))
normC = (coeffsC - np.min(coeffsC)) / (np.max(coeffsC) - np.min(coeffsC))
normG = (coeffsG - np.min(coeffsG)) / (np.max(coeffsG) - np.min(coeffsG))

# You can also plot the normalized coefficients if you wish
fig_norm, axs_norm = plt.subplots(4, 1, figsize=(10, 8))
axs_norm[0].plot(normA)
axs_norm[0].set_title("Normalized Phase A Coefficients")
axs_norm[1].plot(normB)
axs_norm[1].set_title("Normalized Phase B Coefficients")
axs_norm[2].plot(normC)
axs_norm[2].set_title("Normalized Phase C Coefficients")
axs_norm[3].plot(normG)
axs_norm[3].set_title("Normalized Ground Coefficients")

plt.tight_layout()
plt.show()

