#ifndef LEDS_H
#define LEDS_H

#pragma once

volatile int led_index = 0;
//0 = L, 1 = H, 2 = Z. These are the pin states necessary to light a given LED
//THe order seems to matter. I believe I selected it to avoid reverse biasing an LED immediately after it has been lit
//                   U L U L L U N
//                   R R C C L L A
char led0_state[] = {0,1,2,2,0,1,2};
char led1_state[] = {1,0,0,1,2,2,2};
char led2_state[] = {2,2,1,0,1,0,2};


#define UR 0
#define LR 1
#define UC 2
#define LC 3
#define LL 4
#define UL 5

char led_num_map[] = {UL, UC, UR, LL, LC, LR};

// Upper right, lower right, upper middle, lower middle, upper left, lower left
// Upper left, upper middle, upper right, lower left, lower middle, lower right
char led_map[] = {0,0,0,0,0,0};

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

#endif
