EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
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
Text Label 6700 4950 0    50   ~ 0
JTAG_TDO
Text Label 5900 4500 0    50   ~ 0
JTAG_TMS
Text Label 5100 4500 0    50   ~ 0
JTAG_TCK
Text Label 6700 4500 0    50   ~ 0
JTAG_TDI
Text Label 5900 4950 0    50   ~ 0
VJTAG
$Comp
L power:+3V3 #PWR0120
U 1 1 5FD49C01
P 6150 4800
F 0 "#PWR0120" H 6150 4650 50  0001 C CNN
F 1 "+3V3" H 6165 4973 50  0000 C CNN
F 2 "" H 6150 4800 50  0001 C CNN
F 3 "" H 6150 4800 50  0001 C CNN
	1    6150 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 4950 6150 4950
Wire Wire Line
	6150 4950 6150 4800
Text Notes 4900 4200 0    50   ~ 0
JTAG Pogo Pin Part Number:\n0985-0-15-20-71-14-11-0\nUse 0.6 mm/1.1mm diameter hole/pad for mounting.\nExactly 1.5 mm between holes.
$Comp
L Connector:TestPoint VJTAG1
U 1 1 5FD7CF71
P 5900 4950
F 0 "VJTAG1" V 5900 5400 50  0000 R CNN
F 1 "TestPoint" H 5958 4977 50  0001 L CNN
F 2 "ttt_lib:TestPoint_THTPad_D1.1mm_Drill0.6mm" H 6100 4950 50  0001 C CNN
F 3 "~" H 6100 4950 50  0001 C CNN
F 4 "0985-0-15-20-71-14-11-0" H 5900 4950 50  0001 C CNN "MPN"
	1    5900 4950
	0    -1   1    0   
$EndComp
$Comp
L Connector:TestPoint TMS1
U 1 1 5FFEDA0F
P 5900 4500
F 0 "TMS1" V 5900 4900 50  0000 R CNN
F 1 "TestPoint" H 5958 4527 50  0001 L CNN
F 2 "ttt_lib:TestPoint_THTPad_D1.1mm_Drill0.6mm" H 6100 4500 50  0001 C CNN
F 3 "~" H 6100 4500 50  0001 C CNN
F 4 "0985-0-15-20-71-14-11-0" H 5900 4500 50  0001 C CNN "MPN"
	1    5900 4500
	0    -1   1    0   
$EndComp
$Comp
L Connector:TestPoint TCK1
U 1 1 6005CC1E
P 5100 4500
F 0 "TCK1" V 5100 4900 50  0000 R CNN
F 1 "TestPoint" H 5158 4527 50  0001 L CNN
F 2 "ttt_lib:TestPoint_THTPad_D1.1mm_Drill0.6mm" H 5300 4500 50  0001 C CNN
F 3 "~" H 5300 4500 50  0001 C CNN
F 4 "0985-0-15-20-71-14-11-0" H 5100 4500 50  0001 C CNN "MPN"
	1    5100 4500
	0    -1   1    0   
$EndComp
$Comp
L Connector:TestPoint TDO1
U 1 1 600CBE96
P 6700 4950
F 0 "TDO1" V 6650 5350 50  0000 R CNN
F 1 "TestPoint" H 6758 4977 50  0001 L CNN
F 2 "ttt_lib:TestPoint_THTPad_D1.1mm_Drill0.6mm" H 6900 4950 50  0001 C CNN
F 3 "~" H 6900 4950 50  0001 C CNN
F 4 "0985-0-15-20-71-14-11-0" H 6700 4950 50  0001 C CNN "MPN"
	1    6700 4950
	0    -1   1    0   
$EndComp
$Comp
L Connector:TestPoint TDI1
U 1 1 6013B16D
P 6700 4500
F 0 "TDI1" V 6700 4900 50  0000 R CNN
F 1 "TestPoint" H 6758 4527 50  0001 L CNN
F 2 "ttt_lib:TestPoint_THTPad_D1.1mm_Drill0.6mm" H 6900 4500 50  0001 C CNN
F 3 "~" H 6900 4500 50  0001 C CNN
F 4 "0985-0-15-20-71-14-11-0" H 6700 4500 50  0001 C CNN "MPN"
	1    6700 4500
	0    -1   1    0   
$EndComp
$Comp
L Connector:TestPoint GND1
U 1 1 601AA432
P 5100 4950
F 0 "GND1" V 5100 5350 50  0000 R CNN
F 1 "TestPoint" H 5158 4977 50  0001 L CNN
F 2 "ttt_lib:TestPoint_THTPad_D1.1mm_Drill0.6mm" H 5300 4950 50  0001 C CNN
F 3 "~" H 5300 4950 50  0001 C CNN
F 4 "0985-0-15-20-71-14-11-0" H 5100 4950 50  0001 C CNN "MPN"
	1    5100 4950
	0    -1   1    0   
