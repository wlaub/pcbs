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

volatile int poly_sw_prev = 0;

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

  poly_sw_prev = 1-digitalRead(poly_sw_pin);

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
  main_pitch.enabled = 1;
  write_lfsr(0x1, main_pitch.enabled, aux_pitch.enabled);
  
}


int glitch_enabled_memory = 0;


//TODO: Make these be automatically saved and loaded from nonvolatile memory
volatile int polyphony_counter = 0;
volatile unsigned short prev_iox = 0;

signed char poly_mode = 0;
signed char prev_poly_mode = 0;
volatile int poly_active = 0;
signed char poly_changed = 0;

volatile int length_lock = 0;
unsigned int len = 1;
int blink_counter = 0;
int blinker = 0;

unsigned char taps_toggle = 0;


int poly_down_time = 0;
int poly_held_time = 0;

void loop() {
  // put your main code here, to run repeatedly:

  int start_time = micros();

  
  ++blink_counter;
  if (blink_counter == BLINK_RATE)
  {
    blink_counter = 0;
    blinker = 1-blinker;
  }

  int update_lfsr = 0;

  unsigned short iox = 0;
  iox = read_lfsr();  

  /* Poly switch operation*/

  int poly_sw_val = 1-digitalRead(poly_sw_pin);
  if(poly_sw_val != poly_sw_prev)
  {
    poly_sw_prev = poly_sw_val;
    if(poly_sw_val == 0)//Release edge
    {
      poly_held_time = start_time - poly_down_time;
      if(poly_changed == 0)
      {
        if(poly_mode == POLY_LENGTH_LOCK && prev_poly_mode == poly_mode)
        {
          length_lock = 1-length_lock;
        }
        else if(poly_mode == POLY_POLYPHONY)
        {
          if(poly_held_time > POLY_HOLD_TIME)
          {
            aux_pitch.octave = 0;
            aux_pitch.semitone = 0;
          }
          else
          {
            aux_pitch.enabled = 1-aux_pitch.enabled;
            update_lfsr = 1;            
          }
        }
        else if(poly_mode == POLY_RESET && poly_held_time > POLY_HOLD_TIME)
        {
          main_pitch.octave = 0;
          main_pitch.semitone = 0;
          aux_pitch.octave = 0;
          aux_pitch.semitone = 0;
        }
        
      }
      prev_poly_mode = poly_mode;
    }
    else //Press edge
    {
      poly_changed = 0;
      poly_down_time = start_time;
    }
  }
  if(poly_sw_val == 1)
  {
    poly_held_time = start_time - poly_down_time;
  }

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

  signed char poly_delta = 0;
  if (POLY_ENCODER(prev_iox) == 0)
  {
    if(POLY_ENCODER(iox) == 2)
    {
      poly_delta = -1;
    }
    else if(POLY_ENCODER(iox) == 1)
    {
      poly_delta = 1;
    }
    
  }

  if(poly_sw_val == 1)
  {
    if(poly_delta != 0)
    {
      poly_changed = 1;
      poly_mode += poly_delta;
      if(poly_mode > 5)
      {
        poly_mode -= 6;
      }
      else if(poly_mode < 0)
      {
        poly_mode += 6;
      }
    }
  }
  else if(poly_mode == POLY_POLYPHONY)
  {
    //TODO: configuration sequencing?
  } 


//TEMPORARY

  if (SEMI_ENCODER(prev_iox) == 0)
  {
    if(SEMI_ENCODER(iox) == 2)
    {
      if(poly_mode != POLY_POLYPHONY)
      {
        main_pitch.semitone -= 1;
      }
      else
      {
        aux_pitch.semitone -= 1;
      }
    }
    else if(SEMI_ENCODER(iox) == 1)
    {
      if(poly_mode != POLY_POLYPHONY)
      {
        main_pitch.semitone += 1;
      }
      else
      {
        aux_pitch.semitone += 1;
      }
    }
    
  }

  if (OCT_ENCODER(prev_iox) == 0)
  {
    if(OCT_ENCODER(iox) == 2)
    {
      if(poly_mode != POLY_POLYPHONY)
      {
        main_pitch.octave -= 1;
      }
      else
      {
        aux_pitch.octave -= 1;
      }
    }
    else if(OCT_ENCODER(iox) == 1)
    {
      if(poly_mode != POLY_POLYPHONY)
      {
        main_pitch.octave += 1;
      }
      else
      {
        aux_pitch.octave += 1;
      }
    }
    
  }


  /* Reading some knob values*/

  int voct_fine;
  int voct_cv;
//  //int voct_oct; GLOBAL

  voct_fine = adc_memory[pin_to_channel[voct_fine_pin]];
  voct_cv = adc_memory[pin_to_channel[voct_cv_pin]];
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

  freq_lock = digitalRead(freq_lock_pin);
  
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

  int calc_len;
  calc_len = int(pow(2, 1 + knob_len + cv_len));

  if(length_lock == 0)
  {
    
    len = calc_len;
  }
  else if(poly_mode == POLY_LENGTH_LOCK && poly_sw_val == 0)
  {
    
    if(poly_delta == 1)
    {
      len = get_next_length(len);
    }
    else if (poly_delta == -1)
    {
      len = get_prev_length(len);
    }
  }
  if (len < 2)
  {
    len = 2;
  }
  if (len > 4095)
  {
    len = 4095;

  }

  int param_0_combined = (param_0 << 4);
  /* TODO: make configurable
  if(param_0_alpha > 0)
  {
    param_0_combined = param_0_alpha*65545+(1-param_0_alpha)*param_0_combined;
  }
  else
  {
    param_0_combined = (1+param_0_alpha)*param_0_combined;
  }
  */
  
  new_taps = get_taps(len, param_0_combined, param_1 << 4);

  actual_len = get_actual_length(len);


  /******Update taps and indicators******/
  
  if (taps != new_taps)
  {
    taps_toggle = 1-taps_toggle;
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
    write_lfsr(new_taps, main_pitch.enabled, aux_pitch.enabled);
  }
  taps = new_taps;


//  /******Read and process pitch control knobs******/

  
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

  led_map[LL] = 0; 
  led_map[LC] = 0;
  led_map[LR] = 0;
  led_map[UL] = 0;
  led_map[UC] = 0;
  led_map[UR] = 0;
  /*LED Configuration*/
  if(poly_sw_prev == 0)
  {
    if(poly_mode == POLY_RESET)
    {
      led_map[UL] = blinker;
      led_map[UC] = blinker;
      led_map[UR] = blinker;
    }
    else if(poly_mode == POLY_LENGTH_LOCK)
    {
      LEDS_LFSR1_STATUS(UC)
      LEDS_LFSR0_PITCH(UL, UR)
      LEDS_FINE_STATUS(LL)
      LEDS_TAPS_TOGGLE(LC)
      LEDS_LENGTH_LOCK_STATUS(LR)
    }
    else if(poly_mode == POLY_POLYPHONY)
    {
      LEDS_LFSR1_STATUS(UC)
      LEDS_LFSR1_PITCH(UL, UR)
      LEDS_FINE_STATUS(LL)
      LEDS_TAPS_TOGGLE(LC)
      LEDS_LENGTH_LOCK_STATUS(LR)
    }
    else if(poly_mode == POLY_CAL)
    {
      led_map[LC] = blinker;

      
      float voct_cv_value = -2.95 * (float(adc_memory[voct_cv_channel])/half - 1); //TODO: make this DRY
      int voct_cal_sel;
      if(voct_cv_value < -2.5) // error
      {
        voct_cal_sel = -5;
      }
      else if(voct_cv_value < -1.5) // -2
      {
        voct_cal_sel = -2;
      }
      else if(voct_cv_value < -0.5) // -1
      {
        voct_cal_sel = -1;
      }
      else if(voct_cv_value < 0.5) // 0
      {
        voct_cal_sel = 0;
      }
      else if(voct_cv_value < 1.5) // 1
      {
        voct_cal_sel = 1;
      }
      else if(voct_cv_value < 2.5) // 2
      {
        voct_cal_sel = 2;
      }
      else
      {
        voct_cal_sel = 5;
      }
      
      if(voct_cal_sel == -2 )
      {
        led_map[LL] = 1;
      }
      else if(voct_cal_sel == -1)
      {
        led_map[UL] = 1;
      }
      else if(voct_cal_sel == 0)
      {
        led_map[UC] = 1;
      }
      else if(voct_cal_sel == 1)
      {
        led_map[UR] = 1;
      }
      else if(voct_cal_sel == 2)
      {
        led_map[LR] = 1;
      }
      else if(voct_cal_sel < -2)
      {
        led_map[LL] = blinker;
        led_map[UL] = blinker;
      }
      else if(voct_cal_sel > 2)
      {
        led_map[LR] = blinker;
        led_map[UR] = blinker;
      }

      
    }

  }
  else
  {
    if(poly_changed == 0)
    {
      if((poly_mode == POLY_POLYPHONY || poly_mode == POLY_RESET) && poly_held_time > POLY_HOLD_TIME)
      {
        led_map[led_num_map[poly_mode]] = blinker;
      }
      else
      {
        led_map[led_num_map[poly_mode]] = 1;
      }
    }
    else
    {
      led_map[led_num_map[poly_mode]] = 1;
    }
  }
  
  //REMEMBER
  prev_iox = iox;
  
//
//  /*Terminate debug prints*/
//
// //   Serial.print(actual_len);
// //   Serial.print(",");

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
  Serial.print(actual_len);Serial.print(",");
/* ADC Channel Plotting */



//  Serial.print(adc_memory[voct_cv_channel]);Serial.print(",");
//  Serial.print(adc_memory[len_cv_channel]); Serial.print(",");
//  Serial.print(adc_memory[param_0_cv_channel]); Serial.print(",");
//  Serial.print(adc_memory[voct_atv_channel]); Serial.print(",");
Serial.print(adc_memory[len_knob_channel]); Serial.print(",");
//  Serial.print(adc_memory[voct_fine_channel]); Serial.print(",");
//  Serial.print(adc_memory[param_0_channel]); Serial.print(",");
//  Serial.print(adc_memory[param_1_channel]); Serial.print(",");
//  Serial.print(adc_memory[lfo_channel]); Serial.print(",");


  
  Serial.print("\n");
  
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
