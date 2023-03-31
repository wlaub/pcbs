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

void fill(int i, int color, int spacing)
{
  for(int j = 0; j < led_count[i]; j+=spacing)
  {
    leds[i].setPixel(j,color);
  }

}

void setup() {
  Serial.begin(115200);

  for(int j = 0; j < 5; ++j)
  {
    leds[j].begin();
    leds[j].setBrightness(255);
    fill(j, 0,1);
  }
  pinMode(13, OUTPUT);
  digitalWrite(13, 1);
}

volatile byte throb = 0;
volatile int throbdir = 5;

volatile int serial_offset = 0;
volatile int serial_state = 0;
volatile int serial_index = 0;

byte asc_to_byte(byte value)
{
  if(value >= '0' && value <= '9')
  {
    return value-'0';
  }
  if(value >='a' && value <= 'f')
  {
    return value-'a' + 10;
  }
  if(value >='A' && value <= 'F')
  {
    return value-'A' + 10;
  }
  return 0xff;
}

void loop() {

  unsigned int available = Serial.available();
  if (serial_state == 0 && available > 0)
  {
    serial_index = Serial.read();
    if(serial_index >= 0 && serial_index < 5)
    {
      serial_state = 1;
      serial_offset = 0;
    }
    
  }
  else if (serial_state == 1 && available >= 8)
  {
    unsigned int color = 0;
    byte new_byte = 0;
    for(int i = 0; i < 4; ++i)
    {
      byte upper = asc_to_byte(Serial.read());
      byte lower = asc_to_byte(Serial.read());
      if(upper > 0xf)
      {
        serial_state = 0;
        leds[serial_index].show();
      }
      else
      {
        new_byte = (upper<<4)|(lower);
        color <<= 8;
        color |= new_byte;
      }
    }
    if (serial_state == 1)
    {
      leds[serial_index].setPixel(serial_offset, color);
      serial_offset += 1;
    }
  }

  delay(1); // approx 30 Hz refresh rate
}
