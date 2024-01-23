#Message on change fetches data from a website, and notifies the user when the data has changed.
#Copyright (C) 2024  Rūdolfs Driķis
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

from message_on_change.gui import Ui_MainWindow
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QFile
#from gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Hide the custom delay input box and add the switch visibility function
        self.ui.spinBox.hide()
        self.ui.spinBox.setEnabled(True)
        self.ui.checkBox_2.clicked.connect(lambda: self.toggle_widget_visibility(self.ui.checkBox_2, self.ui.spinBox))

        # Custom file input box toggle
        self.ui.pushButton_2.hide()
        self.ui.lineEdit_2.hide()
        self.ui.checkBox.clicked.connect(self.toggle_file_select_visibility)

        # file select logic
        self.ui.pushButton_2.clicked.connect(self.openFile)

    def toggle_widget_visibility(self, cb, widget):
        # Show or hide the widget based on the checkbox state
        if cb.isChecked():
            widget.show()
        else:
            widget.hide()

    def toggle_file_select_visibility(self):
        if self.ui.checkBox.isChecked():
            self.ui.pushButton_2.show()
            self.ui.lineEdit_2.show()
        else:
            self.ui.pushButton_2.hide()
            self.ui.lineEdit_2.hide()

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Sound File", "", "(*.wav *.mp3);;All Files (*)",
                                                   options=options)

        self.ui.lineEdit_2.setText(file_path)


#if __name__ == '__main__':
def main():
    print('something happened')
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
