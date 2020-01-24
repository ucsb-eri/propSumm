# propSumm

Assembling proposal summary data.  Maybe provide some graphs.

See **README.md** file in **sampleData** folder about creating the data files.  Will
need the original data file.

## General layout
+ **utils** - scripts for processing
+ **run** - folder with a Makefile to provide make targets for specific tasks
+ **sampleData** - contains the sample data we started with
+ **webroot** - contains a php script that displays the data using datatables.net.  references the sqlite3 db **sampleData/test.db** 
+ **var** - not really used yet.  Figured it would be used for any dynamically created files that should NOT be in this repo. 

At this point we need to sort out what the specific goals are:
+ graphs?
+ reports?
+ how to summarize the data?
+ where is this installed?

Potential issues:
+ Do we need to see changes from one data import to the next?
  + If so:
    + we need a viable key (or pair of fields to act as a key)
    + what fields do we compare to to determine whether the data is updated or not

## Currently cloned at spin:/home/cricess/propSumm
Configuring system to be used there in a more automated fashion

cron job initiated at: spin:/etc/cron.d/propSumm 

