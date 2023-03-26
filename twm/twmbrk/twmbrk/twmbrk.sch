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
L Connector:RJ45 J1
U 1 1 64B2F19E
P 3750 3050
F 0 "J1" H 3807 3717 50  0000 C CNN
F 1 "RJ45" H 3807 3626 50  0000 C CNN
F 2 "ttt_lib:MJ3225-88-0" V 3750 3075 50  0001 C CNN
F 3 "~" V 3750 3075 50  0001 C CNN
	1    3750 3050
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H3
U 1 1 64B2FBF8
P 4800 2700
F 0 "H3" V 4754 2850 50  0000 L CNN
F 1 "MountingHole_Pad" V 4845 2850 50  0000 L CNN
F 2 "Connector_Pin:Pin_D1.4mm_L8.5mm_W2.8mm_FlatFork" H 4800 2700 50  0001 C CNN
F 3 "~" H 4800 2700 50  0001 C CNN
	1    4800 2700
	0    1    1    0   
$EndComp
$Comp
L Mechanical:MountingHole H1
U 1 1 64B30B25
P 4500 1450
F 0 "H1" H 4600 1496 50  0000 L CNN
F 1 "MountingHole" H 4600 1405 50  0000 L CNN
F 2 "MountingHole:MountingHole_4.3mm_M4_Pad" H 4500 1450 50  0001 C CNN
F 3 "~" H 4500 1450 50  0001 C CNN
	1    4500 1450
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 64B318AB
P 5400 1400
F 0 "H2" H 5500 1446 50  0000 L CNN
F 1 "MountingHole" H 5500 1355 50  0000 L CNN
F 2 "MountingHole:MountingHole_4.3mm_M4_Pad" H 5400 1400 50  0001 C CNN
F 3 "~" H 5400 1400 50  0001 C CNN
	1    5400 1400
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H4
U 1 1 64B32038
P 4800 2900
F 0 "H4" V 4754 3050 50  0000 L CNN
F 1 "MountingHole_Pad" V 4845 3050 50  0000 L CNN
F 2 "Connector_Pin:Pin_D1.4mm_L8.5mm_W2.8mm_FlatFork" H 4800 2900 50  0001 C CNN
F 3 "~" H 4800 2900 50  0001 C CNN
	1    4800 2900
	0    1    1    0   
$EndComp
$Comp
L Mechanical:MountingHole_Pad H5
U 1 1 64B32137
P 4800 3100
F 0 "H5" V 4754 3250 50  0000 L CNN
F 1 "MountingHole_Pad" V 4845 3250 50  0000 L CNN
F 2 "Connector_Pin:Pin_D1.4mm_L8.5mm_W2.8mm_FlatFork" H 4800 3100 50  0001 C CNN
F 3 "~" H 4800 3100 50  0001 C CNN
	1    4800 3100
	0    1    1    0   
$EndComp
$Comp
L Mechanical:MountingHole_Pad H6
U 1 1 64B322CF
P 4800 3350
F 0 "H6" V 4754 3500 50  0000 L CNN
F 1 "MountingHole_Pad" V 4845 3500 50  0000 L CNN
F 2 "Connector_Pin:Pin_D1.4mm_L8.5mm_W2.8mm_FlatFork" H 4800 3350 50  0001 C CNN
F 3 "~" H 4800 3350 50  0001 C CNN
	1    4800 3350
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 64B41DB2
P 4250 3600
F 0 "#PWR0101" H 4250 3350 50  0001 C CNN
F 1 "GND" H 4255 3427 50  0000 C CNN
F 2 "" H 4250 3600 50  0001 C CNN
F 3 "" H 4250 3600 50  0001 C CNN
	1    4250 3600
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0102
U 1 1 64B4210A
P 4350 2350
F 0 "#PWR0102" H 4350 2200 50  0001 C CNN
F 1 "+5V" H 4365 2523 50  0000 C CNN
F 2 "" H 4350 2350 50  0001 C CNN
F 3 "" H 4350 2350 50  0001 C CNN
	1    4350 2350
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 2650 4250 2650
Wire Wire Line
	4250 2650 4250 2850
Wire Wire Line
	4150 2850 4250 2850
Connection ~ 4250 2850
Wire Wire Line
	4250 2850 4250 3050
Wire Wire Line
	4150 3050 4250 3050
Connection ~ 4250 3050
Wire Wire Line
	4250 3050 4250 3100
Wire Wire Line
	4150 3250 4250 3250
Connection ~ 4250 3250
Wire Wire Line
	4250 3250 4250 3600
Wire Wire Line
	4150 3150 4350 3150
Wire Wire Line
	4350 2950 4150 2950
Wire Wire Line
	4350 2350 4350 2700
Connection ~ 4350 2950
Wire Wire Line
	4350 2950 4350 3150
Wire Wire Line
	4150 2750 4350 2750
Connection ~ 4350 2750
Wire Wire Line
	4350 2750 4350 2950
Wire Wire Line
	4150 3350 4700 3350
Wire Wire Line
	4700 3100 4600 3100
Connection ~ 4250 3100
Wire Wire Line
	4250 3100 4250 3250
Wire Wire Line
	4700 2900 4600 2900
Wire Wire Line
	4600 2900 4600 3100
Connection ~ 4600 3100
Wire Wire Line
	4600 3100 4250 3100
Wire Wire Line
	4700 2700 4350 2700
Connection ~ 4350 2700
Wire Wire Line
	4350 2700 4350 2750
$EndSCHEMATC
