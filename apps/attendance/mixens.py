from django.db.models import Count
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from apps.attendance.models import Attendance
from calendar import monthrange

class DashboardAttendanceMixin:
    def get_weekly_attendance_report(self,academic_class=None):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Query and aggregate attendance records by date for the current week
        weekly_data = (
              Attendance.objects.filter(
                date__range=(start_of_week, end_of_week),academic_class=academic_class)
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date') if academic_class else Attendance.objects.filter(date__range=(start_of_week, end_of_week))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        # Transform the queryset to the desired format
        weekly_report = [{"date": entry['date'].strftime('%Y-%m-%d'), "count": entry['count']} for entry in weekly_data]

        return weekly_report

    def get_month_attendance_report(self,academic_class=None):
        today = datetime.today().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = first_day_of_month.replace(month=today.month + 1, day=1) - timezone.timedelta(days=1)
        month_weeks = []
        current_day = first_day_of_month
        week_number = 1

        while current_day <= last_day_of_month:
            start_of_week = current_day
            end_of_week = min(start_of_week + timedelta(days=6), last_day_of_month)
            weekly_count = (Attendance.objects.filter(date__range=(start_of_week, end_of_week),
                                                      academic_class=academic_class).count()
                            if academic_class else
                            Attendance.objects.filter(date__range=(start_of_week, end_of_week)).count()
                            )
            month_weeks.append({"date": f"week{week_number}", "count": weekly_count})
            current_day = end_of_week + timedelta(days=1)
            week_number += 1
        return month_weeks