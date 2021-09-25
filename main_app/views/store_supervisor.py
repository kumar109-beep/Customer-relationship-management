from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from main_app.models.login_models import registration,customerQueries
from main_app.models.store_manager_models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.core.mail import message, send_mail
from django.conf import settings
import random,requests,re,csv
import string
import twilio
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import xlwt
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@login_required(login_url="/signup")
def change_supervisor_pwd(request):
    if request.user:
        if request.user.is_superuser:
            return HttpResponseRedirect('ab_admin')
        if request.user.is_staff:
            # return render(request, 'supervisor_template/change-pwd.html')
            context = {}
            if request.method == 'POST':
                # exit()
                current = request.POST['current_pwd']
                new_pass = request.POST['confirm_pwd']
                user = User.objects.get(id=request.user.id)
                register = registration.objects.get(user = user)
                print('==========================================')
                print('current >>> ',current)
                print('new_pass >>> ',new_pass)
                print('user >>> ',user)
                print('register >>> ',register)

                check = user.check_password(current)

                print('check >>> ',check)
                print('==========================================')
                if check == True:
                    user.set_password(new_pass)
                    user.save()
                    register.password_saved = new_pass
                    register.save()
                    logout(request)
                    return HttpResponseRedirect('/signup',{'success' : 'Password changed successfully.Sign to continue.'})
                else:
                    context['msz'] = 'Incorrect Current Password'
                    return render(request, 'supervisor_template/change-pwd.html',context)
                return render(request, 'supervisor_template/change-pwd.html',context)
            return render(request, 'supervisor_template/change-pwd.html',context)


def store_supervisor_profile(request):
    try:
        if request.user:
            if request.user.is_superuser:
                return HttpResponseRedirect('ab_admin')
            if request.user.is_staff:
                try:
                    array = eval(request.session['storeArray'])
                    storeArray = []
                    storenameArray = ''
                    for i in array:
                        data = store_detail.objects.get(id = int(i))
                        dataDict = {}
                        dataDict['id'] = int(i)
                        dataDict['storeName'] = data.store_name
                        storeArray.append(dataDict)
                        storenameArray = storenameArray + data.store_name+','

                    print('storeArray  >>> ',storeArray)
                    # ------------------------------------------------------------
                    store_supervisor = supervisorDetails.objects.get(supervisor_email = request.user)
                    # ------------------------------------------------------------
                    return render(request, 'supervisor_template/profile.html',{'storenameArray':storenameArray,'storeArray':storeArray,'storelength':len(storeArray),'store_supervisor':store_supervisor})
                except:
                    logout(request)
                    return HttpResponseRedirect('/signin')
    except:
        return render(request, 'supervisor_template/profile.html', {'error': 'An error occured.Try again!'})

def getStores(request):
    array = eval(request.session['storeArray'])
    storeArray = []
    for i in array:
        data = store_detail.objects.get(id = int(i))
        dataDict = {}
        dataDict['id'] = int(i)
        dataDict['storeName'] = data.store_name
        dataDict['storeID'] = data.storeID
        # -------------------------------Today sales data-----------------------------------------------
        # ----------------------------------------------------------------------------------------------
        today = datetime.date.today()
        print('today >>> ',today)
        custData = CustomerShopData.objects.filter(time_stamp__gte=today,storeID=data.storeID)
        todaySales = 0
        for i in custData:
            todaySales = todaySales + i.amount
        dataDict['todaySales'] = float(todaySales)
        # ----------------------------------------------------------------------------------------------
        # -------------------------------Yesterday sales data-------------------------------------------
        # ----------------------------------------------------------------------------------------------
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_data = CustomerShopData.objects.filter(time_stamp__date=yesterday,storeID=data.storeID)
        yesterdaySales = 0
        for i in yesterday_data:
            yesterdaySales = yesterdaySales + i.amount
        dataDict['yesterdaySales'] = float(yesterdaySales)
        # ----------------------------------------------------------------------------------------------
        # -------------------------------Last week sales data-------------------------------------------
        # ----------------------------------------------------------------------------------------------
        one_week_ago = datetime.date.today() - datetime.timedelta(days=7)
        week_data = CustomerShopData.objects.filter(time_stamp__gt=one_week_ago,storeID=data.storeID)
        weekSales = 0
        for i in week_data:
            weekSales = weekSales + i.amount
        dataDict['weekSales'] = float(weekSales)

        # ----------------------------------------------------------------------------------------------
        # -------------------------------current month sales data---------------------------------------
        # ----------------------------------------------------------------------------------------------
        todays_date = date.today()
        currentMonthdata = CustomerShopData.objects.filter(time_stamp__year__gte=todays_date.year,time_stamp__month__gte=todays_date.month,time_stamp__year__lte=todays_date.year,time_stamp__month__lte=todays_date.month,storeID=data.storeID)            
        currentMonthSales = 0
        for i in currentMonthdata:
            currentMonthSales = currentMonthSales + i.amount
        dataDict['currentMonthSales'] = float(currentMonthSales)

        # ----------------------------------------------------------------------------------------------
        # -------------------------------last month sales data------------------------------------------
        # ----------------------------------------------------------------------------------------------
        todays_date = date.today()
        lastMonthdata = CustomerShopData.objects.filter(time_stamp__year__gte=todays_date.year,time_stamp__month__gte=todays_date.month-1,time_stamp__year__lte=todays_date.year,time_stamp__month__lte=todays_date.month-1,storeID=data.storeID)            
        lastMonthSales = 0
        for i in lastMonthdata:
            lastMonthSales = lastMonthSales + i.amount
        dataDict['lastMonthSales'] = float(lastMonthSales)

        # ----------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------
        storeArray.append(dataDict)

    print('storeArray  >>> ',storeArray)
    return JsonResponse({'storeArray':storeArray})
    
