#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import subprocess
import re
import time
from optparse import OptionParser
import threading


class Trace(object):
    __doc__ = '''This class handles the loggic for the "routing" and "tracing" but does not do the actual trace '''

    def __init__(self):
        self.prefix = None
        self.os = None
        self.windows = Trace_Windows()
        self.linux = Trace_Linux()
        self.html = build_HTML()

    def controller(self, ip=None, max_responce=None, html_location=None, html_name=None):
        '''self.controller() : Handles the logic behind this class method
        :param ip: ip / hostname of the device to trace
        :param max_responce: Max response time before marking as having an error
        :param html_location: HTML location to save the file
        :param html_name: HTML name to give the file
        :return: NONE
        '''

        '''LOGIC
        1)Find the current running OS version [self.os]
        2)Set the prefix for that running os Traceroute / Tracert [self.prefix]
        3)Test if the command is installed [self.test_prefix)
        4)Run the Trace [self.run_command], clean output into conformed list [self.clean_output][self.returned_output] 
        5)Test the given output against the max_response [self.return_alert], return list[problem_areas]
        6)Generate the html payload from list[problem_areas] and write to file
        '''

        self.get_os()
        self.get_prefix()
        trace_exists = self.test_prefix()
        if trace_exists == True:
            raw_output = self.run_command(ip=ip, prefix=self.prefix)
            clean_output = self.clean_output(raw_output)
            returned_data = self.return_output(clean_output)
            problem_areas = self.return_alert(returned_data, max_responce)
            html_payload = self.html.controller(ip, problem_areas)
            self.export_html(html_location, html_name, ip, html_payload)
            html_payload = None
            exit()
        else:
            exit()

    def export_html(self, html_location, html_name, ip, html_payload):
        if html_name is None:
            htmlNameDate = (time.strftime("%Y-%m-%d"))
            htmlNameTime = (time.strftime(" %H.%M.%S "))
            html_name = htmlNameDate + htmlNameTime + ip + '.html'
        else:
            #Name entered
            pass

        if html_location is None and self.os == 'windows':
            html_location = 'c:\\temp\\'
        elif html_location is None and self.os == 'linux':
            html_location = '/tmp'

        print('FILE SAVED: ' + html_location + html_name)
        f = open(html_location + html_name, 'w')
        f.write(html_payload)
        f.close


    def get_os(self):
        if 'win' in sys.platform or 'windows' in sys.platform:
            self.os = 'windows'
        elif 'linux' in sys.platform:
            self.os = 'linux'

    def get_prefix(self):
        if self.os == 'windows':
            self.prefix = 'tracert'
        elif self.os == 'linux':
            self.prefix = 'traceroute'

    def test_prefix(self):
        output = self.run_command('127.0.0.1', self.prefix)
        cleaned_output = self.clean_output(output)
        string_output = ''.join(cleaned_output)
        if ('Tracing' in string_output and 'route' in string_output) or \
                ('traceroute' in string_output and 'to' in string_output):
            return True
        else:
            return False

    def run_command(self, ip=None, prefix =None):
        if self.os == 'windows':
            raw_output = self.windows.run_command(ip, prefix)
        elif self.os == 'linux':
            raw_output = self.linux.run_command(ip, prefix)
        return raw_output

    def clean_output(self, output):
        if self.os == 'windows':
            data = self.windows.clean_output(output)
        elif self.os == 'linux':
            pass
            data = self.linux.clean_output(output)
        return data

    def return_output(self, output):
        if self.os == 'windows':
            data = self.windows.return_output(output)
        elif self.os == 'linux':
            pass
            data = self.linux.return_output(output)
        return data

    def return_alert(self, data, max_responce):
        if self.os == 'windows':
            data = self.windows.return_alert(data, max_responce)
        elif self.os == 'linux':
            pass
            data = self.linux.return_alert(data, max_responce)
        return data


