# Final version with fixed fft_bins scope and compatibility handling

import numpy as np
import pandas as pd
import os

# Parameters
directory = "/music-categorizer-data/pr-generator"
output_directory = "/music-categorizer-data/lr-generator"
windows_per_slice = 12
num_bands = 20
DEFAULT_FFT_BINS = 513
sampling_rate = 44100
nyquist_freq = sampling_rate / 2

# Golden ratio for frequency spacing
golden_ratio = 1.618

def compute_golden_ratio_edges(num_bands, nyquist_freq, fft_bins):
    freqs = [0]
    f = 50
    while f < nyquist_freq:
        freqs.append(f)
        f *= golden_ratio
    freqs.append(nyquist_freq)
    freqs = np.array(freqs)

    if len(freqs) - 1 < num_bands:
        freqs = np.interp(np.linspace(0, len(freqs) - 1, num_bands + 1), np.arange(len(freqs)), freqs)

    bin_edges = np.round((freqs / nyquist_freq) * fft_bins).astype(int)
    bin_edges[0] = 0
    bin_edges[-1] = fft_bins
    return bin_edges[:num_bands + 1]

def create_and_store_lr(filepath, filename):
    try:
        pr_matrix = pd.read_csv(filepath, header=None).values
    except Exception as e:
        print(f"Skipping {filename}: {e}")
        return

    num_windows, num_bins = pr_matrix.shape

    fft_bins = DEFAULT_FFT_BINS  # ensure this is always defined

    if num_bins != fft_bins:
        print(f"Warning: {filename} has {num_bins} bins, expected {fft_bins}. Adjusting to use min(num_bins, fft_bins).")
        fft_bins = min(num_bins, fft_bins)
        pr_matrix = pr_matrix[:, :fft_bins]
        num_bins = fft_bins

    num_slices = num_windows // windows_per_slice
    if num_slices == 0:
        print(f"Not enough data in {filename} for even one slice.")
        return

    sliced_matrix = np.array([
        np.mean(pr_matrix[i * windows_per_slice : (i + 1) * windows_per_slice], axis=0)
        for i in range(num_slices)
    ])

    edges = compute_golden_ratio_edges(num_bands, nyquist_freq, fft_bins)

    lr_matrix = np.zeros((num_slices, num_bands))
    for i in range(num_slices):
        for j in range(num_bands):
            start, end = edges[j], edges[j + 1]
            if end > start:
                lr_matrix[i, j] = np.mean(sliced_matrix[i, start:end])
            else:
                lr_matrix[i, j] = 0.0

    output_path = os.path.join(output_directory, f"lr_{filename}.csv")
    os.makedirs(output_directory, exist_ok=True)
    print(f"Saving LR matrix to: {output_path}")
    np.savetxt(output_path, lr_matrix, delimiter=",", fmt="%.6f")

def main():
    print("Starting LR Generator")
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.endswith('.csv'):
            base = filename.replace("pr_", "").replace(".csv", "")
            print(f"Processing: {filename}")
            create_and_store_lr(filepath, base)
    print("Finished LR Generation")

if __name__ == "__main__":
    main()
