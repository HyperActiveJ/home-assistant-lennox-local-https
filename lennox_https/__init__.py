"""The Lennox HTTPS Integration."""

import json
import requests
import time
import urllib3
import asyncio
import logging
import threading
import socket, time
from datetime import timedelta
from typing import Optional
from threading import Thread
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_time_interval
import sys, os
from .const import (
    DOMAIN,
    DEFAULT_NAME,
)

_LOGGER = logging.getLogger(__name__)

LENNOX_HTTPS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({cv.slug: LENNOX_HTTPS_SCHEMA})}, extra=vol.ALLOW_EXTRA
)

PLATFORMS = ["sensor"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

async def async_setup(hass, config):
    """Set up the Lennox HTTPS component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lennox HTTPS from a config entry."""
    host = entry.data[CONF_HOST]
    name = entry.data[CONF_NAME]
    
    #_LOGGER.debug("2 async_setup_entry host %s name %s  port %s DOMAIN %s ", host, name, port, DOMAIN) 
    
    hub = LennoxHTTPSHub(
        hass, name, host
    )
    """Register the hub."""
    hass.data[DOMAIN][name] = {"hub": hub}

    #hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if not unload_ok:
        return False
    hass.data[DOMAIN].pop(entry.data["name"])
    return True


class LennoxHTTPSHub:
    """TODO."""            
    def __init__(
        self,
        hass,
        name,
        host,
    ):
        """Initialize the LennoxHTTPS hub."""
        self._hass = hass
        self._lock = threading.Lock()
        self._name = name
        self._sensors = []
        self.data = {}    
        self.connected = False
        self.host = host
        self.message_id = 0
        self.client_id = "homeassistant"
        self._serial_thread_isEnabled = True
        self._serial_thread = Thread(target = self.tcp_read, args = ())
        self._serial_thread.name = "Lennox HTTPS Reader Thread"
        self._serial_thread.start()
        self.findSensorErrorCount = 0
        
    
    @callback
    def async_add_lennoxhttps_sensor(self, sensor):
        """Listen for data updates."""
        self._sensors.append(sensor)

    @callback
    def async_remove_lennoxhttps_sensor(self, sensor):
        self._sensors.remove(sensor)
        if not self._sensors:
            """stop the interval timer upon removal of last sensor"""
            self._serial_thread_isEnabled = False
 
    @property
    def name(self):
        """Return the name of this hub."""
        return self._name
        
    def available(self):
        return self.connected
            
    
    def updateSensor(self, key, value):
        for sensor in self._sensors:
            if sensor.unique_id == key:
                sensor._data_updated(value)
                #_LOGGER.debug(f"updated sensor {key} {value}")
                return
        self.findSensorErrorCount += 1
        if self.findSensorErrorCount > 100:
            _LOGGER.error(f"Unable to find sensor for key {key}")
    
    def tcp_read(self): 
        #TODO, detect disconnection and reconnect
        #Optional, Uncomment to enable diagnostic data:
        #self.command({
        #   "systemControl": {
        #       "diagControl": {
        #           "level": 2
        #       }
        #   }
        #})
        self.request_data(["/devices", "/equipments", "/zones"])
        for message in self.messages():
            
            try:
                if "Data" in message:
                    data = message["Data"]
                    if "devices" in data:
                        devices = data["devices"]
                        #prettyprint = json.dumps(devices, indent=2, sort_keys=True)
                        _LOGGER.debug(f"*Info: Received Devices message, Not processing it yet but will eventually ")#{prettyprint}")
                    elif "equipments" in data:
                        for equipment_data in data["equipments"]:
                            eid = equipment_data["id"]
                            equipment = equipment_data["equipment"]
                            equipType = equipment["equipType"]                            
                            for diagnostic_data in equipment["diagnostics"]:
                                did = diagnostic_data["id"]
                                for diag in diagnostic_data["diagnostic"]:
                                    key = diag
                                    value = diagnostic_data["diagnostic"].get(key)
                                    #_LOGGER.debug(f"Diag: {eid} {equipType} {did} {key} {value} ")
                                    if key == "value":
                                        sensorkey = f"LennoxHTTPS_Diagnostic_{eid}_{did}"
                                        self.updateSensor(sensorkey, value)
                    elif "zones" in data:
                        for zone_data in data["zones"]:
                            zid = zone_data["id"]          
                            for status in zone_data["status"]:
                                key = status
                                value = zone_data["status"].get(status)
                                if "period" in key:
                                    for substatus in value:
                                       key = substatus
                                       subvalue = value.get(substatus)
                                       #_LOGGER.debug(f"sZone: {zid} {key} {subvalue} ") 
                                       sensorkey = f"LennoxHTTPS_Zone_{zid}_{key}"
                                       self.updateSensor(sensorkey, subvalue)                                       
                                else:                           
                                    #_LOGGER.debug(f"Zone: {zid} {key} {value} ")   
                                    sensorkey = f"LennoxHTTPS_Zone_{zid}_{key}"
                                    self.updateSensor(sensorkey, value)                                    
                    elif "system" in data:
                        system = data["system"]
                        if "status" in system:
                            system_status = system["status"]
                            for status in system_status:
                                    key = status
                                    value = system_status.get(status)
                                    #_LOGGER.debug(f"System Status: {key} {value} ")
                                    sensorkey = f"LennoxHTTPS_System_status_{key}"
                                    self.updateSensor(sensorkey, value)
                        elif "time" in system:
                            system_status = system["time"]
                            for status in system_status:
                                    key = status
                                    value = system_status.get(status)
                                    #_LOGGER.debug(f"System Time: {key} {value} ")
                                    sensorkey = f"LennoxHTTPS_System_time_{key}"
                                    self.updateSensor(sensorkey, value)
                        else:
                            prettyprint = json.dumps(system, indent=2, sort_keys=True)
                            _LOGGER.warning(f"**Warning, Status not found in system message {prettyprint}")
                    elif "rgw" in data:
                        dummy = 0
                        #_LOGGER.debug("Debug: Ignoring Data rgw message, doesnt contain anything very useful...")
                    elif "nmlccwifi" in data:
                        dummy = 0
                        #_LOGGER.debug("Debug: Ignoring Data nmlccwifi message, doesnt contain anything very useful...")
                    elif "serverAssigned" in data:
                        dummy = 0
                        #_LOGGER.debug("Debug: Ignoring Data nmlccwifi message, doesnt contain anything very useful...")
                    elif "interfaces" in data:
                        temp = data["interfaces"]
                        interfaces = temp[0]
                        if "Info" in interfaces:
                            info = interfaces["Info"]
                            for temp in info:
                                for status in info[temp]:
                                    key = status
                                    value = info[temp].get(status)
                                    #_LOGGER.debug(f"Inteface Info: {temp} {key} {value} ")
                                    sensorkey = f"LennoxHTTPS_Interface_{temp}_{key}"
                                    self.updateSensor(sensorkey, value)
                        elif "publisher" in interfaces:
                            #dummy = 0
                            _LOGGER.debug("Debug: Ignoring Data Interfaces Publisher message, doesnt contain anything very useful...")
                        else:
                            prettyprint = json.dumps(interfaces, indent=2, sort_keys=True)
                            _LOGGER.warning(f"**Warning: no info in data interfaces message {interfaces}")
                    else:
                        prettyprint = json.dumps(data, indent=2, sort_keys=True)
                        _LOGGER.warning(f"**Warning: Unknown data message type {prettyprint}")
                else:
                    prettyprint = json.dumps(message, indent=2, sort_keys=True)
                    _LOGGER.warning(f"**Warning: Unkonwn Message Type {prettyprint}")
            except:
                #todo, do somthing better
                raise           
               
    def connect(self):
        requests.post(f"https://{self.host}/Endpoints/{self.client_id}/Connect", verify=False).raise_for_status()
        self.connected = True

    def connect_if_necessary(self):
        if not self.connected:
            self.connect()

    def disconnect(self):
        requests.post(f"https://{self.host}/Endpoints/{self.client_id}/Disconnect", verify=False).raise_for_status()
        self.connected = True

    def _generate_message_id(self):
        used = self.message_id
        self.message_id += 1
        return str(used)

    def command(self, data):
        body = {
            "MessageId": self._generate_message_id(),
            "MessageType": "Command",
            "SenderId": self.client_id,
            "TargetId": "LCC",
            "data": data,
            "AdditionalParameters": {
                "JSONPath": list(data.keys())[0]
            }
        }
        self.connect_if_necessary()
        requests.post(f"https://{self.host}/Messages/Publish", json=body, verify=False).raise_for_status()

    def request_data(self, paths):
        body = {
            "MessageId": self._generate_message_id(),
            "MessageType": "RequestData",
            "SenderId": self.client_id,
            "TargetId": "LCC",
            "AdditionalParameters": {
                "JSONPath": f"1;{';'.join(paths)}"
            }
        }
        self.connect_if_necessary()
        requests.post(f"https://{self.host}/Messages/RequestData", json=body, verify=False).raise_for_status()

    def messages(self):
        while True:
            resp = requests.get(f"https://{self.host}/Messages/{self.client_id}/Retrieve", verify=False)
            if len(resp.text) == 0:
                time.sleep(1)
                continue
            #_LOGGER.debug("Got: %s", resp.json())
            for message in resp.json()["messages"]:
                yield message           
