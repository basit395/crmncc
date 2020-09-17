
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from django.utils import timezone
from django.http import HttpResponseRedirect
import datetime
from datetime import timedelta
from django.shortcuts import redirect
from django.urls import reverse
import random
from django.contrib.auth.models import User
from .models import customer,opportunity,staff,suggestion,order,operationstatus,service,servicecategory,addservices
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Count , Sum , Avg
from accounts.models import Profile
from .forms import opportunityForm,customerForm,staffForm,suggestionForm,orderForm,serviceForm,opportunitycForm,orderoForm,orderdoubleForm,addservicesForm
from django.shortcuts import get_object_or_404, render
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

# @permission_required('customer.can_view')
@login_required
def index(request):
    customerslist = customer.objects.all().order_by('-creationdate')

    context = {'customerslist':customerslist}
    return render(request, 'crmapp/index.html',context)

# @permission_required('customer.can_view')
@login_required
def customerslist(request):
    customerslist = customer.objects.all().order_by('-creationdate')

    context = {'customerslist':customerslist}
    return render(request, 'crmapp/index.html',context)


# @permission_required('opportunity.can_add')
def opportunitynew(request):
    if request.method=='POST':
        form = opportunityForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.salesman=request.user
            myform.save()

            return HttpResponseRedirect(reverse('opportunitylist'))
    else:
        form = opportunityForm()
    return render(request, 'crmapp/opportunity_form.html',{'form':form})

def opportunitycnew(request,pk):
    if request.method=='POST':
        form = opportunitycForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.salesman=request.user
            customer1 = get_object_or_404(customer,pk=pk)
            myform.customer=customer1
            myform.save()
            pk = myform.id
            return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))
            # return HttpResponseRedirect(reverse('opportunitylist'))
    else:
        form = opportunitycForm()
    return render(request, 'crmapp/opportunity_form.html',{'form':form})

# @permission_required('customer.can_add')
@login_required
def customernew(request):

    if request.method=='POST':
        form = customerForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.save()
            return HttpResponseRedirect(reverse('customerslist'))
    else:
        form = customerForm()
    return render(request, 'crmapp/customer_form.html',{'form':form})


class customerUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/customer_detail.html'
    form_class = customerForm
    model = customer


def opportunitydetail(request,pk):
    opportunitynow = get_object_or_404(opportunity,pk=pk)
    opportunityorders = opportunitynow.opportunity_orders.all()
    opportunityservices = opportunitynow.opportunity_addservices.all()
    mrcsumoo = opportunityservices.aggregate(Sum('totalmrc'))
    mrcsumo = mrcsumoo['totalmrc__sum']
    mrcsum= opportunityorders.aggregate(Sum('mrc'))
    mrcsum1 = mrcsum['mrc__sum']

    job = get_object_or_404(Profile,user=request.user)
    totalservices = opportunityservices.aggregate(Total=Sum('noofservices'))

    opportunitynow.save()
    context = {'job':job,'totalservices':totalservices,'mrcsumo':mrcsumo,'opportunityorders':opportunityorders,'opportunitynow':opportunitynow,'mrcsum1':mrcsum1,'opportunityservices':opportunityservices}
    return render(request, 'crmapp/opportunity_detail.html',context)

class opportunityUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/opportunity_detail.html'
    form_class = opportunityForm
    model = opportunity


class customerDetailView(DetailView):
    model = customer

# @permission_required('opportunity.can_change')
@login_required
def opportunitylist(request):
    opportunitylist = opportunity.objects.all().order_by('-creationdate')
    lastno = opportunity.objects.filter(opportunityno__startswith=datetime.datetime.today().strftime('%Y')).count()

    context = {'opportunitylist':opportunitylist,'lastno':lastno}
    return render(request, 'crmapp/opportunitylist.html',context)

# @permission_required('staff.can_change')
@login_required
def stafflist(request):
    stafflist = User.objects.all()
    staffprofile = Profile.objects.all()
    context = {'stafflist':stafflist,'staffprofile':staffprofile}
    return render(request, 'crmapp/stafflist.html',context)


