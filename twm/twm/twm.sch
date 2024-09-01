EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L teensy:Teensy4.0_NoUnderpins U2
U 1 1 640E1BB3
P 8750 2500
F 0 "U2" H 8750 4115 50  0000 C CNN
F 1 "Teensy4.0_NoUnderpins" H 8750 4024 50  0000 C CNN
F 2 "ttt_lib:Teensy40_outerpins" H 8350 3400 50  0001 C CNN
F 3 "" H 8350 3400 50  0001 C CNN
	1    8750 2500
	1    0    0    -1  
$EndComp
$Comp
L Connector:Barrel_Jack J6
U 1 1 640E3473
P 8350 4800
F 0 "J6" H 8120 4850 50  0000 R CNN
F 1 "Barrel_Jack" H 8120 4759 50  0000 R CNN
F 2 "Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal_CircularHoles" H 8400 4760 50  0001 C CNN
F 3 "~" H 8400 4760 50  0001 C CNN
	1    8350 4800
	-1   0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J5
U 1 1 640E4A96
P 950 7150
F 0 "J5" H 1007 7817 50  0000 C CNN
F 1 "RJ45" H 1007 7726 50  0000 C CNN
F 2 "ttt_lib:MJ3225-88-0" V 950 7175 50  0001 C CNN
F 3 "~" V 950 7175 50  0001 C CNN
	1    950  7150
	1    0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J4
U 1 1 640F089F
P 950 5650
F 0 "J4" H 1007 6317 50  0000 C CNN
F 1 "RJ45" H 1007 6226 50  0000 C CNN
F 2 "ttt_lib:MJ3225-88-0" V 950 5675 50  0001 C CNN
F 3 "~" V 950 5675 50  0001 C CNN
	1    950  5650
	1    0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J3
U 1 1 640F0F97
P 950 4150
F 0 "J3" H 1007 4817 50  0000 C CNN
F 1 "RJ45" H 1007 4726 50  0000 C CNN
F 2 "ttt_lib:MJ3225-88-0" V 950 4175 50  0001 C CNN
F 3 "~" V 950 4175 50  0001 C CNN
	1    950  4150
	1    0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J2
U 1 1 640F14DE
P 950 2650
F 0 "J2" H 1007 3317 50  0000 C CNN
F 1 "RJ45" H 1007 3226 50  0000 C CNN
F 2 "ttt_lib:MJ3225-88-0" V 950 2675 50  0001 C CNN
F 3 "~" V 950 2675 50  0001 C CNN
	1    950  2650
	1    0    0    -1  
$EndComp
$Comp
L Connector:RJ45 J1
U 1 1 640F19E1
P 950 1150
F 0 "J1" H 1007 1817 50  0000 C CNN
F 1 "RJ45" H 1007 1726 50  0000 C CNN
F 2 "ttt_lib:MJ3225-88-0" V 950 1175 50  0001 C CNN
F 3 "~" V 950 1175 50  0001 C CNN
	1    950  1150
	1    0    0    -1  
$EndComp
$Comp
L 2023-03-12_18-55-49:CD4504BPWR U1
U 1 1 64106F55
P 4700 1900
F 0 "U1" H 4700 2788 60  0000 C CNN
F 1 "CD4504BPWR" H 4700 2682 60  0000 C CNN
F 2 "footprints:CD4504BPWR" H 4700 1840 60  0001 C CNN
F 3 "" H 4700 1900 60  0000 C CNN
	1    4700 1900
	-1   0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0101
U 1 1 6410F59D
P 7700 4400
F 0 "#PWR0101" H 7700 4250 50  0001 C CNN
F 1 "+5V" H 7715 4573 50  0000 C CNN
F 2 "" H 7700 4400 50  0001 C CNN
F 3 "" H 7700 4400 50  0001 C CNN
	1    7700 4400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 6410FC87
