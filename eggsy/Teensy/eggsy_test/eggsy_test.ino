#include "lookup.h"
#include "globals.h"
#include "pinmap.h"
#include "adc_interrupt.h"
#include "leds.h"


int lfo_counter = 0;

int glitch_counter = 0;

int glitch_in_state = 0;

#define INIT_OUTPUT(pin, value)\
  pinMode(pin, OUTPUT);\
  digitalWrite(pin, value);

int taps = 0;
int glitch_taps;

int sck_pin = 2;
int sdo_pin = 4;
int sdi_pin = 3;
int we_pin = 5;

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


  configure_adc();
  Serial.begin(115200);

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


int glitch_enabled_memory = 0;


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
//TEMPORARY

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

  int current_time = micros();
 /*
  Serial.print("\n");

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
*/

/* ADC Channel Plotting */

//  Serial.print(adc_memory[voct_cv_channel]);Serial.print(",");
//  Serial.print(adc_memory[len_cv_channel]); Serial.print(",");
//  Serial.print(adc_memory[param_0_cv_channel]); Serial.print(",");
//  Serial.print(adc_memory[voct_atv_channel]); Serial.print(",");
//  Serial.print(adc_memory[len_knob_channel]); Serial.print(",");
//  Serial.print(adc_memory[voct_fine_channel]); Serial.print(",");
//  Serial.print(adc_memory[param_0_channel]); Serial.print(",");
//  Serial.print(adc_memory[param_1_channel]); Serial.print(",");
//  Serial.print(adc_memory[lfo_channel]); Serial.print(",");

  
//  Serial.print("\n");
  
  /* ADC Sample Rate Measurement and Printing*/
/*
  int adc_count_duration = current_time - adc_last_time;
  if(adc_count_duration > ADC_MEAS_PERIOD)
  {

//    PRINT_ADC_RATE(voct_cv_channel);
//    PRINT_ADC_RATE(len_cv_channel);
//    PRINT_ADC_RATE(param_0_cv_channel);
//    PRINT_ADC_RATE(voct_atv_channel);
//    PRINT_ADC_RATE(len_knob_channel);
//    PRINT_ADC_RATE(voct_fine_channel);
//    PRINT_ADC_RATE(param_0_channel);
//    PRINT_ADC_RATE(param_1_channel);

    for(int i = 0; i < 16; ++i)
    {
      adc_counter[i] = 0;
    }
    adc_last_time = current_time;

    //overhead in microseconds
    Serial.print(LOOP_PERIOD - (current_time-start_time));

    Serial.print("\n");
  }
  */
  
  delayMicroseconds(LOOP_PERIOD - (current_time-start_time)); // 1000 Hz

  
}
