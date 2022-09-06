from django.contrib import admin
from .models import customer,fcustomer,servicecategory,dealcategory,service,stcstatus,leadsource,operationstatus,employeestatus,jobtitle,customercontactnumber,staff,opportunity,suggestion,order,addservices,invoices,expensecategory,yearslist,expenses,partner,fservice,fastdatad,dealnotes,finvoice,finvoiceitem,fpayment,accounts,activity,activityrecord,orderimport,provider,Action
from import_export.admin import ImportExportModelAdmin

@admin.register(customer)
class customerAdmin(ImportExportModelAdmin):
    list_display = ('customername','cr')
    ordering = ('customername',)
    search_fields = ('customername','cr')

@admin.register(stcstatus)
class stcstatusAdmin(ImportExportModelAdmin):

    list_display = ('stcstatusname',)
    ordering = ('stcstatusname',)
    search_fields = ('stcstatusname',)

class fcustomerAdmin(admin.ModelAdmin):
    list_display = ('customername','cr')
    ordering = ('customername',)
    search_fields = ('customername','cr')
admin.site.register(fcustomer, fcustomerAdmin)

class servicecategoryAdmin(admin.ModelAdmin):
    list_display = ('servicecategoryname',)
    ordering = ('servicecategoryname',)
    search_fields = ('servicecategoryname',)

admin.site.register(servicecategory, servicecategoryAdmin)

class dealcategoryAdmin(admin.ModelAdmin):
    list_display = ('dealcategoryname','id')
    ordering = ('dealcategoryname',)
    search_fields = ('dealcategoryname',)

admin.site.register(dealcategory, dealcategoryAdmin)



@admin.register(service)
class serviceAdmin(ImportExportModelAdmin):
    list_display = ('servicename',)
    ordering = ('servicename',)
    search_fields = ('servicename',)

class accountsAdmin(admin.ModelAdmin):
    list_display = ('accountno','creationdate')
    ordering = ('accountno',)
    search_fields = ('accountno',)

admin.site.register(accounts, accountsAdmin)







class leadsourceAdmin(admin.ModelAdmin):
    list_display = ('leadsourcename',)
    ordering = ('leadsourcename',)
    search_fields = ('leadsourcename',)

admin.site.register(leadsource, leadsourceAdmin)

class operationstatusAdmin(admin.ModelAdmin):
    list_display = ('operationstatusname','id',)
    ordering = ('operationstatusname',)
    search_fields = ('operationstatusname',)

admin.site.register(operationstatus, operationstatusAdmin)

class employeestatusAdmin(admin.ModelAdmin):
    list_display = ('employeestatusname',)
    ordering = ('employeestatusname',)
    search_fields = ('employeestatusname',)

admin.site.register(employeestatus, employeestatusAdmin)

class jobtitleAdmin(admin.ModelAdmin):
    list_display = ('jobtitlename',)
    ordering = ('jobtitlename',)
    search_fields = ('jobtitlename',)

admin.site.register(jobtitle, jobtitleAdmin)


class customercontactnumberAdmin(admin.ModelAdmin):
    list_display = ('customercontactnumbername','mobile1','mobile2','email',)
    ordering = ('customercontactnumbername',)
    search_fields = ('customercontactnumbername',)

admin.site.register(customercontactnumber, customercontactnumberAdmin)

class staffAdmin(admin.ModelAdmin):
    list_display = ('staffname','staff_id','joindate','employeestatus','employeejobtitle',)
    ordering = ('staffname',)
    search_fields = ('staffname',)

admin.site.register(staff, staffAdmin)



class opportunityAdmin(admin.ModelAdmin):
    list_display = ('customer','lms','opportunityno','salesman','creationdate')
    ordering = ('opportunityno',)
    search_fields = ('opportunityno',)
    list_filter = ('salesman','status',)
    date_hierarchy = 'creationdate'
    raw_id_fields = ('salesman','customer',)
admin.site.register(opportunity, opportunityAdmin)



class suggestionAdmin(admin.ModelAdmin):
    list_display = ('requestor','requesttext','completion','creationdate',)
    ordering = ('creationdate',)
    search_fields = ('requesttext',)

