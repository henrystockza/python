#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import threading
import socket
import time
import sys
from optparse import OptionParser

class PortQuery(object):
    __doc__ = ''''Query ports and respond with if open of closed '''

    def __init__(self):
        self.feedbacklist = []


    def controller(self, destination, port, TCP, UDP):
        givenname= destination
        ip = self.get_ipaddress(destination)
        hostname = self.get_hostname(ip)
        if TCP == True:
            self.tcp_scan(ip, hostname, port, givenname)
        else: pass
        if UDP == True:
            self.udp_scan(ip, hostname, port, givenname)
        else: pass

    def get_hostname(self, ip):
        try:
            dns = socket.gethostbyaddr(ip)
            hostname = dns[0]
        except:
            hostname = 'null'
        return hostname

    def get_ipaddress(self, ip):
        try:
            ip = socket.gethostbyname(ip)
        except:
            ip = 'null'
        return ip

    def tcp_scan(self, ip, hostname, port, givenname):
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcpbind = sock.connect_ex((ip, int(port)))
        except:
            tcpbind = 'null'
            conn_success = 'CLOSED'
        if tcpbind == 0:
            conn_success = 'OPEN'
        else:
            conn_success = 'CLOSED'
        self.feedbacklist.append([givenname, ip, hostname, port, 'TCP', conn_success])

    def udp_scan(self, ip, hostname, port, givenname):
        udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udpbind = udpsock.bind((ip, int(port)))
            conn_success = 'OPEN'
        except socket.error:
            conn_success = 'CLOSED'
        self.feedbacklist.append([givenname, ip, hostname, port, 'UDP', conn_success])

class Export(object):
    __doc__ = '''Handles the export of the given inforamtion into diferent file formats'''

    def print_screen(self, payload):
        header = 'GivenName, IP, DNSName, Port, PortType, Status'
        for line in payload:
            amendedline = line[0] + ',' + line[1] + ',' + line[2] + ',' + line[3] + ',' + line[4] + ',' + line[5]
            print(amendedline)

    def export_csv(self, filename, payload):
        filename = filename + '.csv'
        header = 'GivenName, IP, DNSName, Port, PortType, Status\n'
        self.cf = open(filename, 'w')
        self.cf.write(header)
        for line in payload:
            amendedline = line[0] + ',' + line[1] + ',' + line[2] + ',' + line[3] + ',' + line[4] + ',' + line[5] + '\n'
            self.cf.write(amendedline)
        self.cf.close()

    def xml_control(self, filename, payload):
        filename = filename + '.xml'
        self.xf = open(filename, 'w')
        self.xf.write('<payload>')
        self.xml_data_write(payload)
        self.xf.write('</payload>')
        self.xf.close()

    def xml_data_write(self, payload):
        for line in payload:
            self.xf.write('\t<query\n>')
            self.xf.write('\t\t<IP>' + str(payload[0][0]) +'</IP>\n')
            self.xf.write('\t\t<DNSName>' + str(payload[0][1]) +'</DNSName>\n')
            self.xf.write('\t\t<Port>' + str(payload[0][2]) +'</Port>\n')
            self.xf.write('\t\t<PortType>' + str(payload[0][3]) +'</PortType>\n')
            self.xf.write('\t\t<Status>' + str(payload[0][4]) +'</Status>\n')
            self.xf.write('\t</query\n>')

    def json_control(self, filename, payload):
        filename = filename + '.json'
        self.jf = open(filename, 'w')
        self.jf.write('{\n')
        self.jf.write('\t"payload": {\n')
        self.jf.write('\t\t"query": [\n')
        self.json_data_write(payload)
        self.jf.write('\t\t]\n')
        self.jf.write('\t}\n')
        self.jf.write('}\n')
        self.jf.close()

    def json_data_write(self, payload):
        counter = 0
        for line in payload:
            self.jf.write('\t\t\t{\n')
            self.jf.write('\t\t\t"IP":"' + str(payload[0][0]) +'",\n')
            self.jf.write('\t\t\t"DNSName":"' + str(payload[0][1]) +'",\n')
            self.jf.write('\t\t\t"Port":"' + str(payload[0][2]) +'",\n')
            self.jf.write('\t\t\t"PortType":"' + str(payload[0][3]) +'",\n')
            self.jf.write('\t\t\t"Status":"' + str(payload[0][4]) +'"\n')
            counter = counter + 1
            if counter != len(payload):
                self.jf.write('\t\t\t},\n')
            else:
                self.jf.write('\t\t\t}\n')