P 7700 5150
F 0 "#PWR0102" H 7700 4900 50  0001 C CNN
F 1 "GND" H 7705 4977 50  0000 C CNN
F 2 "" H 7700 5150 50  0001 C CNN
F 3 "" H 7700 5150 50  0001 C CNN
	1    7700 5150
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0103
U 1 1 641102ED
P 10100 1000
F 0 "#PWR0103" H 10100 850 50  0001 C CNN
F 1 "+3.3V" H 10115 1173 50  0000 C CNN
F 2 "" H 10100 1000 50  0001 C CNN
F 3 "" H 10100 1000 50  0001 C CNN
	1    10100 1000
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0104
U 1 1 64117FFE
P 5800 700
F 0 "#PWR0104" H 5800 550 50  0001 C CNN
F 1 "+3.3V" H 5815 873 50  0000 C CNN
F 2 "" H 5800 700 50  0001 C CNN
F 3 "" H 5800 700 50  0001 C CNN
	1    5800 700 
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0105
U 1 1 64119B0C
P 6150 700
F 0 "#PWR0105" H 6150 550 50  0001 C CNN
F 1 "+5V" H 6165 873 50  0000 C CNN
F 2 "" H 6150 700 50  0001 C CNN
F 3 "" H 6150 700 50  0001 C CNN
	1    6150 700 
	1    0    0    -1  
$EndComp
Wire Wire Line
	5800 1400 5800 950 
Wire Wire Line
	5500 1400 5800 1400
Wire Wire Line
	5500 1600 6150 1600
Wire Wire Line
	6150 1600 6150 950 
Wire Wire Line
	10100 1000 10100 1050
Wire Wire Line
	10100 1400 9850 1400
$Comp
L power:GND #PWR0106
U 1 1 6412C68A
P 3700 2700
F 0 "#PWR0106" H 3700 2450 50  0001 C CNN
F 1 "GND" H 3705 2527 50  0000 C CNN
F 2 "" H 3700 2700 50  0001 C CNN
F 3 "" H 3700 2700 50  0001 C CNN
	1    3700 2700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 6412CA60
P 10300 2700
F 0 "#PWR0107" H 10300 2450 50  0001 C CNN
F 1 "GND" H 10305 2527 50  0000 C CNN
F 2 "" H 10300 2700 50  0001 C CNN
F 3 "" H 10300 2700 50  0001 C CNN
	1    10300 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	10300 1300 10300 1600
Wire Wire Line
	9850 1300 10300 1300
Wire Wire Line
	8050 4700 7700 4700
Wire Wire Line
	7700 4700 7700 4550
Wire Wire Line
	7700 4900 7700 5050
Wire Wire Line
	7700 4900 8050 4900
Wire Wire Line
	3900 2500 3700 2500
Wire Wire Line
	3700 2500 3700 2700
$Comp
L Device:R R7
U 1 1 6413AA71
P 5800 2800
F 0 "R7" H 5870 2846 50  0000 L CNN
F 1 "0" H 5870 2755 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 5730 2800 50  0001 C CNN
F 3 "~" H 5800 2800 50  0001 C CNN
	1    5800 2800
	1    0    0    -1  
$EndComp
$Comp
L Device:C C6
U 1 1 6414D0E7
P 5950 1250
F 0 "C6" H 6065 1296 50  0000 L CNN
F 1 "C" H 6065 1205 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 5988 1100 50  0001 C CNN
F 3 "~" H 5950 1250 50  0001 C CNN
	1    5950 1250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C7
U 1 1 6414FFB7
P 6400 1250
F 0 "C7" H 6515 1296 50  0000 L CNN
F 1 "C" H 6515 1205 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 6438 1100 50  0001 C CNN
F 3 "~" H 6400 1250 50  0001 C CNN
	1    6400 1250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C10
U 1 1 6415041D
P 10600 1250
F 0 "C10" H 10715 1296 50  0000 L CNN
F 1 "C" H 10715 1205 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 10638 1100 50  0001 C CNN
F 3 "~" H 10600 1250 50  0001 C CNN
	1    10600 1250
	1    0    0    -1  
$EndComp
$Comp
L Device:C C8
U 1 1 64150901
P 7300 4800
F 0 "C8" H 7415 4846 50  0000 L CNN
F 1 "C" H 7415 4755 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 7338 4650 50  0001 C CNN
F 3 "~" H 7300 4800 50  0001 C CNN
	1    7300 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	7300 4650 7300 4550
Wire Wire Line
	7300 4550 7700 4550
Connection ~ 7700 4550
Wire Wire Line
	7700 4550 7700 4400
