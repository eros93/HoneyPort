# HoneyPort

Dependencies: 
  iptables
  ipset

Make sure to add these rules to iptables:

iptables -A OUTPUT -p tcp -m tcp --tcp-flags RST RST -j DROP
iptables -A OUTPUT -p icmp -m icmp --icmp-type 3 -j DROP
iptables -t nat -A PREROUTING -p tcp -m set --match-set set_name dst -j REDIRECT --to-ports 8888
iptables -t nat -I OUTPUT -p tcp -o lo -m set --match-set exported_ports dst -j REDIRECT --to-ports 8888

Then run the script for setting up the ipset:

# op_generate.py
will generate ipset within 1-65535 ports range and will exclude currently opened ports.

# op_monitor.py
script that monitor netstat output for newly opened/closed ports, then add it or remove from ipset.

# proxy.py
Proxy that forward al the traffic coming from port 8888 to different honeypot according to the classification of the protocol

Then run the honeypots:

### set-up Responder ###

socat TCP-LISTEN:2223,reuseaddr,fork -

sudo docker run -p 2222:2222 cowrie/cowrie

httrack https://smartdata.polito.it/ -O .

python3.6 -m http.server 2224 

sudo python3.6 proxy21.py
