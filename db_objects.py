# -*- coding: utf-8 -*-

#
# © 2021 David Strip - david@stripfamily.net
#


from exceptions import *
from copy import copy
from openpyxl import Workbook


class Account():
  def __init__(self, account_id, name, brokerage, account_no):
    self.id = account_id
    self.name = name
    self.brokerage = brokerage
    self.account_no = account_no

   
    #dictionary to map fund ids to fund names
    self.fund_names = {}
    #dictionary to map AccountValue ids (account valuation on specific date) to AccountValue objects
    self.account_values_by_id = {}
    #dictionary to map fund.id to initial units
    self.initial_fund_units = {}
    #dictionary to map fund.id to ending units
    self.end_units = {} # This is initialized in processPurchases
    #account values list
    self.account_values_sorted_by_date = []

    # flag that the account has already been initialized
    self.initialized = False

  def __str__(self):
    return("Name = %s, Brokerage = %s, Account Number = %s" % (self.name, self.brokerage, self.account_no))

  def copy(self, account):
    self.id = account.id
    self.name = account.name
    self.brokerage = account.brokerage
    self.account_no = account.account_no

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

  def addFund(self, new_fund, con):
    self.funds += [new_fund]
    self.fund_names[new_fund.id] = new_fund.name
    self.initialUnitValues()
    self.processPurchases(con)

  def fundChanged(self, con):
    self.initialUnitValues()
    self.processPurchases(con)

  def deleteFund(self, fund, con):
    fund.deletePurchases(con)
    sql_string = "DELETE FROM Funds WHERE id = %d" % fund.id
    con.execute(sql_string)
    con.commit()
    del self.fund_names[fund.id]
    del self.initial_fund_units[fund.id]
    self.funds.remove(fund)
    self.processPurchases(con)

  # the following delete functions are only for use in deleting an entire account. They do not clean up
  # the auxilliary indices and such.

  def deleteAllFunds(self, con):
    sql_string = "DELETE FROM Funds WHERE account_id = %d" % self.id
    con.execute(sql_string)
    con.commit()

  def deleteAllAccountValues(self, con):
    sql_string = "DELETE FROM AccountValue WHERE account_id = %d" % self.id
    con.execute(sql_string)
    con.commit()

  def deleteAccount(self, con):
    self.deleteAllFunds(con)
    self.deleteAllAccountValues(con)
    sql_string = "DELETE FROM Accounts WHERE id = %d" % self.id
    con.execute(sql_string)
    con.commit()

  def updateToDB(self, con):
    sql_string = 'UPDATE Accounts SET name = "%s", brokerage = "%s", account_no = "%s" ' \
      'WHERE id = %d'  % (self.name, self.brokerage, self.account_no, self.id)
    con.execute(sql_string)
    con.commit()

  def fetchValues(self, con):
    """AccountValues for the given account, sorted by date"""
    cursor = con.cursor()
    for row in cursor.execute("Select id, date, value, account_id FROM AccountValue " \
                                "WHERE account_id = %d ORDER BY date" % (self.id)):
      v = makeAccountValue(row)
      self.account_values_sorted_by_date += [v]

  def addValue(self, value):
    self.account_values_sorted_by_date += [value]
    #the list is sorted, so sort to maintain order
    self.account_values_sorted_by_date.sort(key = lambda av: av.date)

  def initialize(self, con):
    if (not self.initialized):
      self.fetchFunds(con)
      self.fetchValues(con)
      self.initialUnitValues()
      self.processPurchases(con)
      self.initialized = True

  def initialUnitValues(self):
    for f in self.funds:
      self.initial_fund_units[f.id] = f.initial_units

  def initialUnitValuesIsZero(self):
    return sum(self.initial_fund_units.values()) == 0

  #We find all the purchases by looking at the fund evaluation dates and finding the purchases associated with that date
  #By processing the fund evaluations in order, we can calculate the number of units of each fund that were purchased.
  #While we could just store the number of units at the purchase date, this would make it very hard to calculate the
  #number of units if we have to edit the purchase amount, the fund value, or add a missed purchase.

  def processPurchases(self, con):
    """Process the purchases for the account, updating the account values and the fund units"""
    self.purchases = []
    last_units = copy(self.initial_fund_units)
    if not self.initialUnitValuesIsZero():
      for v in self.account_values_sorted_by_date:
        self.account_values_by_id[v.id] = v
        total_units = sum(last_units.values())
        v.unit_price = v.value/total_units
        purchases = v.fetchUnitPurchases(con, self.funds) #get the purchases for this date
        for p in purchases:
          p.units_purchased = p.amount/v.unit_price
          last_units[p.fund_id] += p.units_purchased
          self.purchases += [p]
        v.units_out = copy(last_units)
    self.end_units = copy(last_units)
    self.total_units = sum(self.end_units.values())

  def exportXLSX(self, file_name):
    wbk = Workbook()
    funds_sheet = wbk.active
    funds_sheet.title = "Funds"
    funds_sheet.append(["Name", "Initial Units", "Ending Units"])
    funds_sheet.column_dimensions['A'].width = 25
    funds_sheet.column_dimensions['B'].width = 15
    funds_sheet.column_dimensions['C'].width = 15
    for f in self.funds:
      funds_sheet.append([f.name, f.initial_units, self.end_units[f.id]])
    purchases_sheet = wbk.create_sheet("Purchases")
    purchases_sheet.append(["Date", "Fund Name", "Amount", "Units Purchased"])
    purchases_sheet.column_dimensions['A'].width = 15
    purchases_sheet.column_dimensions['B'].width = 25
    purchases_sheet.column_dimensions['C'].width = 15
    purchases_sheet.column_dimensions['D'].width = 15
    for p in self.purchases:
      purchases_sheet.append([self.account_values_by_id[p.date_id].date,
                              self.fund_names[p.fund_id],
                              p.amount, p.units_purchased])
    account_values_sheet = wbk.create_sheet("Account Values")
    account_values_sheet.append(["Date", "Account Value"])
    account_values_sheet.column_dimensions['A'].width = 15
    account_values_sheet.column_dimensions['B'].width = 15
    for av in self.account_values_sorted_by_date:
      account_values_sheet.append([av.date, av.value])
    wbk.save(file_name)

  ##class ends

