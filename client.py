import threading
import socket

KEEP_CONN = True

def send_to_server(socket):
    while KEEP_CONN:
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
    while KEEP_CONN:
        try:
           #receive
            data = socket.recv(1024)
            print("<<< %s" % (data.decode(),))
            if ("Closing connection".encode() in data):
                close_connection()
                break
            
        except:
            break   
    return False
    
def close_connection():
    global KEEP_CONN
    KEEP_CONN = False
    a.close()
    b.close()
    client_socket.close()

    
def start_client(address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, port))
    print("=== Connected to %s:%s" % (address, port))
        
    a = threading.Thread(target = send_to_server ,args = (client_socket,))
    b = threading.Thread(target = receive_from_server,args = (client_socket,))
    a.start()
    b.start()
    while KEEP_CONN:
        pass
   


if __name__ == '__main__':
    start_client('127.0.0.1', 8000)     