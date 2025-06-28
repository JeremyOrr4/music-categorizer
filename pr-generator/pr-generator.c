#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <fftw3.h>
#include <math.h>

#define N 1024

int ends_with_raw(const char *filename) {
    size_t len = strlen(filename);
    return len >= 4 && strcmp(filename + len - 4, ".raw") == 0;
}

void fourier_transform(const char *filepath, const void *buffer, size_t size) {
    double in[N];
    fftw_complex out[N/2 + 1];
    fftw_plan plan;

    const short *samples = (const short *)buffer;
    int num_samples = size / sizeof(short);

    // Fill input with up to N samples, zero-pad if needed
    for (int i = 0; i < N; i++) {
        if (i < num_samples) {
            in[i] = (double)samples[i] / 32768.0; // normalize to [-1, 1]
        } else {
            in[i] = 0.0;
        }
    }

    plan = fftw_plan_dft_r2c_1d(N, in, out, FFTW_ESTIMATE);
    fftw_execute(plan);

    printf("File: %s\n", filepath);
    for (int i = 0; i <= N/2; i++) {
        double mag = sqrt(out[i][0]*out[i][0] + out[i][1]*out[i][1]);
        printf("Bin %d: Magnitude = %f\n", i, mag);
    }
    printf("\n");

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

            // Open and read file contents
            FILE *f = fopen(filepath, "rb");
            if (!f) continue;
            fseek(f, 0, SEEK_END);
            long size = ftell(f);
            fseek(f, 0, SEEK_SET);
            void *buffer = malloc(size);
            if (buffer && size > 0) {
                fread(buffer, 1, size, f);
                fourier_transform(filepath, buffer, size);
            }

            fclose(f);
        }
    }

    closedir(dir);
    return 0;
}
