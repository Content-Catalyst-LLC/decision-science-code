// bounded_search_core.c
// Compile with: cc bounded_search_core.c -o bounded_search_core

#include <stdio.h>

int first_satisficing(const double values[], int n, double aspiration) {
    for (int i = 0; i < n; i++) {
        if (values[i] >= aspiration) {
            return i + 1;
        }
    }
    return -1;
}

int main(void) {
    double values[] = {0.58, 0.71, 0.82, 0.77, 0.91};
    int index = first_satisficing(values, 5, 0.75);
    printf("Satisficing option: %d\n", index);
    return 0;
}
