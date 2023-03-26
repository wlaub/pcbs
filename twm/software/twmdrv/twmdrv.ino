#include <WS2812Serial.h>

//   Teensy 4.0:  1, 8, 14, 17, 20, //24, 29, 39

#define NUMLED1 30
#define LEDPIN1 20

#define NUMLED2 30
#define LEDPIN2 8

#define NUMLED3 30
#define LEDPIN3 1

#define NUMLED4 30
#define LEDPIN4 14

#define NUMLED5 30
#define LEDPIN5 17

byte drawing_memory1[NUMLED1 * 4];       //  4 bytes per LED for RGBW
byte drawing_memory2[NUMLED2 * 4];       //  4 bytes per LED for RGBW
byte drawing_memory3[NUMLED3 * 4];       //  4 bytes per LED for RGBW
byte drawing_memory4[NUMLED4 * 4];       //  4 bytes per LED for RGBW
byte drawing_memory5[NUMLED5 * 4];       //  4 bytes per LED for RGBW
DMAMEM byte display_memory1[NUMLED1 * 16]; // 16 bytes per LED for RGBW
DMAMEM byte display_memory2[NUMLED2 * 16]; // 16 bytes per LED for RGBW
DMAMEM byte display_memory3[NUMLED3 * 16]; // 16 bytes per LED for RGBW
DMAMEM byte display_memory4[NUMLED4 * 16]; // 16 bytes per LED for RGBW
DMAMEM byte display_memory5[NUMLED5 * 16]; // 16 bytes per LED for RGBW

WS2812Serial leds1(NUMLED1, display_memory1, drawing_memory1, LEDPIN1, WS2812_GRBW);
WS2812Serial leds2(NUMLED2, display_memory2, drawing_memory2, LEDPIN2, WS2812_GRBW);
WS2812Serial leds3(NUMLED3, display_memory3, drawing_memory3, LEDPIN3, WS2812_GRBW);
WS2812Serial leds4(NUMLED4, display_memory4, drawing_memory4, LEDPIN4, WS2812_GRBW);
WS2812Serial leds5(NUMLED5, display_memory5, drawing_memory5, LEDPIN5, WS2812_GRBW);

WS2812Serial leds[5] = {leds1, leds2, leds3, leds4, leds5};
const int led_count[5] = {NUMLED1, NUMLED2, NUMLED3, NUMLED4, NUMLED5};

#define RED    0x00FF0000
#define GREEN  0x0000FF00
#define BLUE   0x000000FF
#define YELLOW 0x00FFD000
#define PINK   0x44F00080
#define ORANGE 0x00FF4200
#define WHITE  0xAA000000

void fill(int i, int color)
{
  for(int j = 0; j < led_count[i]; ++j)
  {
    leds[i].setPixel(j,color);
  }

}

void setup() {
  for(int j = 0; j < 5; ++j)
  {
    leds[j].begin();
    leds[j].setBrightness(255);
    fill(j, 0);
  }
}

volatile byte throb = 0;
volatile int throbdir = 5;

void loop() {
  // draw something
  fill(0, throb<<16);
  fill(1, throb<<8);
  fill(2, throb);
  fill(3, throb<<24);
  fill(4, (255-throb)<<24);

  for(int j = 0; j < 5; ++j)
  {
    leds[j].show();
  }

  if(throbdir > 0 && 255-throbdir <= throb)
  {
    throb = 255;
    throbdir *= -1;
  }
  else if(throbdir < 0 && throb <= -throbdir)
  {
    throb = 0;
    throbdir *= -1;
  }
  else{
    throb += throbdir;
  }

  delay(33); // approx 30 Hz refresh rate
}
