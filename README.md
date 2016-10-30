# Dropbox_Business_Purge_Old_Items
Find old content on your Dropbox Business team and (optionally) delete it

By default the script will only report on old items, not delete unless you modify the options. 
By default the script will tell you about things that havnt been touched in 700 days, modify as required.

# Usage
python3 dropboxpurge.py

# Requirements
1. Only tested on OSX
2. Python3
3. Dropbox team member file access token for your team (you must modify variable at top of script)

# Installation
1. Save dropboxpurge.py and requirements.txt in new directory
2. (create a virtualenv if you wish)
3. Run pip install -r requirements.txt



