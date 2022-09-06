

from django.http import HttpResponse
from django.db.models import F
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Q
import datetime
from datetime import timedelta
from django.shortcuts import redirect
from django.urls import reverse
import random
from django.contrib.auth.models import User
from .models import customer,fcustomer,opportunity,staff,suggestion,order,operationstatus,service,fservice,servicecategory,addservices,invoices,expensecategory,expenses,yearslist,leadsource,partner,opportunitynotes,fastdatad,finvoice,finvoiceitem,fpayment,accounts,activityrecord,orderimport
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Count , Sum , Avg , Max
from accounts.models import Profile,thejobtitle
import io
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage

from django.contrib import messages
from decimal import Decimal
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import customerFilter,opportunityFilter,orderFilter,activityrecordFilter
from .forms import opportunityForm,customerForm,fcustomerForm,staffForm,suggestionForm,orderForm,serviceForm,fserviceForm,opportunitycForm,orderoForm,orderdoubleForm,addservicesForm,invoicesForm,expensecategoryForm,expensesForm,orderdouble1Form,orderupdateForm,orderpostForm,customerassigningForm,opportunitynotesForm,fastdatadForm,orderpaymentupdateForm,fpaymentForm,accountsForm,orderdouble2Form,activityrecordForm,activityrecordcForm,emailregisterForm
from django.shortcuts import get_object_or_404, render
from crmapp.utils import create_action
from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)




@login_required
def index(request):

    customerslist = customer.objects.all().order_by('-creationdate')
    myfilter = customerFilter(request.GET,queryset=customerslist)
    customerslist = myfilter.qs

    paginator = Paginator(customerslist,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)

    mycustomers = customer.objects.filter(creator=request.user).order_by('-creationdate')
    myfilter1 = customerFilter(request.GET,queryset=mycustomers)
    mycustomers = myfilter1.qs

    myassignedcustomers = customer.objects.filter(assignedto=request.user).order_by('-creationdate')

    paginator1 = Paginator(mycustomers,10)
    page = request.GET.get('page')
    try:
        opps1 = paginator1.page(page)
    except PageNotAnInteger:
        opps1 = paginator1.page(1)
    except EmptyPage:
        opps1 = paginator1.page(paginator1.num_pages)

    context = {'customerslist':customerslist,'mycustomers':mycustomers,'opps':opps,'opps1':opps1,'myfilter':myfilter,'myfilter1':myfilter1}
    return render(request, 'crmapp/index.html',context)

#new
@login_required
def mycustomers(request):
    mycustomers = customer.objects.filter(creator=request.user).order_by('-creationdate')
    context = {'mycustomers':mycustomers}
    return render(request, 'crmapp/mycustomers.html',context)

#new
@login_required
def usercustomers(request,pk):
    usercustomers = customer.objects.filter(creator=pk).order_by('-creationdate')
    context = {'usercustomers':usercustomers,'pk':pk}
    return render(request, 'crmapp/usercustomers.html',context)


@login_required
def myopportunities(request):

    myopportunities = opportunity.objects.filter(salesman=request.user).order_by('-creationdate')
    paginator = Paginator(myopportunities,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)
    context = {'myopportunities':myopportunities,'opps':opps}
    return render(request, 'crmapp/myopportunities.html',context)


@login_required
def useropportunities(request,pk):
    useropportunities = opportunity.objects.filter(salesman=pk).order_by('-creationdate')
    context = {'useropportunities':useropportunities}
    return render(request, 'crmapp/useropportunities.html',context)


@login_required
def customerslist(request):

    customerslist = customer.objects.all().order_by('-creationdate')
    myfilter = customerFilter(request.GET,queryset=customerslist)
    customerslist = myfilter.qs

    paginator = Paginator(customerslist,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)

    mycustomers = customer.objects.filter(creator=request.user).order_by('-creationdate')
    myfilter1 = customerFilter(request.GET,queryset=mycustomers)
    mycustomers = myfilter1.qs

    myassignedcustomers = customer.objects.filter(assignedto=request.user).order_by('-creationdate')

    paginator1 = Paginator(mycustomers,10)
    page = request.GET.get('page')
    try:
        opps1 = paginator1.page(page)
    except PageNotAnInteger:
        opps1 = paginator1.page(1)
    except EmptyPage:
        opps1 = paginator1.page(paginator1.num_pages)



    context = {'customerslist':customerslist,'mycustomers':mycustomers,'opps':opps,'opps1':opps1,'myfilter':myfilter,'myfilter1':myfilter1,'myassignedcustomers':myassignedcustomers}
    return render(request, 'crmapp/index.html',context)

@login_required
def fcustomerslist(request):
    fcustomerslist = fcustomer.objects.all().order_by('-creationdate')
    context = {'fcustomerslist':fcustomerslist}
    return render(request, 'crmapp/fcustomerslist.html',context)


@login_required
def reportcustomerteam(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    cweek = datetime.datetime.today().strftime("%U")
    if cweek == 1 :
        lastweek = 52
    else:
        lastweek = int(cweek)-1
    if cmonth == 1 :
        lastmonth = 12
    else:
        lastmonth = int(cmonth)-1
    lastyear = int(cyear)-1


    todayc = customer.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todaycsalesman = todayc.values('creator').annotate(Total=Count('id'))

    ydayc = customer.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear)
    ydaycsalesman = ydayc.values('creator').annotate(Total=Count('id'))

    thisweekc = customer.objects.filter(creationdate__week=cweek).filter(creationdate__year=cyear)
    thisweekcsalesman = thisweekc.values('creator').annotate(Total=Count('id'))

    if cweek ==1 :
        lastweekc = customer.objects.filter(creationdate__week=lastweek).filter(creationdate__year=lastyear)
    else:
        lastweekc = customer.objects.filter(creationdate__week=lastweek).filter(creationdate__year=cyear)
    lastweekcsalesman = lastweekc.values('creator').annotate(Total=Count('id'))

    thismonthc = customer.objects.filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    thismonthcsalesman = thismonthc.values('creator').annotate(Total=Count('id'))

    if cmonth ==1 :
        lastmonthc = customer.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=lastyear)
    else:
        lastmonthc = customer.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=cyear)
    lastmonthcsalesman = lastmonthc.values('creator').annotate(Total=Count('id'))

    thisyearc = customer.objects.filter(creationdate__year=cyear)
    thisyearcsalesman = thisyearc.values('creator').annotate(Total=Count('id'))

    lastyearc = customer.objects.filter(creationdate__year=lastyear)
    lastyearcsalesman = lastyearc.values('creator').annotate(Total=Count('id'))

    allc = customer.objects.all()
    allcsalesman = allc.values('creator').annotate(Total=Count('id'))


    allsalesman = User.objects.all()
    context = {'todayc':todayc,'todaycsalesman':todaycsalesman,'allsalesman':allsalesman,'ydaycsalesman':ydaycsalesman,'thisweekcsalesman':thisweekcsalesman,'lastweekcsalesman':lastweekcsalesman,'thismonthcsalesman':thismonthcsalesman,'lastmonthcsalesman':lastmonthcsalesman,'thisyearcsalesman':thisyearcsalesman,'lastyearcsalesman':lastyearcsalesman,'allcsalesman':allcsalesman,'thisweekc':thisweekc,'lastweekc':lastweekc,'thismonthc':thismonthc,'ydayc':ydayc,'lastmonthc':lastmonthc,'thisyearc':thisyearc,'lastyearc':lastyearc,'allc':allc}
    return render(request, 'crmapp/reportcustomerteam.html',context)

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


@login_required
def customernew(request):

    if request.method=='POST':
        form = customerForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.save()
            messages.success(request, 'Customer added successfully')
            create_action(request.user, 'new customer', myform)
            return HttpResponseRedirect(reverse('customerslist'))

    else:
        form = customerForm()
    return render(request, 'crmapp/customer_form.html',{'form':form})

@login_required
def fcustomernew(request):

    if request.method=='POST':
        form = fcustomerForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.save()
            return HttpResponseRedirect(reverse('fcustomerslist'))
    else:
        form = fcustomerForm()
    return render(request, 'crmapp/fcustomer_form.html',{'form':form})

class customerUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/customer_detail.html'
    form_class = customerForm
    model = customer

class fcustomerUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/fcustomer_detail.html'
    form_class = fcustomerForm
    model = fcustomer

@login_required
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

class fcustomerDetailView(DetailView):
    model = fcustomer

@login_required
def opportunitylist(request):

    opportunitylist = opportunity.objects.all().order_by('-creationdate')
    myfilter = opportunityFilter(request.GET,queryset=opportunitylist)
    opportunitylist = myfilter.qs
    aa = order.objects.all().count()
    bb = addservices.objects.all().count()
    paginator = Paginator(opportunitylist,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)


    lastno = opportunity.objects.filter(opportunityno__startswith=datetime.datetime.today().strftime('%Y')).count()

    myopportunities = opportunity.objects.filter(salesman=request.user).order_by('-creationdate')
    myfilter1 = opportunityFilter(request.GET,queryset=myopportunities)
    myopportunities = myfilter1.qs
    paginator1 = Paginator(myopportunities,10)
    page = request.GET.get('page')
    try:
        opps1 = paginator1.page(page)
    except PageNotAnInteger:
        opps1 = paginator1.page(1)
    except EmptyPage:
        opps1 = paginator1.page(paginator1.num_pages)

    # channelopportunities = opportunity.objects.filter(salesman=request.user).order_by('-creationdate')
    # myfilter2 = opportunityFilter(request.GET,queryset=channelopportunities)
    # channelopportunities = myfilter2.qs
    # paginator2 = Paginator(channelopportunities,10)
    # page = request.GET.get('page')
    # try:
    #     opps2 = paginator2.page(page)
    # except PageNotAnInteger:
    #     opps2 = paginator2.page(1)
    # except EmptyPage:
    #     opps2 = paginator2.page(paginator2.num_pages)


    context = {'aa':aa,'bb':bb,'opportunitylist':opportunitylist,'lastno':lastno,'myopportunities':myopportunities,'opps':opps,'opps1':opps1,'myfilter':myfilter,'myfilter1':myfilter1}
    return render(request, 'crmapp/opportunitylist.html',context)


@login_required
def stafflist(request):
    stafflist = User.objects.filter(is_active=True)
    staffprofile = Profile.objects.all()
    context = {'stafflist':stafflist,'staffprofile':staffprofile}
    return render(request, 'crmapp/stafflist.html',context)


class CreatestaffView(CreateView):
    redirect_field_name = 'crmapp/staff_detail.html'
    form_class = staffForm
    model = staff


class staffDetailView(DetailView):
    model = staff


@login_required
def suggestionlist(request):
    suggestionlist = suggestion.objects.all().order_by('-creationdate')
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



@login_required
def orderpostlist(request):

    orderpostlist = order.objects.all().filter(orderstatus='post').order_by('-activationdate')
    myfilter = orderFilter(request.GET,queryset=orderpostlist)
    orderpostlist = myfilter.qs

    paginator = Paginator(orderpostlist,20)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)

    mrcsumoo = orderpostlist.aggregate(Sum('mrc'))
    mrcsumo = mrcsumoo['mrc__sum']
    context = {'orderpostlist':orderpostlist,'mrcsumo':mrcsumo,'opps':opps,'myfilter':myfilter}
    return render(request, 'crmapp/orderpostlist.html',context)

    # orderlist = order.objects.all().order_by('-creationdate')

    # myfilter = orderFilter(request.GET,queryset=orderlist)
    # orderlist = myfilter.qs

    # paginator = Paginator(orderlist,10)
    # page = request.GET.get('page')
    # try:
    #     opps = paginator.page(page)
    # except PageNotAnInteger:
    #     opps = paginator.page(1)
    # except EmptyPage:
    #     opps = paginator.page(paginator.num_pages)

    # context = {'orderlist':orderlist,'opps':opps,'myfilter':myfilter}


def channelcomm(x,y):
    if not x :
        chp=0

    else:

        if x < 225000:
            chp = y
        elif x <= 400000 :
            chp = 1.3*y
        elif x <= 700000:
            chp = 1.7*y
        elif x <= 1200000:
            chp = 2.1*y
        else :
            chp = 2.3*y

    return chp



