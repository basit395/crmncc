import django_filters
from django_filters import DateTimeFromToRangeFilter
from .models import customer,opportunity,order,activityrecord
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit

class customerFilter(django_filters.FilterSet):

    customername = django_filters.CharFilter(lookup_expr='icontains')
    cr = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = customer
        fields = ['customername','cr']


class opportunityFilter(django_filters.FilterSet):

    class Meta:
        model = opportunity
        fields = ['opportunityno','customer','salesman','status']


class orderFilter(django_filters.FilterSet):

    creation_year = django_filters.NumberFilter(field_name='creationdate', lookup_expr='year')
    creation_month = django_filters.NumberFilter(field_name='creationdate', lookup_expr='month')
    class Meta:
        model = order
        fields = ['orderno','opportunity','service','servicecategory','discount','orderstatus','operationexecutive','creationdate','opportunity__salesman']

class activityrecordFilter(django_filters.FilterSet):

    creation_year = django_filters.NumberFilter(field_name='creationdate', lookup_expr='year')
    creation_month = django_filters.NumberFilter(field_name='creationdate', lookup_expr='month')
    class Meta:
        model = activityrecord
        fields = ['activity','creator','customer','creationdate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'activity',
                'creator',
                'customer',
                'creationdate',

            ),
            Submit('submit', 'Submit', css_class='button white'),
        )
