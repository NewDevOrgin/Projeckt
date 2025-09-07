from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
import shutil
import sys
import os

try:
    with open("conf.txt", "r") as c:
        project_directory = c.read()
        c.close()
except:
    pass

def read_projects(directory_path):
    folders = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders

def create_project(template, project_name):
    cwd = f"{project_directory}/{project_name}"
    if os.path.exists(cwd):
        QMessageBox.critical(None, "Project already exists!", "The project you are trying to create already exists!")
        return
    os.mkdir(cwd)

    with open(f"{template}.prt", "r") as t:
        template_contents = t.readlines()

    for cmd in template_contents:
        subprocess.run(cmd, shell=True, cwd=cwd)
    
    with open(f"{cwd}/.projeckt", "w+") as f:
        f.write(project_name)

class Project_Item():
    def __init__(self, title):
        self.frame = QWidget()
        self.frame.setObjectName("Frame")
        self.frame.setMaximumHeight(50)

        self.title = QLabel(title)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.title)

        self.frame.setLayout(self.layout)
    
    def select_me(self):
        self.selected.emit(i)

class Dialog():
    def __init__(self, template):
        self.template = template

        self.window = QWidget()
        self.window.setObjectName("Frame")
        self.window.setWindowFlag(Qt.FramelessWindowHint, True)
        self.window.resize(200, 100)
        self.center()

        self.layout = QVBoxLayout()
        self.top_bar = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.title = QLabel()
        self.close_btn = QPushButton()
        self.close_btn.setMaximumWidth(30)
        self.close_btn.setIcon(Icon_Close)
        self.close_btn.clicked.connect(self.window.close)

        self.top_bar.addWidget(self.title)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.close_btn)

        self.input_1 = QLineEdit()
        self.input_2 = QLineEdit() 
        self.ok_btn = QPushButton()
        self.ok_btn.setIcon(Icon_Check)

        self.layout.addLayout(self.top_bar)
        self.layout.addWidget(self.input_1)
        self.layout.addLayout(self.bottom_layout)

        if self.template == "new":
            self.title.setText("New Project")
            self.input_1.setPlaceholderText("Project Name")
            self.input_2.setPlaceholderText("Template name")
            self.bottom_layout.addWidget(self.input_2)

        elif self.template == "conf":
            self.title.setText("Please enter the path to your projects folder!!!")
            self.input_1.setPlaceholderText("Path")
        
        elif self.template == "delete":
            self.title.setText("Please enter the project name to delete")
            self.input_1.setPlaceholderText("Project Name")
        
        self.bottom_layout.addWidget(self.ok_btn)
        self.window.setLayout(self.layout)

        self.ok_btn.clicked.connect(self.clicked)
    
    def show(self):
        self.window.show()
    
    def clicked(self):
        if self.template == "new":
            self.window.close()
            create_project(self.input_2.text(), self.input_1.text())

        elif self.template == "conf":
            self.window.close()
            with open("conf.txt", "w+") as c:
                c.write(self.input_1.text())
                c.close()
        
        elif self.template == "delete":
            if os.path.exists("conf.txt"):
                self.window.close()

                reply = QMessageBox.question(None, "Do you want to proceed?", "⚠️ Warning: This is irreversible, so be careful!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
                if reply == QMessageBox.StandardButton.Yes:
                    QMessageBox.warning(None, "You chose this!", "You are responsible for what you have done!")
                else:
                    return
                try:
                    shutil.rmtree(f"{project_directory}/{self.input_1.text()}")
                except Exception as e:
                    QMessageBox.critical(None, "Not Deleted!", f"Error: {e}")

    def center(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.window.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.window.move(window_geometry.topLeft())
        
class App():

    def __init__(self):

        self.no_conf = Dialog("conf")
        self.new_project = Dialog("new")
        self.delete_project = Dialog("delete")

        self.window = QWidget()
        self.window.setWindowFlag(Qt.FramelessWindowHint, True)
        self.window.resize(800, 500)
        self.center()

        self.layout = QVBoxLayout()
        self.top_bar = QHBoxLayout()
        self.main_layout = QHBoxLayout()

        self.new_project_btn = QPushButton()
        self.new_project_btn.setMaximumWidth(30)
        self.new_project_btn.setIcon(Icon_New)
        self.new_project_btn.clicked.connect(self.new_project.show)

        self.delete_project_btn = QPushButton()
        self.delete_project_btn.setMaximumWidth(30)
        self.delete_project_btn.setIcon(Icon_Delete)
        self.delete_project_btn.clicked.connect(self.delete_project.show)

        self.close_btn = QPushButton()
        self.close_btn.setMaximumWidth(30)
        self.close_btn.setIcon(Icon_Close)
        self.close_btn.clicked.connect(self.window.close)

        self.top_bar.addWidget(self.new_project_btn)
        self.top_bar.addWidget(self.delete_project_btn)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.close_btn)

        self.project_browser = QWidget()
        self.project_browser.setObjectName("Frame")
        
        self.project_browser_layout = QVBoxLayout()
        self.project_browser.setLayout(self.project_browser_layout)

        self.project_browser_scroll = QScrollArea()
        self.project_browser_scroll.setWidget(self.project_browser)
        self.project_browser.setLayout(self.project_browser_layout)

        self.main_layout.addWidget(self.project_browser)

        self.layout.addLayout(self.top_bar)
        self.layout.addLayout(self.main_layout)
        self.window.setLayout(self.layout)

        self.time = QTimer(self.window)
        self.time.timeout.connect(self.update_browser)
        self.time.start(3000)

    def update_browser(self):
        if os.path.exists("conf.txt"):
            folders = read_projects(project_directory)
        
        while self.project_browser_layout.count():
            child = self.project_browser_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for folder in folders:
            try:
                with open(f"{project_directory}/{folder}/.projeckt") as f:
                    current_name = f.readline().strip()
            
                new_project_item = Project_Item(title=current_name)
                self.project_browser_layout.addWidget(new_project_item.frame)
            except (OSError, UnicodeDecodeError) as e:
                print(e)
    
    def center(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.window.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.window.move(window_geometry.topLeft())

    def run(self):
        self.window.show()
        if not os.path.exists("conf.txt"):
            self.no_conf.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
        f.close()

    Icon_New = QIcon(QPixmap("Icons/New.svg"))
    Icon_Close = QIcon(QPixmap("Icons/Close.svg"))
    Icon_Delete =  QIcon(QPixmap("Icons/Delete.svg"))
    Icon_Check =  QIcon(QPixmap("Icons/Check.svg"))

    my_app = App()
    my_app.run()
    sys.exit(app.exec_())