@login_required(login_url="/signup")
def dashboard(request):
    if request.user:
        print('user >>> ',request.user)
        if request.user.is_superuser:
            return HttpResponseRedirect('ab_admin')
        if request.user.is_staff:
            array = eval(request.session['storeArray'])
            storeArray = []
            storenameArray = ''
            for i in array:
                data = store_detail.objects.get(id = int(i))
                dataDict = {}
                dataDict['id'] = int(i)
                dataDict['storeName'] = data.store_name
                storeArray.append(dataDict)
                storenameArray = storenameArray + data.store_name+','

            print('storeArray  >>> ',storeArray)
            # ------------------------------------------------------------
            store_supervisor = supervisorDetails.objects.get(supervisor_email = request.user)

            # ------------------------------------------------------------
            return render(request,'supervisor_template/supervisor_dash.html',{'storenameArray':storenameArray,'storeArray':storeArray,'storelength':len(storeArray),'store_supervisor':store_supervisor})
        if request.user.is_active:
            return HttpResponseRedirect('store')


@login_required(login_url="/signup")
def storeDetailPage(request,id):
    if request.user:
        print('user >>> ',request.user)
        if request.user.is_superuser:
            return HttpResponseRedirect('ab_admin')
        if request.user.is_staff:
            print('id >> ',id)
            try:
                Storedata = store_detail.objects.get(id = id)
                managerData = store_manager.objects.get(store = Storedata)
            except:
                # Storedata = store_detail.objects.get(id = array[0])
                # managerData = store_manager.objects.get(store = Storedata)
                return HttpResponseRedirect('/dashboard')
                # return render(request,'supervisor_template/storeDetail.html',{'Storedata':Storedata,'storeArray':storeArray,'managerData':managerData,'errorMsg':'You Only Have Access For Assigned Stores!'})

            array = eval(request.session['storeArray'])
            storeArray = []
            print('id value >>> ',id)
            print('array value >>> ',array)
            for i in array:
                data = store_detail.objects.get(id = int(i))
                dataDict = {}
                dataDict['id'] = int(i)
                dataDict['storeName'] = data.store_name
                storeArray.append(dataDict)

            if str(id) not in array:
                print('this is an invalid id !')
                # return HttpResponseRedirect('/dashboard')
                Storedata = store_detail.objects.get(id = array[0])
                managerData = store_manager.objects.get(store = Storedata)
                return render(request,'supervisor_template/storeDetail.html',{'Storedata':Storedata,'storeArray':storeArray,'managerData':managerData,'errorMsg':'You Only Have Access For Assigned Stores!'})

            return render(request,'supervisor_template/storeDetail.html',{'Storedata':Storedata,'storeArray':storeArray,'managerData':managerData})
        if request.user.is_active:
            return HttpResponseRedirect('store')



@login_required(login_url="/signup")
def customer_info(request):
    if request.user:
        print('user >>> ',request.user)
        if request.user.is_superuser:
            return HttpResponseRedirect('ab_admin')
        if request.user.is_staff:
            array = eval(request.session['storeArray'])
            storeArray = []
            customerList = []
            for i in array:
                data = store_detail.objects.get(id = int(i))
                dataDict = {}
                dataDict['id'] = int(i)
                dataDict['storeName'] = data.store_name
                storeArray.append(dataDict)
                # =====================================================
                customerData = CustomerData.objects.filter(storeID = data.storeID)
                for j in customerData:
                    print('customerData >>>> ',j.name)
                    customerList.append(j)
                # =====================================================
            Customer_data_count = len(customerList)
            return render(request,'supervisor_template/customerInfo.html',{'storeArray':storeArray,'customerList':customerList[:50],'Customer_data_count':Customer_data_count})
        if request.user.is_active:
            return HttpResponseRedirect('store')



import datetime,json

