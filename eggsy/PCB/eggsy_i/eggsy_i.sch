EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 14
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 4000 2000 1000 500 
U 60693B66
F0 "12V Current Sense" 50
F1 "12v_current_sense.sch" 50
F2 "12VOUT" O R 5000 2100 50 
F3 "12V_I" O R 5000 2400 50 
F4 "12VIN" I L 4000 2100 50 
$EndSheet
$Sheet
S 4000 1000 1000 500 
U 60693B99
F0 "5V Current Sense" 50
F1 "5v_current_sense.sch" 50
F2 "5VOUT" O R 5000 1100 50 
F3 "5V_I" O R 5000 1400 50 
F4 "5VIN" I L 4000 1100 50 
$EndSheet
$Sheet
S 4000 3000 1000 500 
U 60693BCC
F0 "-12 V Current Snese" 50
F1 "-12v_current_sense.sch" 50
F2 "-12VOUT" O R 5000 3100 50 
F3 "-12V_I" O R 5000 3400 50 
F4 "-12VIN" I L 4000 3100 50 
$EndSheet
$Sheet
S 6500 1000 1000 500 
U 60693C2D
F0 "12 V Switch" 50
F1 "12v_switch.sch" 50
F2 "5VIN" I L 6500 1100 50 
F3 "5VOUT" O R 7500 1100 50 
F4 "5V_PGOOD" O R 7500 1250 50 
F5 "5V_FAULT" O R 7500 1400 50 
F6 "5V_EN" I L 6500 1400 50 
$EndSheet
$Sheet
S 6500 2000 1000 500 
U 60693C5F
F0 "5 V Switch" 50
F1 "5v_switch.sch" 50
F2 "12VIN" I L 6500 2100 50 
F3 "12VOUT" O R 7500 2100 50 
F4 "12V_PGOOD" O R 7500 2250 50 
F5 "12V_FAULT" O R 7500 2400 50 
F6 "12V_EN" I L 6500 2400 50 
$EndSheet
$Sheet
S 6500 3000 1000 500 
U 60693C7C
F0 "-12 V Switch" 50
F1 "-12v_switch.sch" 50
F2 "-12VIN" I L 6500 3100 50 
F3 "-12VOUT" O R 7500 3100 50 
F4 "-12V_PGOOD" O R 7500 3250 50 
F5 "-12V_FAULT" O R 7500 3400 50 
F6 "-12V_EN" I L 6500 3400 50 
$EndSheet
$Sheet
S 8500 1600 1000 1000
U 60693C9A
F0 "Power Exuent" 50
F1 "power_exuent.sch" 50
F2 "5V" I L 8500 1900 50 
F3 "12V" I L 8500 2100 50 
F4 "-12V" I L 8500 2300 50 
F5 "5V_V" O R 9500 2000 50 
F6 "12V_V" O R 9500 2100 50 
F7 "-12V_V" O R 9500 2200 50 
$EndSheet
$Sheet
S 6500 4000 1000 1900
U 60693D62
F0 "Microcontroller" 50
F1 "microcontroller.sch" 50
F2 "VOUT_EN" I L 6500 4100 50 
F3 "5V_I" I L 6500 4250 50 
F4 "12V_I" I L 6500 4350 50 
F5 "-12V_I" I L 6500 4450 50 
F6 "5V_V" I R 7500 5600 50 
F7 "12V_V" I R 7500 5700 50 
F8 "-12V_V" I R 7500 5800 50 
F9 "5V_PGOOD" I R 7500 4100 50 
F10 "12V_PGOOD" I R 7500 4200 50 
F11 "-12V_PGOOD" I R 7500 4300 50 
F12 "5V_FAULT" I R 7500 4500 50 
F13 "12V_FAULT" I R 7500 4600 50 
F14 "-12V_FAULT" I R 7500 4700 50 
F15 "POWER_SW" I R 7500 4900 50 
F16 "PROG_SW" I R 7500 5000 50 
F17 "12V_REF_EN" O L 6500 5300 50 
F18 "5V_REF_EN" O L 6500 5200 50 
F19 "-12V_REF_EN" O L 6500 5400 50 
F20 "STATUS0" O R 7500 5200 50 
F21 "STATUS1" O R 7500 5300 50 
$EndSheet
$Sheet
S 4000 4000 1000 500 
U 60693DAC
F0 "12/5 V Current Reference" 50
F1 "5_12_current_ref.sch" 50
F2 "5VIN" I R 5000 4100 50 
F3 "5V_EN" I R 5000 4300 50 
F4 "12VIN" I R 5000 4200 50 
F5 "12V_EN" I R 5000 4400 50 
$EndSheet
$Sheet
S 4000 5000 1000 500 
U 60693E11
F0 "-12 V Current Reference" 50
F1 "-12_current_ref.sch" 50
F2 "-12VIN" I R 5000 5100 50 
F3 "EN" I R 5000 5400 50 
$EndSheet
$Sheet
S 2050 3750 950  1000
U 60694FB6
F0 "Power Supplies" 50
F1 "power_supplies.sch" 50
$EndSheet
$Sheet
S 2000 1600 1000 1000
U 60693B3F
F0 "Power Entry" 50
F1 "power_entry.sch" 50
F2 "5V" O R 3000 1900 50 
F3 "12V" O R 3000 2100 50 
F4 "-12V" O R 3000 2300 50 
$EndSheet
Wire Wire Line
	3000 1900 3500 1900
