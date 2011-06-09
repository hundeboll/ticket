from PySide.QtCore import *
from PySide.QtGui import *

header_data = ['Cardno', 'Studyno', 'Name', '', '']

class Search(QTableView):
    def __init__(self, db, lookup, parent=None):
        super(Search, self).__init__(parent)
        self.db = db
        self.lookup = lookup
        self.db.get_members(self.handle_members, self.handle_error)

    def handle_members(self, members):
        self.model = SearchModel(members)
        self.filter = QSortFilterProxyModel(self)
        self.filter.setDynamicSortFilter(True)
        self.filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.filter.setSourceModel(self.model)

        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setModel(self.filter)
        self.table_button = TableButton(self.lookup, len(members), self)
        self.setItemDelegateForColumn(3, self.table_button)
        self.setItemDelegateForColumn(4, self.table_button)

    def handle_error(self, error):
        print("Getting members failed")

    def set_search_column(self, column):
        self.filter.setFilterKeyColumn(column)

    def do_search(self, string):
        self.filter.setFilterFixedString(string)


class SearchInput(QTableWidget):
    def __init__(self, member_table, parent=None):
        super(SearchInput, self).__init__(parent)

        self.member_table = member_table

        self.setRowCount(1)
        self.setColumnCount(3)
        self.setFixedHeight(55)
        self.setSelectionMode(QAbstractItemView.NoSelection)


        self.init_editors()
        self.init_columns()
        self.header = self.horizontalHeader()
        self.header.sectionResized.connect(self.column_resized)
        self.setHorizontalHeaderLabels(header_data)
        self.verticalHeader().hide()

    def init_editors(self):
        self.editors = []
        for i in range(self.columnCount()):
            editor = QLineEdit()
            editor.textEdited.connect(self.handle_edit)
            editor.setStyleSheet("QLineEdit { border:none; }")
            editor.installEventFilter(self)
            self.editors.append(editor)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            column = self.editors.index(obj)
            index = QModelIndex()
            self.member_table.set_search_column(column)
            self.setCurrentIndex(index.sibling(0, column))

        return False

    def init_columns(self):
        # Store each column width for comparison in columnResized()
        self.column_widths = {}
        for column in range(self.columnCount()):
            self.setCellWidget(0, column, self.editors[column])
            self.column_widths[column] = self.columnWidth(column)

    def column_resized(self, **args):
        # Hack: args doesn't have column index or column width
        #       so we check if any column has new width
        for column in self.column_widths:
            column_width = self.columnWidth(column)
            if self.column_widths[column] != column_width:
                # Column width has changed
                self.member_table.setColumnWidth(column, column_width)
                self.column_widths[column] = column_width


    def handle_edit(self, text):
        self.member_table.do_search(text)


class TableButton(QStyledItemDelegate):
    def __init__(self, lookup, count, parent=None):
        super(TableButton, self).__init__(parent)
        self.lookup = lookup
        self.button_pressed = [[None, None, None, False, False]] * count

    def paint(self, painter, option, index):
        button_option = QStyleOptionButton()

        if index.column() == 3:
            button_option.text = "Info"
        elif index.column() == 4:
            button_option.text = "Let in"

        if self.button_pressed[index.row()][index.column()]:
            button_option.state = QStyle.State_Sunken | QStyle.State_Enabled
        else:
            button_option.state = QStyle.State_Raised | QStyle.State_Enabled

        button_option.rect = option.rect
        QApplication.style().drawControl(QStyle.CE_PushButton, button_option, painter, None)

    def sizeHint(self, option, index):
        return QSize(20, 20)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonPress:
            self.button_pressed[index.row()][index.column()] = True
            self.pressed(model, index.row())
        elif event.type() == QEvent.MouseButtonRelease:
            self.button_pressed[index.row()][index.column()] = False

        return True

    def pressed(self, model, row):
        cardno = model.data(model.index(row, 0))
        studyno = model.data(model.index(row, 1))
        name = model.data(model.index(row, 2))
        self.lookup.info(name, cardno, studyno)


class SearchModel(QAbstractTableModel):
    def __init__(self, members, parent=None):
        super(SearchModel, self).__init__(parent)
        self.members = members

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return None
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            # Row
            return section
        else:
            return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.members)

    def columnCount(self, parent=QModelIndex()):
        return len(header_data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 3:
                return None
            elif index.column() == 4:
                return None
            else:
                return self.members[index.row()][index.column()]
        else:
            return None
