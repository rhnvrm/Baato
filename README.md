Baato 
=======================

##About 
Baato.py is a Multi threaded HTTP server along with a Flask server (listener.py) which lists all other Baato HTTP servers running on your LAN.

Requires `Python 2.7` (and [Flask](http://flask.pocoo.org/) for `listener.py`)

You can download [Python 2.7](https://www.python.org/downloads/release/python-2710/) and for [windows](https://www.python.org/downloads/release/python-2710/)

Make sure you have added [python to PATH](http://stackoverflow.com/a/21433154/790971) 

This is in the **BETA** stage, please report bugs and suggestions on the Issues section.



##Running the Host Server
Download [baato.py](https://github.com/rhnvrm/Baato/raw/master/baato.py)

You can start a Host Server by running `python baato.py`, which starts a server in port 8000 with the name "New Baato Server".

Your desired Port and Server name can be specified before starting:

For Example: `python baato.py --port 8080 --name "Rohan's Server"` will start a server at port 8080 and list the server as `Rohan's Server` in the Listener. You can use `-p` and `-n` as the short versions of these options.

The host server is an HTTP server that can handle simultaneous requests. It can also be used to run your own static website. Include an `index.html` in the root the directory where you started the server.

If you want to start the server in a different directory you should change your current working directory (eg `cd c:/share`) to that folder and run `python ~/Downloads/baato.py -p 8080 -n "Demo"` or you can copy/paste `baato.py` in the directory you would like to start the server and run it as `python baato.py`

##Running the Listening Server
If you don't have access to the IPs of the Host Servers, you can run the Listening Server on your machine. Ideally, a simple user won't need to bother with this and will just goto the Listening Server hosted by one of the Hosts and just need to bookmark that URL. 

You will need to install Flask.

You can start the server in port 5000 using `python listener.py`. If you want to, you can invoke it with the `-p` or `--port` option to use a different port.
