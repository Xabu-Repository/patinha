import socket

tcp_ip = '10.3.141.1'
tcp_port = 5005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((tcp_ip, tcp_port))
	sock.listen()
	print('Listening...')
	conn, addr = sock.accept()
	with conn:
		print('Connected to ', addr)
		while True:
			data = conn.recv(1024).decode()
			print(data)
			if not data: break
            
