# qrScanner
# CODE IS WORKING AND CURRENTLY BEING TESTED
# In order to run the program:
0) (If you ran the old testing version) open miniconda and type conda remove --name qr_scanner --all
1) Download miniconda from here: https://docs.anaconda.com/free/miniconda/index.html
2) Install miniconda(choose the default options in every step)
3) Import the project to the desired inventory
4) Run the install.bat
5) After the program is finished, you can now open the run.bat
6) If the environment dependencies are updated, install.bat will need to be rerun, although it seems unlikely to happen

This program uses a pc camera to detect and decode qr images in real time, now with GUI
The application of this program is guided towards a company that needs to keep in check with arrival and departure times
Everything is done with button pressing, except when adding a new employee, where you need to type the info
All the data is saved under the "Data" folder, which contains the "Employees" and "Stats" folders
The "Employees" folder will hold all the current employee's data, as well as the qr codes they need to scan in .png form
The "Data" folder holds all arrival and departure data in Year/Month/Day form
If any bug is found, message me to try and fix it

Additional Info:
- The numexpr=2.8.4 is not actually needed for the project to work, we add it to suppress a warning that the default 2.7.3 version provides
- If it throws a nasty error make sure that you have the following c++ redistr installed https://www.microsoft.com/en-us/download/details.aspx?id=40784