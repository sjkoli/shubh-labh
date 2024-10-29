from django.db import models
from labh.choices import ACCOUNT_TYPES, STOCK_EXCHANGES, TRX_TYPES, TRADE_TYPES, ACCOUNT_STATUS
from django.db.models.signals import post_save, post_init, pre_delete
from django.dispatch import receiver

class Account(models.Model):
    bank_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    branch = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    micr_code = models.CharField(max_length=20, blank=True, null=True)
    login_id = models.CharField(max_length=20, blank=True, null=True)
    account_holder = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    status = models.CharField(max_length=20, choices=ACCOUNT_STATUS, default="Active")
    opening_date = models.DateField(default=None, blank=True, null=True)    
    remarks = models.CharField(max_length=200, default=None, null=True, blank=True)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.account_holder

class CatLevel1(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

class CatLevel2(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

class CatLevel3(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title
    

    
class Transaction(models.Model):
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    trx_id = models.CharField(max_length=50, default=None, null=True, blank=True)
    trx_date = models.DateField()
    trx_description = models.CharField(max_length=200)
    trx_type = models.CharField(max_length=10, choices=TRX_TYPES)
    cat_lev_1 = models.ForeignKey(CatLevel1, on_delete=models.SET_NULL, null=True, blank=True)
    cat_lev_2 = models.ForeignKey(CatLevel2, on_delete=models.SET_NULL, null=True, blank=True)
    cat_lev_3 = models.ForeignKey(CatLevel3, on_delete=models.SET_NULL, null=True, blank=True)
    trx_amount = models.DecimalField(max_digits=12, decimal_places=2)
    trx_remarks = models.CharField(max_length=200, default=None, null=True, blank=True)
  
    def __str__(self):        
        return self.trx_type

@receiver(post_init, sender=Transaction, dispatch_uid="init")
def hold_trx_amount(sender, instance, **kwargs):
    instance._old_trx_amount = instance.trx_amount 
    instance._old_trx_type = 0.0 if instance.trx_type is None else instance.trx_type
    
# method for updating
@receiver(post_save, sender=Transaction, dispatch_uid="update_balance")
def update_balance(sender, instance, **kwargs):
    print("Updating Balance on edit or create")
    #print(kwargs.get('raw')) # raw is true when loading fixtures
    if instance._old_trx_amount is None or kwargs.get('raw') is True:
        print("New Transaction")
        if instance.trx_type == "CR":
            instance.account_number.balance = instance.account_number.balance + instance.trx_amount
        else:
            instance.account_number.balance = instance.account_number.balance - instance.trx_amount
    else:
        print("Edit Transaction")
        if instance.trx_type == instance._old_trx_type: # trx_type did not change
            if instance.trx_type == "CR":
                instance.account_number.balance = instance.account_number.balance + instance.trx_amount - instance._old_trx_amount
            else:
                instance.account_number.balance = instance.account_number.balance - instance.trx_amount + instance._old_trx_amount
        else: # trx_type changed
            if instance.trx_type == "CR":
                instance.account_number.balance = instance.account_number.balance + instance.trx_amount + instance._old_trx_amount
            else:
                instance.account_number.balance = instance.account_number.balance - instance.trx_amount - instance._old_trx_amount

    instance.account_number.save()

@receiver(pre_delete, sender=Transaction, dispatch_uid="update_balance_on_delete")
def update_balance_on_delete(sender, instance, **kwargs):
    print("Update Balance on delete transaction")
    print(instance.trx_amount)
    if instance.trx_type == "CR":
        instance.account_number.balance = instance.account_number.balance - instance.trx_amount
    else:
        instance.account_number.balance = instance.account_number.balance + instance.trx_amount 
    
    instance.account_number.save()

    
class Stock(models.Model):
    isin = models.CharField(max_length=20, unique=True)
    stock_symbol = models.CharField(max_length=50)
    stock_name = models.CharField(max_length=100)
    stock_exchange = models.CharField(max_length=10, choices=STOCK_EXCHANGES)

    def __str__(self):
        return self.stock_symbol
    
class StockPrice(models.Model):
    stock_symbol = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price_date = models.DateField()
    close_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.stock_symbol.stock_symbol
    
class StockTradeBook(models.Model):
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    trade_id = models.CharField(max_length=50) # order_id
    trade_date = models.DateField()
    stock_symbol = models.ForeignKey(Stock, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPES) 
    stock_exchange = models.CharField(max_length=10, choices=STOCK_EXCHANGES, default="NSE")
    quatity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    trade_amount = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.CharField(max_length=200, default=None, null=True, blank=True)
    

    def __str__(self):
        return self.stock_symbol.stock_symbol
    
class StockHolding(models.Model):
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock_symbol = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quatity = models.IntegerField()
    stock_exchange = models.CharField(max_length=10, choices=STOCK_EXCHANGES)
    avg_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.stock_symbol.stock_symbol

class MutualFund(models.Model):
    amc = models.CharField(max_length=50)
    fund_name = models.CharField(max_length=100)
    isin = models.CharField(max_length=20)
    scheme_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.fund_name
    
class MutualFundNav(models.Model):
    fund_name = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    nav = models.DecimalField(max_digits=9, decimal_places=4)
    nav_date = models.DateField()

    def __str__(self):
        return self.fund_name
    
class MutualFundTradeBook(models.Model):
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    trade_id = models.CharField(max_length=50) # order_id
    trade_date = models.DateField()
    fund_name = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=10, choices=TRADE_TYPES) 
    trade_amount = models.DecimalField(max_digits=12, decimal_places=2)
    units = models.DecimalField(max_digits=9, decimal_places=4)

    def __str__(self):
        return self.fund_name.fund_name

class MutualFundHolding(models.Model):
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    fund_name = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    folio_number = models.CharField(max_length=50)
    units = models.DecimalField(max_digits=9, decimal_places=4)
    invested_amount = models.FloatField()

    def __str__(self):
        return "{0}-{1}".format(self.fund_name.fund_name, self.folio_number)
    
