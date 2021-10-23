import logging
from typing import Optional, Dict, Any
from .const import (
    DOMAIN,
    ATTR_STATUS_DESCRIPTION,
    ATTR_MANUFACTURER,
)
from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.const import * # TODO only import required...
from homeassistant.components.sensor import (
    DEVICE_CLASS_ENERGY,
    PLATFORM_SCHEMA,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    SensorEntity,
    SensorEntityDescription,
    StateType,
)
from homeassistant.core import callback
from homeassistant.util import dt as dt_util
from homeassistant.helpers.entity import DeviceInfo

import homeassistant.helpers.config_validation as cv

import voluptuous as vol
from threading import Thread


_LOGGER = logging.getLogger(__name__)

SENSORS = (
    SensorEntityDescription(
            key="LennoxHTTPS_System_time_sysUpTime",
            name="sysUpTime",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_System_time_currentTime",
            name="currentTime",
    ),
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
            key="LennoxHTTPS_Diagnostic_1_0",
            name="Comp. Short Cycle Delay Active",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_1",
            name="Cooling Rate",
            native_unit_of_measurement="%",
            state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_2",
            name="High Pressure Switch",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_3",
            name="Low Pressure Switch",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_4",
            name="Top Cap Switch Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_5",
            name="Liquid Line Temp",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_6",
            name="Ambient Temp",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_7",
            name="Compressor Active Alarm",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_8",
            name="Compressor Hz",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_9",
            name="Compressor Speed Reduction",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_10",
            name="Heat Sink Temperature",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_11",
            name="Inverter Input Voltage",
            native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_VOLTAGE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_12",
            name="Inverter Input Current",
            native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_CURRENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_13",
            name="DC Link Voltage",
            native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_VOLTAGE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_1_14",
            name="Compressor Current",
            native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_CURRENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_0",
            name="Heating Rate",
            native_unit_of_measurement="%",
            state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_1",
            name="Blower CFM Demand",
            native_unit_of_measurement=VOLUME_FLOW_RATE_CUBIC_FEET_PER_MINUTE,
            state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_2",
            name="Blower Off Delay",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_3",
            name="Blower On Delay",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_4",
            name="Indoor Blower RPM",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_5",
            name="Indoor Blower Power",
            native_unit_of_measurement="%",
            state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_6",
            name="Inducer Blower RPM",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_7",
            name="Flame Current",
            native_unit_of_measurement="uA",
            state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_8",
            name="Flame Sense",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_9",
            name="Outdoor Temperature",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_10",
            name="Discharge Air Temperature",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_11",
            name="Line Voltage",
            native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_VOLTAGE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_12",
            name="24VAC Voltage",
            native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_VOLTAGE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_13",
            name="Igniter Voltage",
            native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_VOLTAGE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_14",
            name="High Pressure Switch",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_15",
            name="Low Pressure Switch",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_16",
            name="Primary Limit Switch",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_17",
            name="Rollout Switch",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_18",
            name="Gas Valve",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_19",
            name="G - Input",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_20",
            name="Trial for Ignition",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_21",
            name="Ignition Stabilization",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_22",
            name="HSI Warm-up",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_23",
            name="Interpurge",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_24",
            name="Postpurge",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_25",
            name="Prepurge",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_26",
            name="Auto-start Delay",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_27",
            name="Time Left - Auto Restart",
            native_unit_of_measurement="min",
            state_class=STATE_CLASS_MEASUREMENT,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_28",
            name="Recycle Counter",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_29",
            name="Retry Counter",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_30",
            name="Link Relay Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_31",
            name="Dehumidification Relay Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_32",
            name="Humidification Relay Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_33",
            name="Y2 Relay Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_34",
            name="Y1 Relay Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_35",
            name="Ignition Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_36",
            name="Calibration Status",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Diagnostic_2_37",
            name="Calibration Invalid",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_temperatureStatus",
            name="Zone 0 temperatureStatus",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_humidityStatus",
            name="Zone 0 humidityStatus",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_HUMIDITY,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_doNotPersist",
            name="Zone 0 doNotPersist",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_fan",
            name="Zone 0 fan",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_allergenDefender",
            name="Zone 0 allergenDefender",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_humidity",
            name="Zone 0 humidity",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_HUMIDITY,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_temperature",
            name="Zone 0 temperature",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_damper",
            name="Zone 0 damper",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_heatCoast",
            name="Zone 0 heatCoast",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_defrost",
            name="Zone 0 defrost",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_systemMode",
            name="Zone 0 systemMode",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_fanMode",
            name="Zone 0 fanMode",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_husp",
            name="Zone 0 husp",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_sp",
            name="Zone 0 sp",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_desp",
            name="Zone 0 desp",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_csp",
            name="Zone 0 csp",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_hsp",
            name="Zone 0 hsp",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_hspC",
            name="Zone 0 hspC",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_startTime",
            name="Zone 0 startTime",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_humidityMode",
            name="Zone 0 humidityMode",
            native_unit_of_measurement=TEMP_FAHRENHEIT,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_HUMIDITY,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_spC",
            name="Zone 0 spC",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_cspC",
            name="Zone 0 cspC",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_humOperation",
            name="Zone 0 humOperation",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_scheduleExceptionIds",
            name="Zone 0 scheduleExceptionIds",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_balancePoint",
            name="Zone 0 balancePoint",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_tempOperation",
            name="Zone 0 tempOperation",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_ventilation",
            name="Zone 0 ventilation",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_demand",
            name="Zone 0 demand",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_aux",
            name="Zone 0 aux",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_coolCoast",
            name="Zone 0 coolCoast",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_ssr",
            name="Zone 0 ssr",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Zone_0_temperatureC",
            name="Zone 0 temperatureC",
            native_unit_of_measurement=TEMP_CELSIUS,
            state_class=STATE_CLASS_MEASUREMENT,
            device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_macAddr",
            name="status macAddr",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_ssid",
            name="status ssid",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_ip",
            name="status ip",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_router",
            name="status router",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_networkStatus",
            name="status networkStatus",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_channel",
            name="status channel",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_dns",
            name="status dns",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_dns2",
            name="status dns2",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_subnetMask",
            name="status subnetMask",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_bitRate",
            name="status bitRate",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_speed",
            name="status speed",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_status_rssi",
            name="status rssi",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_APDetails_rssi",
            name="APDetails rssi",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_APDetails_security",
            name="APDetails security",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_APDetails_password",
            name="APDetails password",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_APDetails_ssid",
            name="APDetails ssid",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_APDetails_bssid",
            name="APDetails bssid",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_diagnostics_ssid",
            name="diagnostics ssid",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_diagnostics_bssid",
            name="diagnostics bssid",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_diagnostics_txByteCount",
            name="diagnostics txByteCount",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_diagnostics_rxByteCount",
            name="diagnostics rxByteCount",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_diagnostics_ip4addr",
            name="diagnostics ip4addr",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_diagnostics_txPacketCount",
            name="diagnostics txPacketCount",
    ),
    SensorEntityDescription(
            key="LennoxHTTPS_Interface_diagnostics_rxPacketCount",
            name="diagnostics rxPacketCount",
    ),
)


