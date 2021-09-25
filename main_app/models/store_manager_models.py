from django.db import models
import datetime

# Store details model
# priority entry 2 : object of tier model
class store_detail(models.Model):
    storeID = models.CharField(max_length=150,unique=True, null=False)
    store_name = models.CharField(max_length=80,unique=True)
    store_location = models.CharField(max_length=30)
    store_town = models.CharField(max_length=30)
    store_city = models.CharField(max_length=30)
    store_state = models.CharField(max_length=30)
    store_category = models.CharField(max_length=100)
    store_subcategory = models.CharField(max_length=100)
    statusflag = models.BooleanField(default=1)
    # store_assigned_Status = models.CharField(max_length=10,default='NA')
    time_stamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.store_name} - {self.store_location}"


class CustomerData(models.Model):
    storeID = models.CharField(max_length=150) 
    name = models.CharField(max_length=150,default='NA')
    contact = models.CharField(max_length=10, blank=False, null=False)
    email = models.CharField(max_length=100,default='NA')
    DOB = models.CharField(max_length=10, default='NA')
    gender = models.CharField(max_length=6,default='NA')
    DOM = models.CharField(max_length=10,default='NA')
    entry_type = models.CharField(max_length=10)
    emailSubscription = models.CharField(max_length=6,default='True')
    time_stamp = models.DateTimeField(auto_now_add=True)


class CustomerShopData(models.Model):
    storeID = models.CharField(max_length=150)
    customerID = models.ForeignKey(CustomerData, on_delete=models.CASCADE)
    invoice = models.CharField(max_length=100)
    amount = models.FloatField()
    time_stamp = models.DateTimeField(auto_now_add=True)

class CustomerOnboardData(models.Model):
    storeID = models.CharField(max_length=150)
    customerID = models.ForeignKey(CustomerData, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    tierRuleNo = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True)


# Store manager details {[contact & email] should be unique}
class store_manager(models.Model):
    store = models.ForeignKey(store_detail, on_delete=models.CASCADE)
    manager_image = models.ImageField(upload_to='SuperVisorImages/')
    manager_name = models.CharField(max_length=50)
    manager_contact = models.CharField(max_length=10)
    user_unique_id = models.CharField(max_length=30)
    manager_email = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    manager_password = models.CharField(max_length=30)
    DOB = models.CharField(max_length=12, default='01-01-2000', blank=True, null=True)
    entry_type = models.CharField(max_length=12)
    time_stamp = models.DateTimeField(auto_now_add=True)


    # def __str__(self):
    #     return f"{self.manager_name} - {str(self.manager_contact)}"
    

# Store supervisor details
class Store_supervisor(models.Model):
    # store = models.ForeignKey(store_detail, on_delete=models.CASCADE,default=0)
    supervisor_name = models.CharField(max_length=50,default='NA')
    supervisor_contact = models.CharField(max_length=12,default='NA')
    supervisor_email = models.CharField(max_length=100,default='NA')
    supervisor_gender = models.CharField(max_length=30,default='NA')
    time_stamp = models.DateTimeField(auto_now_add=True)


    


class tier_individual(models.Model):
    tierType = models.CharField(max_length=10)
    tierRuleNo = models.IntegerField()
    store_ID = models.CharField(max_length=30)
    shop_start_amt = models.IntegerField()
    shop_end_amt = models.IntegerField()
    time_period = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.tierType} - {str(self.tierRuleNo)}"

class tier_collective(models.Model):
    tierType = models.CharField(max_length=10)
    tierRuleNo = models.IntegerField()
    shop_start_amt = models.IntegerField()
    shop_end_amt = models.IntegerField()
    time_period = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True)


# Product Category model
class category(models.Model):
    category = models.CharField(unique=True, max_length=100)
    sub_category = models.TextField(default='NA')
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.sub_category}"