def orderpostreportthisyear(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    orderpostlist = order.objects.all().filter(orderstatus='post').filter(activationdate__year=cyear)
    myreport = orderpostlist.values('activationdate__year', 'activationdate__month').annotate(count=Sum('mrc'))
    myaccounts = accounts.objects.all().filter(paymentdate__year=cyear)
    customerspayments = myaccounts.values('paymentdate__year', 'paymentdate__month').annotate(count=Sum('payment'))
    mrcsumoo = orderpostlist.aggregate(Sum('mrc'))
    mrcsumo = mrcsumoo['mrc__sum']
    discountmrcsumoo = orderpostlist.aggregate(Sum('discountmrc'))
    discountmrcsumo = discountmrcsumoo['discountmrc__sum']
    paymenttarget= 3*discountmrcsumo
    allpayment = accounts.objects.all().filter(paymentdate__year=cyear)
    totalpayment = allpayment.aggregate(Sum('payment'))['payment__sum']
    if not paymenttarget :
        paymentpercentage = 0
    elif not totalpayment :
        paymentpercentage = 0
    else:
        paymentpercentage = int(100*totalpayment/paymenttarget)

    reportx = []
    for i in range(1,13):
        mpost = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month=int(i)).aggregate(Sum('mrc'))['mrc__sum']
        mpostd = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month=int(i)).aggregate(Sum('discountmrc'))['discountmrc__sum']

        if not mpost:
            channelp = 0
        else:

            if mpostd < 100000:
                channelp = 0
            elif mpostd <200000:
                channelp = 0.5* mpostd
            elif mpostd <350000:
                channelp = 0.7* mpostd
            elif mpostd <500000:
                channelp = 0.9* mpostd
            else:
                channelp = mpostd





        if accounts.objects.filter(paymentdate__year=cyear).filter(paymentdate__month=int(i)).aggregate(Sum('payment'))['payment__sum']:
            mpayment = accounts.objects.filter(paymentdate__year=cyear).filter(paymentdate__month=i).aggregate(Sum('payment'))['payment__sum']
        else:
            mpayment = 0
        reportx.append({'month':i, 'post': mpost,'payment':mpayment,'discountmrc':mpostd,'channelp':channelp})


    q1 = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__lt=4).aggregate(Sum('discountmrc'))['discountmrc__sum']
    q1mrc = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__lt=4).aggregate(Sum('mrc'))['mrc__sum']
    q2 = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__lt=7).exclude(activationdate__month__lt=4).aggregate(Sum('discountmrc'))['discountmrc__sum']
    q2mrc = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__lt=7).exclude(activationdate__month__lt=4).aggregate(Sum('mrc'))['mrc__sum']
    q3 = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__lt=10).exclude(activationdate__month__lt=7).aggregate(Sum('discountmrc'))['discountmrc__sum']
    q3mrc = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__lt=10).exclude(activationdate__month__lt=7).aggregate(Sum('mrc'))['mrc__sum']
    q4 = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__gt=9).aggregate(Sum('discountmrc'))['discountmrc__sum']
    q4mrc = order.objects.filter(orderstatus='post').filter(activationdate__year=cyear).filter(activationdate__month__gt=9).aggregate(Sum('mrc'))['mrc__sum']


    q1p =channelcomm(q1,q1mrc)
    q2p =channelcomm(q2,q2mrc)
    q3p =channelcomm(q3,q3mrc)
    q4p =channelcomm(q4,q4mrc)

    context = {'q4':q4,'q4p':q4p,'q3':q3,'q3p':q3p,'q2':q2,'q2p':q2p,'q1':q1,'q1p':q1p,'reportx':reportx,'customerspayments':customerspayments,'myreport':myreport,'cyear':cyear,'mrcsumo':mrcsumo,'totalpayment':totalpayment,'discountmrcsumo':discountmrcsumo,'paymentpercentage':paymentpercentage,'paymenttarget':paymenttarget}
    return render(request, 'crmapp/orderpostreport.html',context)

@login_required
def orderopenlist(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    orderopenlist = order.objects.all().filter(orderstatus='open').filter(creationdate__year__gte=2021).order_by('opportunity')
    orderopenlists = orderopenlist.aggregate(Total=Sum('discountmrc'))
    context = {'orderopenlists':orderopenlists,'orderopenlist':orderopenlist}
    return render(request, 'crmapp/orderopenlist.html',context)

@login_required
def orderheldlist(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    orderheldlist = order.objects.all().filter(orderstatus='held').filter(creationdate__year__gte=2021).order_by('-creationdate')
    context = {'orderheldlist':orderheldlist}
    return render(request, 'crmapp/orderheldlist.html',context)

@login_required
def ordercancellist(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    ordercancellist = order.objects.all().filter(orderstatus='cancel').filter(creationdate__year__gte=2021).order_by('-creationdate')
    context = {'ordercancellist':ordercancellist}
    return render(request, 'crmapp/ordercancellist.html',context)



@login_required
def ordernopost(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    ordernopost = order.objects.all().exclude(orderstatus='post').filter(creationdate__year=cyear).order_by('-creationdate')
    context = {'ordernopost':ordernopost}
    return render(request, 'crmapp/ordernopost.html',context)


@login_required
def orderlist(request):
    orderlist = order.objects.all().order_by('-creationdate')

    myfilter = orderFilter(request.GET,queryset=orderlist)
    orderlist = myfilter.qs

    paginator = Paginator(orderlist,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)

    context = {'orderlist':orderlist,'opps':opps,'myfilter':myfilter}
    return render(request, 'crmapp/orderlist.html',context)




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
@login_required
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
            addservices_id = order1.addservices.id
            addservices1 = get_object_or_404(addservices,pk=int(addservices_id))
            if addservices1.createdservices < addservices1.noofservices:
                addservices1.save()
                myform.opportunity=opportunity1
                myform.accountno=order1.accountno
                myform.service=order1.service
                myform.dealcategory=order1.dealcategory
                myform.addservices=order1.addservices
                myform.orderno=order1.orderno
                myform.save()
                addservices1.save()
                return redirect('orderdetail', pk=pk1)

    else:
        form = orderdoubleForm()
    return render(request, 'crmapp/order_form.html',{'form':form})

def orderdetail(request,pk):
        myorder = get_object_or_404(order,pk=pk)
        myaddservices = get_object_or_404(addservices,pk=myorder.addservices.id)
        myopportunity = get_object_or_404(opportunity,pk=myorder.opportunity.id)
        myservicecount = myaddservices.noofservices
        myordercount = order.objects.filter(orderno=myorder.orderno).filter(addservices=myaddservices).count()
        myaddservices.save()
        context = {'myordercount':myordercount,'myorder':myorder,'myaddservices':myaddservices,'myopportunity':myopportunity}
        return render(request, 'crmapp/order_detail.html',context)

#service start

@login_required
def servicelist(request):
    servicelist = service.objects.all().order_by('servicecategory').order_by('servicename')
    context = {'servicelist':servicelist}
    return render(request, 'crmapp/servicelist.html',context)

class CreateserviceView(CreateView):
    redirect_field_name = 'crmapp/servicelist.html'
    form_class = serviceForm
    model = service

class serviceUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/service_detail.html'
    form_class = serviceForm
    model = service

class serviceDetailView(DetailView):
    model = service

#service end

class orderUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/order_detail.html'
    form_class = orderupdateForm
    model = order


@login_required
def changetopost(request,pk):

    if request.method=='POST':
        myorder = get_object_or_404(order, pk = pk)
        form = orderpostForm(request.POST or None, instance = myorder)
        myorder.orderstatus = 'post'

        myopportunity = get_object_or_404(opportunity, pk = myorder.opportunity.pk)
        myopportunity.save()
        if form.is_valid():
            myorder.save()
            form.save()
            myopportunity.save()
            pk = pk
            return HttpResponseRedirect(reverse('orderdetail', args=(pk,)))

    else:
        form = orderpostForm()

    return render(request, 'crmapp/order_form.html',{'form':form})


@login_required
def cancelorder(request,pk):
    ordernow = get_object_or_404(order,pk=pk)

    ordernow.orderstatus = 'cancel'
    ordernow.save()


    return HttpResponseRedirect(reverse('orderdetail', args=(pk,)))


@login_required
def openorder(request,pk):
    ordernow = get_object_or_404(order,pk=pk)

    ordernow.orderstatus = 'open'
    ordernow.save()


    return HttpResponseRedirect(reverse('orderdetail', args=(pk,)))


@login_required
def heldorder(request,pk):
    ordernow = get_object_or_404(order,pk=pk)
    ordernow.orderstatus = 'held'
    ordernow.save()
    return HttpResponseRedirect(reverse('orderdetail', args=(pk,)))

@login_required
def proposalopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=2)
    oppnow.status = statusnow
    oppnow.save()
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To Proposal")
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def stcapproval(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=14)
    oppnow.status = statusnow
    oppnow.save()
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To STC Approval")
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def lostopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=13)
    oppnow.status = statusnow
    oppnow.save()
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To Lost")
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def postopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=11)
    oppnow.status = statusnow
    oppnow.save()
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To Post")
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def negotiationopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=1)
    oppnow.status = statusnow
    oppnow.save()
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To Negotiation")
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def documentopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=3)
    oppnow.status = statusnow
    oppnow.save()
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To Document")
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

@login_required
def operationvalidationopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=4)
    oppnow.status = statusnow
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To Operation Validation")
    oppnow.save()
    pk = pk
    return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

def operval(request):
    opplist = opportunity.objects.filter(status__id=4)
    context = {'opplist':opplist}
    return render(request, 'crmapp/operval.html',context)

def opportunitypost(request):
    opplist = opportunity.objects.filter(status__id=11)
    context = {'opplist':opplist}
    return render(request, 'crmapp/opportunitypost.html',context)

