#include "lookup.h"

#define GLITCH_LEN 1

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



int taps_maps [12] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
float poly_maps[8] = {0, 1, 1.2, 1.25, 1.333, 1.5, 1.5, 2};

int clk_pin_0 = 12;
int clk_pin_1 = 13;

int lfsr0_in_pin = 32;
int lfsr1_in_pin = 33;

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

int glitch_in_state = 0;

void init_taps()
{
  for (int i = 0; i < 12; ++i)
  {
    pinMode(taps_maps[i], OUTPUT);
    digitalWrite(taps_maps[i], 0);
  }
}

void set_taps(int taps)
{
  for (int i = 0; i < 12; ++i)
  {
    digitalWrite(taps_maps[i], (taps & 1));
    taps >>= 1;
  }
}

#define INIT_OUTPUT(pin, value)\
  pinMode(pin, OUTPUT);\
  digitalWrite(pin, value);

volatile int adc_accum[16] = {0};
volatile int sample_counter = 0;
volatile int adc_memory[16] = {0};
volatile char adc_channel = 0;

void adc_interrupt()
{
  /*analogRead(lfo_pin);
    adc_memory <<= 2;
    adc_memory += (lfo_pin<<1);
    adc_memory >>= 2;
  */

  //adc_memory[adc_channel] <<= 1;
  adc_accum[adc_channel] += ADC1_R0;
  //adc_accum[adc_channel] >>= 1;
  adc_channel += 1;
  
  if(sample_counter == 0)
  {
    adc_memory[adc_channel] = adc_accum[adc_channel] >> 1;
    adc_accum[adc_channel] = 0;
  }
  
  if(adc_channel == 0xf)
  {
    adc_channel = 0;
    sample_counter += 1;
    if(sample_counter >= 2)
    {
      sample_counter = 0;
    }
  }

  ADC1_HC0 = (0x80|adc_channel);

}

void setup() {

  __disable_irq();
  
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

  pinMode(voct_cv_pin, INPUT);

  init_taps();
  set_taps(0x800);

  ADC1_GC |= 0x80; //Calibrate
  while (ADC1_GC & 0x80);

  ADC1_CFG &= 0xfffe0000;
//              KJJIHHGFFEDDCBBAA
  ADC1_CFG |= 0b01100011100011011;
/*              K Data overwrite disabled (disable/enable)
                 JJ 32 averages (4/8/16/32)
                   I Software triggered (software/hardware)
                    HH VREF - no options
                      G High speed convserion (low/high speed)
                       FF Sample period = 8/24 ADC clocks (short/long sample) (2/12, 4/16, 6/20, 8/24)
                         E Low power mode (low / not low)
                          DD ADCK = Input clock / 1 (/1, /2, /4, /8)
                            C Long sample mode (short/long)
                             BB 12-bit conversion (8/10/12/Reserved)
                               AA Input Clock = IPG Clock (IPG, IPG/2, reserved, ADACK)
*/
  

  ADC1_GC &= 0xffffff00;
//             HGFEDCBA
  ADC1_GC |= 0b00100001;
/*             H Calibration start
                G Continuous conversion (no/yes)
                 F Hardware average enable (no/yes)
                  E Compare function enable (no/yes)
                   D Compare function gt enable (no/yes)
                    C Compare function range enable (no/yes)
                     B DMA enable (no/yes)
                      A Asynchronous clock output enable (no/yes)
*/

/*
Conversion time:

4 ADCK
2 bus clock
1.5 us if ADACKEN = 0

+

AVGS * (Base + long)

Base = 17/21/25 (8/10/12-bit)
long = 3/13, 5/17, 7/21, 9/25 (sample period -> long sample mode)

Max averaging, max sample time, max res:
4+32*(25+25) = 1604 ADCK cycles + 1 bus cycles


*/

  ADC1_HC0 |= 0x80; //Enable interrupt

  attachInterruptVector(IRQ_NUMBER_t::IRQ_ADC1, adc_interrupt);
  NVIC_SET_PRIORITY(IRQ_NUMBER_t::IRQ_ADC1, 10);
  NVIC_ENABLE_IRQ(IRQ_NUMBER_t::IRQ_ADC1);

  Serial.begin(38400);

  __enable_irq();

  ADC1_HC0 = 0x80;
  
}


int freq = 10e6;
int taps = 0;
int half = 2048;