def filterSpecificStoreData(request):
    if request.method == 'GET':
        filtertag = request.GET['filterTag']
        storeID = request.GET['storeId']

        print('filtertag >> ',filtertag)
        print('storeID >> ',storeID)
        # data lists
        storeID_list = []
        storeName_list = []
        managerName_list = []
        managerContact_list = []
        totalEntries = []
        newEntries = []
        oldEntries = []
        nullEntries = []
        efficiency = []

        countNew = 0
        countOld = 0
        count = 0
        countNull = 0
        # =====================================================
        if(filtertag == 'Today'):
            today = datetime.date.today()
            totalEntries.append(len(CustomerShopData.objects.filter(time_stamp__gt=today,storeID=storeID)))
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            data = CustomerShopData.objects.filter(time_stamp__gte=today,storeID=storeID)
            print('data >>>> ',data)
            if(len(data)>0):
                for j in data:
                    print(j.customerID.time_stamp.date(),'<<<------>>>',today)
                    if(j.customerID.time_stamp.date() == today):
                        # new customer count
                        countNew += 1
                    else:
                        # old customer count
                        countOld += 1
                    
                    if(j.customerID.contact == '1000000000'):
                        # new customer count
                        countNull += 1
                        
                newEntries.append(countNew)
                oldEntries.append(countOld)
                nullEntries.append(countNull)
                countNew = 0
                countOld = 0
                countNull = 0
            else:
                # no of entries == 0
                count = 0
                newEntries.append(count)
                oldEntries.append(count)
                nullEntries.append(count)
        
            for i in range(len(totalEntries)):
                if totalEntries[i] != 0:
                    res = (1-(nullEntries[i]/totalEntries[i]))*100
                    efficiency.append(round(res, 2))
                else:
                    efficiency.append('-')



            print(totalEntries,newEntries,oldEntries,nullEntries,efficiency)
            print('totalEntries >>> ',totalEntries)
            print('newEntries >>> ',newEntries)
            print('oldEntries >>> ',oldEntries)
            infoList = []
            infoDict = {}
            infoDict['totalEntries'] = totalEntries[0]
            infoDict['newEntries'] = newEntries[0]
            infoDict['oldEntries'] = oldEntries[0]
            infoList.append(infoDict)

            dataList = []
            for i in data:
                datadict = {}
                datadict['customerName'] = i.customerID.name
                datadict['customerContact'] = i.customerID.contact
                datadict['customerEmail'] = i.customerID.email
                dataList.append(datadict)
        elif(filtertag == 'Yesterday'):
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            totalEntries.append(len(CustomerShopData.objects.filter(time_stamp__gt=yesterday,storeID=storeID)))
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            data = CustomerShopData.objects.filter(time_stamp__date=yesterday,storeID=storeID)
            print('data >>>> ',data)
            if(len(data)>0):
                for j in data:
                    print(j.customerID.time_stamp.date(),'<<<------>>>',yesterday)
                    if(j.customerID.time_stamp.date() == yesterday):
                        # new customer count
                        countNew += 1
                    else:
                        # old customer count
                        countOld += 1
                    
                    if(j.customerID.contact == '1000000000'):
                        # new customer count
                        countNull += 1
                        
                newEntries.append(countNew)
                oldEntries.append(countOld)
                nullEntries.append(countNull)
                countNew = 0
                countOld = 0
                countNull = 0
            else:
                # no of entries == 0
                count = 0
                newEntries.append(count)
                oldEntries.append(count)
                nullEntries.append(count)
        
            for i in range(len(totalEntries)):
                if totalEntries[i] != 0:
                    res = (1-(nullEntries[i]/totalEntries[i]))*100
                    efficiency.append(round(res, 2))
                else:
                    efficiency.append('-')



            print(totalEntries,newEntries,oldEntries,nullEntries,efficiency)
            print('totalEntries >>> ',totalEntries)
            print('newEntries >>> ',newEntries)
            print('oldEntries >>> ',oldEntries)
            infoList = []
            infoDict = {}
            infoDict['totalEntries'] = totalEntries[0]
            infoDict['newEntries'] = newEntries[0]
            infoDict['oldEntries'] = oldEntries[0]
            infoList.append(infoDict)
            
            dataList = []
            for i in data:
                datadict = {}
                datadict['customerName'] = i.customerID.name
                datadict['customerContact'] = i.customerID.contact
                datadict['customerEmail'] = i.customerID.email
                dataList.append(datadict)

        elif(filtertag == 'This Week'):
            one_week_ago = datetime.date.today() - datetime.timedelta(days=7)
            totalEntries.append(len(CustomerShopData.objects.filter(time_stamp__gt=one_week_ago,storeID=storeID)))
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            data = CustomerShopData.objects.filter(time_stamp__gt=one_week_ago,storeID=storeID)
            print('data >>>> ',data,len(data))
            if(len(data)>0):
                for j in data:
                    print(j.customerID.time_stamp.date(),'<<<------>>>',one_week_ago)
                    if(j.customerID.time_stamp.date() == one_week_ago):
                        # new customer count
                        countNew += 1
                    else:
                        # old customer count
                        countOld += 1
                    
                    if(j.customerID.contact == '1000000000'):
                        # new customer count
                        countNull += 1
                        
                newEntries.append(countNew)
                oldEntries.append(countOld)
                nullEntries.append(countNull)
                countNew = 0
                countOld = 0
                countNull = 0
            else:
                # no of entries == 0
                count = 0
                newEntries.append(count)
                oldEntries.append(count)
                nullEntries.append(count)
        
            for i in range(len(totalEntries)):
                if totalEntries[i] != 0:
                    res = (1-(nullEntries[i]/totalEntries[i]))*100
                    efficiency.append(round(res, 2))
                else:
                    efficiency.append('-')



            print(totalEntries,newEntries,oldEntries,nullEntries,efficiency)
            print('totalEntries >>> ',totalEntries)
            print('newEntries >>> ',newEntries)
            print('oldEntries >>> ',oldEntries)
            infoList = []
            infoDict = {}
            infoDict['totalEntries'] = totalEntries[0]
            infoDict['newEntries'] = newEntries[0]
            infoDict['oldEntries'] = oldEntries[0]
            infoList.append(infoDict)
            
            dataList = []
            for i in data:
                print(i)
                datadict = {}
                datadict['customerName'] = i.customerID.name
                datadict['customerContact'] = i.customerID.contact
                datadict['customerEmail'] = i.customerID.email
                dataList.append(datadict)


        elif(filtertag == 'This Month'):
            todays_date = date.today()
  
            # printing todays date
            print("Current date: ", todays_date)
            
            # fetching the current year, month and day of today
            print("Current year:", todays_date.year)
            print("Current month:", todays_date.month)
            print("Current day:", todays_date.day)
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            totalEntries.append(len(CustomerShopData.objects.filter(time_stamp__year__gte=todays_date.year,time_stamp__month__gte=todays_date.month,time_stamp__year__lte=todays_date.year,time_stamp__month__lte=todays_date.month,storeID=storeID)))
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            data = CustomerShopData.objects.filter(time_stamp__year__gte=todays_date.year,time_stamp__month__gte=todays_date.month,time_stamp__year__lte=todays_date.year,time_stamp__month__lte=todays_date.month,storeID=storeID)            
            print('data >>>> ',data)

            if(len(data)>0):
                for j in data:
                    print(j.customerID.time_stamp.date(),'<<<------>>>',todays_date)
                    if(j.customerID.time_stamp.date() == todays_date):
                        # new customer count
                        countNew += 1
                    else:
                        # old customer count
                        countOld += 1
                    
                    if(j.customerID.contact == '1000000000'):
                        # new customer count
                        countNull += 1
                        
                newEntries.append(countNew)
                oldEntries.append(countOld)
                nullEntries.append(countNull)
                countNew = 0
                countOld = 0
                countNull = 0
            else:
                # no of entries == 0
                count = 0
                newEntries.append(count)
                oldEntries.append(count)
                nullEntries.append(count)
        
            for i in range(len(totalEntries)):
                if totalEntries[i] != 0:
                    res = (1-(nullEntries[i]/totalEntries[i]))*100
                    efficiency.append(round(res, 2))
                else:
                    efficiency.append('-')



            print(totalEntries,newEntries,oldEntries,nullEntries,efficiency)
            print('totalEntries >>> ',totalEntries)
            print('newEntries >>> ',newEntries)
            print('oldEntries >>> ',oldEntries)
            infoList = []
            infoDict = {}
            infoDict['totalEntries'] = totalEntries[0]
            infoDict['newEntries'] = newEntries[0]
            infoDict['oldEntries'] = oldEntries[0]
            infoList.append(infoDict)
            
            dataList = []
            for i in data:
                datadict = {}
                datadict['customerName'] = i.customerID.name
                datadict['customerContact'] = i.customerID.contact
                datadict['customerEmail'] = i.customerID.email
                dataList.append(datadict)
        


        # =====================================================
        return JsonResponse({'filteredData' : dataList,'infoDict':infoDict})



