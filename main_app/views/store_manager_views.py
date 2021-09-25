from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse,HttpResponseRedirect
from main_app.models.store_manager_models import *
from main_app.views.admin_view import *
from main_app.models.login_models import registration
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
import csv,io,json
import datetime
from datetime import date
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Sum, Avg
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
from calendar import monthrange
# ===========================================================================
from ..serializers import StoreSerializer,CustomerDataSerializer
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import random
# ===========================================================================
# Create your views here.
@login_required(login_url="/signup")
def store(request):
    try:
        if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
        entry = request.session.get('entry')
        storeid = request.session.get('storeID')
        context_1 = {}
        context_2 = {}
        context_3 = {}
        context_1['month_1'] = 0
        context_1['month_2'] = 0
        context_1['month_3'] = 0
        context_1['month_4'] = 0
        context_1['month_5'] = 0
        context_1['month_6'] = 0
        context_1['month_7'] = 0
        context_1['month_8'] = 0
        context_1['month_9'] = 0
        context_1['month_10'] = 0
        context_1['month_11'] = 0
        context_1['month_12'] = 0
        context_2['month_avg_1'] = 0
        context_2['month_avg_2'] = 0
        context_2['month_avg_3'] = 0
        context_2['month_avg_4'] = 0
        context_2['month_avg_5'] = 0
        context_2['month_avg_6'] = 0
        context_2['month_avg_7'] = 0
        context_2['month_avg_8'] = 0
        context_2['month_avg_9'] = 0
        context_2['month_avg_10'] = 0
        context_2['month_avg_11'] = 0
        context_2['month_avg_12'] = 0
        context_3['total_amount_1'] = 0
        context_3['total_amount_2'] = 0
        context_3['total_amount_3'] = 0
        context_3['total_amount_4'] = 0
        context_3['total_amount_5'] = 0
        context_3['total_amount_6'] = 0
        context_3['total_amount_7'] = 0
        context_3['total_amount_8'] = 0
        context_3['total_amount_9'] = 0
        context_3['total_amount_10'] = 0
        context_3['total_amount_11'] = 0
        context_3['total_amount_12'] = 0
        context = {}
        if(entry == 'Manual'):
            context['entry'] = 'Manual'
        elif(entry == 'SheetUpload'):
            context['entry'] = 'SheetUpload'
        else:
            context['entry'] = 'Both'
        custNo = CustomerData.objects.filter(storeID=storeid).annotate(month=TruncMonth('time_stamp')).values('month').annotate(c=Count('id')).values('month', 'c')
        l1 = []
        for i in custNo:
            context_1['month_'+str(i['month'].date().month)] = i['c']
        for i in context_1.values():
            l1.append(i)
        l2 = []
        l3 = []
        monthArray = []
        # Mothly Wise Amount


        invoices = CustomerShopData.objects.filter(storeID = storeid)
        months = invoices.datetimes("time_stamp", kind="month")

        print('months >>> ',months)
        count = 1
        for month in months:
            month_invs = invoices.filter(time_stamp__month=month.month)
            month_total = month_invs.aggregate(total=Sum("amount")).get("total")
            print(f"Month: {month}, Total: {month_total}")
            context_3['total_amount_'+str(month.month)] = int(month_total)
            count = count + 1


        # exit()

        
        # cusInstance = CustomerData.objects.filter(storeID=storeid)
        # for cusData in cusInstance:
        #     shopData = list(CustomerShopData.objects.filter(storeID=storeid, customerID=cusData).values('amount').annotate(
        #         month=TruncMonth('time_stamp')).values('month').annotate(AMTSUM=Sum('amount')).values('month', 'AMTSUM'))

        #     print('================================')

        #     for j in shopData:
        #         print('monthArray >>> ',monthArray)
        #         if j['month'].date().month not in monthArray:
        #             monthArray.append(j['month'].date().month)
        #             print('j shopdata >> ',j)
        #             l2.append(j['AMTSUM'])
        #             print('list l2 >>> ',l2)

        #             # num_days = monthrange(j['month'].date().year, j['month'].date().month)[1]
        #             # print('num_days >> ',num_days,'int(sum(l2)/num_day >>>>> ',int(sum(l2)/num_days))

        #             context_3['total_amount_'+str(j['month'].date().month)] = int(sum(l2))
        #             l2 = []
        #         else:
        #             context_3['total_amount_'+str(j['month'].date().month)] = int(sum(l2))
        # #         average = sum(l2)//len(l2)
        # #         context_2['month_avg_'+str(j['month'].date().month)] = average
        # # for i in context_2.values():
        # #     l3.append(i)

        # print('l3 data >>> ',l3)
        print('context_3 data >>> ',context_3)

        request.session['admin_cust_list'] = l1
        # request.session['admin_avg_list'] = l3
        return render(request, 'store-manager/store.html', {'entry':entry,'context': context, 'context_1': context_1, 'context_2': context_2, 'context_3' : context_3})
    except:
        entry = request.session.get('entry')
        storeid = request.session.get('storeID')
        context_1 = {}
        context_2 = {}
        context_3 = {}
        context_1['month_1'] = 0
        context_1['month_2'] = 0
        context_1['month_3'] = 0
        context_1['month_4'] = 0
        context_1['month_5'] = 0
        context_1['month_6'] = 0
        context_1['month_7'] = 0
        context_1['month_8'] = 0
        context_1['month_9'] = 0
        context_1['month_10'] = 0
        context_1['month_11'] = 0
        context_1['month_12'] = 0
        context_2['month_avg_1'] = 0
        context_2['month_avg_2'] = 0
        context_2['month_avg_3'] = 0
        context_2['month_avg_4'] = 0
        context_2['month_avg_5'] = 0
        context_2['month_avg_6'] = 0
        context_2['month_avg_7'] = 0
        context_2['month_avg_8'] = 0
        context_2['month_avg_9'] = 0
        context_2['month_avg_10'] = 0
        context_2['month_avg_11'] = 0
        context_2['month_avg_12'] = 0
        context_3['total_amount_1'] = 0
        context_3['total_amount_2'] = 0
        context_3['total_amount_3'] = 0
        context_3['total_amount_4'] = 0
        context_3['total_amount_5'] = 0
        context_3['total_amount_6'] = 0
        context_3['total_amount_7'] = 0
        context_3['total_amount_8'] = 0
        context_3['total_amount_9'] = 0
        context_3['total_amount_10'] = 0
        context_3['total_amount_11'] = 0
        context_3['total_amount_12'] = 0
        return render(request, 'store-manager/store.html', {'context': context, 'context_1': context_1, 'context_2': context_2, 'context_3' : context_3})
