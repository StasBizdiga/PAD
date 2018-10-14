import re
#serverside / clientside
cmd_send = "/send"
cmd_pub = "/pub"
cmd_sub = "/sub"
cmd_subs = "/subs"
cmd_unsub = "/unsub"
cmd_help = "/help"
cmd_showallports = "/showall"
cmd_myport = "/me"
cmd_exit = "/exit"

def show(option):
    if option == cmd_help:
        return wrap(help_description)
    elif option == cmd_showallports:
        return wrap([c.getpeername()[1] for c in get_clients()])
    

def send_msg(word):
    #### do more
    return word.encode()

def wrap(data):
    return str(data).encode()

def add_client(client):
    if client not in client_list:
        client_list.append(client)

def remove_client(client):
    if client in client_list: 
        client_list.remove(client)

def get_clients():
    return client_list
    
def get_command(cmd):
    return cmd.split(' ')[0]          # example: "/command" hey hello

def get_adv_command(cmd):
    return cmd.split(' ')[0].split(':') # ex: "/command:p1:p2:p3" text me
    
def validate_command(cmd):
    return bool((re.match('^[:/ a-zA-Z0-9]+$',cmd)) and cmd[0] == "/")

def show_subs(port):
    try:
        subscribed_to = []
        for x in pubs_subs.keys():
            if port in pubs_subs[x]:
                subscribed_to.append(x)
        if subscribed_to == []: raise Exception
        else: return wrap(str(subscribed_to))
        
    except Exception as e:
        print(e)
        return wrap("No subscriptions!")
    
def subscribe(dest,port):
    if dest not in pubs_subs.keys():
        pubs_subs[dest] = []
    pubs_subs[dest].append(port)
    
    return wrap("\nOk! Subbed to:"+str(dest))

def unsubscribe(dest,port):
    try:
        if port in pubs_subs[dest]:
            pubs_subs[dest].remove(port)
            
            return wrap("\nUnsubbed from:"+str(dest))
            
    except:
        return wrap(" Error. No such uid:"+str(dest))
    
client_list = []
pubs_subs = {}
#subs_pubs = {} # for getting the list of who the user is subbed to
help_description = \
"""
===============
=== h e l p ===
===============
/help - displays this list of available commands

/me - returns your user id
/showall - show the user list currently online
/send <text> - broadcasts the text that was sent as param
/send:<uid>  - unicast send message to user
/send:<uid>:<uid>:<uid>... - multicast send

/exit - closes connection
===============
"""


#==============================================================================
#==============================================================================
#TESTING GROUNDS
#
#add_client('1111')
#add_client('1234')
#add_client('1235')
#add_client('1236')
#subscribe('1111','1234')
#subscribe('1111','1235')
#subscribe('1112','1236')
#print(pubs_subs)
#
#for cl in client_list:                    
#    if cl in pubs_subs['1112']:
#        print(cl,":received")