@login_required(login_url="/signup")
def update_supervisor(request):
    if request.method == 'POST':
        sup_name = request.POST['manager_name']
        try:
            edit_supervisor = supervisorDetails.objects.get(supervisor_email = request.user)
            print(request.user)
            print(edit_supervisor)
            usr = User.objects.get(email=request.user)
            usr.first_name = sup_name
            usr.save()

            edit_supervisor.supervisor_name = sup_name
            edit_supervisor.save()
            message = 'Supervisor Updated Successfully.'

        except:
            message = 'An error occured. Try again!'

        print('message >>>> ',message)

        return redirect('/store_supervisor_profile')


@login_required(login_url="/signup")
def ssder_supervisor(request):
    array = eval(request.session['storeArray'])
    storeArray = []
    for i in array:
        data = store_detail.objects.get(id = int(i))
        dataDict = {}
        dataDict['id'] = int(i)
        dataDict['storeName'] = data.store_name
        dataDict['storeID'] = data.storeID
        storeArray.append(dataDict)
    # ==========================================================================================================
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    ct = date.today()
    start_date = datetime.date(ct.year, ct.month, ct.day) 
    #start_date = datetime.date(2021, 3, 5) 
    font_style = xlwt.XFStyle()
    dateFrmt = start_date.strftime("%d %b %Y")
    ws.write(0, 1, 'Date : '+str(dateFrmt), font_style)
    ws.write(0, 3, 'Store Daily Data Entry Report', font_style)
    d1Sup = str(request.user)
    supObj = supervisorDetails.objects.get(supervisor_email = d1Sup)
    ws.write(2, 1, 'Supervisor Name : '+supObj.supervisor_name+'\nSupervisor Email : '+d1Sup+'\nSupervisor Contact : '+supObj.supervisor_contact, font_style)

    # Sheet header, first row
    row_num = 4

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['S.NO', 'STORE-ID', 'MANAGER NAME', 'MANAGER CONTACT', 'STORE NAME', 'TOTAL NO. OF ENTRIES','TOTAL NO. OF NEW ENTRIES','TOTAL NO. OF OLD ENTRIES','TOTAL NO. OF Null Entries','EFFICIENCY %']
    # COLUMN VOUNT = 6
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # ==========================================================================================================
    # data lists
    storeID_list = []
    storeName_list = []
    managerName_list = []
    managerContact_list = []
    totalEntries = []
    newEntries = []
    oldEntries = []
    nullEntries = []
    efficiency = []

    countNew = 0
    countOld = 0
    count = 0
    countNull = 0

    ct = date.today()
    start_date = datetime.date(ct.year, ct.month, ct.day) 

    store_manager_objects = store_manager.objects.all()
    for i in storeArray:
        print('i.storeID >>> ',i['storeID'])
        # -------------------------------------------------------------------------------------------------------------------------------------------------
        storeID_list.append(i['storeID'])
        storeName_list.append(i['storeName'])
        # ==========================================================
        storeObject = store_detail.objects.get(storeID = i['storeID'])
        managerObject = store_manager.objects.get(store = storeObject)
        print('managerObject 1 >>> ',managerObject.manager_name)
        print('managerObject 2 >>> ',managerObject.manager_contact)
        # ==========================================================
        managerName_list.append(managerObject.manager_name)
        managerContact_list.append(managerObject.manager_contact) 
        totalEntries.append(len(CustomerShopData.objects.filter(time_stamp__gt=start_date,storeID=i['storeID'])))
        # -------------------------------------------------------------------------------------------------------------------------------------------------
        data = CustomerShopData.objects.filter(time_stamp__gt=start_date,storeID=i['storeID'])
        if(len(data)>0):
            for j in data:
                print(j.customerID.time_stamp.date(),'<<<------>>>',start_date)
                if(j.customerID.time_stamp.date() == start_date):
                    # new customer count
                    countNew += 1
                else:
                    # old customer count
                    countOld += 1
                
                if(j.customerID.contact == '1000000000'):
                    # new customer count
                    countNull += 1
                    
            newEntries.append(countNew)
            oldEntries.append(countOld)
            nullEntries.append(countNull)
            countNew = 0
            countOld = 0
            countNull = 0
        else:
            # no of entries == 0
            count = 0
            newEntries.append(count)
            oldEntries.append(count)
            nullEntries.append(count)
    
    for i in range(len(totalEntries)):
        if totalEntries[i] != 0:
            res = (1-(nullEntries[i]/totalEntries[i]))*100
            efficiency.append(round(res, 2))
        else:
            efficiency.append('-')
    print(storeID_list,storeName_list,managerName_list,managerContact_list,totalEntries,newEntries,oldEntries,nullEntries,efficiency)
    print('=======================================================================')
    rows = []
    for i in range(0,len(storeID_list)):
        rows.append((i,storeID_list[i],managerName_list[i],managerContact_list[i],storeName_list[i],totalEntries[i],newEntries[i],oldEntries[i],nullEntries[i],efficiency[i]))
    print(rows)
    # -------------------------------------------------------------------------------------------------
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    today = date.today()
    d1 = today.strftime("%d/%m/%Y")

    excelFile = 'report_'+str(d1)+'.xls'
    csvfile = 'report_'+str(d1)+'.csv'

    # admin_mail = ['siddhant.ratna@yahoo.com','rk468335@gmail.com']
    email = str(request.user)
    to_mail = [email]
    #to_mail = ['manoj@theabacusindia.com','sunit@theabacusindia.com','siddhant.ratna@yahoo.com','rk468335@gmail.com']
    mail = EmailMessage(f"Store Data Daily Entry Report", f'ABACUS PLATINUM CLUB\n----------------------------------------\nDear Supervisor your report for Date : {d1} is prepared in Xls and CSV file format.', settings.DEFAULT_FROM_EMAIL,to_mail)
    mail.attach(excelFile.strip(), response.getvalue(), 'text/xls')
    mail.attach(csvfile.strip(), response.getvalue(), 'text/csv')
    mail.send()
    # ==========================================================================================================
    print('Mail sent successfully!')

    return redirect('/dashboard')





