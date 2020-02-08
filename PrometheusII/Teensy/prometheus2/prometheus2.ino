#include "lookup.h"
#include "adc_interrupt.h"

//In loops
#define GLITCH_LEN 50

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

volatile int adc_counter = 0;

void adc_interrupt();

int taps = 0;
int glitch_taps;

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

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  pinMode(A8, INPUT);
  pinMode(A9, INPUT);
  pinMode(A10, INPUT);
  pinMode(A11, INPUT);

  init_taps();
  set_taps(0x800);

  ADC1_GC |= 0x80; //Calibrate
  while (ADC1_GC & 0x80);

  ADC1_CFG &= 0xfffe0000;
//              KJJIHHGFFEDDCBBAA
  ADC1_CFG |= 0b00000010000001011;
/*              K Data overwrite disabled (disable/enable)
                 JJ 32 averages (4/8/16/32)
                   I Software triggered (software/hardware)
                    HH VREF - no options
                      G High speed convserion (low/high speed)
                       FF Sample period = 2/12 ADC clocks (short/long sample) (2/12, 4/16, 6/20, 8/24)
                         E Low power mode (low / not low)
                          DD ADCK = Input clock / 1 (/1, /2, /4, /8)
                            C Short sample mode (short/long)
                             BB 12-bit conversion (8/10/12/Reserved)
                               AA Input Clock = IPG Clock (IPG, IPG/2, reserved, ADACK)
0b01100010000001011 => ~19.5 kHz
0b00000010000001011 => ~156 kHz
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

ADACK = 20 MHz?

*/

  ADC1_HC0 |= 0x80; //Enable interrupt

  attachInterruptVector(IRQ_NUMBER_t::IRQ_ADC1, adc_interrupt);
  NVIC_SET_PRIORITY(IRQ_NUMBER_t::IRQ_ADC1, 10);
  NVIC_ENABLE_IRQ(IRQ_NUMBER_t::IRQ_ADC1);

  Serial.begin(38400);

  __enable_irq();

  ADC1_HC0 = 0x80;

  glitch_taps = get_taps(4095,65535,65535);
  
}


int freq = 10e6;
int half = 2048;
int zero = half / 16;

int glitch_enabled_memory = 0;

volatile int voct_oct;
volatile float semi;
volatile float fine;
volatile float voct_atv_value;
volatile int freq_lock;
volatile int poly;

volatile float voct = 0;
volatile unsigned short actual_len;

int adc_last_time = 0;
int adc_cumulative_time = 0;
int adc_time_count = 0;

void adc_interrupt()
{
  
  //Read values
  ++adc_counter;
  adc_accum[adc_channel] += ADC1_R0;

  //Update buffers
  if(sample_counter == 0)
  {
    adc_memory[adc_channel] = adc_accum[adc_channel] >> 1;
    adc_accum[adc_channel] = 0;

  }

  //Pin-specific updates
  if(adc_channel == pin_to_channel[voct_cv_pin])
  {  // V/oct pin
    float voct;
    int voct_atv = adc_memory[pin_to_channel[voct_atv_pin]];
    voct_atv -= zero;
    if(voct_atv > 2*half - 2*zero)
    {
      voct_atv = 2*half-2*zero;
    }
    if(voct_atv < 0)
    {
      voct_atv = 0;
    }
    float voct_atv_value = float(voct_atv) / (2*half - 2*zero);
    
    float voct_cv_value = -2.95 * (float(adc_memory[pin_to_channel[voct_cv_pin]])/half - 1) * voct_atv_value;

    voct = 261.63 * pow(2, voct_oct + semi + fine + voct_cv_value);

    if (freq_lock != 0)
    {
      voct *= actual_len;
    }
    else
    {
      voct *= 2; //Normalizing shortest length pitch
    }
  
    analogWriteFrequency(clk_pin_0, voct);
    analogWrite(clk_pin_0, 2);
  
    if (poly > 0)
    {
      analogWriteFrequency(clk_pin_1, voct * poly_maps[poly]);
      analogWrite(clk_pin_1, 2);
    }
    else
    {
      pinMode(clk_pin_1, OUTPUT);
      digitalWrite(clk_pin_1, 0);
    }
  }    

  adc_channel += 1;
  if(adc_channel > 0xf)
  {
    adc_channel = 0;
    sample_counter += 1;
    if(sample_counter >= 2)
    {
      sample_counter = 0;
    }
    
    int current_time = micros();
    adc_cumulative_time += current_time - adc_last_time;
    adc_last_time = current_time;
    adc_time_count +=1;

  }

  ADC1_HC0 = (0x80|adc_channel);

}

#define LOOP_PERIOD 200

