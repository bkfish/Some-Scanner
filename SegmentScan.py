from scapy.all import srp, Ether, ARP
import re
print("Please input SegementScan")
print("If you want Scan 192.168.5.1/24 You just need input 5 ")
Segement=input("input:")
if re.match(r"^[0-9]{1,3}$", Segement):
    print ("Segement is OK")
else:
    print ("Segement format is invaild")
    exit()
IpScan = '192.168.'+Segement+'.1/24'
print("You will Scan Segement "+IpScan+"\n")
try:
    ans,unans = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=IpScan), timeout=2)
except Exception as e:
    print(e)
else:
    for send, rcv in ans:
        ListMACAddr = rcv.sprintf("%Ether.src%---%ARP.psrc%")
        print(ListMACAddr)