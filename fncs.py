import re
#serverside / clientside
cmd_send = "/send"
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


client_list = []

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
