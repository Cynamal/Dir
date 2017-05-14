#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk

class Handler:

    def __init__(self):
        self.gladefile = "schema.glade"
        # signal_dictionary = {"on_button_clicked": self.button_clicked,
        #                     "gtk_main_quit": self.main_quit}
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window1")
        self.window.show()

    def gtk_main_quit(self, object, data=None):
        print "quit with cancel"
        gtk.main_quit()

    def on_gtk_quit_activate(self, menuitem, data=None):
        print "quit from menu"
        gtk.main_quit()

if __name__ == "__main__":
  main = Handler()
  gtk.main()