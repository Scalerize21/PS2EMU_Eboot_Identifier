@echo off
setlocal enabledelayedexpansion

:: Define the files
set "eboot_file=eboot.bin"
set "crc_file=crc.txt"

:: Check if eboot.bin exists
if not exist "%eboot_file%" (
    echo %eboot_file% not found in the current directory.
    exit /b 1
)

:: Compute MD5 checksum of eboot.bin
for /f "delims=" %%i in ('certutil -hashfile "%eboot_file%" MD5 ^| find /i /v "certutil"') do set "md5_checksum=%%i"
set "md5_checksum=%md5_checksum: =%"

:: Check if crc.txt exists
if not exist "%crc_file%" (
    echo %crc_file% not found.
    exit /b 1
)

:: Search for the matching title in crc.txt
set "found=0"
for /f "tokens=1,* delims=:" %%a in (%crc_file%) do (
    set "title=%%a"
    set "crc=%%b"
    set "crc=!crc: =!"
    if "!crc!"=="%md5_checksum%" (
        echo The emulator is !title! with a CRC of %md5_checksum%.
        set "found=1"
    )
)

if !found! == 0 (
    echo No matching title found for CRC %md5_checksum%.
)

:: Keep the script running
echo.
echo The script is running. Press Ctrl+C to exit.
:loop
timeout /t 86400 >nul
goto loop