class Trace_Windows(object):
    __doc__ = ''' Controls Data manipulation for Windows tracert '''

    def run_command(self, ip=None, prefix=None):
        if prefix != None and ip !=None:
            cmd = prefix + ' ' + str(ip)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output = proc.communicate()[0]
            return output
        else:
            return 'ERROR'

    def remove_whitespace(self, string_value):
        # Replace all runs of whitespace with a single dash
        string_value = re.sub(r"\s+", ',', string_value)
        return string_value

    def clean_output(self, output):
        cleaned_output = []
        decoded_output = output.decode('utf-8').encode('utf8')
        linesplit_output = decoded_output.splitlines()
        for line in linesplit_output:
            clean_line = self.remove_whitespace(line)
            cleaned_output.append(clean_line)
        return(cleaned_output)

    def return_output(self, data):
        returned_data = []
        returned_data.append(['HOP', 'TRIP1', 'TRIP2', 'TRIP3', 'HOST', 'HOSTNAME'])
        counter = 0
        for line in data:
            if counter != 1 and counter != 2 and counter != len(data)-1 and counter != len(data)-2 and line != '':

                #Define lines
                line = line[1:]
                first = line.find(',')
                second = line.find(',', first + 1)
                third = line.find(',', second + 1)
                fourth = line.find(',', third + 1)
                fith = line.find(',', fourth + 1)
                sixth = line.find(',', fith + 1)
                seventh = line.find(',', sixth + 1)
                eigth = line.find(',', seventh + 1)

                #Assign lines
                if line.count(',') == 6:
                    hop = line[0:first].strip().replace(',', '')
                    hostname = line[second:third].replace(',', '')
                    host = line[second:third].replace(',', '')
                    round1 = line[second:third].replace(',', '')
                    round2 = line[second:third].replace(',', '')
                    round3 = line[second:third].replace(',', '')
                else:
                    hop = line[0:first].strip().replace(',', '')
                    round1 = line[first:second].replace(',', '')
                    round2 = line[third:fourth].replace(',', '')
                    round3 = line[fith:sixth].replace(',', '')
                    host = line[seventh:eigth].replace(',', '')
                    hostname = line[eigth:].replace(',', '')

                returned_data.append([hop,  round1, round2, round3, host, hostname])
            else:
                #Scrap data, drop
                pass
            counter = counter + 1
        return returned_data

    def return_alert(self, data, max_responce):
        problem_areas = []
        for line in data:
            error = False
            # Set a counter. Use this to miss the HOP when generating the alert
            counter = 0
            problem_item = []
            for item in line:
                if counter != 0 and counter != 4 and counter != 5:
                    try:
                        item_cast = int(item)
                        if item_cast > max_responce:
                            error = True
                    except ValueError:
                        if item == '*':
                            error = False
                        else:
                            # Unexpected, unimportant, pass
                            pass
                else:
                    #Pass over hop
                    pass

                #Increment counter, append items. If last item of dataset, append error=? then append to total list
                counter = counter + 1
                problem_item.append(item)
                if error == True and counter == 6:
                    problem_item.append('ERROR=TRUE')
                elif error == False and counter == 6:
                    problem_item.append('ERROR=FALSE')
                if counter == 6:
                    problem_areas.append(problem_item)
                else:
                    pass
        return problem_areas



class Trace_Linux(object):
    __doc__ = ''' Controls Data manipulation for Linux traceroute '''

    def run_command(self, ip=None, hop=None, prefix=None):
        if hop == None:
            hop = ''

        if prefix != None and ip !=None:
            cmd = prefix + ' ' + str(ip)
            output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
            return output
        else:
            return 'ERROR'

    def remove_whitespace(self, string_value):
        # Replace all runs of whitespace with a single dash
        string_value = re.sub(r"\s+", ',', string_value)
        return string_value

    def clean_output(self, output):
        cleaned_output = []
        decoded_output = output.decode('utf-8').encode('utf-8')
        linesplit_output = decoded_output.splitlines()
        for line in linesplit_output:
            clean_line = self.remove_whitespace(line)
            cleaned_output.append(clean_line)
        return(cleaned_output)

    def return_output(self, data):
        returned_data = []
        returned_data.append(['HOP', 'HOST', 'HOSTNAME', 'TRIP1', 'TRIP2', 'TRIP3'])
        counter = 0
        for line in data:
            if counter != 0 and line != '':

                #Define lines
                line = line[0:]
                first = line.find(',')
                second = line.find(',', first + 1)
                third = line.find(',', second + 1)
                fourth = line.find(',', third + 1)
                fith = line.find(',', fourth + 1)
                sixth = line.find(',', fith + 1)
                seventh = line.find(',', sixth + 1)
                eigth = line.find(',', seventh + 1)
                nineth = line.find(',', eigth + 1)

                #Assign lines
                if line.count(',') == 3:
                    hop = line[0:first].strip().replace(',', '')
                    hostname = line[second:third].replace(',', '')
                    host = line[second:third].replace(',', '')
                    round1 = line[second:third].replace(',', '')
                    round2 = line[second:third].replace(',', '')
                    round3 = line[second:third].replace(',', '')
                elif line.count(',') == 8:
                    hop = line[0:first].strip().replace(',', '')
                    hostname = line[first:second].replace(',', '')
                    host = line[second:third].replace(',', '')
                    round1 = line[third:fourth].replace(',', '')
                    round2 = line[fith:sixth].replace(',', '')
                    round3 = line[seventh:eigth].replace(',', '')
                elif line.count(',') == 9:
                    hop = line[first:second].strip().replace(',', '')
                    hostname = line[second:third].replace(',', '')
                    host = line[third:fourth].replace(',', '')
                    round1 = line[fourth:fith].replace(',', '')
                    round2 = line[sixth:seventh].replace(',', '')
                    round3 = line[eigth:nineth].replace(',', '')

                returned_data.append([hop,  round1, round2, round3, host, hostname])

            else:
                pass
            counter = counter + 1
        return returned_data

    def return_alert(self, data, max_responce):
        problem_areas = []
        lineCounter = 0
        for line in data:
            error = False
            # Set a counter, use this to miss the HOP when generating the alert
            counter = 0
            problem_item = []
            if lineCounter != 0:
                for item in line:
                    if counter != 0:
                        try:
                            item_cast = float(item)
                            if item_cast > max_responce:
                                error = True
                        except ValueError:
                            #Expecting ValueErrors due to hostname and gateway
                            if item == '*':
                                error = False
                            else:
                                #Unexpected, unimportant, pass
                                pass
                    else:
                        #Pass over hop
                        pass

                    #Increment counter, Add item to list, if last item in list, append error value
                    counter = counter + 1
                    problem_item.append(item)
                    if error == True and counter == 6:
                        problem_item.append('ERROR=TRUE')
                    elif error == False and counter == 6:
                        problem_item.append('ERROR=FALSE')
                    else:
                        #Unexpected Return, unimportant
                        pass

                    #If the last item has been reached and error value added, append to main list
                    if counter == 6:
                        problem_areas.append(problem_item)
                    else:
                        #Unexpected Return, unimportant
                        pass
            else:
                #Header Value, Pass
                pass

            lineCounter = lineCounter + 1
        return problem_areas


