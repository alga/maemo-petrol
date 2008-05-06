#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade
import decimal
import datetime


class MaemoPetrol(object):

    def __init__(self):
        self.tree = gtk.glade.XML("maemo-petrol.glade")
        self.tree.signal_autoconnect(self)

        self.fill_list = self.tree.get_widget("fill_list")
        self.fill_store = gtk.TreeStore(str, int, float, str, str)
        self.fill_list.set_model(self.fill_store)

        column = gtk.TreeViewColumn("Car", gtk.CellRendererText(), text=0)
        self.fill_list.append_column(column)

        column = gtk.TreeViewColumn("Mileage", gtk.CellRendererText(), text=1)
        self.fill_list.append_column(column)

        column = gtk.TreeViewColumn("Litres", gtk.CellRendererText(), text=2)
        self.fill_list.append_column(column)

        column = gtk.TreeViewColumn("Price", gtk.CellRendererText(), text=3)
        self.fill_list.append_column(column)

        column = gtk.TreeViewColumn("Date", gtk.CellRendererText(), text=4)
        self.fill_list.append_column(column)

        self.add_dialog = self.tree.get_widget("add_window")

        self.last_edited = None

    #
    # Add form properties
    #

    @property
    def car(self):
        return self.tree.get_widget("car").get_active_text()


    @property
    def odometer(self):
        return self.tree.get_widget("odometer").get_value_as_int()

    @property
    def sum(self):
        return self.tree.get_widget("sum").get_value()

    @property
    def volume(self):
        return self.tree.get_widget("volume").get_value()

    @property
    def date(self):
        y, m, d = self.tree.get_widget("date").get_date()
        m += 1
        return datetime.date(y, m, d)

    @property
    def ppu(self):
        return self.tree.get_widget("ppu").get_value()


    #
    # Event handlers
    #
    def quit(self, *args):
        gtk.main_quit()

    def add_handler(self, event):
        self.add_dialog.show()

    def add_cancel_handler(self, event):
        self.add_dialog.hide()

    def add_ok_handler(self, event):
        self.fill_store.append(None, [self.car, self.odometer, self.volume,
                                      "%.2f" % self.sum,
                                      self.date.strftime("%Y-%m-%d")])

        self.add_dialog.hide()

    def add_volume_changed(self, event):
        if self.last_edited == 'sum':
            self.tree.get_widget("sum").set_value(self.volume * self.ppu)
        else:
            self.tree.get_widget("ppu").set_value(self.sum / self.volume)
        self.last_edited = 'volume'

    def add_ppu_changed(self, event):
        if not self.last_edited == 'sum':
            self.tree.get_widget("sum").set_value(self.volume * self.ppu)
        else:
            self.tree.get_widget("volume").set_value(self.sum / self.ppu)
        self.last_edited = 'ppu'

    def add_sum_changed(self, event):
        if not self.last_edited == 'volume':
            self.tree.get_widget("volume").set_value(self.sum / self.ppu)
        else:
            self.tree.get_widget("ppu").set_value(self.sum / self.volume)
        self.last_edited = 'sum'


def main():
    m = MaemoPetrol()
    try:
        gtk.main()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

