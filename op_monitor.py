from subprocess import check_output
import re
from time import sleep
import os
from datetime import datetime
set_name = 'exported_ports'

def open_ports():
   netstat = check_output('netstat -tan',shell=True)
   lports = re.findall(r'(?<=\:)[0-9]{1,5}\w(?=.+listen)',netstat.lower())
   lports = list(set(lports))
   return lports

def file_write(string):
   f = open("output_monitor.txt","a+")
   f.write(string + '\n')
   f.close()

tmp_ports = []

while 1:
   openports = open_ports()
   new_open = list(set(openports) - set(tmp_ports))
   new_closed = list(set(tmp_ports) - set(openports))
   if len(new_open):
     for port in new_open:
       time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       output1 = '[-] Removing port %s from ipset at %s' % (port, time)
       file_write(output1)
       print output1
       os.system('ipset del %s %s' % (set_name,port))
   if len(new_closed):
     for port in new_closed:
       time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       output2 = '[+] Adding port %s to ipset at %s' % (port, time)
       file_write(output2)
       print output2
       os.system('ipset add %s %s' % (set_name,port))
   tmp_ports = openports
   sleep(1)
