from rest_framework import serializers

class DashboardFilterSerializer(serializers.Serializer):
    time_period = serializers.ChoiceField(choices=[('week', 'Week'), ('this_month', 'This Month')])
    academic_class = serializers.CharField(required=False, allow_blank=True)