# portquery
Query multiple ports (tcp / udp) on multiple hosts, cross platform.
Export to screen, csv, html, xml, json

#Example

Print to Screen

Export CSV
Export XML
Export Json

# Usage
                portquery -d www.google.com -p 80
                portquery -d 127.0.0.1,www.google.com -p 80,445 -u --screen
                portquery -d 127.0.0.1,www.google.com -p 8080,445 -u -t --screen --csv --xml --json
                portquery --destination 127.0.0.1,www.google.com --port 8080,445 --udp --tcp --screen --csv --xml --json


Query list o given ports to determine if they are available

Options:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination=DESTINATION
                        [REQUIRED] Destination'[s] to query
  -p PORT, --port=PORT  Port'[s] to query
  -t, --tcp             Flag to scan only TCP
  -u, --u               Flag to scan only UDP
  -f FILENAME, --filename=FILENAME
                        Full file path and name, excluding extension
  --screen              Print information to screen
  --csv                 Export information to csv
  --xml                 Export information to xml
  --json                Export information to json
  
  
#MIT License

Copyright (c) 2017 HenryStockZa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
