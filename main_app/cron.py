from django.conf import settings
from datetime import date
import xlwt
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from .models.store_manager_models import *
from django.http import HttpResponse

def my_scheduled_job():
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    ct = date.today()
    start_date = datetime.date(ct.year, ct.month, ct.day) 
    # start_date = datetime.date(2021, 2, 20) 
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

    rows = []
    for i in range(0,len(storeID_list)):
        rows.append((i,storeID_list[i],managerName_list[i],managerContact_list[i],storeName_list[i],totalEntries[i],newEntries[i],oldEntries[i],nullEntries[i],efficiency[i]))
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
    #to_mail = ['rk468335@gmail.com']
    to_mail = ['manoj@theabacusindia.com','sunit@theabacusindia.com','manojk.abacus@gmail.com','siddhant.ratna@yahoo.com','rk468335@gmail.com']
    mail = EmailMessage(f"Store Data Daily Entry Report", f'ABACUS PLATINUM CLUB\n----------------------------------------\nDear admin your report for Date : {d1} is prepared in Xls and CSV file format.', settings.DEFAULT_FROM_EMAIL,to_mail)
    mail.attach(excelFile.strip(), response.getvalue(), 'text/xls')
    mail.attach(csvfile.strip(), response.getvalue(), 'text/csv')
    mail.send()




def my_scheduled_job__supervisors():
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
        # email = str(request.user)
        to_mail = [d1Sup]
        #to_mail = ['manoj@theabacusindia.com','sunit@theabacusindia.com','siddhant.ratna@yahoo.com','rk468335@gmail.com']
        mail = EmailMessage(f"Store Data Daily Entry Report", f'ABACUS PLATINUM CLUB\n----------------------------------------\nDear Supervisor your report for Date : {d1} is prepared in Xls and CSV file format.', settings.DEFAULT_FROM_EMAIL,to_mail)
        mail.attach(excelFile.strip(), response.getvalue(), 'text/xls')
        mail.attach(csvfile.strip(), response.getvalue(), 'text/csv')
        mail.send()
        # ==========================================================================================================
        print('Mail sent successfully to >>>',to_mail)
        # ===============================================================================
