import pyshark

def open_capture_file(file_path):
    return pyshark.FileCapture(file_path)

def print_matching_packets(capture, protocol, port, max_count):
    count = max_count
    for packet in capture:
        if count <= 0:
            break
        if protocol in packet and packet[protocol].dstport == port:
            print(packet)
            count -= 1

def print_protocol_packets(capture, protocol, max_count):
    count = max_count
    for packet in capture:
        if count <= 0:
            break
        if protocol in packet:
            print(packet)
            count -= 1
def main():
    # Open the pcapng file
    capture_file_path = 'TAK_TrafficS.pcapng'
    cap = open_capture_file(capture_file_path)

    max_count = 10
    udp_port = '6969'
    tcp_port = '4242'

    # Print matching UDP packets
    #print_matching_packets(cap, 'UDP', udp_port, max_count)

    print_protocol_packets(cap, 'gps',max_count)

    # Print matching TCP packets
    #print_matching_packets(cap, 'TCP', tcp_port, max_count)

if __name__ == "__main__":
    main()