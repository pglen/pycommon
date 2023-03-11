#!/usr/bin/env python

import sys

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2

from pgbutt import *

class testWin(Gtk.Window):

    def __init__(self, *args, **kwargs):
        super(testWin, self).__init__(*args, **kwargs)

        self.connect("destroy", Gtk.main_quit)

        vbox13 = Gtk.VBox()

        hbox13 = Gtk.HBox()
        hbox13.pack_start(Gtk.Label("  "), 1, 1, 0)
        butt3x = smallbutt(" _Find in Text ", self.findx, "Find in text")
        hbox13.pack_start(butt3x, 0, 0, 0)
        hbox13.pack_start(Gtk.Label("  "), 1, 1, 0)

        hbox14 = Gtk.HBox()
        hbox14.pack_start(Gtk.Label("  "), 1, 1, 0)
        butt3y = smallbutt("Te_xt", self.textx, "Find in text")
        hbox14.pack_start(butt3y, 0, 0, 0)
        hbox14.pack_start(Gtk.Label("   "), 1, 1, 0)

        hbox15 = Gtk.HBox()
        hbox15.pack_start(Gtk.Label("  "), 1, 1, 0)
        butt3z = Gtk.Button.new_with_mnemonic("Regular _Button")
        butt3z.set_relief(Gtk.ReliefStyle.NONE)
        #, self.textx, "Find in text")
        hbox15.pack_start(butt3z, 0, 0, 0)
        hbox15.pack_start(Gtk.Label("   "), 1, 1, 0)

        vbox13.pack_start(Gtk.Label("   "), 1, 1, 0)
        vbox13.pack_start(hbox13, 0, 0, 0)
        vbox13.pack_start(Gtk.Label("   "), 0, 0, 0)
        vbox13.pack_start(hbox14, 0, 0, 0)
        vbox13.pack_start(Gtk.Label("   "), 1, 1, 0)
        vbox13.pack_start(hbox15, 0, 0, 0)
        vbox13.pack_start(Gtk.Label("   "), 1, 1, 0)

        self.set_size_request(200, 100)
        self.add(vbox13)
        self.show_all()

    def textx(self, arg, arg2):
        print("textx", arg, arg2)

    def findx(self, arg, arg2):
        print("Findx", arg, arg2)

if __name__ == "__main__":
    Gtk.init(sys.argv)
    testwin = testWin()
    Gtk.main()


