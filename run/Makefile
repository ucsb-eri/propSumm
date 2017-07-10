CREDENTIAL_FILE=../var/acctinfo
USER_CREDENTIALS=`cat $(CREDENTIAL_FILE)`
all: daily

old: cleanRaw buildDB

daily: daily-toCSV daily-toDB daily-toBox

daily-toCSV:
	(cat ../../data/rsyncd/proposals-pi.dat | tr '\r' '\n' > ../var/daily.csv)

daily-toDB:
	../utils/csv2db.py --input-file=../var/daily.csv --dbpath=../var/proposalsSumm.sqlite3

daily-toBox:
	curl --user $(USER_CREDENTIALS) -T ../var/proposalsSumm.sqlite3 --ssl ftp://ftp.box.com/Caylor/proposalsSummary.sqlite3

cleanRaw:
	( cd ../sampleData; cat raw.csv | tr '\r' '\n' > test.csv )

buildDB:
	( cd ../sampleData; ../utils/csv2db.py; )
