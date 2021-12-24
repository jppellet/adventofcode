
/* Horrible, horrible, horrible... just to remind me that I can't code in C! */
#include <stdio.h>

#define N 14
#define N_DIGITS 9


long argsdivz[N] = { 1,  1,  1,  1,  1,  26,  1,  26,  26,  1, 26, 26, 26,  26};
long argsaddx[N] = {10, 12, 10, 12, 11, -16, 10, -11, -13, 13, -8, -1, -4, -14};
long argsaddy[N] = {12,  7,  8,  8, 15,  12,  8,  13,   3, 13,  3,  9,  4,  13};
long digits[N_DIGITS] = {9,8,7,6,5,4,3,2,1};

long checksum(long n) {
    long acc = 0;
    long radix = 10000000000000;
    for (int i = 0; i < N; i++) {
        long digit = n / radix;
        if (digit == 0) {
            return -1;
        }
        n %= radix;
        radix /= 10;

        long x = acc % 26;
        acc = acc / argsdivz[i];
        x += argsaddx[i];
        if (x != digit) {
            acc *= 26;
            acc += digit + argsaddy[i];
        }
    }
    return acc;
}


int main(int argc, char **argv) {
    long i = 0;
    for (int i1 = 0; i1 < N_DIGITS; i1++) {
    long v1 = digits[i1] * 10000000000000;
    for (int i2 = 0; i2 < N_DIGITS; i2++) {
    long v2 = digits[i2] * 1000000000000;
    for (int i3 = 0; i3 < N_DIGITS; i3++) {
    long v3 = digits[i3] * 100000000000;
    for (int i4 = 0; i4 < N_DIGITS; i4++) {
    long v4 = digits[i4] * 10000000000;
    for (int i5 = 0; i5 < N_DIGITS; i5++) {
    long v5 = digits[i5] * 1000000000;
    for (int i6 = 0; i6 < N_DIGITS; i6++) {
    long v6 = digits[i6] * 100000000;
    for (int i7 = 0; i7 < N_DIGITS; i7++) {
    long v7 = digits[i7] * 10000000;
    for (int i8 = 0; i8 < N_DIGITS; i8++) {
    long v8 = digits[i8] * 1000000;
    for (int i9 = 0; i9 < N_DIGITS; i9++) {
    long v9 = digits[i9] * 100000;
    for (int i10 = 0; i10 < N_DIGITS; i10++) {
    long v10 = digits[i10] * 10000;
    for (int i11 = 0; i11 < N_DIGITS; i11++) {
    long v11 = digits[i11] * 1000;
    for (int i12 = 0; i12 < N_DIGITS; i12++) {
    long v12 = digits[i12] * 100;
    for (int i13 = 0; i13 < N_DIGITS; i13++) {
    long v13 = digits[i13] * 10;
    for (int i14 = 0; i14 < N_DIGITS; i14++) {
    long v14 = digits[i14];

        long v = v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + v9 + v10 + v11 + v12 + v13 + v14;
        i++;
        
        long acc = checksum(v);
        if (i % 10000000 == 0) {
            printf("%ld -> %ld\n", v, acc);
        }
        if (acc == 0) {
            printf(" >> works: %lu\n", v);
            return 0;
        }

    }}}}}}}}}}}}}}

    printf("finished");
}