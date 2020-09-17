
from django.db import models
import datetime
from datetime import timedelta
from datetime import date
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import  get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count , Sum , Avg

# Create your models here.

def defaultstatus():
    return operationstatus.objects.get(id=1)

def defaultstatusorder():
    return operationstatus.objects.get(id=4)

def defaulemployeetstatus():
    return employeestatus.objects.get(id=1)


def defaultdealcategory():
    return dealcategory.objects.get(id=1)

class customer(models.Model):
    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_customers',verbose_name ='Creator')
    customername = models.CharField("Customer Name",max_length=100,null=True)
    cr = models.IntegerField(null = True,blank = True, unique=True)
    activity  = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=40,blank=True,null=True)
    no_of_employees = models.IntegerField(null = True,blank = True)
    branches = models.IntegerField(null = True,blank = True)
    district  = models.CharField(max_length = 100,blank = True)
    street  = models.CharField(max_length=100,blank=True)
    phone = models.IntegerField(null = True,blank = True)
    email = models.EmailField(null = True,blank = True)
    current_services = models.CharField(max_length=1000,blank=True)
    notes = models.CharField(max_length=1000,blank=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)

    def __str__(self):
        return self.customername

    def get_absolute_url(self):
        return reverse('customerdetail',kwargs={'pk':self.pk})

class suggestion(models.Model):
    statuslist = (
            ('open', 'Open'),
            ('closed', 'Closed'),
            )
    requestor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_requests')
    requesttext = models.TextField("Request",null=True,unique=True)
    completion = models.BooleanField(default=False)
    status = models.CharField("Status",max_length=1000,blank=True,choices=statuslist,default='open')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)

    class Meta:
        verbose_name ='Suggesion'
        verbose_name_plural ='Suggestions'

    def __str__(self):
        return self.requesttext

    def get_absolute_url(self):
        return reverse('suggestiondetail',kwargs={'pk':self.pk})



class servicecategory(models.Model):
    servicecategoryname = models.CharField("Service Category",max_length=100,null=True)

    class Meta:
        verbose_name ='Service Category'
        verbose_name_plural ='Service Categorys'

    def __str__(self):
        return self.servicecategoryname

class dealcategory(models.Model):
    dealcategoryname = models.CharField("Deal Category Name",max_length=100,null=True)

    class Meta:
        verbose_name ='Deal Category'
        verbose_name_plural ='Deal Categorys'

    def __str__(self):
        return self.dealcategoryname

