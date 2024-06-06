@echo off
pause
call C:\Users\%USERNAME%\miniconda3\Scripts\activate.bat
call conda env create --file environment.yaml
call conda activate qr_scanner
call pip install pyzbar
call pip install qreader
call pip install pyqt5
call pip install pyqt5-tools
call pip install pyqt5designer
call pip install pyqrcode
call conda env update --file environment.yaml
pause