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
from pggui import *

def vspacer(sp = 8):
    #ab = Gtk.Label.new(" ")
    lab = Gtk.VBox()
    #fff = Gtk.Frame()
    #fff.set_size_request(sp, sp)
    #lab.pack_start(fff, 0, 0, 0)
    lab.set_size_request(sp, sp)
    #lab.override_background_color(
    #                Gtk.StateFlags.NORMAL, Gdk.RGBA(1, .5, .5) )
    return lab

#def spacer(sp = 4):
#    #ab = Gtk.Label.new(" ")
#    lab = Gtk.HBox()
#    lab.set_size_request(sp, sp)
    return lab

class testWin(Gtk.Window):

    def __init__(self, *args, **kwargs):
        super(testWin, self).__init__(*args, **kwargs)

        self.connect("destroy", Gtk.main_quit)

        vbox13 = Gtk.VBox()

        #vbox13.pack_start(vspacer(), 0, 0, 0)
        vbox13.pack_start(Gtk.Label.new("  Test root entry window implementation  "), 1, 1, 0)

        popup = Gtk.Window.new( Gtk.WindowType.TOPLEVEL)
        #popup = Gtk.Window.new( Gtk.WindowType.POPUP)
        popup.set_title("Hello")

        popup.set_resizable(True)
        popup.set_transient_for(self)

        hb = Gtk.HeaderBar()
        hb.set_decoration_layout(None)
        hb.set_title("No title")
        hb.set_border_width(0)

        hb.set_size_request(-1, 10)
        #hb.set_show_close_button(True)

        popup.set_default_size(200, 300)
        Gtk.Label.new("Titlebar")
        popup.set_decorated(True)
        popup.set_skip_pager_hint(True)
        popup.set_skip_taskbar_hint(True)
        popup.set_type_hint(Gdk.WindowTypeHint.TOOLBAR)


        #popup.set_titlebar(Gtk.Button())
        #popup.set_titlebar(hb)

        popup.add(Gtk.Label.new("Hello"))
        popup.show_all()

        vbox13.pack_start(vspacer(), 1, 1, 0)

        hbox14 = Gtk.HBox()
        hbox14.pack_start(vspacer(), 1, 1, 0)
        butt3y = smallbutt("E_xit", self.exit_prog, "Exit program")
        hbox14.pack_start(butt3y, 0, 0, 0)
        hbox14.pack_start(vspacer(), 1, 1, 0)

        vbox13.pack_start(hbox14, 0, 0, 0)
        vbox13.pack_start(vspacer(12), 0, 0, 0)

        self.set_size_request(300, 200)
        self.add(vbox13)
        self.show_all()

        # Gtk.Label
        #print("children", butt3x.get_children())

    def regbutt(self, arg):
        print("regbutt pressed", arg)

    def exit_prog(self, arg):
        print("exit butt", arg)
        self.destroy()
        #Gtk.main_exit()

    def findx(self, arg):
        print("Findx", arg)

    def delx(self, arg):
        print("Delx", arg)

if __name__ == "__main__":
    Gtk.init(sys.argv)
    testwin = testWin()
    Gtk.main()

# EOF