import sys
import os
import os.path
from format_call import *
from PyQt5 import QtWidgets, QtGui
from PyQt5 import Qsci
from PyQt5 import QtCore


class TextEditorTab(QtWidgets.QTabWidget):
    def __init__(self):
        super(TextEditorTab, self).__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setUsesScrollButtons(True)
        self.tabCloseRequested.connect(self.closeTab)


    def closeTab(self, index):
        self.removeTab(index)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_GUI()
        self.filename = None


    def init_GUI(self):
        # ----------------------------------------------------------------------
        self.resize(700, 500)
        self.setWindowTitle('Editor')
        text = Qsci.QsciScintilla()
        self.text_setting(text)

        #initiate the tab widget
        self.tab_widget = TextEditorTab()

        # at start, one default tab
        self.tab_widget.addTab(text,'new')
        self.text = text
        self.setCentralWidget(self.tab_widget)

        self.statusBar()

        # COMMON ACTIONS--------------------------------------------------------
        exit_action = self.make_action(name='Exit',
                                        shortCut='Ctrl+Q',
                                        statusTip='Exit',
                                        callback=QtWidgets.qApp.quit)
        # TODO
        run_code_action = self.make_action(name='Run',
                                        shortCut='Ctrl+R',
                                        statusTip='Run Code',
                                        callback=self.run_code)

        # ADD TOOLBAR-----------------------------------------------------------
        self.toolBar = self.addToolBar('Exit')
        self.toolBar.addAction(exit_action)
        self.toolBar.addAction(run_code_action)

        # create menu bar-------------------------------------------------------
        menu_bar = self.menuBar()
        # create actions under file menu----------------------------------------
        file_actions = []
        file_actions.append(self.make_action(name='New',
                                        shortCut='Ctrl+N',
                                        statusTip='New File',
                                        callback=self.new_file))
        file_actions.append(self.make_action(name='Open File...',
                                        shortCut='Ctrl+O',
                                        statusTip='Open File',
                                        callback=self.open_file))
        file_actions.append(self.make_action(name='Save',
                                        shortCut='Ctrl+S',
                                        statusTip='Save File',
                                        callback=self.save_file))
        file_actions.append(self.make_action(name='Save As...',
                                        shortCut='Ctrl+Alt+S',
                                        statusTip='Save File As...',
                                        callback=self.save_as_file))
        file_actions.append(exit_action)



        file_menu = menu_bar.addMenu('File')
        file_menu.addActions(file_actions)

        # create actions under format menu--------------------------------------
        format_actions = []
        format_actions.append(self.make_action(name='Format Code',
                                        shortCut='Ctrl+Alt+F',
                                        statusTip='Format Code',
                                        callback=self.format_code))

        format_actions.append(self.make_action(name='Simplify Code',
                                        shortCut='Ctrl+Shift+S',
                                        statusTip='Simplify Code',
                                        callback=self.simplify_code))

        format_menu = menu_bar.addMenu('Format')
        format_menu.addActions(format_actions)


    def simplify_code(self):
        data = self.tab_widget.currentWidget().text()
        fileWriteObj = open('tempIn.txt', 'w')
        fileWriteObj.write(data)
        fileWriteObj.close()

        simplify('tempIn.txt', 'tempOut.txt')

        fileReadObj = open('tempOut.txt', 'r')
        data = fileReadObj.read()
        fileReadObj.close()

        os.remove('tempIn.txt')
        os.remove('tempOut.txt')
        self.tab_widget.currentWidget().setText(data)


    def format_code(self):
        data = self.tab_widget.currentWidget().text()
        fileWriteObj = open('tempIn.txt', 'w')
        fileWriteObj.write(data)
        fileWriteObj.close()

        format_called('tempIn.txt', 'tempOut.txt')

        fileReadObj = open('tempOut.txt', 'r')
        data = fileReadObj.read()
        fileReadObj.close()

        os.remove('tempIn.txt')
        os.remove('tempOut.txt')
        self.tab_widget.currentWidget().setText(data)


    def open_file(self):
        file_name = \
            QtWidgets.QFileDialog.getOpenFileName(self,
            'Open File',
             "D:\\code\\python\\qt_test\\codes_v2\\codes\\test_sample")

        if file_name[0] is '':
            return

        file = open(file_name[0], "r")

        self.filename = file_name[0]
        data = file.read()
        text = self.tab_widget.currentWidget()
        text.setText(data)
        self.setWindowTitle(self.filename)
        p, f = os.path.split(file_name[0])
        self.tab_widget.setTabText(self.tab_widget.currentIndex(),f)


    def new_file(self):
        if self.tab_widget.tabText(self.tab_widget.currentIndex()) is not 'new':
            text = Qsci.QsciScintilla()
            self.text_setting(text)
            self.tab_widget.addTab(text, 'new')
            self.tab_widget.setCurrentWidget(text)
            self.text = text # set the current text editor to be self.text
        else:
            return



    def save_as_file(self):
        file_name = QtWidgets.QFileDialog.getSaveFileName(self,
                                                    'Save as...',
                                                    'D:\\code\\python')
        try:
            fileWriteObj = open(file_name[0], 'w')
            data = self.text.text()
            fileWriteObj.write(data)
            fileWriteObj.close()
            self.filename = file_name[0]
            self.setWindowTitle(self.filename)
        except:
            return


    def save_file(self):
        if self.filename is None:
            file_name = QtWidgets.QFileDialog.getSaveFileName(self,
                                                        'Save File',
                                                        'D:\\code\\python')
            try:
                fileWriteObj = open(file_name[0], 'w')
                data = self.text.text()
                fileWriteObj.write(data)
                fileWriteObj.close()
                self.filename = file_name[0]
                self.setWindowTitle(self.filename)
            except:
                return
        else:
            data = self.text.text()
            fileWriteObj = open(self.filename, 'w')
            fileWriteObj.write(data)
            fileWriteObj.close()


    def text_setting(self, text):
        # set font
        font = QtGui.QFont()
        font.setFamily ('Consolas')
        font.setBold(True)
        font.setFixedPitch(True)
        font.setPointSize(12)

        # set lex
        lex = Qsci.QsciLexerCPP()
        lex.setFont(font)

        text.setLexer(lex)

        text.setTabWidth(4)
        text.setUtf8(True)

        text.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle)

        # set indentation
        text.setIndentationWidth(4)
        text.setIndentationGuides(True)
        text.setAutoIndent(True)
        text.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll);
        text.setAutoCompletionThreshold(3)

        # set brace matching
        text.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)

        # set Margins
        text.setMarginsFont(font)
        fontmetrics = QtGui.QFontMetrics(font)
        text.setMarginWidth(0, fontmetrics.width("00") + 6)
        text.setMarginLineNumbers(0, True)


    def make_action(self, name='CLICK', shortCut=None, statusTip='CLICK',\
                        callback=None):
        action = QtWidgets.QAction(name, self)
        if not shortCut is None:
            action.setShortcut(shortCut)

        if not statusTip is None:
            action.setStatusTip(statusTip)

        action.triggered.connect(callback)
        return action


    # TODO
	# To fellow coder:
	# if you press the "run" button on the main window, the function will be triggered.
    def run_code(self):
        pass

app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
