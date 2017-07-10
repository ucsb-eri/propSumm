#!/usr/bin/env python
import csv
import os
import sys
import sqlite3
import re
from optparse import OptionParser


p = OptionParser()
p.add_option('--input-file','-i',
             action='store', dest='infile', default='../var/daily.csv',
             help='Generate a .json file in JSONpath instead of stdout')
p.add_option('--dbpath',
             action='store', dest='dbpath', default='../var/proposalsSummary.sqlite3',
             help='Path to the database (default: ../var/proposalsSummary.sqlite3)')
p.add_option('--verbose', '-v',
             action='store_true', dest='verbose', default=False,
             help='increases verbosity of messages to stdout')
p.add_option('--debug', '-d',
             action='store_true', dest='debug', default=False,
             help='adds debugging output')

class proposalsSummary:
    def __init__(self,infile,dbpath):
        self.dateFields = [9,10,12,13,19,21,22]


        self.dbInit(dbpath)
        self.dbLoad(infile)

    def dbInit(self,dbpath):
        #print "Yay!  Here we go."
        fields = [
          "Seq_Num INTEGER",
          "Title TEXT",
          "Agency TEXT",
          "Agency_SeqNum INTEGER",
          "Agency_Number TEXT",
          "Center TEXT",
          "Status TEXT",
          "Type TEXT",
          "Amount INTEGER",
          "Start_Date DATE",
          "End_Date DATE",
          "OR_Record_Number TEXT",
          "Date_Submitted DATE",
          "Fiscal_Year_Submitted TEXT",
          "Notes TEXT",
          "History TEXT",
          "IDC_Rate_Type TEXT",
          "Doc_Notes TEXT",
          "PI_Name_Display TEXT",
          "Status_Date DATE",
          "Revised_Budget TEXT",
          "Revision_Date DATE",
          "Due_Date DATE",
          "PI_Order_Number INTEGER",
          "PI_Code TEXT",
          "First_Name TEXT",
          "Middle_Name TEXT",
          "Last_Name TEXT",
          "Dept TEXT",
          "PI_Title TEXT",
          "epoch INTEGER DEFAULT (STRFTIME('%s','now'))"
        ]

        rem = re.compile('(\d\d)/(\d\d)/(\d\d\d\d)')
        createstr = ','.join(fields)

        self.conn = sqlite3.connect(dbpath)
        self.conn.text_factory = str
        c = self.conn.cursor()
        c.execute('drop table if exists proposals;')
        c.execute('create table if not exists proposals (' + createstr + ');')

    def dbLoad(self,infile):
        if not os.path.exists(infile):
            print "ERROR: specified inputfile:",infile,"Doesnt exist, bailing ..."
        # fields added in per fields derived from the CSV header line, so the fields
        # above are primarily for building the schema, so we can add other fields
        with open (infile, 'r') as f:
            reader = csv.reader(f)
            columns = next(reader)
            query = 'insert into proposals({0}) values ({1})'
            query = query.format(','.join(columns), ','.join('?' * len(columns)))
            cursor = self.conn.cursor()
            for data in reader:
                #print query
                # Lets tweak/cleanup the date fields of the CSV input
                for di in self.dateFields:
                    data[di] = re.sub(' 00:00:00','',data[di])
                    data[di] = re.sub('00/00/0','0000-00-00',data[di])
                    gm = rem.match(data[di])
                    if gm and len(gm.groups()) == 3:
                        data[di] = gm.group(3) + '-' + gm.group(2) + '-' + gm.group(1)

                # Insert the data
                cursor.execute(query, data)
            self.conn.commit()
        self.conn.close()
        print "finished db load"


def main():
    if not opt.debug:
        devnull = open(os.devnull, 'w')
        sys.stderr = devnull

    ps = proposalsSummary(opt.infile,opt.dbpath)



if __name__ == '__main__':
    (opt, args) = p.parse_args()
    main()
    print "finished main"
    if opt.debug:
        print "done"
    sys.exit(0)
