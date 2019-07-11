import socket
import sys
import time
import signal
import resource
# import thread
import _thread as thread

# global SSH 
def printBanner():
	banner = """ 

     /|
    / |                 .' '.            __           Made by 
   /__|______  .        .   .           (__\_             Eros Filippi - s243888@polito
  |  __  __  |  .         .         . -{{_(|8)
  | |  ||  | |    ' .  . ' ' .  . '     (__/ 
  | |__||__| |   
  |  __  __()|  
  | |  ||  | |        __        ___      __   __   __   __            __   __   __          
  | |  ||  | |  |__| /  \ |\ | |__  \ / |  \ /  \ /  \ |__)    __    |__) |__) /  \ \_/ \ /
  | |__||__| |  |  | \__/ | \| |___  |  |__/ \__/ \__/ |  \          |    |  \ \__/ / \  | 
  |__________|
	

  """
	print(banner)
	

class Connection:
	"""docstring for Connection"""
	def __init__(self):
		self.socket_general={}
		self.buffer_general={}
		self.socket_SSH={}
		self.buffer_SSH = {}
		self.socket_HTTP={}
		self.buffer_HTTP = {}
		self.proto_flag = {}
		self.proto_flag["SSH"] = {}
		self.proto_flag["HTTP"] = {}
		self.sockets = []

	def new_connection(self, socket):
		#TODO dict of dicto for protocol type

		# self.proto_flag[]
		self.socket_general[socket] = False
		self.buffer_general[socket] = []
		self.socket_SSH[socket] = False
		self.buffer_SSH[socket] = []
		self.socket_HTTP[socket] = False
		self.buffer_HTTP[socket] = []
		self.sockets.append(socket)

class Proxy:
	"""docstring for ClassName"""
	def __init__(self):
		# self.SSH = False
		self.parts={}
		self.parts[0] = "localhost"
		self.parts[1] = 2223 #server general
		self.parts[2] = 8888 #client
		self.parts[3] = 2222 #server2 SSH
		self.parts[4] = 2224 #server3 HTTP

	def main(self):
		thread.start_new_thread(self.server, (self.parts[0], int(self.parts[1]), int(self.parts[2]), int(self.parts[3]), int(self.parts[4])))

		# print("Starting Proxy .....")
		lock = thread.allocate_lock()
		print(lock)
		lock.acquire()
		lock.acquire()


	def server(self,*settings):
		
		try:
			dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			dock_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			dock_socket.bind(('', settings[2])) #client port
			dock_socket.listen(5)
			connect = Connection()

			while True:
				client_socket = dock_socket.accept()[0]
				connect.new_connection(client_socket)
				thread.start_new_thread(self.forward_inside, (client_socket, connect))
				
		except Exception as e:
			print(e)
			print("exception 1")
			# time.sleep(3)
			for sock in connect.sockets:
				try:
					sock.shutdown(socket.SHUT_RDWR) 
					sock.close()
				except Exception as e:
					# raise e
					print("socket %s error to close ", sock)
		finally:
			
			print("Restart the process....")
			thread.start_new_thread(self.server, settings)

	def forward_inside(self, source, connect):
		print(source)
		HTTP_patterns = ['GET', 'HTTP']
		string = ' '
		try:
			while string:
				string = source.recv(1024)
				if "b''" in str(string):
					# print("stoooooooooooooooooooooooooooooooooooooooop")
					try:
						# source.shutdown(socket.SHUT_RDWR) 
						source.close()
					except:
						print("no source socket to close")
						pass
				# print(string)
				connect.buffer_SSH[source].append(string)
				connect.buffer_general[source].append(string)
				connect.buffer_HTTP[source].append(string)

				# SSH test and connection

				if "SSH" in str(string):
					print("SSH conection started")
					SSH_socket = socket.socket()
					SSH_socket.connect((self.parts[0], self.parts[3]))
					connect.new_connection(SSH_socket)
					connect.socket_SSH[source] = True
					thread.start_new_thread(self.forward_outside, (SSH_socket, source, connect))
					for message in connect.buffer_SSH[source]:
						SSH_socket.sendall(message)
				elif connect.socket_SSH[source] == True:
					print(string)
					SSH_socket.sendall(string) 

				# HTTP test and connection

				elif any(x in str(string) for x in HTTP_patterns):
					print("HTTP connection started")
					HTTP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					HTTP_socket.connect((self.parts[0], self.parts[4]))
					connect.new_connection(HTTP_socket)
					connect.socket_HTTP[source] = True
					thread.start_new_thread(self.forward_outside, (HTTP_socket, source, connect))
					for message in connect.buffer_HTTP[source]:
						HTTP_socket.sendall(message)
				elif connect.socket_HTTP[source] == True:
					HTTP_socket.sendall(string) 

				# general connection
				elif connect.socket_general[source] == True:
					print("general connection started")
					general_socket.sendall(string) 
		
				else:	
					print("general connection started")
					general_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					general_socket.connect((self.parts[0], self.parts[1]))
					connect.new_connection(general_socket)
					connect.socket_general[source] = True
					thread.start_new_thread(self.forward_outside, (general_socket, source, connect))
					for message in connect.buffer_general[source]:
						general_socket.sendall(message)

		except:
			# print("closing the connection .... ")
			# print("exception 2")
			try:
				sys.exit(0)
				print("exception3")
			except:
				pass
			

	def forward_outside(self, source, destination, connect):
		string = ' '
		try:
			while string:
				string = source.recv(1024)
				# print(string)
				connect.buffer_SSH[source].append(string)
				try:
					destination.sendall(string)
				except:
					pass
				if "b''" in str(string):
					# print("stoooooooooooooooooooooooooooooooooooooooop")
					try:
						source.close()
					except:
						print("no source socket to close")
						pass
					try:
						destination.close()
					except:
						print("no destination socket to close")
						pass

				
		except:
			print("closing the connection ....")
			print("exception 4")
			source.shutdown(socket.SHUT_RDWR) 
			source.close()
			destination.shutdown(socket.SHUT_RDWR) 
			destination.close()
			thread.exit()


if __name__ == '__main__':
	# print("Starting proxy .... ")
	# soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
	# resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
	# print(hard)
	printBanner()
	p = Proxy()
	p.main()