@login_required
def validatedopp(request,pk):
    oppnow = get_object_or_404(opportunity,pk=pk)
    statusnow = get_object_or_404(operationstatus,pk=6)
    oppnow.status = statusnow
    oppnow.save()
    opportunitynotes.objects.create(creator=request.user,opportunity=oppnow,note="Change To Validated")
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
def reportthisyear(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    thisyearo = opportunity.objects.filter(creationdate__year=cyear)
    thisyearsum = thisyearo.aggregate(Total=Sum('totalmrc'))
    thisyearosalesman = thisyearo.values('salesman').annotate(Total=Sum('totalmrc'))
    allsalesman = User.objects.all()
    paginator = Paginator(thisyearo,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)
    context = {'cyear':cyear,'page':page,'opps':opps,'thisyearo':thisyearo,'thisyearsum':thisyearsum,'thisyearosalesman':thisyearosalesman,'allsalesman':allsalesman}
    return render(request, 'crmapp/reportthisyear.html',context)

@login_required
def reportthismonth(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    thismontho = opportunity.objects.filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    thismonthcount = thismontho.count()
    thismonthsum = thismontho.aggregate(Total=Sum('totalmrc'))
    thismonthos = thismontho.values('salesman').annotate(Total=Sum('totalmrc'))
    sss = User.objects.all()
    paginator = Paginator(thismontho,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)
    context = {'cyear':cyear,'cmonth':cmonth,'page':page,'opps':opps,'thismontho':thismontho,'thismonthsum':thismonthsum,'thismonthos':thismonthos,'sss':sss}
    return render(request, 'crmapp/reportthismonth.html',context)

def reportweaklastweek(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cweek = datetime.datetime.today().strftime('%U')
    weekd = datetime.datetime.today().isoweekday()
    x = datetime.date.today()
    myday1 = x.strftime("%A")
    if myday1 == 'Sunday':
        range1 = datetime.date.today() - timedelta(days=7)
        range2 = datetime.date.today() - timedelta(days=0)
        myday = myday1
        range3 = datetime.date.today()
        range4 = datetime.date.today() + timedelta(days=7)

    if myday1 == 'Monday':
        range1 = datetime.date.today() - timedelta(days=8)
        range2 = datetime.date.today() - timedelta(days=1)

        range3 = datetime.date.today() - timedelta(days=1)
        range4 = datetime.date.today() + timedelta(days=6)

    if myday1 == 'Tuesday':
        range1 = datetime.date.today() - timedelta(days=9)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=2)
        range4 = datetime.date.today() + timedelta(days=5)

    if myday1 == 'Wednesday':
        range1 = datetime.date.today() - timedelta(days=10)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=3)
        range4 = datetime.date.today() + timedelta(days=4)

    if myday1 == 'Thursday':
        range1 = datetime.date.today() - timedelta(days=11)
        range2 = datetime.date.today() - timedelta(days=4)

        range3 = datetime.date.today() - timedelta(days=4)
        range4 = datetime.date.today() + timedelta(days=3)

    if myday1 == 'Friday':
        range1 = datetime.date.today() - timedelta(days=12)
        range2 = datetime.date.today() - timedelta(days=5)

        range3 = datetime.date.today() - timedelta(days=5)
        range4 = datetime.date.today() + timedelta(days=2)

    if myday1 == 'Saturday':
        range1 = datetime.date.today() - timedelta(days=13)
        range2 = datetime.date.today() - timedelta(days=6)

        range3 = datetime.date.today() - timedelta(days=6)
        range4 = datetime.date.today() + timedelta(days=1)

    allsalesmanid = []
    lastweekosid = []
    lastweekcsid = []

    lastweeko = opportunity.objects.filter(creationdate__range=(range1, range2))

    allsalesman = User.objects.filter(user_profile__jobtitle='SalesExecutive').filter(is_active=True)
    lastweekos = lastweeko.values('salesman').annotate(Total=Sum('totalmrc'))

    lastweekc = customer.objects.filter(creationdate__range=(range1, range2))
    lastweekcs = lastweekc.values('creator').annotate(Total=Count('id'))

    for person in allsalesman :
        allsalesmanid.append(person.id)

    for item in lastweekos :
        lastweekosid.append(item.get('salesman'))

    for item in lastweekcs :
        lastweekcsid.append(item.get('creator'))

    context = {'weekd':weekd,'lastweekos':lastweekos,'lastweeko':lastweeko,'allsalesman':allsalesman,'allsalesmanid':allsalesmanid,'lastweekosid':lastweekosid,'lastweekcs':lastweekcs,'lastweekc':lastweekc,'lastweekcsid':lastweekcsid}
    return render(request, 'crmapp/reportweaklastweek.html',context)

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
    cweek = thisweek = datetime.datetime.today().strftime("%U")
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')

    if cweek == 1 :
        lastweek = 52
    else:  #new
        lastweek = int(cweek)-1

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

    paginator = Paginator(thismontho,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)

    thisyearo = opportunity.objects.filter(creationdate__year=cyear)
    thisyearcount = thisyearo.count()
    thisyearsum = thisyearo.aggregate(Total=Sum('totalmrc'))
    thisyearosalesman = thisyearo.values('salesman').annotate(Total=Sum('totalmrc'))

    context = {'page':page,'opps':opps,'lastyearcount':lastyearcount,'lastmontho':lastmontho,'lastyearo':lastyearo,'lastyear':lastyear,'lastmonth':lastmonth,'ydayo':ydayo,'yday':yday,'todayo':todayo,'cday':cday,'cmonth':cmonth,'cyear':cyear,'categories':categories,'datesweeks':datesweeks,'datesmonths':datesmonths,'datesyears':datesyears,'allsalesmanvalueslist':allsalesmanvalueslist,'allsum':allsum,'allavg':allavg,'allsalesman':allsalesman,'all2':all2,'annotateex':annotateex,'allsalesmanvalues':allsalesmanvalues,'todayocount':todayocount,'todayosum':todayosum,'todayosalesman':todayosalesman,'ydayocount':ydayocount,'ydayosum':ydayosum,'ydayosalesman':ydayosalesman,'lastmonthcount':lastmonthcount,'lastmonthsum':lastmonthsum,'lastmonthosalesman':lastmonthosalesman,'lastyearcount':lastyearcount,'lastyearsum':lastyearsum,'lastyearosalesman':lastyearosalesman,'thismontho':thismontho,'thismonthcount':thismonthcount,'thismonthsum':thismonthsum,'thismonthosalesman':thismonthosalesman,'thisyearo':thisyearo,'thisyearcount':thisyearcount,'thisyearsum':thisyearsum,'thisyearosalesman':thisyearosalesman}
    return render(request, 'crmapp/report.html',context)

# dashboard start

@login_required
def dashboard(request):
    allavg = opportunity.objects.all().aggregate(Average_Price=Avg('totalmrc'))
    allsum = opportunity.objects.all().aggregate(Total=Sum('totalmrc'))
    allrev = opportunity.objects.all().aggregate(Total=Sum('revenue1'))
    allrev2 = order.objects.all().aggregate(Total=Sum('revenue2'))
    allrevp = order.objects.all().aggregate(Total=Sum('revenuep'))
    allpost = order.objects.filter(orderstatus='post').all().aggregate(Total=Sum('discountmrc'))
    target = 1500000




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

    sales_open_operation = opportunity.objects.filter(status__operationstatusname__icontains='open')

    thisyear_sales_validation = opportunity.objects.filter(status__operationstatusname__icontains='valid').filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))['Total']
    oldyear_sales_validation = opportunity.objects.filter(status__operationstatusname__icontains='valid').filter(creationdate__year__lt=cyear).aggregate(Total=Sum('totalmrc'))['Total']

    thisyear_document = opportunity.objects.filter(status__operationstatusname__icontains='Document').filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))['Total']
    oldyear_document = opportunity.objects.filter(status__operationstatusname__icontains='Document').filter(creationdate__year__lt=cyear).aggregate(Total=Sum('totalmrc'))['Total']

    thisyear_stcapproval = opportunity.objects.filter(status__operationstatusname__icontains='STC').filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))['Total']
    oldyear_stcapproval = opportunity.objects.filter(status__operationstatusname__icontains='STC').filter(creationdate__year__lt=cyear).aggregate(Total=Sum('totalmrc'))['Total']

    sales_open_operation = order.objects.filter(orderstatus='open').aggregate(Total=Sum('discountmrc'))['Total']

    thisyearopensales = thisyear_sales_validation + thisyear_document + thisyear_stcapproval + sales_open_operation
    oldyearopensales = oldyear_sales_validation + oldyear_document + oldyear_stcapproval

    cquarter = int(int(cmonth)/4)+1

    if cquarter == 1 :
        cquarterorders = order.objects.filter(activationdate__year=cyear).filter(activationdate__month__lt=4)
        rdays = 90 - int(datetime.datetime.today().strftime('%-j'))

    elif cquarter == 2 :
        cquarterorders = order.objects.filter(activationdate__year=cyear).filter(activationdate__month__lt=7).exclude(activationdate__month__lt=4)

        rdays = 181 - int(datetime.datetime.today().strftime('%-j'))
    elif cquarter == 3 :
        cquarterorders = order.objects.filter(activationdate__year=cyear).filter(activationdate__month__lt=11).exclude(activationdate__month__lt=8)
        rdays = 273 - int(datetime.datetime.today().strftime('%-j'))
    else:
        cquarterorders = order.objects.filter(activationdate__year=cyear).filter(activationdate__month__gt=9)
        rdays = 365 - int(datetime.datetime.today().strftime('%-j'))

    thisquarterNetMrc = cquarterorders.aggregate(Total=Sum('discountmrc'))['Total']



    x = datetime.date.today()

    myday1 = x.strftime("%A")
    myday = None

    if myday1 == 'Sunday':
        range1 = datetime.date.today() - timedelta(days=7)
        range2 = datetime.date.today() - timedelta(days=0)
        myday = myday1
        range3 = datetime.date.today()
        range4 = datetime.date.today() + timedelta(days=7)

    if myday1 == 'Monday':
        range1 = datetime.date.today() - timedelta(days=8)
        range2 = datetime.date.today() - timedelta(days=1)

        range3 = datetime.date.today() - timedelta(days=1)
        range4 = datetime.date.today() + timedelta(days=6)

    if myday1 == 'Tuesday':
        range1 = datetime.date.today() - timedelta(days=9)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=2)
        range4 = datetime.date.today() + timedelta(days=5)

    if myday1 == 'Wednesday':
        range1 = datetime.date.today() - timedelta(days=10)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=3)
        range4 = datetime.date.today() + timedelta(days=4)

    if myday1 == 'Thursday':
        range1 = datetime.date.today() - timedelta(days=11)
        range2 = datetime.date.today() - timedelta(days=4)

        range3 = datetime.date.today() - timedelta(days=4)
        range4 = datetime.date.today() + timedelta(days=3)

    if myday1 == 'Friday':
        range1 = datetime.date.today() - timedelta(days=12)
        range2 = datetime.date.today() - timedelta(days=5)

        range3 = datetime.date.today() - timedelta(days=5)
        range4 = datetime.date.today() + timedelta(days=2)

    if myday1 == 'Saturday':
        range1 = datetime.date.today() - timedelta(days=13)
        range2 = datetime.date.today() - timedelta(days=6)

        range3 = datetime.date.today() - timedelta(days=6)
        range4 = datetime.date.today() + timedelta(days=1)

    lastyear = int(cyear)-1

    lastyear = int(cyear)-1

    allopp = opportunity.objects.all()

    #Today

    todayo = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todayocount = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).count()
    todayosum = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))
    todayosalesman = todayo.values('salesman').annotate(Total=Sum('totalmrc'))
    todayorev = todayo.aggregate(Total=Sum('revenue1'))
    todayorders = order.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todaypostorders = order.objects.filter(activationdate__day=cday).filter(activationdate__month=cmonth).filter(activationdate__year=cyear)
    todayorev2 = todayorders.aggregate(Total=Sum('revenue2'))
    todayorevp = todayorders.aggregate(Total=Sum('revenuep'))
    todayc = customer.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).count()
    tpost = todaypostorders.aggregate(Total=Sum('discountmrc'))
    #Yesterday

    ydayo = opportunity.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear)
    ydayocount = ydayo.count()
    ydayosum = ydayo.aggregate(Total=Sum('totalmrc'))
    ydayosalesman = ydayo.values('salesman').annotate(Total=Sum('totalmrc'))
    ydayorev = ydayo.aggregate(Total=Sum('revenue1'))

    ydayorders = order.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear)
    ydaypostorders = order.objects.filter(activationdate__day=yday).filter(activationdate__month=ymonth).filter(activationdate__year=yyear)
    ydayorev2 = ydayorders.aggregate(Total=Sum('revenue2'))
    ydayorevp = ydayorders.aggregate(Total=Sum('revenuep'))
    ydayc = customer.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear).count()
    ypost = ydaypostorders.aggregate(Total=Sum('discountmrc'))

    #Week

    lastweeko = opportunity.objects.filter(creationdate__range=(range1, range2))

    lastweekcount = lastweeko.count()

    thisweeko = opportunity.objects.filter(creationdate__range=(range3, range4))
    thisweekcount = thisweeko.count()

    lastweeksum = lastweeko.aggregate(Total=Sum('totalmrc'))
    thisweeksum = thisweeko.aggregate(Total=Sum('totalmrc'))
    thisweekrev = thisweeko.aggregate(Total=Sum('revenue1'))
    lastweekrev = lastweeko.aggregate(Total=Sum('revenue1'))

    thisweekorders = order.objects.filter(creationdate__range=(range3, range4))
    thisweekpostorders = order.objects.filter(activationdate__range=(range3, range4))
    thisweekrev2 = thisweekorders.aggregate(Total=Sum('revenue2'))
    thisweekrevp = thisweekorders.aggregate(Total=Sum('revenuep'))

    thisweekc = customer.objects.filter(creationdate__range=(range3, range4)).count()

    lastweekorders = order.objects.filter(creationdate__range=(range1, range2))
    lastweekpostorders = order.objects.filter(activationdate__range=(range1, range2))
    lastweekrev2 = lastweekorders.aggregate(Total=Sum('revenue2'))
    lastweekrevp = lastweekorders.aggregate(Total=Sum('revenuep'))

    lastweekpost = lastweekpostorders.aggregate(Total=Sum('discountmrc'))
    thisweekpost = thisweekpostorders.aggregate(Total=Sum('discountmrc'))

    lastweekc = customer.objects.filter(creationdate__range=(range1, range2)).count()

    #Month

    if int(cmonth) == 1 :
        lastmonth = 12
    else:
        lastmonth = int(cmonth)-1

    if int(cmonth) ==1 :
        lastmontho = opportunity.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=lastyear)
    else:
        lastmontho = opportunity.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=cyear)

    thismonthc = customer.objects.filter(creationdate__month=cmonth).filter(creationdate__year=cyear).count()
    if cmonth ==1 :
        lastmonthc = customer.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=lastyear).count()
    else:
        lastmonthc = customer.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=cyear).count()
    thisyearc = customer.objects.filter(creationdate__year=cyear).count()
    lastyearc = customer.objects.filter(creationdate__year=lastyear).count()
    allc = customer.objects.all().count()

    thismontho = opportunity.objects.filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    thismonthcount = thismontho.count()
    thismonthsum = thismontho.aggregate(Total=Sum('totalmrc'))
    thismonthrev = thismontho.aggregate(Total=Sum('revenue1'))
    thismonthosalesman = thismontho.values('salesman').annotate(Total=Sum('totalmrc'))

    thismonthorders = order.objects.filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    thismonthpostorders = order.objects.filter(activationdate__month=cmonth).filter(activationdate__year=cyear)
    thismonthrev2 = thismonthorders.aggregate(Total=Sum('revenue2'))
    thismonthrevp = thismonthorders.aggregate(Total=Sum('revenuep'))
    thismonthpost = thismonthpostorders.aggregate(Total=Sum('discountmrc'))

    lastmonthcount = lastmontho.count()
    lastmonthsum = lastmontho.aggregate(Total=Sum('totalmrc'))
    lastmonthrev = lastmontho.aggregate(Total=Sum('revenue1'))
    lastmonthosalesman = lastmontho.values('salesman').annotate(Total=Sum('totalmrc'))

    if cmonth ==1 :
        lastmonthorders = order.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=lastyear)
        lastmonthpostorders = order.objects.filter(activationdate__month=lastmonth).filter(activationdate__year=lastyear)

    else:
        lastmonthorders = order.objects.filter(creationdate__month=lastmonth).filter(creationdate__year=cyear)
        lastmonthpostorders = order.objects.filter(activationdate__month=lastmonth).filter(activationdate__year=cyear)

    lastmonthrev2 = lastmonthorders.aggregate(Total=Sum('revenue2'))
    lastmonthrevp = lastmonthorders.aggregate(Total=Sum('revenuep'))

    lastmonthpost = lastmonthpostorders.aggregate(Total=Sum('discountmrc'))
    #Year

    thisyearo = opportunity.objects.filter(creationdate__year=cyear)
    thisyearcount = thisyearo.count()
    thisyearsum = thisyearo.aggregate(Total=Sum('totalmrc'))
    thisyearrev = thisyearo.aggregate(Total=Sum('revenue1'))
    thisyearosalesman = thisyearo.values('salesman').annotate(Total=Sum('totalmrc'))

    thisyearorders = order.objects.filter(creationdate__year=cyear)
    thisyearpostorders = order.objects.filter(activationdate__year=cyear).filter(orderstatus='post')
    thisyearrev2 = thisyearorders.aggregate(Total=Sum('revenue2'))
    thisyearrevp = thisyearorders.aggregate(Total=Sum('revenuep'))
    thisyearpost = thisyearpostorders.aggregate(Total=Sum('discountmrc'))

    lastyearo = opportunity.objects.filter(creationdate__year=lastyear)
    lastyearcount = lastyearo.count()
    lastyearsum = lastyearo.aggregate(Total=Sum('totalmrc'))
    lastyearrev = lastyearo.aggregate(Total=Sum('revenue1'))
    lastyearosalesman = lastyearo.values('salesman').annotate(Total=Sum('totalmrc'))

    lastyearorders = order.objects.filter(creationdate__year=lastyear)
    lastyearpostorders = order.objects.filter(activationdate__year=lastyear)
    lastyearrev2 = lastyearorders.aggregate(Total=Sum('revenue2'))
    lastyearrevp = lastyearorders.aggregate(Total=Sum('revenuep'))
    lastyearpost = lastyearpostorders.aggregate(Total=Sum('discountmrc'))

    if not thisquarterNetMrc:
        remainingtarget = target
    else:
        remainingtarget = target - thisquarterNetMrc

    targetach = 0
    if not thisyearrevp['Total']:
        targetach = 0
    else:
        if not thisquarterNetMrc:
            thisquarterNetMrc = 0
            targetach = 100*thisquarterNetMrc / target

    mmt=1
    for mm in range(13-int(cmonth)):
        mmt = mmt + mm



    rmsales = int(remainingtarget/rdays)

    context = {'thisyearopensales':thisyearopensales,'oldyearopensales':oldyearopensales,'thisyear_document':thisyear_document,'oldyear_document':oldyear_document,'oldyear_sales_validation':oldyear_sales_validation,'thisyear_sales_validation':thisyear_sales_validation,'sales_open_operation':sales_open_operation,'thisquarterNetMrc':thisquarterNetMrc,'cquarter':cquarter,'targetach':targetach,'target':target,'rmsales':rmsales,'mmt':mmt,'remainingtarget':remainingtarget,'lastyearpost':lastyearpost,'thisyearpost':thisyearpost,'lastmonthpost':lastmonthpost,'lastmonthpostorders':lastmonthpostorders,'thismonthpost':thismonthpost,'lastweekpost':lastweekpost,'thisweekpost':thisweekpost,'ypost':ypost,'tpost':tpost,'allpost':allpost,'lastmonth':lastmonth,'lastyearrevp':lastyearrevp,'lastyearrev2':lastyearrev2,'thisyearrevp':thisyearrevp,'thisyearrev2':thisyearrev2,'lastmonthrevp':lastmonthrevp,'lastmonthrev2':lastmonthrev2,'thismonthrevp':thismonthrevp,'thismonthrev2':thismonthrev2,'lastweekrevp':lastweekrevp,'lastweekrev2':lastweekrev2,'thisweekrevp':thisweekrevp,'thisweekrev2':thisweekrev2,'ydayorevp':ydayorevp,'ydayorev2':ydayorev2,'todayorevp':todayorevp,'todayorev2':todayorev2,'allrevp':allrevp,'allrev2':allrev2,'allrev':allrev,'thisyearrev':thisyearrev,'lastyearrev':lastyearrev,'lastmonthrev':lastmonthrev,'thismonthrev':thismonthrev,'lastweekrev':lastweekrev,'thisweekrev':thisweekrev,'todayorev':todayorev,'ydayorev':ydayorev,'myday':myday,'allopp':allopp,'lastyearcount':lastyearcount,'lastmontho':lastmontho,'lastyearo':lastyearo,'lastyear':lastyear,'lastmonth':lastmonth,'ydayo':ydayo,'yday':yday,'todayo':todayo,'cday':cday,'cmonth':cmonth,'cyear':cyear,'categories':categories,'datesweeks':datesweeks,'datesmonths':datesmonths,'datesyears':datesyears,'allsum':allsum,'allavg':allavg,'allsalesman':allsalesman,'todayocount':todayocount,'todayosum':todayosum,'todayosalesman':todayosalesman,'ydayocount':ydayocount,'ydayosum':ydayosum,'ydayosalesman':ydayosalesman,'lastmonthcount':lastmonthcount,'lastmonthsum':lastmonthsum,'lastmonthosalesman':lastmonthosalesman,'lastyearcount':lastyearcount,'lastyearsum':lastyearsum,'lastyearosalesman':lastyearosalesman,'thismontho':thismontho,'thismonthcount':thismonthcount,'thismonthsum':thismonthsum,'thismonthosalesman':thismonthosalesman,'thisyearo':thisyearo,'thisyearcount':thisyearcount,'thisyearsum':thisyearsum,'thisyearosalesman':thisyearosalesman,'thisweeko':thisweeko,'thisweekcount':thisweekcount,'lastweeko':lastweeko,'lastweekcount':lastweekcount,'thisweeksum':thisweeksum,'lastweeksum':lastweeksum,'todayc':todayc,'ydayc':ydayc,'thisweekc':thisweekc,'lastweekc':lastweekc,'thismonthc':thismonthc,'lastmonthc':lastmonthc,'thisyearc':thisyearc,'lastyearc':lastyearc,'allc':allc}
    return render(request, 'crmapp/dashboard.html',context)

