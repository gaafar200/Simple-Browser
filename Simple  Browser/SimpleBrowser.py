from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import os
import sys

                                                           #AboutDialog Inherits of QDialog
class AboutDialog(QDialog):                                # QDialog class is the base class of dialog windows.
    def __init__(self, *args, **kwargs):                   # __init__ method is at the core of OOP and is required to create objects ,the keyword self to bind the object’s attributes to the arguments received.
        super(AboutDialog, self).__init__(*args, **kwargs) #Calling the parent class's initialiser the keyword self to bind the object’s attributes to the arguments received.

        self.setStyleSheet("background-color:white")
        layout = QVBoxLayout()                           #QVBoxLayout class lines up widgets vertically

        title = QLabel("ECOM 4421: Computer Networks")
        font = title.font()
        font.setBold(True)
        font.setPointSize(25)
        title.setFont(font)
        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.jpg')))
        layout.addWidget(logo)

        title = QLabel(" Instructor: Dr. Aiman Abu Samra")
        font = title.font()
        font.setBold(True)
        font.setPointSize(20)
        title.setFont(font)
        layout.addWidget(title)

        title = QLabel("[1] Mohammed Abu Sido 120180586 "
                        "\n[2] Abdullah kamel Habib 120180587"
                        "\n[3] Mahmoud Mohamed Jafar 120180521"
                        "\n[4] Jafar Wael Jaafar 120180534"
                        "\n[5] Baraa Maher El Deeb 120180918" )
        font = title.font()
        font.setPointSize(10)
        title.setFont(font)
        layout.addWidget(title)


        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)                                    # Making document mode true.
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)  # Adding action when double clicked
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        file_menu = self.menuBar().addMenu("File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        help_menu = self.menuBar().addMenu("Help")
        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About Project", self)
        about_action.setStatusTip("Find out more about Project")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_Project_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "Dr.Aiman Homepage", self)
        navigate_Project_action.setStatusTip("Go to Dr.Aiman Homepage")
        navigate_Project_action.triggered.connect(self.navigate_Project)
        help_menu.addAction(navigate_Project_action)

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.show()

        self.setWindowTitle("IUG")
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))

    def add_new_tab(self, qurl=None, label="New Tab"):

        if qurl is None:
            qurl = QUrl('http://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() == 1:
            return
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s IUG" % title)

    def navigate_Project(self):
        self.tabs.currentWidget().setUrl(QUrl("http://site.iugaza.edu.ps/aasamra/"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")
        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Simple Browser")
app.setOrganizationName("Islamic University of Gaza")
app.setOrganizationDomain("https://www.iugaza.edu.ps/")

window = MainWindow()
app.exec_()
