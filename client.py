import threading
import socket


def send_to_server(socket):
    while True:
        try:
            #send
            data = input(">>> ")
            if data == '':
                data = " "
            socket.send(data.encode())            
        except:
            break  
    return False
    
def receive_from_server(socket):
    while True:
        try:
           #receive
            data = socket.recv(1024)
            print("<<< %s" % (data.decode(),))
            if ("Closing connection".encode() in data):
                break
            
        except:
            break   
    return False
        
def start_client(address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    print("=== Connected to %s:%s" % (address, port))
        
    a = threading.Thread(target = send_to_server ,args = (client_socket,))
    b = threading.Thread(target = receive_from_server,args = (client_socket,))
    a.start()
    b.start()
    while(a and b):
        pass
    a.close()
    b.close()
    client_socket.close()


if __name__ == '__main__':
    start_client('127.0.0.1', 8000)     