def makeAccount(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return Account(tuple4[0], tuple4[1], tuple4[2], tuple4[3])


###############################
##
##  Fund
##
###############################


class Fund():

  def __init__(self, fund_id, name, initial_units,  account_id):
    self.id = fund_id
    self.name = name
    self.initial_units= initial_units
    self.account_id = account_id

  def __str__(self):
    return "id = %d, name = %s, initial_units = %f, account_id = %d" \
      % (self.id, self.name, self.initial_units, self.account_id)

  def copy(self, fund):
    self.id = fund.id
    self.name = fund.name
    self.initial_units = fund.initial_units
    self.account_id = fund.account_id

  def insertIntoDB(self, con):
    sql_string = ('INSERT into Funds (name, initial_units, account_id) VALUES("%s", %f,  %d)'
      % (self.name, self.initial_units, self.account_id))
    cursor = con.execute(sql_string)
    self.id = cursor.lastrowid
    con.commit()

  def updateToDB(self, con):
    sql_string = 'UPDATE Funds SET name = "%s", initial_units = %f, account_id = %d ' \
      'WHERE id = %d'  % (self.name, self.initial_units, self.account_id, self.id)
    con.execute(sql_string)
    con.commit()

  def deletePurchases(self, con):
    sql_string = ('DELETE FROM UnitPurchase WHERE fund_id = %d' % self.id)
    con.execute(sql_string)
    con.commit()

  ## class ends

def makeFund(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return Fund(tuple4[0], tuple4[1], tuple4[2], tuple4[3])

###############################
##
##  AccountValue
##
###############################


class AccountValue():

  def __init__(self, account_value_id, date, value, account_id):
    self.id = account_value_id
    self.date = date
    self.value = value
    self.account_id = account_id

  def __str__(self):
    return "id = %d, date = %s, value = %f, account_id = %d" % (self.id, self.date, self.value, self.account_id)

  def copy(self, account_value):
    self.id = account_value.id
    self.date = account_value.date
    self.value = account_value.value
    self.account_id = account_value.account_id

  def insertIntoDB(self, con):
    sql_string = ('INSERT into AccountValue (date, value, account_id) VALUES("%s", %f, %d)'
      % (self.date, self.value,  self.account_id))
    cursor = con.execute(sql_string)
    self.id = cursor.lastrowid
    con.commit()

  def updateToDB(self, con):
    sql_string = 'UPDATE AccountValue SET date = "%s", value = %f, account_id = %d WHERE id = %d' \
      % (self.date, self.value, self.account_id, self.id)
    con.execute(sql_string)
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

  ##class ends

def makeAccountValue(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return AccountValue(tuple4[0], tuple4[1], tuple4[2], tuple4[3])

###############################
##
##  UnitPurchase
##
###############################


class UnitPurchase():

  def __init__(self, purchase_id, fund_id, amount, date_id):
    self.id = purchase_id
    self.fund_id = fund_id
    self.amount = amount
    self.date_id = date_id

  def __str__(self):
    return "id = %d, fund_id = %d, amount = %f, date_id = %d" % (self.id, self.fund_id, self.amount, self.date_id)

  def copy(self, unit_purchase):
    self.id = unit_purchase.id
    self.fund_id = unit_purchase.fund_id
    self.amount = unit_purchase.amount
    self.date_id = unit_purchase.date_id

  def insertIntoDB(self, con):
    sql_string = ('INSERT into UnitPurchase (fund_id, amount, date_id) VALUES("%s", %f, %d)'
      % (self.fund_id, self.amount, self.date_id))
    cursor = con.execute(sql_string)
    self.id = cursor.lastrowid
    con.commit()

  def updateToDB(self, con):
    sql_string = 'UPDATE UnitPurchase SET fund_id = %d, amount = %f, date_id = %d WHERE id = %d' % \
      (self.fund_id, self.amount, self.date_id, self.id)
    con.execute(sql_string)
    con.commit()

  def deleteFromDB(self, con):
    sql_string = ('DELETE FROM UnitPurchase WHERE id = %d' % self.id)
    con.execute(sql_string)
    con.commit()


  ##class ends


def makeUnitPurchase(tuple4):
  if len(tuple4) != 4:
    raise TupleLengthError()
  return UnitPurchase(tuple4[0], tuple4[1], tuple4[2], tuple4[3])




###############################
##
##  Helper functions
##
###############################

def fillCell(s, r, c, v):
  s.cell(row = r, column = c).value = v
