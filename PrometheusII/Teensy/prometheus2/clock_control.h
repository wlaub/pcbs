#ifndef CLOCK_CONTROL_H
#define CLOCK_CONTROL_H

#include "imxrt.h"

/*
    {1, M(1, 1), 0, 4},  // FlexPWM1_1_X   0  // AD_B0_03
    {1, M(1, 0), 0, 4},  // FlexPWM1_0_X   1  // AD_B0_02
M(1,1) = 0|1 = 1
M(1,0) = 0|0 = 0
type, module, channel, muxval
0: 1,1,0,4
1: 1,0,0,4
sub module = module & 0x03 == module in this case

~/Downloads/arduino-1.8.10/hardware/teensy/avr/cores/teensy4

*/

/*
This is the flexpwmFrequency and flexpwmWrite functions from cores/teense4/pwm.c adapted to use pin 0 specifically with a duty cycle of 50%
This substantially improves performancy be eliminating a lot of unneed conditionals and calculations. 
*/
void clock_0_write_freq(float frequency)
{
    IMXRT_FLEXPWM_t *p = &IMXRT_FLEXPWM1; //When module < 8
    uint16_t mask = 1 << 1;
    uint32_t olddiv = p->SM[1].VAL1;
    uint32_t newdiv = (uint32_t)((float)F_BUS_ACTUAL / frequency + 0.5);
    uint32_t prescale = 0;
    while (newdiv > 65535 && prescale < 7) {
        newdiv = newdiv >> 1; 
        prescale = prescale + 1;
    }
    if (newdiv > 65535) {
        newdiv = 65535; 
    } else if (newdiv < 2) {
        newdiv = 2;
    }
    p->MCTRL |= FLEXPWM_MCTRL_CLDOK(mask);

    
    p->SM[1].CTRL = FLEXPWM_SMCTRL_FULL | FLEXPWM_SMCTRL_PRSC(prescale);
    p->SM[1].VAL1 = newdiv - 1;
    p->SM[1].VAL0 = (p->SM[1].VAL0 * newdiv) / olddiv;
    p->SM[1].VAL3 = (p->SM[1].VAL3 * newdiv) / olddiv;
    p->SM[1].VAL5 = (p->SM[1].VAL5 * newdiv) / olddiv;

    p->SM[1].VAL0 = newdiv >> 1;
    p->OUTEN |= FLEXPWM_OUTEN_PWMX_EN(mask);
    
    p->MCTRL |= FLEXPWM_MCTRL_LDOK(mask);
  
}

/*
This is the same thing done for pin 1
*/

void clock_1_write_freq(float frequency)
{
    IMXRT_FLEXPWM_t *p = &IMXRT_FLEXPWM1; //When module < 8
    uint16_t mask = 1 << 0;
    uint32_t olddiv = p->SM[0].VAL1;
    uint32_t newdiv = (uint32_t)((float)F_BUS_ACTUAL / frequency + 0.5);
    uint32_t prescale = 0;
    while (newdiv > 65535 && prescale < 7) {
        newdiv = newdiv >> 1; 
        prescale = prescale + 1;
    }
    if (newdiv > 65535) {
        newdiv = 65535; 
    } else if (newdiv < 2) {
        newdiv = 2;
    }
    p->MCTRL |= FLEXPWM_MCTRL_CLDOK(mask);

    p->SM[0].CTRL = FLEXPWM_SMCTRL_FULL | FLEXPWM_SMCTRL_PRSC(prescale);
    p->SM[0].VAL1 = newdiv - 1;
    p->SM[0].VAL0 = (p->SM[0].VAL0 * newdiv) / olddiv;
    p->SM[0].VAL3 = (p->SM[0].VAL3 * newdiv) / olddiv;
    p->SM[0].VAL5 = (p->SM[0].VAL5 * newdiv) / olddiv;

    p->SM[0].VAL0 = newdiv >> 1;
    p->OUTEN |= FLEXPWM_OUTEN_PWMX_EN(mask);
    
    p->MCTRL |= FLEXPWM_MCTRL_LDOK(mask);
    *(portConfigRegister(1)) = 4;  //I think this is not required in the pin 0 case because that one doesn't ever change configuration
}

#endif
