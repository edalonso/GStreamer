#!/usr/bin/python

import pygst  
pygst.require("0.10")
import sys, gst, gobject
gobject.threads_init()  
 
def main(args):
 
    if len(args) != 2:
        print "Uso:", args[0], " <archivo Ogg>"
        return -1

    pipestr = "filesrc location= %s ! mad ! audioconvert ! audioresample ! alsasink" % args[1]
 
    try:
        pipeline = gst.parse_launch(pipestr)
    except gobject.GError, e:
        print "No es posible crear la tuberia,", str(e)
        return -1
 
    def eventos(bus, msg):
        t = msg.type
        if t == gst.MESSAGE_EOS: 
            loop.quit()
 
        elif t == gst.MESSAGE_ERROR:
            e, d = msg.parse_error()
            print "ERROR:", e
            loop.quit()
 
        return True

    pipeline.get_bus().add_watch(eventos)
 
    pipeline.set_state(gst.STATE_PLAYING)
 
    loop = gobject.MainLoop()
    try:
        print "Reproduciendo..."    
        loop.run()
    except KeyboardInterrupt: # Por si se pulsa Ctrl+C
         pass
 
    print "Parando... \n Adios "
 
    pipeline.set_state(gst.STATE_NULL)
    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv))
