all: cleanRaw buildDB

cleanRaw:
	( cd ../sampleData; cat raw.csv | tr '\r' '\n' > test.csv )

buildDB:
	( cd ../sampleData; ../utils/csv2db.py; )
