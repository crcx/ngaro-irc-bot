# ngaro-irc
# This is basically an attempt to provide access to Ngaro over
# an IRC bridge.
#
# Usage:
# - configure the settings below
# - ensure that retro.py is executable
# - run this file
#
# Upon connection, to evaluate code:
#
# retrobot: <source>
#
# To quit the bot:
#
# retrobot: quit-now

import os
import socket

server = 'irc.freenode.net'
port = 6667
channel = '#retro'
botname = 'retrobot'
botdesc = 'retro via irc'

def sendMessage(socket, message):
     socket.send(message + '\r\n')

def joinChannel(socket, channel):
     socket.send('JOIN ' + channel + '\r\n')

def setNick(socket, nickname, descr):
     socket.send('NICK ' + nickname + '\r\n')
     sendMessage(socket, 'USER retrobot retrobot retrobot :' + descr)

def connectToNetwork(srv, prt):
     sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sck.connect((srv, prt))
     return sck

def sendToChannel(socket, channel, message):
     sendMessage(socket, 'PRIVMSG ' + channel + ' :' + message)


socket = connectToNetwork(server, port)
setNick(socket, botname, botdesc)
joinChannel(socket, channel)

data = ''
while True:
     data = socket.recv(4096)
     if data.find('PING') != -1:
        socket.send('PONG ' + data.split() [1] + '\r\n')
        print data
     if data.find('quit-now') != -1:
          sendMessage(socket, 'QUIT :bye!')
          os._exit(0)
     if data.find(botname + ':') != -1:
         fd = open('eval', 'w')
         fd.write(data[data.find(':' + botname + ':')+(len(botname) + 2):] + '\r\nbye')
         fd.close()
         xx=os.popen("retro.py","r")
         sendToChannel(socket, channel, 'Results:')
         for line in xx:
             sendToChannel(socket, channel, line)
             print line
