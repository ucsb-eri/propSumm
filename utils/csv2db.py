#!/usr/bin/env python
import csv
import sqlite3
import re
#import unicodedata
#import chardet


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

dateFields = [9,10,12,13,19,21,22]

#convertEncoding(chardet.detect(data)['encoding'], "utf-8", "test.csv", "test-fixed.csv")
rem = re.compile('(\d\d)/(\d\d)/(\d\d\d\d)')
createstr = ','.join(fields)

conn = sqlite3.connect('test.db')
conn.text_factory = str
c = conn.cursor()
c.execute('drop table if exists proposals;')
c.execute('create table if not exists proposals (' + createstr + ');')

# fields added in per fields derived from the CSV header line, so the fields
# above are primarily for building the schema, so we can add other fields
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
