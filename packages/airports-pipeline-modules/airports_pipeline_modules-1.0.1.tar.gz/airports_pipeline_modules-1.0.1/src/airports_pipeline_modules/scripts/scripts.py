import os, sys, pathlib, logging
from zipfile import ZipFile
from jinja2 import BaseLoader, Environment

# Add "modules" to sys.path
sys.path.append(os.path.join(pathlib.Path(__file__).resolve().absolute().parents[2])) 

from airports_pipeline_modules.log_config.log_config import LoggingConf
from airports_pipeline_modules.main_config.main_config import Config

loggingConf = LoggingConf().config
logging.config.dictConfig(loggingConf)
logger = logging.getLogger(__file__)

config = Config().mainConfigDict

scriptsBasePath = config["script"]["scriptsBasePath"]
packedScriptsFileName = config["script"]["packedScriptsFileName"]
bucketName = config["upload"]["bucketName"]
hiveSchema = config["ddlh"]["hiveSchema"]
icebergSchema = config["ddlh"]["icebergSchema"]

# DDAE Credentials
host = config["ddlh"]["host"]
port = config["ddlh"]["port"]
username = config["ddlh"]["username"]
password = config["ddlh"]["password"]

# Postgresql Variables
postgresqlDBName = config["database"]["dbname"]
postgresqlSchema = config["database"]["schema"]
dbUsername = config["database"]["dbUsername"]
dbPassword = config["database"]["dbPassword"]
dbHost = config["database"]["dbHost"]
dbPort = config["database"]["dbPort"]

# S3 Variables
bucketName = config["upload"]["bucketName"]
endpoint = config["upload"]["endpoint"]
key = config["upload"]["key"]
secret = config["upload"]["secret"]

######################### Default Templates ###################################
######################### Catalog Definitions #################################
catalogsTemplateString = '''
# 0. Catalog and Cluster Definitions

# Postgresql Catalog
connector.name=postgresql
connection-user={{ dbUsername }}
connection-password={{ dbPassword }}
connection-url=jdbc:postgresql://{{ dbHost }}:{{ dbPort }}/{{ postgresqlDBName }}
cache-service.uri=http://cache-service:8180
redirection.config-source=SERVICE

# Hive Catalog
connector.name=hive
hive.iceberg-catalog-name=iceberg
hive.recursive-directories=true
hive.s3.aws-access-key={{ key }}
hive.s3.aws-secret-key={{ secret }}
hive.s3.endpoint=http://{{ endpoint }}
hive.s3.path-style-access=True
hive.s3.ssl.enabled=False
hive.security=system

# Iceberg Catalog
connector.name=iceberg
hive.s3.aws-access-key={{ key }}
hive.s3.aws-secret-key={{ secret }}
hive.s3.endpoint={{ endpoint }}
hive.s3.path-style-access=True
hive.s3.ssl.enabled=False
iceberg.file-format=PARQUET
iceberg.max-partitions-per-writer=6000
iceberg.security=system

# Table scan redirection
{
  "rules": [
    {
      "catalogName": "postgresext",
      "schemaName": "{{ postgresqlSchema }}",
      "tableName": "airports",
      "refreshInterval": "5m",
      "gracePeriod": "5m",
      "cacheCatalog": "hive",
      "cacheSchema": "cache_storage"
    }
  ]
}
'''

######################### PowerBI Definitions #################################
powerbiTemplateString = '''
# 6. DDAE Credentials For PowerBI

host: {{ host }}
port: {{ port }}
username: {{ username }}
password: {{ password }}
'''