def ssder_to_all(request):
    store_supervisor_model_Data = supervisorDetails.objects.all()
    # ===============================================================================
    for n in store_supervisor_model_Data:
        print('i data >>>> ',n.store_array)

        array = eval(n.store_array)
        storeArray = []
        for i in array:
            data = store_detail.objects.get(id = int(i))
            dataDict = {}
            dataDict['id'] = int(i)
            dataDict['storeName'] = data.store_name
            dataDict['storeID'] = data.storeID
            storeArray.append(dataDict)
        # ==========================================================================================================
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        ct = date.today()
        start_date = datetime.date(ct.year, ct.month, ct.day) 
        #start_date = datetime.date(2021, 3, 5) 
        font_style = xlwt.XFStyle()
        dateFrmt = start_date.strftime("%d %b %Y")
        ws.write(0, 1, 'Date : '+str(dateFrmt), font_style)
        ws.write(0, 3, 'Store Daily Data Entry Report', font_style)
        d1Sup = str(n.supervisor_email)
        print('supervisor email >> ',d1Sup)
        supObj = supervisorDetails.objects.get(supervisor_email = d1Sup)
        ws.write(2, 1, 'Supervisor Name : '+supObj.supervisor_name+'\nSupervisor Email : '+d1Sup+'\nSupervisor Contact : '+supObj.supervisor_contact, font_style)

        # Sheet header, first row
        row_num = 4

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['S.NO', 'STORE-ID', 'MANAGER NAME', 'MANAGER CONTACT', 'STORE NAME', 'TOTAL NO. OF ENTRIES','TOTAL NO. OF NEW ENTRIES','TOTAL NO. OF OLD ENTRIES','TOTAL NO. OF Null Entries','EFFICIENCY %']
        # COLUMN VOUNT = 6
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        # ==========================================================================================================
        # data lists
        storeID_list = []
        storeName_list = []
        managerName_list = []
        managerContact_list = []
        totalEntries = []
        newEntries = []
        oldEntries = []
        nullEntries = []
        efficiency = []

        countNew = 0
        countOld = 0
        count = 0
        countNull = 0

        ct = date.today()
        start_date = datetime.date(ct.year, ct.month, ct.day) 

        store_manager_objects = store_manager.objects.all()
        for i in storeArray:
            print('i.storeID >>> ',i['storeID'])
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            storeID_list.append(i['storeID'])
            storeName_list.append(i['storeName'])
            # ==========================================================
            storeObject = store_detail.objects.get(storeID = i['storeID'])
            managerObject = store_manager.objects.get(store = storeObject)
            print('managerObject 1 >>> ',managerObject.manager_name)
            print('managerObject 2 >>> ',managerObject.manager_contact)
            # ==========================================================
            managerName_list.append(managerObject.manager_name)
            managerContact_list.append(managerObject.manager_contact) 
            totalEntries.append(len(CustomerShopData.objects.filter(time_stamp__gt=start_date,storeID=i['storeID'])))
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            data = CustomerShopData.objects.filter(time_stamp__gt=start_date,storeID=i['storeID'])
            if(len(data)>0):
                for j in data:
                    print(j.customerID.time_stamp.date(),'<<<------>>>',start_date)
                    if(j.customerID.time_stamp.date() == start_date):
                        # new customer count
                        countNew += 1
                    else:
                        # old customer count
                        countOld += 1
                    
                    if(j.customerID.contact == '1000000000'):
                        # new customer count
                        countNull += 1
                        
                newEntries.append(countNew)
                oldEntries.append(countOld)
                nullEntries.append(countNull)
                countNew = 0
                countOld = 0
                countNull = 0
            else:
                # no of entries == 0
                count = 0
                newEntries.append(count)
                oldEntries.append(count)
                nullEntries.append(count)
        
        for i in range(len(totalEntries)):
            if totalEntries[i] != 0:
                res = (1-(nullEntries[i]/totalEntries[i]))*100
                efficiency.append(round(res, 2))
            else:
                efficiency.append('-')
        print(storeID_list,storeName_list,managerName_list,managerContact_list,totalEntries,newEntries,oldEntries,nullEntries,efficiency)
        print('=======================================================================')
        rows = []
        for i in range(0,len(storeID_list)):
            rows.append((i,storeID_list[i],managerName_list[i],managerContact_list[i],storeName_list[i],totalEntries[i],newEntries[i],oldEntries[i],nullEntries[i],efficiency[i]))
        print(rows)
        # -------------------------------------------------------------------------------------------------
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        excelFile = 'report_'+str(d1)+'.xls'
        csvfile = 'report_'+str(d1)+'.csv'

        # admin_mail = ['siddhant.ratna@yahoo.com','rk468335@gmail.com']
        email = str(request.user)
        to_mail = [d1Sup]
        #to_mail = ['manoj@theabacusindia.com','sunit@theabacusindia.com','siddhant.ratna@yahoo.com','rk468335@gmail.com']
        mail = EmailMessage(f"Store Data Daily Entry Report", f'ABACUS PLATINUM CLUB\n----------------------------------------\nDear Supervisor your report for Date : {d1} is prepared in Xls and CSV file format.', settings.DEFAULT_FROM_EMAIL,to_mail)
        mail.attach(excelFile.strip(), response.getvalue(), 'text/xls')
        mail.attach(csvfile.strip(), response.getvalue(), 'text/csv')
        mail.send()
        # ==========================================================================================================
        print('Mail sent successfully to >>>',to_mail)
        # ===============================================================================

    return redirect('/')


