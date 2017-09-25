CREDENTIAL_FILE=../var/acctinfo
USER_CREDENTIALS=`cat $(CREDENTIAL_FILE)`
CREDENTIAL_FILE_AWSPG=../var/acctinfo-aws-postgres
CREDENTIALS_AWSPG=`cat $(CREDENTIAL_FILE_AWSPG)`
SQLITE_DUMPFILE=../var/proposalsSumm.sql
PGXFRLOG=../var/pgXfrLog
all: daily

old: cleanRaw buildDB

daily: daily-toCSV daily-toDB daily-toBox daily-toPostgres

daily-toCSV:
	@(cat ../../data/rsyncd/proposals-pi.dat | tr '\r' '\n' > ../var/daily.csv)

daily-toDB:
	@../utils/csv2db.py --input-file=../var/daily.csv --dbpath=../var/proposalsSumm.sqlite3

daily-toBox:
	@curl --user $(USER_CREDENTIALS) -T ../var/proposalsSumm.sqlite3 --ssl ftp://ftp.box.com/ERI-Admin/ > /dev/null 2>&1
	@curl --user $(USER_CREDENTIALS) -T ../var/daily.csv --ssl ftp://ftp.box.com/ERI-Admin/ > /dev/null 2>&1

daily-toPostgres:
	@( echo "DROP TABLE if exists proposals;" > $(SQLITE_DUMPFILE))
	@( echo ".dump" | sqlite3 ../var/proposalsSumm.sqlite3 | grep -v 'PRAGMA' | sed -e "s/DEFAULT (STRFTIME('%s','now'))//"  -e "s/'0000-00-00'/null/g" >> $(SQLITE_DUMPFILE) )
	@( psql $(CREDENTIALS_AWSPG) < $(SQLITE_DUMPFILE) > $(PGXFRLOG))

daily-comments-archived:
	#@echo "Building CSV from raw file"
	#@echo "building sqlite db"
	#@echo "Copying files to Box"

cleanRaw:
	( cd ../sampleData; cat raw.csv | tr '\r' '\n' > test.csv )

buildDB:
	( cd ../sampleData; ../utils/csv2db.py; )
