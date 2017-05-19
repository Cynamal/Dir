#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk
import os

class Handler:

    def __init__(self):

        #zmienne wykorzystywane przez program
        self.gladefile = "schema.glade"
        self.command = ""
        self.text = ""
        self.parameters = ""
        self.location = " "
        self.activesetting = 0
        self.activeformat = 0
        self.name = ""
        self.sort = "/oN"
        self.state = [True, False, False, False, False]
        self.format = ""
        self.atributes = ""
        self.statec = [False, False, False, False, False, False]

        #stworzenie buildera, połączenie sygnałów
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)

        #deklaracja okien dialogowych
        self.window = self.builder.get_object("window1")
        self.opendialog = self.builder.get_object("filechooserdialog1")
        self.opendialog.set_transient_for(self.window)
        self.opendialog.set_destroy_with_parent(1)
        self.settingsdialog = self.builder.get_object("settingsdialog")
        self.settingsdialog.set_transient_for(self.window)
        self.settingsdialog.set_destroy_with_parent(1)
        self.errordialog = self.builder.get_object("errordialog")
        self.errordialog.set_transient_for(self.window)
        self.errordialog.set_destroy_with_parent(1)
        self.preferencedialog = self.builder.get_object("preferencedialog")
        self.preferencedialog.set_transient_for(self.window)
        self.preferencedialog.set_destroy_with_parent(1)
        self.aboutdialog = self.builder.get_object("aboutdialog")
        self.aboutdialog.set_transient_for(self.window)
        self.aboutdialog.set_destroy_with_parent(1)
        self.savedialog = self.builder.get_object("filechooserdialog2")
        self.savedialog.set_transient_for(self.window)
        self.savedialog.set_destroy_with_parent(1)

        #zawartość listy
        self.settingslist = gtk.ListStore(int, str)
        self.settingslist.append([0, "Białe tło i czarne znaki"])
        self.settingslist.append([1, "Czarne tło i białe znaki"])
        self.formatlist = gtk.ListStore(int, str)
        self.formatlist.append([0, "Domyślny"])
        self.formatlist.append([1, "Tylko nazwy katalogów"])
        self.formatlist.append([2, "Widoczni właściciele plików"])

        #deklaracja obiektow
        self.cell = gtk.CellRendererText()
        self.pathentry = self.builder.get_object("pathentry")
        self.errortext = self.builder.get_object("errortext")
        self.textview = self.builder.get_object("textview")
        self.buffer = self.builder.get_object("buffer")
        self.settingscombobox = self.builder.get_object("settingscombobox")
        self.settingscombobox.set_model(self.settingslist)
        self.settingscombobox.pack_start(self.cell, True)
        self.settingscombobox.add_attribute(self.cell, 'text', 1)
        self.settingscombobox.set_active(self.activesetting)
        self.displayformatcombobox = self.builder.get_object("displayformatcombobox")
        self.displayformatcombobox.set_model(self.formatlist)
        self.displayformatcombobox.pack_start(self.cell, True)
        self.displayformatcombobox.add_attribute(self.cell, 'text', 1)
        self.displayformatcombobox.set_active(self.activeformat)
        self.rb1 = self.builder.get_object("rb1")
        self.rb2 = self.builder.get_object("rb2")
        self.rb3 = self.builder.get_object("rb3")
        self.rb4 = self.builder.get_object("rb4")
        self.rb5 = self.builder.get_object("rb5")
        self.cb1 = self.builder.get_object("cb1")
        self.cb2 = self.builder.get_object("cb2")
        self.cb3 = self.builder.get_object("cb3")
        self.cb4 = self.builder.get_object("cb4")
        self.cb5 = self.builder.get_object("cb5")
        self.cb6 = self.builder.get_object("cb6")

        self.window.show()

    def gtk_main_quit(self, object):
        print "quit with cancel"
        gtk.main_quit()

    def on_save_clicked(self, button):
        print "save file"
        self.filename = self.savedialog.get_filename()
        if self.filename == None:
            print "show error log"
            self.errortext.set_text("Nie podano nazwy pliku!")
            self.errordialog.run()
        else:
            self.filename += ".txt"
            self.textfile = open(self.filename, "w")
            self.textfile.write("%s" % self.text)
            self.textfile.close()

    def on_closeapp_activate(self, menuitem):
        print "quit from menu"
        gtk.main_quit()

    def on_savefile_activate(self, menuitem):
        print "show save window"
        self.savedialog.run()

    def on_about_activate(self, menuitem):
        print "show about window"
        self.aboutdialog.run()

    def on_openpath_activate(self, menuitem):
        print "show selecting path window"
        self.opendialog.run()

    def on_settings_activate(self, menuitem):
        print "show settings window"
        self.settingscombobox.set_active(self.activesetting)
        self.settingsdialog.run()

    def on_cancelopenpath_clicked(self, button):
        print "cancel selecting path"

    def change_format(self, number):
        if number == 0:
            self.format = ""
        elif number == 1:
            self.format = "/b "
        elif number == 2:
            self.format = "/q "

    def on_acceptpreferences_clicked(self, button):
        print "change preferences"
        if not self.cb6.get_active():
            self.change_preferences()
        elif self.cb6.get_active() and (self.cb1.get_active() or self.cb2.get_active() or self.cb3.get_active()
                                      or self.cb4.get_active() or self.cb5.get_active()):
            self.change_preferences()
        else:
            print "show error log"
            self.errortext.set_text("Nie wybrano atrybutów do pominięcia!")
            self.errordialog.run()

    def change_preferences(self):
        self.formatmodel = self.displayformatcombobox.get_model()
        self.selectedformat = self.displayformatcombobox.get_active()
        self.activeformat = self.selectedformat
        self.change_format(int(self.formatmodel[self.selectedformat][0]))
        self.set_sorting()
        self.set_attributes()

    def set_attributes(self):
        if not self.cb1.get_active() and not self.cb2.get_active() and not self.cb3.get_active() and \
                not self.cb4.get_active() and not self.cb5.get_active() and not self.cb6.get_active():
            self.atributes = ""
        else:
            self.atributes = "/a"

        if self.cb6.get_active():
            self.atributes += "-"
            self.statec[5] = True
        else:
            self.statec[5] = False

        if self.cb1.get_active():
            self.atributes += "D"
            self.statec[0] = True
        else:
            self.statec[0] = False

        if self.cb2.get_active():
            self.atributes += "R"
            self.statec[1] = True
        else:
            self.statec[1] = False

        if self.cb3.get_active():
            self.atributes += "H"
            self.statec[2] = True
        else:
            self.statec[2] = False

        if self.cb4.get_active():
            self.atributes += "A"
            self.statec[3] = True
        else:
            self.statec[3] = False

        if self.cb5.get_active():
            self.atributes += "S"
            self.statec[4] = True
        else:
            self.statec[4] = False

        print self.atributes

    def on_cancelpreferences_clicked(self, button):
        print "cancel selecting preferences"

    def on_selectpath_clicked(self, button):
        print "path selected"
        self.location = self.opendialog.get_filename()
        if self.location is None:
            print "show error log"
            self.errortext.set_text("Nie wybrano ścieżki!")
            self.errordialog.run()
        else:
            self.pathentry.set_text(self.location)

    def on_filechooserdialog1_response(self, object, data=None):
        print "hide selecting path window"
        self.opendialog.hide()

    def on_filechooserdialog2_response(self, object, data=None):
        print "hide save window"
        self.savedialog.hide()

    def on_aboutdialog_response(self, object, data=None):
        print "hide about window"
        self.aboutdialog.hide()

    def on_clearall_activate(self, menuitem):
        print "clear area"
        self.pathentry.set_text("")
        self.buffer.set_text("")
        self.text = ""
        self.textview.set_buffer(self.buffer)

    def on_preferences_activate(self, menuitem):
        print 'show preference dialog'
        self.rb1.set_active(self.state[0])
        self.rb2.set_active(self.state[1])
        self.rb3.set_active(self.state[2])
        self.rb4.set_active(self.state[3])
        self.rb5.set_active(self.state[4])
        self.cb1.set_active(self.statec[0])
        self.cb2.set_active(self.statec[1])
        self.cb3.set_active(self.statec[2])
        self.cb4.set_active(self.statec[3])
        self.cb5.set_active(self.statec[4])
        self.cb6.set_active(self.statec[5])
        self.displayformatcombobox.set_active(self.activeformat)
        self.preferencedialog.run();

    def on_cancelsettings_clicked(self, button):
        print "cancel changing settings"

    def on_settingsdialog_response(self, object, data=None):
        print "hide settings window"
        self.settingsdialog.hide()

    def on_errordialog_response(self, object, data=None):
        print "hide error dialog"
        self.errordialog.hide()

    def on_acceptsettings_clicked(self, button):
        print "changed settings"
        self.settingsmodel = self.settingscombobox.get_model()
        self.selectedsetting = self.settingscombobox.get_active()
        self.activesetting = self.selectedsetting
        self.change_textarea(int(self.settingsmodel[self.selectedsetting][0]))

    def change_textarea(self, number):
        if number == 1:
            self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            self.textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        else:
            self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
            self.textview.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))

    def get_values(self):
        self.location = self.pathentry.get_text()
        self.parameters = self.format + self.sort + self.atributes

    def on_preferencedialog_response(self, object, data=None):
        print "hide preference dialog"
        self.preferencedialog.hide()

    def check_location(self):
        if self.location and self.location.strip():
            return True
        else:
            print "show error log"
            self.errortext.set_text("Nie podano ścieżki!")
            self.errordialog.run()
            return False

    def location_is_dir(self):
        if os.path.isdir(self.location):
            return True
        if not os.path.exists(self.location):
            print "show error log"
            self.errortext.set_text("Podana ścieżka nie istnieje!")
            self.errordialog.run()
            return False
        else:
            print "show error log"
            self.errortext.set_text("Podana ścieżka nie prowadzi do katalogu!")
            self.errordialog.run()
            return False

    def on_executedir_clicked(self, button):
        self.get_values()
        if self.check_location() and self.location_is_dir():
            self.command = "dir " + self.location + " " + self.parameters
            self.text = os.popen(self.command).read()
            self.text = unicode(self.text, errors='ignore')
            print "execute DIR command"
            print self.text
            self.buffer.set_text(self.text)
            self.textview.set_buffer(self.buffer)

    def set_sorting(self):
        print "selected sort type"
        self.sort = "/o"
        self.state[0] = self.rb1.get_active()
        self.state[1] = self.rb2.get_active()
        self.state[2] = self.rb3.get_active()
        self.state[3] = self.rb4.get_active()
        self.state[4] = self.rb5.get_active()
        if self.rb1.get_active():
            self.sort += "N "
        elif self.rb2.get_active():
            self.sort += "S "
        elif self.rb3.get_active():
            self.sort += "E "
        elif self.rb4.get_active():
            self.sort += "D "
        elif self.rb5.get_active():
            self.sort += "G "
        else:
            self.sort = ""
        print self.sort

if __name__ == "__main__":
  main = Handler()
  gtk.main()