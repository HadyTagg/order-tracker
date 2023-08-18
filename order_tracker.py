from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import sqlite3


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.show()
        self.create_table()
        self.load_data()

        self.archived_orders_dialog = None

        self.add_order_button.clicked.connect(self.add_order)
        self.edit_order_button.clicked.connect(self.edit_order)
        self.update_order_status_button.clicked.connect(self.update_order_status)
        self.archive_order_button.clicked.connect(self.archive_order)
        self.archived_orders_button.clicked.connect(self.archived_orders)
        self.update_notes_button.clicked.connect(self.update_notes)
        self.main_table.cellClicked.connect(self.show_notes)
        self.main_table.itemSelectionChanged.connect(self.clear_notes)

    @staticmethod
    def create_table():
        conn = sqlite3.connect('order_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS orders
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     DATE TEXT, 
                     OWNER TEXT, 
                     ITEM TEXT,
                     DESCRIPTION TEXT,
                     QUANTITY TEXT,
                     STATUS TEXT, 
                     ARCHIVED INTEGER, 
                     NOTES TEXT)''')
        conn.commit()
        conn.close()

    def load_data(self):
        self.main_table.clearContents()
        self.main_table.setRowCount(0)

        conn = sqlite3.connect('order_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders WHERE archived = 0")
        table_data = c.fetchall()

        for item in table_data:
            row_position = self.main_table.rowCount()
            self.main_table.insertRow(row_position)
            self.main_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.main_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.main_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.main_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.main_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(item[4]))
            self.main_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(item[5]))
            self.main_table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(item[6]))

        conn.close()

        self.main_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.main_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        green = QtGui.QColor(0, 255, 0)
        red = QtGui.QColor(255, 0, 0)

        for row in range(self.main_table.rowCount()):
            status_item = self.main_table.item(row, 6)
            if status_item.text() == "Complete":
                for col in range(self.main_table.columnCount()):
                    cell = self.main_table.item(row, col)
                    cell.setBackground(green)
            elif status_item.text() == "Outstanding":
                for col in range(self.main_table.columnCount()):
                    cell = self.main_table.item(row, col)
                    cell.setBackground(red)

    def load_archived_data(self):
        self.archived_orders_dialog.archived_table.clearContents()
        self.archived_orders_dialog.archived_table.setRowCount(0)

        conn = sqlite3.connect('order_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders WHERE archived = 1")
        archived_table_data = c.fetchall()
        for item in archived_table_data:
            row_position = self.archived_orders_dialog.archived_table.rowCount()
            self.archived_orders_dialog.archived_table.insertRow(row_position)
            self.archived_orders_dialog.archived_table.setItem(row_position, 0,
                                                               QtWidgets.QTableWidgetItem(str(item[0])))
            self.archived_orders_dialog.archived_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(item[1]))
            self.archived_orders_dialog.archived_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(item[2]))
            self.archived_orders_dialog.archived_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(item[3]))
            self.archived_orders_dialog.archived_table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(item[4]))
            self.archived_orders_dialog.archived_table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(item[5]))
            self.archived_orders_dialog.archived_table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(item[6]))

        conn.close()

        green = QtGui.QColor(0, 255, 0)
        red = QtGui.QColor(255, 0, 0)

        for row in range(self.archived_orders_dialog.archived_table.rowCount()):
            status_item = self.archived_orders_dialog.archived_table.item(row, 6)
            if status_item.text() == "Complete":
                for col in range(self.archived_orders_dialog.archived_table.columnCount()):
                    cell = self.archived_orders_dialog.archived_table.item(row, col)
                    cell.setBackground(green)
            elif status_item.text() == "Outstanding":
                for col in range(self.archived_orders_dialog.archived_table.columnCount()):
                    cell = self.archived_orders_dialog.archived_table.item(row, col)
                    cell.setBackground(red)

        self.archived_orders_dialog.archived_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.archived_orders_dialog.archived_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def add_order(self):
        add_order_dialog = QtWidgets.QDialog(self)
        uic.loadUi('add_order_window.ui', add_order_dialog)

        if add_order_dialog.exec_() == QtWidgets.QDialog.Accepted:
            owner_combo_box = add_order_dialog.findChild(QtWidgets.QComboBox, 'owner_combo_box').currentText()
            item_edit = add_order_dialog.findChild(QtWidgets.QTextEdit, 'item_edit').toPlainText()
            description_combo_box = add_order_dialog.findChild(QtWidgets.QComboBox,
                                                               'description_combo_box').currentText()
            quantity_spin_box = add_order_dialog.findChild(QtWidgets.QDoubleSpinBox, 'quantity_spin_box').value()
            status_combo_box = add_order_dialog.findChild(QtWidgets.QComboBox, 'status_combo_box').currentText()
            if not owner_combo_box or not item_edit or not description_combo_box or not quantity_spin_box \
                    or not status_combo_box or len(item_edit.strip()) < 1:
                QtWidgets.QMessageBox.critical(add_order_dialog, "Error", "Please fill in all required fields")
                self.load_data()
                return None
            conn = sqlite3.connect('order_data.db')
            c = conn.cursor()
            c.execute(
                "INSERT INTO orders (DATE, OWNER, ITEM, DESCRIPTION, QUANTITY, STATUS, ARCHIVED, NOTES) VALUES (?, ?, "
                "?, ?, ?, ?, ?, ?)",
                (QtCore.QDate.currentDate().toPyDate(), owner_combo_box, item_edit, description_combo_box,
                 quantity_spin_box, status_combo_box, 0, ''))
            conn.commit()
            conn.close()
            self.load_data()
        else:
            QtWidgets.QMessageBox.warning(add_order_dialog, "Warning", "Order Cancelled")

    def edit_order(self):
        if self.verify():
            selected_items = self.main_table.selectedItems()
            if len(selected_items) == 0:
                QtWidgets.QMessageBox.critical(self, "Error", "No order is currently selected")
            else:
                current_row = self.main_table.currentRow()
                selected_order_id = self.main_table.item(current_row, 0).text()
                conn = sqlite3.connect('order_data.db')
                c = conn.cursor()
                c.execute(f"SELECT * FROM Orders WHERE ID = {selected_order_id}")
                data = c.fetchone()
                conn.close()

                edit_order_dialog = QtWidgets.QDialog(self)
                uic.loadUi('edit_order_window.ui', edit_order_dialog)

                edit_order_dialog.findChild(QtWidgets.QComboBox, 'status_combo_box').setCurrentText(data[6])
                edit_order_dialog.findChild(QtWidgets.QDoubleSpinBox, 'quantity_spin_box').setValue(float(data[5]))
                edit_order_dialog.findChild(QtWidgets.QComboBox, 'owner_combo_box').setCurrentText(data[2])
                edit_order_dialog.findChild(QtWidgets.QComboBox, 'description_combo_box').setCurrentText(data[4])
                edit_order_dialog.findChild(QtWidgets.QTextEdit, 'item_edit').setText(data[3])

                if edit_order_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    item_edit = edit_order_dialog.findChild(QtWidgets.QTextEdit, 'item_edit').toPlainText()
                    description_combo_box = edit_order_dialog.findChild(QtWidgets.QComboBox, 'description_combo_box')\
                        .currentText()
                    quantity_spin_box = edit_order_dialog.findChild(QtWidgets.QDoubleSpinBox, 'quantity_spin_box')\
                        .value()
                    if not item_edit or len(item_edit.strip()) < 1:
                        QtWidgets.QMessageBox.critical(edit_order_dialog, "Error", "Please fill in all required fields")
                        self.load_data()
                        return None
                    conn = sqlite3.connect('order_data.db')
                    c = conn.cursor()
                    c.execute("UPDATE orders SET ITEM = ?, DESCRIPTION = ?, QUANTITY = ? WHERE ID = ?",
                              (item_edit, description_combo_box, quantity_spin_box, selected_order_id))
                    conn.commit()
                    conn.close()
                    self.load_data()
                else:
                    QtWidgets.QMessageBox.warning(edit_order_dialog, "Warning", "Edit cancelled")

    def update_order_status(self):
        selected_items = self.main_table.selectedItems()
        if len(selected_items) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "No order is currently selected")
        else:
            current_row = self.main_table.currentRow()
            selected_order_id = self.main_table.item(current_row, 0).text()
            selected_status = self.main_table.item(current_row, 6).text()

            # Toggle the status from "Complete" to "Outstanding" and vice versa
            new_status = "Outstanding" if selected_status == "Complete" else "Complete"

            conn = sqlite3.connect('order_data.db')
            c = conn.cursor()
            c.execute("UPDATE orders SET STATUS = ? WHERE ID = ?", (new_status, selected_order_id))
            conn.commit()
            conn.close()

            self.load_data()

    def archive_order(self):
        selected_items = self.main_table.selectedItems()
        if len(selected_items) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "No order is currently selected")
        else:
            current_row = self.main_table.currentRow()
            selected_order_id = self.main_table.item(current_row, 0).text()
            conn = sqlite3.connect('order_data.db')
            c = conn.cursor()
            c.execute("UPDATE orders SET ARCHIVED = ? WHERE id = ?", (1, selected_order_id))
            conn.commit()
            conn.close()
            self.load_data()

    def archived_orders(self):
        self.archived_orders_dialog = QtWidgets.QDialog(self)
        uic.loadUi('archived_orders_window.ui', self.archived_orders_dialog)
        self.load_archived_data()
        self.archived_orders_dialog.archived_table.cellClicked.connect(self.show_archived_notes)
        self.archived_orders_dialog.current_orders_button.clicked.connect(self.current_orders)
        self.archived_orders_dialog.unarchive_order_button.clicked.connect(self.unarchive_order)
        self.archived_orders_dialog.archived_table.itemSelectionChanged.connect(self.clear_archived_notes)
        self.archived_orders_dialog.exec_()
        self.load_data()

    def update_notes(self):
        selected_items = self.main_table.selectedItems()
        if len(selected_items) == 0:
            QtWidgets.QMessageBox.critical(self, "Error", "No order is currently selected")
        else:
            current_row = self.main_table.currentRow()
            selected_order_id = self.main_table.item(current_row, 0).text()
            updated_notes = self.findChild(QtWidgets.QTextEdit, 'notes_edit').toPlainText()
            conn = sqlite3.connect('order_data.db')
            c = conn.cursor()
            c.execute("UPDATE orders SET notes = ? WHERE id = ?", (updated_notes, selected_order_id))
            conn.commit()
            conn.close()
            self.findChild(QtWidgets.QTextEdit, 'notes_edit').clear()
            self.load_data()

    def unarchive_order(self):
        selected_items = self.archived_orders_dialog.archived_table.selectedItems()
        if len(selected_items) == 0:
            QtWidgets.QMessageBox.critical(self.archived_orders_dialog, "Error", "No order is currently selected")
        else:
            current_row = self.archived_orders_dialog.archived_table.currentRow()
            selected_order_id = self.archived_orders_dialog.archived_table.item(current_row, 0).text()
            conn = sqlite3.connect('order_data.db')
            c = conn.cursor()
            c.execute("UPDATE orders SET ARCHIVED = ? WHERE id = ?", (0, selected_order_id))
            conn.commit()
            conn.close()
            self.load_archived_data()

    def current_orders(self):
        self.archived_orders_dialog.close()
        self.load_data()

    def show_notes(self):
        current_row = self.main_table.currentRow()
        selected_order_id = self.main_table.item(current_row, 0).text()
        conn = sqlite3.connect('order_data.db')
        c = conn.cursor()
        c.execute(f"SELECT NOTES FROM Orders WHERE ID = {selected_order_id}")
        notes = c.fetchone()
        self.findChild(QtWidgets.QTextEdit, 'notes_edit').setText(notes[0])
        conn.close()

    def show_archived_notes(self):
        current_row = self.archived_orders_dialog.archived_table.currentRow()
        selected_order_id = self.archived_orders_dialog.archived_table.item(current_row, 0).text()
        conn = sqlite3.connect('order_data.db')
        c = conn.cursor()
        c.execute(f"SELECT NOTES FROM Orders WHERE ID = {selected_order_id}")
        notes = c.fetchone()
        self.findChild(QtWidgets.QTextEdit, 'archived_notes_edit').setText(notes[0])
        conn.close()

    def clear_notes(self):
        if not self.main_table.selectedIndexes():
            self.notes_edit.clear()

    def clear_archived_notes(self):
        if not self.archived_orders_dialog.archived_table.selectedIndexes():
            self.archived_orders_dialog.archived_notes_edit.clear()

    def verify(self):
        password_dialog = QtWidgets.QDialog(self)
        uic.loadUi('verify_window.ui', password_dialog)

        if password_dialog.exec_() == QtWidgets.QDialog.Accepted:
            password = password_dialog.findChild(QtWidgets.QLineEdit, "password_line_edit").text()
            if password == "ilovehady":
                return True
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "Incorrect password")
                return False
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Verification cancelled")
            return False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
