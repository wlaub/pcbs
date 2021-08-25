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

//Knob deadzones

int freq = 10e6;
int half = 2048;
int zero = half / 16;

//Poly modes

#define POLY_HOLD_TIME 5000000 // 5 seconds in microseconds

#define POLY_LENGTH_LOCK 0
#define POLY_POLYPHONY 1
#define POLY_RESET 5

//Global knob values

volatile int voct_oct;
volatile float semi;
volatile float fine;
volatile float voct_atv_value;
volatile int freq_lock;
volatile int poly;
volatile int poly_oct;
volatile float poly_oct_val;

volatile float voct = 0;

//Global LFSR configuration

volatile unsigned short actual_len;

volatile unsigned char lfsr_en0 = 1;
volatile unsigned char lfsr_en1 = 0;

#endif
