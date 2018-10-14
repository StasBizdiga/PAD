import fncs
import socket
import threading


def new_client(client,address):
    while True:
#        my_ip = str(address[0])
        my_port = str(address[1])
        data = client.recv(1024).decode()
        print(">>> Received data %s from %s" % (data,address))

        if (fncs.validate_command(data)):

            if (data == " "):
                client.send(fncs.wrap("Write a command! Do you need '/help'?"))
    
            elif (data == fncs.cmd_help):
                client.send(fncs.show(fncs.cmd_help))       
            
            elif (fncs.get_command(data) == fncs.cmd_showallports):
                clientlist = fncs.show(fncs.cmd_showallports) #get raddr ports
                client.send(clientlist) #show them
            
# BROADCAST
            elif (fncs.get_command(data) == fncs.cmd_send): #sending_msg()
            
                try:
                    #full msg with sender info:
                    msg = data.replace(fncs.get_command(data), my_port + ':')          
                    for every_client in fncs.client_list:
                        every_client.send(fncs.send_msg(msg))  
                        
                except Exception as e:
                    client.send(fncs.wrap(e))
                    client.send(fncs.wrap("Err: Check parameters. (ex: /send text)"))
            
# UNI/MULTI-CAST
            elif (fncs.get_adv_command(data)[0] == fncs.cmd_send): #send:<port> 
                destlist = fncs.get_adv_command(data) #LIST with dest ports
                destlist.pop(0) #remove [0] i.e. root command: '/send', which is not a port/dest
                try:
                    #full msg with sender info:
                    msg = data.replace(fncs.get_command(data), my_port + ':')  
                    
                    for cl in fncs.client_list:
                        for dest in destlist:
                            if str(cl.getpeername()[1])==str(dest):
                                cl.send(fncs.send_msg(msg))
                except Exception as e:
                    client.send(fncs.wrap(e))
                    client.send(fncs.wrap("Err: Check parameters. (ex: /send:<uid> text)"))
                                
# PUBLISHER-SUBSCRIBER MULTI-CAST
            elif (fncs.get_command(data) == fncs.cmd_pub): #/pub text
                try:
                    #full msg with sender info:
                    msg = data.replace(fncs.get_command(data), my_port + '[pub]:')  
                    
                    print(fncs.pubs_subs)  
                    for cl in fncs.client_list:                    
                        if str(cl.getpeername()[1]) in fncs.pubs_subs[my_port]:
                            cl.send(fncs.send_msg(msg))
                                
                except Exception as e:
                    client.send(fncs.wrap(e))
# SUBSCRIBE                
            elif (fncs.get_adv_command(data)[0] == fncs.cmd_sub):#/sub:1234:4444:..
                try:                             
                    if(":" not in data): raise Exception
                    destlist = fncs.get_adv_command(data) #LIST with ports to sub to
                    destlist.pop(0) #remove [0] i.e. root command, which is not a port/dest
                    for x in destlist:
                        client.send(fncs.subscribe(x,my_port))
                        
                except Exception as e:
                    client.send(fncs.wrap(e))
                    client.send(fncs.wrap("Err: Check parameters. (ex: /sub:<uid>:<uid>..)"))
# UNSUBSCRIBE                    
            elif (fncs.get_adv_command(data)[0] == fncs.cmd_unsub):#/unsub:1234:4444:..
                try:
                    if(":" not in data): raise Exception
                    destlist = fncs.get_adv_command(data) #LIST with ports to sub to
                    destlist.pop(0) #remove [0] i.e. root command, which is not a port/dest
                    for x in destlist:
                        client.send(fncs.unsubscribe(x,my_port))
                
                except Exception as e:
                    client.send(fncs.wrap(e))
                    client.send(fncs.wrap("Err: Check parameters. (ex: /unsub:<uid>:<uid>..)"))
                    
            elif (data == fncs.cmd_subs):
                client.send(fncs.show_subs(my_port))
                
            elif (data == fncs.cmd_myport): 
                client.send(fncs.wrap(my_port))
                
            elif (data == fncs.cmd_exit): 
                client.send("Closing connection...\n".encode())
                break
            
            else:
                client.send("Unknown command. Type '/help'!".encode())
        else:
            client.send("Unknown command. Type '/help'!".encode())

    
    fncs.remove_client(client)    
    client.close()

def start_server(address, port, max_connections=5):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(max_connections)
    print("=== Listening for connections at %s:%s" % (address, port))
    while True:
        try:
            client, address = server_socket.accept()
            fncs.add_client(client)    
            client.settimeout(450) # autoclosing connections with inactivity 
            print("=== New connection from %s" % (address,))
            threading.Thread(target = new_client,args = (client,address)).start()

        except:
            break
        
    server_socket.close()
    
            
if __name__ == '__main__':
    start_server('127.0.0.1', 8000)
