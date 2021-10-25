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