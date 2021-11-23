# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 17:41:16 2021

@author: David
"""

from exceptions import *
from copy import copy


class Account():
  def __init__(self, account_id, name, brokerage, account_no):
    self.id = account_id
    self.name = name
    self.brokerage = brokerage
    self.account_no = account_no

    #dictionary to map fund ids to fund names
    self.fund_names = {}
    #dictionary to map AccountValue ids (account valuation on specific date) to AccountValue objects
    self.account_values = {}
    #dictionary to map date strings to account_value objects
    self.date_account_value = {}
    #dictionary to map fund.id to initial units
    self.initial_fund_units = {}

  def __str__(self):
    return("Name = %s, Brokerage = %s, Account Number = %s" % (self.name, self.brokerage, self.account_no))


  def insertIntoDB(self, con):
    sql_string = ("""INSERT into Accounts (name, brokerage, account_no)
                  VALUES("%s", "%s", "%s")"""
      % (self.name, self.brokerage, self.account_no))
    cursor = con.execute(sql_string)
    self.id = cursor.lastrowid
    con.commit()

  def fetchFunds(self, con):
    self.funds = []
    cursor = con.cursor()
    for row in cursor.execute("SELECT id, name, initial_units, account_id from Funds WHERE account_id = %d"
                              % self.id):
      self.funds += [makeFund(row)]
      self.fund_names[row[0]] = row[1]

  def fetchValues(self, con):
    """AccountValues for the given account, sorted by date"""
    self.values = []
    cursor = con.cursor()
    for row in cursor.execute("Select id, date, value, account_id FROM AccountValue \
                              WHERE account_id = %d ORDER BY date" % (self.id)):
     self.values += [makeAccountValue(row)]

  def initialize(self, con):
    self.fetchFunds(con)
    self.fetchValues(con)
    self. createFundIdx()
    self.initialUnitValues()
    self.processPurchases(con)

  def createFundIdx(self):
    self.fund_id_to_indx_dict = dict(zip([f.id for f in self.funds], list(range(len(self.funds)))))


  def initialUnitValues(self):
    for f in self.funds:
      self.initial_fund_units[f.id] = f.initial_units

  def processPurchases(self, con):
    self.purchases = []
    last_units = copy(self.initial_fund_units)
    for v in self.values:
      self.account_values[v.id] = v
      self.date_account_value[v.date] = v
      total_units = sum(last_units.values())
      v.unit_price = v.price/total_units
      purchases = v.fetchUnitPurchases(con, self.funds)
      for p in purchases:
        p.units_purchased = p.amount/v.unit_price
        last_units[p.fund_id] += p.units_purchased
        self.purchases += [p]
      v.units_out = copy(last_units)
      print(v.units_out)
    self.end_units = copy(last_units)



def makeAccount(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return Account(tuple4[0], tuple4[1], tuple4[2], tuple4[3])





class Fund():

  def __init__(self, fund_id, name, initial_units,  account_id):
    self.id = fund_id
    self.name = name
    self.initial_units= initial_units
    self.account_id = account_id

  def __str__(self):
    return "id = %d, name = %s, initial_units = %f, account_id = %d" \
      % (self.id, self.name, self.initial_units, self.account_id)

  def insertIntoDB(self, con):
    sql_string = ('INSERT into Funds (name, initial_units, account_id) VALUES("%s", %f,  %d)'
      % (self.name, self.initial_units, self.account_id))
    cursor = con.execute(sql_string)
    self.id = cursor.lastrowid
    con.commit()

def makeFund(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return Fund(tuple4[0], tuple4[1], tuple4[2], tuple4[3])



class AccountValue():

  def __init__(self, account_value_id, date, price, account_id):
    self.id = account_value_id
    self.date = date
    self.price = price
    self.account_id = account_id

  def __str__(self):
    return "id = %d, date = %s, price = %f, account_id = %d" % (self.id, self.date, self.price, self.account_id)

  def insertIntoDB(self, con):
    sql_string = ('INSERT into AccountValue (date, value, account_id) VALUES("%s", %f, %d)'
      % (self.date, self.price,  self.account_id))
    cursor = con.execute(sql_string)
    self.id = cursor.lastrowid
    con.commit()

  def fetchUnitPurchases(self, con, funds):
    purchases = []
    cursor = con.cursor()
    funds_str = str([f.id for f in funds]).strip('[]')
    for row in cursor.execute("SELECT UnitPurchase.id, fund_id, amount, date_id \
                              FROM UnitPurchase JOIN AccountValue ON UnitPurchase.date_id = AccountValue.id \
                              where fund_id in (%s) AND date_id = %d"
                              % (funds_str, self.id)):
      purchases += [makeUnitPurchase(row)]
    return purchases

def makeAccountValue(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return AccountValue(tuple4[0], tuple4[1], tuple4[2], tuple4[3])



class UnitPurchase():

  def __init__(self, purchase_id, fund_id, amount, date_id):
    self.id = purchase_id
    self.fund_id = fund_id
    self.amount = amount
    self.date_id = date_id

  def __str__(self):
    return "id = %d, fund_id = %d, amount = %f, date_id = %d" % (self.id, self.fund_id, self.amount, self.date_id)

  def insertIntoDB(self, con):
    sql_string = ('INSERT into UnitPurchase (fund_id, amount, date_id) VALUES("%s", %f, %d)'
      % (self.fund_id, self.amount, self.date_id))
    cursor = con.execute(sql_string)
    self.id = cursor.lastrowid
    con.commit()

def makeUnitPurchase(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return UnitPurchase(tuple4[0], tuple4[1], tuple4[2], tuple4[3])




