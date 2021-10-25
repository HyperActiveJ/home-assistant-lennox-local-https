#!/usr/bin/env python3

import json
import requests
import time
import urllib3
from collections import defaultdict
from settings import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client:
    def __init__(self, client_id, ip):
        self.client_id = client_id
        self.ip = ip
        self.message_id = 0
        self.connected = False

    def connect(self):
        requests.post(f"https://{self.ip}/Endpoints/{self.client_id}/Connect", verify=False).raise_for_status()
        self.connected = True

    def connect_if_necessary(self):
        if not self.connected:
            self.connect()

    def disconnect(self):
        requests.post(f"https://{self.ip}/Endpoints/{self.client_id}/Disconnect", verify=False).raise_for_status()
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
        requests.post(f"https://{self.ip}/Messages/Publish", json=body, verify=False).raise_for_status()

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
        requests.post(f"https://{self.ip}/Messages/RequestData", json=body, verify=False).raise_for_status()

    def messages(self):
        while True:
            resp = requests.get(f"https://{self.ip}/Messages/{self.client_id}/Retrieve", verify=False)
            if len(resp.text) == 0:
                time.sleep(1)
                continue
            #print(json.dumps(resp.json(), indent=4, sort_keys=True))
            for message in resp.json()["messages"]:
                yield message


client = Client(CLIENT_ID, IP)
#Optional, enable diagnostic data
#client.command({
#    "systemControl": {
#        "diagControl": {
#            "level": 2
#        }
#    }
#})
client.request_data(["/devices", "/equipments", "/zones"])

zone_status_keys = {
    "demand": "Demand",
    "humidity": "Humidity",
    "temperature": "Temperature"
}

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

equipdict = nested_dict(3, str)
zonedict = nested_dict(2, str)
systemdict = nested_dict(2, str)
interfacedict = nested_dict(3, str)

i = 0
for message in client.messages():
    i += 1
    print(i)
    if i > 60:
        break
    try:
        #prettyprint = json.dumps(message, indent=2, sort_keys=True)
        #print(f"{prettyprint}")
        sensorkey = ""
        if "Data" in message:
            data = message["Data"]
            if "devices" in data:
                devices = data["devices"]
                prettyprint = json.dumps(devices, indent=2, sort_keys=True)
                print(f"*Info: Received Devices message, Not processing it yet but will eventually ")#{prettyprint}")
            elif "equipments" in data:
                #prettyprint = json.dumps(data, indent=2, sort_keys=True)
                #print(f"{prettyprint}")
                for equipment_data in data["equipments"]:
                    eid = equipment_data["id"]
                    equipment = equipment_data["equipment"]
                    equipType = equipment["equipType"]                            
                    for diagnostic_data in equipment["diagnostics"]:
                        did = diagnostic_data["id"]
                        for diag in diagnostic_data["diagnostic"]:
                            key = diag
                            value = diagnostic_data["diagnostic"].get(key)
                            #print(f"Diag: {eid} {equipType} {did} {key} {value} ") 
                            equipdict[eid][did][key] = value
                            sensorkey = f"LennoxHTTPS_Diagnostic_{eid}_{did}_{key}"
            elif "zones" in data:
                #prettyprint = json.dumps(data, indent=2, sort_keys=True)
                #print(f"{prettyprint}")
                for zone_data in data["zones"]:
                    zid = zone_data["id"]          
                    for status in zone_data["status"]:
                        key = status
                        value = zone_data["status"].get(status)
                        if "period" in key:
                            for substatus in value:
                               key = substatus
                               subvalue = value.get(substatus)
                               #print(f"sZone: {zid} {key} {subvalue} ") 
                               zonedict[zid][key] = subvalue 
                               sensorkey = f"LennoxHTTPS_Zone_{zid}_{key}"                               
                        else:                           
                            #print(f"Zone: {zid} {key} {value} ")   
                            zonedict[zid][key] = value
                            sensorkey = f"LennoxHTTPS_Zone_{zid}_{key}"   
            elif "system" in data:
                system = data["system"]
                if "status" in system:
                    system_status = system["status"]
                    for status in system_status:
                            key = status
                            value = system_status.get(status)
                            print(f"System Status: {key} {value} ")
                            systemdict["status"][key] = value
                            sensorkey = f"LennoxHTTPS_System_status_{key}"   
                elif "time" in system:
                    system_status = system["time"]
                    for status in system_status:
                            key = status
                            value = system_status.get(status)
                            print(f"System Time: {key} {value} ")
                            systemdict["time"][key] = value
                            sensorkey = f"LennoxHTTPS_System_time_{key}"                               
                else:
                    prettyprint = json.dumps(system, indent=2, sort_keys=True)
                    print(f"**Warning, Status not found in system message {prettyprint}")
            elif "rgw" in data:
                print("Debug: Ignoring Data rgw message, doesnt contain anything very useful...")
            elif "nmlccwifi" in data:
                print("Debug: Ignoring Data nmlccwifi message, doesnt contain anything very useful...")
            elif "serverAssigned" in data:
                print("Debug: Ignoring Data nmlccwifi message, doesnt contain anything very useful...")
            elif "interfaces" in data:
                temp = data["interfaces"]
                interfaces = temp[0]
                if "Info" in interfaces:
                    info = interfaces["Info"]
                    for temp in info:
                        for status in info[temp]:
                            key = status
                            value = info[temp].get(status)
                            print(f"Inteface Info: {temp} {key} {value} ")
                            interfacedict[temp][key] = value
                            sensorkey = f"LennoxHTTPS_Interface_{temp}_{key}"                              
                elif "Publisher" in interfaces:
                     print("Debug: Ignoring Data Interfaces Publisher message, doesnt contain anything very useful...")
                else:
                    prettyprint = json.dumps(interfaces, indent=2, sort_keys=True)
                    print(f"**Warning: no info in data interfaces message {interfaces}")
                    for x in interfaces:
                        print(f"x {x}")
                    print(f"{prettyprint}")

            else:
                prettyprint = json.dumps(data, indent=2, sort_keys=True)
                print(f"**Warning: Unknown data message type {prettyprint}")
        else:
            prettyprint = json.dumps(message, indent=2, sort_keys=True)
            print(f"**Warning: Unkonwn Message Type {prettyprint}")
    except:
        raise