class CampaignEmail(models.Model):
    campaignName = models.CharField(unique=True, max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.campaignName
        
class EmailSubCampaign(models.Model):
    CampaignName = models.ForeignKey(CampaignEmail, on_delete=models.CASCADE)
    allEmails = models.TextField(default='NA')
    text = models.TextField(default='NA')
    time_stamp = models.DateTimeField(auto_now_add=True)






class CampaignSms(models.Model):
    campaignName = models.CharField(unique=True, max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.campaignName

class SmsSubCampaign(models.Model):
    CampaignName = models.ForeignKey(CampaignSms, on_delete=models.CASCADE)
    allsms = models.TextField(default='NA')
    text = models.TextField(default='NA')
    time_stamp = models.DateTimeField(auto_now_add=True)


# ##########################################################################################################
class scheduleEmailList(models.Model):
    emailList = models.TextField(default='NA')
    # emailSubject = models.CharField(max_length=50,default='NA')
    emailText = models.TextField(default='NA')
# ##########################################################################################################
class scheduleSMSList(models.Model):
    emailList = models.TextField(default='NA')
    # emailSubject = models.CharField(max_length=50,default='NA')
    emailText = models.TextField(default='NA')
# ##########################################################################################################
class ApiKey(models.Model):
    Key = models.CharField(unique=True, max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #     return self.Key

# ##########################################################################################################
class supervisorDetails(models.Model):
    supervisor_image = models.ImageField(upload_to='SuperVisorImages/')
    supervisor_name = models.CharField(max_length=50)
    supervisor_contact = models.CharField(max_length=10)
    supervisor_unique_id = models.CharField(max_length=30)
    supervisor_email = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    supervisor_password = models.CharField(max_length=30)
    store_array = models.CharField(max_length=150)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.supervisor_name


# ##########################################################################################################
class storeGroups(models.Model):
    groupName = models.CharField(max_length=50,unique=True)
    groupID = models.CharField(max_length=30,unique=True)
    groupDescription = models.TextField()
    store_array = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)




class groupReport(models.Model):
    storeGroup = models.ForeignKey(storeGroups, on_delete=models.CASCADE)
    reportID = models.CharField(max_length=50,unique=True)
    method = models.CharField(max_length=30)
    selected_Conditions = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reportID



class shareReport(models.Model):
    report_FK = models.ForeignKey(groupReport, on_delete=models.CASCADE)
    supervisorFK = models.ForeignKey(supervisorDetails, on_delete=models.CASCADE)
    supervisor_email = models.CharField(max_length=50,unique=True)
    time_stamp = models.DateTimeField(auto_now_add=True)


class store_Shared_Record_History(models.Model):
    reportID = models.ForeignKey(groupReport, on_delete=models.CASCADE)
    supervisorID = models.ForeignKey(supervisorDetails, on_delete=models.CASCADE)
    supervisor_email = models.CharField(max_length=50)
    time_stamp = models.DateTimeField(auto_now_add=True)



class supervisor_noOfVisit_Report_History(models.Model):
    supervisor_FK = models.ForeignKey(supervisorDetails, on_delete=models.CASCADE)
    reportID = models.CharField(max_length=50,unique=True)
    selected_stores = models.TextField()
    dateRange = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

class supervisor_amountOfPurchase_Report_History(models.Model):
    supervisor_FK = models.ForeignKey(supervisorDetails, on_delete=models.CASCADE)
    reportID = models.CharField(max_length=50,unique=True)
    selected_stores = models.TextField()
    dateRange = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)



class supervisor_Report_History_for_amount(models.Model):
    supervisor_FK = models.ForeignKey(supervisorDetails, on_delete=models.CASCADE)
    reportID = models.CharField(max_length=50,unique=True)
    selected_stores = models.TextField()
    dateRange = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

class supervisor_Report_History_for_visit(models.Model):
    supervisor_FK = models.ForeignKey(supervisorDetails, on_delete=models.CASCADE)
    reportID = models.CharField(max_length=50,unique=True)
    selected_stores = models.TextField()
    dateRange = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)



class admin_Report_History_for_amount(models.Model):
    reportID = models.CharField(max_length=50,unique=True)
    selected_stores = models.TextField()
    dateRange = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

class admin_Report_History_for_visit(models.Model):
    reportID = models.CharField(max_length=50,unique=True)
    selected_stores = models.TextField()
    dateRange = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)