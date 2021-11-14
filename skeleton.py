# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 10:16:23 2021

@author: David
"""

from db_objects import Account, Fund, AccountValue, UnitPurchase
from database import createDB, connectDB, fetchAccounts
import accounting as acc

import os

#%%

acct1 = Account(1, "Master", "JPMorgan", "1239315x133")
acct2 = Account(2, "Second Account", "BankAmerica", "9832519314sv")
fund1 = Fund(1, "Corpus", 11234.153, 1)
fund2 = Fund(2, "Albin", 0 ,  1)
fund3 = Fund(3, "Acct2Fund1", 1000,  2)
fund4 = Fund(4, "Acct2Fund2", 0,  2)
price1 = AccountValue(2, "12/4/2020", 1000000, 1)
price2 = AccountValue(1, "2/6/2021", 1250000,1)
price3 = AccountValue(3, "12/4/2020", 525000, 2)
purchase1 = UnitPurchase(3, 1, 1000000, 1)
purchase2 = UnitPurchase(2,2,250000,2)
purchase3 = UnitPurchase(1, 3, 525000, 3)


#%%

test_file = 'test.db'
if os.path.exists(test_file):
  os.remove(test_file)

con = createDB(test_file)
acct1.insertIntoDB(con)
acct2.insertIntoDB(con)
fund1.insertIntoDB(con)
fund2.insertIntoDB(con)
fund3.insertIntoDB(con)
fund4.insertIntoDB(con)
price2.insertIntoDB(con)
price1.insertIntoDB(con)
price3.insertIntoDB(con)
purchase3.insertIntoDB(con)
purchase2.insertIntoDB(con)
purchase1.insertIntoDB(con)
con.commit()
con.close()

#%%

con = connectDB(test_file)
accounts = fetchAccounts(con)
active_account  = accounts[0]
active_account.initialize(con)
active_account.initialUnitValues(con)


con.close()
