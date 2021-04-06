#!/bin/bash

# This is a script that goes and finds specific configuration files and asks if you want to delete them. 
# It goes and deletes them locally and from S3 or Rackspace as well

# Legit Path
DIR="/Users/$USER/"

# S3 bucket where configs are housed
BUCKET="s3://"

# Rackspace container
RACKSPACE="provision"

# Prompts user and sets as `USERNAME` variable
read -p "Who are we deleting? (ie. 'jjohnson'): "  USERNAME

# Uses `find` to search for any file with the `USERNAME` variable and ending with cfg. or .cfg.enc in the `DIR` variable
FILES=`find $DIR -type f \( -name "*$USERNAME.cfg" -o -name "*$USERNAME.cfg.enc" \)`

# Lists the files found
for FILE in $FILES; do
  echo $FILE
done

# Prompts for deletion and if the answer is any version of `Yes`, it deletes the file, if not, nothing happens
read -p "Do you want to delete these files from your computer? (y/N) " ANSWER
if [[ $ANSWER = "yes" || $ANSWER = "y" || $ANSWER = "Y" || $ANSWER = "Yes" ]]; then
  for FILE in $FILES; do
    rm $FILE
    echo "---- $FILE ---- REMOVED"
  done
else
  echo "No files deleted"
fi

# Prompts for deletion and if the answer is any version of `Yes`, it deletes the file from our S3 bucket.
read -p "Do you want to delete these files from the cloud? (y/N) " ANSWER
if [[ $ANSWER = "yes" || $ANSWER = "y" || $ANSWER = "Y" || $ANSWER = "Yes" ]]; then
  for FILE in $FILES; do
    # If the file contains .enc, it will run delete them in Rackspace or S3
    if [[ $FILE == *.enc ]]; then
      CONFIG_FILE=`echo $FILE | sed 's:.*/::'`
      rack files object delete --container $RACKSPACE --name $CONFIG_FILE
      # Uncomment out lines below when configs are housed in S34
      # s3cmd del $BUCKET$CONFIG_FILE
      # echo "Deleted file ---- $CONFIG_FILE ---- from S3"
    fi
  done
else
  echo "No files deleted"
fi
