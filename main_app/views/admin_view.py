from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from main_app.models.store_manager_models import *
from main_app.models.login_models import registration
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import json,csv,datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Sum,Avg
from django.core.paginator import Paginator
from django.core.mail import message, send_mass_mail
import requests,re
from django.db.models.functions import ExtractYear
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg, Max, Min, Sum
import schedule,calendar,time,datetime
from django.core.mail import send_mail
from django.conf import settings

from datetime import date
import xlwt
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# ---------------------------------------------------------------------------------------------------------------------------------
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/ab_admin')

@staff_member_required(login_url="/signup")
def admin_dash(request):
    # try:
    if request.user.is_superuser:
        usr = User.objects.get(id=request.user.id)
        reg = registration.objects.get(user=usr)
        admin_dash = store_manager.objects.all().order_by('id')
        admin_store = store_detail.objects.all()
        paginator = Paginator(admin_dash,5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        avgAmount = CustomerShopData.objects.values('amount')
        current_date = datetime.datetime.now().date()
        current_month = current_date.month
        current_day = current_date.day


        # Total Customers/month
        total_cust = CustomerData.objects.all()
        x = CustomerData.objects.annotate(month=TruncMonth('time_stamp')).values('month').annotate(customer_count=Count('id')).values('month', 'customer_count')
        avg = CustomerShopData.objects.annotate(month=TruncMonth('time_stamp')).values('month').annotate(month_avg=Avg('amount')).values('month', 'month_avg')
        
        total = CustomerShopData.objects.annotate(month=TruncMonth('time_stamp')).values('month').annotate(month_sum=Sum('amount')).values('month', 'month_sum')


        print('x value ',x)
        print('avg value ',avg)
        print('total value ',total)


        # exit()
        
        customer_count=len(x)
        customer_avg = len(avg)
        context_1 = {}
        context_2 = {}

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

        l1 = []
        for i in range(customer_count):
            context_1['month_'+str(x[i]['month'].date().month)] = x[i]['customer_count']
        for i in context_1.values():
            l1.append(i)  

        invoices = CustomerShopData.objects.all()
        months = invoices.datetimes("time_stamp", kind="month")

        print('months >>> ',months)
        count = 1
        for month in months:
            month_invs = invoices.filter(time_stamp__month=month.month)
            month_total = month_invs.aggregate(total=Sum("amount")).get("total")
            print(f"Month: {month}, Total: {month_total}")
            context_2['month_avg_'+str(month.month)] = int(month_total)
            count = count + 1
            
        # l2 = []
        # for i in range(customer_avg):
        #     context_2['month_avg_' + str(avg[i]['month'].date().month)] = int(avg[i]['month_avg'])
        # # exit()
        # for i in context_2.values():
        #     l2.append(i)
        context ={}
        context['admin_dash'] = admin_dash
        context['admin_store'] = admin_store
                
        request.session['admin_cust_list'] = l1
        # request.session['admin_avg_list'] = l2

        return render(request, 'admin_template/index.html', {'admin_image': reg.profile_pic,'page_obj' : page_obj,'context' : context,'context_1': context_1, 'context_2': context_2})
    
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')
    
    # except:
    #     return render(request,'404.html')+


# ---------------------------------------------------------------------------------------------------------------------------------
@staff_member_required(login_url="/signup")
def add_store(request):
    if request.user.is_superuser:
        data = category.objects.values('category')
        storeID = store_detail.objects.all()
        return render(request, 'admin_template/add-store.html',{'data':data})
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')

# Utility function : format [ABACUS_(n)]
def generateStoreID(storeID):
    previousID = storeID['id']
    nextID = previousID + 1
    generatedID = 'ABACUSxxx'+str(nextID)
    return generatedID

def fetchCategory(request):
    return HttpResponse('hello')
# ---------------------------------------------------------------------------------------------------------------------------------


@staff_member_required(login_url="/signup")
def store_list(request):
    if request.user.is_superuser:
        storeResult = store_detail.objects.all()    
        return render(request, 'admin_template/stores-list.html', {'storeResult': storeResult})
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')


@staff_member_required(login_url="/signup")
def edit_store(request,id):
    # try:
    if request.user.is_superuser:
        if request.method == 'POST':
            storeName = request.POST['store_name'].strip()
            storeLocation = request.POST['store_location'].strip()
            storeCity = request.POST['store_city'].strip()
            storState = request.POST['store_state'].strip()
            managerProfileImage = request.FILES.get('managerProfileImage')
            # -----------------------------------------------------------------------------------
            mangerContactNo = request.POST['mangerContactNo'].strip()
            mangerOldNo = request.POST['mangerOldContactNo'].strip()
            manager_obj = store_manager.objects.get(manager_contact=mangerOldNo)
            img_data = manager_obj.manager_image
            pemail = manager_obj.manager_email

            if(managerProfileImage == None):
                managerProfileImage = img_data
            # -----------------------------------------------------------------------------------
            mangerName = request.POST['mangerName'].strip()
            managerGender = request.POST['managerGender'].strip()
            email = request.POST['managerEmail'].strip()
            newpassword = request.POST.get('managerConfirmPass').strip()

            supervisorName = request.POST.get('supervisorName')
            supervisorContactNO = request.POST.get('supervisorContactNO')
            supervisorEmail = request.POST.get('supervisorEmail')
            supervisorGender = request.POST.get('supervisorGender')
            
            accessEntryOfData = request.POST['accessEntryOfData'].strip()
            usr = User.objects.get(email=pemail)
            usr.first_name = mangerName
            usr.email = email
            usr.usrename = email
            if newpassword != "":
                usr.set_password(newpassword)
            usr.save()

            reg_obj = registration.objects.get(user = usr)
            reg_obj.user = usr
            reg_obj.contact = mangerContactNo
            reg_obj.profile_pic = managerProfileImage
            reg_obj.entry_type = accessEntryOfData
            if newpassword != "":
                reg_obj.password_saved = newpassword
            reg_obj.save()
            
            store_obj = store_detail.objects.get(id=id)
            store_obj.store_name = storeName
            store_obj.store_location = storeLocation
            store_obj.store_town=storeCity
            store_obj.store_city=storeCity
            store_obj.store_state=storState
            store_obj.save()

            manager_obj = store_manager.objects.get(store=store_obj)
            mangerId = manager_obj.id
            manager_obj.manager_name = mangerName
            manager_obj.manager_contact =mangerContactNo
            manager_obj.manager_image =managerProfileImage
            manager_obj.user_unique_id = mangerContactNo
            manager_obj.manager_email =email
            manager_obj.gender =managerGender
            manager_obj.entry_type =accessEntryOfData
            # manager_obj.manager_password = newpassword
            manager_obj.save()
            
            # supervisor_obj = Store_supervisor.objects.get(id=mangerId)
            # supervisor_obj.supervisor_name = supervisorName
            # supervisor_obj.supervisor_contact =supervisorContactNO
            # supervisor_obj.supervisor_email =supervisorEmail
            # supervisor_obj.supervisor_gender =supervisorGender
            # supervisor_obj.save()


            storeResult = store_detail.objects.all()
            return render(request, 'admin_template/stores-list.html', {'storeResult': storeResult,'success' : 'Store details updated successfully!'})

        else:
            # exit()
            store_obj = store_detail.objects.get(pk=id)
            manager_obj = store_manager.objects.get(store=store_obj)
            img_data = manager_obj.manager_image
            managerId = manager_obj.id
            # supervisor_obj = Store_supervisor.objects.get(pk=managerId)
            
            context = {}
            context['store'] = store_obj
            context['manager'] = manager_obj
            # context['supervisor'] = supervisor_obj

            return render(request, 'admin_template/edit-store-detail.html',context)
        # except:
        #     store_obj = store_detail.objects.get(pk=id)
        #     manager_obj = store_manager.objects.get(pk=id)
        #     supervisor_obj = Store_supervisor.objects.get(pk=id)
        #     context = {'error':'An error Occured while updating store details! Please try again with Valid data.'}
        #     context['store'] = store_obj
        #     context['manager'] = manager_obj
        #     context['supervisor'] = supervisor_obj
        #     return render(request, 'admin_template/edit-store-detail.html', context)
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')


@staff_member_required(login_url="/signup")
def checkmanagerstatus(request):
    if request.method == 'POST':
        storeID = request.POST['storeId']
        store = store_detail.objects.get(storeID=storeID)
        manager = store_manager.objects.get(store=store)
        checkManagerStatus = store.statusflag
        # false flag = " Manager is inactive "
        # true flag = " Manager is active "
        flag = False
        if(checkManagerStatus == True):
            user = User.objects.get(email = manager.manager_email )
            if(user.is_active == True):
                user.is_active = False
                store.statusflag = False
                user.save()
                store.save()
                flag = False
                    
        else:
            user = User.objects.get(email = manager.manager_email )
            if(user.is_active == False):
                user.is_active = True
                store.statusflag = True
                user.save()
                store.save()
                flag = True
        return HttpResponse(flag)


@staff_member_required(login_url="/signup")
def delete_store(request, id):
    try:
        if request.user.is_superuser:
            if request.method == 'POST':
                del_data = store_detail.objects.get(pk=id)
                # del_supervisor = Store_supervisor.objects.get(pk=id)
                regData = registration.objects.get(storeID = del_data.storeID)

                managerdata = store_manager.objects.get(store = del_data)
                managerEmail = managerdata.manager_email
                userData = User.objects.get(email = managerEmail)

                del_data.delete()
                # del_supervisor.delete()
                regData.delete()
                userData.delete()
                
                return HttpResponseRedirect('/store_list')
        if request.user.is_staff:
            return HttpResponseRedirect('/dashboard')
    except:
        return render(request, '404.html')

#

# ---------------------------------------------------------------------------------------------------------------------------------

def CreateFilterTierModel(modelData):
    if len(modelData) != 0:
        tierPeriod = modelData[0]['time_period']
        return tierPeriod

def CreateFilterTierYear(timePeriod):
    if int(timePeriod) == 1:
        startdate = datetime.datetime.now()
        enddate = datetime.datetime.now() - datetime.timedelta(days=1*365)
        filterDates = startdate.date(),enddate.date()
        return filterDates
    if int(timePeriod) == 2:
        startdate = datetime.datetime.now()
        enddate = datetime.datetime.now() - datetime.timedelta(days=2*365)
        filterDates = startdate.date(),enddate.date()
        return filterDates
    if int(timePeriod) == 3:
        startdate = datetime.datetime.now()
        enddate = datetime.datetime.now() - datetime.timedelta(days=3*365)
        filterDates = startdate.date(),enddate.date()
        return filterDates
    if int(timePeriod) == 4:
        startdate = datetime.datetime.now()
        enddate = datetime.datetime.now() - datetime.timedelta(days=4*365)
        filterDates = startdate.date(),enddate.date()
        return filterDates





@staff_member_required(login_url="/signup")
def customerFilterApply(request):
    if request.method == 'GET':
        filterCustomerList = []
        filterCustomerDict = {}
        tierSelect = request.GET['tierSelect']
        if tierSelect.strip() == "TierSelect":
            storeNamelist = request.GET.getlist('Category[]')
            tierType = request.GET.get('tierType')
            ListTier = request.GET.getlist('ListTier[]')
            if tierType.strip() == 'collective':
                lenTier = len(ListTier)
                if lenTier > 0:
                    if lenTier == 1:
                        if ListTier[0].strip() == 'Tier 1':
                            
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                tierTimeModel = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1]).values('time_period')
                                tierPeriod = CreateFilterTierModel(tierTimeModel)
                                
                                if tierPeriod != None:
                                    filterDates = CreateFilterTierYear(tierPeriod)
                                    start_date, end_date = filterDates
                                    tierAMT = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                    amountStartTier = tierAMT['amtStart']
                                    amountEndTier = tierAMT['amtEND']
                                    csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                    dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                    if len(dataAMT) != 0:
                                        for checkCust in csutrData:
                                            dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                            if dataAMT['amt'] != None:
                                                if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                    filterCustomerDict["CutomerName"] = checkCust.name
                                                    filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                    filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                    filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                    filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                    filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                    filterCustomerDict["id"] = checkCust.id
                                                    filterCustomerList.append(filterCustomerDict)
                                                    filterCustomerDict = {}
                                            else:
                                                filterCustomerList = filterCustomerList
                                    
                               

                        elif ListTier[0].strip() == 'Tier 2':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                tierTimeModel = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[2]).values('time_period')
                                tierPeriod = CreateFilterTierModel(tierTimeModel)
                                if tierPeriod != None:
                                    filterDates = CreateFilterTierYear(tierPeriod)
                                    start_date, end_date = filterDates
                                    tierAMT = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[2]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                    amountStartTier = tierAMT['amtStart']
                                    amountEndTier = tierAMT['amtEND']
                                    csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                    dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                    if len(dataAMT) != 0:
                                        for checkCust in csutrData:
                                            dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                            if dataAMT['amt'] != None:
                                                if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                    filterCustomerDict["CutomerName"] = checkCust.name
                                                    filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                    filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                    filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                    filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                    filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                    filterCustomerDict["id"] = checkCust.id
                                                    filterCustomerList.append(filterCustomerDict)
                                                    filterCustomerDict = {}
                                            else:
                                                filterCustomerList = filterCustomerList
                            
                        elif ListTier[0].strip() == 'Tier 3':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                tierTimeModel = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1]).values('time_period')
                                tierPeriod = CreateFilterTierModel(tierTimeModel)
                                if tierPeriod != None:
                                    filterDates = CreateFilterTierYear(tierPeriod)
                                    start_date, end_date = filterDates
                                    tierAMT = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                    amountStartTier = tierAMT['amtStart']
                                    amountEndTier = tierAMT['amtEND']
                                    csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                    dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                    if len(dataAMT) != 0:
                                        for checkCust in csutrData:
                                            dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                            if dataAMT['amt'] != None:
                                                if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                    filterCustomerDict["CutomerName"] = checkCust.name
                                                    filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                    filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                    filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                    filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                    filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                    filterCustomerDict["id"] = checkCust.id
                                                    filterCustomerList.append(filterCustomerDict)
                                                    filterCustomerDict = {}
                                            else:
                                                filterCustomerList = filterCustomerList
                            
                           
                    if lenTier == 2:
                        if ListTier[0].strip() == 'Tier 1' and ListTier[1].strip() == 'Tier 2':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                tierTimeModel = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1,2]).values('time_period')
                                tierPeriod = CreateFilterTierModel(tierTimeModel)
                                if tierPeriod != None:
                                    filterDates = CreateFilterTierYear(tierPeriod)
                                    start_date, end_date = filterDates
                                    # tierAMT = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1,2]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                    tierAMTmin = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[2]).aggregate(Min('shop_start_amt'))
                                    tierAMTmax = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1]).aggregate(Max('shop_end_amt'))
                                    amountEndTier = tierAMTmax['shop_end_amt__max']
                                    amountStartTier = tierAMTmin['shop_start_amt__min']
                                    csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                    dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                    if len(dataAMT) != 0:
                                        for checkCust in csutrData:
                                            dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                            if dataAMT['amt'] != None:
                                                if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                    filterCustomerDict["CutomerName"] = checkCust.name
                                                    filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                    filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                    filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                    filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                    filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                    filterCustomerDict["id"] = checkCust.id
                                                    filterCustomerList.append(filterCustomerDict)
                                                    filterCustomerDict = {}
                                            else:
                                                filterCustomerList = filterCustomerList
                            
                        elif ListTier[0].strip() == 'Tier 2' and ListTier[1].strip() == 'Tier 3':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                tierTimeModel = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[2,3]).values('time_period')
                                tierPeriod = CreateFilterTierModel(tierTimeModel)
                                if tierPeriod != None:
                                    filterDates = CreateFilterTierYear(tierPeriod)
                                    start_date, end_date = filterDates
                                    # tierAMT = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[2,3]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                    tierAMTmin = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[3]).aggregate(Min('shop_start_amt'))
                                    tierAMTmax = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[2]).aggregate(Max('shop_end_amt'))
                                    amountEndTier = tierAMTmax['shop_end_amt__max']
                                    amountStartTier = tierAMTmin['shop_start_amt__min']
                                    csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                    dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                    if len(dataAMT) != 0:
                                        for checkCust in csutrData:
                                            dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                            if dataAMT['amt'] != None:
                                                if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                    filterCustomerDict["CutomerName"] = checkCust.name
                                                    filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                    filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                    filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                    filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                    filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                    filterCustomerDict["id"] = checkCust.id
                                                    filterCustomerList.append(filterCustomerDict)
                                                    filterCustomerDict = {}
                                            else:
                                                filterCustomerList = filterCustomerList
                            
                        elif ListTier[0].strip() == 'Tier 1' and ListTier[1].strip() == 'Tier 3':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                tierTimeModel = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1,3]).values('time_period')
                                tierPeriod = CreateFilterTierModel(tierTimeModel)
                                if tierPeriod != None:
                                    filterDates = CreateFilterTierYear(tierPeriod)
                                    start_date, end_date = filterDates
                                    # tierAMT = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1,3]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                    tierAMTmin = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[3]).aggregate(Min('shop_start_amt'))
                                    tierAMTmax = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1]).aggregate(Max('shop_end_amt'))
                                    amountEndTier = tierAMTmax['shop_end_amt__max']
                                    amountStartTier = tierAMTmin['shop_start_amt__min']
                                    csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                    dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                    if len(dataAMT) != 0:
                                        for checkCust in csutrData:
                                            dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                            if dataAMT['amt'] != None:
                                                if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                    filterCustomerDict["CutomerName"] = checkCust.name
                                                    filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                    filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                    filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                    filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                    filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                    filterCustomerDict["id"] = checkCust.id
                                                    filterCustomerList.append(filterCustomerDict)
                                                    filterCustomerDict = {}
                                            else:
                                                filterCustomerList = filterCustomerList
                            
                            

                    if lenTier == 3:
                        for shopName in storeNamelist:                            
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1,2,3]).values('time_period')
                            

                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                # tierAMT = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1,2,3]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                tierAMTmin = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[3]).aggregate(Min('shop_start_amt'))
                                tierAMTmax = tier_collective.objects.filter(tierType='Collective', tierRuleNo__in=[1]).aggregate(Max('shop_end_amt'))

                                amountEndTier = tierAMTmax['shop_end_amt__max']
                                amountStartTier = tierAMTmin['shop_start_amt__min']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
            # ###########################################    ONBOARD FILTER   ############################################################
            elif tierType.strip() == 'onboard':
                lenTier = len(ListTier)
                if lenTier > 0:
                    if lenTier == 1:
                        if ListTier[0].strip() == 'Tier 1':
                            
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)

                                OnboardData = CustomerOnboardData.objects.filter(storeID=shopName.storeID,tierRuleNo=1)
                                for i in OnboardData:
                                    filterCustomerDict["CutomerName"] = i.customerID.name
                                    filterCustomerDict["CutomerCONTACT"] = i.customerID.contact
                                    filterCustomerDict["CutomerEMAIL"] = i.customerID.email
                                    filterCustomerDict["CutomerGENDER"] = i.customerID.gender
                                    filterCustomerDict["CutomerDOB"] = i.customerID.DOB
                                    filterCustomerDict["CutomerDOM"] = i.customerID.DOM
                                    filterCustomerDict["id"] = i.customerID.id
                                    filterCustomerList.append(filterCustomerDict)
                                    filterCustomerDict = {}
                            
                                

                        if ListTier[0].strip() == 'Tier 2':
                            
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)

                                OnboardData = CustomerOnboardData.objects.filter(storeID=shopName.storeID,tierRuleNo=2)
                                for i in OnboardData:
                                    filterCustomerDict["CutomerName"] = i.customerID.name
                                    filterCustomerDict["CutomerCONTACT"] = i.customerID.contact
                                    filterCustomerDict["CutomerEMAIL"] = i.customerID.email
                                    filterCustomerDict["CutomerGENDER"] = i.customerID.gender
                                    filterCustomerDict["CutomerDOB"] = i.customerID.DOB
                                    filterCustomerDict["CutomerDOM"] = i.customerID.DOM
                                    filterCustomerDict["id"] = i.customerID.id
                                    filterCustomerList.append(filterCustomerDict)
                                    filterCustomerDict = {}

                        if ListTier[0].strip() == 'Tier 3':
                            
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)

                                OnboardData = CustomerOnboardData.objects.filter(storeID=shopName.storeID,tierRuleNo=3)
                                for i in OnboardData:
                                    filterCustomerDict["CutomerName"] = i.customerID.name
                                    filterCustomerDict["CutomerCONTACT"] = i.customerID.contact
                                    filterCustomerDict["CutomerEMAIL"] = i.customerID.email
                                    filterCustomerDict["CutomerGENDER"] = i.customerID.gender
                                    filterCustomerDict["CutomerDOB"] = i.customerID.DOB
                                    filterCustomerDict["CutomerDOM"] = i.customerID.DOM
                                    filterCustomerDict["id"] = i.customerID.id
                                    filterCustomerList.append(filterCustomerDict)
                                    filterCustomerDict = {}
                            
                           
                    if lenTier == 2:
                        if ListTier[0].strip() == 'Tier 1' and ListTier[1].strip() == 'Tier 2':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)

                                OnboardData = CustomerOnboardData.objects.filter(storeID=shopName.storeID,tierRuleNo__in=[1,2])
                                for i in OnboardData:
                                    filterCustomerDict["CutomerName"] = i.customerID.name
                                    filterCustomerDict["CutomerCONTACT"] = i.customerID.contact
                                    filterCustomerDict["CutomerEMAIL"] = i.customerID.email
                                    filterCustomerDict["CutomerGENDER"] = i.customerID.gender
                                    filterCustomerDict["CutomerDOB"] = i.customerID.DOB
                                    filterCustomerDict["CutomerDOM"] = i.customerID.DOM
                                    filterCustomerDict["id"] = i.customerID.id
                                    filterCustomerList.append(filterCustomerDict)
                                    filterCustomerDict = {}
                            
                        if ListTier[0].strip() == 'Tier 2' and ListTier[1].strip() == 'Tier 3':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                OnboardData = CustomerOnboardData.objects.filter(storeID=shopName.storeID,tierRuleNo__in=[2,3])
                                for i in OnboardData:
                                    filterCustomerDict["CutomerName"] = i.customerID.name
                                    filterCustomerDict["CutomerCONTACT"] = i.customerID.contact
                                    filterCustomerDict["CutomerEMAIL"] = i.customerID.email
                                    filterCustomerDict["CutomerGENDER"] = i.customerID.gender
                                    filterCustomerDict["CutomerDOB"] = i.customerID.DOB
                                    filterCustomerDict["CutomerDOM"] = i.customerID.DOM
                                    filterCustomerDict["id"] = i.customerID.id
                                    filterCustomerList.append(filterCustomerDict)
                                    filterCustomerDict = {}
                            
                        elif ListTier[0].strip() == 'Tier 1' and ListTier[1].strip() == 'Tier 3':
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                OnboardData = CustomerOnboardData.objects.filter(storeID=shopName.storeID,tierRuleNo__in=[1,3])
                                for i in OnboardData:
                                    filterCustomerDict["CutomerName"] = i.customerID.name
                                    filterCustomerDict["CutomerCONTACT"] = i.customerID.contact
                                    filterCustomerDict["CutomerEMAIL"] = i.customerID.email
                                    filterCustomerDict["CutomerGENDER"] = i.customerID.gender
                                    filterCustomerDict["CutomerDOB"] = i.customerID.DOB
                                    filterCustomerDict["CutomerDOM"] = i.customerID.DOM
                                    filterCustomerDict["id"] = i.customerID.id
                                    filterCustomerList.append(filterCustomerDict)
                                    filterCustomerDict = {}
                            
                            

                    if lenTier == 3:
                            for shopName in storeNamelist:
                                shopName = store_detail.objects.get(store_name=shopName)
                                OnboardData = CustomerOnboardData.objects.filter(storeID=shopName.storeID,tierRuleNo__in=[1,2,3])
                                for i in OnboardData:
                                    filterCustomerDict["CutomerName"] = i.customerID.name
                                    filterCustomerDict["CutomerCONTACT"] = i.customerID.contact
                                    filterCustomerDict["CutomerEMAIL"] = i.customerID.email
                                    filterCustomerDict["CutomerGENDER"] = i.customerID.gender
                                    filterCustomerDict["CutomerDOB"] = i.customerID.DOB
                                    filterCustomerDict["CutomerDOM"] = i.customerID.DOM
                                    filterCustomerDict["id"] = i.customerID.id
                                    filterCustomerList.append(filterCustomerDict)
                                    filterCustomerDict = {}
            # ########################################################################################################################
            else:
                lenTier = len(ListTier)
                if lenTier == 1:
                    if ListTier[0].strip() == 'Tier 1':
                        for shopName in storeNamelist:
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1]).values('time_period')
                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                tierAMT = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                amountStartTier = tierAMT['amtStart']
                                amountEndTier = tierAMT['amtEND']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
                    elif ListTier[0].strip() == 'Tier 2':
                        for shopName in storeNamelist:
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[2]).values('time_period')
                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                tierAMT = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[2]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                amountStartTier = tierAMT['amtStart']
                                amountEndTier = tierAMT['amtEND']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
                    elif ListTier[0].strip() == 'Tier 3':
                        for shopName in storeNamelist:
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[3]).values('time_period')
                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                tierAMT = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[3]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                amountStartTier = tierAMT['amtStart']
                                amountEndTier = tierAMT['amtEND']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
                                                
                if lenTier == 2:
                    if ListTier[0].strip() == 'Tier 1' and ListTier[1].strip() == 'Tier 2':
                        for shopName in storeNamelist:
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1,2]).values('time_period')
                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                tierAMT = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1,2]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                amountStartTier = tierAMT['amtStart']
                                amountEndTier = tierAMT['amtEND']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
                    elif ListTier[0].strip() == 'Tier 2' and ListTier[1].strip() == 'Tier 3':
                        for shopName in storeNamelist:
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[2,3]).values('time_period')
                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                tierAMT = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[2,3]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                amountStartTier = tierAMT['amtStart']
                                amountEndTier = tierAMT['amtEND']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
                    elif ListTier[0].strip() == 'Tier 1' and ListTier[1].strip() == 'Tier 3':
                        for shopName in storeNamelist:
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1,3]).values('time_period')
                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                tierAMT = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1,3]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                amountStartTier = tierAMT['amtStart']
                                amountEndTier = tierAMT['amtEND']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
                        
                if lenTier == 3:
                    for shopName in storeNamelist:
                            shopName = store_detail.objects.get(store_name=shopName)
                            tierTimeModel = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1,2,3]).values('time_period')
                            tierPeriod = CreateFilterTierModel(tierTimeModel)
                            if tierPeriod != None:
                                filterDates = CreateFilterTierYear(tierPeriod)
                                start_date, end_date = filterDates
                                tierAMT = tier_individual.objects.filter(tierType='Individual', tierRuleNo__in=[1,2,3]).aggregate(amtStart = Sum('shop_start_amt'),amtEND = Sum('shop_end_amt'))
                                amountStartTier = tierAMT['amtStart']
                                amountEndTier = tierAMT['amtEND']
                                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                                dataAMT = CustomerShopData.objects.filter(storeID=shopName.storeID).values('time_stamp')
                                if len(dataAMT) != 0:
                                    for checkCust in csutrData:
                                        dataAMT = CustomerShopData.objects.filter(time_stamp__range=[end_date ,start_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                                        if dataAMT['amt'] != None:
                                            if int(amountStartTier) <= int(dataAMT['amt']) and int(amountEndTier) >= int(dataAMT['amt']):
                                                filterCustomerDict["CutomerName"] = checkCust.name
                                                filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                                                filterCustomerDict["CutomerEMAIL"] = checkCust.email
                                                filterCustomerDict["CutomerGENDER"] = checkCust.gender
                                                filterCustomerDict["CutomerDOB"] = checkCust.DOB
                                                filterCustomerDict["CutomerDOM"] = checkCust.DOM
                                                filterCustomerDict["id"] = checkCust.id
                                                filterCustomerList.append(filterCustomerDict)
                                                filterCustomerDict = {}
                                        else:
                                            filterCustomerList = filterCustomerList
        elif(tierSelect.strip() == "NoTierSelect"):
            storeNamelist = request.GET.getlist('cate[]')
            dateRangeFilter = request.GET.get('date')

            print('storeNamelist >>> ',storeNamelist)
            print('dateRangeFilter >>> ',dateRangeFilter)

            dates = dateRangeFilter.split('-')
            date1 = dates[0].strip()
            date2 = dates[1].strip()
            m1 ,d1, y1 = [int(x) for x in date1.split('/')]
            m2, d2, y2 = [int(y) for y in date2.split('/')]
            start_date = datetime.date(y1, m1, d1)
            end_date = datetime.date(y2, m2, d2)
            amountfilter = request.GET.get('amt')
            listAMT = amountfilter.split('-')
            minAMT = 0
            maxAMT = 0
            minAMT = listAMT[0].strip().replace("Rs.", "")
            maxAMT = listAMT[1].strip().replace("Rs.", "")
            filterCustomerList = []
            filterCustomerDict = {}
            for shopName in storeNamelist:
                shopName = store_detail.objects.get(store_name=shopName)
                csutrData = CustomerData.objects.filter(storeID=shopName.storeID)
                # print('csutrData >>> ',len(csutrData))
                for checkCust in csutrData:
                    dataAMT = CustomerShopData.objects.filter(time_stamp__range=[start_date, end_date],customerID=checkCust).aggregate(amt = Sum('amount'))
                    # print('dataAMT >>> ',dataAMT['amt'])
                    if dataAMT['amt'] != None:
                        if int(minAMT) <= int(dataAMT['amt']) and int(maxAMT) >= int(dataAMT['amt']):
                            filterCustomerDict["CutomerName"] = checkCust.name
                            filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                            filterCustomerDict["CutomerEMAIL"] = checkCust.email
                            filterCustomerDict["CutomerGENDER"] = checkCust.gender
                            filterCustomerDict["CutomerDOB"] = checkCust.DOB
                            filterCustomerDict["CutomerDOM"] = checkCust.DOM
                            filterCustomerDict["id"] = checkCust.id
                            filterCustomerList.append(filterCustomerDict)
                            filterCustomerDict = {}
                    else:
                        # filterCustomerList = filterCustomerList
                        filterCustomerDict["CutomerName"] = checkCust.name
                        filterCustomerDict["CutomerCONTACT"] = checkCust.contact
                        filterCustomerDict["CutomerEMAIL"] = checkCust.email
                        filterCustomerDict["CutomerGENDER"] = checkCust.gender
                        filterCustomerDict["CutomerDOB"] = checkCust.DOB
                        filterCustomerDict["CutomerDOM"] = checkCust.DOM
                        filterCustomerDict["id"] = checkCust.id
                        filterCustomerList.append(filterCustomerDict)
                        filterCustomerDict = {}
        start_date = ""
        end_date = ""
        return HttpResponse(json.dumps(filterCustomerList),content_type="application/json")                    
            


@staff_member_required(login_url="/signup")
def customer_management(request):
    if request.user.is_superuser:
        customer_data = CustomerData.objects.all().order_by('id')

        uniqueCustomers = []
        for i in customer_data:
            uniqueCustomers.append(i.contact)


        print('customer_data count >>>> ',len(set(uniqueCustomers)))
        Customer_data_count = len(set(uniqueCustomers))
        store_data = store_detail.objects.all()
        paginator = Paginator(customer_data,20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin_template/customer-management.html', {'page_obj': page_obj,'Customer_data_count':Customer_data_count, 'Customer_data': customer_data, 'store_detail': store_data})
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')    
    
@staff_member_required(login_url="/signup")
def ajaxCustomer_management(request):
    customer_data = CustomerData.objects.all().order_by('id')
    store_data = store_detail.objects.all()

    paginator = Paginator(customer_data,20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return HttpResponse(page_obj)


# ---------------------------------------------------------------------------------------------------------------------------------
def tier_managememt_individual(request):
    store_data = store_detail.objects.all()
    return render(request, 'admin_template/tier-managememt-individual.html', {'store_data': store_data})


# ---------------------------------------------------------------------------------------------------------------------------------
def validate_adminemailID(request):
    try:
        email = request.GET['email']
        if(request.user.email == email):
            return HttpResponse('true')
        else:
            return HttpResponse('false')
    except:
        return render(request, 'store-manager/manual-entry.html')

def admin_profile(request):
    try:
        if request.user.is_superuser:
            if request.method == 'POST':
                name = request.POST['admin_name']
                email = request.POST['admin_email']
                image = request.FILES.get('admin_image')
                
                usr = User.objects.get(id=request.user.id)
                usr.first_name = name
                usr.email = email

                reg = registration.objects.get(user = usr)
                if image != None:
                    reg.profile_pic = image
                usr.save()
                reg.save()
                return redirect('admin_profile')
            else:
                usr = User.objects.get(id=request.user.id)
                reg = registration.objects.get(user = usr)

                return render(request, 'admin_template/profile.html',{'admin_image': reg.profile_pic,'email' : usr.email})
        if request.user.is_staff:
            return HttpResponseRedirect('/dashboard')  
    except:
        return redirect('home')

def chng_pwd(request):
    context = {}
    if request.user.is_superuser:
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
                return render(request, 'admin_template/change-password.html',context)
            return render(request, 'admin_template/change-password.html',context)
        return render(request, 'admin_template/change-password.html')
    if request.user.is_staff:
            return HttpResponseRedirect('/dashboard') 


# ##################################################################################################################################
# ###############################################   PRODUCT CATEGORY MANAGEMENT MODULE   ###########################################
# ##################################################################################################################################
@staff_member_required(login_url="/signup")
def product_category(request):
    try:
        if request.user.is_superuser:
            if request.method == 'POST':
                categoryItem = request.POST.get('Store_category')
                subCateItem = request.POST.getlist('Store_sub_category')
            
                categoryItem = categoryItem.strip()
                chechCate = category.objects.filter(category=categoryItem)
                if len(chechCate) == 0:
                    category_data = category(category=categoryItem,sub_category=subCateItem)
                    category_data.save()
                else:
                    category_data = category.objects.get(category=categoryItem)
                    category_data.sub_category = subCateItem
                    category_data.save()
                return HttpResponseRedirect('product_category_render')
        if request.user.is_staff:
            return HttpResponseRedirect('/dashboard') 
        
    except:
        return render(request, '404.html')
 


@staff_member_required(login_url="/signup")
def product_category_render(request):
    try:
        if request.user.is_superuser:
            subCate = category.objects.all().order_by('id')
            paginator = Paginator(subCate,5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            #for i in subCate:
            return render(request, 'admin_template/product-category.html', {'page_obj' : page_obj,'cat_data': subCate})
        if request.user.is_staff:
            return HttpResponseRedirect('/dashboard')
    except:
        return render(request, '404.html')


def checkCtagory(request):
    if request.method == 'GET':
        cat = request.GET['storeCategory']
        data = category.objects.filter(category=cat)
        catFlag = False
        if len(data) != 0:
            catFlag = True
        else:
            catFlag = False
        dataFlag = {catFlag:catFlag}
        return HttpResponse(dataFlag)


def AddSubCategoryDropDown(request):
    if request.method == 'POST':
        dataList = []
        cat = request.POST.getlist('dataList')
        
        cat = str(cat)
        cat = cat.replace("[", "")
        cat = cat.replace("]", "")
        cat = cat.replace("'", "")
        cat = cat.split(',')
        for i in cat:
            cate = i.strip()
            subCate = list(category.objects.filter(category=cate).values('sub_category'))
            for j in subCate:
                dataList.append(eval(j['sub_category']))
        return HttpResponse(json.dumps(dataList),content_type="application/json")


def checkStoreName(request):
    if request.method == 'GET':
        abacus_StoreName = request.GET['abacus_StoreName']
        data = store_detail.objects.filter(store_name=abacus_StoreName)
        lenData = len(data)
        flag = False
        if lenData == 1:
            flag = True
        else:
            flag = False
        return HttpResponse(flag)


def getLatestStoreID(request):
    if request.method == 'GET':
        try:
            data = store_detail.objects.values('id').latest('id')
            latestID = data['id']
            return HttpResponse(latestID)
        except:
            latestID = '0'
            return HttpResponse(latestID)

# ##################################################################################################################################
# ###############################################   STORE MANAGEMENT MODULE   ######################################################
# ##################################################################################################################################

@staff_member_required(login_url="/signup")
def AddStoreDetail(request):
    # try:
    if request.user.is_superuser:
        if request.method == 'POST':
            storeName = request.POST['storeName'].strip()
            storeLocation = request.POST['storeLocation'].strip()
            storeCity = request.POST['storeCity'].strip()
            storState = request.POST['storState'].strip()
            storCategory = request.POST.getlist('storCategory')
            storSubCategory = request.POST.getlist('storSubCategory')
            # Step2
            managerProfileImage = request.FILES.get('managerProfileImage')

            mangerName = request.POST['mangerName'].strip()
            mangerContactNo = request.POST['mangerContactNo'].strip()
            userUinqueID = request.POST['userUinqueID'].strip()
            managerGender = request.POST['managerGender'].strip()
            email = request.POST['managerEmail'].strip()
            password = request.POST['managerPass'].strip()
            supervisorName = request.POST.get('supervisorName')
            supervisorContactNO = request.POST.get('supervisorContactNO')
            supervisorEmail = request.POST.get('supervisorEmail')
            supervisorGender = request.POST.get('supervisorGender')
            if supervisorGender == None:
                supervisorGender = 'NA'
            accessEntryOfData = request.POST['accessEntryOfData'].strip()
            # Step3
            # imageFileName = managerProfileImage.split('\\')[-1]
            hashed_pwd = make_password(password)
            # check_password("plain_text",hashed_pwd)
            storeID = User.objects.values('id').latest('id')
            Store_newID = generateStoreID(storeID)

            usr = User.objects.create_user(email, email, password)
            usr.first_name = mangerName
            usr.save()

            reg = registration(user=usr, contact=mangerContactNo,
                            password_saved=password, storeID=Store_newID,profile_pic=managerProfileImage, entry_type=accessEntryOfData)
            reg.save()

            storeDetail = store_detail(storeID=Store_newID, store_name=storeName, store_location=storeLocation,
                                    store_town=storeCity, store_city=storeCity, store_state=storState, store_category=storCategory,
                        store_subcategory = storSubCategory) 
            storeDetail.save()
            store_managerData = store_manager(store = storeDetail ,manager_name = mangerName , manager_contact =mangerContactNo, 
                    user_unique_id =userUinqueID, manager_email =email,manager_image=managerProfileImage, gender =managerGender, manager_password = hashed_pwd,entry_type =accessEntryOfData).save()

            # store_supervisorData = Store_supervisor(supervisor_name = supervisorName , supervisor_contact =supervisorContactNO, 
            #         supervisor_email =supervisorEmail, supervisor_gender =supervisorGender).save()

        
            return redirect('store_list')
        else:
            return redirect('store_list')
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')
    # except:
        return render(request, '404.html')

@staff_member_required(login_url="/signup")
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment'
    'filename=CustomerData'+str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Contact', 'Email', 'Gender', 'DOB'])
    customerData = CustomerData.objects.all()
    for customer in customerData:
        writer.writerow([customer.name, customer.contact,
                         customer.email, customer.gender, customer.DOB])

    return response


@staff_member_required(login_url="/signup")
def delete_category(request, id):
    if request.method == 'POST':
        del_data = category.objects.get(pk=id)
        del_data.delete()
        return HttpResponseRedirect('/product_category_render')


@staff_member_required(login_url="/signup")
def edit_category(request):
    if request.method == 'GET':
        id = request.GET['id']
        storeCategory = category.objects.get(pk=id)
        cat_data = {}
        cat_data[storeCategory.category] = storeCategory.sub_category
        return JsonResponse({'cat_data': cat_data})
    else:
        return JsonResponse({'msg': 'Fail'})
# ---------------------------------------------------------------------------------------------------------------------------------

@staff_member_required(login_url="/signup")
def tier_managememt_collective(request):
    return render(request, 'admin_template/tier-managememt-collective.html')

@staff_member_required(login_url="/signup")
def AddTiersRule(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            storeName = request.POST['storeName']
            tierFromAMT = request.POST['tierFromAMT']
            tierToAMT = request.POST['tierToAMT']
            tierTimePeriod = request.POST['tierTimePeriod']
            tierRule = request.POST['tierRule']
            storeModel = store_detail.objects.get(store_name=storeName.strip())
            tier_individual(tierType='Individual', tierRuleNo=tierRule, store_ID=storeModel.storeID.strip(), shop_start_amt=tierFromAMT,
                            shop_end_amt=tierToAMT, time_period=tierTimePeriod).save()
            latestID = tier_individual.objects.latest('id')
            latestid = latestID.id
            return HttpResponse(json.dumps(latestid), content_type="application/json")
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')

@staff_member_required(login_url="/signup")
def CollectiveAddTiersRule(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            tierFromAMT = request.POST['tierFromAMT']
            tierToAMT = request.POST['tierToAMT']
            tierTimePeriod = request.POST['tierTimePeriod']
            tierRule = request.POST['tierRule']
            tier_collective(tierType='Collective', tierRuleNo=tierRule,shop_start_amt=tierFromAMT,
                            shop_end_amt=tierToAMT, time_period=tierTimePeriod).save()
            latestID = tier_collective.objects.latest('id')
            latestid = latestID.id
            return HttpResponse(json.dumps(latestid), content_type="application/json")
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')

@staff_member_required(login_url="/signup")
def CheckExixtingTierRule(request):
    if request.method == 'GET':
        storeName = request.GET['storeName']
        storeModel = store_detail.objects.get(store_name=storeName.strip())
        tierData = tier_individual.objects.filter(store_ID=storeModel.storeID)
        tierDataJson = []
        for i in tierData:
            tierDataJson.append([
                storeName,
                i.shop_start_amt,
                i.shop_end_amt,
                i.time_period,
                i.tierRuleNo,
                i.id
            ])
        return HttpResponse(json.dumps(tierDataJson), content_type="application/json")


@staff_member_required(login_url="/signup")
def CheckExixtingTierRule_collective(request):
    if request.method == 'GET':
        tierData = tier_collective.objects.all()
        tierRuleList = []
        tierRuleDict = {}
        for i in tierData:
            tierRuleDict["tierType"] = i.tierType
            tierRuleDict["tierRuleNo"] = i.tierRuleNo
            tierRuleDict["shop_start_amt"] = i.shop_start_amt
            tierRuleDict["shop_end_amt"] = i.shop_end_amt
            tierRuleDict["time_period"] = i.time_period
            tierRuleDict["id"] = i.id
            tierRuleList.append(tierRuleDict)
            tierRuleDict = {}
    return HttpResponse(json.dumps(tierRuleList), content_type="application/json")
    
@staff_member_required(login_url="/signup")
def deleteTier(request):
    if request.method == 'GET':
        flag = False
        try:
            id = request.GET['tierID']
            ID = int(id)
            a = tier_individual.objects.get(id=ID).delete()
            flag = True
            return HttpResponse(flag)
        except:
            flag = False
            return HttpResponse(flag)


@staff_member_required(login_url="/signup")
def collective_deleteTier(request):
    if request.method == 'GET':
        flag = False
        try:
            id = request.GET['tierID']
            ID = int(id)
            a = tier_collective.objects.get(id=ID).delete()
            flag = True
            return HttpResponse(flag)
        except:
            flag = False
            return HttpResponse(flag)
# ---------------------------------------------------------------------------------------------------------------------------------


def adminCustomerGraph1(request):
    if request.method == 'GET':
        chart1_data = request.session.get('admin_cust_list')
        return HttpResponse(json.dumps(chart1_data), content_type="application/json")


def adminCustomerGraph2(request):
    if request.method == 'GET':
        chart2_data = request.session.get('admin_avg_list')
        return HttpResponse(json.dumps(chart2_data), content_type="application/json")

def email(request):
    return render(request,'admin_template/send-mail.html')


def sms(request):
    return render(request, 'admin_template/send-sms.html')


def preview_mail(request):
    return render(request, 'admin_template/preview-mail.html')


def preview_sms(request):
    return render(request, 'admin_template/preview-sms.html')


def checkStore(request):
    try:
        flag = False
        store_name = request.GET['store_name']
        retrieved_store = store_detail.objects.filter(store_name=store_name)
        if len(retrieved_store) == 1:
            flag = True
        else:
            flag = False


        # creating JSON object

        if retrieved_store:
            return HttpResponse('true')

        else:
            return HttpResponse('false')

    except:
        return render(request, 'admin_template/stores-list.html')


def checkEmail(request):
    if request.method == 'GET':
        email = request.GET['email']
        flag = False
        validmail = store_manager.objects.filter(manager_email=email)
        if len(validmail) == 1:
            flag = True
        return HttpResponse(flag)




def checkmanagerContact(request):
    if request.method == 'GET':
        flag = False
        contact = request.GET['ManagerContact']

        contact = store_manager.objects.filter(manager_contact=contact)
        if len(contact) == 1:
            flag = True

        return HttpResponse(flag)


@staff_member_required(login_url="/signup")
def customer_detailed_info(request):
    if request.method == 'GET':
        cust_id = request.GET['id']
        singleCustomerData = CustomerData.objects.get(id=cust_id)
        allContactExistCustomers = CustomerData.objects.filter(contact = singleCustomerData.contact)
        
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
        customer_detailed_data = CustomerData.objects.filter(id=cust_id).values('storeID','name','contact','email','DOB','DOM','gender')

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
        return HttpResponse(json.dumps(cust_shop_info_list), content_type="application/json")
        

# @staff_member_required(login_url="/signup")
def outOfoRDER(request):
    return render(request,'admin_template/out.html')
    

def allCsvCustomersemailCamp(request):
    if request.method == 'GET':
        customerCsvList = []
        customers = CustomerData.objects.all().values('name','contact','email','DOB','DOM','gender','storeID')
        customerCsvList.append(['Name','Contact','Email','DOB','Gender','DOM','storeID'])
        for i in customers:
            if(i['email'] != ''):
                customerCsvList.append([i['name'],i['contact'],i['email'],i['gender'],i['DOB'],i['DOM'],i['storeID']])
        
    return HttpResponse(json.dumps(customerCsvList), content_type="application/json")

def allCsvCustomers(request):
    if request.method == 'GET':
        customerCsvList = []
        customerCsvList.append(['Name','Contact','Email','Gender','DOB','DOM','storeID'])
        customers = CustomerData.objects.all().values('name','contact','email','DOB','DOM','gender','storeID')
        for i in customers:
            customerCsvList.append([i['name'],i['contact'],i['email'],i['gender'],i['DOB'],i['DOM'],i['storeID']])
    return HttpResponse(json.dumps(customerCsvList), content_type="application/json")
# ##################################################################################################################################
# ###############################################   CAMPAIGN MODULE   ##############################################################
# ##################################################################################################################################
@staff_member_required(login_url="/signup")
def campeignNameEmail(request):
    if request.method == 'GET':
        campeignName = CampaignEmail.objects.values('campaignName')
        List = []
        for i in campeignName:
            List.append([i['campaignName']])
    return HttpResponse(json.dumps(List), content_type="application/json")

@staff_member_required(login_url="/signup")
def campeignNameSms(request):
    if request.method == 'GET':
        campeignName = CampaignSms.objects.values('campaignName')
        List = []
        for i in campeignName:
            List.append([i['campaignName']])
    return HttpResponse(json.dumps(List), content_type="application/json")


@staff_member_required(login_url="/signup")
def SendEmailToCustomer(request):
    if request.method == 'POST':
        AllEmail = request.POST.getlist('AllEmail[]')
        completeEmail = request.POST.getlist('completeEMAIL[]')
        mailSubject = request.POST.get('mailSubject')
        mail_syntax_Text = request.POST.get('EMAILText')
        # exit()
        check = CampaignEmail.objects.filter(campaignName=mailSubject.strip())
        datatuple = []
        flag = False

        for i in range(len(AllEmail)):
            if(AllEmail[i] != "NA"):
                # =====================================================================================================
                today = date.today()
                html_content = render_to_string('emailTemplates/bulkemail.html',{'customer_data_string':completeEmail[i],'date':today})
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(mailSubject,text_content,settings.DEFAULT_FROM_EMAIL,[AllEmail[i]])
                email.attach_alternative(html_content,'text/html')
                email.send()
                print('email sent...')
                # =====================================================================================================
                # datatuple.append((mailSubject,completeEmail[i],settings.DEFAULT_FROM_EMAIL,[AllEmail[i]]))
                flag = True
        # datatuple = tuple(datatuple)
        # send_mass_mail(datatuple)
        if len(check) > 0:
            check = check[0]
            sub_camp = EmailSubCampaign(CampaignName=check,allEmails=AllEmail,text=mail_syntax_Text)
            sub_camp.save()
        else:
            master_campaign = CampaignEmail(campaignName=mailSubject.strip())
            master_campaign.save()
            sub_camp = EmailSubCampaign(CampaignName=master_campaign,allEmails=AllEmail,text=mail_syntax_Text)
            sub_camp.save()

        return HttpResponse(flag)

@staff_member_required(login_url="/signup")
def SendSMSToCustomer(request):
    if request.method == 'POST':
        url = "https://www.fast2sms.com/dev/bulk"
        AllSms = request.POST.getlist('All_Mob_No[]')
        completeSms = request.POST.getlist('completeSms[]')
        smsSub = request.POST.get('smsSub')
        smsText = request.POST.get('smsText')
        
        check = CampaignSms.objects.filter(campaignName=smsSub.strip())
        flag = False
        for i in range(0,len(AllSms)):
            payload = "sender_id=FSTSMS&message=" + completeSms[i] +"&language=english&route=p&numbers=" + AllSms[i]
            headers = {
            'authorization': "QDo5cIdOBq6xG8YygsMkleWt7FAbXpjhimvZPz4J0VunCNEUf1D9H8ugEpaBMfK3FnwOhojeyZQXTWJm",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
            flag = True
            response = requests.request("POST", url, data=payload, headers=headers)
        
        if len(check) > 0:
            check = check[0]
            sub_camp = SmsSubCampaign(CampaignName=check,allsms=AllSms,text=smsText)
            sub_camp.save()
        else:
            master_campaign = CampaignSms(campaignName=smsSub)
            master_campaign.save()
            sub_camp = SmsSubCampaign(CampaignName=master_campaign,allsms=AllSms,text=smsText)
            sub_camp.save()

        return HttpResponse(flag)

@staff_member_required(login_url="/signup")
def selectEmailCampaignName(request):
    if request.method == "GET":
        campaignName = request.GET.get('campaignName')
        campaignName = campaignName.strip()
        data = CampaignEmail.objects.get(campaignName=campaignName)
        subCampData = EmailSubCampaign.objects.filter(CampaignName=data)
        List = []
        for i in subCampData:
            List.append(i.text)
    return HttpResponse(json.dumps(List), content_type="application/json")

@staff_member_required(login_url="/signup")
def selectSmsCampaignName(request):
    if request.method == "GET":
        campaignName = request.GET.get('campaignName')
        campaignName = campaignName.strip()
        data = CampaignSms.objects.get(campaignName=campaignName)
        subCampData = SmsSubCampaign.objects.filter(CampaignName=data)

        List = []
        for i in subCampData:
            List.append(i.text)
    return HttpResponse(json.dumps(List), content_type="application/json")

# ##################################################################################################################################
# ###############################################   BROADCAST & DELIVERY MODULE   ##################################################
# ##################################################################################################################################
# ##################################################   SMS BROADCAST   #############################################################
@staff_member_required(login_url="/signup")
def sms_broadcast(request):
    if request.method == 'GET':
        master_campaign = CampaignSms.objects.all()
    return render(request,'admin_template/sms-campaign.html',{'master_campaign':master_campaign})

@staff_member_required(login_url="/signup")
def campaign_mobile_no_list(request):
    return render(request,'admin_template/campaign-mobile-no-list.html')

@staff_member_required(login_url="/signup")
def campaign_mobile_no_list1(request,Year):
    master = request.session.get('masterCamp')
    masterCampaign = CampaignSms.objects.get(campaignName=master)
    subCampaign = SmsSubCampaign.objects.filter(CampaignName=masterCampaign)
    l1 = []
    for i in subCampaign:
        data = i.allsms
        x = data.strip('"][').split(', ')
        for i in x:
            a = i.strip("'")
            l1.append(a)
    return render(request,'admin_template/campaign-mobile-no-list-1.html',{'emailList':l1,'master' : master})

@staff_member_required(login_url="/signup")
def customers_list_sms(request):
    try:
        customer_data = CustomerData.objects.all().order_by('id')
        store_data = store_detail.objects.all()
        return render(request,'admin_template/customers-list-sms.html',{'Customer_data': customer_data, 'store_detail': store_data})
    except:
        return render(request, '404.html')
    return render(request,'admin_template/customers-list-sms.html')

@staff_member_required(login_url="/signup")
def create_sms_campaign(request):
    customer_data = CustomerData.objects.all().order_by('id')
    store_data = store_detail.objects.all()
    paginator = Paginator(customer_data,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_template/create-sms-campaign.html', {'page_obj': page_obj, 'Customer_data': customer_data, 'store_detail': store_data})


@staff_member_required(login_url="/signup")
def campaign_details(request,id):
    masterCamp = CampaignSms.objects.get(id=id)
    request.session['masterCamp'] = masterCamp.campaignName
    subCampaign = SmsSubCampaign.objects.filter(CampaignName=masterCamp)
    l1 = []
    for i in subCampaign:
        data = i.allsms
        x = data.strip('"][').split(', ')
        for i in x:
            a = i.strip("'")
            l1.append(a)
    total = len(l1)
    data = SmsSubCampaign.objects.all().annotate(Year=ExtractYear('time_stamp')).values('Year','CampaignName').filter(CampaignName=masterCamp).annotate(dataCount=Count('Year')).order_by('CampaignName')
    return render(request,'admin_template/campaign-detail.html',{'data' : data,'masterCamp' : masterCamp,'total' : total})


def send_sms_campaign(request):
    return render(request,'admin_template/send-email-campaign.html')

def check_sms_campaign(request):
    if request.method == 'GET':
        campData = request.GET['s']
        data = list(campData.split('Campaign'))

        filter_master = CampaignSms.objects.get(campaignName = data[0].strip())
        subCamp = SmsSubCampaign.objects.filter(CampaignName=filter_master,time_stamp__year = data[1].strip())
        List=[]
        for i in subCamp:
            List.append(i.text)
    return HttpResponse(json.dumps(List), content_type="application/json")
# ###################################################  EMAIL BROADCAST  ############################################################
@staff_member_required(login_url="/signup")
def email_broadcast(request):
    if request.method == 'GET':
        l1=[]
        master_campaign = CampaignEmail.objects.all()
        for i in master_campaign:
            subCampaign = EmailSubCampaign.objects.filter(CampaignName=i)
            for i in subCampaign:
                data = i.allEmails
                x = data.strip('"][').split(', ')
                for i in x:
                    a = i.strip("'")
                    l1.append(a)
        total = len(l1)

    return render(request,'admin_template/email-campaign.html',{'master_campaign':master_campaign,'total' : total})

@staff_member_required(login_url="/signup")
def campaign_emails_list(request):
    return render(request,'admin_template/campaign-emails-list.html')

@staff_member_required(login_url="/signup")
def campaign_mobile_no_list2(request,Year):
    master = request.session.get('masterCamp')
    masterCampaign = CampaignEmail.objects.get(campaignName=master)
    subCampaign = EmailSubCampaign.objects.filter(CampaignName=masterCampaign)
    yearly_data = EmailSubCampaign.objects.filter(time_stamp__year = Year,CampaignName=masterCampaign)
    l1 = []
    for i in yearly_data:
        data = i.allEmails
        x = data.strip('"][').split(', ')
        for i in x:
            a = i.strip("'")
            l1.append(a)
    total = len(l1)
    return render(request,'admin_template/campaign-mobile-no-list-2.html',{'emailList':l1,'master' : master})

@staff_member_required(login_url="/signup")
def customers_list_email(request):
    try:
        customer_data = CustomerData.objects.all().order_by('id')
        store_data = store_detail.objects.all()
        return render(request,'admin_template/customers-list-email.html',{'Customer_data': customer_data, 'store_detail': store_data})

    except:
        return render(request, '404.html')

@staff_member_required(login_url="/signup")
def create_email_campaign(request):
    customer_data = CustomerData.objects.all().order_by('id')
    store_data = store_detail.objects.all()
    paginator = Paginator(customer_data,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'admin_template/create-email-campaign.html',{'page_obj': page_obj, 'Customer_data': customer_data,'store_detail': store_data})


@staff_member_required(login_url="/signup")
def campaignDetailEmail(request,id):
    # All Customer With Pagination
    customer_data = CustomerData.objects.all().order_by('id')
    store_data = store_detail.objects.all()
    paginator = Paginator(customer_data,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    masterCamp = CampaignEmail.objects.get(id=id)
    request.session['masterCamp'] = masterCamp.campaignName
    subCampaign = EmailSubCampaign.objects.filter(CampaignName=masterCamp)
    l1 = []
    for i in subCampaign:
        data = i.allEmails
        x = data.strip('"][').split(', ')
        for i in x:
            a = i.strip("'")
            l1.append(a)
    total = len(l1)
    data = EmailSubCampaign.objects.all().annotate(Year=ExtractYear('time_stamp')).values('Year','CampaignName').filter(CampaignName=masterCamp).annotate(dataCount=Count('Year')).order_by('CampaignName')
    store_data = store_detail.objects.all()
    return render(request,'admin_template/campaignDetailEmail.html',{'page_obj': page_obj, 'Customer_data': customer_data, 'store_detail': store_data,'data' : data,'masterCamp' : masterCamp,'total' : total, 'store_detail': store_data})



@staff_member_required(login_url="/signup")
def campaign_details2(request,id):
    masterCamp = CampaignEmail.objects.get(id=id)
    request.session['masterCamp'] = masterCamp.campaignName
    subCampaign = EmailSubCampaign.objects.filter(CampaignName=masterCamp)
    l1 = []
    for i in subCampaign:
        data = i.allEmails
        x = data.strip('"][').split(', ')
        for i in x:
            a = i.strip("'")
            l1.append(a)
    total = len(l1)
    data = EmailSubCampaign.objects.all().annotate(Year=ExtractYear('time_stamp')).values('Year','CampaignName').filter(CampaignName=masterCamp).annotate(dataCount=Count('Year')).order_by('CampaignName')
    customer_data = CustomerData.objects.all().order_by('id')
    store_data = store_detail.objects.all()
    return render(request,'admin_template/campaign-detail2.html',{'data' : data,'masterCamp' : masterCamp,'total' : total,'Customer_data': customer_data, 'store_detail': store_data})



def send_email_campaign(request):
    return render(request,'admin_template/send-email-campaign.html')

def check_email_campaign(request):
    if request.method == 'GET':
        campData = request.GET['s']
        data = re.split('(Campaign)', campData)
        filter_master = CampaignEmail.objects.get(campaignName = data[0].strip())
        subCamp = EmailSubCampaign.objects.filter(CampaignName=filter_master,time_stamp__year = data[2])
        List=[]
        for i in subCamp:
            List.append(i.text)
    return HttpResponse(json.dumps(List), content_type="application/json")




@staff_member_required(login_url="/signup")
def campaignDetailSMS(request,id):
    # All Customer With Pagination
    customer_data = CustomerData.objects.all().order_by('id')
    store_data = store_detail.objects.all()
    paginator = Paginator(customer_data,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # 
    masterCamp = CampaignSms.objects.get(id=id)
    request.session['masterCamp'] = masterCamp.campaignName
    subCampaign = SmsSubCampaign.objects.filter(CampaignName=masterCamp)
    l1 = []
    for i in subCampaign:
        data = i.allsms
        x = data.strip('"][').split(', ')
        for i in x:
            a = i.strip("'")
            l1.append(a)
    total = len(l1)
    data = SmsSubCampaign.objects.all().annotate(Year=ExtractYear('time_stamp')).values('Year','CampaignName').filter(CampaignName=masterCamp).annotate(dataCount=Count('Year')).order_by('CampaignName')

    # customer_data = CustomerData.objects.all().order_by('id')
    store_data = store_detail.objects.all()
    return render(request,'admin_template/campaignDetailSMS.html',{'page_obj': page_obj, 'Customer_data': customer_data, 'store_detail': store_data,'data' : data,'masterCamp' : masterCamp,'total' : total, 'store_detail': store_data})


def checkCampaign(request):
    flag = False
    if request.method =='GET':
        camp_name = request.POST['campaignName']
    return HttpResponse(flag)

# ##############################################################################################################################
# ###########################   BROADCAST DATE FILTER VIEW   ###################################################################
# ##############################################################################################################################
# ---------------------------------DATETIME to JSON CONVERTER-------------------------------------------------------------------
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
# ------------------------------------------------------------------------------------------------------------------------------
def filterSmSDate(request):
    if request.method == 'GET':
        sDate = request.GET.get('start_date')
        eDate = request.GET.get('end_date')
        filtered_data = CampaignSms.objects.filter(time_stamp__range = [sDate,eDate])
        List=[]
        sms_dict = {}
        for i in filtered_data:
            sms_dict['id'] = i.id
            sms_dict['campName'] = i.campaignName
            sms_dict['time_stamp'] = i.time_stamp
            List.append(sms_dict)
            sms_dict = {}        
    return HttpResponse(json.dumps(List, default = myconverter),content_type="application/json")


def filterEmailDate(request):
    if request.method == 'GET':
        sDate = request.GET.get('start_date')
        eDate = request.GET.get('end_date')
        filtered_data = CampaignEmail.objects.filter(time_stamp__range = [sDate,eDate])
        List=[]
        email_dict = {}
        for i in filtered_data:
            email_dict['id'] = i.id
            email_dict['campName'] = i.campaignName
            email_dict['time_stamp'] = i.time_stamp
            List.append(email_dict)
            email_dict = {}
    return HttpResponse(json.dumps(List, default = myconverter),content_type="application/json")

# ===============================================================================
# Load more customers in customer management scrren via Load_More button
def load_more(request):
    if request.method == 'POST':
        offset = int(request.POST['offset'])
        limit = 10
        customersData = CustomerData.objects.all()[offset:offset+limit]
        totalData = CustomerData.objects.count()
        customer_json = serializers.serialize('json',customersData)
        # --------------------------------------------------------------------------------------
        return JsonResponse(data={
            'customers' :customer_json,
            'totalResult' :totalData
        })
# ======================================================================================================
# Create New Campaign Name
def NewCampaignNameSMS(request):
    if request.method == 'GET':
        emailCampaignName = request.GET.get('name')
        filtered_data = CampaignSms.objects.filter(campaignName = emailCampaignName.strip())
        flag = False
        if len(filtered_data) != 0:
            flag = True
        else:
            flag = False
        return HttpResponse(json.dumps(flag),content_type="application/json")

# Create New Campaign Name
def NewCampaignNameEMAIL(request):
    if request.method == 'GET':
        emailCampaignName = request.GET.get('name')
        filtered_data = CampaignEmail.objects.filter(campaignName = emailCampaignName.strip())
        flag = False
        if len(filtered_data) != 0:
            flag = True
        else:
            flag = False
        return HttpResponse(json.dumps(flag),content_type="application/json")

# ##############################################################################################################################
# ##################################   EMAIL AND SMS SCHEDULING VIEWS   ########################################################
# ##############################################################################################################################
def findDay(date): 
    born = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    return (calendar.day_name[born]) 

def sudo_placement():
    sendEmail = scheduleEmailList.objects.all()
    emailList = ''
    emailText = ''
    for i in sendEmail:
        emailList = i.emailList
        emailText = i.emailText
    # ==================================================================='
    emailData = emailList.replace('[',"")
    x = emailData.replace(']',"")
    y = x.replace("'","")
    mailList = y.split('|')
    emails = []
    for i in range(len(mailList)):
        emails.append(mailList[i].split(","))
    emails.pop()
    for i in emails:
        i.pop()
    messageData = emailText.replace('[',"")
    x = messageData.replace(']',"")
    y = x.replace("'","")
    message = y.split('|')
    emailMessages = []
    for i in range(len(message)):
        emailMessages.append(message[i].split(","))
    emailMessages.pop()
    for i in emailMessages:
        i.pop()
    # ===============================     SEND SCHEDULED EMAILS    =====================================================
    datatuple = []
    for i in range(len(emails)):
        dataLength = len(emails[i])
        if (dataLength == 6 and len(emailMessages[i]) == 1):
            # current = emails[i][3]
            datatuple.append(('mailSubject',emailMessages[i][0],settings.DEFAULT_FROM_EMAIL,[emails[i][3]]))

        elif(dataLength == 5 and len(emailMessages[i]) == 1):
            # current = emails[i][4]
            datatuple.append(('mailSubject',emailMessages[i][0],settings.DEFAULT_FROM_EMAIL,[emails[i][2]]))
        
        elif (dataLength == 6 and len(emailMessages[i]) > 1):
            current = ''
            for j in emailMessages[i]:
                current += j
            datatuple.append(('mailSubject',current,settings.DEFAULT_FROM_EMAIL,[emails[i][3]]))

        elif(dataLength == 5 and len(emailMessages[i]) > 1):
            current = ''
            for j in emailMessages[i]:
                current += j
            datatuple.append(('mailSubject',current,settings.DEFAULT_FROM_EMAIL,[emails[i][2]]))
    # ----------------------------------------------------------------------------------------------------------------
    datatuple = tuple(datatuple)
    send_mass_mail(datatuple)
    # ================================================================================================================
    scheduleEmailList.objects.all().delete()

def schedulTask(dater,timer):
    timer = timer
    schedulingDay = findDay(dater)
    if schedulingDay == 'Sunday': 
        schedule.every().sunday.at(timer).do(sudo_placement)
    elif schedulingDay == 'Monday': 
        schedule.every().monday.at(timer).do(sudo_placement)
    elif schedulingDay == 'Tuesday': 
        schedule.every().tuesday.at(timer).do(sudo_placement)
    elif schedulingDay == 'Wednesday': 
        schedule.every().wednesday.at(timer).do(sudo_placement)
    elif schedulingDay == 'Thursday': 
        schedule.every().thursday.at(timer).do(sudo_placement)
    elif schedulingDay == 'Friday': 
        schedule.every().friday.at(timer).do(sudo_placement)
    elif schedulingDay == 'Saturday': 
        schedule.every().saturday.at(timer).do(sudo_placement)

    while True:
        schedule.run_pending()
        time.sleep(1)

@staff_member_required(login_url="/signup")
def formatScheduleEmailText(request):
    # try:
    if request.method == 'GET':
        completeEmail = request.GET.getlist('completeEmail[]')
        Emaillist_data = request.GET.getlist('list_data[]')
        flag = False
        completeMessageList = []
        for i in range(len(completeEmail)):
            completeMessageList.append(completeEmail[i])
            completeMessageList.append('|')

        EmailList = []
        for i in range(len(Emaillist_data)):
            EmailList.append(Emaillist_data[i])
            EmailList.append('|')


        data = scheduleEmailList.objects.all()
        if(len(data) > 0):
            scheduleEmailList.objects.all().delete()
            scheduleEmailList(emailList = EmailList,emailText = completeMessageList).save()
            flag = True
        else:
            scheduleEmailList(emailList = EmailList,emailText = completeMessageList).save()
            flag = True
        return HttpResponse(flag)
    # except:
    #     flag = False
    #     return HttpResponse(flag)

def scheduleCustEmail(request):
    if request.method == 'POST':
        scheduleDate = request.POST['date']
        schedule_time = request.POST['time']

        #  formating date
        data = scheduleDate.split('/')
        scheduleformatedDate = data[1] + " " + data[0] + " " + data[2]
        #  formatting time
        timedata = schedule_time.split(' ')
        timeformat = timedata[0].split(':')
        
        if(timedata[1] == 'PM'):
            if(len(timeformat[0]) == 1):
                if (timeformat[0] == '1'):
                    timeformat[0] = '13'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '2'):
                    timeformat[0] = '14'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '3'):
                    timeformat[0] = '15'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '4'):
                    timeformat[0] = '16'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '5'):
                    timeformat[0] = '17'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '6'):
                    timeformat[0] = '18'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '7'):
                    timeformat[0] = '19'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '8'):
                    timeformat[0] = '20'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '9'):
                    timeformat[0] = '21'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)
            else:
                if (timeformat[0] == '10'):
                    timeformat[0] = '22'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)
                elif (timeformat[0] == '11'):
                    timeformat[0] = '23'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)
                elif (timeformat[0] == '12'):
                    timeformat[0] = '24'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTask(scheduleformatedDate,timesechdule)
        else:
            if(len(timeformat[0]) == 1):
                timeformat[0] = "0"+timeformat[0]
                timesechdule = timeformat[0]+':'+timeformat[1]
                schedulTask(scheduleformatedDate,timesechdule)
            else:
                timesechdule = timeformat[0]+':'+timeformat[1]
                schedulTask(scheduleformatedDate,timesechdule)
        return HttpResponse('HEllooo')