class CreatestaffView(CreateView):
    redirect_field_name = 'crmapp/staff_detail.html'
    form_class = staffForm
    model = staff


class staffDetailView(DetailView):
    model = staff

# @permission_required('suggestion.can_change')
@login_required
def suggestionlist(request):
    suggestionlist = suggestion.objects.all()
    opensuggestionlist = suggestion.objects.filter(status="Open").all()
    job = get_object_or_404(Profile,user=request.user)
    context = {'suggestionlist':suggestionlist,'job':job}
    return render(request, 'crmapp/suggestionlist.html',context)

class suggestionUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/suggestion_detail.html'
    form_class = suggestionForm
    model = suggestion

def suggestionnew(request):
    if request.method=='POST':
        form = suggestionForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.requestor=request.user
            myform.save()
            return HttpResponseRedirect(reverse('suggestion'))
    else:
        form = suggestionForm()
    return render(request, 'crmapp/suggestion_form.html',{'form':form})

class suggestionDetailView(DetailView):
    model = suggestion

#Orders


# @permission_required('order.can_change')
@login_required
def orderpostlist(request):
    post = get_object_or_404(operationstatus,pk=8)
    orderpostlist = order.objects.all().filter(status=post).order_by('-creationdate')
    context = {'orderpostlist':orderpostlist}
    return render(request, 'crmapp/orderpostlist.html',context)

# @permission_required('order.can_add')
@login_required
def orderlist(request):
    orderlist = order.objects.all().order_by('-creationdate')
    context = {'orderlist':orderlist}
    return render(request, 'crmapp/orderlist.html',context)


# class CreateorderView(CreateView):
#     redirect_field_name = 'crmapp/order_detail.html'
#     form_class = orderForm
#     model = order

@login_required
def ordernew(request):

    if request.method=='POST':
        form = orderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            oppstatus = get_object_or_404(opportunity,opportunityno=form.cleaned_data['opportunity'].opportunityno )
            print(oppstatus.status)
            if str(oppstatus.status) == 'Document':
                myform = form.save(commit=False)
                myform.operationexecutive=request.user
                myform.save()
                return HttpResponseRedirect(reverse('order'))
            else:
                return render(request, 'crmapp/noorder.html')
    else:
        form = orderForm()
    return render(request, 'crmapp/order_form.html',{'form':form})
# addservice to opportunity

def addservicenew(request,pk):
    if request.method=='POST':
        form = addservicesForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.serviceowner=request.user
            opportunity1 = get_object_or_404(opportunity,pk=pk)

            myform.opportunity=opportunity1
            myform.save()
            pk = pk
            return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

    else:
        form = addservicesForm()
    return render(request, 'crmapp/addservices_form.html',{'form':form})

# ===============

@login_required
def addserviceslist(request):
    mylist = addservices.objects.all().order_by('-creationdate')
    context = {'mylist':mylist}
    return render(request, 'crmapp/addserviceslist.html',context)

#order from opportunity Detail
def orderonew(request,pk,pk1):
    if request.method=='POST':
        form = orderoForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.operationexecutive=request.user
            opportunity1 = get_object_or_404(opportunity,pk=pk)
            service1 = get_object_or_404(addservices,pk=pk1)
            service2 = get_object_or_404(service,servicename=service1.service)
            myform.opportunity=opportunity1
            myform.addservices = service1
            myform.service = service2
            myform.save()
            service1.save()
            pk = pk
            return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

    else:
        form = orderoForm()
    return render(request, 'crmapp/order_form.html',{'form':form})

#order from order Detail
def orderdouble(request,pk,pk1):
    if request.method=='POST':
        form = orderdoubleForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.operationexecutive=request.user
            opportunity1 = get_object_or_404(opportunity,pk=pk)
            order1 = get_object_or_404(order,pk=pk1)
            myform.opportunity=opportunity1
            myform.accountno=order1.accountno
            myform.service=order1.service
            myform.save()
            return HttpResponseRedirect(reverse('order'))
    else:
        form = orderoForm()
    return render(request, 'crmapp/order_form.html',{'form':form})


