# tracer

A simple python multi-os wrapper for Traceroute / Tracert (NetTrace) with a visual output.
Multithread enabled with the ability to variate on what your max reponse time should be alerted on.




Usage:
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