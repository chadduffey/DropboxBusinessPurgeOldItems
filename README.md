# Dropbox_Business_Purge_Old_Items
Find old content on your Dropbox Business team and delete it (what-if mode is default)

By default the script will only report on old items (shown in red), not delete. 
By default the script will tell you about things that havnt been touched in 700 days
Both behaviours can be modified at the top of the script.

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