class orderDetailView(DetailView):
    model = order

#service start
# @permission_required('service.can_change')
@login_required
def servicelist(request):
    servicelist = service.objects.all().order_by('servicecategory')
    context = {'servicelist':servicelist}
    return render(request, 'crmapp/servicelist.html',context)

class CreateserviceView(CreateView):
    redirect_field_name = 'crmapp/servicelist.html'
    form_class = serviceForm
    model = service

class serviceDetailView(DetailView):
    model = service

#service end

class orderUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/order_detail.html'
    form_class = orderForm
    model = order

# @permission_required('order.can_change')
@login_required
def changetopost(request,pk):
    orderpost = get_object_or_404(order,pk=pk)
    post = 'post'
    orderpost.orderstatus = post
    orderpost.save()
    orderlist = order.objects.all().order_by('-creationdate')
    pk = pk
    return HttpResponseRedirect(reverse('orderdetail', args=(pk,)))

# @permission_required('order.can_change')
@login_required
def cancelorder(request,pk):
    ordernow = get_object_or_404(order,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=7)
    ordernow.status = statusnow
    ordernow.save()
    orderlist = order.objects.all().order_by('-creationdate')
    context = {'orderlist':orderlist}
    return render(request, 'crmapp/orderlist.html',context)

# @permission_required('order.can_change')
@login_required
def openorder(request,pk):
    ordernow = get_object_or_404(order,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=5)
    ordernow.status = statusnow
    ordernow.save()
    orderlist = order.objects.all().order_by('-creationdate')
    context = {'orderlist':orderlist}
    return render(request, 'crmapp/orderlist.html',context)

# @permission_required('order.can_change')
@login_required
def heldorder(request,pk):
    ordernow = get_object_or_404(order,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=6)
    ordernow.status = statusnow
    ordernow.save()
    orderlist = order.objects.all().order_by('-creationdate')
    context = {'orderlist':orderlist}
    return render(request, 'crmapp/orderlist.html',context)

@login_required
def proposalopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=2)
    oppnow.status = statusnow
    oppnow.save()
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))


@login_required
def postopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=11)
    oppnow.status = statusnow
    oppnow.save()
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def negotiationopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=1)
    oppnow.status = statusnow
    oppnow.save()
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def documentopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=3)
    opportunitylist = opportunity.objects.all().order_by('-creationdate')
    oppnow.status = statusnow
    oppnow.save()
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def operationvalidationopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=4)
    opportunitylist = opportunity.objects.all().order_by('-creationdate')
    oppnow.status = statusnow
    oppnow.save()
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def validatedopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=6)
    opportunitylist = opportunity.objects.all().order_by('-creationdate')
    oppnow.status = statusnow
    oppnow.save()
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def completedsugg(request,pk):
    suggnow = get_object_or_404(suggestion,pk=pk)
    suggnow.completion = True
    suggnow.save()
    context = {'suggnow':suggnow}
    return render(request, 'crmapp/suggestionlist.html',context)

@login_required
def closedsugg(request,pk):
    suggnow = get_object_or_404(suggestion,pk=pk)
    suggnow.status = 'Closed'
    suggnow.save()
    job = get_object_or_404(Profile,user=request.user)
    return HttpResponseRedirect(reverse('suggestion'))


