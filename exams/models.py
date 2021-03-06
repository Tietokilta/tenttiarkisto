from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from exams.utils import ExtFileField
from django.conf import settings
from os import path

class Course(models.Model):
  code = models.CharField(max_length = 20, unique = True)
  name = models.CharField(max_length = 100)
  def get_absolute_url(self):
    return "/courses/%i/%s/" % (self.id, slugify(self.name))
  def __unicode__(self):
    return "%s: %s" % (self.code, self.name)

class Lang(models.Model):
  code = models.CharField(max_length = 3)
  name = models.CharField(max_length = 20)
  def __unicode__(self):
    return self.name

class Exam(models.Model):
  course = models.ForeignKey(Course)
  desc = models.CharField(max_length = 100, help_text = "e.g. \"second midterm\"")
  exam_date = models.DateField(help_text = "Please use the following format: YYYY-MM-DD.")
  date_added = models.DateField(auto_now_add = True)
  lang = models.ForeignKey(Lang)
  submitter = models.ForeignKey(User, null = True, blank = True)
  def get_absolute_url(self):
    return "/exams/%i/%s/%s/" % (self.id, slugify(self.course.name), slugify(self.exam_date))
  def __unicode__(self):
    return "%s: %s %s" % (self.course.code, self.exam_date, self.desc)

def exam_file_name(instance, filename):
  return '/'.join(['exams',  ''.join([str(instance.exam.id), path.splitext(filename)[1]])])

class ExamFile(models.Model):
  exam = models.ForeignKey(Exam)
  exam_file = ExtFileField(upload_to = exam_file_name, ext_whitelist = settings.TENTTIARKISTO_FILE_EXTENSIONS)

# maintainers for frontpage

class Maintainer(models.Model):
  group = models.CharField(max_length = 100)
  email = models.EmailField()

  def view_email(self):
    return self.email.replace("@", " (at) ")
