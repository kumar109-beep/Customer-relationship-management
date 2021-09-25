from django.contrib import admin
from main_app.models.login_models import registration
from main_app.models.store_manager_models import *


@admin.register(registration)
class registered_user(admin.ModelAdmin):
    list_display = ('id', 'user', 'contact', 'storeID',
                    'entry_type', 'password_saved')


@admin.register(ApiKey)
class Api_Keys(admin.ModelAdmin):
    list_display = ('id', 'Key')


@admin.register(CustomerData)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'storeID', 'name', 'contact','DOM','DOB',
                    'email', 'gender', 'time_stamp')


@admin.register(CustomerShopData)
class Profiles(admin.ModelAdmin):
    list_display = ('invoice', 'storeID','amount', 'time_stamp')

@admin.register(CustomerOnboardData)
class CustomerOnboardData(admin.ModelAdmin):
    list_display = ('customerID', 'storeID','total_amount','tierRuleNo', 'time_stamp')


@admin.register(tier_individual)
class tier_individual(admin.ModelAdmin):
    list_display = ('id', 'store_ID', 'shop_start_amt', 'shop_end_amt',
                    'time_period', 'time_stamp')

@admin.register(tier_collective)
class tier_collective(admin.ModelAdmin):
    list_display = ('id', 'shop_start_amt', 'shop_end_amt',
                    'time_period', 'time_stamp')


@admin.register(category)
class product_category(admin.ModelAdmin):
    list_display = ('id', 'category', 'time_stamp')




@admin.register(store_detail)
class store(admin.ModelAdmin):
    list_display = ('id','storeID', 'store_name', 'store_location', 'store_town',
                    'store_city', 'store_state', 'store_category', 'store_subcategory', 'time_stamp')


@admin.register(store_manager)
class store_manager(admin.ModelAdmin):
    list_display = ('id', 'manager_name', 'manager_contact',
                    'manager_email', 'gender', 'manager_password', 'time_stamp')

@admin.register(supervisorDetails)
class supervisorDetails(admin.ModelAdmin):
    list_display = ('id', 'supervisor_name', 'supervisor_contact', 'supervisor_email', 'supervisor_password','store_array', 'time_stamp')

@admin.register(Store_supervisor)
class store_supervisor(admin.ModelAdmin):
    list_display = ('id', 'supervisor_name', 'supervisor_contact', 'supervisor_email',
                    'supervisor_gender', 'time_stamp')



@admin.register(CampaignEmail)
class CampaignEmail(admin.ModelAdmin):
    list_display = ('id','campaignName',)


@admin.register(CampaignSms)
class CampaignSms(admin.ModelAdmin):
    list_display = ('id','campaignName',)


@admin.register(EmailSubCampaign)
class EmailSubCampaign(admin.ModelAdmin):
    list_display = ('id','CampaignName','time_stamp')


@admin.register(SmsSubCampaign)
class SmsSubCampaign(admin.ModelAdmin):
    list_display = ('id','CampaignName','time_stamp')


@admin.register(scheduleEmailList)
class scheduleEmailList(admin.ModelAdmin):
    list_display = ('id','emailList','emailText')

@admin.register(scheduleSMSList)
class scheduleSMSList(admin.ModelAdmin):
    list_display = ('id','emailList','emailText')

@admin.register(storeGroups)
class storeGroups(admin.ModelAdmin):
    list_display = ('id','groupName','groupID','groupDescription','store_array','time_stamp')

@admin.register(groupReport)
class groupReport(admin.ModelAdmin):
    list_display = ('id','storeGroup','reportID','method','selected_Conditions','time_stamp')


@admin.register(store_Shared_Record_History)
class store_Shared_Record_History(admin.ModelAdmin):
    list_display = ('id','reportID','supervisorID','supervisor_email','time_stamp')



@admin.register(supervisor_noOfVisit_Report_History)
class supervisor_noOfVisit_Report_History(admin.ModelAdmin):
    list_display = ('id','supervisor_FK','reportID','selected_stores','dateRange','time_stamp')


@admin.register(supervisor_Report_History_for_amount)
class supervisor_Report_History_for_amount(admin.ModelAdmin):
    list_display = ('id','supervisor_FK','reportID','selected_stores','dateRange','time_stamp')


@admin.register(admin_Report_History_for_visit)
class admin_Report_History_for_visit(admin.ModelAdmin):
    list_display = ('id','reportID','selected_stores','dateRange','time_stamp')


@admin.register(admin_Report_History_for_amount)
class admin_Report_History_for_amount(admin.ModelAdmin):
    list_display = ('id','reportID','selected_stores','dateRange','time_stamp')