
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
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

def defaultstatus():
    return operationstatus.objects.get(id=1)

def defaultpartner():
    return partner.objects.get(id=1)

def defaultstatusorder():
    return operationstatus.objects.get(id=4)

def defaulemployeetstatus():
    return employeestatus.objects.get(id=1)


def defaultdealcategory():
    return dealcategory.objects.get(id=1)


class company(models.Model):
    companyname = models.CharField("Company",max_length=100,unique=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)

    class Meta:
        verbose_name ='Company'
        verbose_name_plural ='Companies'

    def __str__(self):
        return self.companyname

class provider(models.Model):
    providername = models.CharField("Company",max_length=100,unique=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)

    class Meta:
        verbose_name ='Provider'
        verbose_name_plural ='Providers'

    def __str__(self):
        return self.providername

class project(models.Model):
    projectname = models.CharField("Company",max_length=100)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    company=models.ForeignKey(company,on_delete=models.CASCADE,related_name='company_projects',verbose_name ='Project')


    class Meta:
        verbose_name ='Project'
        verbose_name_plural ='Projects'
        unique_together = ['projectname', 'company']

    def __str__(self):
        return self.projectname

class leadsource(models.Model):
    leadsourcename = models.CharField("Lead Source",max_length=100,null=True)

    class Meta:
        verbose_name ='Lead Source'
        verbose_name_plural ='Lead Source'

    def __str__(self):
        return self.leadsourcename

class customer(models.Model):
    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_customers',verbose_name ='Creator')
    assignedto = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_assignedcustomers',verbose_name ='Assigned To')
    customername = models.CharField("Customer Name",max_length=100,null=True)
    cr = models.IntegerField(null = True,blank = True, unique=True)
    source = models.ForeignKey(leadsource,blank=True,on_delete=models.CASCADE,related_name='source_customers',verbose_name ='Source',null=True)
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

    class Meta:
        ordering = ('customername',)

    def __str__(self):
        return self.customername

    def get_absolute_url(self):
        return reverse('customerdetail',kwargs={'pk':self.pk})

class fcustomer(models.Model):
    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_fcustomers',verbose_name ='Creator')
    customername = models.CharField("Customer Name",max_length=100,null=True)
    cr = models.IntegerField(null = True,blank = True, unique=True)
    activity  = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=40,blank=True,null=True)
    phone = models.IntegerField(null = True,blank = True)
    email = models.EmailField(null = True,blank = True)
    notes = models.CharField(max_length=1000,blank=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)


    def __str__(self):
        return self.customername

    def get_absolute_url(self):
        return reverse('fcustomerdetail',kwargs={'pk':self.pk})

