# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from os import path


class Org(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название для базы")
    titleFull = models.CharField(max_length=255, verbose_name="Полное наименование")
    titleShort = models.CharField(max_length=200, verbose_name="Сокращенное наименование")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    site = models.URLField(blank=True, verbose_name="Сайт")
    phone = models.CharField(blank=True, max_length=200, verbose_name="Телефоны")
    maildir = models.IntegerField(blank=True, null=True, verbose_name="Номер папки в почтовом ящике")
    terms = models.TextField(blank=True, verbose_name="Условия практики")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Employee(models.Model):
    fname = models.CharField(max_length=100, blank=False, null=False, verbose_name="Имя")
    sname = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    lname = models.CharField(max_length=100, blank=True, verbose_name="Фамилия")
    phone = models.CharField(max_length=100, blank=True, verbose_name="Телефон")
    email = models.EmailField(max_length=100, blank=True, verbose_name="Почта")
    post = models.CharField(max_length=150, blank=True, verbose_name="Должность")
    prakt = models.BooleanField(default=False, verbose_name="Практика?")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Организация")
    comment = models.CharField(max_length=255, blank=True, null=False, verbose_name="Примечания")

    def __unicode__(self):
        return '%s %s %s' % (self.lname, self.fname, self.sname)


class EventType(models.Model):
    type = models.CharField(max_length=50, blank=False, null=True, verbose_name="Тип события")
    css = models.CharField(max_length=50, verbose_name="CSS класс")

    def __unicode__(self):
        return self.type


class Events(models.Model):
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name="Тип события")
    date = models.DateField(blank=False, null=True, verbose_name="Дата")
    person = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Контактное лицо")
    org = models.ForeignKey(Org, on_delete=models.SET_NULL, blank=False, null=True,  verbose_name="Организация")
    description = models.TextField(max_length=500, blank=False, null=True,  verbose_name="Описание события")

    class Meta:
        ordering = ('-date',)


class TaskStatus(models.Model):
    status = models.CharField(max_length=15)

    def __unicode__(self):
        return self.status


class Tasks(models.Model):
    deadline = models.DateField(blank=False, null=False, verbose_name="Срок исполнения")
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, verbose_name="Статус")
    statuschangedate = models.DateField(blank=False, null=True, verbose_name="Дата изменения статуса")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, blank=True, null=False, verbose_name="Организация")
    description = models.TextField(max_length=500, verbose_name="Описание")

    class Meta:
        ordering = ('deadline',)

    @property
    def days_until(self):
        return (self.deadline - timezone.now().date()).days


class Students(models.Model):
    fname = models.CharField(max_length=20, verbose_name="Имя")
    sname = models.CharField(max_length=20, verbose_name="Отчество")
    lname = models.CharField(max_length=20, verbose_name="Фамилия")
    enter_year = models.IntegerField(verbose_name="Год зачисления")
    vk_link = models.URLField(verbose_name="Ссылка на личку")
    password = models.CharField(verbose_name="Номер паспорта (пароль)")

    def __unicode__(self):
        return '%s %s. %s.' % (self.lname, self.fname[0], self.sname[0])

    class Meta:
        ordering = ('lname',)


class PracticeType(models.Model):
    type = models.CharField(max_length=150, verbose_name="Тип практики")

    class Meta:
        verbose_name = 'Тип практики'
        verbose_name_plural = 'Типы практик'


class Practice(models.Model):
    year = models.IntegerField(verbose_name="Год проведения")
    course = models.IntegerField(verbose_name="Курс")
    type = models.ForeignKey(PracticeType, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Тип практики")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата завершения")
    editable = models.BooleanField(verbose_name="Возможность редактирования", default=False)

    class Meta:
        verbose_name = 'Практика'
        verbose_name_plural = 'Практики'


class PracticePriorities(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Практика")
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Студент")
    priority_1 = models.ManyToManyField(Org, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Приоритет №1")
    priority_2 = models.ManyToManyField(Org, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Приоритет №2")
    priority_3 = models.ManyToManyField(Org, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Приоритет №3")
    priority_4 = models.ManyToManyField(Org, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Приоритет №4")
    practice_place = models.ManyToManyField(Org, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Место прохождения практики")


class AcademicDegree(models.Model):
    degree = models.CharField(max_length=50, verbose_name="Наименование")
    degree_short = models.CharField(max_length=10, verbose_name="Сокращённо")

    def __unicode__(self):
        return self.degree

    class Meta:
        verbose_name = 'Ученая степень'
        verbose_name_plural = 'Ученые степени'


class AcademicStatus(models.Model):
    status = models.CharField(max_length=50, verbose_name="Наименование")

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name = 'Ученое звание'
        verbose_name_plural = 'Ученые звания'


class Posts(models.Model):
    post_name = models.CharField(max_length=30, verbose_name="Наименование")

    def __unicode__(self):
        return self.post_name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

class Teachers(models.Model):
    fname = models.CharField(max_length=20, verbose_name="Имя")
    sname = models.CharField(max_length=20, verbose_name="Отчество")
    lname = models.CharField(max_length=20, verbose_name="Фамилия")
    post = models.ForeignKey(Posts, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Должность")
    degree = models.ForeignKey(AcademicDegree, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Учёная степень")
    status = models.ForeignKey(AcademicStatus, on_delete=models.SET_NULL, blank=False, null=True, verbose_name="Учёное звание")

    def __unicode__(self):
        return '%s %s. %s.' % (self.lname, self.fname[0], self.sname[0])

    class Meta:
        ordering = ('lname',)
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


def file_upload(instance, filename):
    (fname, ext) = path.splitext(filename)
    fname = fname.encode('utf-8')
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'х': 'H',
              'Ц': 'C', 'Ч': 'Cz', 'Ш': 'Sh', 'Щ': 'Scz', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'Ya', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e'}
    for key in slovar:
        fname = fname.replace(key, slovar[key])
    return fname + ext


class Docs(models.Model):
    number = models.CharField(blank=True, max_length=100, verbose_name="Номер документа")
    date = models.DateField(blank=True, null=True, verbose_name="Дата документа")
    description = models.CharField(blank=True, max_length=150, verbose_name="Описание")
    file = models.FileField(upload_to=file_upload, verbose_name="Файл")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Организация")
    inf = models.BooleanField(default=False, verbose_name="Информационный материал")


@receiver(post_delete, sender=Docs)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