# =============================================================================================================================
#                                                 SHEET ENTRY VIEW
# =============================================================================================================================
@login_required(login_url="/signup")
def sheet(request):
    if request.user:
        if request.user.is_superuser:
            return HttpResponseRedirect('ab_admin')
        if request.method == 'GET':
            entry = request.session.get('entry')
            return render(request,'store-manager/entry-via-sheet.html',{'entry':entry})
# =============================================================================================================================
#                                                MANUAL SEARCH and ENTRY VIEW
# =============================================================================================================================
@login_required(login_url="/signup")
def manualFormSheet(request):
    if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
            
    return render(request, 'store-manager/manual-entry.html')

@login_required(login_url="/signup")
def manualEntryData(request):
    if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
    if request.method == 'POST':
        mannual_contact = request.POST['contact']
        mannual_invoice = request.POST['invoice']
        customerName = request.POST['name']
        CustomerGender = request.POST.get('gender')
        customerDOB = request.POST['DOB']
        customerDOM = request.POST['DOM']
        customerEmail = request.POST['email']
        mannual_amount = request.POST['amount']
        mannual_contact =  mannual_contact.strip()
        mannual_invoice = mannual_invoice.strip()
        customerName =  customerName.strip()
        CustomerGender =  CustomerGender
        customerDOB =  customerDOB.strip()
        customerDOM =  customerDOM.strip()
        customerEmail =  customerEmail.strip()
        mannual_amount =  mannual_amount.strip()
        storeid = request.session.get('storeID')
        checkData = CustomerData.objects.filter(storeID=storeid,contact=mannual_contact)
        if CustomerGender == None:
            CustomerGender = "NA"
        if len(checkData) == 1:
            for i in checkData:
                i.name=customerName
                i.contact=mannual_contact
                i.email=customerEmail
                i.DOB=customerDOB
                i.DOM=customerDOM
                i.gender=CustomerGender
                i.save()                
                shopData = CustomerShopData(storeID=storeid, customerID=i, invoice=mannual_invoice, amount=mannual_amount).save()
        else:
            custData = CustomerData(storeID=storeid, name=customerName, contact=mannual_contact,
                                    email=customerEmail, DOB=customerDOB,DOM=customerDOM,gender=CustomerGender, entry_type='Manual')
            custData.save()
            shopData = CustomerShopData(storeID=storeid, customerID=custData, invoice=mannual_invoice, amount=mannual_amount).save()
        # =======================================   SENDING SMS ON EVERY PURCHASE   ====================================================
        storeid = request.session.get('storeID')
        store_instance = store_detail.objects.get(storeID=storeid)
        store_name = store_instance.store_name
        store_manager_Instance = store_manager.objects.get(store=store_instance)
        managerContact = store_manager_Instance.manager_contact
        managerName = store_manager_Instance.manager_name 

        if(len(customerName.strip()) == 0):
            customerName = 'Sir/Mam'
            
        var1 = customerName+'|'+managerContact+'|'+store_name
        receiver = mannual_contact
        url = "https://www.fast2sms.com/dev/bulkV2"
        querystring = {"authorization":"LrR4KgsUmTWEZM50jlhPBofD2pewQvJHtaYuCx6kV3dNiqOyIFXvk5WJ4snwa7d6G9OhEtQloFIC3bPf","sender_id":"PTMKLB","message":"124397","variables_values":var1,"route":"dlt","numbers":receiver}
        headers = {'cache-control': "no-cache"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        try:
            if len(customerEmail) != 0:
                to_mail = [customerEmail]
                here = 'https://www.platinumklub.com/aboutUs'
                storeid = request.session.get('storeID')
                store_instance = store_detail.objects.get(storeID=storeid)
                store_name = store_instance.store_name
                if len(customerName) != 0:
                    print('customer name : ',customerName)
                    print('customer Email : ',customerEmail)

                    # message = f"\nHello {customerName},\nGreeting of the Day!\n\nWelcome to PLATINUM KLUB, Thank you for shopping from our {store_instance.store_name} store. Please visit Again!\nWe do have other services also to serve you.Visit our website to explore more : www.platinumklub.com/aboutUs\n\n\nHave a Great Day!\n\n\nRegards,\nCustomer Support\nPLATINUM KLUB\nEmail:{'contact@platinumklub.com'}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                    # mail = EmailMessage(f"PLATINUMKLUB",message, settings.DEFAULT_FROM_EMAIL,to_mail)
                    # mail.send()
                    # print('email send successfully 01 !')
                else:
                    customerName = 'Sir/Mam'
                # ===== send html emails =========
                today = date.today()
                html_content = render_to_string('store-manager/sendEmailToCustomer.html',{'customer_name':customerName,'store_name':store_name,'date':today})
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(f"PLATINUM KLUB",text_content,settings.DEFAULT_FROM_EMAIL,to_mail)
                email.attach_alternative(html_content,'text/html')
                email.send()
                print('email sent...')
        except:
            return HttpResponse('data saved!')
        # ==============================================================================================================================
        # =======================================   SENDING SMS ON EVERY PURCHASE   ====================================================
        # url = "https://www.fast2sms.com/dev/bulk"

        # completeSms = f"dear,{customerName} thank to shop in our store! We will happy to see you again."
        
        # payload = "sender_id=FSTSMS&message=" + completeSms +"&language=english&route=p&numbers=" + mannual_contact
        # headers = {
        # 'authorization': "LrR4KgsUmTWEZM50jlhPBofD2pewQvJHtaYuCx6kV3dNiqOyIFXvk5WJ4snwa7d6G9OhEtQloFIC3bPf",
        # 'Content-Type': "application/x-www-form-urlencoded",
        # 'Cache-Control': "no-cache",
        # }
        # response = requests.request("POST", url, data=payload, headers=headers)
        # ==============================================================================================================================
        return HttpResponse('data saved!')
    else:
        entry = request.session.get('entry')
        context = {}
        if(entry == 'Manual'):
            context['entry'] = 'Manual'
        elif(entry == 'SheetUpload'):
            context['entry'] = 'SheetUpload'
        else:
            context['entry'] = 'Both'
        return render(request, 'store-manager/manual-entry.html', context)
# ---------------------------------------------SEARCHING FOR EXISTING CSV_RECORD-----------------------------------------------
def myconverter(o):
    date = str(o.strftime("%m/%d/%Y"))
    return date

@login_required(login_url="/signup")
def checkExistCustomer(request):
    if request.method == 'POST':
        ContactNumber = request.POST['ContactNumber']
        ContactNumber = ContactNumber.strip()        
        storeid = request.session.get('storeID')
        contactData = list(CustomerData.objects.filter(
            storeID=storeid, contact=ContactNumber).values())
        return HttpResponse(json.dumps(contactData, default=myconverter), content_type="application/json")

@login_required(login_url="/signup")
def checkExistInVoiceNo(request):
    if request.method == 'POST':
        flag = "False"
        InVoiceNumber = request.POST['InVoiceNumber']
        MobileNumber = request.POST['MobileNumber']
        InVoiceNumber = InVoiceNumber.strip()
        storeid = request.session.get('storeID')
        shopData = CustomerShopData.objects.filter(invoice=InVoiceNumber, storeID=storeid)
        if len(shopData) == 1:
            flag = "True"
        else:
            flag = "False"
        return HttpResponse(flag)

@login_required(login_url="/signup")
def NewInVoiceNogenrate(request):
    if request.method == 'GET':
        storeid = request.session.get('storeID')
        latestInvoice = CustomerShopData.objects.filter(
            storeID=storeid).values('invoice').latest('id')
        return HttpResponse(json.dumps(latestInvoice), content_type="application/json")
# =============================================================================================================================
#                                         STORE MANAGER PROFILE VIEW
# =============================================================================================================================
@login_required(login_url="/signup")
def edit_store_profile(request):
    try:
        if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
        if request.method == 'POST':
            name = request.POST['manager_name']
            email = request.POST['manager_email']
            image = request.FILES.get('manager_image')
            user = User.objects.get(email =email.strip())
            user.first_name= name.strip()
            storeid = request.session.get('storeID')
            store_instance = store_detail.objects.get(storeID=storeid)
            manager = store_manager.objects.get(store=store_instance)
            manager.manager_name = name.strip()
            if image != None:
                manager.manager_image = image
            user.save()
            manager.save()
            return redirect('profile')
    except:
        return render(request, 'store-manager/profile.html', {'error': 'An error occured.Try again!'})

def store_profile(request):
    try:
        if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
        try:
            entry = request.session.get('entry')

            user = User.objects.get(id=request.user.id)
            storeid = request.session.get('storeID')
            store_instance = store_detail.objects.get(storeID=storeid)
            x = store_instance.store_category
            a = x.replace('[','')
            b = a.replace(']','')
            c = b.replace("'",'')
            manager = store_manager.objects.get(store=store_instance)
            return render(request, 'store-manager/profile.html', {'entry':entry,'storeid':storeid,'store_data': store_instance, 'manager': manager.manager_contact, 'image': manager.manager_image,'category' : c})
        except:
            logout(request)
            return HttpResponseRedirect('/signin')
    except:
        return render(request, 'store-manager/profile.html', {'error': 'An error occured.Try again!'})
# =============================================================================================================================
#                                           PREVIEW SHEET DATA VIEW
# =============================================================================================================================
@login_required(login_url="/signup")
def preview(request):
    if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
    return render(request, 'store-manager/preview-data.html')
# =============================================================================================================================
#                                        CHANGE STORE MANAGER PASSWORD VIEW
# =============================================================================================================================
@login_required(login_url="/signup")
def change_pwd(request):
    if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
    context = {}
    if request.method == 'POST':
        current = request.POST['current_pwd']
        new_pass = request.POST['confirm_pwd']
        user = User.objects.get(id=request.user.id)
        register = registration.objects.get(user = user)
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pass)
            user.save()
            register.password_saved = new_pass
            register.save()
            logout(request)
            return HttpResponseRedirect('/signup',{'success' : 'Password changed successfully.Sign to continue.'})
        else:
            context['msz'] = 'Incorrect Current Password'
            return render(request, 'store-manager/change-password.html',context)
        return render(request, 'store-manager/change-password.html',context)
    return render(request, 'store-manager/change-password.html',context)

