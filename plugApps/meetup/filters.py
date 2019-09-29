from meetup.models import Meeting
import django_filters

class MeetingFilter(django_filters.FilterSet):

    class Meta:
        model = Meeting
        fields = ['data_hora',]