Wire Wire Line
	7300 4950 7300 5050
Wire Wire Line
	7300 5050 7700 5050
Connection ~ 7700 5050
Wire Wire Line
	7700 5050 7700 5150
Wire Wire Line
	5950 1100 5950 950 
Wire Wire Line
	5950 950  5800 950 
Connection ~ 5800 950 
Wire Wire Line
	5800 950  5800 700 
Wire Wire Line
	6400 1100 6400 950 
Wire Wire Line
	6400 950  6150 950 
Connection ~ 6150 950 
Wire Wire Line
	6150 950  6150 700 
$Comp
L power:GND #PWR0110
U 1 1 6419AE9F
P 5950 1400
F 0 "#PWR0110" H 5950 1150 50  0001 C CNN
F 1 "GND" H 5955 1227 50  0000 C CNN
F 2 "" H 5950 1400 50  0001 C CNN
F 3 "" H 5950 1400 50  0001 C CNN
	1    5950 1400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0111
U 1 1 6419B73F
P 6400 1400
F 0 "#PWR0111" H 6400 1150 50  0001 C CNN
F 1 "GND" H 6405 1227 50  0000 C CNN
F 2 "" H 6400 1400 50  0001 C CNN
F 3 "" H 6400 1400 50  0001 C CNN
	1    6400 1400
	1    0    0    -1  
$EndComp
$Comp
L Device:R R8
U 1 1 641A0B19
P 6100 2800
F 0 "R8" H 6170 2846 50  0000 L CNN
F 1 "0" H 6170 2755 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 6030 2800 50  0001 C CNN
F 3 "~" H 6100 2800 50  0001 C CNN
	1    6100 2800
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0112
U 1 1 641A8348
P 6350 3050
F 0 "#PWR0112" H 6350 2900 50  0001 C CNN
F 1 "+3.3V" H 6365 3223 50  0000 C CNN
F 2 "" H 6350 3050 50  0001 C CNN
F 3 "" H 6350 3050 50  0001 C CNN
	1    6350 3050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0113
U 1 1 641AB786
P 5800 3050
F 0 "#PWR0113" H 5800 2800 50  0001 C CNN
F 1 "GND" H 5805 2877 50  0000 C CNN
F 2 "" H 5800 3050 50  0001 C CNN
F 3 "" H 5800 3050 50  0001 C CNN
	1    5800 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	5500 2500 5800 2500
Wire Wire Line
	6100 2500 6100 2650
Connection ~ 5800 2500
Wire Wire Line
	5800 2500 6100 2500
Wire Wire Line
	5800 2950 5800 3050
Wire Wire Line
	6100 2950 6100 3150
Wire Wire Line
	6100 3150 6350 3150
Wire Wire Line
	6350 3150 6350 3050
$Comp
L power:+5V #PWR0115
U 1 1 6426E8FB
P 1700 700
F 0 "#PWR0115" H 1700 550 50  0001 C CNN
F 1 "+5V" H 1715 873 50  0000 C CNN
F 2 "" H 1700 700 50  0001 C CNN
F 3 "" H 1700 700 50  0001 C CNN
	1    1700 700 
	1    0    0    -1  
$EndComp
Connection ~ 1700 6450
Connection ~ 1700 4900
Connection ~ 1700 3450
Connection ~ 1700 1950
Wire Wire Line
	10100 1050 10600 1050
Wire Wire Line
	10600 1050 10600 1100
Connection ~ 10100 1050
Wire Wire Line
	10100 1050 10100 1400
Wire Wire Line
	10600 1600 10300 1600
Connection ~ 10300 1600
Wire Wire Line
	10300 1600 10300 2700
Wire Wire Line
	10600 1400 10600 1600
Wire Wire Line
	5800 2500 5800 2650
