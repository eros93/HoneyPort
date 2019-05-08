#dockerfile thesis
#in Dockerfile fold

#docker build --tag=honeyport .

#docker run -d --net=host --cap-add=NET_ADMIN --cap-add=NET_RAW --name=honeyport -i -t honeyport 

FROM ubuntu:16.04
LABEL maintainer="Eros Filippi <s243888@studenti.polito.it>"
########################################################### ENVIRONMENT: base ################################################
USER root

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv python-pip python2.7 python2.7-dev python-virtualenv libssl-dev libffi-dev build-essential libpython3-dev python3-minimal authbind
RUN python3.6 -m pip install pip --upgrade
RUN apt-get autoremove
RUN apt-get clean
#snap install docker


########################################################### Application needed: ################################################
# ------- Install additionnal libraries with "apt-get -y"
RUN apt-get install -y libsm6 libxext6 libglib2.0-0 libxrender-dev iptables git net-tools ipset nano socat nmap

# ------- Or annd needed libraries into "requirements.txt" file and use it:
#RUN python3.6 -m pip install -r requirements.txt

########################################################### Import files: ################################################
WORKDIR /usr/home/honeyport
#RUN mkdir -p /usr/home/honeyport 
COPY op_generate.py op_monitor.py ./
RUN git clone http://github.com/cowrie/cowrie

########################################################### inside Docker : ################################################

#docker network create --subnet=172.18.0.0/16 mynet123
#docker run -d --net mynet123 --ip 172.18.0.22 --cap-add=NET_ADMIN --name=honeyport -i -t honeyport

#docker network create -d macvlan --subnet 192.168.1.0/24 --gateway 192.168.1.254 -o parent=eth0 mvnet
#docker run -d --net mvnet --ip 192.168.1.123 --cap-add=NET_ADMIN --name=honeyport -i -t honeyport
#docker exec -i -t honeyport /bin/bash


#sudo ipset create exported_ports bitmap:port range 0-65535
#iptables -A OUTPUT -p tcp -m tcp --tcp-flags RST RST -j DROP
#iptables -A OUTPUT -p icmp -m icmp --icmp-type 3 -j DROP
#iptables -t nat -A PREROUTING -p tcp -m set --match-set exported_ports dst -j REDIRECT --to-ports 8888
#socat TCP-LISTEN:8888,reuseaddr,fork -

##########################################################  COWRIE inside #########################################################

#adduser --disabled-password cowrie
#su - cowrie 
#git clone http://github.com/cowrie/cowrie
#cd cowrie
#virtualenv --python=python3 cowrie-env
#source cowrie-env/bin/activate
#(cowrie-env) $ pip install --upgrade pip
<<<<<<< HEAD
#(cowrie-env) $ pip install --upgrade -r requirements.txt
=======
#(#cowrie-env) $ pip install --upgrade -r requirements.txt
>>>>>>> d7044820803d47694946bd1adeee5f7a55a0d1d8

################################## make socat in background ##################
# socat TCP-LISTEN:8888,reuseaddr,fork - &
# jobs
# ps faux
# kill $PID