######################### PostgreSQL ##########################################
postgresqlTemplateString = '''
-- 1. Postgresql Catalog Script

SHOW CATALOGS;
SHOW SCHEMAS FROM postgresext;
SHOW TABLES FROM postgresext.{{ postgresqlSchema }};
USE postgresext.{{ postgresqlSchema }};

SELECT * FROM airports;

-- Total number of airports in the world
SELECT COUNT(*) AS total FROM airports;

-- Total number of airports by type
SELECT DISTINCT(type) as "type", COUNT(*) AS total from airports
GROUP BY "type"
ORDER BY total DESC;

-- All the airport ids and names in the world 
SELECT id, name FROM airports;

-------------------------------------
---------- Cleanup Section ----------
-------------------------------------

-- Drop tables
DROP TABLE airports;
DROP TABLE airport-frequencies;
DROP TABLE runways;
DROP TABLE navaids;
DROP TABLE countries;
DROP TABLE regions;

-- Drop the schema
DROP SCHEMA hive.{{ postgresqlSchema }};
'''

######################### Hive ################################################
hiveTableTemplateSring = '''
-- 2. Hive Catalog Script

SHOW CATALOGS;
SHOW SCHEMAS FROM hive;

-- Create the schema
CREATE SCHEMA hive.{{ hiveSchema }}
WITH (location = 's3a://{{ bucketName }}/raw/');

-- Set schema to be the default
USE hive.{{ hiveSchema }};

-- Show tables and schema creation
SHOW TABLES from hive.{{ hiveSchema }};
SHOW CREATE SCHEMA hive.{{ hiveSchema }};

-- Explore Hive table creation options
SHOW SCHEMAS FROM system;
SHOW TABLES FROM system.metadata;
SELECT * FROM system.metadata.table_properties WHERE catalog_name = 'hive';

-- runways table columns and types
-- "id","airport_ref","airport_ident","length_ft","width_ft","surface",
-- "lighted","closed","le_ident","le_latitude_deg","le_longitude_deg",
-- "le_elevation_ft","le_heading_degT","le_displaced_threshold_ft",
-- "he_ident","he_latitude_deg","he_longitude_deg","he_elevation_ft",
-- "he_heading_degT","he_displaced_threshold_ft"

-- Create runways table
CREATE TABLE runways (id VARCHAR, airport_ref VARCHAR, airport_ident VARCHAR, 
                      length_ft VARCHAR, width_ft VARCHAR, surface VARCHAR, 
                      lighted VARCHAR, closed VARCHAR, le_ident VARCHAR, 
                      le_latitude_deg VARCHAR, le_longitude_deg VARCHAR, 
                      le_elevation_ft VARCHAR, le_heading_degT VARCHAR, 
                      le_displaced_threshold_ft VARCHAR, he_ident VARCHAR, 
                      he_latitude_deg VARCHAR, he_longitude_deg VARCHAR, 
                      he_elevation_ft VARCHAR, he_heading_degT VARCHAR, 
                      he_displaced_threshold_ft VARCHAR)
WITH (
    external_location = 's3a://{{ bucketName }}/raw/runways',
    format = 'CSV',
    skip_header_line_count = 1,
    csv_separator = ',');

-- Create runways_view view
CREATE VIEW runways_view AS
SELECT * FROM "hive"."{{ hiveSchema }}"."runways" LIMIT 10;

-- Select all from runways_view
SELECT * FROM runways_view;

-------------------------------------
---------- Cleanup Section ----------
-------------------------------------

-- Example backend table deletions
show tables from hive.{{ hiveSchema }};
DROP TABLE {{ hiveSchema }}_44ac4867_667d_45e3_a137_01e0f1ed9ba0;
DROP TABLE {{ hiveSchema }}_8de1656a_d3ab_4009_9d30_ed91d7f01697;
DROP TABLE {{ hiveSchema }}_73fc6e0b_3be0_441f_9dd3_81e55c41d830;
DROP TABLE {{ hiveSchema }}_e8673a25_d0db_421f_9f2e_92ec889f08c6;

-- Drop main table
DROP TABLE runways;

-- Drop the schema
DROP SCHEMA hive.{{ hiveSchema }};
'''