$Comp
L Device:R R10
U 1 1 643BAC06
P 6900 1800
F 0 "R10" H 6970 1846 50  0000 L CNN
F 1 "0" H 6970 1755 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 6830 1800 50  0001 C CNN
F 3 "~" H 6900 1800 50  0001 C CNN
	1    6900 1800
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R11
U 1 1 643C196A
P 6900 2000
F 0 "R11" H 6970 2046 50  0000 L CNN
F 1 "0" H 6970 1955 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 6830 2000 50  0001 C CNN
F 3 "~" H 6900 2000 50  0001 C CNN
	1    6900 2000
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R12
U 1 1 643C83FA
P 6900 2200
F 0 "R12" H 6970 2246 50  0000 L CNN
F 1 "0" H 6970 2155 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 6830 2200 50  0001 C CNN
F 3 "~" H 6900 2200 50  0001 C CNN
	1    6900 2200
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R13
U 1 1 643CEE52
P 6900 2400
F 0 "R13" H 6970 2446 50  0000 L CNN
F 1 "0" H 6970 2355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 6830 2400 50  0001 C CNN
F 3 "~" H 6900 2400 50  0001 C CNN
	1    6900 2400
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R9
U 1 1 643E6940
P 6900 1600
F 0 "R9" H 6970 1646 50  0000 L CNN
F 1 "0" H 6970 1555 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 6830 1600 50  0001 C CNN
F 3 "~" H 6900 1600 50  0001 C CNN
	1    6900 1600
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R14
U 1 1 6443A96B
P 5950 3800
F 0 "R14" H 6020 3846 50  0000 L CNN
F 1 "0" H 6020 3755 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 5880 3800 50  0001 C CNN
F 3 "~" H 5950 3800 50  0001 C CNN
	1    5950 3800
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0121
U 1 1 64444451
P 6200 4000
F 0 "#PWR0121" H 6200 3750 50  0001 C CNN
F 1 "GND" H 6205 3827 50  0000 C CNN
F 2 "" H 6200 4000 50  0001 C CNN
F 3 "" H 6200 4000 50  0001 C CNN
	1    6200 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 3800 6200 4000
Wire Wire Line
	6100 3800 6200 3800
$Comp
L Device:R R6
U 1 1 6446B92D
P 3700 1600
F 0 "R6" H 3770 1646 50  0000 L CNN
F 1 "0" H 3770 1555 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 3630 1600 50  0001 C CNN
F 3 "~" H 3700 1600 50  0001 C CNN
	1    3700 1600
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0122
U 1 1 6447DC33
P 7250 1100
F 0 "#PWR0122" H 7250 850 50  0001 C CNN
F 1 "GND" H 7255 927 50  0000 C CNN
F 2 "" H 7250 1100 50  0001 C CNN
F 3 "" H 7250 1100 50  0001 C CNN
	1    7250 1100
	0    1    1    0   
$EndComp
Wire Wire Line
	7650 1150 7250 1150
Wire Wire Line
	7250 1150 7250 1100
Wire Wire Line
	7150 1250 7150 1600
Wire Wire Line
	7150 1600 7050 1600
Wire Wire Line
	7150 1250 7650 1250
Wire Wire Line
	7650 1450 7250 1450
Wire Wire Line
	7250 1450 7250 1800
Wire Wire Line
	7250 1800 7050 1800
Wire Wire Line
	7650 1650 7350 1650
Wire Wire Line
	7350 1650 7350 2000
Wire Wire Line
	7350 2000 7050 2000
Wire Wire Line
	7450 1850 7650 1850
Wire Wire Line
	7650 2050 7550 2050
Wire Wire Line
	5500 1900 5900 1900
Wire Wire Line
	6550 1800 6550 2200
Wire Wire Line
	6550 1800 6750 1800
Wire Wire Line
	6100 1700 6650 1700
Wire Wire Line
	6650 1700 6650 1600
Wire Wire Line
	6650 1600 6750 1600
Wire Wire Line
	2800 2200 3900 2200
Wire Wire Line
	2100 1950 1700 1950
Wire Wire Line
	2100 2000 2100 1950
Wire Wire Line
	2150 3450 1700 3450
Wire Wire Line
	2150 3500 2150 3450
Wire Wire Line
	2150 4900 1700 4900
Wire Wire Line
	2150 5000 2150 4900
Wire Wire Line
	2150 6450 1700 6450
Wire Wire Line
	2150 6500 2150 6450
$Comp
L power:GND #PWR0120
U 1 1 643265DF
P 2150 6800
F 0 "#PWR0120" H 2150 6550 50  0001 C CNN
F 1 "GND" H 2155 6627 50  0000 C CNN
F 2 "" H 2150 6800 50  0001 C CNN
F 3 "" H 2150 6800 50  0001 C CNN
	1    2150 6800
	1    0    0    -1  
