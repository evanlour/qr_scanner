from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functions import *
import datetime

import cv2
shouldClose = False

def getCameraOutput(main):    
    cap = cv2.VideoCapture(0)
    today = datetime.datetime.now()
    directory = "Data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = directory + "\\Stats"
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = directory + "\\" + str(today.year)
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory = directory + "\\" + today.strftime("%B")
    if not os.path.exists(directory):
        os.makedirs(directory)
    date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
    directory = directory + "\\" + date
    if not os.path.exists(directory):
        createDayTable(directory)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if shouldClose == False:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (int(1280 * 2 / 3), int(720 * 2 /3)))
            global image
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            main.cameraLabel.setPixmap(QPixmap(image))
        else:
            break
    cv2.destroyAllWindows()

class ScrollLabel(QScrollArea):
 
    # constructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
 
        # making widget resizable
        self.setWidgetResizable(True)
 
        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)
 
        # vertical box layout
        lay = QVBoxLayout(content)
        # creating label
        self.label = QLabel(content)
 
        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
 
        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)
        
 
    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
    def text(self):
        return self.label.text()
    def addText(self, text):
        self.label.setText(self.label.text() + "\n" + text)
    
 

class Main(object):
    def create(self, MainWindow):
        windowWidth = 1280 #Our Window sizes
        windowHeight = 720
        MainWindow.setObjectName("MainWindow") #Name of the window
        MainWindow.setWindowTitle("qrScannerProject")
        MainWindow.setFixedSize(windowWidth, windowHeight) #Setting a fixed size for our window
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName("centralwidget")
        self.centralWidget.setStyleSheet("QWidget {background-color: #cfcfd1;}")

        #Frame 1, the frame holding the video output
        self.frame1 = QFrame(self.centralWidget)
        self.frame1.setGeometry(QRect(0, 0, int(windowWidth * 2 / 3), int(windowHeight * 2 / 3))) #Set size and position of frame
        self.frame1.setFrameShape(QFrame.StyledPanel) #Fixed so we can align better our frame
        self.frame1.setFrameShadow(QFrame.Raised)
        self.frame1.setObjectName("frame1") #Setting the frame name
        self.frame1.setStyleSheet("QFrame {background-color:#000000;}") #Setting the color to better recognize visualy the frame part(might be commented later)
        #self.frame1.setStyleSheet("QFrame {border: 5px solid black}")
        self.frame1Layout = QVBoxLayout(self.frame1)
        self.frame1Layout.setObjectName("frame1Layout")
        self.cameraLabel = QLabel()
        self.cameraLabel.setObjectName("cameraLabel")
        self.frame1Layout.addWidget(self.cameraLabel)

        #Frame 2, the frame holding the button commands
        self.frame2 = QFrame(self.centralWidget)
        self.frame2.setGeometry(QRect(int(windowWidth * 2 / 3), 0, int(windowWidth * 1 / 3), int(windowHeight * 2 / 3))) #Set size and position of frame
        self.frame2.setFrameShape(QFrame.StyledPanel) #Fixed so we can align better our frame
        self.frame2.setFrameShadow(QFrame.Raised)
        self.frame2.setObjectName("frame2") #Setting the frame name
        self.frame2.setStyleSheet("QFrame {background-color:#cfcfd1;}")
        #self.frame2.setStyleSheet("QFrame {border: 5px solid black}")
        self.frame2Layout = QVBoxLayout(self.frame2)
        self.frame2Layout.setObjectName("frame2Layout")

        self.scannerMode = QPushButton()
        self.scannerMode.setStyleSheet("QPushButton {background-color: white}")
        self.scannerMode.setText("Mode = Arrival")
        self.scannerMode.clicked.connect(self.changeScannerMode)
        self.frame2Layout.addWidget(self.scannerMode)

        self.addEmployeeButton = QPushButton()
        self.addEmployeeButton.setStyleSheet("QPushButton {background-color: white}")
        self.addEmployeeButton.setText("Add new employee")
        self.addEmployeeButton.clicked.connect(self.addEmployee)
        self.frame2Layout.addWidget(self.addEmployeeButton)

        self.arrivalEndButton = QPushButton()
        self.arrivalEndButton.setStyleSheet("QPushButton {background-color: white}")
        self.arrivalEndButton.setText("Click to set arrival deadline")
        self.arrivalEndButton.clicked.connect(self.setArrivalEnd)
        self.frame2Layout.addWidget(self.arrivalEndButton)

        self.departureStartButton = QPushButton()
        self.departureStartButton.setStyleSheet("QPushButton {background-color: white}")
        self.departureStartButton.setText("Click to set departure start time")
        self.departureStartButton.clicked.connect(self.setDepartureStart)
        self.frame2Layout.addWidget(self.departureStartButton)

        #Frame 3, the frame acting as console output
        self.frame3 = QFrame(self.centralWidget)
        self.frame3.setGeometry(QRect(0, int(windowHeight * 2 / 3), int(windowWidth * 2 / 3), int(windowHeight * 1 / 3))) #Set size and position of frame
        self.frame3.setFrameShape(QFrame.StyledPanel) #Fixed so we can align better our frame
        self.frame3.setFrameShadow(QFrame.Raised)
        self.frame3.setObjectName("frame3") #Setting the frame name
        self.frame3Layout = QVBoxLayout(self.frame3)
        self.frame3Layout.setObjectName("frame3Layout")       
        consoleLabel = ScrollLabel()
        self.consoleLabel = consoleLabel
        self.frame3Layout.addWidget(consoleLabel)

        #Frame 4, the frame holding general info
        self.frame4 = QFrame(self.centralWidget)
        self.frame4.setGeometry(QRect(int(windowWidth * 2 / 3), int(windowHeight * 2 / 3), int(windowWidth * 1 / 3), int(windowHeight * 1 / 3))) #Set size and position of frame
        self.frame4.setFrameShape(QFrame.StyledPanel) #Fixed so we can align better our frame
        self.frame4.setFrameShadow(QFrame.Raised)
        self.frame4.setObjectName("frame4") #Setting the frame name
        self.frame4.setStyleSheet("QFrame {background-color:#cfcfd1;}")
        #self.frame4.setStyleSheet("QFrame {border: 5px solid black}")
        self.verticalLayout = QVBoxLayout(self.frame4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.time_label = QLabel("")
        self.date_label = QLabel("")
        self.time_label.setFont(QFont("Arial", 15))
        self.date_label.setFont(QFont("Arial", 15))
        self.time_label.setObjectName("time_label")
        self.date_label.setObjectName("date_label")
        self.verticalLayout.addWidget(self.time_label)
        self.verticalLayout.addWidget(self.date_label)
        # creating a timer object for updating the time every second
        timer = QTimer(self.time_label)
        timer.timeout.connect(self.showInfo) #Connecting the timer with the time function
        timer.start(1000)
        MainWindow.setCentralWidget(self.centralWidget)

    def showInfo(self):

        current_time = QTime.currentTime()
        current_date = QDateTime.currentDateTime()

        label_time = "Current time is: " + current_time.toString('hh:mm:ss')
        label_date = "Current date is: " + current_date.toString("dddd dd/MM/yyyy")

        self.time_label.setText(label_time)
        self.date_label.setText(label_date)
    
    def changeScannerMode(self):
        if(self.scannerMode.text() == "Mode = Arrival"):
            self.scannerMode.setText("Mode = Departure")
            self.consoleLabel.addText("Mode has been changed to Departure")
        else:
            self.scannerMode.setText("Mode = Arrival")
            self.consoleLabel.addText("Mode has been changed to Arrival")

    def addEmployee(self):
        pass

    def setArrivalEnd(self):
        today = datetime.datetime.now()
        currentTime = QTime.currentTime()
        directory = "Data\\Stats\\" + str(today.year) + "\\" + str(today.strftime("%B")) + "\\"
        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
        directory = directory + date + ".csv"
        df = pd.read_csv(directory)
        time = currentTime.toString("hh::mm::ss")
        df["arrival_deadline"] = time
        df.to_csv(directory)
        self.consoleLabel.addText("The time of " + time + " has been registered as arrival_deadline")

    def setDepartureStart(self):
        today = datetime.datetime.now()
        currentTime = QTime.currentTime()
        directory = "Data\\Stats\\" + str(today.year) + "\\" + str(today.strftime("%B")) + "\\"
        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
        directory = directory + date + ".csv"
        df = pd.read_csv(directory)
        time = currentTime.toString("hh::mm::ss")
        df["departure_deadline"] = time
        df.to_csv(directory)
        self.consoleLabel.addText("The time of " + time + " has been registered as departure_deadline")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    main = Main()
    main.create(MainWindow)
    MainWindow.show()

    thread = Thread(target=getCameraOutput, args=(main,))
    thread.start()
    while "image" not in globals():
        pass
    app.exec()
    shouldClose = True
    thread.join()
    sys.exit(app)
