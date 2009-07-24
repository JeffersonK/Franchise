from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


#class ServerManagementProtocol(LineReceiver):
#    #delimiter = "/r/n"  # you can change this to be anything    
#    def lineReceived(self, line):
#        line = line.strip()
#        parts = line.split(" ", 1)
#        self.handleCommand(parts[0], parts[1:])
#
#    def handleCommand(self, command, argument):
#        if command.lower() == "hello":
#            self.factory.serverSideFactory.client_sendHello()
#            self.sendLine("ok")
#        elif command.lower() == "echo":
#            self.factory.serverSideFactory.client_echo("".join(argument))
#            self.sendLine("ok")
#        else:
#            self.sendLine("error")

#class ServerManagementFactory(Factory):
#    protocol = ServerManagementProtocol
#
#    def __init__(self, serverSideFactory):
#        self.serverSideFactory = serverSideFactory

####################################
#
#
#
####################################
import json
import cPickle
import pprint
import os
class DeviceServerSideProtocol(LineReceiver):
    
    #delimiter = "/r/n"  # you can change this to be anything

    #def sendHello(self):
    #    self.sendLine("Server says: Hello")
    
    #def echo(self, stuff):
    #    self.sendLine("Server says: %s" % stuff)
	
    def connectionLost(self, reason):
        # remove myself from the list of connected clients
        self.factory.active_clients.remove(self)
    
    def lineReceived(self, line):
	readplayer = "READPLAYER("

	if line.startswith(readplayer) and line.endswith(')'):
            playerGUID = int(line[len(readplayer):-1])
            if os.path.exists("players/%d.plr" % playerGUID):
                file = open("players/%d.plr" % playerGUID, "r")

#plyr = file.read()
                plyr = cPickle.load(file)
                file.close()
            #print plyr	
            #plyrdict = eval(plyr)
                plyr = eval(str(plyr))
                jsonobj = json.dumps(str(plyr))
                self.sendLine(jsonobj)
            #self.sendLine(str(plyr))
            #self.sendLine("You said: %s" % line)


class DeviceServerSideFactory(Factory):
    protocol = DeviceServerSideProtocol
    
    def __init__(self):
        self.active_clients = []

    def buildProtocol(self, addr):
        '''Override this to store active clients'''
        # you might want to store the addr object for record keeping
        p = Factory.buildProtocol(self, addr)
        self.active_clients.append(p)
        return p
    
    #def client_sendHello(self):
    #    for proto in self.active_clients:
    #        proto.sendHello()
    
    def client_echo(self, stuff):
        for proto in self.active_clients:
            proto.echo(stuff)


# Next lines are magic:
serverSideFactory = DeviceServerSideFactory()
#serverManagementFactory = ServerManagementFactory(serverSideFactory)

# 8007 is the port you want to run under. Choose something >1024
reactor.listenTCP(7000, serverSideFactory)
#reactor.listenTCP(7001, serverManagementFactory)
reactor.run()
