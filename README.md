# home-asssitant-lennox-https
A homeassistant custom component to interface with Lennox S30s over local HTTPS interface


Based upon the work here:
https://github.com/hufman/lennox_lcc

Read only (At this time, in theory might be able to replace Cloud and HomeKit connections for control)

Logs the following.
s status outdoorTemperatureStatus good
s status outdoorTemperature 71
s status outdoorTemperatureC 21.5
e 0 0  ...
e 1 0 Comp. Short Cycle Delay Active ... No
e 1 1 Cooling Rate %... 0.0
e 1 2 High Pressure Switch ... Closed
e 1 3 Low Pressure Switch ... Closed
e 1 4 Top Cap Switch Status ... Closed
e 1 5 Liquid Line Temp F... 69.7
e 1 6 Ambient Temp F... 70.6
e 1 7 Compressor Active Alarm ... None
e 1 8 Compressor Hz ... 0.0
e 1 9 Compressor Speed Reduction ... Off
e 1 10 Heat Sink Temperature F... 69.8
e 1 11 Inverter Input Voltage V... 241.0
e 1 12 Inverter Input Current A... 0.301
e 1 13 DC Link Voltage V... 11.0
e 1 14 Compressor Current A... 0.000
e 2 0 Heating Rate %... 0.0
e 2 1 Blower CFM Demand CFM... 0
e 2 2 Blower Off Delay ... Off
e 2 3 Blower On Delay ... Off
e 2 4 Indoor Blower RPM ... 0
e 2 5 Indoor Blower Power %... 0.0
e 2 6 Inducer Blower RPM ... 0
e 2 7 Flame Current uA... 0.0
e 2 8 Flame Sense ... No Flame
e 2 9 Outdoor Temperature ... open
e 2 10 Discharge Air Temperature ... open
e 2 11 Line Voltage V... 121.6
e 2 12 24VAC Voltage V... 25.2
e 2 13 Igniter Voltage V... 0.0
e 2 14 High Pressure Switch ... Open
e 2 15 Low Pressure Switch ... Open
e 2 16 Primary Limit Switch ... Closed
e 2 17 Rollout Switch ... Closed
e 2 18 Gas Valve ... Off
e 2 19 G - Input ... Off
e 2 20 Trial for Ignition ... Off
e 2 21 Ignition Stabilization ... Off
e 2 22 HSI Warm-up ... Off
e 2 23 Interpurge ... Off
e 2 24 Postpurge ... No
e 2 25 Prepurge ... No
e 2 26 Auto-start Delay ... Off
e 2 27 Time Left - Auto Restart min... 0
e 2 28 Recycle Counter ... 0
e 2 29 Retry Counter ... 0
e 2 30 Link Relay Status ... Closed
e 2 31 Dehumidification Relay Status ... Open
e 2 32 Humidification Relay Status ... Open
e 2 33 Y2 Relay Status ... Open
e 2 34 Y1 Relay Status ... Open
e 2 35 Ignition Status ... Off
e 2 36 Calibration Status ... Off
e 2 37 Calibration Invalid ... Off
z 0 temperatureStatus good
z 0 humidityStatus good
z 0 doNotPersist True
z 0 fan False
z 0 allergenDefender False
z 0 humidity 57
z 0 temperature 73
z 0 damper 0
z 0 heatCoast False
z 0 defrost False
z 0 period {'systemMode': 'off', 'fanMode': 'auto', 'husp': 35, 'sp': 73, 'desp': 44, 'csp': 74, 'hsp': 67, 'hspC': 19.5, 'startTime': 0, 'humidityMode': 'off', 'spC': 23, 'cspC': 23.5}
z 0 humOperation off
z 0 scheduleExceptionIds []
z 0 balancePoint none
z 0 tempOperation off
z 0 ventilation False
z 0 demand 0
z 0 aux False
z 0 coolCoast False
z 0 ssr False
z 0 temperatureC 23
z 1 temperatureStatus not_available
z 1 humidityStatus not_available
z 1 doNotPersist True
z 2 temperatureStatus not_available
z 2 humidityStatus not_available
z 2 doNotPersist True
z 3 temperatureStatus not_available
z 3 humidityStatus not_available
z 3 doNotPersist True