def todayop(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    x = datetime.date.today()
    myday1 = x.strftime("%A")
    myday = None
    todayop = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todayocount = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).count()
    todayosum = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))
    todayosalesman = todayop.values('salesman').annotate(Total=Sum('totalmrc'))
    todayorev = todayop.aggregate(Total=Sum('revenue1'))
    todayorders = order.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todaypostorders = order.objects.filter(activationdate__day=cday).filter(activationdate__month=cmonth).filter(activationdate__year=cyear)
    todayorev2 = todayorders.aggregate(Total=Sum('revenue2'))
    todayorevp = todayorders.aggregate(Total=Sum('revenuep'))
    todayc = customer.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).count()
    tpost = todaypostorders.aggregate(Total=Sum('discountmrc'))


    context = {'todayop':todayop}
    return render(request, 'crmapp/todayop.html',context)

def todaypmrc(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    x = datetime.date.today()
    myday1 = x.strftime("%A")
    lastyear = int(cyear)-1
    lastyear = int(cyear)-1
    todayop = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todayosum = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))
    todayosalesman = todayop.values('salesman').annotate(Total=Sum('totalmrc'))
    todayorders = order.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todaypostorders = order.objects.filter(activationdate__day=cday).filter(activationdate__month=cmonth).filter(activationdate__year=cyear)
    todayc = customer.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    context = {'todaypostorders':todaypostorders}
    return render(request, 'crmapp/todaypmrc.html',context)

def todayc(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    x = datetime.date.today()
    myday1 = x.strftime("%A")
    lastyear = int(cyear)-1
    lastyear = int(cyear)-1
    todayop = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todayosum = opportunity.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear).aggregate(Total=Sum('totalmrc'))
    todayosalesman = todayop.values('salesman').annotate(Total=Sum('totalmrc'))
    todayorders = order.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    todaypostorders = order.objects.filter(activationdate__day=cday).filter(activationdate__month=cmonth).filter(activationdate__year=cyear)
    todayc = customer.objects.filter(creationdate__day=cday).filter(creationdate__month=cmonth).filter(creationdate__year=cyear)
    context = {'todayc':todayc}
    return render(request, 'crmapp/todayc.html',context)

def yesterdayop(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    x = datetime.date.today()
    myday1 = x.strftime("%A")
    myday = None
    lastyear = int(cyear)-1
    lastyear = int(cyear)-1
    ydayo = opportunity.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear)
    context = {'ydayo':ydayo}
    return render(request, 'crmapp/yesterdayop.html',context)