# ##############################################################################################################
# ##############################################################################################################
# ##############################################################################################################
def findDays(date): 
    born = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    return (calendar.day_name[born]) 

def sudo_placements():
    # =========================================================================================================
    sendEmail = scheduleSMSList.objects.all()
    smsList = ''
    smsText = ''
    for i in sendEmail:
        smsList = i.emailList
        smsText = i.emailText
    # ==================================================================='
    SmsData = smsList.replace('[',"")
    x = SmsData.replace(']',"")
    y = x.replace("'","")
    mailList = y.split('|')
    emails = []
    for i in range(len(mailList)):
        emails.append(mailList[i].split(","))
    emails.pop()
    for i in emails:
        i.pop()
    messageData = smsText.replace('[',"")
    x = messageData.replace(']',"")
    y = x.replace("'","")
    message = y.split('|')
    emailMessages = []
    for i in range(len(message)):
        emailMessages.append(message[i].split(","))
    emailMessages.pop()
    for i in emailMessages:
        i.pop()
    # ===============================     SEND SCHEDULED EMAILS    =====================================================
    try:
        url = "https://www.fast2sms.com/dev/bulk"
        for i in range(len(emails)):
            dataLength = len(emails[i])
            if (dataLength == 6 and len(emailMessages[i]) == 1):
                # current = emails[i][3]
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message=" + str(emailMessages[i][0]) +"&language=english&route=p&numbers=" + str(emails[i][1])
                headers = {
                'authorization': "QDo5cIdOBq6xG8YygsMkleWt7FAbXpjhimvZPz4J0VunCNEUf1D9H8ugEpaBMfK3FnwOhojeyZQXTWJm",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
                response = requests.request("POST", url, data=payload, headers=headers)


            elif(dataLength == 5 and len(emailMessages[i]) == 1):
                # current = emails[i][4]
                url = "https://www.fast2sms.com/dev/bulk"
                payload = "sender_id=FSTSMS&message=" + str(emailMessages[i][0]) +"&language=english&route=p&numbers=" + str(emails[i][1])
                headers = {
                'authorization': "QDo5cIdOBq6xG8YygsMkleWt7FAbXpjhimvZPz4J0VunCNEUf1D9H8ugEpaBMfK3FnwOhojeyZQXTWJm",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
                }
                response = requests.request("POST", url, data=payload, headers=headers)

            
            elif (dataLength == 6 and len(emailMessages[i]) > 1):
                current = ''
                for j in emailMessages[i]:
                    current += j
                    url = "https://www.fast2sms.com/dev/bulk"
                    payload = "sender_id=FSTSMS&message=" + current +"&language=english&route=p&numbers=" + emails[i][2]
                    headers = {
                    'authorization': "QDo5cIdOBq6xG8YygsMkleWt7FAbXpjhimvZPz4J0VunCNEUf1D9H8ugEpaBMfK3FnwOhojeyZQXTWJm",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache",
                    }
                    response = requests.request("POST", url, data=payload, headers=headers)


            elif(dataLength == 5 and len(emailMessages[i]) > 1):
                current = ''
                for j in emailMessages[i]:
                    current += j
                    url = "https://www.fast2sms.com/dev/bulk"
                    payload = "sender_id=FSTSMS&message=" + current +"&language=english&route=p&numbers=" + emails[i][2]
                    headers = {
                    'authorization': "QDo5cIdOBq6xG8YygsMkleWt7FAbXpjhimvZPz4J0VunCNEUf1D9H8ugEpaBMfK3FnwOhojeyZQXTWJm",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache",
                    }
                    response = requests.request("POST", url, data=payload, headers=headers)

        # ================================================================================================================
        scheduleSMSList.objects.all().delete()
    except:
        #  exit() 
        print(';error!') 

def schedulTasks(dater,timer):
    timer = timer
    schedulingDay = findDays(dater)
    if schedulingDay == 'Sunday': 
        schedule.every().sunday.at(timer).do(sudo_placements)
    elif schedulingDay == 'Monday': 
        schedule.every().monday.at(timer).do(sudo_placements)
    elif schedulingDay == 'Tuesday': 
        schedule.every().tuesday.at(timer).do(sudo_placements)
    elif schedulingDay == 'Wednesday': 
        schedule.every().wednesday.at(timer).do(sudo_placements)
    elif schedulingDay == 'Thursday': 
        schedule.every().thursday.at(timer).do(sudo_placements)
    elif schedulingDay == 'Friday': 
        schedule.every().friday.at(timer).do(sudo_placements)
    elif schedulingDay == 'Saturday': 
        schedule.every().saturday.at(timer).do(sudo_placements)

    while True:
        schedule.run_pending()
        time.sleep(1)

@staff_member_required(login_url="/signup")
def formatScheduleSMSText(request):
    # try:
    if request.method == 'GET':
        completeSMS = request.GET.getlist('completeSMS[]')
        Emaillist_data = request.GET.getlist('list_data[]')
        flag = False
        completeMessageList = []
        for i in range(len(completeSMS)):
            completeMessageList.append(completeSMS[i])
            completeMessageList.append('|')

        EmailList = []
        for i in range(len(Emaillist_data)):
            EmailList.append(Emaillist_data[i])
            EmailList.append('|')
        data = scheduleSMSList.objects.all()
        if(len(data) > 0):
            scheduleSMSList.objects.all().delete()
            scheduleSMSList(emailList = EmailList,emailText = completeMessageList).save()
            flag = True
        else:
            scheduleSMSList(emailList = EmailList,emailText = completeMessageList).save()
            flag = True
        return HttpResponse(flag)
    # except:
    #     flag = False
    #     return HttpResponse(flag)

def scheduleCustSMS(request):
    if request.method == 'POST':
        scheduleDate = request.POST['date']
        schedule_time = request.POST['time']

        #  formating date
        data = scheduleDate.split('/')
        scheduleformatedDate = data[1] + " " + data[0] + " " + data[2]
        #  formatting time
        timedata = schedule_time.split(' ')
        timeformat = timedata[0].split(':')
        
        if(timedata[1] == 'PM'):
            if(len(timeformat[0]) == 1):
                if (timeformat[0] == '1'):
                    timeformat[0] = '13'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '2'):
                    timeformat[0] = '14'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '3'):
                    timeformat[0] = '15'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '4'):
                    timeformat[0] = '16'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '5'):
                    timeformat[0] = '17'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '6'):
                    timeformat[0] = '18'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '7'):
                    timeformat[0] = '19'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '8'):
                    timeformat[0] = '20'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)

                elif (timeformat[0] == '9'):
                    timeformat[0] = '21'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)
            else:
                if (timeformat[0] == '10'):
                    timeformat[0] = '22'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)
                elif (timeformat[0] == '11'):
                    timeformat[0] = '23'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)
                elif (timeformat[0] == '12'):
                    timeformat[0] = '24'
                    timesechdule = timeformat[0]+':'+timeformat[1]
                    schedulTasks(scheduleformatedDate,timesechdule)
        else:
            if(len(timeformat[0]) == 1):
                timeformat[0] = "0"+timeformat[0]
                timesechdule = timeformat[0]+':'+timeformat[1]
                schedulTasks(scheduleformatedDate,timesechdule)
            else:
                timesechdule = timeformat[0]+':'+timeformat[1]
                schedulTasks(scheduleformatedDate,timesechdule)
        return HttpResponse('HEllooo')


