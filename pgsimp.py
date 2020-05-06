
#!/usr/bin/python

from __future__ import absolute_import
from __future__ import print_function

import os, sys, getopt, signal, string, fnmatch, math
import random, time, subprocess, traceback, serial, glob
import serial.tools.list_ports

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

# ------------------------------------------------------------------------

class   SimpleTree(Gtk.TreeView):

    def __init__(self, head = [], editx = [], skipedit = 0):

        Gtk.TreeView.__init__(self)

        self.callb = None
        self.chcallb = None

        # repair missing column
        if len(head) == 0:
            head.append("")

        if len(editx) == 0:
            editx.append("")

        self.types = []
        for aa in head:
            self.types.append(str)

        self.treestore = Gtk.TreeStore()
        self.treestore.set_column_types(self.types)

        cnt = 0
        for aa in head:
            # Create a CellRendererText to render the data
            cell = Gtk.CellRendererText()
            if cnt > skipedit:
                cell.set_property("editable", True)
                cell.connect("edited", self.text_edited, cnt)

            tvcolumn = Gtk.TreeViewColumn(aa)
            tvcolumn.pack_start(cell, True)
            tvcolumn.add_attribute(cell, 'text', cnt)
            self.append_column(tvcolumn)
            cnt += 1

        self.set_model(self.treestore)
        self.connect("cursor-changed", self.selection)

    def text_edited(self, widget, path, text, idx):
        #print ("edited", widget, path, text, idx)
        self.treestore[path][idx] = text
        args = []
        for aa in self.treestore[path]:
            args.append(aa)
        self.chcallb(args)

    def selection(self, xtree):
        #print("simple tree sel", xtree)
        sel = xtree.get_selection()
        xmodel, xiter = sel.get_selected()
        if xiter:
            self.args = []
            for aa in range(len(self.types)):
                xstr = xmodel.get_value(xiter, aa)
                self.args.append(xstr)
            #print("selection", self.args)
            if self.callb:
                self.callb(self.args)

    def setcallb(self, callb):
        self.callb = callb

    def setCHcallb(self, callb):
        self.chcallb = callb

    def append(self, args):
        piter = self.treestore.append(None, args)

    def sel_last(self):
        sel = self.get_selection()
        xmodel, xiter = sel.get_selected()
        iter = self.treestore.get_iter_first()
        while True:
            iter2 = self.treestore.iter_next(iter)
            if not iter2:
                break
            iter = iter2
        sel.select_iter(iter)

    def clear(self):
        self.treestore.clear()

# ------------------------------------------------------------------------

class   SimpleEdit(Gtk.TextView):

    def __init__(self, head = []):

        Gtk.TextView.__init__(self)
        self.buffer = Gtk.TextBuffer()
        self.set_buffer(self.buffer)
        self.set_editable(True)
        self.connect("unmap", self.unmapx)
        #self.connect("focus-in-event", self.focus_in)
        #self.connect("focus-out-event", self.focus_out)
        self.connect("key-press-event", self.area_key)
        self.modified = False
        self.text = ""
        self.savecb = None
        #self.mefocus = False

    def focus_out(self, win, arg):
        #print("SimpleEdit focus_out")
        self.check_saved()
        #self.mefocus = False

    def check_saved(self):
        if not self.buffer.get_modified():
            return
        #print("Saving")
        startt = self.buffer.get_start_iter()
        endd = self.buffer.get_end_iter()
        self.text = self.buffer.get_text(startt, endd, False)
        if self.savecb:
            self.savecb(self.text)

    def focus_in(self, win, arg):
        pass
        #self.buffer.set_modified(False)
        #self.mefocus = True
        #print("SimpleEdit focus_in")

    def unmapx(self, widget):
        #print("SimpleEdit unmap", widget)
        pass

    def area_key(self, widget, event):
        #print("SimpleEdit keypress")  #, win, arg)
        #self.buffer.set_modified(True)
        pass

    def append(self, strx):
        self.check_saved()
        iter = self.buffer.get_end_iter()
        self.buffer.insert(iter, strx)
        self.buffer.set_modified(False)

    def clear(self):
        self.check_saved()
        startt = self.buffer.get_start_iter()
        endd = self.buffer.get_end_iter()
        self.buffer.delete(startt, endd)
        self.buffer.set_modified(False)

    def setsavecb(self, callb):
        self.savecb = callb

    def get_text(self):
        startt = self.buffer.get_start_iter()
        endd = self.buffer.get_end_iter()
        return self.buffer.get_text(startt, endd, False)


# Select character by index

class   SimpleSel(Gtk.Label):

    def __init__(self, text = " ", callb = None):
        self.text = text
        self.callb = callb
        self.axx = self.text.find("[All]")
        Gtk.Label.__init__(self, text)
        self.set_has_window(True)
        self.set_events(Gdk.EventMask.ALL_EVENTS_MASK )
        self.connect("button-press-event", self.area_button)
        self.modify_font(Pango.FontDescription("Mono 13"))

    def area_button(self, but, event):

        #print("sss =", self.get_allocation().width)
        #print("click", event.x, event.y)

        prop = event.x / float(self.get_allocation().width)
        idx = int(prop * len(self.text))
        if self.text[idx] == " ":
            idx -= 1
        try:
            # See of it is all
            if self.axx >= 0:
                if idx > self.axx:
                    #print("all", idx, self.text[idx-5:idx+7])
                    self.lastsel =  "All"
                    self.newtext = self.text[:self.axx] + self.text[self.axx:].upper()
                    self.set_text(self.newtext)
                else:
                    self.newtext = self.text[:self.axx] + self.text[self.axx:].lower()
                    self.set_text(self.newtext)

            else:
                self.lastsel =  self.text[idx]
                self.newtext = self.text[:idx] + self.text[idx].upper() + self.text[idx+1:]
                self.set_text(self.newtext)


            if self.callb:
                self.callb(self.lastsel)

        except:
            print(sys.exc_info())

# ------------------------------------------------------------------------
# Letter selection control

class   LetterSel(Gtk.VBox):

    def __init__(self, callb = None):

        Gtk.VBox.__init__(self)
        self.callb = callb

        strx = "abcdefghijklmnopqrstuvwxyz"
        hbox3a = Gtk.HBox()
        hbox3a.pack_start(Gtk.Label(" "), 1, 1, 0)
        self.simsel = SimpleSel(strx, self.letter)
        hbox3a.pack_start(self.simsel, 0, 0, 0)
        hbox3a.pack_start(Gtk.Label(" "), 1, 1, 0)

        strn = "1234567890!@#$^&*_+ [All]"
        hbox3b = Gtk.HBox()
        hbox3b.pack_start(Gtk.Label(" "), 1, 1, 0)
        self.simsel2 = SimpleSel(strn, self.letter)
        hbox3b.pack_start(self.simsel2, 0, 0, 0)
        hbox3b.pack_start(Gtk.Label(" "), 1, 1, 0)

        self.pack_start(hbox3a, 0, 0, False)
        self.pack_start(xSpacer(4), 0, 0, False)
        self.pack_start(hbox3b, 0, 0, False)

    def  letter(self, letter):
        #print("LetterSel::letterx:", letter)
        if self.callb:
            self.callb(letter)

