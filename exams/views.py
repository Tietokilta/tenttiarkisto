from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count, Q
from exams.models import Course, Exam, ExamFile, Maintainer
from django.forms import EmailField, ModelForm, Form, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from datetime import datetime

def frontpage(request):
  maintainers = Maintainer.objects.order_by('group').all()
  return render(request, 'index.html', {'maintainers': maintainers})

def courselist(request):
  q = request.GET.get('q', '').strip()
  all_courses = Course.objects.annotate(exam_count=Count('exam')).order_by('code').filter(Q(name__icontains=q)|Q(code__icontains=q)).all()
  return render(request, 'course/courselist.html', {'courses': all_courses})

def courseview(request, course_id, _ignore=None):
  course = get_object_or_404(Course, pk=course_id)
  return render(request, 'course/courseview.html', {'course': course, 'exams': course.exam_set.order_by('-exam_date').all()})

class CourseForm(ModelForm):
  class Meta:
    model = Course
    fields = ['code', 'name']

def addcourse(request):
  saved = False
  course = None
  if request.method == 'POST':
    form = CourseForm(request.POST)
    if form.is_valid():
      course = form.save()
      saved = True
      form = CourseForm()
  else:
    form = CourseForm()
  return render(request, 'course/addcourse.html', {'form': form, 'saved': saved, 'course': course})

# exam & add exam views

class ExamForm(ModelForm):
  class Meta:
    model = Exam
    exclude = ('submitter',)

class ExamFileForm(ModelForm):
  class Meta:
    model = ExamFile
    exclude = ('exam',)

def allowed_to_edit_exam(exam, user):
  return exam.submitter == user

def examview(request, exam_id, _ignore=None):
  exam = get_object_or_404(Exam, pk=exam_id)
  fileform = ExamFileForm()
  added = False
  if request.method == 'POST':
    fileform = ExamFileForm(request.POST, request.FILES)
    if fileform.is_valid():
      examfile = fileform.save(commit = False)
      examfile.exam = exam
      examfile.save()
      fileform = ExamFileForm()
      added = True
  return render(request, 'exam/examview.html', {'exam': exam, 'files': exam.examfile_set.all(), 'fileform': fileform, 'added': added, 'allowed_to_edit_exam': allowed_to_edit_exam(exam, request.user)})

def delete_exam(request, exam_id, _ignore=None):
  if request.method == 'POST':
    exam = get_object_or_404(Exam, pk=exam_id)
    if allowed_to_edit_exam(exam, request.user):
      exam.delete()
      return HttpResponseRedirect(exam.course.get_absolute_url())
    else:
      return HttpResponseForbidden("403 Forbidden")
  else:
    return HttpResponseNotAllowed("405 Method not allowed")

def delete_examfile(request, examfile_id):
  if request.method == 'POST':
    examfile = get_object_or_404(ExamFile, pk=examfile_id)
    if allowed_to_edit_exam(examfile.exam, request.user):
      examfile.delete()
      return HttpResponseRedirect(examfile.exam.get_absolute_url())
    else:
      return HttpResponseForbidden("403 Forbidden")
  else:
    return HttpResponseNotAllowed("405 Method not allowed")

def edit_exam(request, exam_id, _ignore=None):
  exam = get_object_or_404(Exam, pk=exam_id)
  if not allowed_to_edit_exam(exam, request.user):
    return HttpResponseForbidden("403 Forbidden")
  form = ExamForm(instance=exam)
  if request.method == 'POST':
    form = ExamForm(request.POST, instance=exam)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(exam.get_absolute_url())
  return render(request, 'exam/editexam.html', {'form': form})

def addexam(request):
  added = False
  exam = None
  form = ExamForm(initial = {"exam_date": datetime.now().strftime("%Y-%m-%d")})
  fileform = ExamFileForm()
  if request.method == 'POST':
    form = ExamForm(request.POST)
    fileform = ExamFileForm(request.POST, request.FILES)
    if form.is_valid() and fileform.is_valid():
      exam = form.save(commit = False)
      if request.user.is_authenticated:
        exam.submitter = request.user
      exam.save()
      examfile = fileform.save(commit = False)
      examfile.exam = exam
      examfile.save()
      fileform = ExamFileForm()
      form = ExamForm()
      added = True
  # sort the courses properly
  form.fields["course"].queryset = Course.objects.order_by('code').all()
  return render(request, 'exam/addexam.html', {'form': form, 'added': added, 'fileform': fileform, 'new_exam': exam})


# user registration view

# a user creation form that requires email
class UserCreationEmailForm(UserCreationForm):
  email = EmailField(required=True, help_text = "We will only use email to help you recover your account.")
  class Meta:
    model = User
    fields = ("username", "email", "password1", "password2")
  def save(self, commit=True):
    user = super(UserCreationEmailForm, self).save(commit=False)
    user.email = self.cleaned_data["email"]
    if commit:
      user.save()
    return user

def register(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect('/')

  created = False
  if request.method == 'POST':
    form = UserCreationEmailForm(request.POST)
    if form.is_valid():
      created = True
      form.save()
      # a hack (?) to log the user in after registering
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
      login(request, user)
  else:
    form = UserCreationEmailForm()
  return render(request, 'account/register.html', {'form': form, 'created': created})

# view for changing account details

class ModifyAccountForm(Form):
  current_password = CharField(widget = PasswordInput)
  email = EmailField()
  new_password1 = CharField(label = "New password", help_text = "Optional", widget = PasswordInput, required = False)
  new_password2 = CharField(label = "New password confirmation", help_text = "Enter the same password as above, for verification if you want to change your password.", widget = PasswordInput, required = False)

  def clean(self):
    cleaned_data = super(ModifyAccountForm, self).clean()
    new_pw1 = cleaned_data.get('new_password1')
    new_pw2 = cleaned_data.get('new_password2')
    if new_pw1 != new_pw2:
      del cleaned_data['new_password1']
      del cleaned_data['new_password2']
      self._errors['new_password2'] = self.error_class(["The two password fields didn't match."])

    return cleaned_data

@login_required
def modifyaccount(request):
  form = ModifyAccountForm(initial = {"email": request.user.email})
  saved = False
  if request.method == "POST":
    form = ModifyAccountForm(request.POST)
    if form.is_valid():
      auth_user = authenticate(username = request.user.username, password = form.cleaned_data['current_password'])
      if auth_user is not None:
        # form valid, password correct, save the data
        if form.cleaned_data['new_password1'] != '':
          auth_user.set_password(form.cleaned_data['new_password1'])
          new_pw = True
        auth_user.email = form.cleaned_data['email']
        saved = True
        auth_user.save()
      else:
        form._errors['current_password'] = form.error_class(["The password was wrong!"])
  return render(request, 'account/modifyaccount.html', {"form": form, 'saved': saved})

# view for exams added by current user
@login_required
def accountexams(request):
  exams = Exam.objects.filter(submitter = request.user).order_by("-date_added")
  return render(request, 'account/ownexams.html', {"exams": exams})
