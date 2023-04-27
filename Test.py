import pyshark
import pandas as pd

# Replace this with the path to your pcap file
pcap_file = '011723-WSMR-Unclass-NIKTOSCAN.pcapng'
print("Reading ", pcap_file)
capture = pyshark.FileCapture(pcap_file)

# Initialize the data structure to store the information
data = []

# Define a function to process each packet
def process_packet(packet):
    try:
        system_ip = packet.ip.src
        destination_ip = packet.ip.dst
        protocol_number = packet.transport_layer
        sent_packets = packet.length

        # Add the extracted information to the data structure
        
        data.append([system_ip, destination_ip, protocol_number, sent_packets])

    except AttributeError:
        # Ignore the packet if it doesn't have the required attributes
        pass

# Start processing packets
capture.apply_on_packets(process_packet)

# Create a DataFrame from the data
columns = ['System IP', 'Destination IP','Protocol', 'Sent Packets' ]
df = pd.DataFrame(data, columns=columns)

# Print the DataFrame
#print(df)
print(df['System IP'].unique())

print(df[df['System IP'] == "172.16.100.240"])
print("END\n-----------------------------------")