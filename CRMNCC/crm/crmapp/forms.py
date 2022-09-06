from django import forms
from .models import opportunity,customer,fcustomer,staff,suggestion,order,service,fservice,addservices,invoices,expensecategory,expenses,opportunitynotes,fastdatad,fpayment,accounts,activityrecord
import datetime
from django.utils import timezone



class opportunityForm(forms.ModelForm):
    class Meta:
        model = opportunity
        fields = ('lms','customer','authorized','coordinates','source','opportunitydate','expectedclosingdate','note',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'expectedclosingdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }


class opportunitycForm(forms.ModelForm):

    class Meta:
        model = opportunity
        fields = ('lms','source','opportunitydate','expectedclosingdate','note',)

        def clean(self):
            data = super().clean()
            mydate = data.get("expectedclosingdate")
            if mydate < timezone.now():
                raise forms.ValidationError('values must be today or greater')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'expectedclosingdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'opportunitydate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),

        }

class addservicesForm(forms.ModelForm):

    class Meta:
        model = addservices
        fields = ('service','noofservices',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class customerForm(forms.ModelForm):

    class Meta:
        model = customer
        fields = ('customername','cr','activity','no_of_employees','city', 'branches','district','street','phone','email','current_services','source','notes',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class fcustomerForm(forms.ModelForm):

    class Meta:
        model = fcustomer
        fields = ('customername','cr','city', 'phone','email','notes',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class staffForm(forms.ModelForm):

    class Meta:
        model = staff
        fields = ('staffname','staff_id','joindate','employeejobtitle',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
             'joindate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class suggestionForm(forms.ModelForm):

    class Meta:
        model = suggestion
        fields = ('requesttext',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class orderForm(forms.ModelForm):

    class Meta:
        model = order
        fields = ('dealcategory','opportunity','cabinetno','orderno','accountno','service','serviceout','circuitno','dealcategory','addservices','discount','orderdate','note',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
             'orderdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            #  'dealcategory':forms.ChoiceField(attrs={'onchange': 'myFunction();'}),
        }

class orderupdateForm(forms.ModelForm):

    # activationdate = forms.DateField(label='What is the activation date?', widget=forms.SelectDateWidget)

    class Meta:
        model = order
        fields = ('dealcategory','opportunity','orderno','accountno','discount','serviceno','cabinetno','circuitno','granite','dealcategory','serviceout','orderdate','activationdate','note',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'activationdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'orderdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),

        }



class orderoForm(forms.ModelForm):

    class Meta:
        model = order
        fields = ('dealcategory','cabinetno','serviceno','service','serviceout','accountno','orderno','granite','imei','circuitno','discount','orderdate','note',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
             'orderdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            #  'dealcategory':forms.ChoiceField(attrs={'onchange': 'myFunction();'}),
        }

class orderpostForm(forms.ModelForm):

    class Meta:
        model = order
        fields = ('activationdate',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
             'activationdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class orderdoubleForm(forms.ModelForm):

    class Meta:
        model = order
        fields = ('serviceno',)

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'textinputclass'}),
        #     'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        # }

class serviceForm(forms.ModelForm):

    class Meta:
        model = service
        fields = ('servicename','servicecategory','ncc_id','catalogue_id','nrc','mrc','commission',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


YEAR_CHOICES = ['2017', '2018', '2019', '2020', '2021','2022','2023']
class invoicesForm(forms.ModelForm):

    invoicedate = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))
    stcemaildate = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))
    bankdepoitdate = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))

    class Meta:
        model = invoices
        fields = ('invoice_no','invoicedate','stcemaildate','relatedyear','relatedperiod','amount','purchaseno','receiptno','bankdepoitdate',)


    def clean_relatedyear(self):
        relatedyear = self.cleaned_data.get("relatedyear")
        if relatedyear > 2017 :
           myyear =  int(datetime.datetime.today().strftime('%Y'))
           if relatedyear <= myyear:
                return relatedyear
           else:
                forms.ValidationError("Future Year")
        else:
            raise forms.ValidationError("This year is wrong")


    widgets = {
            'invoicedate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'stcemaildate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'bankdepoitdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),

        }


class expensecategoryForm(forms.ModelForm):

    class Meta:
        model = expensecategory
        fields = ('expensecategoryname',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class expensesForm(forms.ModelForm):

    class Meta:
        model = expenses
        fields = ('Category','amount','year','month','note',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),

        }

class orderdouble1Form(forms.ModelForm):

    class Meta:
        model = order
        fields = ('serviceno','accountno',)

class orderdouble2Form(forms.ModelForm):

    class Meta:
        model = order
        fields = ('serviceno','accountno','orderno',)

class customerassigningForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ('assignedto',)

class opportunitynotesForm(forms.ModelForm):
    class Meta:
        model = opportunitynotes
        fields = ('note',)

class fastdatadForm(forms.ModelForm):
    class Meta:
        model = fastdatad
        fields = ('customer','service','noofservices','provider','description','broker','totalnrc','totalmrc','ourcommission','brokercommission','commissiontype','referenceno','coordinates','expectedclosingdate','activationdate','cancellationdate')

        widgets = {
                'title': forms.TextInput(attrs={'class': 'textinputclass'}),
                'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
                'expectedclosingdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
                'activationdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
                'cancellationdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            }

class fserviceForm(forms.ModelForm):

    class Meta:
        model = fservice
        fields = ('servicename','nrc','mrc','commission',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class orderpaymentupdateForm(forms.ModelForm):

    class Meta:
        model = order
        fields = ('stcsalesreport','stcpostreport','stccommissionreport','issuedbills','paidbills',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            'activationdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'orderdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),

        }

class fpaymentForm(forms.ModelForm):

    class Meta:
        model = fpayment
        fields = ('invoiceno','paymentdate','payment','notes',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }




class accountsForm(forms.ModelForm):

    class Meta:
        model = accounts
        fields = ('accountno','noofbills','billsvalue','paymentdate','payment','notes',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'notes': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
             'paymentdate': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }

class activityrecordForm(forms.ModelForm):

    class Meta:
        model = activityrecord
        fields = ('activity','customer',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class activityrecordcForm(forms.ModelForm):

    class Meta:
        model = activityrecord
        fields = ('activity',)


class emailregisterForm(forms.Form):
    myemail = forms.EmailField(max_length = 200)



