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
    path('order/new/', views.ordernew, name='ordernew'),
    path('order/<pk>/', views.orderDetailView.as_view(), name='orderdetail'),
    path('order/update/<pk>/', views.orderUpdateView.as_view(), name='orderupdate'),
    path('order/changetopost/<pk>/', views.changetopost, name='changetopost'),
    path('order/cancel/<pk>/', views.cancelorder, name='cancel'),
    path('order/open/<pk>/', views.openorder, name='open'),
    path('order/held/<pk>/', views.heldorder, name='held'),
    path('ordero/new/<pk>/<pk1>/', views.orderonew, name='newordero'),
    path('orderdouble/new/<pk>/<pk1>', views.orderdouble, name='orderdouble'),
    #
    path('service/', views.servicelist, name='servicelist'),
    path('service/new/', views.CreateserviceView.as_view(), name='servicenew'),
    path('service/<pk>/', views.serviceDetailView.as_view(), name='servicedetail'),

    path('report/', views.all_users_sum, name='report'),
    path('reportall/', views.reportall, name='reportall'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('oppnogen/', views.oppnogen, name='oppnogen'),


    ]
