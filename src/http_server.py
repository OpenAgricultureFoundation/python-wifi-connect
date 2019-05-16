import os, getopt, sys, json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO

# Defaults
PORT = 5000
UI_PATH = '../ui'


#------------------------------------------------------------------------------
# A custom http server class in which we can set the default path it serves
# when it gets a GET request.
class MyHTTPServer(HTTPServer):
    def __init__(self, base_path, server_address, RequestHandlerClass):
        self.base_path = base_path
        HTTPServer.__init__(self, server_address, RequestHandlerClass)


#------------------------------------------------------------------------------
# A custom http request handerl class to handle the POST-ed data from the form.
class MyHTTPReqHandler(SimpleHTTPRequestHandler):

    # See if this is a specific request, otherwise let the server handle it.
    def do_GET(self):

        # Handle a REST API request to return the list of SSIDs
        if '/networks' == self.path:
            self.send_response(200)
            self.end_headers()
            response = BytesIO()
#debugrob, test ssids, get from NetworkManager on RPI
            ssids = [{"ssid": "open network", "security": "NONE"}, \
                     {"ssid": "wpa2", "security":"WPA2"}, \
                     {"ssid": "enterprise", "security": "ENTERPRISE"}]
            # always add a hidden place holder
            ssids.append({"ssid": "Enter a hidden WiFi name", \
                          "security": "HIDDEN"})

#debugrob: also test the UI handling no SSIDs
#            ssids = []
            response.write(json.dumps(ssids).encode('utf-8'))
            print(f'GET {self.path} returning: {response.getvalue()}')
            self.wfile.write(response.getvalue())
            return
            """debugrob, how do these compare with the python NetworkManager,
            and the debian server?   (they match iPhone options)
            Security:
                NONE         
                HIDDEN         
                WEP         
                WPA        
                WPA2      
                ENTERPRISE
            Creds:
                NONE,
                HIDDEN, WEP, WPA, WPA2 need password
                ENTERPRISE needs username and password
            """
#debugrob: UI needs to handle the security type and ask for (un-hide form fields) for the proper creds.

        # All other requests are handled by the server which vends files from
        # the ui_path we were initialized with.
        super().do_GET()


    # test with: curl localhost:5000 -d "{'name':'value'}"
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        print(f'POST received: {body}')
#debugrob: parse this body for the form fields
        response.write(b'OK\n')
        self.wfile.write(response.getvalue())


#------------------------------------------------------------------------------
# Run the HTTP server.
def main(port, ui_path):
    # Find the ui directory which is up one from where this file is located.
    web_dir = os.path.join(os.path.dirname(__file__), ui_path)
    print(f'HTTP serving directory: {web_dir}')

    # Change to this directory so the HTTPServer returns the index.html in it 
    # by default when it gets a GET.
    os.chdir(web_dir)

    # Start an HTTP server to serve the content in the ui dir and handle the 
    # POST request in the handler class.
    httpd = MyHTTPServer(web_dir, ('localhost', port), MyHTTPReqHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


#------------------------------------------------------------------------------
# Util to convert a string to an int, or provide a default.
def string_to_int(s, default):
    try:
        return int(s)
    except ValueError:
        return default


#------------------------------------------------------------------------------
# Entry point and command line argument processing.
if __name__ == "__main__":
    port = PORT
    ui_path = UI_PATH

    usage = ''\
f'Command line args: \n'\
f'  -p <HTTP server port>       Default: {port} \n'\
f'  -u <UI directory to serve>  Default: "{ui_path}" \n'\
f'  -h                          Show help. \n'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:u:h")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()

        elif opt in ("-p"):
            port = string_to_int(arg, port)

        elif opt in ("-u"):
            ui_path = arg

    print(f'Port={port}')
    print(f'UI path={ui_path}')
    main(port, ui_path)


