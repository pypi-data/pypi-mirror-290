import logging
import logging.config
import os, pathlib, csv, sys

# Add "modules" to sys.path
sys.path.append(os.path.join(pathlib.Path(__file__).resolve().absolute().parents[2])) 

from airports_pipeline_modules.postgres.postgres import Postgres
from airports_pipeline_modules.log_config.log_config import LoggingConf


loggingConfig = LoggingConf()
logging.config.dictConfig(loggingConfig.config)
logger = logging.getLogger(__name__)

filePath = os.path.join(os.path.abspath(os.getcwd()),'sources','airports.csv')


class Parser(object):

    def read_all_rows(self, filePath = filePath):
        with open(filePath, "r", newline="", encoding='utf-8') as csvfile:
            
            # reader = csv.DictReader(csvFile, dialect='excel', delimiter=',' )
            _reader = csv.reader(csvfile, dialect='excel', delimiter=',')
            for _row in _reader:
                print(_row)
   

    def insert_rows(self, database = None, tableName = None, filePath = filePath, commitSize = 1000):

        if not database:
            print("No database connection!")
            sys.exit()

        with open(filePath, "r", newline="", encoding="utf-8") as csvfile:

            # create the dictinary reader
            _reader = csv.DictReader(csvfile, dialect="excel", delimiter=',')

            database.create_table(tableName = tableName, fieldNames = _reader.fieldnames)

            _counter = commitSize
            _recordCount = 0
            _commitCount = 0
            _values = []

            for _row in _reader:               
                # Add the row to values to be inserted
                _values.append(_row)

                # Increse the recordCount and decrease the counter after INSERT
                _recordCount += 1
                _counter = _counter - 1 if _counter > 1 else commitSize

                if _counter == 1:
                    _commitCount += 1

                    ### This is where the commit happens
                    # Call the INSERT statement
                    database.insert(tableName = tableName, values = _values)
                    _values = []

                    print(f"commit {_commitCount}: {commitSize} rows have been commited")

            # No more rows to add but the last batch need to be inserted still   
            if not _counter == 1:
                _commitCount += 1

                database.insert(tableName = tableName, values = _values)
                _values = []

                print(f"commit {_commitCount}: {commitSize - _counter} rows have been commited")


            print(f"Record Count: {_recordCount}")
            print(f"Commit Count: {_commitCount}")

            # print(_reader.fieldnames)
            
if __name__ == '__main__':
    # csvParser = Parser()
    # csvParser.read_all_rows()

    # database = Postgres()
    # csvParser.insert_rows(database = database)

    logging.info("Hello")
            