# ================================================================================================================
# ==============================================      ONBOARD FILTER      ========================================
# ================================================================================================================
# def onboardFilter(request):
#     return HttpResponse('HEllooo')
# ================================================================================================================
def ajaxSearchObj(requests):
    if requests.method == 'GET':
        searchData = requests.GET['searchString']
        print(searchData)
        responseData = CustomerData.objects.filter(contact__startswith = searchData)
        responseDataList = []
        responseID = []
        responseName = []
        responseContact = []
        responseEmail = []
        responseGender = []
        responseDob = []
        responseDom = []


        responseDataDict = {}
        for i in range(len(responseData)):
            responseID.append(responseData[i].id)
            responseName.append(responseData[i].name)
            responseContact.append(responseData[i].contact)
            responseEmail.append(responseData[i].email)
            responseGender.append(responseData[i].gender)
            responseDob.append(responseData[i].DOB)
            responseDom.append(responseData[i].DOM)

        responseDataDict['responseID'] = responseID
        responseDataDict['responseName'] = responseName
        responseDataDict['responseContact'] = responseContact
        responseDataDict['responseEmail'] = responseEmail
        responseDataDict['responseGender'] = responseGender
        responseDataDict['responseDob'] = responseDob
        responseDataDict['responseDom'] = responseDom

        print(responseDataDict)
        responseDataList.append(responseDataDict)
        responseDataDict={}



        return HttpResponse(json.dumps(responseDataList),content_type="application/json")

