#!/usr/bin/env python2

import sys, os
from PySide.QtCore import *
from PySide.QtGui import *

app = QApplication(sys.argv)
import libticket as ticket

class Ticket(QMainWindow):
    def __init__(self, parent=None):
        super(Ticket, self).__init__(parent)

        self.config = ticket.Config()
        self.db = ticket.Db(self.config.db_type, self.config.db_host, self.config.db_user, self.config.db_pass, self.config.db_winkas, self.config.db_ticket)

        central_widget = QWidget(self)
        grid_layout = QGridLayout(central_widget)
        self.events = ticket.Events(self.db, central_widget)
        self.lookup = ticket.Lookup(self.db, central_widget)
        self.search = ticket.Search(self.db, self.lookup, central_widget)
        self.search_input = ticket.SearchInput(self.search, central_widget)

        grid_layout.addWidget(self.events, 0, 0)
        grid_layout.addWidget(self.lookup, 0, 1)
        grid_layout.addWidget(self.search_input, 1, 0, 1, 2)
        grid_layout.addWidget(self.search, 2, 0, 1, 2)


        self.setCentralWidget(central_widget)
        self.resize(QSize(800, 600))
        self.show()

    def about_to_quit(self):
        print("Quitting")
        self.db.stop()


if __name__ == "__main__":
    ticket = Ticket()
    app.aboutToQuit.connect(ticket.about_to_quit)
    app.exec_()

    from subprocess import call
    call(["kill", "-9", str(os.getpid())])
