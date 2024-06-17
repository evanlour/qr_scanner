import pandas as pd
from pyzbar.pyzbar import decode, ZBarSymbol
import pyqrcode
import os

def createQr(userIn): #This function uses text and converts it to qrcode
    qrcode = pyqrcode.create(userIn) #We encode our data to a qr code
    out = "Data"
    if not os.path.exists(out): #We check if the required directories exist
        os.makedirs(out)
    out = out + "\\Employees"
    if not os.path.exists(out):
        os.makedirs(out)
    out = out + "\\" + userIn + ".png"
    qrcode.png(out, scale=10) #We extract our qrcode as png

def getQrCodeInfo(inputImage): #This function decodes the info the given QR has and returns it
    retData = "-1"
    for i in decode(inputImage, symbols=[ZBarSymbol.QRCODE]):
        data = i.data.decode('utf-8')
        if(data != None):
            retData = data
    return retData

def createUserId(Main, employeeFirstName, employeeLastName, employeeEmail, employeePhone): #This function creates a new employee entity with the given data
    if not os.path.exists("Data\\Employees\\employees.csv"):
        createEmployeeTable()
    df = pd.read_csv("Data\\Employees\\employees.csv") #We read the employee table
    df = df.set_index("employee_id")
    temp_df = df.loc[df['employee_first_name'] == employeeFirstName]
    if employeeLastName in temp_df.values:
        Main.consoleLabel.addText('Employee already present, if he is not in the system please contract an administrator')
    else:
        if(len(df) == 0):
            employeeId = 1
        else:
            employeeId = df.index[-1] + 1
            
        employeeAlias = employeeLastName[0] + employeeFirstName[0] + str(employeeId)
        employeeInfo = pd.DataFrame([{"employee_id" : employeeId, #create a temporary dataframe so we can merge it with the existing one
                        "employee_first_name" : employeeFirstName,
                        "employee_last_name" : employeeLastName,
                        "employee_alias" : employeeAlias,
                        "employee_email" : employeeEmail,
                        "employee_phone" : employeePhone}])
        employeeInfo = employeeInfo.set_index('employee_id')
        df = pd.concat([df, employeeInfo], axis=0) #We add the employee to the main employee table
        createQr(employeeAlias)
        Main.consoleLabel.addText("The employee " + employeeFirstName + " " + employeeLastName + " has been added to the employees table")
        df.to_csv('Data\\Employees\\employees.csv')

def createDayTable(directory): #CSV blueprint for our daily data
    columns = ['DateTime', 'employee_alias', 'employee_arrival', 'arrival_deadline', 'employee_departure', 'departure_deadline']
    df = pd.DataFrame(columns=columns)
    df = df.set_index("DateTime")
    df.to_csv(directory + ".csv")
    pass

def createEmployeeTable(): #CSV blueprint for our employee table data
    columns = ["employee_id", "employee_first_name", "employee_last_name", "employee_alias", "employee_email", "employee_phone"]
    df = pd.DataFrame(columns=columns)
    df = df.set_index("employee_id")
    if not os.path.exists("Data\\Employees"):
        os.makedirs("Data\\Employees")
    df.to_csv("Data\\Employees\\employees.csv")