class service(models.Model):
    servicename = models.CharField("Service",max_length=100,null=True)
    servicecategory = models.ForeignKey(servicecategory,blank=True,on_delete=models.CASCADE,related_name='category_services',verbose_name ='Service Category')
    ncc_id = models.IntegerField(unique=True)
    catalogue_id = models.IntegerField(unique=True)
    nrc = models.IntegerField()
    mrc = models.IntegerField()
    commission = models.IntegerField()

    def get_absolute_url(self):
        return reverse('servicedetail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.servicename

class stcstatus(models.Model):
    stcstatusname = models.CharField("STC Status",max_length=100,null=True)

    class Meta:
        verbose_name ='STC Status'
        verbose_name_plural ='STC Status'


    def __str__(self):
        return self.stcstatusname

class leadsource(models.Model):
    leadsourcename = models.CharField("Lead Source",max_length=100,null=True)

    class Meta:
        verbose_name ='Lead Source'
        verbose_name_plural ='Lead Source'

    def __str__(self):
        return self.leadsourcename

class operationstatus(models.Model):
    operationstatusname = models.CharField("Operation_Status",max_length=100,null=True)

    class Meta:
        verbose_name ='Operation Status'
        verbose_name_plural ='Operation Status'

    def __str__(self):
        return self.operationstatusname

class employeestatus(models.Model):
    employeestatusname = models.CharField("Employee Status",max_length=100,null=True)

    class Meta:
        verbose_name ='Employee  Status'
        verbose_name_plural ='Employee Status'

    def __str__(self):
        return self.employeestatusname

class jobtitle(models.Model):
    jobtitlename = models.CharField("Job Title",max_length=100,null=True)

    class Meta:
        verbose_name ='Job Title'
        verbose_name_plural ='Job Titles'

    def __str__(self):
        return self.jobtitlename

class customercontactnumber(models.Model):
    customercontactnumbername = models.CharField("Customer Contact No",max_length=100,null=True)
    mobile1 = models.IntegerField(null = True,blank = True)
    mobile2 = models.IntegerField(null = True,blank = True)
    email = models.EmailField(null = True,blank = True)

    class Meta:
        verbose_name ='Customer Contact Number'
        verbose_name_plural ='Customer Contact Numbers'

    def __str__(self):
        return self.customercontactnumbername

class staff(models.Model):
    staffname = models.CharField("Name Of Staff",max_length=100,null=True,unique=True)
    staff_id = models.IntegerField("Staff_ID",unique=True)
    joindate = models.DateField("Join Date",null=True,blank=True)
    employeestatus = models.ForeignKey(employeestatus,blank=True,on_delete=models.CASCADE,related_name='employeestatus_staff',verbose_name ='Employee Status',default=defaulemployeetstatus)
    employeejobtitle = models.ForeignKey(jobtitle,blank=True,on_delete=models.CASCADE,related_name='jobtitle_staff',verbose_name ='Job Title')
    updatedate = models.DateTimeField("Update Date",auto_now=True)

    class Meta:
        verbose_name ='Staff'
        verbose_name_plural ='Staff'

    def __str__(self):
        return self.staffname

    def get_absolute_url(self):
        return reverse('staffdetail',kwargs={'pk':self.pk})

class opportunity(models.Model):
    lms = models.IntegerField("LMS No",unique=True)
    opportunityno = models.IntegerField("Opportunity No",unique=True)
    creationdate = models.DateTimeField("Creation Date",default=timezone.now())
    salesman = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='salesman_opportunities',verbose_name ='Sales Man')
    employeejobtitle = models.CharField("Job Title",max_length=100,null=True,default='Sales Executive') #def
    customer = models.ForeignKey(customer,blank=True,on_delete=models.CASCADE,related_name='customer_opportunities',verbose_name ='Customer')
    status = models.ForeignKey(operationstatus,blank=True,on_delete=models.CASCADE,related_name='status_opportunities',verbose_name ='Status',null=True,default=defaultstatus)
    updatedate = models.DateTimeField("Update Date",auto_now=True)
    authorized = models.CharField("Authorized Person",max_length=100,null=True,blank=True)
    totalnrc = models.IntegerField("Total NRC",default=0)
    totalmrc = models.IntegerField("Total MRC",default=0)
    coordinates = models.CharField("Coordinates",max_length=100,null=True,blank=True)
    source = models.ForeignKey(leadsource,blank=True,on_delete=models.CASCADE,related_name='source_opportunities',verbose_name ='Source',null=True)
    class Meta:
        verbose_name ='Opportunity'
        verbose_name_plural ='Opportunitys'

    def __str__(self):
        return str(self.opportunityno)

    # @receiver(post_save, sender=addservices)
    # def totalvalues(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    def save(self, *args, **kwargs):

        if not self.opportunityno:
            lastno = opportunity.objects.filter(opportunityno__startswith=datetime.datetime.today().strftime('%Y')).count()
            if lastno:
                lastno2 = lastno + 1
                if lastno2 <= 9:
                    self.opportunityno = int(str(datetime.datetime.today().strftime('%Y')) + '000' + str(lastno2))
                if lastno2  > 9 and lastno2 <= 99:
                    self.opportunityno = int(str(datetime.datetime.today().strftime('%Y')) + '00' + str(lastno2))
                if lastno2  > 99 and lastno2 <= 999:
                    self.opportunityno = int(str(datetime.datetime.today().strftime('%Y')) + '0' + str(lastno2))
                if lastno2  > 999 :
                    self.opportunityno = int(str(datetime.datetime.today().strftime('%Y')) + str(lastno2))
            else:
                self.opportunityno = int(str(datetime.datetime.today().strftime('%Y')) + '000' + str(1))


        opportunityorders =self.opportunity_orders.all()
        opportunityorderspost =self.opportunity_orders.filter(orderstatus='post').all()
        opportunityservices = self.opportunity_addservices.all()

        if opportunityorders:
            self.status = operationstatus.objects.get(id=7)

        if opportunityorderspost:
            self.status = operationstatus.objects.get(id=12)



        if opportunityservices:
            mrcsumoo = opportunityservices.aggregate(Sum('totalmrc'))
            mrcsumo = mrcsumoo['totalmrc__sum']
            self.totalmrc = mrcsumo
        super(opportunity, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('opportunitydetail',kwargs={'pk':self.pk})

# opportunity-Services

class addservices(models.Model):
    serviceowner = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='salesman_addservices',verbose_name ='Service Owner')
    opportunity = models.ForeignKey(opportunity,on_delete=models.CASCADE,related_name='opportunity_addservices',verbose_name ='Opportunity')
    service = models.ForeignKey(service,blank=True,on_delete=models.CASCADE,related_name='service_opportunities',verbose_name ='Service')
    noofservices = models.IntegerField("No Of Services",default=1)
    servicecategory = models.CharField("Service Category",max_length=100,null=True)
    totalnrc = models.IntegerField("Total NRC",default=0)
    totalmrc = models.IntegerField("Total MRC",default=0)
    createdservices = models.IntegerField("Created Services",default=0)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)


    class Meta:
        verbose_name ='Add Service'
        verbose_name_plural ='Add Services'

    def save(self, *args, **kwargs):
         obj1 = get_object_or_404(service,servicename = self.service)
         obj2 = order.objects.filter(service = self.service).filter(opportunity=self.opportunity).count()
         self.servicecategory = str(obj1.servicecategory)
         self.totalnrc = obj1.nrc * self.noofservices
         self.totalmrc = obj1.mrc * self.noofservices
         if obj2:
             self.createdservices = obj2
         super(addservices, self).save(*args, **kwargs)
