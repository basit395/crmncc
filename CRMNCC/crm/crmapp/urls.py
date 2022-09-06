from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.index, name='home'),

    path('customers/', views.customerslist, name='customerslist'),
    path('customer/new/', views.customernew, name='customernew'),
    path('customer/<pk>/', views.customerDetailView.as_view(), name='customerdetail'),
    path('customer/update/<pk>/', views.customerUpdateView.as_view(), name='customerupdate'),

    path('opportunity/new/', views.opportunitynew, name='newopportunity'),
    path('opportunityc/new/<pk>', views.opportunitycnew, name='newopportunityc'),
    path('opportunity/<pk>/', views.opportunitydetail, name='opportunitydetail'),
    path('opportunity/', views.opportunitylist, name='opportunitylist'),
    path('opportunity/update/<pk>/', views.opportunityUpdateView.as_view(), name='opportunityupdate'),
    path('opportunity/proposal/<pk>/', views.proposalopp, name='proposal'),
    path('opportunity/document/<pk>/', views.documentopp, name='document'),
    path('opportunity/negotiation/<pk>/', views.negotiationopp, name='negotiation'),
    path('opportunity/operationvalidation/<pk>/', views.operationvalidationopp, name='operationvalidation'),
    path('opportunity/validated/<pk>/', views.validatedopp, name='validated'),
    path('opportunity/post/<pk>/', views.postopp, name='postopp'),
    path('opportunity/lost/<pk>/', views.lostopp, name='lost'),
    path('opportunity/stcapproval/<pk>/', views.stcapproval, name='stcapproval'),
    path('operval/', views.operval, name='operval'),
    path('opportunitypost/', views.opportunitypost, name='opportunitypost'),

    path('addservice/new/<pk>/', views.addservicenew, name='addservice'),
    path('addservice/list/', views.addserviceslist, name='addservicelist'),

    path('staff/', views.stafflist, name='stafflist'),
    path('staff/new/', views.CreatestaffView.as_view(), name='staffnew'),
    path('staff/<pk>/', views.staffDetailView.as_view(), name='staffdetail'),

    path('suggestion/', views.suggestionlist, name='suggestion'),
    path('suggestion/new/', views.suggestionnew, name='suggestionnew'),
    path('suggestion/<pk>/', views.suggestionDetailView.as_view(), name='suggestiondetail'),
    path('suggestion/update/<pk>/', views.suggestionUpdateView.as_view(), name='suggestionupdate'),
    path('suggestion/completion/<pk>/', views.completedsugg, name='completed'),
    path('suggestion/closed/<pk>/', views.closedsugg, name='closed'),

    path('order/', views.orderlist, name='order'),
    path('order/post/', views.orderpostlist, name='orderpost'),
    path('order/open/', views.orderopenlist, name='orderopen'),
    path('order/held/', views.orderheldlist, name='orderheld'),
    path('order/cancel/', views.ordercancellist, name='ordercancel'),
    path('order/new/', views.ordernew, name='ordernew'),
    path('order/<pk>/', views.orderdetail, name='orderdetail'), #new
    path('order/update/<pk>/', views.orderUpdateView.as_view(), name='orderupdate'),
    path('order/changetopost/<pk>/', views.changetopost, name='changetopost'),
    path('order/cancel/<pk>/', views.cancelorder, name='cancel'),
    path('order/open/<pk>/', views.openorder, name='open'),
    path('order/held/<pk>/', views.heldorder, name='held'),
    path('ordero/new/<pk>/<pk1>/', views.orderonew, name='newordero'),
    path('orderdouble/new/<pk>/<pk1>', views.orderdouble, name='orderdouble'),
    path('orderdouble1/new/<pk>/<pk1>', views.orderdouble1, name='orderdouble1'),
    path('orderdouble2/new/<pk>/<pk1>', views.orderdouble2, name='orderdouble2'),
    path('ordernopost', views.ordernopost, name='ordernopost'),
    path('orderupgrade', views.orderupgrade, name='orderupgrade'),
    path('orderfingerprint', views.orderfingerprintlist, name='orderfingerprint'),
    path('orderpaymentupdate/<pk>/', views.orderpaymentupdate, name='orderpaymentupdate'),

    path('stafforderlist/<pk>/', views.stafforderlist, name='stafforderlist'),
    path('orderslistnoactivationdate/', views.orderslistnoactivationdate, name='orderslistnoactivationdate'),



    path('service/', views.servicelist, name='servicelist'),
    path('service/new/', views.CreateserviceView.as_view(), name='servicenew'),
    path('service/<pk>/', views.serviceDetailView.as_view(), name='servicedetail'),
    path('service/update/<pk>/', views.serviceUpdateView.as_view(), name='serviceupdate'),

    path('report/', views.all_users_sum, name='report'),
    path('report/thisyear', views.reportthisyear, name='reportthisyear'),
    path('report/thismonth', views.reportthismonth, name='reportthismonth'),
    path('reportall/', views.reportall, name='reportall'),
    path('report/customer/team', views.reportcustomerteam, name='reportcustomerteam'), #new

    path('report/weak/lastweek', views.reportweaklastweek, name='reportweaklastweek'),#new


    path('dashboard/', views.dashboard, name='dashboard'),
    path('oppnogen/', views.oppnogen, name='oppnogen'),

    path('invoice/new/', views.invoicenew, name='invoicenew'),#new
    path('invoice/<pk>/', views.invoiceDetailView.as_view(), name='invoicedetail'),#new
    path('invoice/update/<pk>/', views.invoiceUpdateView.as_view(), name='invoiceupdate'),#new
    path('invoices/', views.invoiceslist, name='invoiceslist'),#new

    path('expensecategory/new/', views.expensecategorynew, name='expensecategorynew'),#new
    path('expensecategory/<pk>/', views.expensecategoryDetailView.as_view(), name='expensecategorydetail'),#new
    path('expensecategory/update/<pk>/', views.expensecategoryUpdateView.as_view(), name='expensecategoryupdate'),#new
    path('expensecategory/', views.expensecategorylist, name='expensecategorylist'),#new

    path('expenses/new/', views.expensesnew, name='expensesnew'),#new
    path('expenses/<pk>/', views.expensesDetailView.as_view(), name='expensesdetail'),#new
    path('expenses/update/<pk>/', views.expensesUpdateView.as_view(), name='expensesupdate'),#new
    path('expenses/', views.expenseslist, name='expenseslist'),#new
    path('expenses/total', views.expensestotal, name='expensestotal'),#new


    path('mycustomers', views.mycustomers, name='mycustomers'),#new
    path('usercustomers/<pk>/', views.usercustomers, name='usercustomers'),#new

    path('myopportunities', views.myopportunities, name='myopportunities'),#new
    path('useropportunities/<pk>/', views.useropportunities, name='useropportunities'),#new

    path('opportunity/<pk>/delete', views.opportunityDeleteView.as_view(), name='opportunitydelete'), #new


    path('addservice/<pk>/', views.addservicesDetailView.as_view(), name='addservicesdetail'),#new
    path('addservice/<pk>/delete', views.addservicesDeleteView.as_view(), name='addservicedelete'),
    path('addservice/<pk>/delete1', views.addservicesdelete, name='addservicedelete1'),
    path('addservice/update/<pk>/', views.addservicesUpdateView.as_view(), name='addservicesupdate'),
    path('order/<pk>/delete', views.orderDeleteView.as_view(), name='orderdelete'),

    path('order/<pk>/delete1', views.orderdelete, name='orderdelete1'), #new

    path('productreport', views.productreport, name='productreport'),

    path('sourcereport', views.sourcereport, name='sourcereport'),
    path('opportunity/hotlead', views.opportunityhotlead, name='opportunityhotlead'),
    path('customer/oneback', views.customeroneback, name='customeroneback'),
    path('customer/<pk>/assignedto', views.assignedto, name='assignedto'),
    path('pipeline', views.pipeline, name='pipeline'),
    path('megapipeline', views.megapipeline, name='megapipeline'),
    path('operationreport', views.operationreport, name='operationreport'),
    path('salesman/<pk>/', views.salesmandetail, name='salesmandetail'),
    path('salesteam/', views.salesteam, name='salesteam'),
    path('operationstages', views.operationstages, name='operationstages'),
    path('operationstages/<pk>/', views.operationstagedetail, name='operationstagedetail'),
    path('checkv/', views.checkv, name='checkv'),
    path('postreport/', views.orderpostreportthisyear, name='postreport'),
    path('opportunitynotes/<pk>/', views.opportunitynotesn, name='opportunitynotes'),
    path('operationstages/<pk>/<pk1>/', views.salesmanoperationstage, name='salesmanoperationstage'),
    path('postordersnodate/', views.postordersnodate, name='postordersnodate'),
    path('partners/', views.partners, name='partners'),

    path('deal/new/', views.dealnew, name='dealnew'),
    path('dealslist/', views.dealslist, name='dealslist'),
    path('deal/<pk>/', views.dealdetail, name='dealdetail'),
    path('deal/update/<pk>/', views.fastdatadUpdateView.as_view(), name='dealupdate'),
    path('deal/<pk>/delete', views.fastdatadDeleteView.as_view(), name='dealdelete'),
    path('bulkorderupdate', views.bulkorderupdate, name='bulkorderupdate'),
    path('bulkordernew', views.bulkordernew, name='bulkordernew'),

    path('fservice/', views.fservicelist, name='fservicelist'),
    path('fservice/new/', views.CreatefserviceView.as_view(), name='fservicenew'),
    path('fservice/<pk>/', views.fserviceDetailView.as_view(), name='fservicedetail'),
    path('fservice/update/<pk>/', views.fserviceUpdateView.as_view(), name='fserviceupdate'),

    path('fcustomers/', views.fcustomerslist, name='fcustomerslist'),
    path('fcustomer/new/', views.fcustomernew, name='fcustomernew'),
    path('fcustomer/<pk>/', views.fcustomerDetailView.as_view(), name='fcustomerdetail'),
    path('fcustomer/update/<pk>/', views.fcustomerUpdateView.as_view(), name='fcustomerupdate'),

    path('finvoice/', views.finvoicelist, name='finvoicelist'),
    path('finvoice/<pk>/', views.finvoiceDetailView.as_view(), name='finvoicedetail'),
    path('finvoicetemplate/<pk>/', views.finvoicetemplate, name='finvoicetemplate'),
    path('topdf/<pk>/', views.pdfDetail.as_view(), name='topdf'),

    path('fpayment/', views.fpaymentlist, name='fpaymentlist'),
    path('fpayment/new/', views.CreatefpaymentView.as_view(), name='fpaymentnew'),
    path('fpayment/<pk>/', views.fpaymentDetailView.as_view(), name='fpaymentdetail'),
    path('fpayment/update/<pk>/', views.fpaymentUpdateView.as_view(), name='fpaymentupdate'),


    path('cctv', views.cctv, name='cctv'),
    path('topdf', views.topdf, name='topdf'),

    path('commission', views.commission, name='commission'),

    path('accountlist', views.accountlist, name='accountlist'),
    path('lastpayments', views.lastpayments, name='lastpayments'),
    path('account/new/', views.CreateaccountsView.as_view(), name='accountnew'),
    path('account/<pk>/', views.accountsDetailView.as_view(), name='accountdetail'),
    path('account1/<pk>/', views.accountsdetail1, name='accountdetail1'),
    path('account/update/<pk>/', views.accountsUpdateView.as_view(), name='accountupdate'),


    path('billspaymentlist', views.billspayment, name='billspayment'),

    path('activityrecord/new/', views.CreateactivityrecordView.as_view(), name='activityrecordnew'),
    path('activityrecord/<pk>/', views.activityrecordDetailView.as_view(), name='activityrecorddetail'),
    path('activityrecord/new/<pk>', views.activityrecordcnew, name='newactivityrecordc'),
    path('activityrecordlist', views.activityrecordlist, name='activityrecordlist'),

    path('postcustomers', views.postcustomers, name='postcustomers'),
    path('posttitle', views.posttitle, name='posttitle'),

    path('customersmrc', views.customersmrc, name='customersmrc'),
    path('todayop', views.todayop, name='todayop'),
    path('todaypmrc', views.todaypmrc, name='todaypmrc'),
    path('todayc', views.todayc, name='todayc'),
    path('yesterdayop', views.yesterdayop, name='yesterdayop'),
    path('yesterdaypostorders', views.yesterdaypostorders, name='yesterdaypostorders'),
    path('yesterdaycustomers', views.yesterdaycustomers, name='yesterdaycustomers'),
    path('thisweekop', views.thisweekop, name='thisweekop'),
    path('thisweekpostorders', views.thisweekpostorders, name='thisweekpostorders'),

    path('mychart', views.mychart, name='mychart'),
    path('mysendemail', views.mysendemail, name='mysendemail'),
    path('emailregister', views.emailregister, name='emailregister'),






    ]
