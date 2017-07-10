all: daily

old: cleanRaw buildDB

daily: daily-toCSV daily-toDB

daily-toCSV:
	(cat ../../data/rsyncd/proposals-pi.dat | tr '\r' '\n' > ../var/daily.csv)

daily-toDB:
	../utils/csv2db.py --input-file=../var/daily.csv --dbpath=../var/proposalsSumm.sqlite3

cleanRaw:
	( cd ../sampleData; cat raw.csv | tr '\r' '\n' > test.csv )

buildDB:
	( cd ../sampleData; ../utils/csv2db.py; )
