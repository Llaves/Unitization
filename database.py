
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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
