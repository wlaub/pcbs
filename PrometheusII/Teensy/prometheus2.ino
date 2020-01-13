#include "lookup.h"

#define GLITCH_LEN 1

int taps_maps [12]= {0,1,2,3,4,5,6,7,8,9,10,11};
float poly_maps[8] = {0, 1, 1.2, 1.25, 1.333, 1.5, 1.5, 2};

int clk_pin_0 = 12;
int clk_pin_1 = 13;

int lfsr0_in_pin=32;
int lfsr1_in_pin=33;

int glitch_pin = 31;
int freq_lock_pin = 29;
int glitch_en_pin = 27;
int ext_clk_en_pin = 30;

int lfo_led_pin  = 26;
int taps_led_pin = 28;

int voct_semi_pin = A10;
int voct_fine_pin = A0;
int voct_atv_pin = A1;
int voct_cv_pin = A2;
int param_0_cv_pin = A3;
int lfo_pin = A4;
int len_cv_pin = A5;
int poly_pin = A6;
int param_1_pin = A7;
int voct_oct_pin = A8;
int len_knob_pin = A9;
int param_0_pin = A11;

int lfo_counter = 0;

int glitch_counter = 0;

void init_taps()
{
  for(int i = 0; i < 12; ++i)
  {
    pinMode(taps_maps[i], OUTPUT);
    digitalWrite(taps_maps[i], 0);
  }  
}

void set_taps(int taps)
{
  for(int i = 0; i < 12; ++i)
  {
    digitalWrite(taps_maps[i], (taps&1));
    taps >>=1;
  }
}

#define INIT_OUTPUT(pin, value)\
    pinMode(pin, OUTPUT);\
    digitalWrite(pin, value);

void setup() {
  // put your setup code here, to run once:
  analogWriteFrequency(clk_pin_0, 100e3);
  analogWriteFrequency(clk_pin_1, 100e3);
  analogWriteResolution(2);
  analogWrite(clk_pin_0, 2);
  pinMode(lfsr0_in_pin, OUTPUT);
  pinMode(lfsr1_in_pin, OUTPUT);
  digitalWrite(lfsr0_in_pin, 1);
  digitalWrite(lfsr1_in_pin, 1);

  INIT_OUTPUT(taps_led_pin, 0)
  INIT_OUTPUT(lfo_led_pin, 0)

  pinMode(glitch_en_pin, INPUT);
  pinMode(glitch_pin, INPUT);
  pinMode(freq_lock_pin, INPUT);
  pinMode(ext_clk_en_pin, INPUT);
  
  init_taps();
  set_taps(0x800);
  analogReadResolution(12);
  *(int*)(0x400C4044)|=0xC000; //Set ADC to max averaging mode
  *(int*)(0x400C8044)|=0xC000; //Set ADC to max averaging mode
  Serial.begin(38400);
}


int freq = 10e6;
int taps = 0;
int half = 2048;

void loop() {
  // put your main code here, to run repeatedly:
  delay(10);
  float voct = 0;
  int voct_semi;
  int voct_fine;
  int voct_cv;
  int voct_oct;
  int voct_atv;
  voct_semi = analogRead(voct_semi_pin);
  voct_fine = analogRead(voct_fine_pin);
  voct_cv = analogRead(voct_cv_pin);
  voct_atv = analogRead(voct_atv_pin);
  voct_oct = analogRead(voct_oct_pin);

  int param_0;
  int param_0_cv;
  int param_1;
  param_0 = analogRead(param_0_pin);
  param_0_cv = analogRead(param_0_cv_pin);
  param_1 = analogRead(param_1_pin);

  int len_knob;
  int len_cv;
  len_knob = analogRead(len_knob_pin);
  len_cv = analogRead(len_cv_pin);

  int poly;
  int lfo;
  poly = analogRead(poly_pin);
  lfo = analogRead(lfo_pin);

  int zero = half/16;

  int new_taps;

  //new_taps = voct_semi&0xaa8;
  
  lfo_counter += 1;
  if(lfo_counter > lfo+4)
  {
    lfo_counter = 0;
    glitch_counter = GLITCH_LEN;
  }
  if(lfo_counter < 4)
  {
    digitalWrite(lfo_led_pin,0);
  }
  else
  {
    digitalWrite(lfo_led_pin,1);
  }

  unsigned short len = short(pow(2,1+float(len_knob)*11/4000));  
  unsigned short actual_len;
  if (len > 4095)
  {
    len = 4095;
    digitalWrite(lfsr1_in_pin, 0);
  }
  if(glitch_counter > 0)
  {
    len = 4095;
    digitalWrite(lfsr1_in_pin, 1);
    glitch_counter -= 1;
  }
  //len = short(voct_semi/410+1)*2;

 // new_taps = get_taps(len, voct_fine << 4, 65535);
  //new_taps = 0x1 << int(voct_semi/410);
  new_taps = get_taps(len, param_0<<4, param_1<<4);
  

  actual_len = get_actual_length(len);
  //Serial.println(get_actual_length(len));
  //Serial.println(len);
  //Serial.println(new_taps);

  //digitalWrite(taps_led_pin,0);
  voct_semi -= half;
  voct_fine -= half;
  if(voct_semi > -zero and voct_semi < zero)
  {
    voct_semi = 0;
    //digitalWrite(taps_led_pin, 1);
  }
  else if(voct_semi <= zero)
  {
    voct_semi += zero;
  }
  else if(voct_semi >= zero)
  {
    voct_semi -= zero;
  }

  if(voct_fine > -zero and voct_fine < zero)
  {
    voct_fine = 0;
    //digitalWrite(13, 1);
  }
  else if(voct_fine <= -zero)
  {
    voct_fine += zero;
  }
  else if(voct_fine >= zero)
  {
    voct_fine -= zero;
  }
  float voct_cv_value = 10*float(voct_cv)/half-10;

  voct = float(voct_semi*0 + voct_fine)/(half-zero);
  voct = round(voct*12.0f)/12.0f;
  voct += voct_cv_value;
  //Serial.println(voct_cv_value);

  voct_oct >>= 9;
  voct_oct -= 4;

  float semi;
  semi = round((float(voct_semi)/(half-zero))*(3))/12.0;

  float fine;
  fine = float(voct_fine)/(12.0*(half-zero));
  
  voct = 261.63*pow(2, voct_oct+semi+fine)*actual_len;
//  voct = 261.63*actual_len;


  poly >>= 9;
  
  
  //Serial.println(*(int*)(0x400C8044));

  if(taps != new_taps)
  {
    digitalWrite(taps_led_pin,1-digitalRead(taps_led_pin));
  }
  taps = new_taps;
  set_taps(taps);
//  set_taps(0x800);
  Serial.println(semi);

  analogWriteFrequency(clk_pin_0, voct);
  analogWrite(clk_pin_0, 2);
  
  if(poly > 0)
  {
    analogWriteFrequency(clk_pin_1, voct*poly_maps[poly]);
    analogWrite(clk_pin_1, 2);
  }
  else
  {
    analogWrite(clk_pin_1, 0);
  }
  
  freq -= 1e3;
  if(freq < 1e3)
  {
    freq = 100e3;
  }
}