Wire Wire Line
	3500 1900 3500 1100
Wire Wire Line
	3500 1100 4000 1100
Wire Wire Line
	3000 2100 4000 2100
Wire Wire Line
	3000 2300 3500 2300
Wire Wire Line
	3500 2300 3500 3100
Wire Wire Line
	3500 3100 4000 3100
Wire Wire Line
	5000 2100 5150 2100
Wire Wire Line
	5000 3100 5300 3100
Wire Wire Line
	5000 1100 5100 1100
Wire Wire Line
	5100 1100 5100 4100
Wire Wire Line
	5100 4100 5000 4100
Connection ~ 5100 1100
Wire Wire Line
	5100 1100 6500 1100
Wire Wire Line
	5150 2100 5150 4200
Wire Wire Line
	5150 4200 5000 4200
Connection ~ 5150 2100
Wire Wire Line
	5150 2100 6500 2100
Wire Wire Line
	5300 3100 5300 5100
Wire Wire Line
	5300 5100 5000 5100
Connection ~ 5300 3100
Wire Wire Line
	5300 3100 6500 3100
Wire Wire Line
	6500 4100 6400 4100
Wire Wire Line
	6400 4100 6400 3400
Wire Wire Line
	6400 3400 6500 3400
Wire Wire Line
	6400 3400 6400 2400
Wire Wire Line
	6400 2400 6500 2400
Connection ~ 6400 3400
Wire Wire Line
	6400 2400 6400 1400
Wire Wire Line
	6400 1400 6500 1400
Connection ~ 6400 2400
Wire Wire Line
	5000 1400 6100 1400
Wire Wire Line
	6100 1400 6100 3650
Wire Wire Line
	6100 4250 6500 4250
Wire Wire Line
	6500 4350 6000 4350
Wire Wire Line
	6000 2400 5000 2400
Wire Wire Line
	6500 4450 5900 4450
Wire Wire Line
	5900 4450 5900 3850
Wire Wire Line
	5900 3400 5000 3400
Wire Wire Line
	5700 5200 5700 4300
Wire Wire Line
	5700 4300 5000 4300
Wire Wire Line
	5700 5200 6500 5200
Wire Wire Line
	5600 5300 5600 4400
Wire Wire Line
	5600 4400 5000 4400
Wire Wire Line
	5600 5300 6500 5300
Wire Wire Line
	8500 1900 8250 1900
Wire Wire Line
	8250 1900 8250 1100
Wire Wire Line
	8250 1100 7500 1100