class partner(models.Model):

    partnername = models.CharField("Partner",max_length=50)
    contractstart = models.DateTimeField("Contract Start Date")
    contractend = models.DateTimeField("Contract End Date")
    contractstatus =models.BooleanField("Status")
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)

    class Meta:
        verbose_name ='Partner'
        verbose_name_plural ='Partners'

    def __str__(self):
        return self.partnername

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
    ncc_id = models.CharField(unique=True,max_length=25)
    catalogue_id = models.CharField(unique=True,max_length=25)
    nrc = models.IntegerField()
    mrc = models.IntegerField()
    commission = models.IntegerField()

    class Meta:
        ordering = ('servicename',)

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
    lms = models.CharField("LMS No",unique=True,max_length=20)

    opportunityno = models.IntegerField("Opportunity No",unique=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    opportunitydate = models.DateField("Open Date",blank=True,null=True)
    salesman = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='salesman_opportunities',verbose_name ='Sales Man')
    employeejobtitle = models.CharField("Job Title",max_length=100,null=True,default='Sales Executive') #def
    customer = models.ForeignKey(customer,blank=True,on_delete=models.CASCADE,related_name='customer_opportunities',verbose_name ='Customer')
    status = models.ForeignKey(operationstatus,blank=True,on_delete=models.CASCADE,related_name='status_opportunities',verbose_name ='Status',null=True,default=defaultstatus)
    updatedate = models.DateTimeField("Update Date",auto_now=True)
    authorized = models.CharField("Authorized Person",max_length=100,null=True,blank=True)
    totalnrc = models.IntegerField("Total NRC",default=0)
    totalmrc = models.IntegerField("Total MRC",default=0)
    ordersmrc = models.IntegerField("Orders MRC",default=0)
    revenue1 = models.IntegerField("Revenue Before Post",default=0)
    coordinates = models.CharField("Coordinates",max_length=100,null=True,blank=True)
    source = models.ForeignKey(leadsource,blank=True,on_delete=models.CASCADE,related_name='source_opportunities',verbose_name ='Source',null=True)
    expectedclosingdate = models.DateField("Expected Closing Date",null=True,blank=True) #new
    note = models.TextField("Note",blank=True,null=True)

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
            oppcount = opportunity.objects.filter(opportunityno__startswith=datetime.datetime.today().strftime('%Y')).count()
            if oppcount:
                lastopp = opportunity.objects.last()
                newno = lastopp.opportunityno + 1
                self.opportunityno = newno

            else:
                self.opportunityno = int(str(datetime.datetime.today().strftime('%Y')) + '000' + str(1))

        opportunityorders =self.opportunity_orders.all()


        opportunityorderspost =self.opportunity_orders.filter(orderstatus='post').all()
        opportunityservices = self.opportunity_addservices.all()


        if opportunityorders:
            self.status = operationstatus.objects.get(id=7)
            self.ordersmrc  = opportunityorders.aggregate(Sum('mrc'))['mrc__sum']

        if opportunityorderspost:
            self.status = operationstatus.objects.get(id=12)
            if opportunityorderspost.count() >= opportunityservices.aggregate(Sum('noofservices'))['noofservices__sum']:
                self.status = operationstatus.objects.get(id=11)





        if opportunityservices:
            mrcsumoo = opportunityservices.aggregate(Sum('totalmrc'))
            mrcsumo = mrcsumoo['totalmrc__sum']
            self.totalmrc = mrcsumo
            self.revenue1 = (365-int(self.creationdate.strftime('%j')))*(int(self.totalmrc)/30)


        super(opportunity, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('opportunitydetail',kwargs={'pk':self.pk})

# opportunity-Services

class addservices(models.Model):
    serviceowner = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='salesman_addservices',verbose_name ='Service Owner')
    opportunity = models.ForeignKey(opportunity,on_delete=models.CASCADE,related_name='opportunity_addservices',verbose_name ='Opportunity')
    service = models.ForeignKey(service,blank=True,on_delete=models.CASCADE,related_name='service_opportunities',verbose_name ='Service')
    noofservices = models.IntegerField("No Of Services",default=1)
    # myservicecategory = models.ForeignKey(servicecategory,on_delete=models.CASCADE,related_name='servicecategory_addservices',verbose_name ='Service Category')
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

    def get_absolute_url(self):
        return reverse('addservicesdetail',kwargs={'pk':self.pk})

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
    dealcategory = models.CharField("Deal Category",max_length=1, choices=dealcategory,default='New')
    addservices = models.ForeignKey(addservices,on_delete=models.CASCADE,related_name='addservices_orders',verbose_name ='Services')
    orderno = models.CharField("Order No",max_length=20)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    accountno = models.IntegerField("Account No")
    serviceno = models.IntegerField("Service No",null = True,blank = True)
    imei = models.IntegerField("IMEI",null = True,blank = True)
    service = models.ForeignKey('service',blank=True,on_delete=models.CASCADE,related_name='service_order',verbose_name ='Service')
    servicecategory = models.CharField("Service Category",max_length=100,null=True)

    serviceout = models.ForeignKey('service',null=True,blank=True,on_delete=models.CASCADE,related_name='service_orderout',verbose_name ='Service out')

    discount = models.DecimalField("Discount",default=0,decimal_places=2,max_digits=3,validators=[MinValueValidator(0.0), MaxValueValidator(0.99)])
    status = models.ForeignKey(operationstatus,blank=True,on_delete=models.CASCADE,related_name='status_orders',verbose_name ='Status',null=True,default=defaultstatusorder)
    operationexecutive = models.ForeignKey(User,on_delete=models.CASCADE,related_name='executive_orders',verbose_name ='Operation Executive')
    orderstatus = models.CharField("Order Status",max_length=12, choices=orderstatuslist,default="open")
    orderdate = models.DateField("Open Date",blank=True,null=True)
    nrc = models.IntegerField("NRC")
    mrc = models.IntegerField("MRC")
    discountmrc = models.IntegerField("New MRC",default=0)
    updatedate = models.DateTimeField("Update Date",auto_now=True)
    activationdate = models.DateField("Activation Date",blank=True,null=True)
    activationdate1 = models.DateField("Activation Date",null=True,blank=True)
    cabinetno = models.CharField("Cabinet No",max_length=100,null = True,blank = True)
    circuitno = models.CharField("Circuit No",max_length=100,null = True,blank = True)
    granite = models.CharField("Granite",max_length=100,null = True,blank = True)
    stcsalesreport = models.BooleanField("STC Sales Report",default=False) #new
    stcpostreport = models.BooleanField("STC Post Report",default=False)#new
    stccommissionreport = models.BooleanField("STC Commission  Report",default=False)#new
    stccommissionrecieved = models.BooleanField("STC Recieved Commission ",default=False)#new
    revenue2 = models.IntegerField("Revenue Before Post",default=0)
    revenuep = models.IntegerField("Post Revenue",default=0)
    note = models.TextField("Note",blank=True,null=True)
    issuedbills = models.FloatField("الفواتير الصادرة",default=0)
    paidbills = models.FloatField("الفواتير المدفوعة",default=0)
    commission = models.DecimalField("Commission",default=0,max_digits=8, decimal_places=2)

    class Meta:
        verbose_name ='Order'
        verbose_name_plural ='Orders'

    def save(self, *args, **kwargs):

         if not accounts.objects.filter(accountno=self.accountno):
             accounts.objects.create(accountno=self.accountno)
         if self.activationdate:
            self.activationdate1 = self.activationdate
         if not self.activationdate and self.activationdate1:
            self.activationdate= self.activationdate1
         obj1 =  get_object_or_404(service,servicename = self.service)
         self.commission = obj1.commission
         if self.dealcategory == 'u':
            self.commission = 0.5 * obj1.commission
         if self.discount  > 0.5:
            self.commission = (Decimal(1)-(self.discount - Decimal(0.5)))*obj1.commission
         self.servicecategory = str(obj1.servicecategory)
         self.nrc = obj1.nrc
         self.mrc = obj1.mrc
         self.discountmrc = self.mrc * (1-self.discount)
         if self.dealcategory == 'n':
             if self.creationdate:
                self.revenue2 = (365-int(self.creationdate.strftime('%j')))*(int(self.discountmrc)/30)
             else :
                 tt = timezone.now()
                 self.revenue2 = (365-int(tt.strftime('%j')))*(int(self.discountmrc)/30)
         if self.activationdate:
             self.revenuep = (365-int(self.activationdate.strftime('%j')))*(int(self.discountmrc)/30)
         if self.dealcategory == 'u':
             if self.serviceout:
                 objout =  get_object_or_404(service,servicename = self.serviceout)
                 netmrc = self.mrc - objout.mrc
                 self.revenue2 = (365-int(self.creationdate.strftime('%j')))*(int(netmrc)/30)
             else :
                tt = timezone.now()

                self.revenue2 = (365-int(tt.strftime('%j')))*(int(self.mrc)/30)

             if self.activationdate and self.serviceout:
                self.revenuep = (365-int(self.activationdate.strftime('%j')))*(int(netmrc)/30)

         if accounts.objects.filter(accountno=self.accountno):
             myaccount = accounts.objects.filter(accountno=self.accountno)[0]
             myaccount.save()



         super(order, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('orderdetail',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.orderno)

    @property
    def getcustomername(self):
        return self.opportunity.customer.customername

class yearslist(models.Model):
    yeardetail = models.IntegerField("Year")

    class Meta:
        verbose_name ='Year'
        verbose_name_plural ='Years List'

    def __str__(self):
        return str(self.yeardetail)

class invoices(models.Model):

    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_invoices',verbose_name ='Service Owner')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)
    invoice_no = models.CharField("Invoice No",max_length=15,unique=True)
    invoicedate = models.DateField("Invoice Date")
    stcemaildate = models.DateField("STC Email Date",null=True,blank=True)
    relatedyear = models.IntegerField("Related Year",default = 0)
    relatedperiod = models.CharField("Related Period",max_length=80)
    amount = models.IntegerField("Amount",default=0)
    purchaseno = models.IntegerField("Purchase No",default=0)
    receiptno = models.IntegerField("Receipt No",default=0)
    bankdepoitdate = models.DateField("Deposit Date",null=True,blank=True)

    def get_absolute_url(self):
        return reverse('invoicedetail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.invoice_no

class expensecategory(models.Model):
    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_expensecategory',verbose_name ='Category Owner')
    expensecategoryname = models.CharField("Expense Category",max_length=25,null=True,unique=True)

    class Meta:
        verbose_name ='Expense Category'
        verbose_name_plural ='Expense Categoryies'

    def __str__(self):
        return self.expensecategoryname

class expenses(models.Model):

    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_expenses',verbose_name ='Creator')
    Category = models.ForeignKey(expensecategory,on_delete=models.CASCADE,related_name='category_expenses',verbose_name ='Category')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)
    amount = models.IntegerField("Amount",default=0)
    year = models.ForeignKey(yearslist,on_delete=models.CASCADE,related_name='year_expenses',verbose_name ='Year')
    month = models.IntegerField(choices=[(i,i) for i in range(1,13)],verbose_name ='Month')
    note = models.TextField("Note",blank=True,null=True)


    def get_absolute_url(self):
        return reverse('expensedetail',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.amount)

class opportunitynotes(models.Model):
    opportunity = models.ForeignKey(opportunity,on_delete=models.CASCADE,related_name='opportunity_notes',verbose_name ='Opportunity')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_opportunitynotes',verbose_name ='Note Owner')
    note = models.TextField("Note",blank=True,null=True)

    def __str__(self):
        return str(self.note)

class fservice(models.Model):
    servicename = models.CharField("Service",max_length=100,null=True,unique=True)
    nrc = models.IntegerField(default=0)
    mrc = models.IntegerField(default=0)
    commission = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('fservicedetail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.servicename

class fastdatad(models.Model):

    types = (
            ('onetime', 'onetime'),
            ('monthly', 'monthly'),
            )

    dealno  = models.IntegerField("Deal No",unique=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    updatedate = models.DateTimeField("Update Date",auto_now=True)
    creator = models.ForeignKey(User,blank=True,on_delete=models.CASCADE,related_name='user_deals',verbose_name ='Note Owner')
    customer = models.ForeignKey(fcustomer,blank=True,on_delete=models.CASCADE,related_name='fcustomer_deals',verbose_name ='Customer')
    provider = models.ForeignKey(provider,blank=True,null=True,on_delete=models.CASCADE,related_name='provider_deals',verbose_name ='Provider')
    service = models.ForeignKey(fservice,blank=True,on_delete=models.CASCADE,related_name='fservice_deals',verbose_name ='Service')
    noofservices = models.IntegerField("No Of Services",default=1)
    description = models.TextField("Description",blank=True,null=True)
    status = models.ForeignKey(operationstatus,blank=True,on_delete=models.CASCADE,related_name='status_deals',verbose_name ='Status',null=True,default=defaultstatus)
    broker = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='broker_deals',verbose_name="Broker")
    totalnrc = models.IntegerField("Total NRC",default=0)
    totalmrc = models.IntegerField("Total MRC",default=0)
    ourcommission = models.IntegerField("Company Commission",default=0)
    brokercommission = models.IntegerField("Broker Commission",default=0)
    commissiontype = models.CharField("Commissionype",max_length=20,choices=types)
    activationdate = models.DateField("Activation Date",null=True,blank=True)
    activationdate1 = models.DateField("Activation Date",null=True,blank=True)
    cancellationdate = models.DateField("Cancellation Date",null=True,blank=True)
    revenue1 = models.IntegerField("Revenue Before Post",default=0)
    revenuep = models.IntegerField("Post Revenue",default=0)
    referenceno = models.CharField("Reference No",max_length=100,null=True,blank=True)
    coordinates = models.CharField("Coordinates",max_length=100,null=True,blank=True)
    expectedclosingdate = models.DateField("Expected Closing Date",null=True,blank=True)
    datescore = models.IntegerField(default=0)
    netcommission = models.IntegerField("Net Commission",default=0)

    def get_absolute_url(self):
        return reverse('dealdetail',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.dealno)

    def save(self, *args, **kwargs):

        if not self.dealno:
            oppcount = fastdatad.objects.filter(dealno__startswith=datetime.datetime.today().strftime('%Y')).count()
            if oppcount:
                lastopp = fastdatad.objects.last()
                newno = lastopp.dealno + 1
                self.dealno = newno

            else:
                self.dealno = int(str(datetime.datetime.today().strftime('%Y')) + '000' + str(1))
        if self.activationdate:
            self.activationdate1 = self.activationdate

            if not self.cancellationdate:
                if self.commissiontype == 'monthly':
                    if self.activationdate >= date(2021, 1, 1):
                        self.revenuep = (self.totalmrc/30)*(datetime.date.today() - self.activationdate).days

        if self.activationdate:
            if not self.cancellationdate:
                if self.commissiontype == 'monthly':
                    if self.activationdate < date(2021, 1, 1):
                        self.revenuep = (self.totalmrc/30)*(datetime.date.today() - date(2021, 1, 1)).days

        if self.activationdate:
            if self.cancellationdate:
                if self.commissiontype == 'monthly':
                    if self.activationdate >= date(2021, 1, 1):
                        self.revenuep = (self.totalmrc/30)*( self.cancellationdate - self.activationdate ).days

        if self.activationdate:
            if self.commissiontype == 'onetime':
                if self.activationdate >= date(2021, 1, 1):
                    self.revenuep = self.totalnrc

        if self.activationdate:
            if int(self.activationdate.strftime("%m"))  < 10 and int(self.activationdate.strftime("%m")) > 0 :

                self.datescore = int(str(int(self.activationdate.strftime("%Y")))+str(0)+str(int(self.activationdate.strftime("%m"))))
            else:
                self.datescore = int(str(int(self.activationdate.strftime("%Y")))+str(int(self.activationdate.strftime("%m"))))

        if not self.activationdate and self.activationdate1:
            self.activationdate= self.activationdate1

        self.netcommission = self.ourcommission - self.brokercommission

        super(fastdatad, self).save(*args, **kwargs)

class dealnotes(models.Model):

    deal = models.ForeignKey(fastdatad,on_delete=models.CASCADE,related_name='deal_notes',verbose_name ='Deal')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_dealnotes',verbose_name ='Note Owner')
    note = models.TextField("Note",blank=True,null=True)

    def __str__(self):
        return str(self.note)

class finvoice(models.Model):

    invoiceno = models.IntegerField("Invoice No",unique=True)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    year = models.IntegerField("Year")
    month = models.IntegerField("Month")
    value = models.IntegerField("Value",default=0)
    paid = models.BooleanField("Paid",default=False)
    recievedamount = models.IntegerField("Recieved Amount",default=0)
    remainingamount = models.IntegerField("Remaining Amount",default=0)
    datescore = models.IntegerField(blank=True,null=True,unique=True)

    def save(self, *args, **kwargs):

        if not self.invoiceno:
            oppcount = finvoice.objects.filter(invoiceno__startswith=datetime.datetime.today().strftime('%Y')).count()
            if oppcount:
                lastopp = finvoice.objects.last()
                newno = lastopp.invoiceno + 1
                self.invoiceno = newno

            else:
                self.invoiceno = int(str(datetime.datetime.today().strftime('%Y')) + '00' + str(1))
        if self.month < 10 and self.month > 0 :

            self.datescore = int(str(self.year)+str(0)+str(self.month))
        else:
            self.datescore = int(str(self.year)+str(self.month))

        if finvoiceitem.objects.filter(invoiceno=self.id).aggregate(Sum('itemvalue'))['itemvalue__sum'] :

            self.value = finvoiceitem.objects.filter(invoiceno=self.id).aggregate(Sum('itemvalue'))['itemvalue__sum']

        if fpayment.objects.filter(invoiceno=self.id).aggregate(Sum('payment'))['payment__sum'] :

            self.recievedamount = fpayment.objects.filter(invoiceno=self.id).aggregate(Sum('payment'))['payment__sum']
            self.remainingamount = self.value - self.recievedamount
        else:
            self.recievedamount = 0
            self.remainingamount = self.value - self.recievedamount

        super(finvoice, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.invoiceno)

    def get_absolute_url(self):
        return reverse('finvoicedetail',kwargs={'pk':self.pk})

class finvoiceitem(models.Model):

    invoiceno = models.ForeignKey(finvoice,on_delete=models.CASCADE,related_name='invoice_items',verbose_name ='Invoice No')
    deal = models.ForeignKey(fastdatad,on_delete=models.CASCADE,related_name='deal_invoiceitems',verbose_name ='Deal')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    itemvalue = models.IntegerField("Value",default=0)

    def __str__(self):
        return str(self.invoiceno)

class fpayment(models.Model):

    invoiceno = models.ForeignKey(finvoice,on_delete=models.CASCADE,related_name='invoice_payment',verbose_name ='Invoice No')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    paymentdate = models.DateField("Payment Date",blank=True,null=True)
    payment = models.IntegerField("Payment")
    notes = models.CharField(max_length=1000,blank=True,null=True)

    def get_absolute_url(self):
        return reverse('fpaymentdetail',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.payment)

class accounts(models.Model):

    accountno = models.IntegerField("Account No",default=0)
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    nooforders = models.IntegerField("No of orders",default=0)
    noofpostorders = models.IntegerField("No of orders",default=0)
    activationdate = models.DateTimeField("Activation Date",blank=True,null=True)
    noofbills = models.IntegerField("No of bills",default=0)
    billsvalue = models.IntegerField("Value",default=0)
    paymentdate = models.DateField("Payment Date",blank=True,null=True)
    payment = models.IntegerField("Payment",default=0)
    notes = models.CharField(max_length=1000,blank=True,null=True)
    ispayed = models.BooleanField("Is payed",default=False)

    def save(self, *args, **kwargs):

        if order.objects.filter(accountno=self.accountno).all():
            self.nooforders = order.objects.filter(accountno=self.accountno).all().count()
        if order.objects.filter(accountno=self.accountno).filter(orderstatus='post').all():
            self.noofpostorders = order.objects.filter(accountno=self.accountno).filter(orderstatus='post').all().count()
        if  self.noofbills >=3 and self.payment >= self.billsvalue:
            self.ispayed = True
        else:
            self.ispayed = False

            # self.activationdate = order.objects.filter(accountno=self.accountno).filter(orderstatus='post').all().order_by('activationdate').first().activationdate
        super(accounts, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.accountno)

    def get_absolute_url(self):
        return reverse('accountdetail',kwargs={'pk':self.pk})

class activity(models.Model):
    activityname = models.CharField("Activity",max_length=50,null=True,unique=True)
    def __str__(self):
        return self.activityname

class activityrecord(models.Model):
    activity = models.ForeignKey(activity,on_delete=models.CASCADE,related_name='record_activities',verbose_name ='Activity')
    creationdate = models.DateTimeField("Creation Date",auto_now_add=True)
    creator = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='user_activities',verbose_name ='Creator')
    customer = models.ForeignKey(customer,blank=True,on_delete=models.CASCADE,related_name='customer_activities',verbose_name ='Customer')

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('activityrecorddetail',kwargs={'pk':self.pk})


class orderimport(models.Model):


    orderno= models.CharField("Order No",max_length=20)
    accountno = models.IntegerField("Account No")
    serviceno = models.IntegerField("Service No",null = True,blank = True)
    product = models.CharField("Product",max_length=40)
    discount = models.DecimalField("Discount",default=0,decimal_places=2,max_digits=3,validators=[MinValueValidator(0.0), MaxValueValidator(0.99)])
    mymonth = models.IntegerField("month",default = 1)
    myday = models.IntegerField("Day",default = 1)
    myyear = models.IntegerField("Year",default = 2000)


    def __str__(self):
        return self.orderno

class Action(models.Model):
    user = models.ForeignKey('auth.User',related_name='actions',db_index=True,on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj',on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,blank=True,db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)