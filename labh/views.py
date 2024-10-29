from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'labh/home.html')

def account_list():
    pass

def account_detail():
    pass

def monthly_ledger():
    pass

def yearly_ledger():
    pass

def account_summary():
    pass

def stock_summary():
    pass

def networth():
    pass