admin.site.register(suggestion, suggestionAdmin)

# class orderAdmin(admin.ModelAdmin):
#     list_display = ('orderno','opportunity','service','creationdate','activationdate','id','mrc','accountno',)
#     ordering = ('creationdate',)
#     search_fields = ('orderno','accountno','opportunity',)

# admin.site.register(order, orderAdmin)


@admin.register(order)
class orderAdmin(ImportExportModelAdmin):

    list_display = ('orderno','opportunity','service','serviceno','creationdate','activationdate','id','mrc','accountno',)
    ordering = ('creationdate',)
    search_fields = ('orderno',)




class addservicesAdmin(admin.ModelAdmin):
    list_display = ('opportunity','service','noofservices','id')
    ordering = ('opportunity',)
    search_fields = ('opportunity',)

admin.site.register(addservices, addservicesAdmin)

#new

class invoicesAdmin(admin.ModelAdmin):
    list_display = ('invoice_no','invoicedate',)
    ordering = ('invoicedate',)
    search_fields = ('invoice_no',)

admin.site.register(invoices, invoicesAdmin)

class expensecategoryAdmin(admin.ModelAdmin):
    list_display = ('expensecategoryname',)
    ordering = ('expensecategoryname',)
    search_fields = ('expensecategoryname',)

admin.site.register(expensecategory, expensecategoryAdmin)

class yearslistAdmin(admin.ModelAdmin):
    list_display = ('yeardetail',)
    ordering = ('yeardetail',)
    search_fields = ('yeardetail',)

admin.site.register(yearslist, yearslistAdmin)



class expensesAdmin(admin.ModelAdmin):
    list_display = ('amount','Category','year','month',)
    ordering = ('year',)
    search_fields = ('year',)

admin.site.register(expenses, expensesAdmin)

class partnerAdmin(admin.ModelAdmin):
    list_display = ('partnername','contractstart','contractend','contractstatus','id',)
    ordering = ('partnername',)
    search_fields = ('partnername',)

admin.site.register(partner, partnerAdmin)

class fastdatadAdmin(admin.ModelAdmin):
    list_display = ('dealno','customer','service',)
    ordering = ('customer',)
    search_fields = ('customer',)

admin.site.register(fastdatad, fastdatadAdmin)

class fserviceAdmin(admin.ModelAdmin):
    list_display = ('servicename',)
    ordering = ('servicename',)
    search_fields = ('servicename',)

admin.site.register(fservice, fserviceAdmin)

class dealnotesAdmin(admin.ModelAdmin):
    list_display = ('note',)
    ordering = ('note',)
    search_fields = ('note',)

admin.site.register(dealnotes, dealnotesAdmin)

class finvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoiceno',)
    ordering = ('invoiceno',)
    search_fields = ('invoiceno',)

admin.site.register(finvoice, finvoiceAdmin)

class finvoiceitemAdmin(admin.ModelAdmin):
    list_display = ('invoiceno','deal',)
    ordering = ('invoiceno',)
    search_fields = ('invoiceno',)

admin.site.register(finvoiceitem, finvoiceitemAdmin)

class fpaymentAdmin(admin.ModelAdmin):
    list_display = ('payment','paymentdate','invoiceno')
    ordering = ('payment',)
    search_fields = ('payment',)

admin.site.register(fpayment, fpaymentAdmin)

class activityAdmin(admin.ModelAdmin):
    list_display = ('activityname',)
    ordering = ('activityname',)
    search_fields = ('activityname',)

admin.site.register(activity, activityAdmin)

class activityrecordAdmin(admin.ModelAdmin):
    list_display = ('activity',)
    ordering = ('activity',)
    search_fields = ('activity',)

admin.site.register(activityrecord, activityrecordAdmin)


@admin.register(orderimport)
class orderimportAdmin(ImportExportModelAdmin):

    list_display = ('orderno',)
    ordering = ('orderno',)
    search_fields = ('orderno',)

@admin.register(provider)
class providerAdmin(ImportExportModelAdmin):

    list_display = ('providername',)
    ordering = ('providername',)
    search_fields = ('providername',)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)
