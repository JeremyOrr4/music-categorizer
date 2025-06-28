#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <fftw3.h>

int ends_with_raw(const char *filename) {
    size_t len = strlen(filename);
    return len >= 4 && strcmp(filename + len - 4, ".raw") == 0;
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
            printf("Found .raw file: %s\n", entry->d_name);
        }
    }

    closedir(dir);
    return 0;
}
