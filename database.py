
#
# © 2021 David Strip - david@stripfamily.net
#


import sqlite3 as sql
from os.path import exists
from db_objects import makeAccount, makeFund, makeUnitPurchase, makeAccountValue

#%%


def createDB(filename):
  "Creates sqlite db. Returns false if file already exists, otherwise returns db connection object"
  if exists(filename):
    return False
  else:
    con = sql.Connection(filename)
    initializeDB(con)
    return con

def connectDB(filename):
  "Connects to existing db. Returns false if db doesn't exist, otherwise returns connection object"
  if exists(filename):
    return sql.Connection(filename)
  else:
    return False


def initializeDB(con):
  "Creates initial tables in new db. Throws error if database previously initalized"
  initializeAcctTable(con)
  initializeFundTable(con)
  initializeAccountValueTable(con)
  initializeUnitPurchaseTable(con)


def initializeAcctTable(con):
  "Creates account table in db"
  con.execute("""
CREATE TABLE Accounts (
    id integer PRIMARY KEY,
	name text,
	brokerage text,
	account_no text)""")


def initializeFundTable(con):
  "Creates Fund Table in db"
  con.execute("""
CREATE TABLE Funds (
 	id integer PRIMARY KEY,
 	name text,
    initial_units,
 	account_id integer)""")

def initializeAccountValueTable(con):
  "Creates AccountValue table in db"
  con.execute("""
CREATE TABLE AccountValue (
 	id integer PRIMARY KEY,
 	date text,
 	value float,
 	account_id integer)""")


def initializeUnitPurchaseTable(con):
  "Creates Transaction table in db"
  con.execute("""
CREATE TABLE UnitPurchase (
 	id integer PRIMARY KEY,
 	fund_id integer,
 	amount decimal,
 	date_id integer)""")


def fetchAccounts(con):
  accounts = []
  cursor = con.cursor()
  for row in cursor.execute("SELECT id, name, brokerage, account_no from Accounts "):
    accounts += [makeAccount(row)]
  return accounts
