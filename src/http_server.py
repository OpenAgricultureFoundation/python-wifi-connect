import os, getopt, sys, json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from io import BytesIO

# Defaults
PORT = 80
UI_PATH = '../ui'
SIMULATE = False


#------------------------------------------------------------------------------
# A custom http server class in which we can set the default path it serves
# when it gets a GET request.
class MyHTTPServer(HTTPServer):
    def __init__(self, base_path, server_address, RequestHandlerClass):
        self.base_path = base_path
        HTTPServer.__init__(self, server_address, RequestHandlerClass)


#------------------------------------------------------------------------------
# A custom http request handler class factory.
# Handle the GET and POST requests from the UI form and JS.
# The class factory allows us to pass custom arguments to the handler.
def RequestHandlerClassFactory(simulate):

    class MyHTTPReqHandler(SimpleHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            # We must set our custom class properties first, since __init__() of
            # our super class will call do_GET().
            self.simulate = simulate
            super(MyHTTPReqHandler, self).__init__(*args, **kwargs)

        # See if this is a specific request, otherwise let the server handle it.
        def do_GET(self):

            #debugrob do a redirect to "http://<gateway>/" if path is???
            print(f'GET {self.path}')

            # Handle a REST API request to return the list of SSIDs
            if '/networks' == self.path:
                self.send_response(200)
                self.end_headers()
                response = BytesIO()
                ssids = []
                if self.simulate:
                    print(f'Simulating a list of NetworkManager APs')
                    ssids = [{"ssid": "open network", "security": "NONE"}, \
                             {"ssid": "wpa2", "security":"WPA2"}, \
                             {"ssid": "wep", "security":"WEP"}, \
                             {"ssid": "wpa", "security":"WPA"}, \
                             {"ssid": "enterprise", "security": "ENTERPRISE"}]
                else:
                    pass #debugrob, get list of AP from net man on RPI

                # always add a hidden place holder
                ssids.append({"ssid": "Enter a hidden WiFi name", \
                              "security": "HIDDEN"})

                response.write(json.dumps(ssids).encode('utf-8'))
                print(f'GET {self.path} returning: {response.getvalue()}')
                self.wfile.write(response.getvalue())
                return
                """debugrob, use these constants, map net man to these
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

            # All other requests are handled by the server which vends files 
            # from the ui_path we were initialized with.
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

    return  MyHTTPReqHandler # the class our factory just created.


#------------------------------------------------------------------------------
# Run the HTTP server.
def main(port, ui_path, simulate):

    # Find the ui directory which is up one from where this file is located.
    web_dir = os.path.join(os.path.dirname(__file__), ui_path)
    print(f'HTTP serving directory: {web_dir}')

    # Change to this directory so the HTTPServer returns the index.html in it 
    # by default when it gets a GET.
    os.chdir(web_dir)

    # Host:Port our HTTP server listens on
#    server_address = ('localhost', port)
#debugrob, add command line option and default for this:
    server_address = ('192.168.42.1', port)

    # Custom request handler class (so we can pass in our own args)
    MyRequestHandlerClass = RequestHandlerClassFactory(simulate)

    # Start an HTTP server to serve the content in the ui dir and handle the 
    # POST request in the handler class.
    httpd = MyHTTPServer(web_dir, server_address, MyRequestHandlerClass)
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
    simulate = SIMULATE

    usage = ''\
f'Command line args: \n'\
f'  -p <HTTP server port>       Default: {port} \n'\
f'  -u <UI directory to serve>  Default: "{ui_path}" \n'\
f'  -s Simulate NetworkManager  Default: {simulate} \n'\
f'  -h Show help.\n'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:u:sh")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()

        elif opt in ("-s"):
            simulate = True

        elif opt in ("-p"):
            port = string_to_int(arg, port)

        elif opt in ("-u"):
            ui_path = arg

    print(f'Port={port}')
    print(f'UI path={ui_path}')
    print(f'Simulate={simulate}')
    main(port, ui_path, simulate)


