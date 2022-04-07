from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from exams.utils import ExtFileField
from django.conf import settings
from os import path

class Course(models.Model):
  code = models.CharField(max_length = 20, unique = True)
  name = models.CharField(max_length = 100)
  def get_absolute_url(self):
    return "/courses/%i/%s/" % (self.id, slugify(self.name))
  def __str__(self):
    return "%s: %s" % (self.code, self.name)

class Lang(models.Model):
  code = models.CharField(max_length = 3)
  name = models.CharField(max_length = 20)
  def __str__(self):
    return self.name

class Exam(models.Model):
  course = models.ForeignKey(Course, on_delete=models.PROTECT)
  desc = models.CharField(max_length = 100, help_text = "e.g. \"second midterm\"")
  exam_date = models.DateField(help_text = "Please use the following format: YYYY-MM-DD.")
  date_added = models.DateField(auto_now_add = True)
  lang = models.ForeignKey(Lang, on_delete=models.PROTECT)
  submitter = models.ForeignKey(User, null = True, blank = True, on_delete=models.SET_NULL)
  def get_absolute_url(self):
    return "/exams/%i/%s/%s/" % (self.id, slugify(self.course.name), slugify(self.exam_date))
  def __str__(self):
    return "%s: %s %s" % (self.course.code, self.exam_date, self.desc)

def exam_file_name(instance, filename):
  return path.join('exams', str(instance.exam.id) + path.splitext(filename)[1])

class ExamFile(models.Model):
  exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
  exam_file = ExtFileField(upload_to = exam_file_name, ext_whitelist = settings.TENTTIARKISTO_FILE_EXTENSIONS)

@receiver(post_delete, sender=ExamFile)
def post_delete_file(instance, **kwargs):
  instance.exam_file.delete(save=False)

# maintainers for frontpage

class Maintainer(models.Model):
  group = models.CharField(max_length = 100)
  email = models.EmailField()

  def view_email(self):
    return self.email.replace("@", " (at) ")