$EndComp
$Comp
L power:GND #PWR0187
U 1 1 603128FD
P 5350 5050
F 0 "#PWR0187" H 5350 4800 50  0001 C CNN
F 1 "GND" H 5355 4877 50  0000 C CNN
F 2 "" H 5350 5050 50  0001 C CNN
F 3 "" H 5350 5050 50  0001 C CNN
	1    5350 5050
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5350 5050 5350 4950
Wire Wire Line
	5350 4950 5100 4950
$Comp
L dk_Rectangular-Connectors-Headers-Male-Pins:0878311420 J1
U 1 1 5FC59A40
P 7850 4700
F 0 "J1" H 7850 5225 50  0000 C CNN
F 1 "0878311420" H 7850 5134 50  0000 C CNN
F 2 "digikey-footprints:PinHeader_2x7_P2mm_Drill1mm" H 8050 4900 60  0001 L CNN
F 3 "https://www.molex.com/pdm_docs/sd/878311420_sd.pdf" H 8050 5000 60  0001 L CNN
F 4 "WM17469-ND" H 8050 5100 60  0001 L CNN "Digi-Key_PN"
F 5 "0878311420" H 8050 5200 60  0001 L CNN "MPN"
F 6 "Connectors, Interconnects" H 8050 5300 60  0001 L CNN "Category"
F 7 "Rectangular Connectors - Headers, Male Pins" H 8050 5400 60  0001 L CNN "Family"
F 8 "https://www.molex.com/pdm_docs/sd/878311420_sd.pdf" H 8050 5500 60  0001 L CNN "DK_Datasheet_Link"
F 9 "/product-detail/en/molex/0878311420/WM17469-ND/662449" H 8050 5600 60  0001 L CNN "DK_Detail_Page"
F 10 "CONN HEADER VERT 14POS 2MM" H 8050 5700 60  0001 L CNN "Description"
F 11 "Molex" H 8050 5800 60  0001 L CNN "Manufacturer"
F 12 "Active" H 8050 5900 60  0001 L CNN "Status"
	1    7850 4700
	1    0    0    -1  
$EndComp
Text Label 8050 4700 0    50   ~ 0
JTAG_TDO
Text Label 8050 4500 0    50   ~ 0
JTAG_TMS
Text Label 8050 4600 0    50   ~ 0
JTAG_TCK
Text Label 8050 4800 0    50   ~ 0
JTAG_TDI
Text Label 8050 4400 0    50   ~ 0
VJTAG
Wire Wire Line
	8050 4400 8300 4400
$Comp
L power:GND #PWR0101
U 1 1 5FC5E1A2
P 7550 5100
F 0 "#PWR0101" H 7550 4850 50  0001 C CNN
F 1 "GND" H 7555 4927 50  0000 C CNN
F 2 "" H 7550 5100 50  0001 C CNN
F 3 "" H 7550 5100 50  0001 C CNN
	1    7550 5100
	-1   0    0    -1  
$EndComp
Wire Wire Line
	7650 4400 7550 4400
Wire Wire Line
	7550 4400 7550 4500
Wire Wire Line
	7650 5000 7550 5000
Connection ~ 7550 5000
Wire Wire Line
	7550 5000 7550 5100
Wire Wire Line
	7650 4900 7550 4900
Connection ~ 7550 4900
Wire Wire Line
	7550 4900 7550 5000
Wire Wire Line
	7650 4800 7550 4800
Connection ~ 7550 4800
Wire Wire Line
	7550 4800 7550 4900
Wire Wire Line
	7650 4700 7550 4700
Connection ~ 7550 4700
Wire Wire Line
	7550 4700 7550 4800
Wire Wire Line
	7650 4600 7550 4600
Connection ~ 7550 4600
Wire Wire Line
	7550 4600 7550 4700
Wire Wire Line
	7650 4500 7550 4500
Connection ~ 7550 4500
Wire Wire Line
	7550 4500 7550 4600
$Comp
L power:+3V3 #PWR0102
U 1 1 5FC6438E
P 8300 4200
F 0 "#PWR0102" H 8300 4050 50  0001 C CNN
F 1 "+3V3" H 8315 4373 50  0000 C CNN
F 2 "" H 8300 4200 50  0001 C CNN
F 3 "" H 8300 4200 50  0001 C CNN
	1    8300 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	8300 4200 8300 4400
Text Notes 4900 4300 0    50   ~ 0
Looking down through PCB from behind pogo pins:
$EndSCHEMATC
