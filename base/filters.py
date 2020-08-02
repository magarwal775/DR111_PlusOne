from accounts.models import User, Alumni
from college.models import College, Department, Course, Specialization
import django_filters


class UserFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    college = django_filters.ModelChoiceFilter(queryset=College.objects.all())
    department = django_filters.ModelChoiceFilter(queryset=Department.objects.all())
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all())
    specialization = django_filters.ModelChoiceFilter(queryset=Specialization.objects.all())

    class Meta:
        model = User
        fields = ['full_name', 'first_name', 'last_name', 'college', 'department', 'course', 'specialization']
