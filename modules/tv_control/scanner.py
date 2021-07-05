import scapy.all as scapy
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP Address/Adresses')
    options = parser.parse_args()

    if not options.target:
        parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options

def scan(ip):
    # scapy.arping(ip)


    arp_req_frame = scapy.ARP(pdst = ip)
    # arp_req_frame.show()

    broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    # broadcast_ether_frame.show()

    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
    # broadcast_ether_arp_req_frame.show()

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 3, verbose = False)[0]
    result = []
    for i in range(0,len(answered_list)):
        client_dict = {"ip" : answered_list[i][1].psrc, "mac" : answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result


def display_result(result):
    #print("-----------------------------------\nIP Address\tMAC Address\n-----------------------------------")
    with open('ip.txt', 'w') as f:
        #f.write(result)
        for i in result:
            #f.write(str(i['ip']))
            print("{}\t{}".format(i["ip"], i["mac"]))
    


#options = get_args()
# scanned_output = scan(options.target)
# display_result(scanned_output)