# qr_scanner
This is a program that enables the creation and monitoring of custom employee qr codes. It is extremely simple on purpose in order
to highlight the ease of use and expandability of the pyqt5 and opencv libraries, along as show their strengths. Along with the python files, 
an environment.yaml file is provided in order to install the required environment.
## Dependencies
- A conda installation
- Make sure that you have the following c++ redistr installed https://www.microsoft.com/en-us/download/details.aspx?id=40784
## How to install
First, clone the repo. After, type:
~~~
conda env create --file environment.yaml
conda activate qr_scanner
~~~
And you are set to run the main.py file

## How the program works
This program uses a pc camera to detect and decode qr images in real time
The application of this program is guided towards a company that needs to keep in check with arrival and departure times
Everything is done with button pressing, except when adding a new employee, where you need to type the info
All the data is saved under the "Data" folder, which contains the "Employees" and "Stats" folders
The "Employees" folder will hold all the current employee's data, as well as the qr codes they need to scan in .png form
The "Data" folder holds all arrival and departure data in Year/Month/Day form

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.