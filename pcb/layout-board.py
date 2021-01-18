# Automatic PCB Layout for Fermat's Spiral LED arragnement
#
# Copyright (C) 2021, Uri Shaked
#
# Released under the terms of the GNU General Public License(GPL) version 3 or greater.

import pcbnew
import math

LEDS = 256
CENTER_POS = [130, 90]
LED_SPACING = 5
VIA_OFFSET_UP = 0.9
VIA_OFFSET_DOWN = 1.5

LED_MAP = []
LED_ROTATE = []

for stripidx, j in enumerate([1, 9, 17, 4, 12, 20, 7, 15, 2, 10, 18, 5, 13, 21, 8, 16, 3, 11, 19, 6, 14]):
  strip = []
  for i in range(j, LEDS + 1, 21):
    strip.append(i)
    LED_ROTATE.append(180 if stripidx % 2 == 0 else 0)
  if stripidx % 2 == 1:
    strip.reverse()
  LED_MAP += strip

print(LED_MAP)

SCALE = 1e6

def draw_track(start, end, layer, net, width = None):
  track = pcbnew.TRACK(board)
  track.SetStart(start)
  track.SetEnd(end)
  track.SetLayer(layer)
  board.Add(track)
  track.SetNet(net)
  if width:
    track.SetWidth(int(width))
  return track

def draw_via(pos, layer, net, diameter = 0.8 * SCALE, drill = 0.4 * SCALE):
  via = pcbnew.VIA(board)
  via.SetPosition(pos)
  via.SetLayer(layer)
  via.SetWidth(int(diameter))
  via.SetDrill(int(drill))
  board.Add(via)
  via.SetNet(net)
  return via

def vector(length, angle, scale = SCALE):
  return pcbnew.wxPoint(length * math.sin(angle) * scale, length * math.cos(angle) * scale)

board = pcbnew.GetBoard()

matrix_origin = pcbnew.wxPoint(CENTER_POS[0] * SCALE, CENTER_POS[1] * SCALE)
prev_dout = None
for led_idx in range(1, LEDS + 1):
  n = LED_MAP[led_idx - 1] + 1
  r = LED_SPACING * math.sqrt(n)
  theta_deg = n * 137.508
  theta = (theta_deg / 180) * math.pi
  pos = matrix_origin + pcbnew.wxPoint(r * math.cos(theta) * SCALE, r * math.sin(theta) * SCALE)
  mod = board.FindModule("D{}".format(led_idx))
  mod.SetPosition(pos)
  rotate = LED_ROTATE[led_idx - 1] - theta_deg - 40
  rotate_rad = (rotate / 180.) * math.pi
  mod.SetOrientationDegrees(rotate)
  mod.Reference().SetVisible(False)
  vdd_pad, dout_pad, din_pad, gnd_pad = list(mod.Pads())
  if prev_dout:
    draw_track(prev_dout.GetCenter(), din_pad.GetCenter(), pcbnew.F_Cu, din_pad.GetNet(), 0.25 * SCALE)
  prev_dout = dout_pad

  cap = board.FindModule("C{}".format(led_idx))
  cap_distance = 3.75
  cap_rotate = rotate + 180
  cap_rotate_rad = ((cap_rotate - LED_ROTATE[led_idx - 1]) / 180.) * math.pi
  cap.SetPosition(pos + vector(cap_distance, cap_rotate_rad))
  cap.SetOrientationDegrees(cap_rotate)
  cap.Reference().SetVisible(False)
  cap_vdd, cap_gnd = list(cap.Pads())
  via = draw_via(gnd_pad.GetCenter() + vector(1.5, rotate_rad - math.pi / 2), pcbnew.F_Cu, gnd_pad.GetNet())
  draw_track(gnd_pad.GetCenter(), via.GetCenter(), pcbnew.F_Cu, gnd_pad.GetNet(), 0.8 * SCALE)
  draw_track(via.GetCenter(), cap_gnd.GetCenter(), pcbnew.F_Cu, via.GetNet(), 0.4 * SCALE)