class build_HTML(object):
    __doc__ = '''Class to handle HTML building function / Wrapper with logic'''

    def __init__(self):
        self.html = []

    def controller(self, ip, payload):
        self.build_head(ip)
        self.insert_css()
        self.close_head()
        self.open_body()
        self.insert_list(payload)
        self.insert_table(payload)
        self.close_body()
        return ''.join(self.html)

    def builder(self, tab, data):
        counter = 0
        line = []
        while counter < tab:
            line.append('\t')
            counter = counter + 1
        line.append(data)
        line.append('\n')
        self.html.append(''.join(line))

    def build_head(self, ip):
        self.builder(0, '<!DOCTYPE html>')
        self.builder(0, '<html>')
        self.builder(0, '<head>')
        title = '<h3> Trace:' + ip + '</h3>'
        self.builder(1, title)
        self.builder(0, '<style>')

    def close_head(self):
        self.builder(0, '</style>')
        self.builder(0, '</head>')

    def insert_css(self):
        
        #Table
        self.builder(1, 'table {')
        self.builder(2, 'max-width: 100%;')
        self.builder(2, 'min-width: 20%;')
        self.builder(2, 'border-style: solid;')
        self.builder(2, 'border: 2px solid grey;')
        self.builder(2, 'font-family: sans-serif;')
        self.builder(2, 'font-size:15px;')
        self.builder(2, 'background:#C0C0C0;')
        self.builder(2, 'color: white;')
        self.builder(2, 'font-weight:bold;')
        self.builder(1, '}')

        self.builder(1, 'td, th {')
        self.builder(2, 'min-width: 5px;')
        self.builder(2, 'height: 20px;')
        self.builder(2, 'text-align: center;')
        self.builder(2, 'border: 1px solid grey;')
        self.builder(1, '}')

        #List
        self.builder(1, 'li {')
        self.builder(2, 'width: 2em;')
        self.builder(2, 'height: 2em;')
        self.builder(2, 'text-align: center;')
        self.builder(2, 'line-height: 2em;')
        self.builder(2, 'border-radius: 1em;')
        self.builder(2, 'background: dodgerblue;')
        self.builder(2, 'margin: 0 1em;')
        self.builder(2, 'display: inline-block;')
        self.builder(2, 'color: white;')
        self.builder(2, 'position: relative;')
        self.builder(1, '}')

        self.builder(1, 'li::before{')
        self.builder(2, 'content:"";')
        self.builder(2, 'position: absolute;')
        self.builder(2, 'top: .9em;')
        self.builder(2, 'left: -4em;')
        self.builder(2, 'width: 4em;')
        self.builder(2, 'height: .2em;')
        self.builder(2, 'background: grey;')
        self.builder(2, 'z-index: -1;')
        self.builder(1, '}')

        self.builder(1, 'li:first-child::before {')
        self.builder(2, 'display: none;')
        self.builder(1, '}')

        self.builder(1, '.OK {')
        self.builder(2, 'background: green;')
        self.builder(1, '}')

        self.builder(1, '.ERROR{')
        self.builder(2, 'background: red;')
        self.builder(1, '}')

        self.builder(1, 'body {')
        self.builder(2, 'font-family: sans-serif;')
        self.builder(2, 'padding: 2em;')
        self.builder(1, '}')

    def open_body(self):
        self.builder(0, '<body>')

    def close_body(self):
        self.builder(0, '</body>')
        self.builder(0, '</html>')

    def insert_list(self, payload):
        self.builder(1, '<ul>')
        counter = 0
        
        for item in payload:
            if counter != 0:
                if item[6] == 'ERROR=FALSE':
                    htmlList = '<li class="OK">' + item[0] + '</li>'
                    self.builder(2, htmlList)
                elif item[6] == 'ERROR=TRUE':
                    htmlList = '<li class="ERROR">' + item[0] + '</li>'
                    self.builder(2, htmlList)
                else:
                    #Unexpected Error, not important
                    pass
            else:
                #headervalue
                pass
            counter = counter + 1
        self.builder(1, '</ul>')
        self.builder(1, '</br>')
        self.builder(1, '</br>')

    def insert_table(self, payload):
        self.builder(1, '<table>')
        self.builder(2, '<tr>')
        self.builder(3, '<td>' + 'HOP' + '</td>')
        self.builder(3, '<td>' + 'HOST' + '</td>')
        self.builder(3, '<td>' + 'MAX RESPONSE' + '</td>')
        self.builder(2, '</tr>')
        
        counter = 0
        for item in payload:
            if counter != 0:
                try:
                    if float(item[1]) > float(item[2]) and float(item[1]) > float(item[3]):
                        max_resp = item[1]
                    elif float(item[2]) > float(item[1]) and float(item[2]) > float(item[3]):
                        max_resp = item[2]
                    elif float(item[3]) > float(item[1]) and float(item[3]) > float(item[2]):
                        max_resp = item[3]
                    else:
                        max_resp = item[1]
                except:
                    #Can occur due to item = *
                    max_resp = item[1]

                if item[6] == 'ERROR=FALSE':
                    self.builder(2, '<tr>')
                    self.builder(3, '<td class="OK">' + item[0] + '</td>')
                    self.builder(3, '<td class="OK">' + item[4] + '</td>')
                    self.builder(3, '<td class="OK">' + max_resp + '</td>')
                    self.builder(2, '</tr>')
                elif item[6] == 'ERROR=TRUE':
                    self.builder(2, '<tr>')
                    self.builder(3, '<td class="ERROR">' + item[0] + '</td>')
                    self.builder(3, '<td class="ERROR">' + item[4] + '</td>')
                    self.builder(3, '<td class="ERROR">' + max_resp + '</td>')
                    self.builder(2, '</tr>')
                else:
                    #Unexpected Error, not important
                    pass
            else:
                #header value
                pass
            counter = counter + 1
        self.builder(1, '<table>')


