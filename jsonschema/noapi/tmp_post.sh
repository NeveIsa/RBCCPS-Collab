curl -v http://localhost:8001/cat?id=test1234 -XPOST -H "no-check:1" -H "pwd: local123" -H "Content-Type: application/json" --data '
{
  "refCatalogueSchema": "generic_iotdevice_schema.json",
  "id": "test1234",
  "resourceType": "streetlight",
  "tags": [
    "onstreet",
    "Energy",
    "still under development !##"
  ],
  "refCatalogueSchemaRelease":"0.1.0",
  "latitude": {
    "value": 13.0143335,
    "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"
  },
  "longitude": {
    "value": 77.5678424,
    "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"
  },
  "owner": {
    "name": "IISC",
    "website": "http://www.iisc.ac.in"
  },
  "provider": {
    "name": "Robert Bosch Centre for Cyber Physical Systems, IISc",
    "website": "http://rbccps.org"
  },
  "geoLocation": {
    "address": "80 ft Road, Bangalore, 560012"
  },
  "accessMechanism": {
    "requestAccessSite": {
      "describes": "URI for getting permissions to access the device", 
      "value": "http://rbccps.org/middleware/requestAccess"
    }, 
    "accessEndPoint": {
       "value": "https://rbccps.org/middleware/api/{api_ver}/db",
       "describes": "End point to access the archived values (database access endpoint)"
    },
    "subscriptionEndPoint": {
       "value": "mqtt://rbccps.org/subscription/live",
       "describes": "End point for subscribing to LIVE data"
    },
    "additionalResourceInfo": {
       "value": "http://rbccps.org/resourceInfo/{id}",
       "describes": "Additional information about the device"
    },
    "resourceAPIInfo": {
       "value": "http://rbccps.org/resourceInfo/api",
       "describes": "Information on how to use various APIs (access, update, cat) associated with this resource"
    }
  },
  "data_schema": {
    "type": "object",
    "properties": {
        "dataSamplingInstant": {
          "type": "number",
          "description": "Sampling Time in EPOCH format",
          "units": "seconds",
          "permissions": "read",
          "accessModifier": "public"
        },
        "caseTemperature": {
          "type": "number",
          "description": "Temperature of the device casing",
          "units": "degreeCelsius",
          "permissions": "read",
          "accessModifier": "public"
        },
        "powerConsumption": {
          "type": "number",
          "description": "Power consumption of the device",
          "units": "watts",
          "permissions": "read",
          "accessModifier": "public"
        },
        "luxOutput": {
          "type": "number",
          "description": "lux output of LED measured at LED",
          "units": "lux",
          "permissions": "read",
          "accessModifier": "public"
        },
        "ambientLux": {
          "type": "number",
          "description": "lux value of ambient",
          "units": "lux",
          "permissions": "read",
          "accessModifier": "public"
        },
        "targetPowerState": {
          "type": "string",
          "enum": [
            "ON",
            "OFF"
          ],
          "units": "dimensionless",
          "description": "If set to ON, turns ON the device. If OFF turns OFF the device. Writeable parameter. Writeable only allowed for authorized apps",
          "permissions": "read-write",
          "accessModifier": "protected"
        },
        "targetBrightnessLevel": {
          "type": "number",
          "description": "Number between 0 to 100 to indicate the percentage brightness level. Writeable only allowed for authorized apps",
          "units": "percent",
          "permissions": "read-write",
          "accessModifier": "protected"
        },
        "targetControlPolicy": {
          "enum": [
            "AUTO_TIMER",
            "AUTO_LUX",
            "MANUAL"
          ],
          "units": "dimensionless",
          "permissions": "read-write",
          "description": "Indicates which of the behaviours the device should implement. AUTO_TIMER is timer based, AUTO_LUX uses ambient light and MANUAL is controlled by app. Writeable only allowed for authorized apps",
          "accessModifier": "protected"
        },
        "targetAutoTimerParams": {
          "type": "object",
          "permissions": "read-write",
          "properties": {
            "targetOnTime": {
              "type": "number",
              "description": "Indicates time of day in seconds from 12 midnight when device turns ON in AUTO_TIMER. Writeable only allowed for authorized apps",
              "units": "seconds",
              "accessModifier": "protected"
            },
            "targetOffTime": {
              "type": "number",
              "description": "Indicates time of day in seconds from 12 midnight when device turns OFF in AUTO_TIMER. Writeable only allowed for authorized apps",
              "units": "seconds",
              "accessModifier": "protected"
            }
          }
        },
        "targetAutoLuxParams": {
          "type": "object",
          "permissions": "read-write",
          "properties": {
            "targetOnLux": {
              "type": "number",
              "description": "Indicates ambient lux when device turns ON in AUTO_LUX. Writeable only allowed for authorized apps",
              "units": "lux",
              "accessModifier": "protected"
            },
            "targetOffLux": {
              "type": "number",
              "description": "Indicates ambient lux when device turns OFF in AUTO_LUX. Writeable only allowed for authorized apps",
              "units": "lux",
              "accessModifier": "protected"
            }
          }
        }
    },
    "additionalProperties": false
  },
  "serialization_from_device":{
    "format": "protocol-buffers",
    "schema_ref": {
       "type": "proto 2",
       "mainMessageName": "sensor_values",
       "link": "https://raw.githubusercontent.com/rbccps-iisc/applications-streetlight/master/proto_stm/txmsg/sensed.proto"
    }
  },
  "serialization_to_device":{
    "format": "protocol-buffers",
    "schema_ref": {
       "type": "proto 2",
       "mainMessageName": "targetConfigurations",
       "link": "https://raw.githubusercontent.com/rbccps-iisc/applications-streetlight/master/proto_stm/rxmsg/actuated.proto"
    }
  }
}
'
