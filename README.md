Baato | A simple HTTP Host and Online Server Listing
=======================
Requires `Python 2.7` (and [Flask](http://flask.pocoo.org/) for `listener.py`)

You can download [Python 2.7](https://www.python.org/downloads/release/python-2710/) and for [windows](https://www.python.org/downloads/release/python-2710/)

This is in the **ALPHA** stage and it has not been tested, please report bugs and suggestions on the Issues section.



##Running the Host Server
Download [baato.py](https://github.com/rhnvrm/Baato/raw/master/baato.py)

You can start a Host Server by running `python baato.py`

Your desired Port and Server name can be specified before starting:

For Example: `python baato.py 8080 "Rohan's Server"` will start a server at port 8080 and list the server as `Rohan's Server` in the Listener.

The host server is an HTTP server that can handle simultaneous requests. It can also be used to run your own static website. Include an `index.html` in the root the directory where you started the server.

If you want to start the server in a different directory you should change your current working directory (eg `cd c:/share`) to that folder and run `python ~/Downloads/baato.py 8080 "Demo"`

##Running the Listening Server
If you don't have access to the IPs of the Host Servers, you can run the Listening Server on your machine. Ideally, a simple user won't need to bother with this and will just goto the Listening Server hosted by one of the Hosts and just need to bookmark that URL. 

You will need to install Flask.

Download the file and just start the server using `python listener.py`
