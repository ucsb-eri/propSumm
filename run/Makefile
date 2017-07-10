all: daily
	
old: cleanRaw buildDB

daily:
	(cat ../../data/rsyncd/proposals-pi.dat | tr '\r' '\n' > ../var/daily.csv)

cleanRaw:
	( cd ../sampleData; cat raw.csv | tr '\r' '\n' > test.csv )

buildDB:
	( cd ../sampleData; ../utils/csv2db.py; )
