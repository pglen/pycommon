#!/usr/bin/env python

''' This encapsulates the browser window wit the webkia an toolbars '''

import os, sys, getopt, signal, random, time, warnings

realinc = os.path.realpath(os.path.dirname(__file__) + os.sep + "../pycommon")
sys.path.append(realinc)

from pgutils import  *
from pggui import  *
from pgsimp import  *

import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

try:
    import pgwkit
except:
    print("Cannot load WebKit2", sys.exc_info())
    sys.exit(1)

class  brow_win(Gtk.VBox):

    ''' Collection of URL bar, toolbar, status bar '''

    def __init__(self):

        try:
            Gtk.VBox.__init__(self)
        except:
            pass

        hbox3 = self.urlbar()
        self.pack_start(hbox3, 0, 0, 0)

        #if not conf.kiosk:
        #    vbox.pack_start(hbox3, False, False, 2)

        self.scroll_win = Gtk.ScrolledWindow()

        try:
            self.webview = pgwkit.pgwebw(self)
        except:
            print("Please install webkit2")
            #sys.exit(1)
            raise

        self.ui = pgwkit.generate_ui(self.webview)

        self.scroll_win.add(self.webview)
        self.webview.editor = self.webview

        self.toolbar2 = self.ui.get_widget("/toolbar_format")
        self.pack_start(self.toolbar2, False, False, 0)

        self.pack_start(self.scroll_win, 1, 1, 2)

        hbox5 = Gtk.HBox()
        hbox5.pack_start(Gtk.Label("  "), 0, 0, 0)
        self.status = Gtk.Label(" Idle ");
        self.status.set_xalign(0)

        hbox5.pack_start(self.status, 1, 1, 0)
        hbox5.pack_start(Gtk.Label("  "), 0, 0, 0)
        self.set_status(" Idle State ")

        self.pack_start(hbox5, 0, 0, 2)

    def url_callb(self, xtxt):
        self.webview.go(xtxt)

    def url_callb(self, xtxt):
        self.go(xtxt)

    def backurl(self, url, parm, buff):
        self.webview.go_back()

    def baseurl(self, url, parm, buff):
        self.webview.load_uri("file://" + self.fname)

    def forwurl(self, url, parm, buff):
        self._win.webview.go_forward()

    def gourl(self, url, parm, buff):
        self.go(self.edit.get_text())

    def go(self, xstr):
        print("go", xstr)

        #  Leave known URL scemes alone
        if xstr[:7] == "file://":
            sss = os.path.realpath(xstr[7:])
            xstr = "file://" + sss
            pass
        elif xstr[:7] == "http://":
            pass
        elif xstr[:8] == "https://":
            pass
        elif xstr[:6] == "ftp://":
            pass
        elif str.isdecimal(xstr[0]):
            #print("Possible IP")
            pass
        else:
            # Yeah, padd it
            xstr = "https://" + xstr

        self.brow_win.webview.load_uri(xstr)

    def set_status(self, xtxt):
        self.status.set_text(xtxt)

    def urlbar(self):

        self.edit = SimpleEdit();
        self.edit.setsavecb(self.url_callb)
        self.edit.single_line = True

        hbox3 = Gtk.HBox()
        uuu  = Gtk.Label("  URL:  ")
        uuu.set_tooltip_text("Current / New URL; press Enter to go")
        hbox3.pack_start(uuu, 0, 0, 0)

        hbox3.pack_start(self.edit, True, True, 2)

        bbb = LabelButt(" Go ", self.gourl, "Go to speified URL")
        ccc = LabelButt(" <-Back  ", self.backurl, "Go Back")
        ddd = LabelButt("  Forw-> ", self.forwurl, "Go Forw")
        eee = LabelButt("   Base  ", self.baseurl, "Go to base URL")

        hbox3.pack_start(Gtk.Label("  "), 0, 0, 0)

        hbox3.pack_start(bbb, 0, 0, 0)
        hbox3.pack_start(ccc, 0, 0, 0)
        hbox3.pack_start(ddd, 0, 0, 0)
        hbox3.pack_start(eee, 0, 0, 0)

        hbox3.pack_start(Gtk.Label("  ^  "), 0, 0, 0)
        hbox3.pack_start(Gtk.Label(" "), 0, 0, 0)

        return hbox3

# EOF