# ==============================================================================================================================================
def ssder(request):
    if request.method == 'GET':
        today = date.today()
        currentDAte = today.strftime("%d/%m/%Y")
        store_supervisor_model_Data = supervisorDetails.objects.all()

        return render(request,'admin_template/ssder.html',{'currentDAte':currentDAte,'store_supervisor_model_Data':store_supervisor_model_Data})
    elif request.method == 'POST':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        ct = date.today()
        start_date = datetime.date(ct.year, ct.month, ct.day) 
        #start_date = datetime.date(2021, 3, 5) 
        font_style = xlwt.XFStyle()
        dateFrmt = start_date.strftime("%d %b %Y")
        ws.write(0, 1, str(dateFrmt), font_style)
        ws.write(0, 3, 'Store Daily Data Entry Report', font_style)
        # Sheet header, first row
        row_num = 2

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['S.NO', 'STORE-ID', 'MANAGER NAME', 'MANAGER CONTACT', 'STORE NAME', 'TOTAL NO. OF ENTRIES','TOTAL NO. OF NEW ENTRIES','TOTAL NO. OF OLD ENTRIES','TOTAL NO. OF Null Entries','EFFICIENCY %']
        # COLUMN VOUNT = 6
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        # -------------------------------------------------------------------------------------------------
        #                                     MODEL FILTERED DATA
        # -------------------------------------------------------------------------------------------------

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


        store_manager_objects = store_manager.objects.all()
        for i in range(len(store_manager_objects)):
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            storeID_list.append(store_manager_objects[i].store.storeID)
            storeName_list.append(store_manager_objects[i].store.store_name)
            managerName_list.append(store_manager_objects[i].manager_name)
            managerContact_list.append(store_manager_objects[i].manager_contact) 
            totalEntries.append(len(CustomerShopData.objects.filter(time_stamp__gt=start_date,storeID=store_manager_objects[i].store.storeID)))
            # -------------------------------------------------------------------------------------------------------------------------------------------------
            data = CustomerShopData.objects.filter(time_stamp__gte=start_date,storeID=store_manager_objects[i].store.storeID)
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
        # exit()
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
        to_mail = ['rk468335@gmail.com']
        #to_mail = ['manoj@theabacusindia.com','sunit@theabacusindia.com','siddhant.ratna@yahoo.com','rk468335@gmail.com']
        mail = EmailMessage(f"Store Data Daily Entry Report", f'ABACUS PLATINUM CLUB\n----------------------------------------\nDear admin your report for Date : {d1} is prepared in Xls and CSV file format.', settings.DEFAULT_FROM_EMAIL,to_mail)
        mail.attach(excelFile.strip(), response.getvalue(), 'text/xls')
        mail.attach(csvfile.strip(), response.getvalue(), 'text/csv')
        mail.send()
        # print('email sent!')
        return redirect('ssder')

