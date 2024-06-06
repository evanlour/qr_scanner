from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functions import *
import datetime
from functools import partial
import time
import cv2
shouldClose = False

#This function runs as a seperate thread and will serve as
#the camera output, as well as decoder for the qr images
def getCameraOutput(main):    
    cap = cv2.VideoCapture(0) #We start the main camera of our system
    today = datetime.datetime.now() #We get the current time
    directory = "Data"
    #We now make sure that all the necessary folders exists
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
    if not os.path.exists(directory + ".csv"):
        createDayTable(directory)
    
    if not os.path.exists("Data\\Employees"):
        os.makedirs("Data\\Employees")
    
    if not os.path.exists("Data\\Employees\\employees.csv"):
        createEmployeeTable()
    
    #This while loop will work until the camera is closed, which
    #happens when we close the main window
    while(cap.isOpened()):
        ret, frame = cap.read() #We read the camera info
        if shouldClose == False: #While the camera should stay open..
            currentTime = datetime.datetime.now()#We get the current time again
            qr_text = getQrCodeInfo(frame) #We decode the qr text
            if(qr_text != "-1"): #If we decode text succesfully, we read and setup our tables
                employees = pd.read_csv("Data\\Employees\\employees.csv")
                dayData = pd.read_csv(directory + ".csv")

                if(main.scannerMode.text() == "Mode = Arrival"):#This will work when the mode is set to arrival
                    if(qr_text in employees["employee_alias"].unique() and qr_text not in dayData["employee_alias"].unique()): #If the arrival is correctly detected
                        dayData.loc[len(dayData.index)] = [date, qr_text, "-1", "-1", "-1", "-1"]
                        arrivalTime = str(currentTime.hour) + ":" + str(currentTime.minute) + ":" + str(currentTime.second)#We record the arrival time
                        dayData.loc[dayData["employee_alias"] == qr_text, "employee_arrival"] = arrivalTime
                        main.consoleLabel.addText("Employee with alias " + qr_text + " arrived at " + arrivalTime) #We give the output to our console
                    elif qr_text in dayData["employee_alias"].unique(): #If the employee has already arrived
                        main.consoleLabel.addText("The employee " + qr_text + " has already been recorded to arrive")
                    else:#If the employee is not part of the system
                        main.consoleLabel.addText(qr_text + " is not in the system, you might need to add him")
                else:
                    if qr_text not in employees["employee_alias"].unique():#If the employee is not part of the system
                        main.consoleLabel.addText(qr_text + " is not in the system, you might need to add him")
                    elif qr_text not in dayData["employee_alias"].unique():#If the employee has no arrival time, he can't leave
                        main.consoleLabel.addText(qr_text + " does not have an arrival time, he cannot depart!")
                    elif str(dayData.set_index("employee_alias").loc[qr_text, "employee_departure"]) != "-1":#If he already left
                        main.consoleLabel.addText(qr_text + "has already departed!")
                    else:#If the departure detection is correct
                        departureTime = str(currentTime.hour) + ":" + str(currentTime.minute) + ":" + str(currentTime.second)
                        dayData.loc[dayData["employee_alias"] == qr_text, "employee_departure"] = departureTime #We record the departure time
                        main.consoleLabel.addText(qr_text + " has departed at " + departureTime)
                time.sleep(1.2)
                dayData = dayData.set_index("DateTime")#We format and save the data
                dayData.to_csv(directory + ".csv")


            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #We edit the image so we can display it
            frame = cv2.resize(frame, (int(1280 * 2 / 3), int(720 * 2 /3)))
            global image
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            main.cameraLabel.setPixmap(QPixmap(image))
        else:
            break
    cv2.destroyAllWindows()#On closure

class ScrollLabel(QScrollArea): #This class is the base for our console
 
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
    def text(self): #This function returns the current text of the label
        return self.label.text()
    def addText(self, text): #This function adds text to the existing one
        self.label.setText(self.label.text() + "\n" + text)
    
