import os
import socket

irc = 'irc.freenode.net'
port = 6667
channel = '#retro'
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect((irc, port))
sck.send('NICK retrobot\r\n')
sck.send('USER retrobot retrobot retrobot :retro via irc\r\n')
sck.send('JOIN #retro' + '\r\n')
data = ''
while True:
     data = sck.recv(4096)
     if data.find('PING') != -1:
        sck.send('PONG ' + data.split() [1] + '\r\n')
        print data
     if data.find('retrobot:') != -1:
         fd = open('eval', 'w')
         fd.write(data[data.find(':retrobot:')+10:] + '\r\nbye')
         fd.close()
         xx=os.popen("retro.py","r")
         sck.send('PRIVMSG #retro :Results:\r\n')
         for line in xx:
             sck.send('PRIVMSG #retro :' + line + '\r\n')
