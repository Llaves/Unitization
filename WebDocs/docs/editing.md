Editing your accounts should only be done with great care. When you go back in time to change a value or add a new purchase, it has an impact on every subsequent purchase. This is because you are changing the number of existing units from that point in time forward, changing the value of units at every purchase point after that. There are times when edits are unavoidable, but be aware of the ripple effects. If you have been providing donors with stewardship reports, the value of their accounts will have changed for reporting periods after the date on the edit (not the date when the edit occurred, but the date for which a purchase was changed or added.) In addition, there is no "undo" capability. You should backup your `accounts.db` file before starting edits and keep track of the name of the file so that you can restore the previous state if necessary. 

## Enabling Editing

By default the edit functions are not available. You may have noticed that menu items related to editing are grayed-out, preventing you from using them. Likewise, double-clicking on a cell has no effect. You can enable editing by cllcking `Advanced->Edit Mode` on the main menu or using the `Alt-E` shortcut key.

![Edit Mode](img/edit_mode.png)

## Disabling Warnings

Because of the potential for damaging your records, all edits are accompanied with a warning that you must confirm before the edit is committed. If you're doing a lot of edits you can disable the warnings from `Advanced->No Warnings` menu item or using the `Alt-W` shortcut key. You are on your own if you disable the warnings. 

## Editing the Account Information

As noted in the section *Getting Started*, the account information is for your use only. It carries no significance within the UnitTracker program. Editing this information will have no impact on the count of units. You might want to edit if you've changed investment advisor or brokerage firm or perhaps because account numbers have changed. As in the case of all edits, there is no undo. You can always manually edit back to the original information, but you will have to know the values in order to do that. You can only edit the currently open account.

To edit account information, click `Accounts->Edit Account`

![Edit Account Menu](img/edit_account.png)

This will pop up the edit dialog:

![Edit Current Account](img/edit_current_account.png)

Make the changes you desire and click `Save`. If you change your mind about editing the account, just click `Cancel`.

## Deleting an Account

There aren't very many good reasons for deleting an account, especially if you are a non-profit and the only account in the database is yours. You will lose all your information and history if you delete an account. Deleting an account is mostly useful if you were experimenting and created one or more accounts to experiment with and want to clean up your databae. If you are an investment advisor to multiple non-profits, you might want to delete an account that you no longer manage. Be reminded that once you delete an account you cannot recover the data unless you restore from a backup, which has it's own consequences. 

To delete an account, click `Accounts->Delete Account`

![Delete Account](img/delete_account.png)

This dialog will pop-up:

![Delete Account Dialog](img/delete_account_dialog.png)

You can select any account *except the currently open account* to delete. If you select the open account, the request will be refused. 
