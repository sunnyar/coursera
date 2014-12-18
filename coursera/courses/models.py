from django.db import models

class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    suffix_name= models.CharField(max_length=100)

    def __unicode__(self) :
        return '%s - %s, %s' % (self.first_name, self.last_name, self.suffix_name)

class Category(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)

    def __unicode__(self) :
        return '%s' % (self.name)

class University(models.Model):
    name = models.CharField(max_length=100)
    banner = models.CharField(max_length=100)
    home_link = models.URLField()

    def __unicode__(self) :
        return '%s, %s, %s' % (self.name, self.banner, self.home_link)

class Session(models.Model):
    home_link = models.URLField()
    active = models.BooleanField(default=False)
    duration_string = models.CharField(max_length=100)
    start_day = models.CharField(max_length=100)
    start_month = models.CharField(max_length=100)
    start_year = models.CharField(max_length=100)

    def __unicode__(self) :
        return '%s, %s, %s, %s-%s-%s' % (self.home_link, self.active, self.duration_string, self.start_day, self.start_month, self.start_year)


class Course(models.Model):

    key = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=20)
    photo = models.CharField(max_length=100)
    trailer = models.CharField(max_length=100)
    short_summary = models.CharField(max_length=200)
    summary = models.CharField(max_length=1000)
    recommended_background = models.CharField(max_length=200)
    syllabus = models.CharField(max_length=100)
    faq = models.CharField(max_length=100)
    instructors = models.ManyToManyField(Instructor)
    categories = models.ManyToManyField(Category)
    universities = models.ManyToManyField(University)
    sessions = models.ManyToManyField(Session)

    def __unicode__(self) :
        return '%s, %s, %s' % (self.key, self.title, self.language)