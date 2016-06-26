# --------------------------------------------------------------------------
# Logic for the 'serve' command.
# --------------------------------------------------------------------------

import ark
import sys
import os
import http.server
import webbrowser


# Command help text.
helptext = """
Usage: %s serve [FLAGS] [OPTIONS]

  Serve the site's output directory using Python's builtin web server.
  Automatically launches the default web browser to view the site.

  Host IP defaults to localhost (127.0.0.1). Specify an IP address to serve
  only on that address or '0.0.0.0' to serve on all available IPs.

  Port number defaults to 8080 as ports below 1024 require sudo. Set to 0 to
  randomly select an available port.

Options:
  -h, --host <str>    Host IP address. Defaults to localhost.
  -p, --port <int>    Port number. Defaults to 8080.

Flags:
      --help          Print this command's help text and exit.
      --no-browser    Do not launch the default web browser.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not ark.site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if not os.path.exists(ark.site.out()):
        sys.exit("Error: cannot locate the site's output directory.")

    os.chdir(ark.site.out())

    try:
        server = http.server.HTTPServer(
            (parser['host'], parser['port']),
            http.server.SimpleHTTPRequestHandler
        )
    except PermissionError:
        sys.exit("Error: use 'sudo' to run on a port below 1024.")
    except OSError:
        sys.exit("Error: address already in use. Choose a different port.")

    address = server.socket.getsockname()

    print("-" * 80)
    print("Root: %s" % ark.site.out())
    print("Host: %s"  % address[0])
    print("Port: %s" % address[1])
    print("Stop: Ctrl-C")
    print("-" * 80)

    if not parser['no-browser']:
        webbrowser.open("http://%s:%s" % (parser['host'], parser['port']))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "-" * 80 + "Stopping server...\n" + "-" * 80)
        server.server_close()