@login_required
def all_users_sum(request):
    allavg = opportunity.objects.all().aggregate(Average_Price=Avg('totalmrc'))
    allsum = opportunity.objects.all().aggregate(Total=Sum('totalmrc'))
    allsalesman = User.objects.all()
    annotateex = opportunity.objects.annotate(Count('opportunity_orders'))
    all2 = opportunity.objects.values('salesman').annotate(Total=Sum('totalmrc'))
    allsalesmanvalues = User.objects.all().values()
    allsalesmanvalueslist = User.objects.all().values_list('id','email')
    datesyears = order.objects.dates('creationdate','year')
    datesmonths = order.objects.dates('creationdate','month')
    datesweeks = order.objects.dates('creationdate','week')
    categories = service.objects.all().prefetch_related('servicecategory')
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    if cmonth == 1 :
        lastmonth = 12
    else:
        lastmonth = int(cmonth)-1
    lastyear = int(cyear)-1


    todayo = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todayocount = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).count()
    todayosum = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))
    todayosalesman = todayo.values('salesman').annotate(Total=Sum('totalmrc'))

    ydayo = opportunity.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear)

    ydayocount = ydayo.count()
    ydayosum = ydayo.aggregate(Total=Sum('totalmrc'))
    ydayosalesman = ydayo.values('salesman').annotate(Total=Sum('totalmrc'))


    if cmonth ==1 :
        lastmontho = opportunity.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=lastyear)
    else:
        lastmontho = opportunity.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=cyear)
    lastmonthcount = lastmontho.count()
    lastmonthsum = lastmontho.aggregate(Total=Sum('totalmrc'))
    lastmonthosalesman = lastmontho.values('salesman').annotate(Total=Sum('totalmrc'))

    lastyearo = opportunity.objects.filter(creationdate__year=lastyear)
    lastyearcount = lastyearo.count()
    lastyearsum = lastyearo.aggregate(Total=Sum('totalmrc'))
    lastyearosalesman = lastyearo.values('salesman').annotate(Total=Sum('totalmrc'))

    thismontho = opportunity.objects.filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    thismonthcount = thismontho.count()
    thismonthsum = thismontho.aggregate(Total=Sum('totalmrc'))
    thismonthosalesman = thismontho.values('salesman').annotate(Total=Sum('totalmrc'))

    thisyearo = opportunity.objects.filter(creationdate__year=cyear)
    thisyearcount = thisyearo.count()
    thisyearsum = thisyearo.aggregate(Total=Sum('totalmrc'))
    thisyearosalesman = thisyearo.values('salesman').annotate(Total=Sum('totalmrc'))

    context = {'lastyearcount':lastyearcount,'lastmontho':lastmontho,'lastyearo':lastyearo,'lastyear':lastyear,'lastmonth':lastmonth,'ydayo':ydayo,'yday':yday,'todayo':todayo,'cday':cday,'cmonth':cmonth,'cyear':cyear,'categories':categories,'datesweeks':datesweeks,'datesmonths':datesmonths,'datesyears':datesyears,'allsalesmanvalueslist':allsalesmanvalueslist,'allsum':allsum,'allavg':allavg,'allsalesman':allsalesman,'all2':all2,'annotateex':annotateex,'allsalesmanvalues':allsalesmanvalues,'todayocount':todayocount,'todayosum':todayosum,'todayosalesman':todayosalesman,'ydayocount':ydayocount,'ydayosum':ydayosum,'ydayosalesman':ydayosalesman,'lastmonthcount':lastmonthcount,'lastmonthsum':lastmonthsum,'lastmonthosalesman':lastmonthosalesman,'lastyearcount':lastyearcount,'lastyearsum':lastyearsum,'lastyearosalesman':lastyearosalesman,'thismontho':thismontho,'thismonthcount':thismonthcount,'thismonthsum':thismonthsum,'thismonthosalesman':thismonthosalesman,'thisyearo':thisyearo,'thisyearcount':thisyearcount,'thisyearsum':thisyearsum,'thisyearosalesman':thisyearosalesman}
    return render(request, 'crmapp/report.html',context)

# dashboard start