######################### Iceberg ################################################
icebergTableTemplateSring = '''
-- 4. Iceberg Catalog Script

SHOW CATALOGS;
SHOW SCHEMAS FROM iceberg;

CREATE SCHEMA iceberg.{{ icebergSchema }}
WITH (location = 's3a://{{ bucketName }}/{{ icebergSchema }}');

USE iceberg.{{ icebergSchema }};

-- Create extended_runways table
/* extended_runways columns
(airport_id INTEGER, name VARCHAR, ident VARCHAR, 
type VARCHAR, country_code VARCHAR, country_name VARCHAR, 
iso_region VARCHAR, municipality VARCHAR, runway_id VARCHAR, 
surface VARCHAR, lighted VARCHAR, closed VARCHAR, 
length_ft VARCHAR, widht_ft VARCHAR)
*/

CREATE TABLE extended_runways (airport_id INTEGER, name VARCHAR, 
                               airport_code VARCHAR, type VARCHAR, 
                               country_code VARCHAR, country_name VARCHAR, 
                               iso_region VARCHAR, municipality VARCHAR, 
                               runway_id VARCHAR, surface VARCHAR, lighted VARCHAR, 
                               closed VARCHAR, length_ft VARCHAR, width_ft VARCHAR)
WITH(
    location = 's3://{{ bucketName }}/{{ icebergSchema }}/extended_runways',
    format = 'PARQUET',
    partitioning = ARRAY['bucket(type, 2)'],
    sorted_by = ARRAY['country_code ASC', 'country_name ASC']
);


SHOW CREATE TABLE extended_runways;

-- Schema evolution
ALTER TABLE extended_runways RENAME COLUMN widht_ft TO width_ft;
ALTER TABLE extended_runways RENAME COLUMN ident TO airport_code;

-- Populate extented_runways table with CTE that spans Postgresql and Hive tables
INSERT INTO extended_runways

WITH airports AS (
    SELECT id AS airport_id, name AS airport_name, ident AS airport_code, 
    type, iso_country AS country_code, iso_region, municipality
    FROM "postgresext"."{{ postgresqlSchema }}"."airports" 
),

runways AS (
    SELECT CAST(airport_ref AS INTEGER) AS airport_id, id as runway_id, 
            surface, lighted, closed, length_ft, width_ft 
    FROM "hive"."{{ hiveSchema }}"."runways" 
),

countries AS (
    SELECT code AS country_code, name as country_name
    FROM "postgresext"."{{ postgresqlSchema }}"."countries"  
)

SELECT a.airport_id, a.airport_name, a.airport_code, a.type, 
a.country_code, c.country_name, a.iso_region, a.municipality, 
r.runway_id, r.surface, r.lighted, r.closed, r.length_ft, r.width_ft
FROM airports AS a
INNER JOIN runways AS r ON a.airport_id = r.airport_id
INNER JOIN countries AS c ON a.country_code = c.country_code;

SELECT * FROM extended_runways LIMIT 10;

-- Show recent queries
SELECT * FROM "system"."runtime"."queries" LIMIT 10;

-------------------------------------
---------- Cleanup Section ----------
-------------------------------------

-- Example backend table deletions
show tables from iceberg.{{ icerbergSchema }};
DROP TABLE {{ icerbergSchema }}_44ac4867_667d_45e3_a137_01e0f1ed9ba0;
DROP TABLE {{ icerbergSchema }}_8de1656a_d3ab_4009_9d30_ed91d7f01697;
DROP TABLE {{ icerbergSchema }}_73fc6e0b_3be0_441f_9dd3_81e55c41d830;
DROP TABLE {{ icerbergSchema }}_e8673a25_d0db_421f_9f2e_92ec889f08c6;

-- Drop main table
DROP TABLE extended_runways;
DROP TABLE runways;

-- Drop the schema
DROP SCHEMA iceberg.{{ icerbergSchema }}
'''