def yesterdaypostorders(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    x = datetime.date.today()
    myday1 = x.strftime("%A")
    yesterdaypostorders = order.objects.filter(activationdate__day=yday).filter(activationdate__month=ymonth).filter(activationdate__year=yyear)
    context = {'yesterdaypostorders':yesterdaypostorders}
    return render(request, 'crmapp/yesterdaypostorders.html',context)

def yesterdaycustomers(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    x = datetime.date.today()
    myday1 = x.strftime("%A")
    yesterdaycustomers = customer.objects.filter(creationdate__day=yday).filter(creationdate__month=ymonth).filter(creationdate__year=yyear)
    context = {'yesterdaycustomers':yesterdaycustomers}
    return render(request, 'crmapp/yesterdaycustomers.html',context)

def thisweekop(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')

    x = datetime.date.today()

    myday1 = x.strftime("%A")
    myday = None

    if myday1 == 'Sunday':
        range1 = datetime.date.today() - timedelta(days=7)
        range2 = datetime.date.today() - timedelta(days=0)
        myday = myday1
        range3 = datetime.date.today()
        range4 = datetime.date.today() + timedelta(days=7)

    if myday1 == 'Monday':
        range1 = datetime.date.today() - timedelta(days=8)
        range2 = datetime.date.today() - timedelta(days=1)

        range3 = datetime.date.today() - timedelta(days=1)
        range4 = datetime.date.today() + timedelta(days=6)

    if myday1 == 'Tuesday':
        range1 = datetime.date.today() - timedelta(days=9)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=2)
        range4 = datetime.date.today() + timedelta(days=5)

    if myday1 == 'Wednesday':
        range1 = datetime.date.today() - timedelta(days=10)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=3)
        range4 = datetime.date.today() + timedelta(days=4)

    if myday1 == 'Thursday':
        range1 = datetime.date.today() - timedelta(days=11)
        range2 = datetime.date.today() - timedelta(days=4)

        range3 = datetime.date.today() - timedelta(days=4)
        range4 = datetime.date.today() + timedelta(days=3)

    if myday1 == 'Friday':
        range1 = datetime.date.today() - timedelta(days=12)
        range2 = datetime.date.today() - timedelta(days=5)

        range3 = datetime.date.today() - timedelta(days=5)
        range4 = datetime.date.today() + timedelta(days=2)

    if myday1 == 'Saturday':
        range1 = datetime.date.today() - timedelta(days=13)
        range2 = datetime.date.today() - timedelta(days=6)

        range3 = datetime.date.today() - timedelta(days=6)
        range4 = datetime.date.today() + timedelta(days=1)

    lastyear = int(cyear)-1

    lastyear = int(cyear)-1



    #Week
    lastweekop = opportunity.objects.filter(creationdate__range=(range1, range2))

    thisweekop = opportunity.objects.filter(creationdate__range=(range3, range4))

    thisweekorders = order.objects.filter(creationdate__range=(range3, range4))
    thisweekpostorders = order.objects.filter(activationdate__range=(range3, range4))

    thisweekc = customer.objects.filter(creationdate__range=(range3, range4)).count()
    lastweekorders = order.objects.filter(creationdate__range=(range1, range2))
    lastweekpostorders = order.objects.filter(activationdate__range=(range1, range2))


    lastweekc = customer.objects.filter(creationdate__range=(range1, range2)).count()



    context = {'thisweekop':thisweekop}
    return render(request, 'crmapp/thisweeko.html',context)

def thisweekpostorders(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')

    x = datetime.date.today()

    myday1 = x.strftime("%A")
    myday = None

    if myday1 == 'Sunday':
        range1 = datetime.date.today() - timedelta(days=7)
        range2 = datetime.date.today() - timedelta(days=0)
        myday = myday1
        range3 = datetime.date.today()
        range4 = datetime.date.today() + timedelta(days=7)

    if myday1 == 'Monday':
        range1 = datetime.date.today() - timedelta(days=8)
        range2 = datetime.date.today() - timedelta(days=1)

        range3 = datetime.date.today() - timedelta(days=1)
        range4 = datetime.date.today() + timedelta(days=6)

    if myday1 == 'Tuesday':
        range1 = datetime.date.today() - timedelta(days=9)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=2)
        range4 = datetime.date.today() + timedelta(days=5)

    if myday1 == 'Wednesday':
        range1 = datetime.date.today() - timedelta(days=10)
        range2 = datetime.date.today() - timedelta(days=2)

        range3 = datetime.date.today() - timedelta(days=3)
        range4 = datetime.date.today() + timedelta(days=4)

    if myday1 == 'Thursday':
        range1 = datetime.date.today() - timedelta(days=11)
        range2 = datetime.date.today() - timedelta(days=4)

        range3 = datetime.date.today() - timedelta(days=4)
        range4 = datetime.date.today() + timedelta(days=3)

    if myday1 == 'Friday':
        range1 = datetime.date.today() - timedelta(days=12)
        range2 = datetime.date.today() - timedelta(days=5)

        range3 = datetime.date.today() - timedelta(days=5)
        range4 = datetime.date.today() + timedelta(days=2)

    if myday1 == 'Saturday':
        range1 = datetime.date.today() - timedelta(days=13)
        range2 = datetime.date.today() - timedelta(days=6)

        range3 = datetime.date.today() - timedelta(days=6)
        range4 = datetime.date.today() + timedelta(days=1)

    lastyear = int(cyear)-1

    lastyear = int(cyear)-1



    #Week
    lastweekop = opportunity.objects.filter(creationdate__range=(range1, range2))

    thisweekop = opportunity.objects.filter(creationdate__range=(range3, range4))

    thisweekorders = order.objects.filter(creationdate__range=(range3, range4))
    thisweekpostorders = order.objects.filter(activationdate__range=(range3, range4))

    thisweekc = customer.objects.filter(creationdate__range=(range3, range4)).count()
    lastweekorders = order.objects.filter(creationdate__range=(range1, range2))
    lastweekpostorders = order.objects.filter(activationdate__range=(range1, range2))


    lastweekc = customer.objects.filter(creationdate__range=(range1, range2)).count()



    context = {'thisweekpostorders':thisweekpostorders}
    return render(request, 'crmapp/thisweekpostorders.html',context)



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

class CreateinvoiceView(CreateView):
    redirect_field_name = 'crmapp/invoice_detail.html'
    form_class = invoicesForm
    model = invoices

@login_required
def invoicenew(request):
    if request.method=='POST':
        form = invoicesForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.save()
            pk = myform.id
            return HttpResponseRedirect(reverse('invoicedetail', args=(pk,)))

    else:
        form = invoicesForm()
    return render(request, 'crmapp/invoices_form.html',{'form':form})

class invoiceDetailView(DetailView):
    model = invoices

class invoiceUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/invoices_detail.html'
    form_class = invoicesForm
    model = invoices

class addservicesUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/addservices_detail.html'
    form_class = addservicesForm
    model = addservices

@login_required
def invoiceslist(request):
    invoiceslist = invoices.objects.all().order_by('-creationdate')
    context = {'invoiceslist':invoiceslist}
    return render(request, 'crmapp/invoiceslist.html',context)

@login_required
def expensecategorynew(request):
    if request.method=='POST':
        form = expensecategoryForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.save()
            pk = myform.id
            return HttpResponseRedirect(reverse('expensecategorydetail', args=(pk,)))

    else:
        form = expensecategoryForm()
    return render(request, 'crmapp/expensecategory_form.html',{'form':form})

class expensecategoryDetailView(DetailView):
    model = expensecategory

class expensecategoryUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/expensecategory_detail.html'
    form_class = expensecategoryForm
    model = expensecategory

@login_required
def expensecategorylist(request):
    expensecategorylist = expensecategory.objects.all().order_by('expensecategoryname')
    context = {'expensecategorylist':expensecategorylist}
    return render(request, 'crmapp/expensecategorylist.html',context)


@login_required
def expensesnew(request):
    if request.method=='POST':
        form = expensesForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.save()
            pk = myform.id
            return HttpResponseRedirect(reverse('expensesdetail', args=(pk,)))

    else:
        form = expensesForm()
    return render(request, 'crmapp/expenses_form.html',{'form':form})

class expensesDetailView(DetailView):
    model = expenses


class expensesUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/expenses_detail.html'
    form_class = expensesForm
    model = expenses

@login_required
def expenseslist(request):
    expenseslist = expenses.objects.all().order_by('-creationdate')
    context = {'expenseslist':expenseslist}
    return render(request, 'crmapp/expenseslist.html',context)


@login_required
def expensestotal(request):
    expenseslist = expenses.objects.all()
    invoiceslist = invoices.objects.all()
    allyears = yearslist.objects.all()
    allyearsc = allyears.count()

    allyearsyears = []
    allyearslist = []
    expenseslist2 = []
    invoiceslist2 = []
    expensestable = {}
    expensestotal = expenseslist.values('year').annotate(Total=Sum('amount'))
    invoicestotal = invoiceslist.values('relatedyear').annotate(Total=Sum('amount'))

    for item in allyears:
        allyearslist.append(item.id)


    for item in expensestotal:
        expenseslist2.append(item.get('year'))

    for item in invoicestotal:
        invoiceslist2.append(item.get('relatedyear'))

    invo=[]
    exp=[]
    for item in allyearslist :

        item2 = get_object_or_404(yearslist,pk=item).yeardetail

        if item2 in invoiceslist2:


            allyearsyears.append(item2)
            invo.append(invoices.objects.filter(relatedyear=item2).values('relatedyear').annotate(Total=Sum('amount'))[0]['Total'])
        else:
            invo.append(0)

        if item in expenseslist2:
            exp.append(expenses.objects.filter(year=item).values('year').annotate(Total=Sum('amount'))[0]['Total'])
        else:
            exp.append(0)


    context = {'allyearsyears':allyearsyears,'n':range(allyearsc),'invo':invo,'item':item,'exp':exp,'allyearslist':allyearslist,'invoiceslist2':invoiceslist2,'expenseslist2':expenseslist2,'expensestable':expensestable,'allyearsc':allyearsc,'expensestotal':expensestotal,'allyears':allyears,'invoicestotal':invoicestotal}
    return render(request, 'crmapp/expensesreport.html',context)

class opportunityDeleteView(DeleteView):
    model = opportunity
    success_url = reverse_lazy('opportunitylist')

#new
class addservicesDetailView(DetailView):
    model = addservices

class addservicesDeleteView(DeleteView):
    model = addservices
    success_url = reverse_lazy('opportunitylist')

class orderDeleteView(DeleteView):
    model = order
    success_url = reverse_lazy('opportunitylist')

def orderdelete(request,pk):
    obj = get_object_or_404(order,pk=pk)
    addservice=obj.addservices
    addservicesobject = get_object_or_404(addservices,pk=addservice.id)

    if request.method =='POST':
        obj.delete()
        addservicesobject.save()
        return redirect('opportunitydetail', pk=obj.opportunity.id)

    context = {"object":obj}
    return render(request,'crmapp/order_confirm_delete.html',context)

def addservicesdelete(request,pk):
    obj = get_object_or_404(addservices,pk=pk)
    opportunity1=obj.opportunity
    opportunityobject = get_object_or_404(opportunity,pk=opportunity1.id)

    if request.method =='POST':
        obj.delete()
        opportunityobject.save()
        return redirect('opportunitydetail', pk=opportunity1.id)

    context = {"object":obj}
    return render(request,'crmapp/order_confirm_delete.html',context)

def orderdouble1(request,pk,pk1):
    if request.method=='POST':
        form = orderdouble1Form(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.operationexecutive=request.user
            opportunity1 = get_object_or_404(opportunity,pk=pk)
            order1 = get_object_or_404(order,pk=pk1)
            addservices_id = order1.addservices.id
            addservices1 = get_object_or_404(addservices,pk=int(addservices_id))
            if addservices1.createdservices < addservices1.noofservices:
                addservices1.save()
                myform.opportunity=opportunity1

                myform.service=order1.service
                myform.dealcategory=order1.dealcategory
                myform.addservices=order1.addservices
                myform.orderno=order1.orderno
                myform.save()
                addservices1.save()
                return redirect('orderdetail', pk=pk1)

    else:
        form = orderdouble1Form()
    return render(request, 'crmapp/order_form.html',{'form':form})

def orderdouble2(request,pk,pk1):
    if request.method=='POST':
        form = orderdouble2Form(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.operationexecutive=request.user
            opportunity1 = get_object_or_404(opportunity,pk=pk)
            order1 = get_object_or_404(order,pk=pk1)
            addservices_id = order1.addservices.id
            addservices1 = get_object_or_404(addservices,pk=int(addservices_id))
            if addservices1.createdservices < addservices1.noofservices:
                addservices1.save()
                myform.opportunity=opportunity1

                myform.service=order1.service
                myform.dealcategory=order1.dealcategory
                myform.addservices=order1.addservices
                myform.orderdate = order1.orderdate
                myform.save()
                addservices1.save()
                return redirect('orderdetail', pk=pk1)

    else:
        form = orderdouble2Form()
    return render(request, 'crmapp/order_form.html',{'form':form})

def productreport(request):
    productlist = addservices.objects.all()
    servicelist = service.objects.all()
    productreport = productlist.values('service').annotate(Total=Sum('noofservices')).order_by('-Total')
    context = {'servicelist':servicelist,'productreport':productreport}
    return render(request, 'crmapp/productreport.html',context)

def sourcereport(request):
    allcustomers = customer.objects.all()
    sourcelist = leadsource.objects.all()
    sourcereport = allcustomers.values('source').annotate(Total=Count('id'))

    context = {'sourcereport':sourcereport,'sourcelist':sourcelist}
    return render(request, 'crmapp/sourcereport.html',context)

def opportunityhotlead(request):
    aa = get_object_or_404(leadsource,leadsourcename='STC Hot Lead')
    opportunityhotlead = opportunity.objects.filter(source=aa.id)
    context = {'opportunityhotlead':opportunityhotlead}
    return render(request, 'crmapp/opportunityhotlead.html',context)

def customeroneback(request):
    aa = get_object_or_404(leadsource,leadsourcename='One Back')
    customeroneback = customer.objects.filter(source=aa.id)
    creatorreport = customeroneback.values('creator').annotate(Total=Count('id'))
    dic2 = []
    dic3 = []
    dic4 = {}
    for xx in creatorreport:
        aa = xx["creator"]
        uu = get_object_or_404(User,id=aa)
        nn = uu.username
        dic2.append(nn)
        dic3.append(xx['Total'])
        dic4.update({nn:xx['Total']})

    context = {'customeroneback':customeroneback,'creatorreport':creatorreport,'dic2':dic2,'dic3':dic3,'dic4':dic4}
    return render(request, 'crmapp/customeroneback.html',context)

def assignedto(request,pk):
    if request.method=='POST':
        mycustomer = get_object_or_404(customer, pk = pk)
        form = customerassigningForm(request.POST or None, instance = mycustomer)
        if form.is_valid():
            form.save()
            pk = pk
            return HttpResponseRedirect(reverse('customerdetail', args=(pk,)))

    else:
        form = customerassigningForm()
    return render(request, 'crmapp/customer_form.html',{'form':form})

@login_required
def pipeline(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    pipeline = opportunity.objects.filter(Q(status =2) | Q(status=3) | Q(status=1) | Q(status=4)).filter(creationdate__year=cyear).order_by('-creationdate')
    mrcsumoo = pipeline.aggregate(Sum('totalmrc'))
    mrcsumo = mrcsumoo['totalmrc__sum']
    context = {'pipeline':pipeline,'mrcsumo':mrcsumo}
    return render(request, 'crmapp/pipeline.html',context)

@login_required
def megapipeline(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    megapipeline = opportunity.objects.filter(Q(status =2) | Q(status=3) | Q(status=1) | Q(status=4)).filter(creationdate__year=cyear).filter(totalmrc__gt=20000).filter(creationdate__year=cyear).order_by('-totalmrc')
    mrcsumoo = megapipeline.aggregate(Sum('totalmrc'))
    mrcsumo = mrcsumoo['totalmrc__sum']
    context = {'megapipeline':megapipeline,'mrcsumo':mrcsumo}
    return render(request, 'crmapp/megapipeline.html',context)

@login_required
def operationreport(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    cmonth =  datetime.datetime.today().strftime('%m')
    cday =  datetime.datetime.today().strftime('%d')
    yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    cdo = order.objects.filter(creationdate__year=cyear).filter(creationdate__month=cmonth).filter(creationdate__day=cday).order_by('-creationdate') #current day operation
    ydo = order.objects.filter(creationdate__year=yyear).filter(creationdate__month=ymonth).filter(creationdate__day=yday).order_by('-creationdate') #yesterday  operation

    monthlyorders = order.objects.all().values('creationdate__year', 'creationdate__month','operationexecutive').annotate(count=Count('id')).order_by('-creationdate__year','-creationdate__month','-count')
    allusers = User.objects.all()


    cdos = cdo.aggregate(Sum('discountmrc'))
    cdost = cdos['discountmrc__sum']

    ydos = ydo.aggregate(Sum('discountmrc'))
    ydost = ydos['discountmrc__sum']

    context = {'cdo':cdo,'ydo':ydo,'cdost':cdost,'ydost':ydost,'monthlyorders':monthlyorders,'allusers':allusers}
    return render(request, 'crmapp/operationreport.html',context)

@login_required
def salesmandetail(request,pk):
    cyear =  datetime.datetime.today().strftime('%Y')
    customerme = customer.objects.filter(creationdate__year=cyear).filter(creator=pk).all()
    opportunityme = opportunity.objects.filter(salesman=pk).filter(creationdate__year=cyear).all()
    opportunitymes = opportunityme.aggregate(Sum('totalmrc'))
    opportunitymest= opportunitymes['totalmrc__sum']
    nameme = User.objects.filter(pk=pk)
    orderme = order.objects.filter(opportunity__salesman=pk).filter(creationdate__year=cyear).all()
    ordermes = orderme.aggregate(Sum('mrc'))
    ordermest= ordermes['mrc__sum']
    ordermepost = order.objects.filter(opportunity__salesman=pk).filter(orderstatus='post').filter(activationdate__year=cyear).all()
    ordermeposts = ordermepost.aggregate(Sum('mrc'))
    ordermepostst= ordermeposts['mrc__sum']
    orderpostrevenue = ordermepost.aggregate(Sum('revenuep'))
    orderpostrevenuet = orderpostrevenue['revenuep__sum']
    myaddservices = addservices.objects.filter(opportunity__salesman=pk).filter(creationdate__year=cyear).all()
    myoperationstatus= operationstatus.objects.all()
    oppstages = opportunityme.values('status').annotate(Total=Sum('totalmrc'))
    ordservicecategory = myaddservices.values('servicecategory').annotate(Total=Sum('totalmrc'))
    myreport = ordermepost.values('activationdate__year', 'activationdate__month').annotate(count=Sum('mrc'))
    myreport2 = opportunityme.values('creationdate__year', 'creationdate__month').annotate(count=Sum('totalmrc'))

    list1= myreport.values_list('activationdate__month', flat=True)
    list2= myreport.values_list('count', flat=True)
    list3= myreport2.values_list('count', flat=True)
    list4 = zip(list1,list2,list3)

    # cyear =  datetime.datetime.today().strftime('%Y')
    # cmonth =  datetime.datetime.today().strftime('%m')
    # cday =  datetime.datetime.today().strftime('%d')
    # yday = (datetime.date.today() - timedelta(days=1)).strftime('%d')
    # ymonth = (datetime.date.today() - timedelta(days=1)).strftime('%m')
    # yyear = (datetime.date.today() - timedelta(days=1)).strftime('%Y')
    # cdo = order.objects.filter(creationdate__year=cyear).filter(creationdate__month=cmonth).filter(creationdate__day=cday).order_by('-creationdate') #current day operation
    # ydo = order.objects.filter(creationdate__year=yyear).filter(creationdate__month=ymonth).filter(creationdate__day=yday).order_by('-creationdate') #yesterday  operation
    # cdos = cdo.aggregate(Sum('mrc'))
    # cdost = cdos['mrc__sum']
    # ydos = ydo.aggregate(Sum('mrc'))
    # ydost = ydos['mrc__sum']
    myday = int(datetime.datetime.today().strftime('%j'))
    if customerme :
        wcustomer = 7*customerme.count()/myday
    else:
        wcustomer = 0

    if opportunityme :

        wopportunity = 7*opportunityme.count()/myday
    else:
        wopportunity = 0

    if opportunitymest :
        wopportunitymest = 7*opportunitymest/myday
    else:
        wopportunitymest = 0

    if orderme :
        worderme = 7*orderme.count()/myday
    else:
        worderme = 0

    if ordermest :
        wordermest = 7*ordermest/myday
    else:
        wordermest = 0

    if ordermepost :
        wordermepost = 7*ordermepost.count()/myday
    else:
        wordermepost = 0

    if ordermepostst :
        wordermepostst = 7*ordermepostst/myday
    else:
        wordermepostst = 0

    if orderpostrevenuet :
        worderpostrevenuet = 7*orderpostrevenuet/myday
    else:
        worderpostrevenuet = 0

    context = {'opportunityme':opportunityme,'list4':list4,'list3':list3,'list2':list2,'list1':list1,'myreport2':myreport2,'myreport':myreport,'pk1':pk,'myoperationstatus':myoperationstatus,'ordservicecategory':ordservicecategory,'oppstages':oppstages,'worderpostrevenuet':worderpostrevenuet,'wordermepostst':wordermepostst,'wordermepost':wordermepost,'wordermest':wordermest,'worderme':worderme,'wopportunitymest':wopportunitymest,'wopportunity':wopportunity,'wcustomer':wcustomer,'myday':myday,'orderpostrevenuet':orderpostrevenuet,'ordermepostst':ordermepostst,'ordermest':ordermest,'opportunitymest':opportunitymest,'ordermepost':ordermepost,'customerme':customerme,'opportunityme':opportunityme,'orderme':orderme,'nameme':nameme,'cyear':cyear}
    return render(request, 'crmapp/salesmanreport.html',context)

@login_required
def salesteam(request):
    salesteamlist =  User.objects.filter(user_profile__jobtitle='SalesExecutive').filter(is_active=True)
    mylist = []
    for xx in salesteamlist:
        mydic = {}
        thisopp = opportunity.objects.filter(salesman = xx.id).filter(creationdate__year=2022)
        thisopps = thisopp.aggregate(Sum('totalmrc'))
        thisoppst = thisopps['totalmrc__sum']
        thisor = order.objects.filter(opportunity_id__salesman = xx.id).filter(activationdate__year=2022).filter(orderstatus='post').all()
        thisors = thisor.aggregate(Sum('mrc'))
        thisorst = thisors['mrc__sum']
        mydic.update({"idd": xx.id})
        mydic.update({"name": xx.username})
        mydic.update({"mrc": thisoppst})
        mydic.update({"post": thisorst})
        mylist.append(mydic)
    context = {'salesteamlist':salesteamlist,'mydic':mydic,'mylist':mylist}
    return render(request, 'crmapp/salesteam.html',context)

@login_required
def operationstages(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    myopportunities =  opportunity.objects.filter(creationdate__year__lte=cyear)
    mysome = opportunity.objects.filter(status=12)
    for som in mysome:
        som.save()
    myoperationstatus= operationstatus.objects.all()
    myopportunitiessum = myopportunities.values('status').annotate(Total=Sum('totalmrc'))
    context = {'cyear':cyear,'myoperationstatus':myoperationstatus,'myopportunitiessum':myopportunitiessum}
    return render(request, 'crmapp/operationstages.html',context)

@login_required
def operationstagedetail(request,pk):
    cyear =  datetime.datetime.today().strftime('%Y')
    mystatus = get_object_or_404(operationstatus,pk=pk)
    myopportunities =  opportunity.objects.filter(creationdate__year=cyear).filter(status=mystatus).order_by('-totalmrc')
    summ = myopportunities.aggregate(Sum('totalmrc'))['totalmrc__sum']
    context = {'cyear':cyear,'summ':summ,'myopportunities':myopportunities,'mystatus':mystatus}
    return render(request, 'crmapp/operationstagedetail.html',context)

@login_required
def check(request):
    opps =  opportunity.objects.all()
    for xx in opps:
        mypartner = partner.objects.get(id=1)
        xx.partner = mypartner
        xx.save()
    return render(request, 'crmapp/operationstagedetail.html')

@login_required
def opportunitynotesn(request,pk):
    if request.method=='POST':
        form = opportunitynotesForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            opportunity1 = get_object_or_404(opportunity,pk=pk)
            myform.opportunity=opportunity1
            myform.save()
            pk = pk
            return HttpResponseRedirect(reverse('opportunitydetail', args=(pk,)))

    else:
        form = opportunitynotesForm()
    return render(request, 'crmapp/opportunitynotes_form.html',{'form':form})

@login_required
def salesmanoperationstage(request,pk,pk1):
    cyear =  datetime.datetime.today().strftime('%Y')
    mystatus = get_object_or_404(operationstatus,pk=pk)
    myopportunities =  opportunity.objects.filter(creationdate__year=cyear).filter(status=mystatus).filter(salesman=pk1).order_by('-totalmrc')
    summ = myopportunities.aggregate(Sum('totalmrc'))['totalmrc__sum']
    context = {'cyear':cyear,'summ':summ,'myopportunities':myopportunities,'mystatus':mystatus}
    return render(request, 'crmapp/salesmanoperationstage.html',context)

@login_required
def postordersnodate(request):
    orderpostlist = order.objects.all().filter(orderstatus='post').filter(activationdate__isnull=True).order_by('-creationdate')
    mrcsumoo = orderpostlist.aggregate(Sum('mrc'))
    mrcsumo = mrcsumoo['mrc__sum']
    context = {'orderpostlist':orderpostlist,'mrcsumo':mrcsumo}
    return render(request, 'crmapp/postordersnodate.html',context)

@login_required
def partners(request):
    salesteamlist =  User.objects.filter(user_profile__jobtitle='PSalesExecutive').filter(is_active=True)
    mylist = []
    for xx in salesteamlist:
        mydic = {}
        thisopp = opportunity.objects.filter(salesman = xx.id).filter(creationdate__year=2022)
        thisopps = thisopp.aggregate(Sum('totalmrc'))
        thisoppst = thisopps['totalmrc__sum']
        thisor = order.objects.filter(opportunity_id__salesman = xx.id).filter(activationdate__year=2022).filter(orderstatus='post').all()
        thisors = thisor.aggregate(Sum('mrc'))
        thisorst = thisors['mrc__sum']
        mydic.update({"idd": xx.id})
        mydic.update({"name": xx.username})
        mydic.update({"mrc": thisoppst})
        mydic.update({"post": thisorst})
        mylist.append(mydic)
    context = {'salesteamlist':salesteamlist,'mydic':mydic,'mylist':mylist}
    return render(request, 'crmapp/partners.html',context)

@login_required
def dealnew(request):
    if request.method=='POST':
        form = fastdatadForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            myform.broker=request.user
            myform.save()

            return HttpResponseRedirect(reverse('dealslist'))
    else:
        form = fastdatadForm()
    return render(request, 'crmapp/fastdatad_form.html',{'form':form})

@login_required
def dealslist(request):
    dealslist1 = fastdatad.objects.all().order_by('-creationdate').order_by('customer','activationdate')
    for xx in dealslist1:
        xx.save()
    summ = dealslist1.aggregate(Sum('totalmrc'))['totalmrc__sum']
    deals2020 = fastdatad.objects.filter(activationdate__year__lte=2020).filter(cancellationdate__isnull=True).filter(commissiontype='monthly')
    deals2020_sum = deals2020.aggregate(Sum('totalmrc'))['totalmrc__sum']
    deals2020_rsum = deals2020.aggregate(Sum('revenuep'))['revenuep__sum']
    deals_rsum = dealslist1.aggregate(Sum('revenuep'))['revenuep__sum']
    deals_ourrsum = 0.15*deals_rsum
    context = {'deals_ourrsum':deals_ourrsum,'dealslist1':dealslist1,'summ':summ,'deals2020':deals2020,'deals2020_sum':deals2020_sum,'deals2020_rsum':deals2020_rsum,'deals_rsum':deals_rsum}
    return render(request, 'crmapp/dealslist.html',context)

@login_required
def dealdetail(request,pk):
    dealnow = get_object_or_404(fastdatad,pk=pk)
    context = {'dealnow':dealnow}
    return render(request, 'crmapp/deal_detail.html',context)

class fastdatadUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/deal_detail.html'
    form_class = fastdatadForm
    model = fastdatad

class fastdatadDeleteView(DeleteView):
    model = fastdatad
    success_url = reverse_lazy('dealslist')

@login_required
def bulkorderupdate(request):


    xx = get_object_or_404(opportunity,opportunityno=20210456)
    oo = order.objects.filter(opportunity=xx)
    for ord in oo:
        ord.activationdate = ord.creationdate
        ord.orderstatus = 'post'
        ord.save()


    # order.objects.filter(opportunity=xx,creationdate__year=2021,creationdate__month=8,creationdate=19).update(orderstatus='post',activationdate=datetime.date(2021, 8, 19))


    # oo = order.objects.filter(opportunity=xx)
    # for ooo in oo:
    #     ooo.save()
    # # oo = order.objects.filter(opportunity=xx,creationdate=datetime.date(2021, 8, 12)).first()
    # # opp = oo.opportunity
    # # xx = get_object_or_404(opportunity,opportunityno=opp.opportunityno)
    xx.save()

    return redirect('opportunitydetail', pk=xx.pk)







    return redirect('orderdetail', pk=oo.pk)

@login_required
def checkv(request):

    checkl = get_object_or_404(opportunity,opportunityno=20210224)
    opportunityorderspost =checkl.opportunity_orders.filter(orderstatus='post').all()
    opportunityservices = checkl.opportunity_addservices.all()
    allservices = opportunityservices.aggregate(Sum('noofservices'))['noofservices__sum']
    context = {'allservices':allservices,'checkl':checkl,'opportunityorderspost':opportunityorderspost,'opportunityservices':opportunityservices}

    return render(request, 'crmapp/checkl.html',context)

@login_required
def cctv(request):

    cctvs  = get_object_or_404(service,servicename='CCTV')
    cctvservices = addservices.objects.filter(service=cctvs)
    context = {'cctvservices':cctvservices}

    return render(request, 'crmapp/cctv.html',context)



@login_required
def fservicelist(request):
    fservicelist = fservice.objects.all().order_by('servicename')
    context = {'fservicelist':fservicelist}
    return render(request, 'crmapp/fservicelist.html',context)

class CreatefserviceView(CreateView):
    redirect_field_name = 'crmapp/fservicelist.html'
    form_class = fserviceForm
    model = fservice

class fserviceUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/fservice_detail.html'
    form_class = fserviceForm
    model = fservice

class fserviceDetailView(DetailView):
    model = fservice

@login_required
def finvoicelist(request):
    finvoicelist = finvoice.objects.all().order_by('-year')
    if not finvoicelist:
        year = 2021
        month = 1
        finvoice.objects.create(year=year,month=month)

    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)

    if int(lastMonth.strftime("%m"))  < 10 and int(lastMonth.strftime("%m")) > 0 :
        lastdatescore = int(str(int(lastMonth.strftime("%Y")))+str(0)+str(int(lastMonth.strftime("%m"))))
    else:
        lastdatescore = int(str(int(lastMonth.strftime("%Y")))+str(int(lastMonth.strftime("%m"))))


    maxdatescore = finvoice.objects.all().aggregate(Max('datescore'))['datescore__max']

    if maxdatescore < lastdatescore:
        for i in range(maxdatescore+1,lastdatescore+1):
            myyear = int(str(i)[0:4])
            mymonth = int(str(i)[4:])
            if mymonth > 12:

                finvoice.objects.create(year=myyear+1,month=1)
            else:
                finvoice.objects.create(year=myyear,month=mymonth)

    thismonth = int(str(int(today.strftime("%Y")))+str(int(today.strftime("%m"))))

    myyear = int(str(thismonth)[0:4])
    mymonth = int(str(thismonth)[4:])
    if not finvoice.objects.filter(year=myyear).filter(month=mymonth):
        finvoice.objects.create(year=myyear,month=mymonth)

    open_invoices = finvoice.objects.filter(paid=False)
    for xx in open_invoices:

        xxdeals = fastdatad.objects.filter(datescore__lt=xx.datescore).filter(cancellationdate__isnull=True).filter(activationdate__isnull=False).filter(commissiontype='monthly')
        for yy in xxdeals:
            if not finvoiceitem.objects.filter(invoiceno=xx).filter(deal=yy):
                finvoiceitem.objects.create(invoiceno = xx,deal=yy,itemvalue=yy.ourcommission)
        xxdealsonetime = fastdatad.objects.filter(datescore=xx.datescore).filter(cancellationdate__isnull=True).filter(activationdate__isnull=False).filter(commissiontype='onetime')
        for oo in xxdealsonetime:
            if not finvoiceitem.objects.filter(invoiceno=xx).filter(deal=oo):
                finvoiceitem.objects.create(invoiceno = xx,deal=oo,itemvalue=oo.ourcommission)

        xxdealsthis = fastdatad.objects.filter(datescore=xx.datescore).filter(cancellationdate__isnull=True).filter(activationdate__isnull=False).filter(commissiontype='monthly')
        for tt in xxdealsthis:
            if not finvoiceitem.objects.filter(invoiceno=xx).filter(deal=tt):
                dayofactivation = int(tt.activationdate.strftime("%d"))
                finvoiceitem.objects.create(invoiceno = xx,deal=tt,itemvalue=(31-dayofactivation)*(tt.ourcommission/30))



        xx.save()

    allinvoices = finvoiceitem.objects.all().aggregate(Sum('itemvalue'))['itemvalue__sum']
    thismonthinvoice = finvoice.objects.filter(year=myyear).filter(month=mymonth).first()
    allduesinvoices = finvoiceitem.objects.exclude(invoiceno=thismonthinvoice).aggregate(Sum('itemvalue'))['itemvalue__sum']
    if fpayment.objects.all().aggregate(Sum('payment'))['payment__sum']:
        allpaid = fpayment.objects.all().aggregate(Sum('payment'))['payment__sum']
    else:
        allpaid = 0
    unpaidamount = allduesinvoices - allpaid

    finvoicelist = finvoice.objects.all().order_by('-year').order_by('-month')
    context = {'unpaidamount':unpaidamount,'allpaid':allpaid,'allinvoices':allinvoices,'finvoicelist':finvoicelist,'open_invoices':open_invoices,'lastdatescore':lastdatescore,'maxdatescore':maxdatescore}
    return render(request, 'crmapp/finvoicelist.html',context)

class finvoiceDetailView(DetailView):
    model = finvoice


@login_required
def finvoicetemplate(request,pk):
    myinvoice = get_object_or_404(finvoice,pk=pk)
    context = {'myinvoice':myinvoice}
    return render(request, 'crmapp/finvoicetemplate.html',context)



def topdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

class pdfDetail(PDFTemplateResponseMixin,DetailView):
    template_name = 'crmapp/pdf_detail.html'
    context_object_name = 'myinvoice'
    model = finvoice


@login_required
def orderupgrade(request):

    orderupgradelist = order.objects.all().filter(dealcategory='u').order_by('-creationdate')
    context = {'orderupgradelist':orderupgradelist}
    return render(request, 'crmapp/orderupgradelist.html',context)

@login_required
def orderfingerprintlist(request):

    orderfingerprintlist = order.objects.all().filter(orderstatus='fingerprint').order_by('-creationdate')
    context = {'orderfingerprintlist':orderfingerprintlist}
    return render(request, 'crmapp/orderfingerprintlist.html',context)

@login_required
def commission(request):
    if order.objects.filter(orderstatus='post').filter(activationdate1__isnull=True):
        ordernocommission = order.objects.filter(orderstatus='post').filter(activationdate1__isnull=True)

        for xx in ordernocommission:
            xx.save()



    orderpostlist = order.objects.filter(orderstatus='post').all()
    totalpostmrc = orderpostlist.aggregate(Sum('mrc'))['mrc__sum']
    commissionreport = orderpostlist.values('activationdate__year','activationdate__month').annotate(Total=Sum('commission'))
    commissiontotal = orderpostlist.aggregate(Sum('commission'))['commission__sum']
    comratio = commissiontotal/totalpostmrc
    comperorder = commissiontotal/orderpostlist.count()
    mrcperorder = totalpostmrc/orderpostlist.count()
    context = {'mrcperorder':mrcperorder,'comperorder':comperorder,'comratio':comratio,'totalpostmrc':totalpostmrc,'commissionreport':commissionreport,'commissiontotal':commissiontotal,'orderpostlist':orderpostlist}
    return render(request, 'crmapp/commissionreport.html',context)

@login_required
def fpaymentlist(request):

    fpaymentlist = fpayment.objects.all().order_by('paymentdate')
    context = {'fpaymentlist':fpaymentlist}
    return render(request, 'crmapp/fpaymentlist.html',context)




@login_required
def bulkordernew(request):

    myimport = orderimport.objects.all()

    myopp = get_object_or_404(opportunity,opportunityno =  20211505)
    # s50 = get_object_or_404(service,id = 5)
    # s120 = get_object_or_404(service,id = 9)
    # s230 = get_object_or_404(service,id = 89)
    # s450 = get_object_or_404(service,id = 2)
    # ad50 = addservices.objects.filter(opportunity=myopp).filter(service=s50).first()
    # ad120 = addservices.objects.filter(opportunity=myopp).filter(service=s120).first()
    # ad230 = addservices.objects.filter(opportunity=myopp).filter(service=s230).first()
    # ad450 = addservices.objects.filter(opportunity=myopp).filter(service=s450).first()
    myadd = addservices.objects.filter(opportunity=myopp).first()
    operation = get_object_or_404(User,username = 'hamza')

    for ii in myimport:

        # if 'paid 50' in ii.product:
        #     add = ad50
        #     myservice = s50
        # if '120' in ii.product:
        #     add = ad120
        #     myservice = s120
        # if '230' in ii.product:
        #     add = ad230
        #     myservice = s230
        # if '450' in ii.product:
        #     add = ad450
        #     myservice= s450

        order.objects.create(orderno=ii.orderno,opportunity=myopp,addservices=myadd,accountno=ii.accountno,serviceno=ii.serviceno,service=myadd.service,discount=Decimal(ii.discount),orderstatus='post',operationexecutive=operation,orderdate=datetime.datetime(ii.myyear,ii.mymonth,ii.myday),activationdate=datetime.datetime(ii.myyear,ii.mymonth,ii.myday))
        myadd.save()








    myopp.save()


    # myorders = order.objects.filter(id__gt=2908,discount=0.17)
    # for oo in myorders:
    #     # pass

    # myopp = myorder.opportunity
    # myadd = myorder.addservices
    # myservice = myorder.service
    # operation = get_object_or_404(User,username = 'hamza')

    # x2 = '545565793	35021721482	3-155594560323 545567198	35021722004	3-155594872234 545567925	35021722012	3-155602318871 545567965	35021722594	3-155602668788 546023844	35021722616	3-155602319425 560224174	35021722624	3-155602669346 561195716	35021722632	3-155602319973 561197104	35021722640	3-155602669890 561197316	35021718562	3-155604526527 561198053	35021718570	3-155602670448 561392897	35021718597	3-155604527085 561393029	35021718619	3-155601505088 561393071	35021718651	3-155604959000 561393369	35021718678	3-155604527637 561403699	35021719593	3-155604959552 561457247	35021719607	3-155604528196 562167152	35021719615	3-155604960102'
    # tt2 = x2.split()
    # # for i in range(18):

    # #     order.objects.create(orderno=tt2[3*i + 2],opportunity=myopp,addservices=myadd,accountno=int(tt2[3*i + 1]),serviceno=int(tt2[3*i]),service=myservice,discount=Decimal(0.17),orderstatus='post',operationexecutive=operation,orderdate=datetime.datetime(2021,7,28),activationdate=datetime.datetime(2021,7,28))

    # # x = 'aaaaa	11/04/2021	Cancel	550127854	35021479401	3-54579945530	Business Postpaid 50	0.17	%aaaaa	11/04/2021	Cancel	530113698	35021479444	3-54579946378	Business Postpaid 50	0.17	%'
    # # tt = x.split("%")

    # # for mm in tt:
    # #     xx = mm.split()
    # #     if len(xx):
    # #         if not order.objects.filter(orderno = xx[5]):
    # #             # order.objects.create(orderno=xx[5],opportunity=myopp,addservices=myadd,accountno=int(xx[4]),serviceno=int(xx[3]),service=myservice,discount=Decimal(xx[9]),orderstatus='post',operationexecutive=operation,orderdate=datetime.datetime(int(xx[1][6:]),int(xx[1][3:5]),int(xx[1][0:2])),activationdate=datetime.datetime(int(xx[0][6:]),int(xx[0][3:5]),int(xx[0][0:2])))
    # #             order.objects.create(orderno=xx[5],opportunity=myopp,addservices=myadd,accountno=int(xx[4]),serviceno=int(xx[3]),service=myservice,discount=Decimal(xx[9]),orderstatus='cancel',operationexecutive=operation,orderdate=datetime.datetime(int(xx[1][6:]),int(xx[1][3:5]),int(xx[1][0:2])))

    # myadd.save()
    # myopp.save()

    x2 = ''
    tt2= ''
    context = {'x2':x2,'tt2':tt2}
    return render(request, 'crmapp/bulkordernew.html',context)


@login_required
def stafforderlist(request,pk):
    staff = User.objects.filter(id=pk)
    myuser = staff[0]
    myaddservices = addservices.objects.filter(serviceowner=myuser)
    orderlist = order.objects.filter(orderstatus='post').filter(addservices_id__in=myaddservices)
    orderlist = order.objects.filter(opportunity_id__salesman = myuser).filter(activationdate__year=datetime.datetime.today().strftime('%Y')).filter(orderstatus='post').all()
    mrcsumoo = orderlist.aggregate(Sum('mrc'))['mrc__sum']
    revsumoo = orderlist.aggregate(Sum('revenuep'))['revenuep__sum']
    trevenue = order.objects.filter(activationdate__year=datetime.datetime.today().strftime('%Y')).aggregate(Sum('revenuep'))['revenuep__sum']
    rratio = 100*revsumoo/trevenue

    context = {'orderlist':orderlist,'staff':staff,'myuser':myuser,'mrcsumoo':mrcsumoo,'revsumoo':revsumoo,'trevenue':trevenue,'rratio':rratio}
    return render(request, 'crmapp/stafforderpostlist.html',context)


@login_required
def orderslistnoactivationdate(request):

    orderlist = order.objects.filter(orderstatus='post').filter(activationdate__isnull=True)
    context = {'orderlist':orderlist}
    return render(request, 'crmapp/orderslistnoactivationdate.html',context)


@login_required
def accountlist(request):

    today = datetime.date.today()
    delta = datetime.timedelta(days=60) # ~ 2 months
    thatDay = today - delta
    mylist  = accounts.objects.filter(noofpostorders__gt=0).filter(activationdate__lt=thatDay).all().filter(ispayed=False).order_by('activationdate')
    monthlist = [x for x in range(1,13)]
    context = {'mylist':mylist,'monthlist':monthlist}
    return render(request, 'crmapp/accountlist.html',context)

@login_required
def lastpayments(request):


    mylist  = accounts.objects.filter(payment__gt=0).order_by('-paymentdate')

    context = {'mylist':mylist}
    return render(request, 'crmapp/lastpayments.html',context)

class CreateaccountsView(CreateView):
    redirect_field_name = 'crmapp/fpaymentlist.html'
    form_class = accountsForm
    model = accounts

class accountsUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/fpayment_detail.html'
    form_class = accountsForm
    model = accounts

class accountsDetailView(DetailView):
    model = accounts

@login_required
def billspayment(request):
    orderpostlist = order.objects.all().filter(orderstatus='post').order_by('-creationdate')
    context = {'orderpostlist':orderpostlist}

    return render(request, 'crmapp/billspayment.html',context)

@login_required
def orderpaymentupdate(request,pk):

    thisorder = get_object_or_404(order, pk = pk)
    form = orderpaymentupdateForm(request.POST or None, instance = thisorder)

    if request.method=='POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('billspayment'))
    else:

        form = orderpaymentupdateForm()

    return render(request, 'crmapp/order_form.html',{'form':form,'thisorder':thisorder})

class CreatefpaymentView(CreateView):
    redirect_field_name = 'crmapp/fpaymentlist.html'
    form_class = fpaymentForm
    model = fpayment

class fpaymentUpdateView(UpdateView):
    redirect_field_name = 'repeatitapp/fpayment_detail.html'
    form_class = fpaymentForm
    model = fpayment

class fpaymentDetailView(DetailView):
    model = fpayment

@login_required
def accountsdetail1(request,pk):
    myaccount = get_object_or_404(accounts,pk=pk)

    myaccount.save()
    orderlists = order.objects.filter(accountno=myaccount.accountno).filter(orderstatus='post')
    myopportunity = orderlists.first().opportunity
    mycustomer = orderlists.first().opportunity.customer


    context = {'myaccount':myaccount,'orderlists':orderlists,'mycustomer':mycustomer,'myopportunity':myopportunity}
    return render(request, 'crmapp/accountsdetail1.html',context)

class CreateactivityrecordView(CreateView):
    redirect_field_name = 'crmapp/activityrecordlist.html'
    form_class = activityrecordForm
    model = activityrecord

class activityrecordDetailView(DetailView):
    model = activityrecord

def activityrecordcnew(request,pk):
    if request.method=='POST':
        form = activityrecordcForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.creator=request.user
            customer1 = get_object_or_404(customer,pk=pk)
            myform.customer=customer1
            myform.save()
            pk = myform.id
            return HttpResponseRedirect(reverse('activityrecorddetail', args=(pk,)))
            # return HttpResponseRedirect(reverse('opportunitylist'))
    else:
        form = activityrecordcForm()
    return render(request, 'crmapp/activityrecord_form.html',{'form':form})

@login_required
def activityrecordlist(request):

    activityrecords = activityrecord.objects.all().order_by('-creationdate')
    myactivityrecords = activityrecord.objects.filter(creator=request.user).order_by('-creationdate')

    # aaaaaaaaaaaaaaaaaaaa
    myfilter = activityrecordFilter(request.GET,queryset=activityrecords)
    activityrecords = myfilter.qs

    paginator = Paginator(activityrecords,10)
    page = request.GET.get('page')
    try:
        opps = paginator.page(page)
    except PageNotAnInteger:
        opps = paginator.page(1)
    except EmptyPage:
        opps = paginator.page(paginator.num_pages)


    myfilter1 = activityrecordFilter(request.GET,queryset=myactivityrecords)
    myactivityrecords = myfilter1.qs



    paginator1 = Paginator(myactivityrecords,10)
    page = request.GET.get('page')
    try:
        opps1 = paginator1.page(page)
    except PageNotAnInteger:
        opps1 = paginator1.page(1)
    except EmptyPage:
        opps1 = paginator1.page(paginator1.num_pages)


    context = {'activityrecords':activityrecords,'myactivityrecords':myactivityrecords,'opps':opps,'opps1':opps1,'myfilter':myfilter}
    return render(request, 'crmapp/activityrecordlist.html',context)


@login_required
def postcustomers(request):
    orderpostlist = order.objects.all().filter(orderstatus='post')
    myreport = orderpostlist.values('opportunity__customer').annotate(Total=Sum('mrc')).order_by('-Total')


    context = {'myreport':myreport}
    return render(request, 'crmapp/postcustomers.html',context)

@login_required
def customersmrc(request):

    orderpostlist = order.objects.all().filter(orderstatus='post')
    myreport = orderpostlist.values('opportunity__customer').annotate(Total=Sum('mrc')).order_by('-Total')

    context = {'myreport':myreport}
    return render(request, 'crmapp/customersmrc.html',context)

@login_required
def posttitle(request):
    orderpostlist = order.objects.all().filter(orderstatus='post')

    myreport = orderpostlist.values('opportunity__salesman__user_profile__jobtitle').annotate(Total=Sum('mrc')).order_by('-Total')
    myreport1 = orderpostlist.values('opportunity__salesman__user_profile__jobtitle').annotate(Total=Sum('discountmrc')).order_by('-Total')

    context = {'myreport':myreport,'myreport1':myreport1}
    return render(request, 'crmapp/posttitle.html',context)

@login_required
def mychart(request):
    cyear =  datetime.datetime.today().strftime('%Y')
    orderpostlist = order.objects.all().filter(orderstatus='post').filter(activationdate__year=cyear)
    myreport = orderpostlist.values('activationdate__month').annotate(count=Sum('discountmrc'))
    ll = []
    xx = []
    for rr in myreport:
        if rr['activationdate__month'] == 1:
            mymonth = 'Jan'
        elif rr['activationdate__month'] == 2:
            mymonth = 'Feb'

        elif rr['activationdate__month'] == 3:
            mymonth = 'March'

        elif rr['activationdate__month'] == 4:
            mymonth = 'April'

        elif rr['activationdate__month'] == 5:
            mymonth = 'May'

        elif rr['activationdate__month'] == 6:
            mymonth = 'June'

        elif rr['activationdate__month'] == 7:
            mymonth = 'July'

        elif rr['activationdate__month'] == 8:
            mymonth = 'Aug'

        elif rr['activationdate__month'] == 9:
            mymonth = 'Sep'

        elif rr['activationdate__month'] == 10:
            mymonth = 'Oct'

        elif rr['activationdate__month'] == 11:
            mymonth = 'Nov'

        elif rr['activationdate__month'] == 12:
            mymonth = 'Dec'

        # ll.append(rr['activationdate__month'])
        ll.append(mymonth)
        xx.append(rr['count'])

    orderpostlist2 = order.objects.all().filter(orderstatus='post')
    myreport2 = orderpostlist2.values('activationdate__year').annotate(count=Sum('discountmrc'))
    ll2 = []
    xx2 = []
    for kk in myreport2:
        if kk.get('activationdate__year', None) is None or kk.get('count', None) is None:
            continue
        if kk['activationdate__year'] < 2021:
            continue
        ll2.append(kk['activationdate__year'])
        xx2.append(kk['count'])



    myopportunities =  opportunity.objects.select_related('status_operationstatusname').filter(creationdate__year=cyear)
    myreport3 = myopportunities.values('status').annotate(Total=Sum('totalmrc'))
    ll3 = []
    xx3 = []
    for kk3 in myreport3:
        if kk3.get('status', None) is None or kk3.get('Total', None) is None:
            continue
        mystatus = get_object_or_404(operationstatus,id=kk3['status'])
        ll3.append(mystatus.operationstatusname)
        xx3.append(kk3['Total'])

    myorderpostlist = order.objects.all().filter(orderstatus='post').filter(activationdate__year=cyear)
    myreport4 = myorderpostlist.values('opportunity__salesman').annotate(Total=Sum('discountmrc'))
    ll4 = []
    xx4 = []
    for kk4 in myreport4:
        if kk4.get('opportunity__salesman', None) is None or kk3.get('Total', None) is None:
            continue
        mysalesman = get_object_or_404(User,id=kk4['opportunity__salesman'])
        ll4.append(mysalesman.username)
        xx4.append(kk4['Total'])

    firstlabel = 'MRC VS Month in ' + cyear
    context = {'xx':xx,'ll':ll,'myreport':myreport,'cyear':cyear,'ll2':ll2,'xx2':xx2,'ll3':ll3,'xx3':xx3,'ll4':ll4,'xx4':xx4,'firstlabel':firstlabel}
    return render(request, 'crmapp/mychart.html',context)

def mysendemail(request):
    with get_connection(
    host='mail.minaexc.com.sa',
    port=587,
    username='a.abdulbasit@minaexc.com.sa',
    password='abufaisal@mina',
    use_tls=True
    ) as connection:

        EmailMessage('subject1', 'body1', 'a.abdulbasit@minaexc.com.sa', ['basit395@gmail.com'],
                     connection=connection).send()

    return HttpResponse('Message is sent')

def emailregister(request):
    myuser = request.user
    if request.method=='POST':
        form = emailregisterForm(request.POST)
        if form.is_valid():

            myuser.email = form.cleaned_data['myemail']
            myuser.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = emailregisterForm()
    return render(request, 'crmapp/emailregister_form.html',{'form':form})

    return render(request, 'crmapp/customersmrc.html',context)