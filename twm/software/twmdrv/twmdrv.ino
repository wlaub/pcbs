#include <WS2812Serial.h>

//   Teensy 4.0:  1, 8, 14, 17, 20, 24, 29, 39

const int numled1 = 30;
const int pin1 = 8;
byte drawingMemory1[numled1 * 4];       //  4 bytes per LED for RGBW
DMAMEM byte displayMemory1[numled1 * 16]; // 16 bytes per LED for RGBW
WS2812Serial leds1(numled1, displayMemory1, drawingMemory1, pin1, WS2812_GRBW);

#define RED    0x00FF0000
#define GREEN  0x0000FF00
#define BLUE   0x000000FF
#define YELLOW 0x00FFD000
#define PINK   0x44F00080
#define ORANGE 0x00FF4200
#define WHITE  0xAA000000

void setup() {
  leds1.begin();
  leds1.setBrightness(255);
  for (int i = 0; i < numled1; ++i)
  {
    leds1.setPixel(i, 0);
  }
}

volatile byte red = 0;
volatile byte green = 60;
volatile byte blue = 120;
volatile byte white = 0;
volatile int offset = 0;
volatile int offdir = 1;

void loop() {
  // draw something
  int color = 0;
  //color |= blue;
  //color |= green<<8;
  color |= red<<16;
  //color |= white<<24;
  for (int i = 0; i < numled1; i+=1)
  {
    leds1.setPixel(i, color);
  }
  leds1.show();
  red +=1;
  blue +=2;
  green +=3;
  offset +=offdir;
  if(offset >= numled1)
  {
    offdir = -1;
    offset = numled1-1;
  }
  else if(offset < 0)
  {
    offdir = 1;
    offset = 0;
  }
  delay(33); // approx 30 Hz refresh rate
}
