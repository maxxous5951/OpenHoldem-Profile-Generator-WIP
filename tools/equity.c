/* Matrice d'equite 169x169 (classes de mains preflop) par Monte Carlo.
   Compile : gcc -O3 -o equity equity.c ; usage : ./equity N_ECHANTILLONS > matrix.txt (169 lignes de 169 valeurs) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static uint64_t s[2] = {0x9E3779B97F4A7C15ULL, 0xD1B54A32D192ED03ULL};
static inline uint64_t rnd(void) {
    uint64_t a = s[0], b = s[1]; s[0] = b; a ^= a << 23; s[1] = a ^ b ^ (a >> 17) ^ (b >> 26); return s[1] + b;
}
/* carte = rang*4 + couleur, rang 0..12 (2..A) */
static uint32_t score7(const int *c) {
    int cnt[13] = {0}; int suit[4] = {0}; uint32_t smask[4] = {0}; uint32_t rmask = 0;
    for (int i = 0; i < 7; i++) { int r = c[i] >> 2, u = c[i] & 3; cnt[r]++; suit[u]++; smask[u] |= 1u << r; rmask |= 1u << r; }
    /* quinte couleur / couleur */
    int fs = -1; for (int u = 0; u < 4; u++) if (suit[u] >= 5) fs = u;
    #define STRAIGHT(m, out) { out = -1; uint32_t mm = (m) | (((m) >> 12) & 1); /* as bas */ \
        uint32_t mm2 = ((m) << 1) | (((m) >> 12) & 1); \
        for (int hi = 12; hi >= 3; hi--) { uint32_t need = 0x1Fu << (hi - 4 + 1); if ((mm2 & need) == need) { out = hi; break; } } (void)mm; }
    if (fs >= 0) {
        int sf; STRAIGHT(smask[fs], sf);
        if (sf >= 0) return (8u << 20) | (uint32_t)sf;
    }
    int quad = -1, trips[2] = {-1, -1}, nt = 0, pairs[3] = {-1, -1, -1}, np = 0;
    for (int r = 12; r >= 0; r--) {
        if (cnt[r] == 4) quad = r; else if (cnt[r] == 3) { if (nt < 2) trips[nt++] = r; } else if (cnt[r] == 2) { if (np < 3) pairs[np++] = r; }
    }
    if (quad >= 0) { int k = -1; for (int r = 12; r >= 0; r--) if (r != quad && cnt[r]) { k = r; break; } return (7u << 20) | (quad << 4) | k; }
    if (nt >= 1 && (nt >= 2 || np >= 1)) { int p = nt >= 2 ? trips[1] : pairs[0]; if (nt >= 2 && np >= 1 && pairs[0] > p) p = pairs[0]; return (6u << 20) | (trips[0] << 4) | p; }
    if (fs >= 0) { uint32_t m = smask[fs]; uint32_t v = 0; int n = 0; for (int r = 12; r >= 0 && n < 5; r--) if (m & (1u << r)) { v = (v << 4) | r; n++; } return (5u << 20) | v; }
    int st; STRAIGHT(rmask, st);
    if (st >= 0) return (4u << 20) | (uint32_t)st;
    if (nt >= 1) { uint32_t v = trips[0]; int n = 0; for (int r = 12; r >= 0 && n < 2; r--) if (cnt[r] == 1) { v = (v << 4) | r; n++; } return (3u << 20) | v; }
    if (np >= 2) { int k = -1; for (int r = 12; r >= 0; r--) if (cnt[r] && r != pairs[0] && r != pairs[1]) { k = r; break; } return (2u << 20) | (pairs[0] << 8) | (pairs[1] << 4) | k; }
    if (np == 1) { uint32_t v = pairs[0]; int n = 0; for (int r = 12; r >= 0 && n < 3; r--) if (cnt[r] == 1) { v = (v << 4) | r; n++; } return (1u << 20) | v; }
    { uint32_t v = 0; int n = 0; for (int r = 12; r >= 0 && n < 5; r--) if (cnt[r]) { v = (v << 4) | r; n++; } return v; }
}

static int rk[169], r1[169], r2[169], su[169];
static void classes(void) {
    int n = 0;
    for (int i = 0; i < 13; i++) for (int j = 0; j < 13; j++) {
        int a = 12 - i, b = 12 - j; /* i = 0 -> A */
        if (i == j) { rk[n] = 0; r1[n] = a; r2[n] = a; su[n] = 0; n++; }
        else if (i < j) { r1[n] = a; r2[n] = b; su[n] = 1; n++; r1[n] = a; r2[n] = b; su[n] = 0; n++; }
    }
}
int main(int argc, char **argv) {
    long N = argc > 1 ? atol(argv[1]) : 20000;
    classes();
    /* ordre de sortie : meme ordre que classes() */
    for (int x = 0; x < 169; x++) {
        for (int y = 0; y < 169; y++) {
            long w = 0, t = 0, done = 0;
            for (long k = 0; k < N * 4 && done < N; k++) {
                int used[52] = {0}; int c[7], d[7];
                int ok = 1;
                /* main x */
                int s1, s2;
                if (su[x]) { s1 = s2 = rnd() & 3; } else { s1 = rnd() & 3; s2 = rnd() & 3; if (r1[x] == r2[x]) { while (s2 == s1) s2 = rnd() & 3; } else if (s1 == s2) s2 = (s2 + 1 + (rnd() % 3)) & 3; }
                if (r1[x] == r2[x] && s1 == s2) continue;
                int a0 = r1[x] * 4 + s1, a1 = r2[x] * 4 + s2;
                if (a0 == a1) continue;
                used[a0] = used[a1] = 1;
                int u1, u2;
                if (su[y]) { u1 = u2 = rnd() & 3; } else { u1 = rnd() & 3; u2 = rnd() & 3; if (r1[y] == r2[y]) { while (u2 == u1) u2 = rnd() & 3; } else if (u1 == u2) u2 = (u2 + 1 + (rnd() % 3)) & 3; }
                int b0 = r1[y] * 4 + u1, b1 = r2[y] * 4 + u2;
                if (b0 == b1 || used[b0] || used[b1]) continue;
                used[b0] = used[b1] = 1;
                int bd[5];
                for (int i = 0; i < 5; i++) { int cd; do { cd = rnd() % 52; } while (used[cd]); used[cd] = 1; bd[i] = cd; }
                c[0] = a0; c[1] = a1; d[0] = b0; d[1] = b1;
                for (int i = 0; i < 5; i++) { c[2 + i] = bd[i]; d[2 + i] = bd[i]; }
                uint32_t sa = score7(c), sb = score7(d);
                if (sa > sb) w++; else if (sa == sb) t++;
                done++; (void)ok;
            }
            printf("%.5f%c", done ? (w + 0.5 * t) / done : 0.5, y == 168 ? '\n' : ' ');
        }
        fflush(stdout);
    }
    return 0;
}