# ===========================================================================================================================
def storeAjaxSearch(request):
    if request.method == 'GET':
        searchStr = request.GET['searchString']
        store_search_objects = store_detail.objects.filter(storeID__icontains = searchStr)|store_detail.objects.filter(store_name__icontains = searchStr)
        data = store_search_objects.values()

        return JsonResponse(list(data),safe=False)



@staff_member_required(login_url="/signup")
def apiKeysManagement(request):
    apiKeyData = ApiKey.objects.all()
    print('apiKeyData >> ',apiKeyData)
    return render(request,'admin_template/apikeys.html',{'apiKeyData':apiKeyData})


@staff_member_required(login_url="/signup")
def delete_api_key(request, id):
    if request.method == 'POST':
        del_data = ApiKey.objects.get(pk=id)
        del_data.delete()
        return HttpResponseRedirect('/apiKeysManagement')


import string
import random

@staff_member_required(login_url="/signup")
def generate_api_key(request):
    if request.method == 'POST':
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 30))
        data = ApiKey(Key = res.strip()).save()
        print('data ssaved successfully!')
        return HttpResponseRedirect('/apiKeysManagement')



@staff_member_required(login_url="/signup")
def create_store_supervisor(request):
    if request.method == 'GET':
        store_data = store_detail.objects.all()
        print('store data >> ',store_data)
        return render(request,'admin_template/create-supervisor.html',{'store_detail': store_data})

    if request.method == 'POST':
        supervisorProfileImage = request.FILES.get('supervisorProfileImage')
        supervisorName = request.POST['supervisorName'].strip()
        supervisorContactNo = request.POST['supervisorContactNo'].strip()
        supervisorGender = request.POST.get('supervisorGender')
        if supervisorGender == None:
            supervisorGender = 'NA'
        supervisorEmail = request.POST.get('supervisorEmail')
        # supervisorAddress = request.POST['supervisorAddress'].strip()
        # supervisorCountry = request.POST['supervisorCountry'].strip()
        # supervisorState = request.POST['supervisorState'].strip()
        # supervisorPincode = request.POST['supervisorPincode'].strip()
        supervisorPassword = request.POST['supervisorPassword'].strip()
        storList = request.POST.getlist('StoreIDS')

        # ===================================================================================================
        print('supervisorProfileImage >>>> ',supervisorProfileImage)
        print('supervisorName >>>> ',supervisorName)
        print('supervisorContactNo >>>> ',supervisorContactNo)
        print('supervisorGender >>>> ',supervisorGender)
        print('supervisorEmail >>>> ',supervisorEmail)
        # print('supervisorAddress >>>> ',supervisorAddress)
        # print('supervisorCountry >>>> ',supervisorCountry)
        # print('supervisorState >>>> ',supervisorState)
        # print('supervisorPincode >>>> ',supervisorPincode)
        print('supervisorPassword >>>> ',supervisorPassword)
        print('storList >>>> ',storList)
        store_data = store_detail.objects.all()
        try:
            # ===================================================================================================
            # =====================  STORE SUPERVISOR INFO TO USER MODEL  =======================================
            usr = User.objects.create_user(supervisorEmail, supervisorEmail, supervisorPassword,is_staff=True)
            usr.first_name = supervisorName
            usr.save()
            # ===================================================================================================
            # =================  STORE SUPERVISOR INFO TO REGISTRATION MODEL  ===================================
            reg = registration(user=usr, contact=supervisorContactNo,storeID=supervisorContactNo,password_saved=supervisorPassword,profile_pic=supervisorProfileImage, entry_type='NA')
            reg.save()
            # ===================================================================================================
            # ============================  STORE SUPERVISOR INFO   =============================================
            supervisorDetail = supervisorDetails(supervisor_image=supervisorProfileImage, supervisor_name=supervisorName,supervisor_contact=supervisorContactNo,
                                    supervisor_unique_id=supervisorContactNo,supervisor_email=supervisorEmail,gender=supervisorGender, supervisor_password=supervisorPassword,store_array=storList) 
            supervisorDetail.save()
            print('all data saved successfully')
            # ===================================================================================================
            # ===================================================================================================
            return render(request,'admin_template/create-supervisor.html',{'success_msg': 'Supervisor Created Successfully.','store_detail': store_data})
        except:
            return render(request,'admin_template/create-supervisor.html',{'error_msg': 'An error Occured. Try again!.','store_detail': store_data})



@staff_member_required(login_url="/signup")
def edit_supervisor(request,id):
    if request.method == 'GET':
        data = supervisorDetails.objects.get(id=id)
        store_data = store_detail.objects.all()
        return render(request,'admin_template/edit-supervisor.html',{'data':data,'store_detail':store_data})

    else:
        # -----------------------------------------------------------------------------------
        supervisorProfileImage = request.FILES.get('supervisorProfileImage')
        supervisor_obj = supervisorDetails.objects.get(id=id)
        img_data = supervisor_obj.supervisor_image
        
        if(supervisorProfileImage == None):
            supervisorProfileImage = img_data

        supervisor_Name = request.POST['supervisor_Name'].strip()
        supervisor_ContactNo = request.POST['supervisor_ContactNo'].strip()
        supervisorEmail = request.POST.get('supervisorEmail')
        supervisorOldEmail = request.POST.get('supervisorOldEmail')

        supervisorGender = request.POST.get('supervisorGender')
        newpassword = request.POST.get('supervisorConfirmPass').strip()
        # -----------------------------------------------------------------------------------
        print('supervisorProfileImage >> ',supervisorProfileImage)
        print('supervisor_Name >> ',supervisor_Name)
        print('supervisor_ContactNo >> ',supervisor_ContactNo)
        print('supervisorEmail >> ',supervisorEmail)
        print('supervisorGender >> ',supervisorGender)
        print('newpassword >> ',newpassword)
        # -----------------------------------------------------------------------------------
        message = ''
        error_msg = ''
        # try:
        usr = User.objects.get(email=supervisorOldEmail)
        usr.first_name = supervisor_Name
        usr.email = supervisorEmail
        usr.username = supervisorEmail
        if newpassword != "":
            usr.set_password(newpassword)
        usr.save()

        reg_obj = registration.objects.get(user = usr)
        reg_obj.user = usr
        reg_obj.contact = supervisor_ContactNo
        reg_obj.profile_pic = supervisorProfileImage
        if newpassword != "":
            reg_obj.password_saved = newpassword
        reg_obj.save()

        supervisor_obj = supervisorDetails.objects.get(id=id)
        supervisor = supervisor_obj
        supervisor.supervisor_name = supervisor_Name
        supervisor.supervisor_contact =supervisor_ContactNo
        supervisor.supervisor_image =supervisorProfileImage
        supervisor.user_unique_id = supervisor_ContactNo
        supervisor.supervisor_email =supervisorEmail
        supervisor.gender =supervisorGender
        supervisor.save()
        message = 'Supervisor Updated Successfully'
        # except:
        #     error_msg = 'Updation Failed. Try Again!'

        # -----------------------------------------------------------------------------------
        data = supervisorDetails.objects.get(id=id)
        store_data = store_detail.objects.all()
        return render(request,'admin_template/edit-supervisor.html',{'data':data,'store_detail':store_data,'message':message,'error_msg':error_msg})



@staff_member_required(login_url="/signup")
def store_supervisor_list(request):
    if request.method == 'GET':
        data = supervisorDetails.objects.all()

        for i in data:
            x = eval(i.store_array)
            print(x,type(x))
            storeArray = []
            for j in x:
                storeData = store_detail.objects.get(id=int(j))
                print(storeData.store_name)
                storeArray.append(storeData.store_name)
            print('storeArray >> ',storeArray,i)
            i.stores = storeArray
        return render(request,'admin_template/supervisor-management.html',{'data':data})



@staff_member_required(login_url="/signup")
def specific_store_supervisor(request,id):
    if request.method == 'GET':
        print('id >> ',id)
        data = supervisorDetails.objects.get(id=id)


        x = eval(data.store_array)
        print(x,type(x))
        storeArray = []
        for j in x:
            storeData = store_detail.objects.get(id=int(j))
            print(storeData.store_name)
            storeArray.append(storeData.store_name)
        print('storeArray >> ',storeArray)
        data.stores = storeArray

        dataDict = {}
        dataDict['sup_name'] = data.supervisor_name
        dataDict['sup_contact'] = data.supervisor_contact
        dataDict['sup_email'] = data.supervisor_email
        dataDict['sup_store_list'] = data.store_array
        dataDict['stores'] = data.stores

        print('data dict >> ',dataDict)
        return JsonResponse({'data':dataDict})


def subscription_management(request):
    if request.method == 'GET':
        data = Store_supervisor.objects.all()
        for i in data:
            splitData = i.supervisor_gender.split('|')
            i.Customer_gender = splitData[0]
            i.Customer_DOB = splitData[1]

            print(i)

        return render(request,'admin_template/subsctiptionManagement.html',{'data':data})




