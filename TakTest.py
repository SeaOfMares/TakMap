import plotly.express as px
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
                    'Lat': lat,
                    'Lon': lon,
                    'Endpoint': endpoint,
                })

        except Exception as e:
            print("Something went wrong... ")
            print(dData+" .Error: "+str(e))

#print(extracted_data[:10])
df = pd.DataFrame(extracted_data)
print(df.iloc[0])
# Create a scatter_mapbox
fig = px.scatter_mapbox(
    df,
    lat='Lat',
    lon='Lon',
    hover_name='Callsign',
    hover_data=['Endpoint'],
    zoom=2,
    mapbox_style='carto-positron'  # OpenStreetMap based style
)

# Show the figure
fig.show()