class Controller(object):
    __doc__ = ''''Controller class for clean main() use and class import with multi-thread enablement  '''

    def __init__(self):
        self.PQ = PortQuery()
        self.exp = Export()

    def main(self):
        parser = OptionParser()
        parser.set_description('Query list o given ports to determine if they are available')
        parser.set_usage('''
                portquery -d www.google.com -p 80 
                portquery -d 127.0.0.1,www.google.com -p 80,445 -u --screen
                portquery -d 127.0.0.1,www.google.com -p 8080,445 -u -t --screen --csv --xml --json
                portquery --destination 127.0.0.1,www.google.com --port 8080,445 --udp --tcp --screen --csv --xml --json
                ''')

        parser.add_option("-d", "--destination", dest='destination', help="[REQUIRED] Destination'[s] to query")
        parser.add_option("-p", "--port", dest='port', default=300,
                          help="Port'[s] to query")
        parser.add_option("-t", "--tcp", action="store_true", dest="TCP", help="Flag to scan only TCP")
        parser.add_option("-u", "--u", action="store_true", dest="UDP", help="Flag to scan only UDP")
        parser.add_option("-f", "--filename", dest="filename", help="Full file path and name, excluding extension")
        parser.add_option("--screen", action="store_true", dest="screen", help="Print information to screen")
        parser.add_option("--csv", action="store_true", dest="csv", help="Export information to csv")
        parser.add_option("--xml", action="store_true", dest="xml", help="Export information to xml")
        parser.add_option("--json", action="store_true", dest="json", help="Export information to json")
        (options, args) = parser.parse_args()

        #Check nulls
        if options.destination == None or options.destination == '':
            parser.error('parameter -d is required')
        else:
            if options.destination.find(',') > 1:
                destinations = options.destination.split(',')
            else:
                destinations = [options.destination]
        if options.port == None or options.port == '':
            parser.error('parameter -p is required')
        else:
            if options.port.find(',') > 1:
                ports = options.port.split(',')
            else:
                ports = [options.port]
        if (options.TCP == None or options.TCP == '') and (options.UDP == None or options.UDP == ''):
            TCP = True
            UDP = True
        else:
            TCP = options.TCP
            UDP = options.UDP
        if (options.screen is None or options.screen == '') and options.xml != True \
                and options.json != True and options.csv != True:
            screen = True
        else:
            screen = options.screen
        if options.csv is None or options.csv == '':
            csv = False
        else:
            csv = options.csv
        if options.json is None or options.json == '':
            json = False
        else:
            json = options.json
        if options.xml is None or options.xml == '':
            xml = False
        else:
            xml = options.xml
        if options.filename is None or options.filename == '':
            fdate = time.strftime("%Y-%m-%d")
            ftime = time.strftime(" %H.%M.%S ")
            if 'win' or 'windows' in sys.platform:
                filename = "c:\\temp\\" + fdate + ftime + 'PortQuery'
            elif 'lin' or 'linux' in sys.platform:
                filename = "/tmp" + fdate + ftime + 'PortQuery'
            else:
                filename = "/" + fdate + ftime + 'PortQuery'
        else:
            filename = options.filename

        self.controller(destinations, ports, TCP, UDP, filename, screen, csv, xml, json)

    def controller(self, destinations, ports, TCP, UDP, filename, screen, csv, xml, json):
        #Loop for each destination, subloop each port, subsub TCP, UDP
        for destination in destinations:
            for port in ports:
                threading.Thread(target=self.PQ.controller, args=(destination, port, TCP, UDP)).start()

        #Wait for all threds to finish befor sorting list for prining out
        while threading.activeCount() >= 2:
            time.sleep(0.1)
        else:
            self.PQ.feedbacklist.sort()

        if screen == True:
            self.exp.print_screen(self.PQ.feedbacklist)
        else: pass
        if csv == True:
            self.exp.export_csv(filename, self.PQ.feedbacklist)
        else: pass
        if json == True:
            self.exp.json_control(filename, self.PQ.feedbacklist)
        else: pass
        if xml == True:
            self.exp.xml_control(filename, self.PQ.feedbacklist)
        else: pass


if __name__ == '__main__':
    cnt = Controller()
    cnt.main()
