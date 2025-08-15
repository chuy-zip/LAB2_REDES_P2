#include "viterbi.h"

#include <iostream>
#include <string>
#include <vector>

std::string viterbi(std::string input) {
    std::string output;
    int shift_register[3] = {0, 0, 0}; // bit0: actual, bit1: anterior, bit2: anterior del anterior

    for (char bit_char : input) {
        int bit = bit_char - '0';

        shift_register[2] = shift_register[1];
        shift_register[1] = shift_register[0];
        shift_register[0] = bit;

        int out1 = shift_register[0] ^ shift_register[1] ^ shift_register[2];  // g1 = 111
        int out2 = shift_register[0] ^ shift_register[2];                      // g2 = 101

        output += std::to_string(out1);
        output += std::to_string(out2);
    }

    return output;
}