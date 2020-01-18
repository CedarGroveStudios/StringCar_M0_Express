# StringCar_M0_Express

A Circuit-Python compatible string car racer controller board.

![Glamour Shot](https://github.com/CedarGroveStudios/StringCar_M0_Express/blob/master/photos_graphics/nuevo_StringCar_M0_Express_glamour_v01_wide.jpg)

The Cedar Grove StringCar M0 Express is an ATSAMD21-based CircuitPython compatible board used to control a simple string car racer robot. The board is architecturally similar to the Adafruit Trinket M0 and ItsyBitsy M0 Express microcontroller boards with the addition of battery management and a DC motor controller. This board features JST connectors for the racer's battery, motor output, and sensor input. LiPo battery management charge rate is 500mA. For sensor experimentation, a 3.3-volt Stemma-QT connection is available on-board. The micro-USB connector is used for REPL operation, operational status data output, and battery charging. On-board flash memory size is 2MB.

The StringCar M0 Express board will not be sold. The GitHub repository will contain design files and links for the BOM and to the shared OSH Park project.

The string car racer is a simple one-motor robot that is suspended from a string using a pulley attached to the motor shaft. Its challenge is to race back and forth from one end of a taut string to the other. The fastest car wins. The controller board uses sensor switches to detect the ends of the string, calculate the string length, then control motor speed and braking to avoid string-end collisions.

The objective is to create a string car racer that can autonomously learn about its environment and adjust tradeoffs for speed and battery longevity. CircuitPython is used to easily add and interactively adjust performance features such as motor and battery efficiency, end-of-string collision avoidance, string length calculation, and predictive braking. Also, being able to watch its own battery status means that it'll always return to the home end of the string when battery capacity begins to wane. Circuit Python also supports libraries that abstract string car functions, simplifying the primary code module to make it easier for novice programmers to get involved in customizing  string car racer operation.
