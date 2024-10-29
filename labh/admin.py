from django.contrib import admin
from .models import Account, Transaction, CatLevel1, CatLevel2, CatLevel3
from .models import Stock, StockPrice, StockTradeBook, StockHolding
from .models import MutualFund, MutualFundNav, MutualFundTradeBook, MutualFundHolding

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank_name', 'account_number', 'account_holder', 'balance', 'account_type')
    #search_fields = ('account_number', 'account_name')
    list_filter = ('account_type','status')
    #ordering = ('account_type', )

admin.site.register(Account, AccountAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_number', 'cat_lev_1', 'cat_lev_2', 'cat_lev_3', 'trx_date', 'trx_description', 'trx_type', 'trx_amount')
    list_filter = ('account_number','trx_date')

admin.site.register(Transaction, TransactionAdmin)

class CatLevel1Admin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('title', )

admin.site.register(CatLevel1, CatLevel1Admin)

class CatLevel2Admin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('title', )

admin.site.register(CatLevel2, CatLevel2Admin)

class CatLevel3Admin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('title', )

admin.site.register(CatLevel3, CatLevel3Admin)


admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(StockTradeBook)
admin.site.register(StockHolding)
admin.site.register(MutualFund)
admin.site.register(MutualFundNav)
admin.site.register(MutualFundTradeBook)
admin.site.register(MutualFundHolding)
