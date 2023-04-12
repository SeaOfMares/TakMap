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
extracted_data = []
with open(file, 'rb') as f:
    parsedData=f.read()
    idx = 0
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
            tak_os = dData.cotEvent.detail.takv.os
            #print("OS: ", tak_os)
            print(dData.cotEvent)
            break
        except Exception as e:
            print("Something went wrong... ")
            print(dData+" .Error: "+str(e))

#print(extracted_data[:10])