@login_required(login_url="/signup")
def uploadcsvData(request):
    if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
    if request.method == 'POST':
        try:
            name = request.POST['Name']
            ContactNO = request.POST['ContactNO']
            DOB = request.POST['DOB']
            MAILID = request.POST['MAILID']
            GENDER = request.POST['GENDER']
            AMT = request.POST['AMT']
            INVONO = request.POST['INVONO']
            DOM = request.POST['DOM']
            ListContactNO = ContactNO.split(',')
            Listname = checkList(name.split(','),len(ListContactNO))
            ListDOB = checkList(DOB.split(','),len(ListContactNO))
            ListMAILID = checkList(MAILID.split(','),len(ListContactNO))
            ListGENDER = checkList(GENDER.split(','),len(ListContactNO))
            ListAMT = AMT.split(',') 
            ListINVONO = INVONO.split(',')
            ListDOM =  checkList(DOM.split(','),len(ListContactNO))        
            storeid = request.session.get('storeID')
            for i in range(len(ListContactNO)):
                checkData = CustomerData.objects.filter(storeID=storeid,contact=ListContactNO[i].strip())
                if len(checkData) == 1:
                    Duplicateinvoice = CustomerShopData.objects.filter(storeID=storeid,invoice=ListINVONO[i].strip())
                    if not Duplicateinvoice:
                        dataInstance = CustomerData.objects.get(storeID=storeid,contact=ListContactNO[i].strip())
                        shopData = CustomerShopData(storeID=storeid,customerID=dataInstance,invoice=ListINVONO[i].strip(),amount=ListAMT[i].strip()).save()
                else:
                    custData = CustomerData(storeID=storeid,name=Listname[i].strip(),contact=ListContactNO[i].strip(),email=ListMAILID[i].strip(),DOB=ListDOB[i].strip(),DOM=ListDOM[i].strip(),gender=ListGENDER[i].strip(),entry_type='CSV')
                    custData.save()
                    shopData = CustomerShopData(storeID=storeid,customerID=custData,invoice=ListINVONO[i].strip() ,amount=ListAMT[i].strip()).save()
            return JsonResponse({'msg': 'Success'})
        except:
            return JsonResponse({'msg': 'Fail'})
    if request.method == 'GET':
        entry = request.session.get('entry')
        # context = {}
        # if(entry == 'Manual'):
        #     context['entry'] = 'Manual'
        # elif(entry == 'SheetUpload'):
        #     context['entry'] = 'SheetUpload'
        # else:
        #     context['entry'] = 'Both'
        print(entry)
        return render(request, 'store-manager/entry-via-sheet.html',{'entry':entry})