async def async_setup_entry(hass, config, async_add_entities, discovery_info=None):
    hub_name = config.data[CONF_NAME]
    hub = hass.data[DOMAIN][hub_name]["hub"]
    entities = [LennoxHTTPSSensor(hub_name, hub, description) for description in SENSORS]
    async_add_entities(entities)



class LennoxHTTPSSensor(SensorEntity):
    """Representation of an Rainforest EMU2 Eagle sensor."""

   
    def __init__(self, platform_name, hub, entity_description):
        """Initialize the sensor."""
        super().__init__() 
        self._platform_name = platform_name
        self._hub = hub
        self.entity_description = entity_description
        self.val = ""
        

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._hub.async_add_lennoxhttps_sensor(self)


    async def async_will_remove_from_hass(self) -> None:
        self._hub.async_remove_lennoxhttps_sensor(self)

    @callback
    def _data_updated(self, val):
        self.val = val
        self.async_write_ha_state()

    @property
    def unique_id(self) -> str:
        """Return unique ID of entity."""
        return f"{self.entity_description.key}"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self._hub.available()

    @property
    def native_value(self) -> StateType:
        """Return native value of the sensor."""
        return self.val

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return {
            "name": self._platform_name,
            "identifiers": {(DOMAIN, self._platform_name)},
            "manufacturer": "P Jorgensen / Lennox",
            "model": "S30 HTTPS",
        }