@login_required(login_url="/signup")
def amountOfPurchaseReport(request):
    if request.method == 'GET':
        if request.user:
            print('user >>> ',request.user)
        if request.user.is_superuser:
            return HttpResponseRedirect('ab_admin')
        if request.user.is_staff:
            array = eval(request.session['storeArray'])
            storeArray = []
            storenameArray = ''
            for i in array:
                data = store_detail.objects.get(id = int(i))
                dataDict = {}
                dataDict['id'] = int(i)
                dataDict['storeName'] = data.store_name
                dataDict['storeID'] = data.storeID
                storeArray.append(dataDict)
                storenameArray = storenameArray + data.store_name+','

            print('storeArray  >>> ',storeArray)
            supervisorObj = supervisorDetails.objects.get(supervisor_email = request.user)
            supervisor_amountOfPurchase_Report_HistoryData = supervisor_Report_History_for_amount.objects.filter(supervisor_FK = supervisorObj)
        return render(request,'supervisor_template/amountOfPurchaseReport.html',{'supervisor_amountOfPurchase_Report_HistoryData': supervisor_amountOfPurchase_Report_HistoryData,'storeArray':storeArray,'storelength':len(storeArray)})

    if request.method == 'POST':
        selectedStoreArray = request.POST.getlist('storeArray[]')
        dateRange = request.POST['dateRange']

        reportId = ''
        try:
            store_groups = supervisor_Report_History_for_amount.objects.latest('id').id
            store_groups = int(store_groups) + 1
            reportId = 'RPID_00'+str(store_groups)
        except:
            reportId = 'RPID_001'

        print('=========================================================================')
        print('reportId >>>>> ',reportId)
        print('selectedStoreArray >>>>> ',selectedStoreArray)
        print('dateRange >>>>> ',dateRange)
        print('=========================================================================')
        # ---------------------------------------------------------------
        message = ''
        try:
            supervisorObj = supervisorDetails.objects.get(supervisor_email = request.user)
            supervisor_amountOfPurchase_Report_HistoryObject = supervisor_Report_History_for_amount(supervisor_FK = supervisorObj,reportID=reportId.strip(),selected_stores=selectedStoreArray,dateRange=dateRange)
            supervisor_amountOfPurchase_Report_HistoryObject.save()
            message = 'Success'
        except:
            message = 'Failed'
        # ---------------------------------------------------------------

        return JsonResponse({'message' : message})