class Controller(object):
    __doc__ = '''Controller class for clean main() use and class import with multi-thread enablement '''

    def main(self):
        parser = OptionParser()
        parser.set_description('NeTrace to HTML path generator')
        parser.set_usage('''
        Trace -d www.google.com,www.new24.com,127.0.0.1
        Trace -d www.google.com -r 300
        Trace -d www.google.com -r 300 -l /tmp -f google.html
        Trace --destination www.google.com --maxresponce 300 --filelocation c:\\temp\\ --filename google.html
        ''')

        parser.add_option("-d", "--destination", dest='destination', help="[REQUIRED] Destination to trace")
        parser.add_option("-r", "--maxresponce", dest='response', default=300,
                          help="Max response time before marking as an error")
        parser.add_option("-l", "--filelocation", dest="html_location", help="Filepath including trailing slash")
        parser.add_option("-f", "--filename", dest="html_name", help="Filename including .html")
        (options, args) = parser.parse_args()

        # Check for null values (Accounted for, so they are allowed)
        if options.destination is None or options.html_location == '':
            parser.error("parameter -d is required")
        else:
            # check if multiple destinations, split
            if options.destination.find(',') > 1:
                destinations = options.destination.split(',')
            else:
                destinations = [options.destination]
        if options.html_location is None or options.html_location == '':
            html_location = None
        else:
            html_location = options.html_location
        if options.html_name is None or options.html_name == '':
            html_name = None
        else:
            html_name = options.html_name

        max_response = float(options.response)
        self.controller(destinations, max_response, html_location, html_name)

    def controller(self, destinations, max_response, html_location, html_name):
        '''self.controller(): Enable for multithread site checking '''
        for item in destinations:
            self.trace = Trace()
            threading.Thread(target=self.trace.controller, args=(item, max_response, html_location, html_name)).start()

if __name__ == "__main__":
    ctl = Controller()
    ctl.main()