print("done")
for e in systemdict:
    for d in systemdict[e]:
        val  = systemdict[e][d]
        #print(f"s {e} {d} {val}")
        print("SensorEntityDescription(")
        print(f"\tkey=\"LennoxHTTPS_System_{e}_{d}\",")
        print(f"\tname=\"{d}\",")
        if "TemperatureC" in d:
            print(f"\tnative_unit_of_measurement=TEMP_CELSIUS,")
            print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
            print(f"\tdevice_class=DEVICE_CLASS_TEMPERATURE,")
        elif "Temperature" in d:
            print(f"\tnative_unit_of_measurement=TEMP_FAHRENHEIT,")
            print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
            print(f"\tdevice_class=DEVICE_CLASS_TEMPERATURE,")
        print("),")
        
for e in equipdict:
    for d in equipdict[e]:
        if(e>0): #equipment 0 has no diagnostic data
            name = equipdict[e][d]['name']
            unit = equipdict[e][d]['unit']
            val = equipdict[e][d]['value']
            #print(f"e {e} {d} {name} {unit}... {val}")
            print("SensorEntityDescription(")
            print(f"\tkey=\"LennoxHTTPS_Diagnostic_{e}_{d}_{name}\",")
            print(f"\tname=\"{name}\",")
            if "V" == unit:
                print(f"\tnative_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
                print(f"\tdevice_class=DEVICE_CLASS_VOLTAGE,")
            elif "A" == unit:
                print(f"\tnative_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
                print(f"\tdevice_class=DEVICE_CLASS_CURRENT,")
            elif "F" == unit:
                print(f"\tnative_unit_of_measurement=TEMP_FAHRENHEIT,")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
                print(f"\tdevice_class=DEVICE_CLASS_TEMPERATURE,")
            elif "CFM" == unit:
                print(f"\tnative_unit_of_measurement=VOLUME_FLOW_RATE_CUBIC_FEET_PER_MINUTE,")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
            elif "Temperature" in name:
                print(f"\tnative_unit_of_measurement=TEMP_FAHRENHEIT,")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
                print(f"\tdevice_class=DEVICE_CLASS_TEMPERATURE,")
            elif unit != "":
                print(f"\tnative_unit_of_measurement=\"{unit}\",")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
            #todo device classes
            print("),")

for e in zonedict:
    for d in zonedict[e]:
        if(e==0): #only handle one zone for now, dont have a way to test more then one
            val  = zonedict[e][d]
            #print(f"z {e} {d} {val}")
            print("SensorEntityDescription(")
            print(f"\tkey=\"LennoxHTTPS_Zone_{e}_{d}\",")
            print(f"\tname=\"{d}\",")
            if "temperature" in d or d == "sp":
                print(f"\tnative_unit_of_measurement=TEMP_FAHRENHEIT,")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
                print(f"\tdevice_class=DEVICE_CLASS_TEMPERATURE,")
            elif "humidity" in d:
                print(f"\tnative_unit_of_measurement=TEMP_FAHRENHEIT,")
                print(f"\tstate_class=STATE_CLASS_MEASUREMENT,")
                print(f"\tdevice_class=DEVICE_CLASS_HUMIDITY,")
            print("),")        
    
for e in interfacedict:
    for d in interfacedict[e]:
            val  = interfacedict[e][d]
            #print(f"i {e} {val}") 
            print("SensorEntityDescription(")
            print(f"\tkey=\"LennoxHTTPS_Interface_{e}_{d}\",")
            print(f"\tname=\"{e} {d}\",")
            print("),")       
