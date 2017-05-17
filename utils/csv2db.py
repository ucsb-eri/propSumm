#!/usr/bin/env python
import csv
import sqlite3
import re
#import unicodedata
#import chardet


fields = [
  "Seq_Num integer",
  "Title text",
  "Agency text",
  "Agency_SeqNum text",
  "Agency_Number text",
  "Center text",
  "Status text",
  "Type text",
  "Amount text",
  "Start_Date date",
  "End_Date date",
  "OR_Record_Number text",
  "Date_Submitted date",
  "Fiscal_Year_Submitted text",
  "Notes text",
  "History text",
  "IDC_Rate_Type text",
  "Doc_Notes text",
  "PI_Name_Display text",
  "Status_Date date",
  "Revised_Budget text",
  "Revision_Date date",
  "Due_Date date",
  "PI_Order_Number text",
  "PI_Code text",
  "First_Name text",
  "Middle_Name text",
  "Last_Name text",
  "Dept text",
  "PI_Title text"
]

dateFields = [9,10,12,13,19,21,22]

#convertEncoding(chardet.detect(data)['encoding'], "utf-8", "test.csv", "test-fixed.csv")
rem = re.compile('(\d\d)/(\d\d)/(\d\d\d\d)')
createstr = ','.join(fields)

conn = sqlite3.connect('test.db')
conn.text_factory = str
c = conn.cursor()
c.execute('drop table if exists proposals;')
c.execute('create table if not exists proposals (' + createstr + ');')

with open ('test.csv', 'r') as f:
    reader = csv.reader(f)
    columns = next(reader)
    query = 'insert into proposals({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    cursor = conn.cursor()
    for data in reader:
        #print query
        for di in dateFields:
            data[di] = re.sub(' 00:00:00','',data[di])
            data[di] = re.sub('00/00/0','0000-00-00',data[di])
            gm = rem.match(data[di])
            if gm and len(gm.groups()) == 3:
                data[di] = gm.group(3) + '-' + gm.group(2) + '-' + gm.group(1)

        #print data[9],data[10],data[12],data[13],data[19],data[21]
        cursor.execute(query, data)
    conn.commit()
conn.close()
