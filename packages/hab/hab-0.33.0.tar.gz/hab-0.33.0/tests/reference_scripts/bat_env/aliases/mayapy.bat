@ECHO OFF
REM This script is the alias command for batch. We can't define a function in
REM memory that can be called from the command prompt like in other shells.

"C:\Program Files\Autodesk\Maya2020\bin\mayapy.exe" %*

@ECHO ON
