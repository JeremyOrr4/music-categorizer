import numpy as np
import pandas as pd
import os

directory = "/music-categorizer-data/pr-generator"
output_directory = "/music-categorizer-data/lr-generator"
windows_per_slice = 12
num_bands = 20
golden_ratio = 1.618


def create_and_store_lr(filepath, filename): 

    # === Load PR Matrix ===
    try:
        pr_matrix = pd.read_csv(filepath, header=None).values
    except Exception as e:
        print(f"Skipping {filename}: {e}")
        return
    num_windows, num_bins = pr_matrix.shape
    num_slices = num_windows // windows_per_slice

    # === Step 1: Average FFT magnitudes across each slice ===
    sliced_matrix = np.zeros((num_slices, num_bins))
    for i in range(num_slices):
        start = i * windows_per_slice
        end = start + windows_per_slice
        sliced_matrix[i] = np.mean(pr_matrix[start:end], axis=0)

    # === Step 2: Create band edges using golden ratio ===
    powers = np.array([golden_ratio**i for i in range(num_bands)])
    normalized = powers / powers.sum()
    edges = np.round(np.cumsum(normalized) * num_bins).astype(int)
    edges = np.concatenate([[0], edges])
    edges[-1] = num_bins  # make sure we cover all bins

    # === Step 3: Average frequency bins within each band ===
    lr_matrix = np.zeros((num_slices, num_bands))
    for i in range(num_slices):
        for j in range(num_bands):
            start = edges[j]
            end = edges[j+1]
            if end > start:
                lr_matrix[i, j] = np.mean(sliced_matrix[i, start:end])
            else:
                lr_matrix[i, j] = 0.0

    # === Step 4: Save LR Vectors to file ===
    output_path = os.path.join(output_directory, f"lr_{filename}.csv")
    print(f"Saving LR matrix to: {output_path}")
    np.savetxt(output_path, lr_matrix, delimiter=",", fmt="%.6f")


def main():
    print("Starting LR Generator")

    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.endswith('.csv'):
            print(f"Processing file: {filename}")
            filename = filename.replace("pr_", "").replace(".csv", "")
            create_and_store_lr(filepath, filename)
        else:
            continue

    print("Finishing LR Generator")



if __name__ == "__main__":
    main()


