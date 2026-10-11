#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * DOOMSDAY.ELF — Alien Logic Bomb Disarm Module
 * 
 * The binary takes a numeric PIN as input.
 * It applies mathematical transformations (multiply by 3, XOR with 0x5A)
 * and compares against hardcoded expected values.
 * 
 * Correct PIN: 7283
 * 
 * Verification logic:
 *   For each digit character c in the PIN:
 *     transformed = (c * 3) ^ 0x5A
 *   Compare against expected[] array.
 * 
 * Students must reverse the math:
 *   original = (expected[i] ^ 0x5A) / 3
 */

/* Pre-computed expected values for PIN "7283":
 * '7' = 55  -> (55 * 3) ^ 0x5A = 165 ^ 90 = 255  (0xFF)
 * '2' = 50  -> (50 * 3) ^ 0x5A = 150 ^ 90 = 196  (0xC4)
 * '8' = 56  -> (56 * 3) ^ 0x5A = 168 ^ 90 = 242  (0xF2)
 * '3' = 51  -> (51 * 3) ^ 0x5A = 153 ^ 90 = 195  (0xC3)
 */
static const unsigned char expected[] = { 0xFF, 0xC4, 0xF2, 0xC3 };
static const int PIN_LENGTH = 4;

static const char *FLAG = "ALIEN{r3v3rs1ng_s4v3d_34rth}";

int check_pin(const char *input) {
    int i;
    unsigned char transformed;

    if ((int)strlen(input) != PIN_LENGTH) {
        return 0;
    }

    for (i = 0; i < PIN_LENGTH; i++) {
        transformed = ((unsigned char)input[i] * 3) ^ 0x5A;
        if (transformed != expected[i]) {
            return 0;
        }
    }

    return 1;
}

void print_banner(void) {
    printf("\n");
    printf("  ╔══════════════════════════════════════════════╗\n");
    printf("  ║     DOOMSDAY PROTOCOL — LOGIC BOMB v6.6.6   ║\n");
    printf("  ║  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ║\n");
    printf("  ║     STATUS: ARMED — AWAITING DISARM PIN     ║\n");
    printf("  ╚══════════════════════════════════════════════╝\n");
    printf("\n");
}

int main(int argc, char *argv[]) {
    print_banner();

    if (argc != 2) {
        printf("  [ERROR] Usage: %s <4-digit PIN>\n", argv[0]);
        printf("  [INFO]  Enter the correct disarm PIN to neutralize the payload.\n\n");
        return 1;
    }

    printf("  [*] Analyzing PIN: %s\n", argv[1]);
    printf("  [*] Running transformation matrix...\n");
    printf("  [*] Comparing against expected signature...\n\n");

    if (check_pin(argv[1])) {
        printf("  ╔══════════════════════════════════════════════╗\n");
        printf("  ║           ✓ DISARM SUCCESSFUL ✓             ║\n");
        printf("  ║                                              ║\n");
        printf("  ║  Logic bomb neutralized. Earth is safe.      ║\n");
        printf("  ║                                              ║\n");
        printf("  ║  FLAG: %-37s ║\n", FLAG);
        printf("  ╚══════════════════════════════════════════════╝\n\n");
        return 0;
    } else {
        printf("  ╔══════════════════════════════════════════════╗\n");
        printf("  ║           ✗ DISARM FAILED ✗                 ║\n");
        printf("  ║                                              ║\n");
        printf("  ║  Incorrect PIN. Detonation imminent.         ║\n");
        printf("  ║  Analyze the binary to find the algorithm.   ║\n");
        printf("  ╚══════════════════════════════════════════════╝\n\n");
        return 1;
    }
}