void loop() {
  // put your main code here, to run repeatedly:
  delay(10); // 100 Hz
  float voct = 0;
  int voct_semi;
  int voct_fine;
  int voct_cv;
  int voct_oct;
  int voct_atv;
  
  voct_semi = adc_memory[pin_to_channel[voct_semi_pin]];
  voct_fine = adc_memory[pin_to_channel[voct_fine_pin]];
  voct_cv = adc_memory[pin_to_channel[voct_cv_pin]];
  voct_atv = adc_memory[pin_to_channel[voct_atv_pin]];
  voct_oct = adc_memory[pin_to_channel[voct_oct_pin]];
  
  int param_0;
  int param_0_cv;
  int param_1;
  
  param_0 = adc_memory[pin_to_channel[param_0_pin]];
  param_0_cv = adc_memory[pin_to_channel[param_0_cv_pin]];
  param_1 = adc_memory[pin_to_channel[param_1_pin]];

  int len_knob;
  int len_cv;
  len_knob = adc_memory[pin_to_channel[len_knob_pin]];
  len_cv = adc_memory[pin_to_channel[len_cv_pin]];

  int poly;
  int lfo;
  poly = adc_memory[pin_to_channel[poly_pin]];
  lfo = adc_memory[pin_to_channel[lfo_pin]];

  int glitch_enabled = 1 - digitalRead(glitch_en_pin);
  glitch_enabled = 0;

  int glitch_in = 1 - digitalRead(glitch_pin);
  int ext_glitch = glitch_in - glitch_in_state;

  int freq_lock = 1 - digitalRead(freq_lock_pin);
  freq_lock = 1;
  
    Serial.print(voct_cv);
    Serial.print(",");
  /*  Serial.print(voct_atv);
    Serial.print(",");
    Serial.print(voct_fine);
    Serial.print(",");
    Serial.print(voct_semi);
    Serial.print(",");
    Serial.print(param_0_cv);
    Serial.print(",");
    Serial.print(param_0);
    Serial.print(",");
    Serial.print(param_1);
    Serial.print(",");
    Serial.print(poly);
    Serial.print(",");
    Serial.print(len_cv);
    Serial.print(",");
    Serial.print(len_knob);
    Serial.print(",");
    Serial.print(voct_oct);
    */
    Serial.print(",");
    Serial.print(lfo);

  
  Serial.print("\n");

  int zero = half / 16;

  int new_taps;

  //new_taps = voct_semi&0xaa8;

  lfo_counter += 1;
  if ((lfo_counter > lfo + 4 && glitch_enabled) || ext_glitch == 1)
  {
    lfo_counter = 0;
    glitch_counter = GLITCH_LEN;
  }
  if (glitch_counter > 0)
  {
    digitalWrite(lfo_led_pin, 0);
  }
  else
  {
    digitalWrite(lfo_led_pin, 1);
  }

  glitch_in_state = glitch_in;


  unsigned short len = short(pow(2, 1 + float(len_knob) * 11 / 4000));
  unsigned short actual_len;
  if (len > 4095)
  {
    len = 4095;

  }

  //len = short(voct_semi/410+1)*2;

  // new_taps = get_taps(len, voct_fine << 4, 65535);
  //new_taps = 0x1 << int(voct_semi/410);
  new_taps = get_taps(len, param_0 << 4, param_1 << 4);

  actual_len = get_actual_length(len);

  if (taps != new_taps)
  {
    digitalWrite(taps_led_pin, 1 - digitalRead(taps_led_pin));
  }
  taps = new_taps;

  digitalWrite(lfsr1_in_pin, 0);
  if (glitch_counter > 0)
  {
    digitalWrite(lfsr1_in_pin, 1);
    glitch_counter -= 1;
    taps = get_taps(4095, 65535, 65535);
  }


  set_taps(taps);



  //Serial.println(get_actual_length(len));
  //Serial.println(len);
  //Serial.println(new_taps);

  //digitalWrite(taps_led_pin,0);
  voct_semi -= half;
  voct_fine -= half;
  if (voct_semi > -zero and voct_semi < zero)
  {
    voct_semi = 0;
    //digitalWrite(taps_led_pin, 1);
  }
  else if (voct_semi <= zero)
  {
    voct_semi += zero;
  }
  else if (voct_semi >= zero)
  {
    voct_semi -= zero;
  }

  if (voct_fine > -zero and voct_fine < zero)
  {
    voct_fine = 0;
    //digitalWrite(13, 1);
  }
  else if (voct_fine <= -zero)
  {
    voct_fine += zero;
  }
  else if (voct_fine >= zero)
  {
    voct_fine -= zero;
  }

  if (voct_atv > 2 * half - zero)
  {
    voct_atv = 2 * half;

  }
  float voct_atv_value = float(voct_atv) / (2 * (half - zero));

  float voct_cv_value = -2.783 * (float(voct_cv) / (half) - 1) * voct_atv_value;

  voct = float(voct_semi * 0 + voct_fine) / (half - zero);
  voct = round(voct * 12.0f) / 12.0f;
  voct += voct_cv_value;
  //Serial.println(voct_cv_value);

  voct_oct >>= 9;
  voct_oct -= 4;

  float semi;
  semi = round((float(voct_semi) / (half - zero)) * (3)) / 12.0;

  float fine;
  fine = float(voct_fine) / (12.0 * (half - zero));

  voct = 261.63 * pow(2, voct_oct + semi + fine + voct_cv_value);
  if (freq_lock != 0)
  {
    voct *= actual_len;
  }


  poly >>= 9;




  //  set_taps(0x800);
  //Serial.println(voct_cv_value);

  analogWriteFrequency(clk_pin_0, voct);
  analogWrite(clk_pin_0, 2);

  if (poly > 0)
  {
    analogWriteFrequency(clk_pin_1, voct * poly_maps[poly]);
    analogWrite(clk_pin_1, 2);
  }
  else
  {
    analogWrite(clk_pin_1, 0);
  }

  freq -= 1e3;
  if (freq < 1e3)
  {
    freq = 100e3;
  }
}