# utility function : check blank list
def checkList(listData,lenList):
    empList = []
    if len(listData) == 1:
        for i in range(lenList):
            empList.append('')
        return empList
    else:
        return listData

def validate_emailID(request):
    try:
        email = request.GET['email']
        if(request.user.username == email):
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    except:
        return render(request, 'store-manager/manual-entry.html')

def StoreCustomerGraph1(request):
    if request.method == 'GET':
        chart1_data = request.session.get('admin_cust_list')
        return HttpResponse(json.dumps(chart1_data), content_type="application/json")

def StoreCustomerGraph2(request):
    if request.method == 'GET':
        chart2_data = request.session.get('admin_avg_list')
        return HttpResponse(json.dumps(chart2_data), content_type="application/json")

def onboardentry(request):
    entry = request.session.get('entry')
    return render(request,'store-manager/onboardentry.html',{'entry':entry})
# =================================================================================================================================
@login_required(login_url="/signup")
def uploadOnboarCsvData(request):
    print('<<<---onboard called--->>>')
    if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                return HttpResponseRedirect('/dashboard')
    if request.method == 'POST':
        try:
            name = request.POST['Name']
            ContactNO = request.POST['ContactNO']
            DOB = request.POST['DOB']
            MAILID = request.POST['MAILID']
            GENDER = request.POST['GENDER']
            AMT = request.POST['AMT']
            INVONO = request.POST['INVONO']
            DOM = request.POST['DOM']
            TIER = request.POST['TIER']
            ListContactNO = ContactNO.split(',')
            Listname = checkList(name.split(','),len(ListContactNO))
            ListDOB =checkList( DOB.split(','),len(ListContactNO))
            ListMAILID =checkList( MAILID.split(','),len(ListContactNO))
            ListGENDER =checkList( GENDER.split(','),len(ListContactNO))
            ListAMT = AMT.split(',')
            ListINVONO = checkList(INVONO.split(','),len(ListContactNO))
            ListDOM = checkList(DOM.split(','),len(ListContactNO))
            ListTIER = TIER.split(',')
            storeid = request.session.get('storeID')
            for i in range(len(ListContactNO)):
                checkCustomerData = CustomerData.objects.filter(storeID=storeid,contact=ListContactNO[i])
                if len(checkCustomerData) == 1:
                    for j in range(len(checkCustomerData)):
                        checkOnboardData  = CustomerOnboardData.objects.filter(storeID=storeid,customerID=checkCustomerData[j])
                        if len(checkOnboardData) == 0:
                            print('xxx')
                            dataInstance = CustomerData.objects.get(storeID=storeid,contact=int(ListContactNO[i])) 
                            onboardData = CustomerOnboardData(storeID=storeid,customerID=dataInstance,tierRuleNo=int(ListTIER[i]),total_amount=float(ListAMT[i])).save()
                        else:
                            print('yyy')
                            x = checkCustomerData[j]
                            x.name=Listname[i]
                            x.email=ListMAILID[i]
                            x.gender=ListGENDER[i]
                            x.DOM=ListDOM[i]
                            x.DOB=ListDOB[i]
                            x.save()
                else:
                    custData = CustomerData(storeID=storeid, name=Listname[i], contact=int(ListContactNO[i]), email=ListMAILID[i], DOB=ListDOB[i], DOM=ListDOM[i], gender=ListGENDER[i],entry_type='CSV-Onboard')
                    custData.save()
                    onboardData = CustomerOnboardData(storeID=storeid,customerID=custData,tierRuleNo=int(ListTIER[i]) ,total_amount=float(ListAMT[i]))
                    onboardData.save()
            return JsonResponse({'msg': 'Success'})
        except:
            return JsonResponse({'msg': 'Fail'})
    else:
        entry = request.session.get('entry')
        context = {}
        if(entry == 'Manual'):
            context['entry'] = 'Manual'
        elif(entry == 'SheetUpload'):
            context['entry'] = 'SheetUpload'
        else:
            context['entry'] = 'Both'
        return render(request, 'store-manager/entry-via-sheet.html',context)




