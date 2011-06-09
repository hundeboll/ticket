from PySide.QtCore import *
from PySide.QtGui import *

CARDNO = 0
STUDYNO = 1
NAME = 2

class Lookup(QWidget):
    def __init__(self, db, parent=None):
        super(Lookup, self).__init__(parent)
        self.db = db

        # Static text
        self.info_label = QLabel("<b>Member Info</b>")
        self.name_label = QLabel("Name:")
        self.tickets_label = QLabel("Tickets:")
        self.used_label = QLabel("Used:")

        # Variable text
        self.name = QLabel()
        self.tickets = QLabel()
        self.used = QLabel()

        layout = QGridLayout()
        layout.addWidget(self.info_label, 0, 0, 1, 2)
        layout.addWidget(self.name_label, 1, 0)
        layout.addWidget(self.tickets_label, 2, 0)
        layout.addWidget(self.used_label, 3, 0)
        layout.addWidget(self.name, 1, 1)
        layout.addWidget(self.tickets, 2, 1)
        layout.addWidget(self.used, 3, 1)
        self.setLayout(layout)

    def info(self, name, cardno=None, studyno=None):
        self.db.get_member_tickets(self.handle_tickets, self.handle_error, cardno, studyno)
        self.db.get_member_used(self.handle_used, self.handle_error, cardno, studyno)
        self.name.setText(name)

    def use(self, cardno=None, studyno=None):
        pass

    def handle_used(self, rows):
        used = len(rows)
        self.used.setText(str(used))

    def handle_tickets(self, rows):
        tickets = len(rows)
        self.tickets.setText(str(tickets))

    def handle_error(self, error):
        print "Lookup failed"


if __name__ == "__main__":
    app = QApplication([])
    lookup = Lookup()
    lookup.show()
    app.exec_()
