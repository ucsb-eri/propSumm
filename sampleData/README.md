# sampleData

The data should not be made publically available.

So to create it:
+ Drop the original file into this directory as **raw.csv**
+ cd into the **run** folder
+ run **make**

## Quick description of the resulting files in this directory:
+ **raw.csv** - original raw csv from Kevin's export, records separated with carraige returns.
+ **test.csv** - carraige returns replaced with newlines.
+ **test.db** - sqlite3 db generated from the text.csv using the csv2db.py utility in the utils folder.