Wire Wire Line
	8500 2100 7500 2100
Wire Wire Line
	8500 2300 8250 2300
Wire Wire Line
	8250 2300 8250 3100
Wire Wire Line
	8250 3100 7500 3100
Wire Wire Line
	8500 3650 6100 3650
Connection ~ 6100 3650
Wire Wire Line
	6100 3650 6100 4250
Wire Wire Line
	8500 3750 6000 3750
Connection ~ 6000 3750
Wire Wire Line
	6000 3750 6000 2400
Wire Wire Line
	7500 4300 7650 4300
Wire Wire Line
	7500 4700 7600 4700
Wire Wire Line
	7500 4900 8500 4900
Wire Wire Line
	8500 5000 7500 5000
Wire Wire Line
	7500 4100 8050 4100
Wire Wire Line
	7500 4500 8000 4500
Wire Wire Line
	7500 3400 7600 3400
Wire Wire Line
	7600 3400 7600 4700
Wire Wire Line
	7500 3250 7650 3250
Wire Wire Line
	7650 3250 7650 4300
Wire Wire Line
	7500 2400 7800 2400
Wire Wire Line
	7800 2400 7800 4600
Wire Wire Line
	7800 4600 7500 4600
Wire Wire Line
	7500 2250 7850 2250
Wire Wire Line
	7850 2250 7850 4200
Wire Wire Line
	7850 4200 7500 4200
Wire Wire Line
	8000 1400 8000 4500
Wire Wire Line
	7500 1400 8000 1400
Wire Wire Line
	8050 4100 8050 1250
Wire Wire Line
	7500 1250 8050 1250
Wire Wire Line
	9500 2200 9650 2200
Wire Wire Line
	9500 2100 9700 2100
Wire Wire Line
	9700 2100 9700 5700
Wire Wire Line
	9750 5600 9750 2000
Wire Wire Line
	9750 2000 9500 2000
Wire Wire Line
	6000 3750 6000 4350
Wire Wire Line
	8500 3850 5900 3850
Connection ~ 5900 3850
Wire Wire Line
	5900 3850 5900 3400
$Sheet
S 8500 3500 1000 1950
U 60693CC8
F0 "Panel Controls" 50
F1 "panel_controls.sch" 50
F2 "POWER_SW" O L 8500 4900 50 
F3 "PROG_SW" O L 8500 5000 50 
F4 "5V_I" I L 8500 3650 50 
F5 "12V_I" I L 8500 3750 50 
F6 "-12V_I" I L 8500 3850 50 
F7 "5V_PGOOD" I L 8500 4100 50 
F8 "12V_PGOOD" I L 8500 4200 50 
F9 "-12V_PGOOD" I L 8500 4300 50 
F10 "5V_FAULT" I L 8500 4500 50 
F11 "12V_FAULT" I L 8500 4600 50 
F12 "-12V_FAULT" I L 8500 4700 50 
F13 "STATUS0" I L 8500 5200 50 
F14 "STATUS1" I L 8500 5300 50 
$EndSheet
Wire Wire Line
	7500 5600 9750 5600
Wire Wire Line
	7500 5700 9700 5700
Wire Wire Line
	9650 2200 9650 5800
Wire Wire Line
	7500 5800 9650 5800
Wire Wire Line
	8050 4100 8500 4100
Connection ~ 8050 4100
Wire Wire Line
	8500 4200 7850 4200
Connection ~ 7850 4200
Wire Wire Line
	7650 4300 8500 4300
Connection ~ 7650 4300
Connection ~ 7600 4700
Wire Wire Line
	7600 4700 8500 4700
Wire Wire Line
	8500 4600 7800 4600
Connection ~ 7800 4600
Wire Wire Line
	8000 4500 8500 4500
Connection ~ 8000 4500
Wire Wire Line
	5000 5400 6500 5400
Wire Wire Line
	7500 5200 8500 5200
Wire Wire Line
	8500 5300 7500 5300
$EndSCHEMATC
