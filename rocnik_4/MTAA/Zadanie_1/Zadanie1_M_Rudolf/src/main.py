import sipfullproxy as sip
import SocketServer
import socket
import sys
import time
import logging




if __name__ == "__main__":    
    ipaddress = sys.argv[1]
    sip.recordroute = "Record-Route: <sip:%s:%d;lr>" % (ipaddress,sip.PORT)
    sip.topvia = "Via: SIP/2.0/UDP %s:%d" % (ipaddress,sip.PORT)
    server = SocketServer.UDPServer((sip.HOST, sip.PORT), sip.UDPHandler)
    server.serve_forever()