from scapy.all import TCP, rdpcap
import collections
import os
import re
import sys
import zlib

OUTDIR = '/home/kali/Documents/BlackHatPython2/virtual-env1/projects-python/pcap-processing'
PCAPS  = '/home/kali/Documents/BlackHatPython2/virtual-env1/projects-python/pcap-processing'

Response = collections.namedtuple('Response', ['header','payload'])

def get_header(payload):
    try:
        print(payload)
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]
        print(header_raw)
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None

    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', header_raw.decode()))
    if 'Content-Type' not in header:
        return None
    return header

def extract_content(Response, content_name='image'):
    content, content_type = None, None
    # Header with image as Content-Type: (image/png) or (image/jpg)
    if content_name in Response.header['Content-Type']:
        content_type = Response.header['Content-Type'].split('/')[1]
        print(content_type)
        content      = Response.payload[Response.payload.index(b'\r\n\r\n')+4:]
        print(content)

        if 'Content-Encoding' in Response.header:
            if Response.header['Content-Encoding'] == 'gzip':
                content = zlib.decompress(Response.payload, zlib.MAX_WBITS | 32)
            elif Response.header['Content-Encoding'] == 'deflate':
                content = zlib.decompress(Response.payload)
    
    return content, content_type

class Recapper:
    def __init__(self, fname):
        # Rdpcap read PCAP file and return a packet list
        pcap = rdpcap(fname)
        # Separates each TCP session into a dict with each TCP stream
        self.sessions  = pcap.sessions()
        self.responses = list()

    def get_responses(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:
                try:
                    # Same as Follow TCP Stream in Wireshark
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        payload += bytes(packet[TCP].payload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()

            if payload:
                header = get_header(payload)
                if header is None:
                    continue
                       
                        # Append to list 'responses'
                self.responses.append(Response(header=header, payload=payload)) 

    def write(self, content_name):
        for i, response in enumerate(self.responses):
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                # File name Name from counter in enumerate fuction and content-type value
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                print(f'Writing {fname}')
                with open(fname, 'wb') as f:
                    f.write(content)

if __name__ == '__main__':
    pfile    = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responses() 
    recapper.write('image')
