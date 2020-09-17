from django.contrib import admin
from .models import customer,servicecategory,dealcategory,service,stcstatus,leadsource,operationstatus,employeestatus,jobtitle,customercontactnumber,staff,opportunity,suggestion,order,addservices


class customerAdmin(admin.ModelAdmin):
    list_display = ('customername','cr')
    ordering = ('customername',)
    search_fields = ('customername',)

admin.site.register(customer, customerAdmin)

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

class serviceAdmin(admin.ModelAdmin):
    list_display = ('servicename','servicecategory','ncc_id','catalogue_id','nrc','mrc','commission',)
    ordering = ('servicename',)
    search_fields = ('servicename',)

admin.site.register(service, serviceAdmin)

class stcstatusAdmin(admin.ModelAdmin):
    list_display = ('stcstatusname',)
    ordering = ('stcstatusname',)
    search_fields = ('stcstatusname',)

admin.site.register(stcstatus, stcstatusAdmin)

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

admin.site.register(opportunity, opportunityAdmin)


class suggestionAdmin(admin.ModelAdmin):
    list_display = ('requestor','requesttext','completion','creationdate',)
    ordering = ('creationdate',)
    search_fields = ('requesttext',)

admin.site.register(suggestion, suggestionAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display = ('orderno','opportunity','service','creationdate','id')
    ordering = ('creationdate',)
    search_fields = ('orderno',)

admin.site.register(order, orderAdmin)

class addservicesAdmin(admin.ModelAdmin):
    list_display = ('opportunity','service','noofservices',)
    ordering = ('opportunity',)
    search_fields = ('opportunity',)

admin.site.register(addservices, addservicesAdmin)