def onboardDataAjax(request):
    if request.method == 'POST':
        content = request.POST['contents']
        data = json.loads(content)
        print(data)
        # exit()
        a = data['Sheet1']
        blankList = []
        headerDict = {}
        for j in range(len(a[0])):
            headerList = [i[j] for i in a]
            headerDict[headerList[0]] =  headerList[1:]
            blankList.append(headerDict)
            headerDict = {}
        print('====================================================')
        print(blankList)
           
        # exit()
        return JsonResponse({'blankList' : blankList})



# =======================================================================================================================================
# =======================================================================================================================================
def customer_history_info(request):
    if request.method == 'GET':
        cust_id = request.GET['search_contact']
        print(cust_id)
        allContactExistCustomers = CustomerData.objects.filter(contact = cust_id)
        print(allContactExistCustomers)
        
        customerShopDataList = []
        customerOnboardDataList = []
        for customer in allContactExistCustomers:
            shopData = CustomerShopData.objects.filter(customerID=customer)
            onboardData = CustomerOnboardData.objects.filter(customerID=customer)
            customerShopDataList.append(shopData)
            if(len(onboardData) != 0):
                customerOnboardDataList.append(onboardData)
        storeNameList = []
        amtSum = []
        tierNo = []

        for i in customerShopDataList:
            if(len(i) != 0):
                store = store_detail.objects.filter(storeID=i[0].storeID).values('store_name')
                storeNameList.append(store[0]['store_name'])
                customerShopData = CustomerShopData.objects.filter(customerID=i[0].customerID).values('storeID').annotate(amount=Sum('amount'))
                amtSum.append(customerShopData[0])
                tierRule = tier_individual.objects.filter(store_ID=i[0].storeID,shop_start_amt__lte=int(i[0].amount),shop_end_amt__gte=int(i[0].amount)).values('tierRuleNo')
                if(len(tierRule) > 0):
                    tierNo.append(tierRule[0]['tierRuleNo'])
                else:
                    tierNo.append('NA')

        OnboardstoreNameList = []
        totalAmt = []
        onboardTierNo = []

        for i in customerOnboardDataList:
            if(len(i) != 0):
                store = store_detail.objects.filter(storeID=i[0].storeID).values('store_name')
                OnboardstoreNameList.append(store[0]['store_name'])
                CustomerOnbData = CustomerOnboardData.objects.filter(customerID=i[0].customerID).values('storeID').annotate(amount=Sum('total_amount'))
                totalAmt.append(CustomerOnbData[0])
                tierRule = CustomerOnboardData.objects.filter(storeID=i[0].storeID,tierRuleNo=i[0].tierRuleNo).values('tierRuleNo')
                if(len(tierRule) > 0):
                    onboardTierNo.append(tierRule[0]['tierRuleNo'])
                else:
                    onboardTierNo.append('NA')
        
        cust_shop_info_list=[]
        cust_shop_info_dict = {}
        cust_onboard_info_dict = {}
        customer_detailed_data = CustomerData.objects.filter(contact=cust_id).values('storeID','name','contact','email','DOB','DOM','gender')

        for i in customer_detailed_data:
            cust_shop_info_dict['name'] = i['name']
            cust_shop_info_dict['contact'] = i['contact']
            cust_shop_info_dict['email'] = i['email']
            cust_shop_info_dict['DOB'] = i['DOB']
            cust_shop_info_dict['DOM'] = i['DOM']
            cust_shop_info_dict['gender'] = i['gender']

            cust_onboard_info_dict['name'] = i['name']
            cust_onboard_info_dict['contact'] = i['contact']
            cust_onboard_info_dict['email'] = i['email']
            cust_onboard_info_dict['DOB'] = i['DOB']
            cust_onboard_info_dict['DOM'] = i['DOM']
            cust_onboard_info_dict['gender'] = i['gender']
            break
        cust_shop_info_list.extend((cust_shop_info_dict,storeNameList,amtSum,tierNo,cust_onboard_info_dict,OnboardstoreNameList,totalAmt,onboardTierNo))
        print('this is modal data : ',cust_shop_info_list)
        # exit()
        return HttpResponse(json.dumps(cust_shop_info_list), content_type="application/json")

