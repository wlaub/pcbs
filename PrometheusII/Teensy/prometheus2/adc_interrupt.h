#ifndef ADC_INTERRUPT_H
#define ADC_INTERRUPT_H

volatile char adc_channel = 0;

//Accumulates ADC measurements for sum and dump filtering
volatile int adc_accum[16] = {0};

//Count samples on each ADC for filtering
volatile int sample_counter[16] = {0};

//Store filtered ADC data for real
volatile int adc_memory[16] = {0};

//Filter configuration.
#define FILTER_SHIFT 3
#define FILTER_COUNT (0x1<<FILTER_SHIFT)


//ADC sample rate measurement
#define PRINT_ADC_RATE(x) \
    Serial.print(adc_counter[x]*1e6/(adc_count_duration));\
    Serial.print(",");

//Number of times the adc interrupt has been called
volatile int adc_counter[16] = {0};
//The time when the adc_counter was last set to 0
int adc_last_time = 0;
//Adc measurement interval in microseconds
#define ADC_MEAS_PERIOD 10000


//ADC channel sequencing

const int voct_cv_channel = pin_to_channel[voct_cv_pin];
const int len_cv_channel = pin_to_channel[len_cv_pin];
const int param_0_cv_channel = pin_to_channel[param_0_cv_pin];
const int voct_fine_channel = pin_to_channel[voct_fine_pin];
const int voct_atv_channel = pin_to_channel[voct_atv_pin];
const int lfo_channel = pin_to_channel[lfo_pin];
const int param_1_channel = pin_to_channel[param_1_pin];
const int len_knob_channel = pin_to_channel[len_knob_pin];
const int param_0_channel = pin_to_channel[param_0_pin];

//adc_sequence used to interleave ADC channels and give more sample rate to high-bandwidth CV inputs (i.e. just v/oct)
#define VOCT_DECIM  voct_cv_channel,
volatile int adc_sequence[] = {
  VOCT_DECIM
  voct_fine_channel,
  VOCT_DECIM
  voct_atv_channel,
  VOCT_DECIM
  param_0_cv_channel,
  VOCT_DECIM
  lfo_channel, 
  VOCT_DECIM
  len_cv_channel, 
  VOCT_DECIM
  param_1_channel, 
  VOCT_DECIM
  len_knob_channel,
  VOCT_DECIM
  param_0_channel,
  };
volatile int adc_seq_index = 0;  
const int adc_seq_length = sizeof(adc_sequence)/sizeof(int);

void adc_interrupt();

void configure_adc()
{
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
  
}

void adc_interrupt()
{
  

  /* ADC read and filter */
  
  //Read values
  adc_accum[adc_channel] += ADC1_R0;

  //Simple sum and dump filtering
  ++sample_counter[adc_channel];
  sample_counter[adc_channel] %= FILTER_COUNT;
  
  //Update buffers
  if(sample_counter[adc_channel] == 0)
  {
    adc_memory[adc_channel] = adc_accum[adc_channel] >> FILTER_SHIFT;
    adc_accum[adc_channel] = 0;
    
    /* ADC performance measurement */
    ++adc_counter[adc_channel];
  }

  /* Channel-specific high speed updates only when new data is available */
  
  if(adc_channel == voct_cv_channel && sample_counter[adc_channel] == 0)
  {  // V/oct pin
    float voct;
    int voct_atv = adc_memory[voct_atv_channel];
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
    
    float voct_cv_value = -2.95 * (float(adc_memory[voct_cv_channel])/half - 1) * voct_atv_value;

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

  /* Select next channel */

  ++adc_seq_index;
  adc_seq_index %= adc_seq_length;
  adc_channel = adc_sequence[adc_seq_index];

  ADC1_HC0 = (0x80|adc_channel);

}


#endif
