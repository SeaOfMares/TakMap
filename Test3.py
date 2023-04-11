import pyshark
from takprotobuf import CoT

def parse_pcapng(file_path):
    cap = pyshark.FileCapture(file_path)

    extracted_data = []

    for packet in cap:
        if hasattr(packet, 'data'):
            raw_data = bytes.fromhex(packet.data.data)
            try:
                cot_event = CoT.ParseFromString(raw_data)
                
                callsign = cot_event.detail.contact.callsign
                lat = cot_event.lat
                lon = cot_event.lon
                endpoint = cot_event.endpoint
                os = cot_event.detail.link.os
                device = cot_event.detail.link.device
                platform = cot_event.detail.link.platform
                version = cot_event.detail.link.version

                extracted_data.append({
                    'Callsign': callsign,
                    'Location': {
                        'Lat': lat,
                        'Lon': lon
                    },
                    'Endpoint': endpoint,
                    'OS': os,
                    'Device': device,
                    'Platform': platform,
                    'Version': version
                })
            except Exception as e:
                print(f"Error decoding message: {e}")

    return extracted_data

file_path = 'TAK_TrafficS.pcapng'
result = parse_pcapng(file_path)
print(result)
