# System Requirements
In order to run the application your (virtual) machine needs at least 6GB of RAM
# Installation
## Linux and MacOS
### Step 1: Downloading VarPred
In order to use VarPred you need to fork the repository or download the source code from GitHub.
### Step 2: Installing Docker
VarPred uses Docker to run, make sure you have Docker installed correctly. You can download Docker using the following [link](https://www.docker.com/get-started). <br>
To test if Docker is installed correctly, type the command `docker` in the terminal. If everything is installed correctly, you should see and overview of the Docker commands available.
### Step 3: Running VarPred
Once you have downloaded the source code and started Docker, navigate to the directory with VarPred and run the build.sh script using the command `source build.sh`.<br>
Make sure build.sh (project root), seed-script.sh (/database), pipeline.sh (/ml_scripts), update_clinvar.sh (/ml_scripts) have permissions to be executed. Execute permissions can be granted with `chmod 711 *file name*`.<br>
If everything is set up correctly the application should now be building and running. This may take a while.
If everything is set up correctly the application should now be building, this may take a while. Once it has finished building you can access it by typing `localhost:5000` in the navigation bar within your browser.

## Windows 10 & 11
### Step 1: Setting up and installing WSL2
Before you start make sure you have enabled hardware assisted virtualisation (Intel) or svm (AMD) in the BIOS settings.
* Run a PowerShell window as administrator and allow it to make changes to your device. This can be done by pressing Start and searching for PowerShell.
  Once you found PowerShell, right click and slelect `Run as administrator`.
* Run the following command: `wsl --install`. This should install both WSL2 and Ubuntu.
* Run the command `wsl -l -v`. This should give you an overview of the installed Linux distributions currently installed.
  If everything is installed correctly, you should see Ubuntu in the list.
  Make sure the version is set as 2, this should be the standard setting.
  If this is not the case, please run the command `wsl --set-version Ubuntu 2`

You can now close the PowerShell window.<br><br>
Now go to Start and look for an application called "Ubuntu". Open this application and go through the set-up process. Do not close the window after setting up your account.
### Step 2: Downloading VarPred
In order to use VarPred you need to fork the repository or download the source code from GitHub.
### Step 3: Installing Docker
VarPred uses Docker to run, make sure you have Docker installed correctly. You can download Docker using the following [link](https://www.docker.com/get-started). <br>
To test if Docker is installed correctly, type the command `docker` in the Ubuntu terminal. If everything is installed correctly, you should see and overview of the Docker commands available.
### Step 4: Running VarPred
Once you have downloaded the source code and started Docker, use the Ubuntu terminal to navigate to the directory with VarPred.
Ubuntu on Windows uses a different file system than Windows. In order to access your Windows C drive, run the command `cd /mnt/c` in the Ubuntu terminal.
From here you can access your Windows files like you normally would. Once you have navigated to the VarPred directory you run build.sh. with `source build.sh`. <br>
Make sure build.sh (project root), seed-script.sh (/database), pipeline.sh (/ml_scripts), update_clinvar.sh (/ml_scripts) have permissions to be executed. Execute permissions can be granted with `chmod 711 *file name*`.<br>
If everything is set up correctly the application should now be building, this may take a while. Once it has finished building you can access it by typing `localhost:5000` in the navigation bar within your browser.
### Troubleshooting
While running VarPred on Windows we encountered a few issues:
1. Windows and Linux both use diffrent line seperators (\r\n for Windows and \n for Linux). It is possible that your bash files (files with the extention ".sh") are formatted for the wrong operating system.
   You can change the line seperator for each files individually in applications like [Notepad++](https://notepad-plus-plus.org/) or [PyCharm](https://www.jetbrains.com/pycharm/).
   In these programs there is a button in the lower right section containing the letters "CR", "LF" or "CRLF".
   Make sure this option is set to "LF". If it isn't. Click on the button, set it to "LF" and save the file.
   Do this for all of the following files: build.sh (project root), seed-script.sh (/database), pipeline.sh (/ml_scripts), update_clinvar.sh (/ml_scripts).
2. If you have already installed a Linux command line, this commandline might run on WSL version 1. In order for the commandline to integrate WSL should be updated.
   This can be done by running a PowerShell window as administrator (as explained in Step 1) and running the command `wsl --updadte`.
   After this use the command `wsl -l -v` and make sure your Linux distro is running on WSL version 2.
   If this is not the case you can covert the Linux installation to WSL version 2 with the command wsl --set-version [distribution name (shown in the previous command)] 2.
   In case this does not work either we have found that running the command `sudo systemctl restart docker` in your Linux terminal might make Docker work.

# Information scraping NCBI pages
#### Last update .JSON files: 24-01-2022
Webscraping of the 2 NCBI pages has to be run separately. The .JSON files are included in the docker setup. Only for updating the 
.JSON files (NCBI Gene and Medgen pages) you need to run the script, which is located in the directory 'webscraping'.

## Running webscraping script
1. Go to the directory 'webscraping'.
2. Run `python .\webscraping_ncbi.py location_of_clinvar_file`
   - **Important: This take approximately 2 days of running.**