$EndComp
$Comp
L Device:C C5
U 1 1 643265D9
P 2150 6650
F 0 "C5" H 2265 6696 50  0000 L CNN
F 1 "C" H 2265 6605 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2188 6500 50  0001 C CNN
F 3 "~" H 2150 6650 50  0001 C CNN
	1    2150 6650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0119
U 1 1 64320CB1
P 2150 5300
F 0 "#PWR0119" H 2150 5050 50  0001 C CNN
F 1 "GND" H 2155 5127 50  0000 C CNN
F 2 "" H 2150 5300 50  0001 C CNN
F 3 "" H 2150 5300 50  0001 C CNN
	1    2150 5300
	1    0    0    -1  
$EndComp
$Comp
L Device:C C4
U 1 1 64320CAB
P 2150 5150
F 0 "C4" H 2265 5196 50  0000 L CNN
F 1 "C" H 2265 5105 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2188 5000 50  0001 C CNN
F 3 "~" H 2150 5150 50  0001 C CNN
	1    2150 5150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0118
U 1 1 6431B03D
P 2150 3800
F 0 "#PWR0118" H 2150 3550 50  0001 C CNN
F 1 "GND" H 2155 3627 50  0000 C CNN
F 2 "" H 2150 3800 50  0001 C CNN
F 3 "" H 2150 3800 50  0001 C CNN
	1    2150 3800
	1    0    0    -1  
$EndComp
$Comp
L Device:C C3
U 1 1 6431B037
P 2150 3650
F 0 "C3" H 2265 3696 50  0000 L CNN
F 1 "C" H 2265 3605 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2188 3500 50  0001 C CNN
F 3 "~" H 2150 3650 50  0001 C CNN
	1    2150 3650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0117
U 1 1 64315209
P 2100 2300
F 0 "#PWR0117" H 2100 2050 50  0001 C CNN
F 1 "GND" H 2105 2127 50  0000 C CNN
F 2 "" H 2100 2300 50  0001 C CNN
F 3 "" H 2100 2300 50  0001 C CNN
	1    2100 2300
	1    0    0    -1  
$EndComp
$Comp
L Device:C C1
U 1 1 64315203
P 2100 2150
F 0 "C1" H 2215 2196 50  0000 L CNN
F 1 "C" H 2215 2105 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2138 2000 50  0001 C CNN
F 3 "~" H 2100 2150 50  0001 C CNN
	1    2100 2150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0116
U 1 1 642FB155
P 2300 850
F 0 "#PWR0116" H 2300 600 50  0001 C CNN
F 1 "GND" H 2305 677 50  0000 C CNN
F 2 "" H 2300 850 50  0001 C CNN
F 3 "" H 2300 850 50  0001 C CNN
	1    2300 850 
	0    -1   -1   0   
$EndComp
Wire Wire Line
	2800 7450 2300 7450
Wire Wire Line
	2800 2200 2800 7450
Wire Wire Line
	2700 2100 3900 2100
Wire Wire Line
	2700 5950 2300 5950
Wire Wire Line
	2700 2100 2700 5950
Wire Wire Line
	2600 4450 2300 4450
Wire Wire Line
	2600 2000 2600 4450
Wire Wire Line
	3900 2000 2600 2000
Wire Wire Line
	2500 1900 3900 1900
Wire Wire Line
	2500 2950 2250 2950
Wire Wire Line
	2500 1900 2500 2950
Wire Wire Line
	3150 1450 2300 1450
$Comp
L power:GND #PWR0114
U 1 1 641D8FE0
P 1800 7550
F 0 "#PWR0114" H 1800 7300 50  0001 C CNN
F 1 "GND" H 1805 7377 50  0000 C CNN
F 2 "" H 1800 7550 50  0001 C CNN
F 3 "" H 1800 7550 50  0001 C CNN
	1    1800 7550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R5
