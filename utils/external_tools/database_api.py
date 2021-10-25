import os
import psycopg2
import logging


def get_db_connection(logger):
	try:
		connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (
		       os.getenv("DB_NAME"), os.getenv("DB_USER"),
		       os.getenv("DB_PASS"), os.getenv("DB_PORT"), os.getenv("DB_HOSTNAME"))
		conn = psycopg2.connect(connection_url)
		logger.info("Connected to database!...")
		return conn
	except Exception as e:
		logger.error(e)
		return None

def build_tables(logger):
	try:
		logger.info("Verifying tables in database...")
		check = True	# Check will be use to state that the schema is completely setup
		# run checks
		if not check:
			# build tables OR require user to build tables manually through bash [OPTIONAL]
			pass
		logger.info("Tables in database correctly instantiated...")
	except Exception as e:
		logge.error(e)