class newEmployeeWindow(QWidget): #The popup window when we want to add an employee
    def create(self, main):
        self.setFixedSize(300, 170)
        layout = QFormLayout()

        #We create the labels telling the worker where to input the data correctly
        self.firstNameLabel = QLabel("Write the employee first name here: ")
        self.lastNameLabel = QLabel("Write the employee last name here: ")
        self.emailLabel = QLabel("Write the employee email here")
        self.phoneLabel = QLabel("Write the employee phone here")

        #The place where we will type our data
        self.firstNameLine = QLineEdit()
        self.lastNameLine = QLineEdit()
        self.emailLine = QLineEdit()
        self.phoneLine = QLineEdit()

        #We create the accept/cancel buttons
        self.acceptButton = QPushButton("Add employee")
        self.acceptButton.clicked.connect(partial(self.acceptButtonFunc, main))
        self.rejectButton = QPushButton("Cancel")
        self.rejectButton.clicked.connect(partial(self.rejectButtonFunc, main))

        #We add them all to our window in lines
        layout.addRow(self.firstNameLabel, self.firstNameLine)
        layout.addRow(self.lastNameLabel, self.lastNameLine)
        layout.addRow(self.emailLabel, self.emailLine)
        layout.addRow(self.phoneLabel, self.phoneLine)
        layout.addRow(self.acceptButton, self.rejectButton)

        self.setLayout(layout)

    def acceptButtonFunc(self, main): #When we accept, we will try to create the employee data
        main.consoleLabel.addText("Trying to add new employee!")
        createUserId(main, self.firstNameLine.text(), self.lastNameLine.text(), self.emailLine.text(), self.phoneLine.text())
        self.close()

    def rejectButtonFunc(self, main): #If we accidentally pressed the create new employee, this will be the cancel button
        main.consoleLabel.addText("Canceling the insertion of new employee")
        self.close()