######################### View and Materialized View ################################################
viewsTemplateSring = '''
-- 5. View and Materialized View Script

SHOW TABLES FROM iceberg.{{ icebergSchema }};
USE iceberg.{{ icebergSchema }};

SELECT * FROM extended_runways LIMIT 1000;

-- Create a View for airports with runways which are lighted and open. Group by airport and sort by number of eligible runways.
CREATE OR REPLACE VIEW eligible_airports_view
-- Following is needed for Iceberg views. Default is DEFINER.
SECURITY INVOKER
AS
SELECT airport_id, name, airport_code, COUNT(*) as total_eligible_runways
FROM extended_runways
WHERE lighted = '1' AND closed = '0'
GROUP BY airport_id, name, airport_code
ORDER BY total_eligible_runways DESC;

-- Create cache schema in hive catalog for "Table Scan Redirect" feature. Queries against postgresext.airports.airports table should be directed to the following schema shortly after creating this.
CREATE SCHEMA IF NOT EXISTS hive.cache_storage WITH (location = 's3a://{{ bucketName }}/hive/cache_storage/');

-- Create a schema to host materialized views in hive catalog
CREATE SCHEMA IF NOT EXISTS hive.mv_data WITH (location = 's3a://{{ bucketName }}/hive/mv_data/');

-- Iceberg materialized views are problematic, therefore Hive is used.
-- Create a Materialized View
CREATE OR REPLACE MATERIALIZED VIEW hive.mv_data.eligible_airports_mview
AS
SELECT airport_id, name, airport_code, COUNT(*) as total_eligible_runways
FROM iceberg.{{ icebergSchema }}.extended_runways
WHERE lighted = '1' AND closed = '0'
GROUP BY airport_id, name, airport_code
ORDER BY total_eligible_runways DESC;

SELECT * FROM iceberg.{{ icebergSchema }}.eligible_airports_view;
SELECT * FROM hive.mv_data.eligible_airports_mview;

REFRESH MATERIALIZED VIEW hive.mv_data.eligible_airports_mview;

-------------------------------------
---------- Cleanup Section ----------
-------------------------------------

-- Drop views and materialized views
DROP VIEW iceberg.{{ icebergSchema }}.eligible_airports_view;
DROP MATERIALIZED VIEW hive.mv_data.eligible_airports_mview;
'''

######################### Unfied Queries ##########################################
federatedQueriesTemplateString = '''
-- 3. Federated Queries Script

-- Use SQL Common Table Execution (CTE) syntax to merge airports table from postresql database and runways external table from hive 
WITH airports AS (
    SELECT id, ident, type, name, continent, iso_country
    FROM "postgresext"."{{ postgresqlSchema }}"."airports" 
),

runways AS (
    SELECT CAST(airport_ref AS INTEGER) AS airport_id, id as runway_id, lighted, closed 
    FROM "hive"."{{ hiveSchema }}"."runways" 
)

SELECT airports.*, runways.*
FROM airports
INNER JOIN runways ON airports.id = runways.airport_id
ORDER BY id, iso_country;

-- Count of lighted and open runways per airport ordered by the count of those eligible runways 
WITH airports AS (
    SELECT id, ident, type, name, continent, iso_country
    FROM "postgresext"."{{ postgresqlSchema }}"."airports" 
),

runways AS (
    SELECT CAST(airport_ref AS INTEGER) AS airport_id, id AS runway_id, lighted, closed 
    FROM "hive"."{{ hiveSchema }}"."runways" 
)

SELECT airports.name, iso_country, COUNT(*) AS "total_runways"
FROM airports
INNER JOIN runways ON airports.id = runways.airport_id
GROUP BY airports.name, iso_country
ORDER BY total_runways DESC;

-- List of airports sorted by highest closed runways
WITH airports AS (
    SELECT id, ident, type, name, continent, iso_country
    FROM "postgresext"."{{ postgresqlSchema }}"."airports" 
),

runways AS (
    SELECT CAST(airport_ref AS INTEGER) AS airport_id, id as runway_id, lighted, closed 
    FROM "hive"."{{ hiveSchema }}"."runways" 
)

SELECT airports.name, iso_country, COUNT(*) AS "total_runways_closed"
FROM airports
INNER JOIN runways ON airports.id = runways.airport_id
WHERE runways.closed = '1'
GROUP BY airports.name, iso_country
ORDER BY total_runways_closed DESC;
'''