# ===============================================================================================================================
# ===============================================================================================================================
# ===============================================================================================================================
# =================================   API CODE  =================================================================================
# ===============================================================================================================================
# StoreSerializer
def getStoreList(request):
    if request.method == 'GET':
        jsonData = request.body
        stream = io.BytesIO(jsonData)
        try:
            pythonData = JSONParser().parse(stream)
            api_key = pythonData.get('api_key',None)

            print('api_key >> ',api_key)
            apiCheck = ApiKey.objects.filter(Key=api_key.strip())
            if(len(apiCheck) == 0):
                json_data = 'Invalid API key!'
                return HttpResponse(json_data,content_type="application/json")

        except:
            json_data = 'Invalid API key!'
            return HttpResponse(json_data,content_type="application/json")

        storeList = store_detail.objects.all()
        serializer = StoreSerializer(storeList,many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type="application/json")

def store_details(request):
    if request.method == 'GET':
        jsonData = request.body
        stream = io.BytesIO(jsonData)
        # exit()
        try:
            pythonData = JSONParser().parse(stream)
            storeId = pythonData.get('store_id',None)
            api_key = pythonData.get('api_key',None)

            print('store id >> ',storeId)
            print('api_key >> ',api_key)
            apiCheck = ApiKey.objects.filter(Key=api_key.strip())
            if(len(apiCheck) == 0):
                json_data = 'Invalid API key!'
                return HttpResponse(json_data,content_type="application/json")

        except:
            json_data = 'Store ID can not be blank!'
            return HttpResponse(json_data,content_type="application/json")

        if storeId is not None:
            try:
                storeList = store_detail.objects.get(storeID=storeId)
                serializer = StoreSerializer(storeList)
                json_data = JSONRenderer().render(serializer.data)
            except:
                json_data = 'Store does not exist!'
            return HttpResponse(json_data,content_type="application/json")
        else:
            json_data = 'Store ID can not be blank!'
            return HttpResponse(json_data,content_type="application/json")


