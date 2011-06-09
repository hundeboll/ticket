from PySide.QtCore import *
from PySide.QtGui import *

class Events(QWidget):
    def __init__(self, db, parent=None):
        super(Events, self).__init__(parent)
        self.db = db

        self.layout = QGridLayout()
        self.add_widgets()
        self.setLayout(self.layout)

        db.get_events(self.handle_events, self.handle_events_error)
        self.event_list.currentIndexChanged[int].connect(self.handle_select)

    def add_widgets(self):
        self.event_title = QLabel("<b>Event info</b>")
        self.event_list_label = QLabel("Event:")
        self.event_tickets_label = QLabel("Tickets:")
        self.event_sold_label = QLabel("Sold:")
        self.event_used_label = QLabel("Used:")

        # Dynamic Text
        self.event_list = QComboBox()
        self.event_tickets = QLabel()
        self.event_sold = QLabel()
        self.event_used = QLabel()

        # Static Text
        self.layout.addWidget(self.event_title, 0, 0, 1, 2)
        self.layout.addWidget(self.event_list_label, 1, 0)
        self.layout.addWidget(self.event_tickets_label, 2, 0)
        self.layout.addWidget(self.event_sold_label, 3, 0)
        self.layout.addWidget(self.event_used_label, 4, 0)

        # Dynamic Text
        self.layout.setColumnMinimumWidth(0, 80)
        self.layout.addWidget(self.event_list, 1, 1)
        self.layout.addWidget(self.event_tickets, 2, 1)
        self.layout.addWidget(self.event_sold, 3, 1)
        self.layout.addWidget(self.event_used, 4, 1)

    def handle_select(self, index):
        event = self.event_list.itemData(index)
        self.db.set_event(event)
        self.db.get_event_info(self.handle_event_info, self.handle_event_info_error)
        self.db.get_event_used(self.handle_event_used, self.handle_event_used_error)

    def handle_events(self, events):
        self.event_list.addItem("Select event", None)
        for event in events:
            self.event_list.addItem(event[1], event[0])

    def handle_events_error(self, error):
        print("Getting events failed")

    def handle_event_info(self, infos):
        tickets = 0
        sold = 0
        for info in infos:
            tickets = info[0]
            sold = info[1]
            break

        self.event_tickets.setText(str(int(tickets)))
        self.event_sold.setText(str(int(sold)))

    def handle_event_info_error(self, error):
        print("Getting event info failed")

    def handle_event_used(self, rows):
        used = 0
        for row in rows:
            used = row[0]

        self.event_used.setText(str(int(used)))

    def handle_event_used_error(self, error):
        print("Getting event used failed")


if __name__ == "__main__":
    app = QApplication([])
    events = Events()
    events.show()
    app.exec_()
