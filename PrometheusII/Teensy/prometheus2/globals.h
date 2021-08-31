#ifndef GLOBALS_H
#define GLOBALS_H

#pragma once

//main loop period in us
//200 = 5 kHz
#define LOOP_PERIOD 100

//length of a glitch in main loop cycles
#define GLITCH_LEN 10000/LOOP_PERIOD

//blink duration in main loop cycles
#define BLINK_RATE 2000

//Option to detune lfsr1 from lfsr0 by rounding
#define DETUNE_LFSR1

//FM configuration
#define FM_SCALE 2
#define FM_HALF_SCALE (0.5/12)

//Knob deadzones

int freq = 10e6;
int half = 2048;
int zero = half / 16;

//Poly modes

#define POLY_HOLD_TIME 5000000 // 5 seconds in microseconds

#define POLY_LENGTH_LOCK 0
#define POLY_POLYPHONY 1
#define POLY_CAL 2
#define POLY_RESET 5

//Configurations

struct PitchConfig 
{
  signed char octave = 0;
  signed char semitone = 0;
  unsigned char enabled = 0;
};

volatile struct PitchConfig main_pitch;
volatile struct PitchConfig aux_pitch;

//Global knob values

//volatile int voct_oct;

volatile float fine;
volatile float voct_atv_value;
volatile int freq_lock;

volatile float voct = 0;

//Global LFSR configuration

volatile unsigned short actual_len;


#endif