U 1 1 6414C374
P 2150 7450
F 0 "R5" V 2357 7450 50  0000 C CNN
F 1 "470" V 2266 7450 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 2080 7450 50  0001 C CNN
F 3 "~" H 2150 7450 50  0001 C CNN
	1    2150 7450
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R1
U 1 1 6414BF0C
P 2150 5950
F 0 "R1" V 2357 5950 50  0000 C CNN
F 1 "470" V 2266 5950 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 2080 5950 50  0001 C CNN
F 3 "~" H 2150 5950 50  0001 C CNN
	1    2150 5950
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R4
U 1 1 6414BA38
P 2150 4450
F 0 "R4" V 2357 4450 50  0000 C CNN
F 1 "470" V 2266 4450 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 2080 4450 50  0001 C CNN
F 3 "~" H 2150 4450 50  0001 C CNN
	1    2150 4450
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R2
U 1 1 6414B585
P 2100 2950
F 0 "R2" V 2307 2950 50  0000 C CNN
F 1 "470" V 2216 2950 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 2030 2950 50  0001 C CNN
F 3 "~" H 2100 2950 50  0001 C CNN
	1    2100 2950
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R3
U 1 1 641411E0
P 2150 1450
F 0 "R3" V 2357 1450 50  0000 C CNN
F 1 "470" V 2266 1450 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 2080 1450 50  0001 C CNN
F 3 "~" H 2150 1450 50  0001 C CNN
	1    2150 1450
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1700 1950 1700 2350
Wire Wire Line
	1700 4900 1700 5350
Wire Wire Line
	1700 6450 1700 6850
Wire Wire Line
	1350 850  1700 850 
Connection ~ 1700 850 
Wire Wire Line
	1350 1050 1700 1050
Connection ~ 1700 1050
Wire Wire Line
	1700 1050 1700 1250
Wire Wire Line
	1350 1250 1700 1250
Connection ~ 1700 1250
Wire Wire Line
	1700 1250 1700 1950
Wire Wire Line
	1700 700  1700 850 
Wire Wire Line
	1800 750  1350 750 
Wire Wire Line
	1800 750  1800 950 
Wire Wire Line
	1700 850  2000 850 
Wire Wire Line
	1700 850  1700 1050
Wire Wire Line
	1350 950  1800 950 
Connection ~ 1800 950 
Wire Wire Line
	1800 950  1800 1150
Wire Wire Line
	1350 1150 1800 1150
Connection ~ 1800 1150
Wire Wire Line
	1800 1150 1800 1350
Wire Wire Line
	1350 1350 1800 1350
Connection ~ 1800 1350
Wire Wire Line
	1350 1450 2000 1450
Wire Wire Line
	1350 2350 1700 2350
Wire Wire Line
	1350 2550 1700 2550
Wire Wire Line
	1350 2750 1700 2750
Wire Wire Line
	1350 2450 1800 2450
Wire Wire Line
	1350 2650 1800 2650
Wire Wire Line
	1350 2850 1800 2850
Wire Wire Line
	1350 2950 1950 2950
Wire Wire Line
	1800 2250 1350 2250
Wire Wire Line
	1800 1350 1800 2250
Wire Wire Line
	1700 3450 1700 3850
Wire Wire Line
	1350 3850 1700 3850
Wire Wire Line
	1350 4050 1700 4050
Wire Wire Line
	1350 4250 1700 4250
Wire Wire Line
	1800 3750 1350 3750
Wire Wire Line
	1350 3950 1800 3950
Wire Wire Line
	1350 4150 1800 4150
Wire Wire Line
	1350 4350 1800 4350
Wire Wire Line
	1350 4450 2000 4450
Wire Wire Line
	1350 5350 1700 5350
Wire Wire Line
	1350 5550 1700 5550
Wire Wire Line
	1350 5750 1700 5750
Wire Wire Line
	1800 5250 1350 5250
Wire Wire Line
	1350 5450 1800 5450
Wire Wire Line
	1350 5650 1800 5650
Wire Wire Line
	1350 5850 1800 5850
Wire Wire Line
	1350 5950 2000 5950
Wire Wire Line
	1350 6850 1700 6850
Wire Wire Line
	1350 7050 1700 7050
Wire Wire Line
	1350 7250 1700 7250
Wire Wire Line
	1800 6750 1350 6750
Wire Wire Line
	1350 6950 1800 6950
Wire Wire Line
	1350 7350 1800 7350
Wire Wire Line
	1350 7450 2000 7450
