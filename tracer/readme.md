# tracer

A simple python multi-os wrapper for Traceroute / Tracert (NetTrace) with a visual output.
Multithread enabled with the ability to variate on what your max reponse time should be alerted on.

# Useage
        Trace -d www.google.com,www.new24.com,127.0.0.1
        Trace -d www.google.com -r 300
        Trace -d www.google.com -r 300 -l /tmp -f google.html
        Trace --destination www.google.com --maxresponce 300 --filelocation c:\temp\ --filename google.html


NeTrace to HTML path generator

Options:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination=DESTINATION 
				       [REQUIRED] Destination to trace 
  -r RESPONSE, --maxresponce=RESPONSE
                        Max response time before marking as an error
  -l HTML_LOCATION, --filelocation=HTML_LOCATION
                        Filepath including trailing slash
  -f HTML_NAME, --filename=HTML_NAME
                        Filename including .html
			
# Examples
Trace -d www.google.com -r 5
			
![Google trace](https://github.com/henrystockza/python/blob/master/tracer/content/Example1.PNG "Google Trace")


Trace -d 127.0.0.1 -r 5
			
![Local trace](https://github.com/henrystockza/python/blob/master/tracer/content/Example2.PNG "Local Trace")

# LICENSE

MIT License

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

