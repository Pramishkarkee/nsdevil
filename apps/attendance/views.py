from django.shortcuts import render
from apps.attendance.mixens import DashboardAttendanceMixin
from django.views.generic import TemplateView
from apps.attendance.models import AcademicClass,Student,Attendance,Teacher
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from apps.attendance.forms import CustomLoginForm,FilterForm
import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DashboardFilterSerializer
from rest_framework import status
from apps.user.permission import IsTeacherUser,IsStudentUser

def logout_view(request):
    logout(request)
    return redirect('login')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('get-class-list')  # Redirect to a success page on successful login

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)  # Redirect authenticated users to home or another page
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Login successful")
        else:
            messages.error(self.request, "Invalid username or password")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)

class AcademicClassViews(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.user_type=='student_user':
            try:
                student = Student.objects.get(user=self.request.user)
                context['total_attendance'] = Attendance.objects.filter(student=student).count()
            except Student.DoesNotExist:
                return context
        context['class_data'] = AcademicClass.objects.annotate(student_count=Count('student')).\
        all() if self.request.user.user_type =="teacher_user" or self.request.user.user_type =="portal_user"\
            else AcademicClass.objects.filter(id=student.academic_class_id ).annotate(student_count=Count('student'))

        return context

class AttendanceViews(TemplateView):
    template_name = 'get_attendance.html'

    def get_context_data(self, **kwargs):
        class_id = kwargs.get('class_id')
        today = timezone.now().date()
        context = super().get_context_data(**kwargs)
        context['attendance'] = Attendance.objects.filter(date=today)
        context['class_id']=class_id
        return context

class TakeAttendanceViews(TemplateView):
    template_name = 'take_attendance.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != "teacher_user":
            return render(request, 'error.html', {'message': 'Permission Denied'})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        class_id = kwargs.get('class_id')
        context = super().get_context_data(**kwargs)
        context['student'] = Student.objects.filter(academic_class=class_id)
        context['class_data'] = AcademicClass.objects.get(id=class_id)
        return context

    def post(self, request, *args, **kwargs):
        try:
            teacher=Teacher.objects.get(user=request.user)
            class_id = kwargs.get('class_id')
            students = Student.objects.filter(academic_class=class_id)
            today_date = datetime.today().date()
            for student in students:
                # Assuming the form has a checkbox input for each student to mark attendance
                status = request.POST.get(f'attendance_{student.id}')
                status = status == 'on'  # Convert checkbox value to boolean
                Attendance.objects.update_or_create(
                        student=student,
                        date=today_date,
                        defaults={'status': status,
                                  'teacher':teacher,
                                  'academic_class':student.academic_class
                                  }
                    )

            return redirect(reverse('get-attendance', kwargs={'class_id': class_id}))
        except Teacher.DoesNotExist:
            return render(request, 'error.html', {'message': 'Permission Denied'})


class DashboardViews(DashboardAttendanceMixin,TemplateView):
    form_class = FilterForm
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != "teacher_user":
            return render(request, 'error.html', {'message': 'Permission Denied'})
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        query_params = self.request.GET.urlencode()
        return f"{self.request.path}?{query_params}"

    def get_context_data(self, **kwargs):
        form = FilterForm(self.request.GET or None)
        context = super().get_context_data(**kwargs)
        time_period=self.request.GET.get('time_period', None)
        academic_class=self.request.GET.get('academic_class', None)

        data = self.get_weekly_attendance_report( academic_class=academic_class)if time_period == 'week' else self.get_month_attendance_report( academic_class=academic_class)
        labels = [item['date'] for item in data]
        counts = [item['count'] for item in data]
        context['labels']=json.dumps(labels)
        context['counts'] = json.dumps(counts)
        context['form']=form
        return context


class DashboardAPIView(DashboardAttendanceMixin, APIView):
    def get(self, request, *args, **kwargs):
        time_period = request.GET.get('time_period', None)
        academic_class = request.GET.get('academic_class', None)
        data = self.get_weekly_attendance_report( academic_class=academic_class)if time_period == 'week' else self.get_month_attendance_report( academic_class=academic_class)
        return Response(data)