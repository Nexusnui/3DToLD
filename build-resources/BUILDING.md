This is intended for documenting on how to build the distributable files for this project.

## Setup Project

### TBD

## Build Python Packages

To build the python package open a terminal in the project folder with virtual environment activated and run
`python -m build`. 
This creates both a ".tar.gz" and ".whl" file in the "dist" folder, either can be installed with pip/pipx.

## Build the Windows Executables

To build the Windows executable open a terminal in the project folder with virtual environment activated and run 
`pyinstaller app_windows.spec --noconfirm` to build the executable for the installer and
`pyinstaller app_windows_portable.spec` for the portable version. The result is placed in the "dist" folder.

## Creating the Windows Installer

After building the executables the installer is created by compiling "InnoSetupScript.iss" with InnoSetup.