class Main(object): #This is our main window
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
        self.frame1.setStyleSheet("QFrame {background-color:#000000;}")
        self.frame1Layout = QVBoxLayout(self.frame1) #We create a layout to add our items efficiently
        self.frame1Layout.setObjectName("frame1Layout")
        self.cameraLabel = QLabel()#This is the label where our image from the camera will display
        self.cameraLabel.setObjectName("cameraLabel")
        self.frame1Layout.addWidget(self.cameraLabel)

        #Frame 2, the frame holding the button commands
        self.frame2 = QFrame(self.centralWidget)
        self.frame2.setGeometry(QRect(int(windowWidth * 2 / 3), 0, int(windowWidth * 1 / 3), int(windowHeight * 2 / 3))) #Set size and position of frame
        self.frame2.setFrameShape(QFrame.StyledPanel) #Fixed so we can align better our frame
        self.frame2.setFrameShadow(QFrame.Raised)
        self.frame2.setObjectName("frame2") #Setting the frame name
        self.frame2.setStyleSheet("QFrame {background-color:#cfcfd1;}")
        self.frame2Layout = QVBoxLayout(self.frame2) #We create a layout to add our items efficiently
        self.frame2Layout.setObjectName("frame2Layout")

        self.scannerMode = QPushButton()#This is the button that changes between arrival and departure mode
        self.scannerMode.setStyleSheet("QPushButton {background-color: white}")
        self.scannerMode.setText("Mode = Arrival")
        self.scannerMode.clicked.connect(self.changeScannerMode) #We connect the button with a function so it works when the button is pressed
        self.frame2Layout.addWidget(self.scannerMode)

        self.addEmployeeButton = QPushButton()#This is the button which we will use when we want to add a new employee
        self.addEmployeeButton.setStyleSheet("QPushButton {background-color: white}")
        self.addEmployeeButton.setText("Add new employee")
        self.addEmployeeButton.clicked.connect(self.addEmployee)#We connect the addemployee function so we can add employees
        self.frame2Layout.addWidget(self.addEmployeeButton)

        self.arrivalEndButton = QPushButton()#This button sends to our data the arrival deadline time
        self.arrivalEndButton.setStyleSheet("QPushButton {background-color: white}")
        self.arrivalEndButton.setText("Click to set arrival deadline")
        self.arrivalEndButton.clicked.connect(self.setArrivalEnd) #We give the button the functionality
        self.frame2Layout.addWidget(self.arrivalEndButton)

        self.departureStartButton = QPushButton() #This button sends to our data the departure start time
        self.departureStartButton.setStyleSheet("QPushButton {background-color: white}")
        self.departureStartButton.setText("Click to set departure start time")
        self.departureStartButton.clicked.connect(self.setDepartureStart) #We give the button functionality
        self.frame2Layout.addWidget(self.departureStartButton)

        #Frame 3, the frame acting as console output
        self.frame3 = QFrame(self.centralWidget)
        self.frame3.setGeometry(QRect(0, int(windowHeight * 2 / 3), int(windowWidth * 2 / 3), int(windowHeight * 1 / 3))) #Set size and position of frame
        self.frame3.setFrameShape(QFrame.StyledPanel) #Fixed so we can align better our frame
        self.frame3.setFrameShadow(QFrame.Raised)
        self.frame3.setObjectName("frame3") #Setting the frame name
        self.frame3Layout = QVBoxLayout(self.frame3)
        self.frame3Layout.setObjectName("frame3Layout")       
        consoleLabel = ScrollLabel() #Our custom class object that we made above
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
        self.time_label = QLabel("") #We create a time and a date label for convenience
        self.date_label = QLabel("")
        self.time_label.setFont(QFont("Arial", 15))
        self.date_label.setFont(QFont("Arial", 15))
        self.time_label.setObjectName("time_label")
        self.date_label.setObjectName("date_label")
        self.verticalLayout.addWidget(self.time_label)
        self.verticalLayout.addWidget(self.date_label)
        # creating a timer object for updating the currentTime every second
        timer = QTimer(self.time_label)
        timer.timeout.connect(self.showInfo) #Connecting the timer with the currentTime function
        timer.start(1000)
        MainWindow.setCentralWidget(self.centralWidget)

    def showInfo(self): #this function is tied with frame 4, it gives the time and date data to the frame

        current_time = QTime.currentTime()
        current_date = QDateTime.currentDateTime()

        label_time = "Current currentTime is: " + current_time.toString('hh:mm:ss')
        label_date = "Current date is: " + current_date.toString("dddd dd/MM/yyyy")

        self.time_label.setText(label_time)
        self.date_label.setText(label_date)
    
    def changeScannerMode(self): #This function is used to give functionality to our scanner mode button
        if(self.scannerMode.text() == "Mode = Arrival"):
            self.scannerMode.setText("Mode = Departure")
            self.consoleLabel.addText("Mode has been changed to Departure")
        else:
            self.scannerMode.setText("Mode = Arrival")
            self.consoleLabel.addText("Mode has been changed to Arrival")

    def addEmployee(self): #The function used to give functionality to the addEmployee button
        self.window = newEmployeeWindow()
        self.window.create(self)
        self.window.show()

    def setArrivalEnd(self): #This function sends to our data the arrival end time
        today = datetime.datetime.now()
        currentTime = QTime.currentTime()
        directory = "Data\\Stats\\" + str(today.year) + "\\" + str(today.strftime("%B")) + "\\"
        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
        directory = directory + date + ".csv"
        df = pd.read_csv(directory)
        currentTime = currentTime.toString("hh::mm::ss")
        if(len(df.axes[0]) != 0): #If the arrival table isn't empty
            df["arrival_deadline"] = currentTime
            df = df.set_index("DateTime")
            df.to_csv(directory)
            self.consoleLabel.addText("The currentTime of " + currentTime + " has been registered as arrival_deadline")
        else:
            self.consoleLabel.addText("No employee has arrived!")

    def setDepartureStart(self): #This function sends to our data the departure start time
        today = datetime.datetime.now()
        currentTime = QTime.currentTime()
        directory = "Data\\Stats\\" + str(today.year) + "\\" + str(today.strftime("%B")) + "\\"
        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
        directory = directory + date + ".csv"
        df = pd.read_csv(directory)
        currentTime = currentTime.toString("hh::mm::ss")
        if(len(df.axes[0]) != 0): #If we have arrivals and the table isn't empty
            df["departure_deadline"] = currentTime
            df = df.set_index("DateTime")
            df.to_csv(directory)
            self.consoleLabel.addText("The currentTime of " + currentTime + " has been registered as departure_deadline")
        else:
            self.consoleLabel.addText("No employee has arrived!")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv) #We create the app
    MainWindow = QMainWindow() #We create the main window
    main = Main()
    main.create(MainWindow)
    MainWindow.show() #We show the window when it is ready

    thread = Thread(target=getCameraOutput, args=(main,)) #We create the video thread
    thread.start()
    while "image" not in globals(): #We await for the camera to start up
        pass
    app.exec() #We execute the app
    shouldClose = True
    thread.join()
    sys.exit(app)
