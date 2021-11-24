from django.shortcuts import render, redirect
from .models import Account, AdminLogin, Statement
from  django.core.exceptions import ObjectDoesNotExist
import datetime
# Create your views here.

def index(request):
    return render(request, "index.html")
def createaccount(request):
    return render(request, "createaccount.html")
def create(request):
    acno = request.POST['acno']
    name = request.POST['name']
    address = request.POST['address']
    contactno = request.POST['contactno']
    emailaddress = request.POST['emailaddress']
    panno = request.POST['panno']
    aadharno = request.POST['aadharno']
    balance = request.POST['balance']
    password = request.POST['password']
    ac = Account(acno=acno, name=name, address=address, contactno=contactno, emailaddress=emailaddress, panno=panno, aadharno=aadharno, balance=balance, password=password)
    ac.save()
    return redirect('index')

def login(request):
    return  render(request, "login.html")

def logcode(request):
    acno = request.POST['acno']
    password = request.POST['password']
    op = request.POST['op']
    msg =''
    try:
        obj = Account.objects.get(acno=acno, password=password )
        if obj is not None:
            if op == "deposit":
                acno = obj.acno
                request.session['acno'] = acno
                return render(request, "deposit.html")
            elif op == "withdraw":
                acno = obj.acno
                request.session['acno'] = acno
                return render(request, "withdraw.html")
            elif op == "transfer":
                acno = obj.acno
                request.session['acno'] = acno
                return render(request, "transfer.html")
            elif op == "statement":
                acno = obj.acno
                stmt = Statement.objects.filter(fromaccount = acno)
                return render(request, "statement.html",{'stmt':stmt})
            elif op == "enquiry":
                acno = obj.acno
                enq = Account.objects.get(acno = acno)

                # request.session['acno'] = acno
                return render(request, "enquiry.html",{'enq':enq});
            # msg ='Valid Account'
    except ObjectDoesNotExist:
        msg = 'Invalid Account'
    return render(request, "login.html", {'msg':msg})

def depositamt(request):
    amt = int(request.POST['amt'])
    obj = Account.objects.get(acno=request.session['acno'])
    balance = obj.balance
    balance = balance + amt
    acno = obj.acno
    Account.objects.filter(pk = acno).update(balance=balance)
    opdate = datetime.datetime.today()
    operation = "Deposit"
    stmt = Statement(fromaccount = acno, toaccount=acno , operation=operation, amount=amt, opdate=opdate)
    stmt.save()
    request.session['acno'] = None
    return redirect('index')

def widthdrawamt(request):
    amt = int(request.POST['amt'])
    obj = Account.objects.get(acno = request.session['acno'])
    balance = obj.balance
    if amt > balance:
        return render(request, "index.html", {'msg':'Insufficient balance'})
    balance = balance-amt
    acno = obj.acno
    Account.objects.filter(pk = acno).update(balance=balance)
    opdate = datetime.datetime.today()
    operation = "Withdraw"
    stmt = Statement(fromaccount = acno, toaccount=acno, operation=operation, amount=amt , opdate=opdate)
    stmt.save()
    request.session['acno'] = None
    return redirect('index')

def transferamt(request):
    toaccount = request.POST['toaccount']
    amt = int(request.POST['amt'])
    msg = ''
    try:
        obj2 = Account.objects.get(acno = toaccount)
        if obj2 is not None:
            obj1 = Account.objects.get(acno = request.session['acno'])
            balance1 = obj1.balance
            if amt >balance1:
                return render(request, "index.html", {'msg':'Insufficient balance'})
            balance1 = balance1-amt
            balance2 = obj2.balance
            balance2 = balance2+amt
            acno = obj1.acno
            Account.objects.filter(pk = acno).update(balance= balance1)
            Account.objects.filter(pk = obj2.acno).update(balance= balance2)
            opdate = datetime.datetime.today()
            operation = "Transfer"
            stmt1 = Statement(fromaccount= acno, toaccount= obj2.acno, operation=operation, amount=amt, opdate=opdate)
            stmt2 = Statement(fromaccount=obj2.acno, toaccount= obj1.acno, operation=operation, amount=amt, opdate=opdate)
            stmt1.save()
            stmt2.save()
            request.session['acno'] =None
            return redirect('index')
    except ObjectDoesNotExist:
        request.session['acno'] = None
        return render(request, "index.html", {'msg':'Invalid Account No'})

def back(request):
    request.session['acno'] = None
    return redirect('index')

def adminlogin(request):
    return render(request, "adminlogin.html")

def adminlogcode(request):
     adminid = request.POST['adminid']
     password = request.POST['password']
     msg = ''
     try:
         obj = AdminLogin.objects.get(userid = adminid, password = password)
         if obj is not None:
             ac = Account.objects.all()
             return render(request, "viewaccounts.html", {'ac':ac})
             # msg = "Valid user"
     except ObjectDoesNotExist:
         msg = 'Invalid User'
     return render(request, "adminlogin.html", {'msg':msg})

def deleteaccount(request, acno):
    obj = Account.objects.get(acno = acno)
    obj.delete()
    ac = Account.objects.all()
    return render(request, "viewaccounts.html", {'ac':ac})
