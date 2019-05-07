
import os
import re
from subprocess import check_output

set_name = 'exported_ports'

def open_ports():
   netstat = check_output('netstat -tan',shell=True)
   lports = re.findall(r'(?<=\:)[0-9]{1,5}\w(?=.+listen)',netstat.lower())
   lports = list(set(lports))
   return lports

# os.system('ipset list %s' % set_name)
os.system('ipset flush  %s' % set_name)
os.system('ipset destroy %s' % set_name)
os.system('ipset create %s bitmap:port range 0-65535' % set_name)
os.system('ipset add %s 0-65535' % set_name)

openports = open_ports()
for port in openports:
   print '[+] Removing port %s to ipset' % port
   os.system('ipset del %s %s' % (set_name,port))



#os.system('iptables -F') os.system('iptables -t nat -F') 
#os.system('iptables-restore < /etc/iptables.rules')

#iptables -A OUTPUT -p tcp -m tcp --tcp-flags RST RST -j DROP 
#iptables -t nat -A PREROUTING -p tcp -m set --match-set rports dst -j REDIRECT --to-ports 81


