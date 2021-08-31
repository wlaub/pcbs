#ifndef PINMAP_H
#define PINMAP_H

#pragma once

const uint8_t pin_to_channel[] = { // pg 482
        7,      // 0/A0  AD_B1_02
        8,      // 1/A1  AD_B1_03
        12,     // 2/A2  AD_B1_07
        11,     // 3/A3  AD_B1_06
        6,      // 4/A4  AD_B1_01
        5,      // 5/A5  AD_B1_00
        15,     // 6/A6  AD_B1_10
        0,      // 7/A7  AD_B1_11
        13,     // 8/A8  AD_B1_08
        14,     // 9/A9  AD_B1_09
#if 0
        128,    // 10
        128,    // 11
        128,    // 12
        128,    // 13
#else
        1,      // 24/A10 AD_B0_12 
        2,      // 25/A11 AD_B0_13
        128+3,  // 26/A12 AD_B1_14 - only on ADC2, 3
        128+4,  // 27/A13 AD_B1_15 - only on ADC2, 4
#endif
        7,      // 14/A0  AD_B1_02
        8,      // 15/A1  AD_B1_03
        12,     // 16/A2  AD_B1_07
        11,     // 17/A3  AD_B1_06
        6,      // 18/A4  AD_B1_01
        5,      // 19/A5  AD_B1_00
        15,     // 20/A6  AD_B1_10
        0,      // 21/A7  AD_B1_11
        13,     // 22/A8  AD_B1_08
        14,     // 23/A9  AD_B1_09
        1,      // 24/A10 AD_B0_12
        2,      // 25/A11 AD_B0_13
        128+3,  // 26/A12 AD_B1_14 - only on ADC2, 3
        128+4   // 27/A13 AD_B1_15 - only on ADC2, 4
};

const int poly_count = 6;
float poly_maps[poly_count] = {1, 1.2, 1.25, 1.333, 1.5, 1.667};

int clk_pin_0 = 0; //The LFSR Clocks
int clk_pin_1 = 1;

int lfsr0_in_pin = 7; //XOR'd with the LFSR feedback
int lfsr1_in_pin = 6;

//int glitch_pin = 31; //Moved to expander
int freq_lock_pin = 13;  
int glitch_en_pin = 23;
//int ext_clk_en_pin = 30; //Moved to expander

int poly_sw_pin = 8;

int lfo_led_pin  = 9;
int led0_pin = 10;
int led1_pin = 11;
int led2_pin = 12;

int voct_fine_pin = A0; 
int voct_atv_pin = A3;
int voct_cv_pin = A2;
int param_0_cv_pin = A4;
int lfo_pin = A6;
int len_cv_pin = A5;
int param_1_pin = A7;
int len_knob_pin = A8;
int param_0_pin = A1;

//For extracting pins/encoders from expander register value
#define SEMI_ENCODER(x) ((x>>5)&3)
#define POLY_ENCODER(x) ((x>>7)&3)
#define OCT_ENCODER(x) ((x>>9)&3)

  
#endif