# Orders

class order(models.Model):
    dealcategory = (
            ('n', 'New'),
            ('u', 'Upgrade'),
            ('d', 'Downgrade'),
        )
    orderstatuslist = (
            ('open', 'Open'),
            ('held', 'Held'),
            ('finger', 'FingerPrint'),
            ('post', 'Post'),
            ('cancel', 'Cancel'),
        )
    opportunity = models.ForeignKey(opportunity,on_delete=models.CASCADE,related_name='opportunity_orders',verbose_name ='Opportunity')
    dealcategory = models.CharField("Deal Category",max_length=1, choices=dealcategory)
    addservices = models.ForeignKey(addservices,on_delete=models.CASCADE,related_name='addservices_orders',verbose_name ='Services')
    orderno= models.IntegerField("Order No",unique=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    accountno = models.IntegerField("Account No")
    serviceno = models.IntegerField("Service No",null = True,blank = True)
    imei = models.IntegerField("IMEI",null = True,blank = True)
    service = models.ForeignKey(service,blank=True,on_delete=models.CASCADE,related_name='service_orders',verbose_name ='Service')
    servicecategory = models.CharField("Service Category",max_length=100,null=True) #def
    status = models.ForeignKey(operationstatus,blank=True,on_delete=models.CASCADE,related_name='status_orders',verbose_name ='Status',null=True,default=defaultstatusorder)
    operationexecutive = models.ForeignKey(User,on_delete=models.CASCADE,related_name='executive_orders',verbose_name ='Operation Executive')
    orderstatus = models.CharField("Order Status",max_length=12, choices=orderstatuslist,default="open")
    nrc = models.IntegerField("NRC")
    mrc = models.IntegerField("MRC")
    updatedate = models.DateTimeField("Update Date",auto_now=True)
    activationdate = models.DateField("Activation Date",blank=True,null=True)
    cabinetno = models.CharField("Cabinet No",max_length=100,null=True)
    circuitno = models.CharField("Circuit No",max_length=100,null=True)
    granite = models.CharField("Granite",max_length=100,null=True)


    class Meta:
        verbose_name ='Order'
        verbose_name_plural ='Orders'

    def save(self, *args, **kwargs):
         obj1 =  get_object_or_404(service,servicename = self.service)
         self.servicecategory = str(obj1.servicecategory)
         self.nrc = obj1.nrc
         self.mrc = obj1.mrc

         super(order, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('orderdetail',kwargs={'pk':self.pk})