def delete_subscriber(request,id):
    if request.method == 'GET':
        data = Store_supervisor.objects.get(id=id)
        data.delete()
        return redirect('/subscription-management')

@staff_member_required(login_url="/signup")
def createStoreGroup(request):
    if request.method == 'GET':
        store_groups_id = ''
        try:
            store_groups = storeGroups.objects.latest('id').id
            store_groups = int(store_groups) + 1
            store_groups_id = 'GPID-00'+str(store_groups)
        except:
            store_groups_id = 'GPID-001'

        print('storeGroups >>> ',store_groups_id)
        store_data = store_detail.objects.all()
        return render(request,'admin_template/createStoreGroup.html',{'store_data':store_data,'store_groups_id':store_groups_id})

    if request.method == 'POST':
        groupName = request.POST['groupName']
        groupDescription = request.POST['groupDescription']
        groupID = request.POST['groupID']
        storeIDs = request.POST.getlist('storeIDs[]')

        print('groupName >>> ',groupName)
        print('groupDescription >>> ',groupDescription)
        print('groupID >>> ',groupID)
        print('storeIDs >>> ',storeIDs)

        # ---------------------------------------------------------------
        message = ''
        try:
            storeGroupObject = storeGroups(groupName=groupName.strip(), groupID=groupID.strip(),groupDescription=groupDescription.strip(), store_array=storeIDs)
            storeGroupObject.save()
            message = 'Success'
        except:
            message = 'Failed'
        # ---------------------------------------------------------------
        return JsonResponse({'responseData': message})





@staff_member_required(login_url="/signup")
def storeGroupList(request):
    if request.method == 'GET':
        store_groups_List = storeGroups.objects.all().order_by('-id')
        lent = len(store_groups_List)
        return render(request,'admin_template/storeGroupList.html',{'store_groups_List':store_groups_List,'lent':lent})



@staff_member_required(login_url="/signup")
def storeGroupDetail(request,id):
    if request.method == 'GET':
        store_groups_detail= storeGroups.objects.get(id=id)
        print('store_groups_detail >>> ',store_groups_detail.groupName)        
        print('store_groups_detail >>> ',store_groups_detail.groupID)        
        print('store_groups_detail >>> ',store_groups_detail.groupDescription)        

        storeDetail = []
        for i in eval(store_groups_detail.store_array):
            data = store_detail.objects.get(storeID = i)
            storeDetail.append(data)  

        return render(request,'admin_template/viewStoreGroupDetails.html',{'store_groups_detail':store_groups_detail,'storeDetail':storeDetail})


@staff_member_required(login_url="/signup")
def edit_storeGroupDetail(request,id):
    if request.method == 'GET':
        store_groups_detail= storeGroups.objects.get(id=id)
        print('store_groups_detail >>> ',store_groups_detail.groupName)        
        print('store_groups_detail >>> ',store_groups_detail.groupID)        
        print('store_groups_detail >>> ',store_groups_detail.groupDescription)   
        print('store_groups_detail >>> ',store_groups_detail.store_array)        

        storeDetail = []
        storeList = store_detail.objects.all()
        for i in storeList:
            for j in eval(store_groups_detail.store_array):
                if(i.storeID == j) :
                    print(i.storeID,type(i.storeID),'<==============>',j,type(j))
                    i.S_status = 'Exist'
                else:
                    i.S_status = 'Not Exist'

        print('storeList >>> ',storeList)
        # ------------------------------------------
        return render(request,'admin_template/editGroupDetails.html',{'store_groups_detail':store_groups_detail,'storeDetail':storeList})


    if request.method == 'POST':
        groupName = request.POST['groupName']
        groupDescription = request.POST['groupDescription']
        groupID = request.POST['groupID']
        storeIDs = request.POST.getlist('storeIDs[]')

        print('groupName >>> ',groupName)
        print('groupDescription >>> ',groupDescription)
        print('groupID >>> ',groupID)
        print('storeIDs >>> ',storeIDs)

        # ---------------------------------------------------------------
        message = ''
        try:
            # storeGroupObject = storeGroups(groupName=groupName.strip(), groupID=groupID.strip(),groupDescription=groupDescription.strip(), store_array=storeIDs)
            # storeGroupObject.save()
            storeGroupObject = storeGroups.objects.get(id=id)
            storeGroupObject.groupName = groupName
            storeGroupObject.groupID = groupID
            storeGroupObject.groupDescription=groupDescription
            storeGroupObject.store_array=storeIDs
            storeGroupObject.save()
            message = 'Success'
        except:
            message = 'Failed'
        # ---------------------------------------------------------------
        return JsonResponse({'responseData': message})




@staff_member_required(login_url="/signup")
def delete_StoreGroup(request,id):
    if request.method == 'GET':
        data = storeGroups.objects.get(id=id)
        data.delete()
        return redirect('storeGroupList')

@staff_member_required(login_url="/signup")
def storeGroupDataReportList(request,id):
    if request.method == 'GET':
        storeGroupObj = storeGroups.objects.get(id=id)
        reportData = groupReport.objects.filter(storeGroup=storeGroupObj).order_by('-id')
        print('report data >>>> ',reportData)
        lent = len(reportData)
        request.session['reportDatID'] = id
        supervisorData = supervisorDetails.objects.all().order_by('-id')
        return render(request,'admin_template/generateData.html',{'id':id,'reportData':reportData,'lent':lent,'storeGroupObj':storeGroupObj,'supervisorData':supervisorData})

@staff_member_required(login_url="/signup")
def CreateStoreGroupDataReport(request,id):
    if request.method == 'GET':
        store_groups_id = ''
        try:
            store_groups = groupReport.objects.latest('id').id
            store_groups = int(store_groups) + 1
            store_groups_id = 'RPID_00'+str(store_groups)
        except:
            store_groups_id = 'RPID_001'

        print('storeGroups >>> ',store_groups_id)
        return render(request,'admin_template/createDataRepost.html',{'id':id,'store_groups_id':store_groups_id})


@staff_member_required(login_url="/signup")
def getStoresArray(request,id):
    if request.method == 'GET':
        store_groups_detail= storeGroups.objects.get(id=id)
        print('store_groups_detail >>> ',store_groups_detail.groupName)        
        print('store_groups_detail >>> ',store_groups_detail.groupID)        
        print('store_groups_detail >>> ',store_groups_detail.groupDescription)        

        storeDetail = []
        dataDict = {}
        for i in eval(store_groups_detail.store_array):
            data = store_detail.objects.get(storeID = i)
            dataDict['StoreID'] = data.storeID
            dataDict['storeName'] = data.store_name
            storeDetail.append(dataDict)
            dataDict = {}

        print('storeDetail >> ',storeDetail)
        return JsonResponse(storeDetail,safe=False)


@staff_member_required(login_url="/signup")
def create_group_report(request,id):
    if request.method == 'POST':
        reportId = request.POST['reportID']
        reportMethod = request.POST['reportMethod']
        selectedList = request.POST.getlist('selectedStores[]')
        deSelectedList = request.POST.getlist('DeSelectedStores[]')

        reportCondition = ''

        if(reportMethod == 'OR'):
            reportCondition = selectedList

            print('reportId >>>>> ',reportId)
            print('reportMethod >>>>> ',reportMethod)
            print('reportCondition >>>>> ',reportCondition)

            # ---------------------------------------------------------------
            message = ''
            try:
                storeGroupObj = storeGroups.objects.get(id=id)
                groupReportObject = groupReport(storeGroup=storeGroupObj, reportID=reportId.strip(),method=reportMethod.strip(), selected_Conditions=reportCondition)
                groupReportObject.save()
                message = 'Success'
            except:
                message = 'Failed'
            # ---------------------------------------------------------------

        elif reportMethod == 'AND':
            print('=========================================================================')
            reportCondition = str(selectedList) +'|'+ str(deSelectedList)
            print('reportId >>>>> ',reportId)
            print('reportMethod >>>>> ',reportMethod)
            print('reportCondition >>>>> ',reportCondition)
            print('=========================================================================')

            # ---------------------------------------------------------------
            message = ''
            try:
                storeGroupObj = storeGroups.objects.get(id=id)
                groupReportObject = groupReport(storeGroup=storeGroupObj, reportID=reportId.strip(),method=reportMethod.strip(), selected_Conditions=reportCondition)
                groupReportObject.save()
                message = 'Success'
            except:
                message = 'Failed'
            # ---------------------------------------------------------------

        elif reportMethod == 'OR-NOT':
            print('=========================================================================')
            reportCondition = str(selectedList) +'|'+ str(deSelectedList)
            print('reportId >>>>> ',reportId)
            print('reportMethod >>>>> ',reportMethod)
            print('reportCondition >>>>> ',reportCondition)
            print('=========================================================================')

            # ---------------------------------------------------------------
            message = ''
            try:
                storeGroupObj = storeGroups.objects.get(id=id)
                groupReportObject = groupReport(storeGroup=storeGroupObj, reportID=reportId.strip(),method=reportMethod.strip(), selected_Conditions=reportCondition)
                groupReportObject.save()
                message = 'Success'
            except:
                message = 'Failed'
            # ---------------------------------------------------------------

        elif reportMethod == 'VISIT SINCE':
            print('=========================================================================')
            reportCondition = str(selectedList) +'|'+ str(deSelectedList)
            print('reportId >>>>> ',reportId)
            print('reportMethod >>>>> ',reportMethod)
            print('reportCondition >>>>> ',reportCondition)
            print('=========================================================================')

            # ---------------------------------------------------------------
            message = ''
            try:
                storeGroupObj = storeGroups.objects.get(id=id)
                groupReportObject = groupReport(storeGroup=storeGroupObj, reportID=reportId.strip(),method=reportMethod.strip(), selected_Conditions=reportCondition)
                groupReportObject.save()
                message = 'Success'
            except:
                message = 'Failed'
            # ---------------------------------------------------------------

        elif reportMethod == 'VISIT NUMBER':
            print('=========================================================================')
            reportCondition = str(selectedList) +'|'+ str(deSelectedList[0]) +'|'+ str(deSelectedList[1])
            print('reportId >>>>> ',reportId)
            print('reportMethod >>>>> ',reportMethod)
            print('reportCondition >>>>> ',reportCondition)
            print('=========================================================================')

            # ---------------------------------------------------------------
            message = ''
            try:
                storeGroupObj = storeGroups.objects.get(id=id)
                groupReportObject = groupReport(storeGroup=storeGroupObj, reportID=reportId.strip(),method=reportMethod.strip(), selected_Conditions=reportCondition)
                groupReportObject.save()
                message = 'Success'
            except:
                message = 'Failed'
            # ---------------------------------------------------------------

        return JsonResponse({'responseData':message})


