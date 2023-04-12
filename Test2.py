import os
import shutil
from takprotobuf import parseProto
import pandas as pd
# Again, not sure what we are doing here, but I think it's from fileParser.
#This is actually something unique for XML parser. 

# To keep track while we look for the header info.
idx = 0
file = 'TAK_TrafficS.pcapng'
finalResult={'Callsign':[],'Lat':[],'Lon':[]}
with open(file, 'rb') as f:
    parsedData=f.read()
    idx = 0
    extracted_data = []
# \xbf, \x01, \xbf are interesting things we want. What are they?
    while parsedData.find(b'\xbf\x01\xbf', idx) != -1:
        headerLocation = parsedData.find(b'\xbf\x01\xbf', idx)
        idx = headerLocation + 3
        #print(idx - 3)
        # Part of the prototak library???
        toDecode = parsedData[headerLocation:]
        dData = parseProto(toDecode)
        # Print tests until we get the map connected.
        try:
            uid = dData.cotEvent.uid
            endpoint = dData.cotEvent.detail.contact.endpoint
            callsign = dData.cotEvent.detail.contact.callsign
            lat = dData.cotEvent.lat
            lon = dData.cotEvent.lon
            device = dData.cotEvent.detail.takv.device
            platform = dData.cotEvent.detail.takv.platform
            tak_os = dData.cotEvent.detail.takv.os
            version = dData.cotEvent.detail.takv.version
            
            extracted_data.append({
                    'Uid': uid,
                    'Callsign': callsign,
                    'Location': {
                        'Lat': lat,
                        'Lon': lon
                    },
                    'Endpoint': endpoint,
                    'OS': tak_os,
                    'Device': device,
                    'Platform': platform,
                    'Version': version
                })

        except Exception as e:
            print("Something went wrong... ")
            print(dData+" .Error: "+str(e))

print(extracted_data[:10])