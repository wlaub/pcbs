EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 8 14
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text HLabel 4500 3500 0    50   Input ~ 0
5V
Text HLabel 4500 3600 0    50   Input ~ 0
12V
Text HLabel 4500 4000 0    50   Input ~ 0
-12V
Text HLabel 7000 4400 2    50   Output ~ 0
5V_V
Text HLabel 7000 4500 2    50   Output ~ 0
12V_V
Text HLabel 7000 4600 2    50   Output ~ 0
-12V_V
$Comp
L Connector_Generic:Conn_02x08_Odd_Even J?
U 1 1 6072B9BF
P 5300 3700
AR Path="/60693B3F/6072B9BF" Ref="J?"  Part="1" 
AR Path="/60693C9A/6072B9BF" Ref="J?"  Part="1" 
F 0 "J?" H 5350 3075 50  0000 C CNN
F 1 "Conn_02x08_Odd_Even" H 5350 3166 50  0000 C CNN
F 2 "" H 5300 3700 50  0001 C CNN
F 3 "~" H 5300 3700 50  0001 C CNN
	1    5300 3700
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_02x05_Odd_Even J?
U 1 1 6072B9C5
P 6300 3800
AR Path="/60693B3F/6072B9C5" Ref="J?"  Part="1" 
AR Path="/60693C9A/6072B9C5" Ref="J?"  Part="1" 
F 0 "J?" H 6350 3050 50  0000 C CNN
F 1 "Conn_02x05_Odd_Even" H 6350 3150 50  0000 C CNN
F 2 "" H 6300 3800 50  0001 C CNN
F 3 "~" H 6300 3800 50  0001 C CNN
	1    6300 3800
	-1   0    0    1   
$EndComp
Wire Wire Line
	5000 4000 5500 4000
Connection ~ 5500 4000
Wire Wire Line
	5500 4000 6000 4000
Connection ~ 6000 4000
Wire Wire Line
	6000 4000 6500 4000
Connection ~ 5500 3900
Wire Wire Line
	5500 3900 6000 3900
Connection ~ 6000 3900
Wire Wire Line
	6000 3900 6500 3900
Wire Wire Line
	5000 3800 5500 3800
Connection ~ 5500 3800
Connection ~ 6000 3800
Wire Wire Line
	6000 3800 6500 3800
Wire Wire Line
	5000 3900 5500 3900
Wire Wire Line
	5000 3700 5500 3700
Connection ~ 5500 3700
Wire Wire Line
	5500 3700 6000 3700
Connection ~ 6000 3700
Wire Wire Line
	6000 3700 6500 3700
Wire Wire Line
	5000 3600 5500 3600
Connection ~ 5500 3600
Wire Wire Line
	5500 3600 6000 3600
Connection ~ 6000 3600
Wire Wire Line
	6000 3600 6500 3600
NoConn ~ 5500 3300
NoConn ~ 5500 3400
NoConn ~ 5000 3400
NoConn ~ 5000 3300
Wire Wire Line
	5000 3700 5000 3800
Connection ~ 5000 3700
Connection ~ 5000 3900
Connection ~ 5000 3800
Wire Wire Line
	5000 3800 5000 3900
Wire Wire Line
	5500 3700 5500 3800
Wire Wire Line
	5500 3800 5500 3900
Wire Wire Line
	6000 3700 6000 3800
Wire Wire Line
	6000 3800 6000 3900
Wire Wire Line
	6500 3700 6500 3800
Connection ~ 6500 3700
Connection ~ 6500 3900
Connection ~ 6500 3800
Wire Wire Line
	6500 3800 6500 3900
Wire Wire Line
	5000 3500 5500 3500
$Comp
L power:GND #PWR?
U 1 1 6072B9F7
P 4900 4100
AR Path="/60693B3F/6072B9F7" Ref="#PWR?"  Part="1" 
AR Path="/60693C9A/6072B9F7" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4900 3850 50  0001 C CNN
F 1 "GND" H 4905 3927 50  0000 C CNN
F 2 "" H 4900 4100 50  0001 C CNN
F 3 "" H 4900 4100 50  0001 C CNN
	1    4900 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 4100 4900 3800
Wire Wire Line
	4900 3800 5000 3800
Wire Wire Line
	4500 4000 5000 4000
Connection ~ 5000 4000
Wire Wire Line
	4500 3600 5000 3600
Connection ~ 5000 3600
Wire Wire Line
	4500 3500 5000 3500
Connection ~ 5000 3500
Wire Wire Line
	5500 3800 6000 3800
Wire Wire Line
	5500 3600 5650 3750
Wire Wire Line
	5500 3500 5750 3750
Wire Wire Line
	5500 4000 5550 4050
Wire Wire Line
	5550 4600 6150 4600
Wire Wire Line
	5550 4050 5550 4600
Wire Wire Line
	5650 4500 6150 4500
Wire Wire Line
	5750 4400 6150 4400
Connection ~ 5500 3500
Wire Wire Line
	5750 3750 5750 4400
Wire Wire Line
	5650 3750 5650 4500
Text Notes 5650 3400 0    50   ~ 0
Note: Kelvin connection not strictly necessary here.\nRoute from the "end" connector pad that won't have any current through it.
$Comp
L Device:Net-Tie_2 NT?
U 1 1 607C420E
P 6250 4400
F 0 "NT?" H 6250 4450 50  0000 C CNN
F 1 "Net-Tie_2" H 6700 4050 50  0001 C CNN
F 2 "" H 6250 4400 50  0001 C CNN
F 3 "~" H 6250 4400 50  0001 C CNN
	1    6250 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 4400 7000 4400
$Comp
L Device:Net-Tie_2 NT?
U 1 1 607CA138
P 6250 4500
F 0 "NT?" H 6250 4550 50  0000 C CNN
F 1 "Net-Tie_2" H 6700 4050 50  0001 C CNN
F 2 "" H 6250 4500 50  0001 C CNN
F 3 "~" H 6250 4500 50  0001 C CNN
	1    6250 4500
	1    0    0    -1  
$EndComp
$Comp
L Device:Net-Tie_2 NT?
U 1 1 607CA87D
P 6250 4600
F 0 "NT?" H 6250 4650 50  0000 C CNN
F 1 "Net-Tie_2" H 6250 4690 50  0001 C CNN
F 2 "" H 6250 4600 50  0001 C CNN
F 3 "~" H 6250 4600 50  0001 C CNN
	1    6250 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 4500 7000 4500
Wire Wire Line
	6350 4600 7000 4600
$EndSCHEMATC
