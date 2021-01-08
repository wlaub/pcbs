#include "lookup.h"
#include "adc_interrupt.h"

//In loops
#define GLITCH_LEN 50

#define DETUNE_LFSR1

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



//int taps_maps [12] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}; //Moved to serial interface
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

//int voct_semi_pin = A10; //Moved to encoder
int voct_fine_pin = A1; 
int voct_atv_pin = A0;
int voct_cv_pin = A2;
int param_0_cv_pin = A4;
int lfo_pin = A6;
int len_cv_pin = A5;
//int poly_pin = A6; //Moved to encoder
int param_1_pin = A7;
//int voct_oct_pin = A8; //Moved to encoder
int len_knob_pin = A8;
int param_0_pin = A3;

int lfo_counter = 0;

int glitch_counter = 0;

int glitch_in_state = 0;

void init_taps()
{
  /*
  for (int i = 0; i < 12; ++i)
  {
    pinMode(taps_maps[i], OUTPUT);
    digitalWrite(taps_maps[i], 0);
  }
  */
}

void set_taps(int taps)
{
  /*
  for (int i = 0; i < 12; ++i)
  {
    digitalWrite(taps_maps[i], (taps & 1));
    taps >>= 1;
  }
  */
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

int sck_pin = 2;
int sdo_pin = 4;
int sdi_pin = 3;
int we_pin = 5;

volatile unsigned char lfsr_en0 = 1;
volatile unsigned char lfsr_en1 = 1;

void write_lfsr(unsigned short taps, unsigned char oe0, unsigned char oe1)
{
  /*
  Data is shifted in on rising edge
  WE is active high
  oe0 and oe1 must be 0 or 1
  output buffer will be shifted left for convenience
  0xXXTTT00
  where TTT is the feedback configuration
  XX is oe0 oee
  */
  unsigned short data = 0;
  data |= taps<<2;
  data |= oe0<<14;
  data |= oe1<<15;
  //data = 0b1000000000000000;

  int rate = 0;
  digitalWrite(sck_pin, 0);
  digitalWrite(we_pin, 1);  
  for(int i = 0; i < 14; ++i)
  {
    
    digitalWrite(sck_pin, 0);
    digitalWrite(sdi_pin, data>>15);
    digitalWrite(sck_pin, 1);
    data <<= 1;
    
  }
  digitalWrite(we_pin, 0); //Output enables are latched in
  digitalWrite(sck_pin, 0);
}

unsigned short read_lfsr()
{
  /*
  Data is shifted out on rising edge of clock
  inputs are locked latched in on WE high
  data is
  0000
  CLK_SEL
  VOCT_OCT_B
  VOCT_OCT_A
  POLY_B
  POLY_A
  VOCT_SEMI_B
  VOCT_SEMI_A
  GLITCH_IN
  0000
  */
  unsigned short result = 0;
  
  digitalWrite(sck_pin, 0);
  digitalWrite(we_pin, 1);  
  digitalWrite(we_pin, 0);  
  for(int i = 0; i < 12; ++i)
  {
        
    result<<=1;
    result|=digitalRead(sdo_pin);
    digitalWrite(sck_pin, 1);
    digitalWrite(sck_pin, 0);
    
  }
  digitalWrite(we_pin, 0); //Output enables are latched in
  digitalWrite(sck_pin, 0);
  return result;
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

  INIT_OUTPUT(lfo_led_pin, 0)
  //INIT_OUTPUT(led0_pin, 0)
  //INIT_OUTPUT(led1_pin, 0)
  //INIT_OUTPUT(led2_pin, 0)

  pinMode(glitch_en_pin, INPUT);
  //pinMode(glitch_pin, INPUT);
  pinMode(freq_lock_pin, INPUT);
  //pinMode(ext_clk_en_pin, INPUT);

  pinMode(voct_atv_pin, INPUT);
  pinMode(voct_fine_pin, INPUT);
  pinMode(voct_cv_pin, INPUT);
  pinMode(param_0_pin, INPUT);
  pinMode(param_0_cv_pin, INPUT);
  pinMode(len_cv_pin, INPUT);
  pinMode(lfo_pin, INPUT);
  pinMode(param_1_pin, INPUT);
  pinMode(len_knob_pin, INPUT);
  pinMode(poly_sw_pin, INPUT);

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

  //Setup serial interface pins
  pinMode(we_pin, OUTPUT); //Active high write enable
  pinMode(sck_pin, OUTPUT);
  pinMode(sdo_pin, INPUT); //LFSR serial data out to MCU
  pinMode(sdi_pin, OUTPUT); //LFSR serial data in from MCU
  //Initialize LFSR
  write_lfsr(0x1, lfsr_en0,lfsr_en1);
  
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
volatile int poly_oct;
volatile float poly_oct_val;

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
//    analogWriteFrequency(clk_pin_1, voct);
//    analogWrite(clk_pin_1, 2);
   
  
    if (lfsr_en1 == 1)
    {
      #ifdef DETUNE_LFSR1
      float scale = actual_len*4;
      analogWriteFrequency(clk_pin_1, floor((voct * poly_maps[poly] * poly_oct_val)/scale)*scale);
      #else
      analogWriteFrequency(clk_pin_1, (voct * poly_maps[poly] * poly_oct_val));
      #endif
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

volatile int led_index = 0;
//0 = L, 1 = H, 2 = Z. These are the pin states necessary to light a given LED
char led0_state[] = {0,1,2,2,0,1,2};
char led1_state[] = {1,0,0,1,2,2,2};
char led2_state[] = {2,2,1,0,1,0,2};

#define UR 0
#define LR 1
#define UC 2
#define LC 3
#define UL 5
#define LL 4

// Upper right, lower right, upper middle, lower middle, upper left, lower left
char led_map[] = {0,0,0,1,0,0};

int led_cycle_counter = 0;

void set_led(int pin, int state)
{
  //Just configures the output according the scheme above
  if(state == 0)
  {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, 0);
  }
  else if(state == 1)
  {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, 1);
  }
  else if(state == 2)
  {
    pinMode(pin, INPUT);
  }
  
}

//TODO: Make these be automatically saved and loaded from nonvolatile memory
volatile int semi_enc_counter = 0;
volatile int poly_enc_counter = 0;
volatile int oct_enc_counter = 0;
volatile unsigned short prev_iox = 0;

void loop() {
  // put your main code here, to run repeatedly:

  int start_time = micros();

  int update_lfsr = 0;

  unsigned short iox = 0;
  iox = read_lfsr();  



  /*Charlieplexed LEDs*/

  if(led_map[led_index] != 0)
  {
    set_led(led0_pin, led0_state[led_index]);
    set_led(led1_pin, led1_state[led_index]);
    set_led(led2_pin, led2_state[led_index]);
  }
  else
  {
    set_led(led0_pin, led0_state[6]);
    set_led(led1_pin, led1_state[6]);
    set_led(led2_pin, led2_state[6]);

  }

  led_index += 1;
  if (led_index >5)
  {
    led_index = 0;
  }

  /* Encoders*/

  #define SEMI_ENCODER(x) ((x>>5)&3)
  
  if (SEMI_ENCODER(prev_iox) == 0)
  {
    if(SEMI_ENCODER(iox) == 2)
    {
    semi_enc_counter -= 1;  
    }
    else if(SEMI_ENCODER(iox) == 1)
    {
    semi_enc_counter += 1;  
    }
    
  }
  led_map[UL] = 0;
  if(semi_enc_counter == 0)
  {
    led_map[UL] = 1;
  }

  #define POLY_ENCODER(x) ((x>>7)&3)
  
  if (POLY_ENCODER(prev_iox) == 0)
  {
    if(POLY_ENCODER(iox) == 2)
    {
    poly_enc_counter -= 1;  
    }
    else if(POLY_ENCODER(iox) == 1)
    {
    poly_enc_counter += 1;  
    }
    
  }

  poly = 0;
  if(poly_enc_counter > 0)
  {
    poly = (poly_enc_counter-1)%poly_count;
    poly_oct = floor((poly_enc_counter-1)/float(poly_count));
  }
  else if(poly_enc_counter < 0)
  {
    poly = (poly_enc_counter+1)%poly_count+poly_count-1;
    poly_oct = floor(poly_enc_counter/float(poly_count));
  }
  poly_oct_val = pow(2, poly_oct);
  
  if(poly_enc_counter == 0 && lfsr_en1 == 1)
  {
    lfsr_en1 = 0;
    update_lfsr = 1;
    
  }
  else if(poly_enc_counter != 0 && lfsr_en1 == 0)
  {
    lfsr_en1 = 1;
    update_lfsr = 1;
  }
    

//TEMPORARY
  led_map[UC] = 0;
  if(poly_enc_counter == 0)
  {
    led_map[UC] = 1;
  }

  #define OCT_ENCODER(x) ((x>>9)&3)
  
  if (OCT_ENCODER(prev_iox) == 0)
  {
    if(OCT_ENCODER(iox) == 2)
    {
    oct_enc_counter -= 1;  
    }
    else if(OCT_ENCODER(iox) == 1)
    {
    oct_enc_counter += 1;  
    }
    
  }
  led_map[UR] = 0;
  if(oct_enc_counter == 0)
  {
    led_map[UR] = 1;
  }

  /* Reading some knob values*/

  int voct_fine;
  int voct_cv;
//  //int voct_oct; GLOBAL

  voct_fine = adc_memory[pin_to_channel[voct_fine_pin]];
  //voct_cv = adc_memory[pin_to_channel[voct_cv_pin]];
  //voct_atv = adc_memory[pin_to_channel[voct_atv_pin]];

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
  
//  
//  /*  Serial.print(voct_cv);
//    Serial.print(",");
//    Serial.print(adc_memory[pin_to_channel[poly_pin]]);
//    Serial.print(",");
//*/
//    /*
//    Serial.print(voct_atv);
//    Serial.print(",");
//    Serial.print(voct_fine);
//    Serial.print(",");
//    Serial.print(voct_semi);
//    Serial.print(",");
//    Serial.print(param_0_cv);
//    Serial.print(",");
//    Serial.print(param_0);
//    Serial.print(",");
//    Serial.print(param_1);
//    Serial.print(",");
//    Serial.print(poly);
//    Serial.print(",");
//    Serial.print(len_cv);
//    Serial.print(",");
//    Serial.print(len_knob);
//*/    
//    /*Serial.print(",");
//    Serial.print(lfo);
//
//    Serial.print(",");
//    Serial.print(adc_memory[pin_to_channel[voct_oct_pin]]);
//
//
//    Serial.print(",");
//    Serial.print(adc_counter);*/
//    adc_counter = 0;
//    
//  
//  /******Internal LFO and glitch******/

  int new_taps;

  int lfo;
  lfo = adc_memory[pin_to_channel[lfo_pin]];

  float lfo_result;
  lfo_result = pow(2,4.32*float(lfo)/(half)); //20 Hz to 1 Hz at center = 20 to 1/20Hz. log_2(400)= 8.64
  lfo_result *= 50000/LOOP_PERIOD;            //20 Hz = 50e3 us
  lfo = int(lfo_result);  

  int glitch_enabled = 1 - digitalRead(glitch_en_pin);
  
  int glitch_in = 1-((iox>>4)&0x1);  
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
      (glitch_enabled_memory != glitch_enabled && glitch_enabled) //The first tick on enabling
      || (lfo_counter > lfo )                                     //subsequence ticks
      || ext_glitch == 1                                          //external glitch trigger
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
    led_map[LC] = 1-led_map[LC];
  }


  //digitalWrite(lfsr1_in_pin, 0); //Uninverts LFSR1 during glitch, kinda buggy?
  if (glitch_counter > 0)
  {
    //digitalWrite(lfsr1_in_pin, 1); //Uninverts LFSR1 during glitch, kinda buggy/ tends to stick?
    glitch_counter -= 1;
    actual_len=2048; //To freq lock during glitch
    new_taps = glitch_taps;
  }

  if (taps != new_taps || update_lfsr )
  {
    write_lfsr(new_taps, lfsr_en0, lfsr_en1);
  }
  taps = new_taps;


//  /******Read and process pitch control knobs******/

  /*Map encoder counters to values*/
  semi = semi_enc_counter / 12.0;
  voct_oct = oct_enc_counter; 
  
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

  //TEMPORARY
  led_map[LL] = 0;
  if(voct_fine == 0)
  {
    led_map[LL] = 1;
  }

  fine = float(voct_fine) / (12.0 * (half - zero));
  
//
//  /*Terminate debug prints*/
//
// //   Serial.print(actual_len);
// //   Serial.print(",");
 
  Serial.print("\n");

  int current_time = micros();
  //Serial.print(actual_len);
  Serial.print(len_knob);
  Serial.print(",");
  Serial.print(len_cv);
  Serial.print(",");
  Serial.print(actual_len);


  //Serial.print(",");
  //Serial.print(cv_len);
  //Serial.print(",");
  //Serial.print(current_time-start_time);

  Serial.print(",");
  Serial.print(poly);
  Serial.print(",");
  Serial.print(poly_oct);
  //Serial.print(iox, BIN);

  

  prev_iox = iox;
  
//  Serial.print(",");
//  Serial.print(1e6*adc_time_count/(float(adc_cumulative_time))); // Hz
  adc_cumulative_time = 0;
  adc_time_count = 0;
  
  delayMicroseconds(LOOP_PERIOD - (current_time-start_time)); // 1000 Hz

  
}
