#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <fftw3.h>
#include <math.h>

#define N 1024          // FFT window size
#define MAX_WINDOWS 10000  // Adjust as needed

int ends_with_raw(const char *filename) {
    size_t len = strlen(filename);
    return len >= 4 && strcmp(filename + len - 4, ".raw") == 0;
}

void fourier_transform_windows(const char *filepath, const short *samples, int num_samples) {
    fftw_complex out[N / 2 + 1];
    fftw_plan plan;
    double in[N];

    int num_windows = num_samples / N;
    if (num_windows > MAX_WINDOWS) num_windows = MAX_WINDOWS;

    // Allocate matrix for magnitude values: [time][frequency]
    double **matrix = malloc(num_windows * sizeof(double *));
    for (int t = 0; t < num_windows; t++) {
        matrix[t] = malloc((N / 2 + 1) * sizeof(double));
    }

    plan = fftw_plan_dft_r2c_1d(N, in, out, FFTW_ESTIMATE);

    for (int t = 0; t < num_windows; t++) {
        int offset = t * N;
        for (int i = 0; i < N; i++) {
            in[i] = (double)samples[offset + i] / 32768.0;
        }

        fftw_execute(plan);

        for (int f = 0; f <= N / 2; f++) {
            matrix[t][f] = sqrt(out[f][0] * out[f][0] + out[f][1] * out[f][1]);
        }
    }

    printf("File: %s\n", filepath);
    for (int t = 0; t < num_windows; t++) {
        printf("Time Window %d: ", t);
        for (int f = 0; f <= N / 2; f++) {
            printf("%.4f ", matrix[t][f]);
        }
        printf("\n");
    }

    // Cleanup
    for (int t = 0; t < num_windows; t++) {
        free(matrix[t]);
    }
    free(matrix);
    fftw_destroy_plan(plan);
}

int main(int argc, char *argv[]) {
    const char *dir_path = "/music-categorizer-data/pcm_encoder";
    DIR *dir = opendir(dir_path);
    if (dir == NULL) {
        perror("opendir failed");
        return 1;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (ends_with_raw(entry->d_name)) {
            char filepath[1024];
            snprintf(filepath, sizeof(filepath), "%s/%s", dir_path, entry->d_name);

            FILE *f = fopen(filepath, "rb");
            if (!f) continue;

            fseek(f, 0, SEEK_END);
            long size = ftell(f);
            fseek(f, 0, SEEK_SET);

            if (size < N * sizeof(short)) {
                fclose(f);
                continue;
            }

            void *buffer = malloc(size);
            if (buffer && size > 0) {
                fread(buffer, 1, size, f);
                int num_samples = size / sizeof(short);
                fourier_transform_windows(filepath, (short *)buffer, num_samples);
            }

            free(buffer);
            fclose(f);
        }
    }

    closedir(dir);
    return 0;
}
