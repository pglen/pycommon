#!/usr/bin/env python

''' This encapsulates the webkit '''

import os, sys, getopt, signal, random, time, warnings
import inspect

realinc = os.path.realpath(os.path.dirname(__file__) + os.sep + "../pycommon")
sys.path.append(realinc)

from pgutils import  *
from pggui import  *
from pgsimp import  *
from pgtextview import  *

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango

try:
    gi.require_version('WebKit2', '4.0')
    from gi.repository import WebKit2

    #print(WebKit2)
    print("Webkit ver", WebKit2.get_major_version(), WebKit2.get_minor_version(), WebKit2.get_micro_version())
    present = 1

except:
    # Define a blank one  -- too complex to work
    #class   WebKit2():
    #    def __init__(self):
    #        pass
    #    class  WebView(Gtk.Label):
    #        def __init__(self):
    #            pass
    #        def load_uri(self, url):
    #            pass
    print("Cannot import webkit2, web functions may not be available.")
    present = 0
    raise

class pgwebw(WebKit2.WebView):

    def __init__(self, xlink=None):
        try:
            GObject.GObject.__init__(self)
        except:
            print("Cannot ??? in parent object", sys.exc_info())
            pass
        self.xlink = xlink
        self.set_editable(True)

        #if editable:
        #    self.set_editable(True)

        self.filename = ""
        self.load_html("", "file:///")
        self.editor = self

    def do_ready_to_show(self):
        #print("do_ready_to_show() was called")
        pass

    def do_load_changed(self, status):

        #print("do_load_changed() was called", status)
        if self.get_uri():
            if self.xlink:
                self.xlink.status.set_text("Loading ... " + self.get_uri()[:64])

        if status == 3: #WebKit2.LoadEvent.WEBKIT_LOAD_FINISHED:
            #print("got WEBKIT_LOAD_FINISHED")
            if self.get_uri():
                if self.xlink:
                    self.xlink.edit.set_text(self.get_uri()[:64])
                    self.xlink.status.set_text("Finished: " + self.get_uri()[:64])
            self.grab_focus()

    def do_load_failed(self, load_event, failing_uri, error):
        print("do_load_failed() was called", failing_uri)
        if self.xlink:
            self.xlink.status.set_text("Failed: " + failing_uri[:64])

    def on_action(self, action):
        #print("on_action", action.get_name())
        self.run_javascript("document.execCommand('%s', false, false);" % action.get_name())

    def on_paste(self, action):
        self.execute_editing_command(WebKit2.EDITING_COMMAND_PASTE)

    def on_new(self, action):
        self.load_html("", "file:///")

    def on_fontsize(self, action):
        print("on_fontsize")
        c = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        sel = c.wait_for_targets()
        #print("sel", sel)
        target = Gdk.Atom.intern ("text/plain", True);
        ccc = c.wait_for_contents(target)
        ddd = ccc.get_data().decode()
        #print("ddd", ddd)
        sizex = sizedialog(ddd)
        if sizex:
            #print("sizex", sizex)
            htmlx = "<div style=font-size:%dpx;>%s</div>" % (int(sizex), ddd)
            print("htmlx", htmlx)
            self.run_javascript("document.execCommand('insertHTML', null, '%s');" % htmlx)
            #self.run_javascript("document.execCommand('insertText', null, '%s');" % htmlx)

        #for aa in sel[1]:
        #    try:
        #        print(aa.name())
        #        ccc = c.wait_for_contents(aa)
        #        print("ccc", ccc.get_data())
        #    except:
        #        pass

        #sel = Gtk.TextBuffer()
        #c.wait_is_rich_text_available(sel)
        #print("sel", sel.get_text(sel.get_start_iter(), sel.get_end_iter(), 0))

        #sel = self.run_javascript("document.getSelection();")
        #def completion(comp, user_data):
        #    print("sel=", comp)
        #    sel = comp
        #self.get_sel(completion, None)

    def on_select_font(self, action):
        dialog = Gtk.FontChooserDialog("Select a font")
        if dialog.run() == Gtk.ResponseType.OK:
            fname = dialog.get_font_desc().get_family()
            fsize = dialog.get_font_desc().get_size() / Pango.SCALE
            ttt = int(1 + round(fsize / 10)) % 9
            print("Setting font", fname, fsize, ttt)
            self.run_javascript("document.execCommand('fontname', null, '%s');" % fname)
            self.run_javascript("document.execCommand('fontsize', null, '%s');" % ttt)
        dialog.destroy()

    def on_select_color(self, action):
        dialog = Gtk.ColorChooserDialog("Select Color")
        if dialog.run() == Gtk.ResponseType.OK:
            (r, g, b, a) = dialog.get_rgba()
            color = "#%0.2x%0.2x%0.2x%0.2x" % (
                int(r * 255),
                int(g * 255),
                int(b * 255),
                int(a * 255))
            self.run_javascript("document.execCommand('forecolor', null, '%s');" % color)
        dialog.destroy()

    def on_select_bgcolor(self, action):
        dialog = Gtk.ColorChooserDialog("Select Background Color")
        if dialog.run() == Gtk.ResponseType.OK:
            (r, g, b, a) = dialog.get_rgba()
            color = "#%0.2x%0.2x%0.2x%0.2x" % (
                int(r * 255),
                int(g * 255),
                int(b * 255),
                int(a * 255))
            self.run_javascript("document.execCommand('backcolor', null, '%s');" % color)
        dialog.destroy()

    def on_edit_marker(self, action):
        print("on_edit_marker", action.get_name())

        c = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        sel = c.wait_for_targets()
        target = Gdk.Atom.intern ("text/html", True);
        ccc = c.wait_for_contents(target)
        print("sel", ccc.get_data())
        #ccc.free()
        htmlx = markdialog(ccc.get_data().decode())
        if htmlx:
            print("markdialog result:\n", htmlx)
            self.run_javascript("document.execCommand('insertHTML', null, '%s');" % htmlx)

    def on_insert_table(self, action):
        htmlx = "<table align=center border=0 contentEditable=true>" + \
                "<tr><td>TR1 C1 <td>| TR1 C2 <tr><td>TR2 C1<td>| TR2 C1</table><br>"

        #print("table", htmlx)
        self.run_javascript("document.execCommand('insertHTML', null, '%s');" % htmlx)

        #self.run_javascript("document.execCommand('insertHorizontalRule', null, null);")

    def on_insert_link(self, action):
        dialog = Gtk.Dialog("   Enter a URL:   ", None, 0,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        entry = Gtk.Entry()
        dialog.vbox.pack_start(Gtk.Label(" a "), False, False, 0)
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label(" x "), False, False, 0)
        hbox.pack_start(entry, False, False, 0)
        hbox.pack_start(Gtk.Label(" y "), False, False, 0)
        dialog.vbox.pack_start(hbox, False, False, 0)

        dialog.vbox.pack_start(Gtk.Label(" b "), False, False, 0)
        dialog.show_all()

        if dialog.run() == Gtk.ResponseType.OK:
            self.editor.run_javascript(
                "document.execCommand('createLink', True, '%s');" % entry.get_text())
        dialog.destroy()

    def on_insert_image(self, action):
        dialog = Gtk.FileChooserDialog("Select an image file", None, Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        if dialog.run() == Gtk.ResponseType.OK:
            fn = dialog.get_filename()
            if os.path.exists(fn):
                self.run_javascript(
                "document.execCommand('insertImage', null, '%s');" % fn)
        dialog.destroy()

    def on_open(self, action):
        dialog = Gtk.FileChooserDialog("Select an HTML file", self, Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        if dialog.run() == Gtk.ResponseType.OK:
            fn = dialog.get_filename()
            if os.path.exists(fn):
                self.filename = fn
                with open(fn) as fd:
                    self.load_html(fd.read(), "file:///")
        dialog.destroy()

    def on_save(self, action):
        def completion(html, user_data):
            open_mode = user_data
            with open(self.filename, open_mode) as fd:
                fd.write(html)

        if self.filename:
            self.get_html(completion, 'w')
        else:
            dialog = Gtk.FileChooserDialog("Select an HTML file", None,
                    Gtk.FileChooserAction.SAVE,
                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                            Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            if dialog.run() == Gtk.ResponseType.OK:
                self.filename = dialog.get_filename()
                print("Saving", self.filename)
                self.get_html(completion, "w+")
            dialog.destroy()

    def get_html(self, completion_function, user_data):

        #print("get_html")
        def javascript_completion(obj, result, user_data):
            #print("javascript_completion", result)
            fin = self.run_javascript_finish(result)
            #print("fin", fin)
            html = fin.get_js_value().to_string()
            #print("html", html, "\n")
            completion_function(html, user_data)
        self.run_javascript("document.title=document.documentElement.innerHTML;",
                                   None,
                                   javascript_completion,
                                   user_data)

# This is kicked in if  there is no

class pgwebw_fake(Gtk.VBox):

    def __init__(self):
        super(pgwebw_fake, self).__init__();
        pass

    def load_uri(self, url):
        pass


class   HtmlEdit(Gtk.VBox):

    def __init__(self, editable = False, statsetter = None):

        self.statsetter = statsetter
        self.editable = editable

        self._htmlx = pgwebw(editable)
        self.ui = generate_ui(self._htmlx)
        self.urlbar  = self.create_urlbar()
        self.toolbar = self.ui.get_widget("/toolbar_format")
        browse_scroll = Gtk.ScrolledWindow()
        browse_scroll.add(self._htmlx)
        self.pack_start(self.urlbar, False, False, 0)
        self.pack_start(self.toolbar, False, False, 0)
        self.pack_start(browse_scroll, 1, 1, 2)

    def get_view(self):
        return self._htmlx

    def url_callb(self):
        pass

    def backurl(self, url, parm, buff):
        self.webview.go_back()

    def baseurl(self, url, parm, buff):
        self.webview.load_uri("file://" + self.fname)

    def forwurl(self, url, parm, buff):
        self.webview.go_forward()

    def go(self, xstr):
        print("go", xstr)

        if not len(xstr):
            return

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

        self.webview.load_uri(xstr)

    def url_callb(self, xtxt):
        self.go(xtxt)


    def gourl(self, url, parm, buff):
        self.go(self.edit.get_text())

    def create_urlbar(self):

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

def generate_ui(self):

    ''' define toolbar items here '''

    ui_def = """
    <ui>
        <toolbar name="toolbar_format">
            <toolitem action="new" />
            <toolitem action="open" />
            <toolitem action="save" />
            <separator />
            <toolitem action="undo" />
            <toolitem action="redo" />
            <separator />
            <toolitem action="cut" />
            <toolitem action="copy" />
            <toolitem action="paste" />
            <separator />
            <toolitem action="removeformat" />
            <toolitem action="bold" />
            <toolitem action="italic" />
            <toolitem action="underline" />
            <toolitem action="strikethrough" />
            <separator />
            <toolitem action="font" />
            <toolitem action="fontsize" />
            <toolitem action="color" />
            <toolitem action="backgroundcolor" />
            <separator />
            <toolitem action="justifyleft" />
            <toolitem action="justifyright" />
            <toolitem action="justifycenter" />
            <toolitem action="justifyfull" />
            <separator />
            <toolitem action="insertimage" />
            <toolitem action="insertlink" />
            <toolitem action="inserttable" />
            <toolitem action="editmarker" />
        </toolbar>
    </ui>
    """

    actions = Gtk.ActionGroup("Actions")
    actions.add_actions([
    ("menuFile", None, "_File"),
    ("menuEdit", None, "_Edit"),
    ("menuInsert", None, "_Insert"),
    ("menuFormat", None, "_Format"),

    ("new", Gtk.STOCK_NEW, "_New", None, None, self.on_new),
    ("open", Gtk.STOCK_OPEN, "_Open", None, None, self.on_open),
    ("save", Gtk.STOCK_SAVE, "_Save", None, None, self.on_save),

    ("undo", Gtk.STOCK_UNDO, "_Undo", "<ctrl>Z", None, self.on_action),
    ("redo", Gtk.STOCK_REDO, "_Redo", None, None, self.on_action),

    ("cut", Gtk.STOCK_CUT, "_Cut", None, None, self.on_action),
    ("copy", Gtk.STOCK_COPY, "_Copy", None, None, self.on_action),
    ("paste", Gtk.STOCK_PASTE, "_Paste", None, None, self.on_paste),

    ("removeformat", Gtk.STOCK_PROPERTIES, "_removeFormat", "<ctrl>M", None, self.on_action),
    ("bold", Gtk.STOCK_BOLD, "_Bold", "<ctrl>B", None, self.on_action),
    ("italic", Gtk.STOCK_ITALIC, "_Italic", "<ctrl>I", None, self.on_action),
    ("underline", Gtk.STOCK_UNDERLINE, "_Underline", "<ctrl>U", None, self.on_action),
    ("strikethrough", Gtk.STOCK_STRIKETHROUGH, "_Strike", "<ctrl>T", None, self.on_action),
    ("font", Gtk.STOCK_SELECT_FONT, "Select _Font", "<ctrl>F", None, self.on_select_font),
    ("fontsize", None, "Select _Font", "<ctrl>F", None, self.on_fontsize),
    ("color", Gtk.STOCK_SELECT_COLOR, "Select _Color", None, None, self.on_select_color),
    ("backgroundcolor", Gtk.STOCK_COLOR_PICKER, "Select Back Color", None, None, self.on_select_bgcolor),

    ("justifyleft", Gtk.STOCK_JUSTIFY_LEFT, "Justify _Left", None, None, self.on_action),
    ("justifyright", Gtk.STOCK_JUSTIFY_RIGHT, "Justify _Right", None, None, self.on_action),
    ("justifycenter", Gtk.STOCK_JUSTIFY_CENTER, "Justify _Center", None, None, self.on_action),
    ("justifyfull", Gtk.STOCK_JUSTIFY_FILL, "Justify _Full", None, None, self.on_action),

    ("insertimage", "insert-image", "Insert _Image", None, None, self.on_insert_image),
    ("insertlink", "insert-link", "Insert _Link", None, None, self.on_insert_link),
    ("inserttable", "insert-table", "Insert _Table", None, None, self.on_insert_table),
    ("editmarker", "edit-marker", "edit _Marker", None, None, self.on_edit_marker),
    ])

    actions.get_action("insertimage").set_property("icon-name", "insert-image")
    actions.get_action("insertlink").set_property("icon-name", "insert-link")
    actions.get_action("inserttable").set_property("icon-name", "appointment-new")
    actions.get_action("editmarker").set_property("icon-name", "text-editor")
    actions.get_action("fontsize").set_property("icon-name", "preferences-desktop-font")
    actions.get_action("removeformat").set_property("icon-name", "text-direction")

    ui = Gtk.UIManager()
    ui.insert_action_group(actions)
    ui.add_ui_from_string(ui_def)

    #xxx = ui.get_toplevels(Gtk.UIManagerItemType.MENUBAR)
    xxx = ui.get_action_groups()[0].list_actions()
    for aa in xxx:
        nnn = aa.get_name()
        #print(nnn, aa.get_accel_path())
        aa.set_tooltip(nnn)

    return ui


def markdialog(sss):

    spaceneed = 64
    # Wrap tesxt if long
    ssss = ""
    cnt = 0; fff = 0
    for aa in sss:
        if cnt > spaceneed:
            fff = 1
        if fff and aa.isspace():
            cnt = 0; fff = 0
            ssss += "\n"
        ssss += aa
        cnt += 1

    dialog = Gtk.Dialog("   Edit markup   ", None, 0,
    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

    textview = Gtk.TextView()
    textview.set_editable(True)

    textbuffer = textview.get_buffer()
    textbuffer.set_text(ssss)

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)
    scrolledwindow.add(textview)
    scrolledwindow.set_size_request(640, 480)

    hhh = "\n          " \
            "In general, any valid html can go here. Keep it simple.\n" \
            "The editor already decorated this sufficiently, "\
              "try to edit existing items in place.\n"

    lll = Gtk.Label(hhh)
    fd = Pango.FontDescription("Sans 9")
    lll.override_font(fd)
    thbox = Gtk.HBox()
    thbox.pack_start(lll, 1, 1, 1)
    dialog.vbox.pack_start(thbox, False, False, 0)
    hbox = Gtk.HBox()
    hbox.pack_start(Gtk.Label(" "), False, False, 0)
    hbox.pack_start(scrolledwindow, 1, 1, 0)
    hbox.pack_start(Gtk.Label(" "), False, False, 0)
    dialog.vbox.pack_start(hbox, 1, 1, 0)
    #dialog.vbox.pack_start(Gtk.Label(" "), False, False, 0)
    dialog.show_all()

    htmlx = ""
    if dialog.run() == Gtk.ResponseType.OK:
        bi = textbuffer.get_start_iter()
        ei = textbuffer.get_end_iter()
        htmlx = textbuffer.get_text(bi, ei, False)

    dialog.destroy()

    # Unwrap it
    usss = ""
    cnt = 0; fff = 0
    for aa in htmlx:
        if aa == '\n':
            pass
        else:
            usss += aa
    return usss

def treecallb(ddd):
    global sizex
    #print("tree cb", ddd[0])
    sizex = ddd[0]

def sizedialog(sss):

    dialog = Gtk.Dialog("   Select Font Size   ", None, 0,
    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

    global sizex
    sizex = ""
    treedat = ["9", "10", "12", "14", "20", "24", "32", "48", "56", "64",
                    "70", "96", "128"]

    tree = SimpleTree(["Font Sizes"])
    for aa in treedat:
        tree.append((aa,))

    def actcallb(ddd):
        #print("Activate cb", ddd, dialog)
        dialog.response(Gtk.ResponseType.OK)
        #print("Activate cb2", ddd, dialog)

    tree.setcallb(treecallb)
    tree.setActcallb(actcallb)

    hhh = "\n          " \
            "In general, any valid html can go here. Keep it simple.\n" \
            "The editor already decorated this sufficiently, "\
              "try to edit existing items in place.\n"

    lll = Gtk.Label(hhh)
    fd = Pango.FontDescription("Sans 9")
    lll.override_font(fd)
    thbox = Gtk.HBox()
    thbox.pack_start(lll, 1, 1, 1)
    #dialog.vbox.pack_start(thbox, False, False, 0)

    hbox = Gtk.HBox()
    hbox.pack_start(Gtk.Label(" "), False, False, 0)
    hbox.pack_start(tree, 1, 1, 0)
    hbox.pack_start(Gtk.Label(" "), False, False, 0)
    dialog.vbox.pack_start(hbox, 1, 1, 0)
    #dialog.vbox.pack_start(Gtk.Label(" "), False, False, 0)
    dialog.show_all()

    if dialog.run() == Gtk.ResponseType.OK:
        #print("ok", sizex)
        pass
    else:
        sizex = 0

    dialog.destroy()
    return sizex

# EOF