Connection ~ 1700 3850
Wire Wire Line
	1700 3850 1700 4050
Connection ~ 1700 4050
Wire Wire Line
	1700 4050 1700 4250
Connection ~ 1700 4250
Wire Wire Line
	1700 4250 1700 4900
Connection ~ 1700 5350
Wire Wire Line
	1700 5350 1700 5550
Connection ~ 1700 5550
Wire Wire Line
	1700 5550 1700 5750
Connection ~ 1700 5750
Wire Wire Line
	1700 5750 1700 6450
Connection ~ 1700 6850
Wire Wire Line
	1700 6850 1700 7050
Connection ~ 1800 2250
Wire Wire Line
	1800 2250 1800 2450
Connection ~ 1800 2450
Wire Wire Line
	1800 2450 1800 2650
Connection ~ 1800 2650
Wire Wire Line
	1800 2650 1800 2850
Connection ~ 1800 2850
Wire Wire Line
	1800 2850 1800 3750
Connection ~ 1800 3750
Wire Wire Line
	1800 3750 1800 3950
Connection ~ 1800 3950
Wire Wire Line
	1800 3950 1800 4150
Connection ~ 1800 4150
Wire Wire Line
	1800 4150 1800 4350
Connection ~ 1800 4350
Wire Wire Line
	1800 4350 1800 5250
Connection ~ 1800 5250
Wire Wire Line
	1800 5250 1800 5450
Connection ~ 1800 5450
Wire Wire Line
	1800 5450 1800 5650
Connection ~ 1800 5650
Wire Wire Line
	1800 5650 1800 5850
Connection ~ 1800 5850
Wire Wire Line
	1800 5850 1800 6750
Connection ~ 1800 6750
Wire Wire Line
	1800 6750 1800 6950
Connection ~ 1800 6950
Connection ~ 1800 7150
Wire Wire Line
	1800 7150 1800 7350
Connection ~ 1800 7350
Wire Wire Line
	1800 7350 1800 7550
Connection ~ 1700 2350
Wire Wire Line
	1700 2350 1700 2550
Connection ~ 1700 2550
Wire Wire Line
	1700 2550 1700 2750
Connection ~ 1700 2750
Wire Wire Line
	1700 2750 1700 3450
Wire Wire Line
	1350 7150 1800 7150
Wire Wire Line
	1800 6950 1800 7150
Wire Wire Line
	1700 7050 1700 7250
Connection ~ 1700 7050
$Comp
L Device:C C2
U 1 1 642FB14F
P 2150 850
F 0 "C2" V 2402 850 50  0000 C CNN
F 1 "C" V 2311 850 50  0000 C CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2188 700 50  0001 C CNN
F 3 "~" H 2150 850 50  0001 C CNN
	1    2150 850 
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3900 2300 3150 2300
Wire Wire Line
	3150 1450 3150 2300
Wire Wire Line
	6100 2300 5500 2300
Wire Wire Line
	6100 1700 6100 2300
Wire Wire Line
	5500 2200 6550 2200
Wire Wire Line
	5500 2100 6400 2100
Wire Wire Line
	6400 2100 6400 2000
Wire Wire Line
	6400 2000 6750 2000
Wire Wire Line
	7450 1850 7450 2200
Wire Wire Line
	7450 2200 7050 2200
Wire Wire Line
	7050 2400 7550 2400
Wire Wire Line
	7550 2050 7550 2400
Wire Wire Line
	5450 2000 5500 2000
Wire Wire Line
	6250 2000 6250 2250
Wire Wire Line
	6250 2250 6650 2250
Wire Wire Line
	6650 2250 6650 2200
Wire Wire Line
	6650 2200 6750 2200
Connection ~ 5500 2000
Wire Wire Line
	5500 2000 6250 2000
Wire Wire Line
	5900 2400 5900 1900
Wire Wire Line
	5900 2400 6750 2400
Wire Wire Line
	5500 1800 5600 1800
Wire Wire Line
	5600 1800 5600 3800
Wire Wire Line
	5600 3800 5800 3800
Wire Wire Line
	3900 1800 3700 1800
Wire Wire Line
	3700 1800 3700 1750
Text Notes 6300 2800 0    50   ~ 0
DNP
$EndSCHEMATC
