from django.db import models
from apps.core.models import BaseModel
from django.db.models import Max
from apps.user.models import StudentUser,TeacherUser

class CourseName(BaseModel):
    name= models.CharField(max_length=255)
    faculty = models.CharField(max_length=255,null=True,blank=True)
    duration = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AcademicClass(BaseModel):
    class_name = models.CharField(max_length=255)
    course = models.ForeignKey(CourseName,on_delete=models.CASCADE,null=True,blank=True)
    student_capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.class_name

class Student(BaseModel):
    user = models.OneToOneField(StudentUser, on_delete=models.CASCADE)
    roll_number = models.IntegerField(blank=True,null=True)
    join_date = models.DateField()
    academic_class = models.ForeignKey(AcademicClass,on_delete=models.DO_NOTHING,blank=True,null=True)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

    def save(self, *args, **kwargs):
        if not self.roll_number:
            self.roll_number = self.generate_roll_number()
        super().save(*args, **kwargs)

    def generate_roll_number(self):
        """Generate a unique roll number for the student within the same academic class."""
        if self.academic_class is None:
            return '1'  # Default value if academic_class is not set
        last_roll_number = Student.objects.filter(
            academic_class=self.academic_class
        ).aggregate(
            Max('roll_number')
        )['roll_number__max']

        if last_roll_number:
            last_number = int(last_roll_number)  # Assuming roll number format is CLASS0001
        else:
            last_number = 0

        new_number = last_number + 1
        return f"{new_number}"


class Teacher(BaseModel):
    user = models.OneToOneField(TeacherUser, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    teacher_type = models.CharField(max_length=255)#part time
    hire_date = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    class_teacher = models.OneToOneField(AcademicClass,on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.user.username} - {self.hire_date}"


class Attendance(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING)
    academic_class = models.ForeignKey(AcademicClass,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=True)  # True for Present, False for Absent

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.status else 'Absent'}"

    def is_present(self):
        """Returns a string indicating whether the student is present or absent."""
        return 'Present' if self.status else 'Absent'
