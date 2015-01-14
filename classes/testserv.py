import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 34567                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

print host

s.listen(5)
print 'waiting at ',port             # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    data = c.recv(20)
    print data
    c.close()
