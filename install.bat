@echo off
pause
call C:\Users\%USERNAME%\miniconda3\Scripts\activate.bat
call conda env create --file test.yaml
call conda activate qr_scanner_exp
call pip install pyzbar
call pip install qreader
call pip install pyqt5-tools --pre
call conda env update --file test.yaml
pause