@login_required(login_url="/signup")
def downloadAmountPurchaseReport(request,id):
    reportData = supervisor_Report_History_for_amount.objects.get(id = int(id))
    report_ID = reportData.reportID
    selected_stores = eval(reportData.selected_stores)
    dateRange = reportData.dateRange.split('-')

    print('report_ID >>> ',report_ID)
    print('selected_stores >>> ',selected_stores)
    print('dateRange >>> ',dateRange)
    # ------------------------------------------------------------------
    startDate = dateRange[0].strip().split('/')
    endDate = dateRange[1].strip().split('/')

    start_date = datetime.date(int(startDate[2]), int(startDate[0]), int(startDate[1])) 
    end_date = datetime.date(int(endDate[2]), int(endDate[0]), int(endDate[1])) 
    print('startDate >>> ',start_date)
    print('endDate >>> ',end_date)
    # ------------------------------------------------------------------
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Date Range : '+reportData.dateRange,'','','',''])
    writer.writerow(['========================================================================================================================','','','',''])
    for storeIDs in selected_stores:
        storeDeta = store_detail.objects.get(storeID=storeIDs)
        writer.writerow(['REPORT ID : '+report_ID,'','','',''])
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Stores Detail : '+str(storeIDs),' >>> ',storeDeta.store_name,'',''])
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Customer Name','Customer Contact','Customer Email','Total Purchase (In Rs.)'])
        # user = CustomerShopData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=storeIDs)
        user = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=storeIDs).distinct()
        print('user data >>>',len(user),user)


        for i in user:
            print('i data',i.contact)
            customerInfo = CustomerShopData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,customerID=i,storeID=storeIDs)
            # if(len(customerInfo) !=0):
            print('customerInfo data',customerInfo)
            amountSum = 0
            for j in customerInfo:
                amountSum = amountSum + int(j.amount)
                print('amountSum data',amountSum)
            writer.writerow([i.name,i.contact,i.email,amountSum])
            print('------------------------------------------------------------------')
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
    response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'.csv"'
    return response





@login_required(login_url="/signup")
def noOfvisitReport(request):
    if request.method == 'GET':
        if request.user:
            print('user ==>>> ',request.user)
        if request.user.is_superuser:
            return HttpResponseRedirect('ab_admin')
        if request.user.is_staff:
            array = eval(request.session['storeArray'])
            storeArray = []
            storenameArray = ''
            for i in array:
                data = store_detail.objects.get(id = int(i))
                dataDict = {}
                dataDict['id'] = int(i)
                dataDict['storeName'] = data.store_name
                dataDict['storeID'] = data.storeID
                storeArray.append(dataDict)
                storenameArray = storenameArray + data.store_name+','

            print('storeArray  >>> ',storeArray)
            store_data = store_detail.objects.all()
            supervisorObj = supervisorDetails.objects.get(supervisor_email = request.user)
            supervisor_amountOfPurchase_Report_HistoryData = supervisor_Report_History_for_visit.objects.filter(supervisor_FK = supervisorObj)
        return render(request,'supervisor_template/noOfVisitreport.html',{'supervisor_amountOfPurchase_Report_HistoryData': supervisor_amountOfPurchase_Report_HistoryData,'store_detail': store_data,'storeArray':storeArray,'storelength':len(storeArray)})
    if request.method == 'POST':
        selectedStoreArray = request.POST.getlist('storeArray[]')
        dateRange = request.POST['dateRange']

        reportId = ''
        try:
            store_groups = supervisor_Report_History_for_visit.objects.latest('id').id
            store_groups = int(store_groups) + 1
            reportId = 'RPID_00'+str(store_groups)
        except:
            reportId = 'RPID_001'

        print('=========================================================================')
        print('reportId >>>>> ',reportId)
        print('selectedStoreArray >>>>> ',selectedStoreArray)
        print('dateRange >>>>> ',dateRange)
        print('=========================================================================')
        # ---------------------------------------------------------------
        message = ''
        try:
            supervisorObj = supervisorDetails.objects.get(supervisor_email = request.user)
            supervisor_noOfVisit_Report_HistoryObject = supervisor_Report_History_for_visit(supervisor_FK = supervisorObj,reportID=reportId.strip(),selected_stores=selectedStoreArray,dateRange=dateRange)
            supervisor_noOfVisit_Report_HistoryObject.save()
            message = 'Success'
        except:
            message = 'Failed'
        # ---------------------------------------------------------------

        return JsonResponse({'message' : message})



@login_required(login_url="/signup")
def downloadNumberOfVisitReport(request,id):
    reportData = supervisor_noOfVisit_Report_History.objects.get(id = int(id))
    report_ID = reportData.reportID
    selected_stores = eval(reportData.selected_stores)
    dateRange = reportData.dateRange.split('-')

    print('report_ID >>> ',report_ID)
    print('selected_stores >>> ',selected_stores)
    print('dateRange >>> ',dateRange)
    # ------------------------------------------------------------------
    startDate = dateRange[0].strip().split('/')
    endDate = dateRange[1].strip().split('/')

    start_date = datetime.date(int(startDate[2]), int(startDate[0]), int(startDate[1])) 
    end_date = datetime.date(int(endDate[2]), int(endDate[0]), int(endDate[1])) 
    print('startDate >>> ',start_date)
    print('endDate >>> ',end_date)
    # ------------------------------------------------------------------
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Date Range : '+reportData.dateRange,'','','',''])
    writer.writerow(['========================================================================================================================','','','',''])
    for storeIDs in selected_stores:
        storeDeta = store_detail.objects.get(storeID=storeIDs)
        writer.writerow(['REPORT ID : '+report_ID,'','','',''])
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Stores Detail : '+str(storeIDs),' >>> ',storeDeta.store_name,'',''])
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Customer Name','Customer Contact','Customer Email','Total Number of Visits'])
        # user = CustomerShopData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=storeIDs)
        user = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=storeIDs).distinct()
        print('user data >>>',len(user),user)


        for i in user:
            customerInfo = CustomerShopData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,customerID=i,storeID=storeIDs)
            writer.writerow([i.name,i.contact,i.email,len(customerInfo)])
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
    response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'.csv"'
    return response