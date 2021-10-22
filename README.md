# home-asssitant-lennox-https
A homeassistant custom component to interface with Lennox S30s over local HTTPS interface


Based upon the work here:
https://github.com/hufman/lennox_lcc

Read only (At this time, in theory might be able to replace Cloud and HomeKit connections for control)

Currently records the following sensors, with additional to come

```
SensorEntityDescription(
        key="LennoxHTTPS_System_status_outdoorTemperatureStatus",
        name="outdoorTemperatureStatus",
        native_unit_of_measurement=TEMP_FAHRENHEIT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_System_status_outdoorTemperature",
        name="outdoorTemperature",
        native_unit_of_measurement=TEMP_FAHRENHEIT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_System_status_outdoorTemperatureC",
        name="outdoorTemperatureC",
        native_unit_of_measurement=TEMP_CELSIUS,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_0_Comp. Short Cycle Delay Active",
        name="Comp. Short Cycle Delay Active",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_1_Cooling Rate",
        name="Cooling Rate",
        native_unit_of_measurement="%",
        state_class=STATE_CLASS_MEASUREMENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_2_High Pressure Switch",
        name="High Pressure Switch",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_3_Low Pressure Switch",
        name="Low Pressure Switch",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_4_Top Cap Switch Status",
        name="Top Cap Switch Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_5_Liquid Line Temp",
        name="Liquid Line Temp",
        native_unit_of_measurement=TEMP_FAHRENHEIT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_6_Ambient Temp",
        name="Ambient Temp",
        native_unit_of_measurement=TEMP_FAHRENHEIT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_7_Compressor Active Alarm",
        name="Compressor Active Alarm",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_8_Compressor Hz",
        name="Compressor Hz",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_9_Compressor Speed Reduction",
        name="Compressor Speed Reduction",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_10_Heat Sink Temperature",
        name="Heat Sink Temperature",
        native_unit_of_measurement=TEMP_FAHRENHEIT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_11_Inverter Input Voltage",
        name="Inverter Input Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_VOLTAGE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_12_Inverter Input Current",
        name="Inverter Input Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_CURRENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_13_DC Link Voltage",
        name="DC Link Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_VOLTAGE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_1_14_Compressor Current",
        name="Compressor Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_CURRENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_0_Heating Rate",
        name="Heating Rate",
        native_unit_of_measurement="%",
        state_class=STATE_CLASS_MEASUREMENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_1_Blower CFM Demand",
        name="Blower CFM Demand",
        native_unit_of_measurement=VOLUME_FLOW_RATE_CUBIC_FEET_PER_MINUTE,
        state_class=STATE_CLASS_MEASUREMENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_2_Blower Off Delay",
        name="Blower Off Delay",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_3_Blower On Delay",
        name="Blower On Delay",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_4_Indoor Blower RPM",
        name="Indoor Blower RPM",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_5_Indoor Blower Power",
        name="Indoor Blower Power",
        native_unit_of_measurement="%",
        state_class=STATE_CLASS_MEASUREMENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_6_Inducer Blower RPM",
        name="Inducer Blower RPM",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_7_Flame Current",
        name="Flame Current",
        native_unit_of_measurement="uA",
        state_class=STATE_CLASS_MEASUREMENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_8_Flame Sense",
        name="Flame Sense",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_9_Outdoor Temperature",
        name="Outdoor Temperature",
        native_unit_of_measurement=TEMP_FAHRENHEIT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_10_Discharge Air Temperature",
        name="Discharge Air Temperature",
        native_unit_of_measurement=TEMP_FAHRENHEIT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_TEMPERATURE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_11_Line Voltage",
        name="Line Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_VOLTAGE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_12_24VAC Voltage",
        name="24VAC Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_VOLTAGE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_13_Igniter Voltage",
        name="Igniter Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_VOLTAGE,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_14_High Pressure Switch",
        name="High Pressure Switch",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_15_Low Pressure Switch",
        name="Low Pressure Switch",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_16_Primary Limit Switch",
        name="Primary Limit Switch",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_17_Rollout Switch",
        name="Rollout Switch",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_18_Gas Valve",
        name="Gas Valve",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_19_G - Input",
        name="G - Input",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_20_Trial for Ignition",
        name="Trial for Ignition",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_21_Ignition Stabilization",
        name="Ignition Stabilization",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_22_HSI Warm-up",
        name="HSI Warm-up",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_23_Interpurge",
        name="Interpurge",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_24_Postpurge",
        name="Postpurge",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_25_Prepurge",
        name="Prepurge",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_26_Auto-start Delay",
        name="Auto-start Delay",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_27_Time Left - Auto Restart",
        name="Time Left - Auto Restart",
        native_unit_of_measurement="min",
        state_class=STATE_CLASS_MEASUREMENT,
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_28_Recycle Counter",
        name="Recycle Counter",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_29_Retry Counter",
        name="Retry Counter",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_30_Link Relay Status",
        name="Link Relay Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_31_Dehumidification Relay Status",
        name="Dehumidification Relay Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_32_Humidification Relay Status",
        name="Humidification Relay Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_33_Y2 Relay Status",
        name="Y2 Relay Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_34_Y1 Relay Status",
        name="Y1 Relay Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_35_Ignition Status",
        name="Ignition Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_36_Calibration Status",
        name="Calibration Status",
),
SensorEntityDescription(
        key="LennoxHTTPS_Diagnostic_2_37_Calibration Invalid",
        name="Calibration Invalid",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_temperatureStatus",
        name="temperatureStatus",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_humidityStatus",
        name="humidityStatus",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_doNotPersist",
        name="doNotPersist",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_fan",
        name="fan",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_allergenDefender",
        name="allergenDefender",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_humidity",
        name="humidity",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_temperature",
        name="temperature",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_damper",
        name="damper",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_heatCoast",
        name="heatCoast",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_defrost",
        name="defrost",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_systemMode",
        name="systemMode",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_fanMode",
        name="fanMode",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_husp",
        name="husp",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_sp",
        name="sp",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_desp",
        name="desp",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_csp",
        name="csp",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_hsp",
        name="hsp",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_hspC",
        name="hspC",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_startTime",
        name="startTime",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_humidityMode",
        name="humidityMode",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_spC",
        name="spC",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_cspC",
        name="cspC",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_humOperation",
        name="humOperation",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_scheduleExceptionIds",
        name="scheduleExceptionIds",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_balancePoint",
        name="balancePoint",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_tempOperation",
        name="tempOperation",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_ventilation",
        name="ventilation",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_demand",
        name="demand",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_aux",
        name="aux",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_coolCoast",
        name="coolCoast",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_ssr",
        name="ssr",
),
SensorEntityDescription(
        key="LennoxHTTPS_Zone_0_temperatureC",
        name="temperatureC",
),

```
