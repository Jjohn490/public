# This script is to check if Office 365 is installed and upgrade the program if it is installed.
# If its not installed it will echo that its not installed.
# This script will need to be updated from time to time by downloading a newer 
# install file of Office 365 and uploaded somewhere and change the download link here.

#!/bin/sh

DOWNLOAD='http://MicrosoftOffice.pkg'
INSTALL_PATH='MicrosoftOffice.pkg'
FOLDER='/Library/packages/'
PACKAGE='/Library/Microsoft'

if [[ -d $PACKAGE ]]; then
  cd $FOLDER
  sudo curl -O -L $DOWNLOAD
  sudo installer -pkg $INSTALL_PATH -target /
  sudo rm -rf $INSTALL_PATH
  echo "Office 365 Suite has been upgraded"
else
  echo "This user doesn't have Office 365 Suite"
fi

