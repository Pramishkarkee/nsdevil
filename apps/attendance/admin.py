from django.contrib import admin
from apps.attendance.models import Student, Attendance,CourseName,AcademicClass,Teacher
from apps.core.admin import BaseModelAdmin

@admin.register(Student)
class StudentAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display+('user', 'roll_number', )
    search_fields = BaseModelAdmin.search_fields+('roll_number', 'user__username')

@admin.register(Attendance)
class AttendanceAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display +('student', 'date', 'status')
    list_filter = BaseModelAdmin.list_filter+('date', 'status')
    search_fields = BaseModelAdmin.search_fields+ ('student__roll_number', 'date')

@admin.register(CourseName)
class CourseNameAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display +('name', 'faculty', 'duration')
    list_filter = BaseModelAdmin.list_filter+('name', 'faculty')

@admin.register(AcademicClass)
class AcademicClassAdmin(BaseModelAdmin):
    pass

@admin.register(Teacher)
class TeacherAdmin(BaseModelAdmin):
    pass