@staff_member_required(login_url="/signup")
def fetchReportData(request,id):
    if request.method == 'GET':
        reportData = groupReport.objects.get(id=id)
        if reportData.method.strip() == 'OR':
            customerData = []
            uniqueCustomerDataList = []

            response = HttpResponse(content_type='text/csv')

            writer = csv.writer(response)
            writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            writer.writerow(['Stores ID : '+reportData.selected_Conditions,'','','',''])
            writer.writerow(['','','','',''])
            # writer.writerow(['Total Customers : '+str(len(uniqueCustomerDataList)),'','','',''])
            # writer.writerow(['','','','',''])
            writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email'])
            count = 0

            for i in eval(reportData.selected_Conditions):
                data = CustomerData.objects.filter(storeID = i)
                print('customer data >>> ',len(data))

                for i in data:
                    customersData = CustomerData.objects.filter(contact = i.contact)[0]
                    count = count + 1
                    print('count >> ',count)
                    cusInfoData = CustomerShopData.objects.filter(customerID = customersData)
                    if(customersData.entry_type == 'CSV-Onboar'):
                        writer.writerow([count,customersData.name,customersData.contact,customersData.email,0,'CSV-Onboard'])
                    else:
                        writer.writerow([count,customersData.name,customersData.contact,customersData.email,len(cusInfoData),customersData.entry_type])
            
            response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_OR_method.csv"'
            return response


        elif reportData.method.strip() == 'AND':
            stores = reportData.selected_Conditions.split('|')

            selectedStores = eval(stores[0])
            deSelectedStores = eval(stores[1])

            uniqueSelectedCustomers = []
            selectedcustomers = []

            uniqueUnselectedCustomers = []
            unselectedcustomers = []
            
            # =======================================================================================
            # =======================================================================================
            for store_ID in selectedStores:
                selectedcustomers = []
                customerData = CustomerData.objects.filter(storeID = store_ID)
                for customer in customerData:
                    selectedcustomers.append(customer.contact)               
                if len(uniqueSelectedCustomers) == 0:
                    uniqueSelectedCustomers = set(selectedcustomers)
                else:
                    uniqueSelectedCustomers = set(uniqueSelectedCustomers).intersection(selectedcustomers)
                    if len(uniqueSelectedCustomers) == 0:
                        response = HttpResponse(content_type='text/csv')
                        writer = csv.writer(response)
                        writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
                        writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
                        writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
                        writer.writerow(['','','','',''])
                        writer.writerow(['Total Customers : '+str(len(uniqueSelectedCustomers)),'','','',''])
                        writer.writerow(['','','','',''])
                        writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email'])
                        writer.writerow(['-','-','-','-','-'])
                
                        response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_AND_method.csv"'
                        return response
                print('uniqueSelectedCustomers >>> ',len(uniqueSelectedCustomers))
            # =======================================================================================
            mainList = []
            if(len(deSelectedStores)!=0):
                for store_ID in deSelectedStores:
                    customerData = CustomerData.objects.filter(storeID = store_ID)
                    for customer in customerData:
                        unselectedcustomers.append(customer.contact)                    
                    if len(uniqueUnselectedCustomers) == 0:
                        uniqueUnselectedCustomers = list(set(unselectedcustomers))
                    else:
                        uniqueUnselectedCustomers = list(set(unselectedcustomers).intersection(uniqueUnselectedCustomers))
            # =======================================================================================
                print('uniqueSelectedCustomers >>> ',uniqueSelectedCustomers)
                print('uniqueUnselectedCustomers >>> ',uniqueUnselectedCustomers)

                flag = False
                for data_i in uniqueSelectedCustomers:
                    print('checking >>> ',data_i)
                    if data_i in uniqueUnselectedCustomers:
                        print('contact exist!')
                    else:
                        flag = True
                        mainList.append(data_i)
            # =======================================================================================
            print('mainList >>> ',mainList)

            if(len(mainList) == 0 and len(deSelectedStores) == 0):
                count = 0
                response = HttpResponse(content_type='text/csv')
                writer = csv.writer(response)
                writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
                writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
                writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
                writer.writerow(['','','','',''])
                writer.writerow(['Total Customers : '+str(len(uniqueSelectedCustomers)),'','','',''])
                writer.writerow(['','','','',''])
                writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email','Number of Visits','Entry Type'])
                for i in list(set(uniqueSelectedCustomers)):
                    customersData = CustomerData.objects.filter(contact = i)[0]
                    # uniqueCustomerDataList.append(customersData)
                    count = count + 1
                    cusInfoData = CustomerShopData.objects.filter(customerID = customersData)
                    if(customersData.entry_type == 'CSV-Onboar'):
                        writer.writerow([count,customersData.name,customersData.contact,customersData.email,0,'CSV-Onboard'])
                    else:
                        writer.writerow([count,customersData.name,customersData.contact,customersData.email,len(cusInfoData),customersData.entry_type])
                response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_AND_method.csv"'
                return response

            elif(len(mainList) == 0):
                response = HttpResponse(content_type='text/csv')
                writer = csv.writer(response)
                writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
                writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
                writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
                writer.writerow(['','','','',''])
                writer.writerow(['Total Customers : '+str(len(mainList)),'','','',''])
                writer.writerow(['','','','',''])
                writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email'])
                writer.writerow(['-','-','-','-','-'])
        
                response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_AND_method.csv"'
                return response

            else:
                count = 0
                response = HttpResponse(content_type='text/csv')

                writer = csv.writer(response)
                writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
                writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
                writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
                writer.writerow(['','','','',''])
                writer.writerow(['Total Customers : '+str(len(mainList)),'','','',''])
                writer.writerow(['','','','',''])
                writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email','Number of Visits','Entry Type'])
                for i in list(set(mainList)):
                    customersData = CustomerData.objects.filter(contact = i)[0]
                    # uniqueCustomerDataList.append(customersData)
                    count = count + 1
                    cusInfoData = CustomerShopData.objects.filter(customerID = customersData)

                    if(customersData.entry_type == 'CSV-Onboar'):
                        writer.writerow([count,customersData.name,customersData.contact,customersData.email,0,'CSV-Onboard'])
                    else:
                        writer.writerow([count,customersData.name,customersData.contact,customersData.email,len(cusInfoData),customersData.entry_type])
                response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_AND_method.csv"'
                return response



        elif reportData.method.strip() == 'OR-NOT':
            stores = reportData.selected_Conditions.split('|')

            selectedStores = eval(stores[0])
            deSelectedStores = eval(stores[1])

            uniqueSelectedCustomers = []
            selectedcustomers = []

            uniqueUnselectedCustomers = []
            unselectedcustomers = []


            customerCOntactData = []
            uniqueCustomerDataList = []
            uniqueCustomerDataList2 = []


            response = HttpResponse(content_type='text/csv')

            writer = csv.writer(response)
            writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
            writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
            writer.writerow(['','','','',''])
            # writer.writerow(['Total Customers : '+str(len(uniqueCustomerDataList)),'','','',''])
            # writer.writerow(['','','','',''])
            writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email'])
            count = 0

            for i in selectedStores:
                data = CustomerData.objects.filter(storeID = i)

                for i in data:
                    if i.contact not in customerCOntactData:
                        customerCOntactData.append(i.contact)


            for j in deSelectedStores:
                data = CustomerData.objects.filter(storeID = i)

                for m in data:
                    if m.contact not in uniqueCustomerDataList:
                        uniqueCustomerDataList.append(m.contact)

            # print('customerCOntactData >> ',len(customerCOntactData))
            # print('uniqueCustomerDataList >> ',len(uniqueCustomerDataList))


            for k in customerCOntactData:
                if k not in  uniqueCustomerDataList:
                    count = count + 1
                    # print('counter >> ',count)
                    cusInfoData = CustomerData.objects.filter(contact = k)[0]
                    if(cusInfoData.entry_type == 'CSV-Onboar'):
                        writer.writerow([count,cusInfoData.name,cusInfoData.contact,cusInfoData.email,'CSV-Onboard'])
                    else:
                        writer.writerow([count,cusInfoData.name,cusInfoData.contact,cusInfoData.email,cusInfoData.entry_type])










            # for i in selectedStores:
            #     data = CustomerData.objects.filter(storeID = i)
            #     print('customer data >>> ',len(data))

            #     for i in data:
            #         if i.contact not in customerCOntactData:
            #             customersData = CustomerData.objects.filter(contact = i.contact)[0]
            #             customerCOntactData.append(i.contact)

            #             count = count + 1
            #             print('count >> ',count)
            #             cusInfoData = CustomerShopData.objects.filter(customerID = customersData)
            #             if(customersData.entry_type == 'CSV-Onboar'):
            #                 writer.writerow([count,customersData.name,customersData.contact,customersData.email,0,'CSV-Onboard'])
            #             else:
            #                 writer.writerow([count,customersData.name,customersData.contact,customersData.email,len(cusInfoData),customersData.entry_type])

            # for i in deSelectedStores:
            #     data = CustomerData.objects.filter(storeID = i)
            #     print('customer data >>> ',len(data))

            #     for i in data:
            #         if i.contact in customerCOntactData:
            #             pass
            #         else:
            #             customersData = CustomerData.objects.filter(contact = i.contact)[0]
            #             count = count + 1
            #             print('count >> ',count)
            #             cusInfoData = CustomerShopData.objects.filter(customerID = customersData)
            #             if(customersData.entry_type == 'CSV-Onboar'):
            #                 writer.writerow([count,customersData.name,customersData.contact,customersData.email,0,'CSV-Onboard'])
            #             else:
            #                 writer.writerow([count,customersData.name,customersData.contact,customersData.email,len(cusInfoData),customersData.entry_type])
            
            response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_OR_NOT_method.csv"'
            return response
            
            # # =======================================================================================
            # # =======================================================================================
            # for store_ID in selectedStores:
            #     selectedcustomers = []
            #     customerData = CustomerData.objects.filter(storeID = store_ID)
            #     for customer in customerData:
            #         selectedcustomers.append(customer.contact)               
            #     if len(uniqueSelectedCustomers) == 0:
            #         uniqueSelectedCustomers = set(selectedcustomers)
            #     else:
            #         uniqueSelectedCustomers = set(uniqueSelectedCustomers).intersection(selectedcustomers)
            #         if len(uniqueSelectedCustomers) == 0:
            #             response = HttpResponse(content_type='text/csv')
            #             writer = csv.writer(response)
            #             writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            #             writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
            #             writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
            #             writer.writerow(['','','','',''])
            #             writer.writerow(['Total Customers : '+str(len(uniqueSelectedCustomers)),'','','',''])
            #             writer.writerow(['','','','',''])
            #             writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email'])
            #             writer.writerow(['-','-','-','-','-'])
                
            #             response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_AND_method.csv"'
            #             return response
            #     print('uniqueSelectedCustomers >>> ',len(uniqueSelectedCustomers))
            # # =======================================================================================
            # mainList = []
            # if(len(deSelectedStores)!=0):
            #     for store_ID in deSelectedStores:
            #         customerData = CustomerData.objects.filter(storeID = store_ID)
            #         for customer in customerData:
            #             unselectedcustomers.append(customer.contact)                    
            #         if len(uniqueUnselectedCustomers) == 0:
            #             uniqueUnselectedCustomers = list(set(unselectedcustomers))
            #         else:
            #             uniqueUnselectedCustomers = list(set(unselectedcustomers).intersection(uniqueUnselectedCustomers))
            # # =======================================================================================
            #     print('uniqueSelectedCustomers >>> ',len(uniqueSelectedCustomers))
            #     print('uniqueUnselectedCustomers >>> ',len(uniqueUnselectedCustomers))

            #     flag = False
            #     for data_i in uniqueSelectedCustomers:
            #         print('checking >>> ',data_i)
            #         if data_i in uniqueUnselectedCustomers:
            #             # uniqueSelectedCustomers.remove(data_i)
            #             uniqueUnselectedCustomers.remove(data_i)
            #             print('contact removed!')
            #         else:
            #             flag = True
            #             mainList.append(data_i)
            # print('uniqueUnselectedCustomers after >>> ',len(uniqueUnselectedCustomers))
            # mainList.extend(uniqueUnselectedCustomers)
            # # =======================================================================================
            # print('mainList >>> ',len(mainList))

            # if(len(mainList) == 0 and len(deSelectedStores) == 0):
            #     count = 0
            #     response = HttpResponse(content_type='text/csv')
            #     writer = csv.writer(response)
            #     writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            #     writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
            #     writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
            #     writer.writerow(['','','','',''])
            #     writer.writerow(['Total Customers : '+str(len(uniqueSelectedCustomers)),'','','',''])
            #     writer.writerow(['','','','',''])
            #     writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email','Number of Visits','Entry Type'])
            #     for i in list(set(uniqueSelectedCustomers)):
            #         customersData = CustomerData.objects.filter(contact = i)[0]
            #         # uniqueCustomerDataList.append(customersData)
            #         count = count + 1
            #         cusInfoData = CustomerShopData.objects.filter(customerID = customersData)
            #         if(customersData.entry_type == 'CSV-Onboar'):
            #             writer.writerow([count,customersData.name,customersData.contact,customersData.email,0,'CSV-Onboard'])
            #         else:
            #             writer.writerow([count,customersData.name,customersData.contact,customersData.email,len(cusInfoData),customersData.entry_type])
            #     response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_OR_NOT_method.csv"'
            #     return response

            # elif(len(mainList) == 0):
            #     response = HttpResponse(content_type='text/csv')
            #     writer = csv.writer(response)
            #     writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            #     writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
            #     writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
            #     writer.writerow(['','','','',''])
            #     writer.writerow(['Total Customers : '+str(len(mainList)),'','','',''])
            #     writer.writerow(['','','','',''])
            #     writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email'])
            #     writer.writerow(['-','-','-','-','-'])
        
            #     response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_AND_method.csv"'
            #     return response

            # else:
            #     count = 0
            #     response = HttpResponse(content_type='text/csv')

            #     writer = csv.writer(response)
            #     writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            #     writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
            #     writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
            #     writer.writerow(['','','','',''])
            #     writer.writerow(['Total Customers : '+str(len(mainList)),'','','',''])
            #     writer.writerow(['','','','',''])
            #     writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email','Number of Visits','Entry Type'])
            #     for i in list(set(mainList)):
            #         customersData = CustomerData.objects.filter(contact = i)[0]
            #         # uniqueCustomerDataList.append(customersData)
            #         count = count + 1
            #         cusInfoData = CustomerShopData.objects.filter(customerID = customersData)

            #         if(customersData.entry_type == 'CSV-Onboar'):
            #             writer.writerow([count,customersData.name,customersData.contact,customersData.email,0,'CSV-Onboard'])
            #         else:
            #             writer.writerow([count,customersData.name,customersData.contact,customersData.email,len(cusInfoData),customersData.entry_type])
            #     response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_AND_method.csv"'
            #     return response



        elif reportData.method.strip() == 'VISIT SINCE':
            stores = reportData.selected_Conditions.split('|')

            selectedStores = eval(stores[0])
            deSelectedStores = eval(stores[1])

            uniqueSelectedCustomers = []
            selectedcustomers = []

            uniqueUnselectedCustomers = []
            unselectedcustomers = []
            # =======================================================================================
            # =======================================================================================
            for store_ID in selectedStores:
                print('store id >>> ',store_ID)
                customerData = CustomerData.objects.filter(storeID = store_ID)
                print('customerData count >>> ',len(customerData))

                for customer in customerData:
                    selectedcustomers.append(customer.contact)
                print('selectedcustomers count >>> ',len(set(selectedcustomers)))
                
                if len(uniqueSelectedCustomers) == 0:
                    uniqueSelectedCustomers.extend(list(set(selectedcustomers)))
                    print('uniqueSelectedCustomers when u=0 >>> ',len(uniqueSelectedCustomers))

                else:
                    uniqueSelectedCustomers.extend(list(set(selectedcustomers).intersection(uniqueSelectedCustomers)))
                    print('uniqueSelectedCustomers when u!=0 >>> ',len(uniqueSelectedCustomers))

                print('final data uniqueSelectedCustomers >>>> ',len(uniqueSelectedCustomers))
            # =======================================================================================
            if(len(deSelectedStores)!=0):
                for store_ID in deSelectedStores:
                    print('store id >>> ',store_ID)
                    customerData = CustomerData.objects.filter(storeID = store_ID)
                    print('customerData count >>> ',len(customerData))

                    for customer in customerData:
                        unselectedcustomers.append(customer.contact)
                    print('unselectedcustomers count >>> ',len(set(unselectedcustomers)))
                    
                    if len(uniqueUnselectedCustomers) == 0:
                        uniqueUnselectedCustomers.extend(list(set(unselectedcustomers)))
                        print('uniqueUnselectedCustomers when u=0 >>> ',len(uniqueUnselectedCustomers))

                    else:
                        uniqueUnselectedCustomers.extend(list(set(unselectedcustomers).intersection(uniqueUnselectedCustomers)))
                        print('uniqueUnselectedCustomers when u!=0 >>> ',len(uniqueUnselectedCustomers))

                    print('final data uniqueUnselectedCustomers >>>> ',len(uniqueUnselectedCustomers))
            else:
                print('final data uniqueUnselectedCustomers else part >>>> ',len(uniqueUnselectedCustomers))
            # =======================================================================================
            print('=========================================================================')
            print('AND data report customers >>> ',len(list(set(uniqueSelectedCustomers).intersection(uniqueUnselectedCustomers))),list(set(uniqueSelectedCustomers).intersection(uniqueUnselectedCustomers)))
            print('=========================================================================')
            # =======================================================================================
            uniqueCustomerDataList = []
            if(len(list(set(uniqueSelectedCustomers).intersection(uniqueUnselectedCustomers))) == 0):
                pass
            else:
                for i in list(set(uniqueSelectedCustomers).intersection(uniqueUnselectedCustomers)):
                    customersData = CustomerData.objects.filter(contact = i)

                    if(len(customersData) > 0):
                        print('customersData >>> ',customersData[0].name)
                        dataDict = {}
                        dataDict['customerName'] = customersData[0].name
                        dataDict['customerContact'] = customersData[0].contact
                        dataDict['customerEmail'] = customersData[0].email
                        dataDict['customerStoreID'] = customersData[0].storeID
                        uniqueCustomerDataList.append(dataDict)

                    else:
                        print('customersData >>> ',customersData[0].name)
                        dataDict = {}
                        dataDict['customerName'] = customersData[0].name
                        dataDict['customerContact'] = customersData[0].contact
                        dataDict['customerEmail'] = customersData[0].email
                        dataDict['customerStoreID'] = customersData[0].storeID

                        uniqueCustomerDataList.append(dataDict)

            response = HttpResponse(content_type='text/csv')

            writer = csv.writer(response)
            writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            writer.writerow(['Selected Stores ID : '+str(selectedStores),'','','',''])
            # writer.writerow(['De-Selected Stores ID : '+str(deSelectedStores),'','','',''])
            writer.writerow(['','','','',''])
            writer.writerow(['Total Customers : '+str(len(uniqueCustomerDataList)),'','','',''])
            writer.writerow(['','','','',''])
            writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email','Store ID'])
            count = 0

            if(len(uniqueCustomerDataList) == 0):
                writer.writerow(['-','-','-','-','-'])
                
                response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_VisitSince_method.csv"'
                return response
            else:
                for k in uniqueCustomerDataList:
                    count = count + 1
                    writer.writerow([count,k['customerName'],k['customerContact'],k['customerEmail'],k['customerStoreID']])
                
                response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_VisitSince_method.csv"'
                return response

        elif reportData.method.strip() == 'VISIT NUMBER':
            customerData = []
            uniqueCustomerDataList = []

            conditionData = reportData.selected_Conditions.split('|')

            storeIDS = eval(conditionData[0])
            numberOfVisit = conditionData[1]
            formula = conditionData[2]

            print('storeIDS >>>> ',storeIDS)
            print('numberOfVisit >>>> ',numberOfVisit)
            print('formula >>>> ',formula)

            uniqueCustomerDataList = []
            for store in storeIDS:
                data = CustomerData.objects.filter(storeID = store)
                print('store id >>> ',store,'count >> ',len(data))
                for i in data:
                    print('i data >>> ',i.contact)
                    customerInfo = CustomerShopData.objects.filter(customerID = i)

                    if(formula == 'Number of Visits>=N' and len(customerInfo) >= int(numberOfVisit)):
                        dataDict = {}
                        dataDict['customerName'] = i.name
                        dataDict['customerContact'] = i.contact
                        dataDict['customerEmail'] = i.email
                        dataDict['customerStoreID'] = i.storeID
                        dataDict['Visit Count'] = len(customerInfo)

                        uniqueCustomerDataList.append(dataDict)

                    elif(formula == 'Number of Visits<N' and len(customerInfo) < int(numberOfVisit)):
                        dataDict = {}
                        dataDict['customerName'] = i.name
                        dataDict['customerContact'] = i.contact
                        dataDict['customerEmail'] = i.email
                        dataDict['customerStoreID'] = i.storeID
                        dataDict['Visit Count'] = len(customerInfo)


                        uniqueCustomerDataList.append(dataDict)

            response = HttpResponse(content_type='text/csv')

            writer = csv.writer(response)
            writer.writerow(['REPORT ID : '+reportData.reportID,'','','',''])
            writer.writerow(['Stores ID : '+conditionData[0],'','','',''])
            writer.writerow(['','','','',''])
            writer.writerow(['Total Customers : '+str(len(uniqueCustomerDataList)),'','','',''])
            writer.writerow(['','','','',''])
            writer.writerow(['S.No.','Customer Name','Customer Contact','Customer Email','Store ID','Visit Count'])
            count = 0
            if(len(uniqueCustomerDataList) == 0):
                writer.writerow(['-','-','-','-','-'])
                
                response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_VisitNumber_method.csv"'
                return response
            else:
                for k in uniqueCustomerDataList:
                    count = count + 1
                    writer.writerow([count,k['customerName'],k['customerContact'],k['customerEmail'],k['customerStoreID'],k['Visit Count']])
                
                response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'_VisitNumber_method.csv"'
                return response

        else:
            return HttpResponseRedirect('/store-Group-DataReport-List/'+str(request.session['reportDatID']))



@staff_member_required(login_url="/signup")
def delete_report(request,id):
    if request.method == 'GET':
        data = groupReport.objects.get(id=id)
        data.delete()
        idData = request.session['reportDatID']
        return HttpResponseRedirect('/store-Group-DataReport-List/'+str(idData))



@staff_member_required(login_url="/signup")
def getReportDetails(request,id):
    if request.method == 'GET':
        reportDetail = groupReport.objects.get(id=id)
        print('reportDetail >>>> ',reportDetail)

        if reportDetail.method == 'AND':
            stores = reportDetail.selected_Conditions.split('|')


            selectedStores = eval(stores[0])
            deSelectedStores = eval(stores[1])

            print('selectedStores >>> ',selectedStores)
            print('deSelectedStores >>> ',deSelectedStores)

            storesDataList = []

            for i in selectedStores:
                data = store_detail.objects.get(storeID = i)
                dataDict = {}
                dataDict['storeID'] = data.storeID
                dataDict['storeName'] = data.store_name
                dataDict['storeAddress'] = data.store_location+','+ data.store_town+','+ data.store_city+','+ data.store_state
                dataDict['SelectionStatus'] = 'selected'
                print('dataDict >>> ',dataDict)

                storesDataList.append(dataDict)

            for i in deSelectedStores:
                data = store_detail.objects.get(storeID = i)
                dataDict = {}
                dataDict['storeID'] = data.storeID
                dataDict['storeName'] = data.store_name
                dataDict['storeAddress'] = data.store_location+','+ data.store_town+','+ data.store_city+','+ data.store_state
                dataDict['SelectionStatus'] = 'deSelected'
                print('dataDict >>> ',dataDict)

                storesDataList.append(dataDict)

            print('storesDataList >>> ',storesDataList)

        elif reportDetail.method == 'OR-NOT':
            stores = reportDetail.selected_Conditions.split('|')


            selectedStores = eval(stores[0])
            deSelectedStores = eval(stores[1])

            print('selectedStores >>> ',selectedStores)
            print('deSelectedStores >>> ',deSelectedStores)

            storesDataList = []

            for i in selectedStores:
                data = store_detail.objects.get(storeID = i)
                dataDict = {}
                dataDict['storeID'] = data.storeID
                dataDict['storeName'] = data.store_name
                dataDict['storeAddress'] = data.store_location+','+ data.store_town+','+ data.store_city+','+ data.store_state
                dataDict['SelectionStatus'] = 'selected'
                print('dataDict >>> ',dataDict)

                storesDataList.append(dataDict)

            for i in deSelectedStores:
                data = store_detail.objects.get(storeID = i)
                dataDict = {}
                dataDict['storeID'] = data.storeID
                dataDict['storeName'] = data.store_name
                dataDict['storeAddress'] = data.store_location+','+ data.store_town+','+ data.store_city+','+ data.store_state
                dataDict['SelectionStatus'] = 'deSelected'
                print('dataDict >>> ',dataDict)

                storesDataList.append(dataDict)

            print('storesDataList >>> ',storesDataList)


        elif reportDetail.method == 'VISIT NUMBER':
            stores = reportDetail.selected_Conditions.split('|')


            selectedStores = eval(stores[0])

            print('selectedStores >>> ',selectedStores)

            storesDataList = []
            for i in selectedStores:
                data = store_detail.objects.get(storeID = i)
                dataDict = {}
                dataDict['storeID'] = data.storeID
                dataDict['storeName'] = data.store_name
                dataDict['storeAddress'] = data.store_location+','+ data.store_town+','+ data.store_city+','+ data.store_state
                dataDict['SelectionStatus'] = 'selected'
                print('dataDict >>> ',dataDict)

                storesDataList.append(dataDict)

            print('storesDataList >>> ',storesDataList)

        elif reportDetail.method == 'OR':
            stores = eval(reportDetail.selected_Conditions)
            storesDataList = []
            for i in stores:
                data = store_detail.objects.get(storeID = i)
                storesDataList.append(data)

        

        elif reportDetail.method == 'VISIT SINCE':
            stores = reportDetail.selected_Conditions.split('|')


            selectedStores = eval(stores[0])
            deSelectedStores = eval(stores[1])

            print('selectedStores >>> ',selectedStores)
            print('deSelectedStores >>> ',deSelectedStores)

            storesDataList = []

            for i in selectedStores:
                data = store_detail.objects.get(storeID = i)
                dataDict = {}
                dataDict['storeID'] = data.storeID
                dataDict['storeName'] = data.store_name
                dataDict['storeAddress'] = data.store_location+','+ data.store_town+','+ data.store_city+','+ data.store_state
                dataDict['SelectionStatus'] = 'selected'
                print('dataDict >>> ',dataDict)

                storesDataList.append(dataDict)

            print('storesDataList >>> ',storesDataList)

        return render(request,'admin_template/viewReportDetails.html',{'reportDetails':reportDetail,'storesDataList':storesDataList})



