#ifndef CONFIG_H
#define CONFIG_H

#pragma once

struct PitchConfig 
{
  signed char octave = 0;
  signed char semitone = 0;
  unsigned char enabled = 0;
  float semitone_val = 0;
};

#define RESET_PITCH_CONFIG(_CONFIG)\
  _CONFIG.octave = 0;\
  _CONFIG.semitone = 0;\
  _CONFIG.semitone_val = 0;\

#define SET_PITCH_CONFIG_SEMITONE(_CONFIG, _VAL)\
  _CONFIG.semitone = _VAL;\
  _CONFIG.semitone_val = float(_VAL)/12.0;\

#define INC_PITCH_CONFIG_SEMITONE(_CONFIG)\
  ++_CONFIG.semitone;\
  _CONFIG.semitone_val = float(_CONFIG.semitone)/12.0;\

#define DEC_PITCH_CONFIG_SEMITONE(_CONFIG)\
  --_CONFIG.semitone;\
  _CONFIG.semitone_val = float(_CONFIG.semitone)/12.0;\


unsigned char global_config[6]= {0};
#define GLOBAL_CONFIG_DETUNE 0
#define GLOBAL_CONFIG_PARAM_CV 4
  
#endif
