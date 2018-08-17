curl -v http://10.156.14.162:8001/cat?id=cdx1234 -XPOST -H "no-check:1" -H "pwd: local123" -H "Content-Type: application/json" --data '
{
  "refCatalogueSchema": "cdx_base_staticThing.json",
  "id": "cdx1234",
  "resourceType": "streetlight",
  "tags": [
    "onstreet",
    "Energy",
    "still under development"
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
    "accessEndPoint": {
      "value": "https://smartcity.rbccps.org/api/0.1.0/historicData",
      "describes": "End point to access the archived values (database access endpoint)"
    },
    "subscriptionEndPoint": {
      "value": "https://smartcity.rbccps.org/api/0.1.0/subscribe",
      "describes": "End point for subscribing to LIVE data"
    },
    "resourceAPIInfo": {
      "value": "https://rbccps-iisc.github.io",
      "describes": "Information on how to use various APIs (access, update, cat) associated with this resource"
    }
  },
  "message_schemas": {
     "type": "object",
     "properties": {
         "observation_msg": {
             "schema": "http://json-schema.org/draft-07/schema#",
             "type": "object",
             "describes": "Observation messages from the streetlight",
             "direction": "fromThing",
             "priority": "low",
             "tags": ["onstreet sensors","energy"],
             "sharing": "public",
             "required": ["caseTemperature","dataSamplingInstant"],
             "properties": {
               "dataSamplingInstant": {
                 "type": "number",
                 "description": "Sampling Time in EPOCH format",
                 "units": "seconds"
               },
               "caseTemperature": {
                 "type": "number",
                 "description": "Temperature of the device casing",
                 "units": "degreeCelsius"
               },
               "powerConsumption": {
                 "type": "number",
                 "description": "Power consumption of the device",
                 "units": "watts"
               },
               "luxOutput": {
                 "type": "number",
                 "description": "lux output of LED measured at LED",
                 "units": "lux"
               },
               "ambientLux": {
                 "type": "number",
                 "description": "lux value of ambient",
                 "units": "lux"
               }
            },
            "additionalProperties": false
           }
      },
      "additionalProperties": false
  }
}
'