# @staff_member_required(login_url="/signup")
def shareReport(request):
    if request.method == 'GET':
        sharedReportData = store_Shared_Record_History.objects.all()
        return render(request,'admin_template/sharedReportHistory.html',{'sharedReportData':sharedReportData})

    if request.method == 'POST':
        supervisorFk = request.POST.getlist('supervisor_fk[]')
        reportId= request.POST['report_fk']

        print('supervisorFk >>> ',supervisorFk)
        print('reportFk >>> ',reportId)

        # --------------------- SAVE RECORD TO SHARE REPORT MODEL   -------------------------
        # ===================================================================================
        message = ''
        try:
            reportObj = groupReport.objects.get(id=reportId)
            for i in supervisorFk:
                print('i >>. ',i)
                supervisorObj = supervisorDetails.objects.get(id=int(i))
                print('supervisorObj >>. ',supervisorObj)
                print('supervisor_email >>. ',supervisorObj.supervisor_email)
                print('reportObj >>. ',reportObj)
                # ---------------------------------------------------------------------------
                shareReportObject = store_Shared_Record_History(reportID=reportObj, supervisorID=supervisorObj,supervisor_email=supervisorObj.supervisor_email.strip())
                shareReportObject.save()
                # ---------------------------------------------------------------------------
            message = 'success'
        except:
            message = 'Failed'
        # ===================================================================================
        return JsonResponse({'responseData':message})




# =------------------------=-=-=-=-=-=-=-=-=-=-=-=-==-==-==-=

@login_required(login_url="/signup")
def adminAmountOfPurchaseReport(request):
    if request.method == 'GET':
        if request.user:
            print('user >>> ',request.user)
        if request.user.is_superuser:
            storeArray = store_detail.objects.all()
            # supervisorObj = supervisorDetails.objects.get(supervisor_email = request.user)
            supervisor_amountOfPurchase_Report_HistoryData = admin_Report_History_for_amount.objects.all().order_by('-id')
        return render(request,'admin_template/amountOfPurchasereport.html',{'supervisor_amountOfPurchase_Report_HistoryData': supervisor_amountOfPurchase_Report_HistoryData,'storeArray':storeArray,'storelength':len(storeArray)})

    if request.method == 'POST':
        selectedStoreArray = request.POST.getlist('storeArray[]')
        dateRange = request.POST['dateRange']

        reportId = ''
        try:
            store_groups = admin_Report_History_for_amount.objects.latest('id').id
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
            supervisor_amountOfPurchase_Report_HistoryObject = admin_Report_History_for_amount(reportID=reportId.strip(),selected_stores=selectedStoreArray,dateRange=dateRange)
            supervisor_amountOfPurchase_Report_HistoryObject.save()
            message = 'Success'
        except:
            message = 'Failed'
        # ---------------------------------------------------------------

        return JsonResponse({'message' : message})




@login_required(login_url="/signup")
def downloadAdminAmountPurchaseReport(request,id):
    reportData = admin_Report_History_for_amount.objects.get(id = int(id))
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
    writer.writerow(['REPORT ID : '+report_ID,'','','',''])
    writer.writerow(['Date Range : '+reportData.dateRange,'','','',''])
    writer.writerow(['========================================================================================================================','','','',''])

    for storeIDs in selected_stores:
        storeDeta = store_detail.objects.get(storeID=storeIDs)
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Stores Detail : '+str(storeIDs),' >>> ',storeDeta.store_name,'',''])
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Customer Name','Customer Contact','Customer Email','Total Purchase (In Rs.)'])
        user = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=storeIDs).distinct()
        # user = CustomerData.objects.filter(storeID=storeIDs).distinct()
        print('user data >>>',len(user),user)


        for i in user:
            print('i data',i)
            customerInfo = CustomerShopData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,customerID=i,storeID=storeIDs)
            # if(len(customerInfo) !=0):
            amountSum = 0
            for j in customerInfo:
                amountSum = amountSum + int(j.amount)
            writer.writerow([i.name,i.contact,i.email,amountSum])
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
        # exit()
    response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'.csv"'
    return response





@login_required(login_url="/signup")
def adminNoOfvisitReport(request):
    if request.method == 'GET':
        if request.user:
            print('user ==>>> ',request.user)
        if request.user.is_superuser:
            storeArray = store_detail.objects.all()
            supervisor_amountOfPurchase_Report_HistoryData = admin_Report_History_for_visit.objects.all().order_by('-id')
        return render(request,'admin_template/noOfVisitReport.html',{'supervisor_amountOfPurchase_Report_HistoryData': supervisor_amountOfPurchase_Report_HistoryData,'storeArray':storeArray,'storelength':len(storeArray)})
    if request.method == 'POST':
        selectedStoreArray = request.POST.getlist('storeArray[]')
        dateRange = request.POST['dateRange']

        reportId = ''
        try:
            store_groups = admin_Report_History_for_visit.objects.latest('id').id
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
            supervisor_noOfVisit_Report_HistoryObject = admin_Report_History_for_visit(reportID=reportId.strip(),selected_stores=selectedStoreArray,dateRange=dateRange)
            supervisor_noOfVisit_Report_HistoryObject.save()
            message = 'Success'
        except:
            message = 'Failed'
        # ---------------------------------------------------------------

        return JsonResponse({'message' : message})



@login_required(login_url="/signup")
def downloadAdminNumberOfVisitReport(request,id):
    reportData = admin_Report_History_for_visit.objects.get(id = int(id))
    report_ID = reportData.reportID
    selected_stores = eval(reportData.selected_stores)
    dateRange = reportData.dateRange.split('-')
    # ------------------------------------------------------------------
    startDate = dateRange[0].strip().split('/')
    endDate = dateRange[1].strip().split('/')

    start_date = datetime.date(int(startDate[2]), int(startDate[0]), int(startDate[1])) 
    end_date = datetime.date(int(endDate[2]), int(endDate[0]), int(endDate[1]))
    # ------------------------------------------------------------------
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['REPORT ID : '+report_ID,'','','',''])
    writer.writerow(['Date Range : '+reportData.dateRange,'','','',''])
    writer.writerow(['========================================================================================================================','','','',''])
    for storeIDs in selected_stores:
        storeDeta = store_detail.objects.get(storeID=storeIDs)
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Stores Detail : '+str(storeIDs),' >>> ',storeDeta.store_name,'',''])
        writer.writerow(['========================================================================================================================','','','',''])
        writer.writerow(['Customer Name','Customer Contact','Customer Email','Total Number of Visits'])
        # user = CustomerShopData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=storeIDs)
        user = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=storeIDs).distinct()
        for i in user:
            customerInfo = CustomerShopData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,customerID=i,storeID=storeIDs)
            writer.writerow([i.name,i.contact,i.email,len(customerInfo)])
        # ------------------------------------------------------------------
        # ------------------------------------------------------------------
    response['content-Disposition'] = 'attachment; filename = "customer_report_'+reportData.reportID+'.csv"'
    return response




@login_required(login_url="/signup")
def viewAdminAmountOfPurchseReport(request,id):
    if request.method == 'GET':
        if request.user:
            print('user ==>>> ',request.user)
        if request.user.is_superuser:
            storeArray = store_detail.objects.all()
            supervisor_amountOfPurchase_Report_HistoryData = admin_Report_History_for_visit.objects.all().order_by('-id')
            # ==========================================================================================================================
            reportData = admin_Report_History_for_amount.objects.get(id = int(id))
            report_ID = reportData.reportID
            selected_stores = eval(reportData.selected_stores)
            dateRange = reportData.dateRange.split('-')

            date_range = reportData.dateRange

            storeArray = []
            for i in selected_stores:
                storeDict = {}
                storeDict['storeName'] = i
                storeData = store_detail.objects.get(storeID = i)
                storeDict['storeiD'] = storeData.store_name
                storeArray.append(storeDict)

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
            # ========================================================================================================================
            customerContactArray = []
            customerDict = []
            for stores in selected_stores:
                customer_Data = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=stores).distinct()
                print('customer data >>> ',len(customer_Data))

                for j in customer_Data:
                    dataDict = {}
                    if j.storeID in selected_stores:
                        # print('j data >>> ',j.storeID)
                        dataDict['customerName'] = j.name
                        dataDict['customerContact'] = j.contact
                        # dataDict['customerEmail'] = j.email

                        customerInfo = CustomerShopData.objects.filter(customerID = j,storeID = j.storeID,time_stamp__gte=start_date,time_stamp__lte=end_date)
                        # print('customerInfo >>>>>>>>', customerInfo)
                        if(len(customerInfo) !=0):
                            amountSum = 0
                            for j in customerInfo:
                                amountSum = amountSum + int(j.amount)
                            dictList = []
                            for stores in selected_stores:
                                sumDict = {}
                                if(stores == j.storeID):
                                    # print('store matched >>>>>')
                                    sumDict['storeID'] = j.storeID
                                    sumDict['totalSum'] = amountSum
                                    dictList.append(sumDict)
                                else:
                                    # print('store not matched <<<<<')
                                    sumDict['storeID'] = stores
                                    sumDict['totalSum'] = '-'
                                    dictList.append(sumDict)
                                
                            dataDict['storeData'] = dictList
                    customerDict.append(dataDict)




            #     for customers in customer_Data:
            #         customerContactArray.append(customers.contact)
            #     print('customer data >>> ',len(customerContactArray))
            # totalCount = len(set(customerContactArray))
            # for contact in set(customerContactArray):
            #     dataDict = {}
            #     customer = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,contact = contact)
                # print('customer >>> ',customer)
                # for j in customer:
                #     if j.storeID in selected_stores:
                #         # print('j data >>> ',j.storeID)
                #         dataDict['customerName'] = j.name
                #         dataDict['customerContact'] = j.contact
                #         # dataDict['customerEmail'] = j.email

                #         customerInfo = CustomerShopData.objects.filter(customerID = j,storeID = j.storeID,time_stamp__gte=start_date,time_stamp__lte=end_date)
                #         # print('customerInfo >>>>>>>>', customerInfo)
                #         if(len(customerInfo) !=0):
                #             amountSum = 0
                #             for j in customerInfo:
                #                 amountSum = amountSum + int(j.amount)
                #             dictList = []
                #             for stores in selected_stores:
                #                 sumDict = {}
                #                 if(stores == j.storeID):
                #                     # print('store matched >>>>>')
                #                     sumDict['storeID'] = j.storeID
                #                     sumDict['totalSum'] = amountSum
                #                     dictList.append(sumDict)
                #                 else:
                #                     # print('store not matched <<<<<')
                #                     sumDict['storeID'] = stores
                #                     sumDict['totalSum'] = '-'
                #                     dictList.append(sumDict)
                                
                #             dataDict['storeData'] = dictList

                #     customerDict.append(dataDict)

                # print('customerDict >>>>>>>>', customerDict)
            # ========================================================================================================================
        return render(request,'admin_template/viewAmountReport.html',{'report_ID':report_ID,'dateRange':date_range,'selected_stores':storeArray,'customerDict':customerDict})
    



@staff_member_required(login_url="/signup")
def deleteAdminAmountOfPurchaseReport(request,id):
    if request.user.is_superuser:
        if request.method == 'GET':
            del_data = admin_Report_History_for_amount.objects.get(pk=id)
            del_data.delete()
            return HttpResponseRedirect('/report-amount-of-purchase')
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')









@login_required(login_url="/signup")
def viewAdminNoOfvisitReport(request,id):
    if request.method == 'GET':
        if request.user:
            print('user ==>>> ',request.user)
        if request.user.is_superuser:
            storeArray = store_detail.objects.all()
            supervisor_amountOfPurchase_Report_HistoryData = admin_Report_History_for_visit.objects.all().order_by('-id')
            # ==========================================================================================================================
            reportData = admin_Report_History_for_visit.objects.get(id = int(id))
            report_ID = reportData.reportID
            selected_stores = eval(reportData.selected_stores)
            dateRange = reportData.dateRange.split('-')

            date_range = reportData.dateRange

            storeArray = []
            for i in selected_stores:
                storeDict = {}
                storeDict['storeName'] = i
                storeData = store_detail.objects.get(storeID = i)
                storeDict['storeiD'] = storeData.store_name
                storeArray.append(storeDict)

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
            # ========================================================================================================================
            customerContactArray = []
            customerDict = []
            for stores in selected_stores:
                count = 0
                customer_Data = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,storeID=stores).distinct()
                print('customer data >>> ',len(customer_Data))
                for j in customer_Data:
                    dataDict = {}
                    if j.storeID in selected_stores:
                        # print('j data >>> ',j.storeID)
                        dataDict['customerName'] = j.name
                        dataDict['customerContact'] = j.contact
                        # dataDict['customerEmail'] = j.email

                        customerInfo = CustomerShopData.objects.filter(customerID = j,storeID = j.storeID,time_stamp__gte=start_date,time_stamp__lte=end_date)
                        # print('customerInfo >>>>>>>>', customerInfo)
                        if(len(customerInfo) !=0):
                            # amountSum = 0
                            # for j in customerInfo:
                            #     amountSum = amountSum + int(j.amount)
                            dictList = []
                            for stores in selected_stores:
                                sumDict = {}
                                if(stores == j.storeID):
                                    # print('store matched >>>>>')
                                    sumDict['storeID'] = j.storeID
                                    sumDict['totalSum'] = len(customerInfo)
                                    dictList.append(sumDict)
                                else:
                                    # print('store not matched <<<<<')
                                    sumDict['storeID'] = stores
                                    sumDict['totalSum'] = '0'
                                    dictList.append(sumDict)
                                
                            dataDict['storeData'] = dictList

                    count = count + 1
                    customerDict.append(dataDict)

                    print('count >>>>>>>>', count)
                    # print('customerDict >>> ',customerDict)
        return render(request,'admin_template/viewNumberOfVisits.html',{'report_ID':report_ID,'dateRange':date_range,'selected_stores':storeArray,'customerDict':customerDict})
                





            #     for customers in customer_Data:
            #         customerContactArray.append(customers.contact)
            #     print('customer data >>> ',len(customerContactArray))
            # totalCount = len(set(customerContactArray))
            # for contact in list(set(customerContactArray)):
            #     dataDict = {}
            #     customer = CustomerData.objects.filter(time_stamp__gte=start_date,time_stamp__lte=end_date,contact = contact)
                # print('customer >>> ',customer)
                # for j in customer:
                #     if j.storeID in selected_stores:
                #         # print('j data >>> ',j.storeID)
                #         dataDict['customerName'] = j.name
                #         dataDict['customerContact'] = j.contact
                #         # dataDict['customerEmail'] = j.email

                #         customerInfo = CustomerShopData.objects.filter(customerID = j,storeID = j.storeID,time_stamp__gte=start_date,time_stamp__lte=end_date)
                #         # print('customerInfo >>>>>>>>', customerInfo)
                #         if(len(customerInfo) !=0):
                #             amountSum = 0
                #             # for j in customerInfo:
                #             #     amountSum = amountSum + int(j.amount)
                #             dictList = []
                #             for stores in selected_stores:
                #                 sumDict = {}
                #                 if(stores == j.storeID):
                #                     # print('store matched >>>>>')
                #                     sumDict['storeID'] = j.storeID
                #                     sumDict['totalSum'] = len(customerInfo)
                #                     dictList.append(sumDict)
                #                 else:
                #                     # print('store not matched <<<<<')
                #                     sumDict['storeID'] = stores
                #                     sumDict['totalSum'] = '0'
                #                     dictList.append(sumDict)
                                
                #             dataDict['storeData'] = dictList

                #     count = count + 1
                #     customerDict.append(dataDict)

                #     print('count >>>>>>>>', count)
                #     print('customerDict >>> ',customerDict)
            # ========================================================================================================================
        # return render(request,'admin_template/viewNumberOfVisits.html',{'report_ID':report_ID,'dateRange':date_range,'selected_stores':storeArray,'customerDict':customerDict,'totalCount':totalCount})
    



@staff_member_required(login_url="/signup")
def deleteAdminNoOfvisitReport(request,id):
    if request.user.is_superuser:
        if request.method == 'GET':
            del_data = admin_Report_History_for_visit.objects.get(pk=id)
            del_data.delete()
            return HttpResponseRedirect('/report-no-of-visits')
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard')