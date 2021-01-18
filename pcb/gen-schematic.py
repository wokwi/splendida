# Generate Splendida LED Spiral
#
# Copyright (C) 2021, Uri Shaked
#
# Released under the terms of the GNU General Public License(GPL) version 3 or greater.

import math

LEDS = 256
COLUMN_SIZE = 15

HEADER = """
EESchema Schematic File Version 4
LIBS:splendida-leds-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
""".strip()

def create_noconnect(x, y):
  return "NoConn ~ {x} {y}\n".format(x=x, y=y)

def create_junction(x, y):
  return "Connection ~ {x} {y}\n".format(x=x, y=y)

def create_wire(x1, y1, x2, y2):
  return "Wire Wire Line\n  {: <4} {: <4} {: <4} {: <4}\n".format(x1, y1, x2, y2)

def create_label(x, y, id, orient=0):
  return "Text Label {x} {y: <4} {orient}    50   ~ 0\n{id}\n".format(x=x, y=y, id=id, orient=orient)

def create_hlabel(x, y, id, orient=0):
  return "Text HLabel {x} {y: <4} {orient}    50   Input ~ 0\n{id}\n".format(x=x, y=y, id=id, orient=orient)

def create_vdd(x, y):
  return """$Comp
L power:VDD #PWR?
U 1 1 5FFB54F1
P {left} {top}
F 0 "#PWR?" H {left} {top_symbol} 50  0001 C CNN
F 1 "VDD" V {left_label} {top_label} 50  0000 L CNN
F 2 "" H {left} {top} 50  0001 C CNN
F 3 "" H {left} {top} 50  0001 C CNN
	1    {left} {top} 
	0    -1   -1   0   
$EndComp
""" .format(left=x, top=y, left_label=x+15, top_label=y+127, top_symbol=y-150)

def create_gnd(x, y):
  return """$Comp
L power:GND #PWR?
U 1 1 5FFB5607
P {left} {top}
F 0 "#PWR?" H {left} {top_symbol} 50  0001 C CNN
F 1 "GND" H {left_label} {top_label} 50  0000 C CNN
F 2 "" H {left} {top} 50  0001 C CNN
F 3 "" H {left} {top} 50  0001 C CNN
	1    {left} {top}
	1    0    0    -1  
$EndComp
""".format(left=x, top=y, left_label=x-150, top_label=y-50, top_symbol=y-250)

def create_led(x, y, id):
  return """$Comp
L LED:WS2812B D{id}
U 1 1 5FFD4{id:03X}
P {left} {top}
F 0 "D{id}" H {left_designator} {top_designator} 50  0000 L CNN
F 1 "WS2812B" H {left_label} {top_label} 50  0001 L CNN
F 2 "LED_SMD:LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm" H {left} {top} 50  0001 L TNN
F 3 "https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf" H 4250 1675 50  0001 L TNN
F 4 "C114586" V {left} {top} 50  0001 C CNN "LCSC Part"
	1    {left} {top}
	1    0    0    -1  
$EndComp
""".format(id=id, left=x, top=y, top_label=y+250, top_designator=y-250, left_designator=x+75, left_label=x+75)

def create_capacitor(x, y, id):
  return """$Comp
L Device:C C{id}
U 1 1 5FFB9{id:03X}
P {left} {top}
F 0 "C{id}" V {left_designator} {top_designator} 50  0000 L CNN
F 1 "100nF" H {left} {top} 50  0001 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H {left} {top} 50  0001 C CNN
F 3 "~" H {left} {top} 50  0001 C CNN
F 4 "C14663" V {left} {top} 50  0001 C CNN "LCSC Part"
	1    {left} {top}
	0    1    1    0   
$EndComp
""".format(id=id, left=x, top=y, left_designator=x - 130, top_designator=y - 90)

def create_led_unit(id, x, y):
  origin = [1000, 800]
  left = origin[0] + x * 700
  top = origin[1] + y * 800
  
  second_pin = row + 2 if row >= col else row + 1
  parts = [
    create_vdd(left, top - 50),
    create_gnd(left, top + 550),
    create_led(left, top + 250, id),
    create_wire(left + 300, top + 250, left + 400, top + 250),
    create_capacitor(left + 150, top - 50, id),
    create_junction(left, top - 50),
  ]
  if x == 0:
    if y == 0:
      parts.append(create_hlabel(left - 300, top + 250, "DIN"))
    else:
      parts.append(create_wire(left - 300, top + 250, left - 400, top + 250))
      parts.append(create_label(left - 400, top + 250, "L{}".format(id)))
  # capacitor to GND
  parts.append(create_wire(left + 300, top - 50, left + 300, top - 250))
  if y == 0:
    if x == 0:
      parts.append(create_gnd(left, top - 250))
    if x == COLUMN_SIZE - 1 or id == LEDS and id < COLUMN_SIZE - x:
      parts.append(create_wire(origin[0], top - 250, left + 300, top - 250))
    else:
      parts.append(create_junction(left + 300, top - 250))
  else:
    parts.append(create_wire(left, top - 250, left + 300, top - 250))
    parts.append(create_junction(left, top - 250))
  if id == LEDS:
    parts.append(create_hlabel(left + 400, top + 250, "DOUT", 2))
  elif x == COLUMN_SIZE - 1:
    parts.append(create_label(left + 400, top + 250, "L{}".format(id+1), 2))
  return "".join(parts)

with open('splendida-leds.sch', 'w') as schematic:
  schematic.write(HEADER + "\n")
  for led_idx in range(LEDS):
    col = led_idx % COLUMN_SIZE
    row = led_idx // COLUMN_SIZE
    schematic.write(create_led_unit(led_idx + 1, col, row))
  schematic.write("$EndSCHEMATC\n")
