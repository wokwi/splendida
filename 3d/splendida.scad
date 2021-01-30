/**
 * Splendida r1 simplified 3D model
 *
 * This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
 *
 * Copyright (C) 2021, Uri Shaked
 */

include <MCAD/units.scad>;

$fn = 60;

module Splendida() {
  color("black") {
    linear_extrude(1.6)
    difference() {
      circle(r=86);
      
      for (angle = [27, 164, 269]) {
        rotate([0, 0, -angle])
        translate([0, 81.5])
        circle(r=1.5);
      }
    }
  }
  
  // aligator clips [GND, VDD]
  color("silver")
  translate([0, 0, -0.05])
  linear_extrude(0.1)
  intersection() {
    circle(r=86);
    for (angle = [100.481, 88.833]) {
      rotate([0, 0, -angle])
      translate([0, 85.36])
      scale([1, 2])
      circle(r=1.6);
    }
  }
  
  // pins [DIN, DOUT]
  color("gold") 
  for (angle = [-178.268, -1.7319874897703897]) {
    rotate([0, 0, -angle])
    translate([0, 84.1, -epsilon]) {
      translate([-2.54, 0, 0])
      cylinder(r=0.5, h=3);

      cylinder(r=0.5, h=3);

      translate([2.54, 0, 0])
      cylinder(r=0.5, h=3);
    }
  }
  
  color("white")
  for (n = [2 : 257]) {
    rotate([0, 0, -n * 137.508])
    translate([0, 5 * sqrt(n), 1.6])
    rotate([0, 0, -40])
    translate([-2.5, -2.5, 0])
    cube([5, 5, 1.6]);
  }
  
  color("white")
  mirror([1, 0, 0])
  text("Splendida r1", halign="center", valign="center", size=5);
}

Splendida();