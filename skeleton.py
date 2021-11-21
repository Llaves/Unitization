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




#%%

test_file = 'skeleton.db'
if os.path.exists(test_file):
  os.remove(test_file)

con = createDB(test_file)

master = Account(1, "Master", "JPMorgan", "1239315x133")
master.insertIntoDB(con)
BofA = Account(2, "Second Account", "BankAmerica", "9832519314sv")
BofA.insertIntoDB(con)
corpus = Fund(1, "Corpus", 11234.153, master.id)
corpus.insertIntoDB(con)
Albin = Fund(2, "Albin", 0 ,  master.id)
Albin.insertIntoDB(con)
fund3 = Fund(3, "Acct2Fund1", 1000,  BofA.id)
fund3.insertIntoDB(con)
fund4 = Fund(4, "Acct2Fund2", 0,  BofA.id)
fund4.insertIntoDB(con)
master_price1 = AccountValue(2, "12/4/2020", 1000000, master.id)
master_price1.insertIntoDB(con)
master_price2 = AccountValue(1, "2/6/2021", 1500000, master.id)
master_price2.insertIntoDB(con)
BofA_price3 = AccountValue(3, "12/4/2020", 525000, BofA.id)
BofA_price3.insertIntoDB(con)
purchase1 = UnitPurchase(3, corpus.id, 1000000, master_price2.id)
purchase1.insertIntoDB(con)
purchase2 = UnitPurchase(2,Albin.id,250000, master_price1.id)
purchase2.insertIntoDB(con)
purchase3 = UnitPurchase(1, fund3.id, 525000, BofA_price3.id)
purchase3.insertIntoDB(con)
con.commit()
con.close()

#%%

con = connectDB(test_file)
accounts = fetchAccounts(con)
active_account  = accounts[0]
active_account.initialize(con)
active_account.initialUnitValues()


con.close()