class Script(object):

    def __init__(self, scriptsBasePath = scriptsBasePath, packedScriptsFileName = packedScriptsFileName,
                 host = host, port = port, username = username, password = password,  
                 endpoint = endpoint, bucketName = bucketName, key = key, secret = secret,
                 hiveSchema = hiveSchema, icebergSchema = icebergSchema, 
                 dbHost= dbHost, dbPort= dbPort, dbUsername = dbUsername, dbPassword = dbPassword, postgresqlDBName = postgresqlDBName, postgresqlSchema = postgresqlSchema ):
        
        self.scriptsPath = os.path.join(pathlib.Path(__file__).resolve().parents[2], scriptsBasePath)
        
        # DDAE Variables
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        # Hive And Iceberg Variables
        self.hiveSchema = hiveSchema
        self.icebergSchema = icebergSchema

        # PostgreSQL Variables
        self.postgresqlSchema = postgresqlSchema
        self.dbUsername = dbUsername
        self.dbPassword = dbPassword
        self.postgresqlDBName = postgresqlDBName
        self.dbHost = dbHost
        self.dbPort = dbPort

        # S3 Variables
        self.endpoint = endpoint
        self.bucketName = bucketName
        self.key = key
        self.secret = secret

        try:
            (os.path.exists(self.scriptsPath) and os.path.isdir(self.scriptsPath)) or os.makedirs(name = self.scriptsPath)
        except Exception as err:
            logger.critical(msg = f"Cannot find or create {self.scriptsPath}, aborting...")
            sys.exit()
        
        self.zipFile = os.path.join(self.scriptsPath, packedScriptsFileName)

    def create_catalogs_script(self):
        
        try:
            # Load catalog template from string
            
            _env = Environment( loader = BaseLoader )
            _catalogsTemplate = _env.from_string( source = catalogsTemplateString )

            # Render the template
            _catalogsRenderedTemplate = _catalogsTemplate.render( dbHost = self.dbHost, dbPort = self.dbPort, dbUsername = self.dbUsername, dbPassword = self.dbPassword, postgresqlDBName = self.postgresqlDBName, postgresqlSchema = self.postgresqlSchema, 
                                                                 key = self.key, secret = self.secret, endpoint = self.endpoint )

            # Write the template into the script file
            _catalogsScriptPath = os.path.join( self.scriptsPath, "0_catalog_definitions.txt")
            with open(_catalogsScriptPath, "w") as file:
                file.write(_catalogsRenderedTemplate)

        except Exception as err:
            logger.error(err)
            return False
        
        self.catalogs = _catalogsRenderedTemplate

    def create_powerbi_script(self):
        
        try:
            # Load powerbi template from string
            
            _env = Environment( loader = BaseLoader )
            _powerbiTemplate = _env.from_string( source = powerbiTemplateString )

            # Render the template
            _powerbiRenderedTemplate = _powerbiTemplate.render( host = self.host, port = self.port, username = self.username, password = self.password )

            # Write the template into the script file
            _powerbiScriptPath = os.path.join( self.scriptsPath, "6_ddae_credentials_for_powerbi.txt")
            with open(_powerbiScriptPath, "w") as file:
                file.write(_powerbiRenderedTemplate)

        except Exception as err:
            logger.error(err)
            return False
        
        self.powerbi = _powerbiRenderedTemplate
        

    def create_postgresql_script(self):
        
        try:
            # Load postgresql template from string
            
            _env = Environment( loader = BaseLoader )
            _postgresqlTemplate = _env.from_string( source = postgresqlTemplateString )

            # Render the template
            _postgresqlRenderedTemplate = _postgresqlTemplate.render( postgresqlSchema = self.postgresqlSchema )

            # Write the template into the script file
            _postgresqlScriptPath = os.path.join( self.scriptsPath, "1_postgresql_catalog.txt")
            with open(_postgresqlScriptPath, "w") as file:
                file.write(_postgresqlRenderedTemplate)

        except Exception as err:
            logger.error(err)
            return False
        
        self.postgresql = _postgresqlRenderedTemplate

    def create_hive_script(self):
        
        try:
            # Load the hive template from string
            
            _env = Environment( loader = BaseLoader )
            _hiveTemplate = _env.from_string( source = hiveTableTemplateSring )

            # Render the template
            _hiveRenderedTemplate = _hiveTemplate.render( bucketName = self.bucketName, hiveSchema = self.hiveSchema )

            # Write the template into the script file
            _hiveScriptPath = os.path.join( self.scriptsPath, "2_hive_catalog.txt")
            with open(_hiveScriptPath, "w") as file:
                file.write(_hiveRenderedTemplate)

        except Exception as err:
            logger.error(err)
            return False

        self.hive = _hiveRenderedTemplate
    
    def create_iceberg_script(self):
        
        try:
            # Load the iceberg template from string
            _env = Environment( loader = BaseLoader )
            _icebergTemplate = _env.from_string( source = icebergTableTemplateSring )

            # Render the template
            _icebergRenderedTemplate = _icebergTemplate.render( bucketName = self.bucketName, postgresqlSchema = self.postgresqlSchema, 
                                                                hiveSchema = self.hiveSchema, icebergSchema = self.icebergSchema  )

            # Write the template into the script file
            _icebergScriptPath = os.path.join( self.scriptsPath, "4_iceberg_catalog.txt")
            with open(_icebergScriptPath, "w") as file:
                file.write(_icebergRenderedTemplate)

        except Exception as err:
            logger.error(err)
            return False
        
        self.iceberg = _icebergRenderedTemplate

    def create_views_script(self):
        
        try:
            # Load the hive template from string
            _env = Environment( loader = BaseLoader )
            _viewsTemplate = _env.from_string( source = viewsTemplateSring )

            # Render the template
            _viewsRenderedTemplate = _viewsTemplate.render( bucketName = self.bucketName, postgresqlSchema = self.postgresqlSchema, 
                                                                hiveSchema = self.hiveSchema, icebergSchema = self.icebergSchema  )

            # Write the template into the script file
            _viewsScriptPath = os.path.join( self.scriptsPath, "5_view_mview_definitions.txt")
            with open(_viewsScriptPath, "w") as file:
                file.write(_viewsRenderedTemplate)

        except Exception as err:
            logger.error(err)
            return False
        
        self.views = _viewsRenderedTemplate
        
    def create_federated_queries_script(self):
        
        try:
            # Load the hive template from string
            _env = Environment( loader = BaseLoader )
            _federatedQueriesTemplate = _env.from_string( source = federatedQueriesTemplateString )

            # Render the template
            _federatedQueriesRenderedTemplate = _federatedQueriesTemplate.render( bucketName = self.bucketName, postgresqlSchema = self.postgresqlSchema, 
                                                                hiveSchema = self.hiveSchema, icebergSchema = self.icebergSchema  )

            # Write the template into the script file
            _unifiedQueriesScriptPath = os.path.join( self.scriptsPath, "3_postresql_hive_federated_queries.txt")
            with open(_unifiedQueriesScriptPath, "w") as file:
                file.write(_federatedQueriesRenderedTemplate )

        except Exception as err:
            logger.error(err)
            return False
        
        self.federated = _federatedQueriesRenderedTemplate
        
    
    def pack_scripts(self):
        fileList = os.listdir(self.scriptsPath)
        print(fileList)

        with ZipFile(file = self.zipFile, mode = "w") as _zipFile:
            _currentPath = os.getcwd()
            os.chdir(self.scriptsPath)

            for file in fileList:
                filePath = os.path.join(self.scriptsPath, file)

                if os.path.isfile(filePath) and not file.endswith(".zip"):
                    logger.debug(filePath)
                    _zipFile.write(file)
            
            os.chdir(_currentPath)


if __name__ == '__main__':

    scriptCreator = Script()
    scriptCreator.create_catalogs_script()
    scriptCreator.create_powerbi_script()
    scriptCreator.create_hive_script()
    scriptCreator.create_iceberg_script()
    scriptCreator.create_postgresql_script()
    scriptCreator.create_views_script()
    scriptCreator.create_federated_queries_script()
    scriptCreator.pack_scripts()
    


            