void loop() {
  // put your main code here, to run repeatedly:

  int start_time = micros();

  /**/
  //Serial Test
  int out_data = 0xaa;
  for(int i = 0; i < 14; ++i) // mock write
  {
     /* digitalWrite(clk_pin_1, 0);
      digitalWrite(clk_pin_1, out_data&0x1);
      digitalWrite(clk_pin_1, 1);*/
      out_data >>= 1;
  }
  for(int i = 0; i < 8; ++i) //mock read
  {
  /*    digitalWrite(clk_pin_1, 0);
      digitalWrite(clk_pin_1, out_data&0x1);
      digitalWrite(clk_pin_1, 1);*/
      out_data >>= 1;
  }
  /**/

  int voct_semi;
  int voct_fine;
  int voct_cv;
  //int voct_oct; GLOBAL
  int voct_atv;
  voct_semi = adc_memory[pin_to_channel[voct_semi_pin]];
  voct_fine = adc_memory[pin_to_channel[voct_fine_pin]];
  voct_cv = adc_memory[pin_to_channel[voct_cv_pin]];
  voct_atv = adc_memory[pin_to_channel[voct_atv_pin]];
  voct_oct = adc_memory[pin_to_channel[voct_oct_pin]];
  voct_oct -= half;
  voct_oct = round(3.5*float(voct_oct)/half); //7 octaves

  
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



  freq_lock = 1 - digitalRead(freq_lock_pin);
  
  /*  Serial.print(voct_cv);
    Serial.print(",");
    Serial.print(adc_memory[pin_to_channel[poly_pin]]);
    Serial.print(",");
*/
    /*
    Serial.print(voct_atv);
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
*/    
    /*Serial.print(",");
    Serial.print(lfo);

    Serial.print(",");
    Serial.print(adc_memory[pin_to_channel[voct_oct_pin]]);


    Serial.print(",");
    Serial.print(adc_counter);*/
    adc_counter = 0;
    
  
  /******Internal LFO and glitch******/

  int new_taps;

  int lfo;
  poly = (adc_memory[pin_to_channel[poly_pin]]>>9);
  lfo = adc_memory[pin_to_channel[lfo_pin]];

  float lfo_result;
  lfo_result = pow(2,4.32*float(lfo)/(half)); //20 Hz to 1 Hz at center = 20 to 1/20Hz. log_2(400)= 8.64
  lfo_result *= 50/LOOP_PERIOD; //20 Hz = 50 ms
  lfo = int(lfo_result);  

  //int glitch_enabled = 1 - digitalRead(glitch_en_pin);
  int glitch_enabled = digitalRead(glitch_en_pin); //For rev00 w/ wrong switch
  

  int glitch_in = 1 - digitalRead(glitch_pin);
  int ext_glitch = glitch_in - glitch_in_state;

  if(glitch_enabled)
  {
    lfo_counter += 1;
  }
  else
  {
    lfo_counter = 0;
  }
  if (
      (glitch_enabled_memory != glitch_enabled && glitch_enabled)
      || (lfo_counter > lfo && glitch_enabled)
      || ext_glitch == 1
     )
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
  glitch_enabled_memory = glitch_enabled;

  glitch_in_state = glitch_in;

  /******Length selection******/

  float knob_len = float(len_knob) * 11 / 4000;
  float cv_len = -9.17*((float(len_cv)-2055)/(half));

  //Serial.print(cv_len);
  //Serial.print(",");
  //Serial.print(len_cv);

  float param_0_alpha = -5.06*(float(param_0_cv)/(half)-1)/5;

  unsigned int len = int(pow(2, 1 + knob_len + cv_len));
  if (len < 2)
  {
    len = 2;
  }
  if (len > 4095)
  {
    len = 4095;

  }

  int param_0_combined = (param_0 << 4);
  if(param_0_alpha > 0)
  {
    param_0_combined = param_0_alpha*65545+(1-param_0_alpha)*param_0_combined;
  }
  else
  {
    param_0_combined = (1+param_0_alpha)*param_0_combined;
  }
  
  new_taps = get_taps(len, param_0_combined, param_1 << 4);

  actual_len = get_actual_length(len);


  /******Update taps and indicators******/
  
  if (taps != new_taps)
  {
    digitalWrite(taps_led_pin, 1 - digitalRead(taps_led_pin));
  }
  taps = new_taps;

  //digitalWrite(lfsr1_in_pin, 0); //Uninverts LFSR1 during glitch, kinda buggy?
  if (glitch_counter > 0)
  {
    //digitalWrite(lfsr1_in_pin, 1); //Uninverts LFSR1 during glitch, kinda buggy/ tends to stick?
    glitch_counter -= 1;
    set_taps(glitch_taps);
    actual_len=2048; //To freq lock during glitch
  }
  else
  {
    set_taps(taps);
  }

  /******Read and process pitch control knobs******/

  /*quantize to +/- 6 semitones*/
  /*center*/
  voct_semi -= half; 
  //float semi;
  semi = round(6*float(voct_semi)/half) / 12.0;

  /*Scale tuning knob to +/- 1/12*/
  /*Center*/
  voct_fine -= half;
  /*Deadzone at zero*/
  if (voct_fine > -zero and voct_fine < zero)
  {
    voct_fine = 0;
    //digitalWrite(XXX, 1); //This is where you would indicate deadzone if you had a light
  }
  else if (voct_fine <= -zero)
  {
    voct_fine += zero;
  }
  else if (voct_fine >= zero)
  {
    voct_fine -= zero;
  }

  fine = float(voct_fine) / (12.0 * (half - zero));

  /*Terminate debug prints*/

 //   Serial.print(actual_len);
 //   Serial.print(",");
 
  Serial.print("\n");

  int current_time = micros();
  Serial.print(actual_len);
  Serial.print(",");
  Serial.print(current_time-start_time);
  Serial.print(",");
  Serial.print(1e6*adc_time_count/(float(adc_cumulative_time))); // Hz
  adc_cumulative_time = 0;
  adc_time_count = 0;
  
  delayMicroseconds(LOOP_PERIOD - (current_time-start_time)); // 1000 Hz

  
}