def customer_details(request):
    if request.method == 'GET':
        jsonData = request.body
        stream = io.BytesIO(jsonData)
        try:
            pythonData = JSONParser().parse(stream)
            customer_contact = pythonData.get('customer_contact',None)
            api_key = pythonData.get('api_key',None)

            apiCheck = ApiKey.objects.filter(Key=api_key.strip())
            if(len(apiCheck) == 0):
                json_data = 'Invalid API key!'
                return HttpResponse(json_data,content_type="application/json")
        except:
            json_data = 'customer_contact can not be blank!'
            return HttpResponse(json_data,content_type="application/json")
            
        if customer_contact is not None:
            try:
                customer_data = CustomerData.objects.filter(contact=customer_contact.strip())
                serializer = CustomerDataSerializer(customer_data,many=True)
                json_data = JSONRenderer().render(serializer.data)
            except:
                json_data = 'Customer does not exist!'
            return HttpResponse(json_data,content_type="application/json")
        else:
            json_data = 'customer contact can not be blank!'
            return HttpResponse(json_data,content_type="application/json")



def send_OTP(request):
    if request.method == 'GET':
        jsonData = request.body
        stream = io.BytesIO(jsonData)
        # try:
        pythonData = JSONParser().parse(stream)
        contact = pythonData.get('contact',None)
        print('customer_contact >>> ',contact)

        api_key = pythonData.get('api_key',None)

        apiCheck = ApiKey.objects.filter(Key=api_key.strip())
        if(len(apiCheck) == 0):
            json_data = 'Invalid API key!'
            return HttpResponse(json_data,content_type="application/json")
        # except:
        # json_data = 'contact can not be blank!'
            # return HttpResponse(json_data,content_type="application/json")
            
        if contact is not None:
            try:
                otp = random.randint(1111, 9999)
                print('=>>>>>>>>',contact, otp)
                request.session['otp'] = otp
                print("ON GOING OTP")
                url = "https://www.fast2sms.com/dev/bulkV2"
                querystring = {"authorization":"LrR4KgsUmTWEZM50jlhPBofD2pewQvJHtaYuCx6kV3dNiqOyIFXvk5WJ4snwa7d6G9OhEtQloFIC3bPf","sender_id":"PTMKLB","message":"124396","variables_values":otp,"route":"dlt","numbers":contact}
                headers = {'Cache-Control': "no-cache"}
                json_data = requests.request("GET", url, headers=headers, params=querystring)
            except:
                json_data = 'Customer does not existCannot send OTP!'
            return HttpResponse(json_data,content_type="application/json")
        else:
            json_data = 'contact can not be blank!'
            return HttpResponse(json_data,content_type="application/json")