@login_required
def dashboard(request):
    allavg = opportunity.objects.all().aggregate(Average_Price=Avg('totalmrc'))
    allsum = opportunity.objects.all().aggregate(Total=Sum('totalmrc'))
    allsalesman = User.objects.all()
    datesyears = order.objects.dates('creationdate','year')
    datesmonths = order.objects.dates('creationdate','month')
    datesweeks = order.objects.dates('creationdate','week')
    categories = service.objects.all().prefetch_related('servicecategory')
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    if cmonth == 1 :
        lastmonth = 12
    else:
        lastmonth = int(cmonth)-1
    lastyear = int(cyear)-1

    allopp = opportunity.objects.all()
    todayo = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todayocount = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).count()
    todayosum = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))
    todayosalesman = todayo.values('salesman').annotate(Total=Sum('totalmrc'))

    ydayo = opportunity.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear)

    ydayocount = ydayo.count()
    ydayosum = ydayo.aggregate(Total=Sum('totalmrc'))
    ydayosalesman = ydayo.values('salesman').annotate(Total=Sum('totalmrc'))


    if cmonth ==1 :
        lastmontho = opportunity.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=lastyear)
    else:
        lastmontho = opportunity.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=cyear)
    lastmonthcount = lastmontho.count()
    lastmonthsum = lastmontho.aggregate(Total=Sum('totalmrc'))
    lastmonthosalesman = lastmontho.values('salesman').annotate(Total=Sum('totalmrc'))

    lastyearo = opportunity.objects.filter(creationdate__year=lastyear)
    lastyearcount = lastyearo.count()
    lastyearsum = lastyearo.aggregate(Total=Sum('totalmrc'))
    lastyearosalesman = lastyearo.values('salesman').annotate(Total=Sum('totalmrc'))

    thismontho = opportunity.objects.filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    thismonthcount = thismontho.count()
    thismonthsum = thismontho.aggregate(Total=Sum('totalmrc'))
    thismonthosalesman = thismontho.values('salesman').annotate(Total=Sum('totalmrc'))

    thisyearo = opportunity.objects.filter(creationdate__year=cyear)
    thisyearcount = thisyearo.count()
    thisyearsum = thisyearo.aggregate(Total=Sum('totalmrc'))
    thisyearosalesman = thisyearo.values('salesman').annotate(Total=Sum('totalmrc'))

    context = {'allopp':allopp,'lastyearcount':lastyearcount,'lastmontho':lastmontho,'lastyearo':lastyearo,'lastyear':lastyear,'lastmonth':lastmonth,'ydayo':ydayo,'yday':yday,'todayo':todayo,'cday':cday,'cmonth':cmonth,'cyear':cyear,'categories':categories,'datesweeks':datesweeks,'datesmonths':datesmonths,'datesyears':datesyears,'allsum':allsum,'allavg':allavg,'allsalesman':allsalesman,'todayocount':todayocount,'todayosum':todayosum,'todayosalesman':todayosalesman,'ydayocount':ydayocount,'ydayosum':ydayosum,'ydayosalesman':ydayosalesman,'lastmonthcount':lastmonthcount,'lastmonthsum':lastmonthsum,'lastmonthosalesman':lastmonthosalesman,'lastyearcount':lastyearcount,'lastyearsum':lastyearsum,'lastyearosalesman':lastyearosalesman,'thismontho':thismontho,'thismonthcount':thismonthcount,'thismonthsum':thismonthsum,'thismonthosalesman':thismonthosalesman,'thisyearo':thisyearo,'thisyearcount':thisyearcount,'thisyearsum':thisyearsum,'thisyearosalesman':thisyearosalesman}
    return render(request, 'crmapp/dashboard.html',context)


# dashboar end


@login_required
def reportall(request):
    yy = 'Zero'
    # allcategories = opportunity.objects.values('servicecategory').annotate(Totalc=Sum('totalmrc'))
    allservices = opportunity.objects.values('service').annotate(Total=Sum('totalmrc'))
    allcategoriesall = servicecategory.objects.all()
    allservicesall = service.objects.all()
    context = {'yy':yy,'allservicesall':allservicesall,'allcategoriesall':allcategoriesall,'allservices':allservices}
    return render(request, 'crmapp/reportall.html',context)

@login_required
def oppnogen(request):


    lastno = opportunity.objects.filter(opportunityno__startswith=datetime.datetime.today().strftime('%Y')).last()
    newno = lastno.opportunityno +1
    context = {'lastno':lastno,'newno':newno}
    return render(request, 'crmapp/lastno.html',context)
