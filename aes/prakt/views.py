# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist, SuspiciousFileOperation
from .models import Org, Employee, Events, EventType, TaskStatus, Tasks, Docs
from .forms import orgForm, empForm, evtForm, tskForm, loginForm, docsForm
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from pathlib import Path
from django.conf import settings
import os
import mimetypes


def log_in(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["userpass"])
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.POST.get("backlink", "/internship/org1/"))
            else:
                return render(request, "login.html",
                              {"form": form.as_p(), "message": "Такой пользователь не найден.",
                               "backlink": request.POST.get('backlink')})
        else:
            return render(request, "login.html", {"form": form.as_p(), "message": "Форма не прошла валидацию.",
                                                  "backlink": request.POST.get('backlink')})
    else:
        form = loginForm()
        return render(request, "login.html", {"form": form.as_p(), "message": request.user.username,
                                              "backlink": request.GET.get('next')})


def log_out(request):
    logout(request)
    return HttpResponse("Выход выполнен.") # HttpResponseRedirect("/login/")


@login_required
def documents(request, orgId="", docId=""):
    action = request.GET.get("action", "")
    if action == "create" or action == "edit":
        if request.method == "POST":
            form = docsForm(request.POST, request.FILES)
            if form.is_valid():
               if action == "create":
                   doc = Docs(number=form.cleaned_data['number'], date=form.cleaned_data['date'],
                              description=form.cleaned_data['description'], file=form.cleaned_data['file'],
                              org=Org.objects.get(id=orgId))
               elif action == "edit":
                   doc = Docs.objects.get(id=docId)
                   doc.number = form.cleaned_data['number']
                   doc.date = form.cleaned_data['date']
                   doc.description = form.cleaned_data['description']
                   if form.cleaned_data['file'] is not None: doc.file = form.cleaned_data['file']
                   doc.org = Org.objects.get(id=orgId)
               doc.save()
               return HttpResponseRedirect(request.POST.get("backlink", "/internship/"))
            else:
               return render(request, "form.html", {"form": form.as_p(), "message": form.errors,
                                                    "backlink": request.POST.get("backlink", "/internship/")})
        else:
            form = docsForm() if action == "create" else docsForm(instance=Docs.objects.get(id=docId))
            if action == "edit": form.base_fields['file'].required = False
            return render(request, "form.html", {"title": "Документы " + str(Org.objects.get(id=orgId)), "form": form.as_p(), "backlink": request.META['HTTP_REFERER']})
    elif action == "delete":
        doc = Docs.objects.get(id=docId)
        doc.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("Ошибка вычисление действия.")


@login_required
def index(request):
    #return HttpResponse("Необходимо ввести более конкретный адрес")
    return HttpResponseRedirect("/internship/org1/")


@login_required
def internship_org(request, orgId=""):
    action = request.GET.get("action", "")
    if action == "":
        # выводим информацию об организации
        orgs = Org.objects.all()
        currentOrg = Org.objects.get(id=orgId) if orgId != "" else ""
        currentOrgEmpl = Employee.objects.filter(org=orgId) if orgId != "" else ""
        currentOrgEvts = Events.objects.filter(org=orgId) if orgId != "" else ""
        tasks = Tasks.objects.filter(status=TaskStatus.objects.get(status='В работе')) if orgId != "" else ""
        currentOrgDocs = Docs.objects.filter(org=orgId) if orgId != "" else ""
        # выбираем доменную часть из электронной почты ответственного за практику
        empemail = Employee.objects.filter(org=orgId, prakt=True).exclude(email="") if orgId != "" else ""
        if empemail != "" and empemail.count()>0:
            domen = empemail[0].email.split("@")[1]
        else: domen = ""
        return render(request, "index.html", {"organisations": orgs, "currentOrg": currentOrg,
                                              "emps": currentOrgEmpl, "evts": currentOrgEvts,
                                              "tasks": tasks, "docs": currentOrgDocs,
                                              "mailbox": settings.MAILBOX_BASE_PATH,
                                              "orgdomen": domen})
    elif action == "create":
        # выводим форму на добавление новой организации
        if request.method == "POST":
            form = orgForm(request.POST)
            if form.is_valid():
                org = Org()
                org.title = form.cleaned_data["title"]
                org.titleFull = form.cleaned_data["titleFull"]
                org.titleShort = form.cleaned_data["titleShort"]
                org.address = form.cleaned_data["address"]
                org.site = form.cleaned_data["site"]
                org.phone = form.cleaned_data["phone"]
                org.maildir = form.cleaned_data["maildir"]
                org.terms = form.cleaned_data.get("terms")
                org.save()
                return HttpResponseRedirect("/internship/org" + str(org.id) + "/")
            else:
                form = orgForm(request.POST)
                return render(request, "org.html", {"form": form.as_p(), "backlink": request.META['HTTP_REFERER']})
        else:
            form = orgForm()
            return render(request, "org.html", {"form": form.as_p(), "backlink": request.META['HTTP_REFERER']})
    elif action == "edit":
        # выводим форму на изменение данных организации
        if request.method == "POST":
            form = orgForm(request.POST)
            if form.is_valid():
                org = Org.objects.get(id=orgId)
                org.title = form.cleaned_data["title"]
                org.titleFull = form.cleaned_data["titleFull"]
                org.titleShort = form.cleaned_data["titleShort"]
                org.address = form.cleaned_data["address"]
                org.site = form.cleaned_data["site"]
                org.phone = form.cleaned_data["phone"]
                org.maildir = form.cleaned_data["maildir"]
                org.terms = form.cleaned_data.get("terms")
                org.save()
                return HttpResponseRedirect("/internship/org" + orgId + "/")
            else:
                return render(request, "org.html", {"form": form.as_p(), "message": form.errors, "backlink": request.META['HTTP_REFERER']})
        else:
            try:
                form = orgForm(instance=Org.objects.get(id=orgId))
                return render(request, "org.html", {"form": form.as_p(), "backlink": request.META['HTTP_REFERER']})
            except ObjectDoesNotExist:
                return HttpResponse("Организация не найдена")


@login_required
def file_download(request, filename=""):
    fullpath = str(settings.MEDIA_ROOT).replace("\\", "/") + "/" + filename
    file = open(fullpath, "rb")
    response = HttpResponse(file.read())
    file_type = mimetypes.guess_type(fullpath)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(fullpath).st_size)
    response['Content-Disposition'] = "attachment; filename=" + filename
    file.close()
    return response


@login_required
def file_view(request, filename=""):
    try:
        return FileResponse(open(str(settings.MEDIA_ROOT).replace("\\", "/") + "/" + filename, "rb"),
                            content_type='application/pdf')
    except FileNotFoundError:
        return Http404()


@login_required
def internship_emp(request, orgId="", empId=""):
    action = request.GET.get("action", "")
    if action == "" or orgId == "":
        # без указания действия или организации выводим форму организации
        internship_org(request, orgId)
    elif action == "create":
        # выводим форму на добавление работника с предопределенной организацией
        orgtitle = Org.objects.get(id=orgId).title
        if request.method == "POST":
            form = empForm(request.POST)
            if form.is_valid():
                emp = Employee(fname = form.cleaned_data["fname"], sname = form.cleaned_data["sname"], lname = form.cleaned_data["lname"],
                               phone = form.cleaned_data["phone"], email = form.cleaned_data["email"], post = form.cleaned_data["post"],
                               prakt = form.cleaned_data['prakt'], comment = form.cleaned_data["comment"], org_id = orgId)
                emp.save()
                return HttpResponseRedirect("/internship/org" + orgId + "/#employees")
            else:
                return render(request, "emp.html", {"form": form.as_p(), "message": form.errors, "org": orgtitle,
                              "backlink": request.POST.get('backlink')})
        else:
            return render(request, "emp.html", {"form": empForm().as_p(), "org": orgtitle,
                              "backlink": request.META['HTTP_REFERER']})
    elif action == "edit":
        # изменение характеристик работника
        orgtitle = Org.objects.get(id=orgId).title
        if request.method == "POST":
            form = empForm(request.POST)
            if form.is_valid():
                emp = Employee.objects.get(id=empId)
                emp.fname = form.cleaned_data["fname"]
                emp.sname = form.cleaned_data["sname"]
                emp.lname = form.cleaned_data["lname"]
                emp.phone = form.cleaned_data["phone"]
                emp.email = form.cleaned_data["email"]
                emp.post = form.cleaned_data["post"]
                emp.prakt = form.cleaned_data["prakt"]
                emp.comment = form.cleaned_data["comment"]
                emp.save()
                return HttpResponseRedirect("/internship/org" + orgId + "/#employees")
            else:
                return render(request, "emp.html", {"form": form.as_p(), "message": "Значения не прошли проверку.",
                                                    "org": orgtitle, "backlink": request.POST.get('backlink')})
        else:
            try:
                form = empForm(instance=Employee.objects.get(id=empId))
                return render(request, "emp.html", {"form": form.as_p(), "org": orgtitle,
                              "backlink": request.META['HTTP_REFERER']})
            except ObjectDoesNotExist:
                return HttpResponse("Работник не найден")
    elif action == "delete":
        # удаление работника
        try:
            emp = Employee.objects.get(id=empId)
            emp.delete()
            return HttpResponseRedirect("/internship/org" + orgId + "/#employees")
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/internship/org" + orgId + "/#employees")


@login_required
def internship_evt(request, orgId="", evtId=""):
    action = request.GET.get("action", "")
    type = request.GET.get("type", "")
    empid = request.GET.get("emp", "")
    if action == "" or orgId == "":
        # без указания - выводим форму организации
        internship_org(request, orgId)
    elif action == "create":
        # выводим форму на добавление события
        orgtitle = Org.objects.get(id=orgId).title
        if request.method == "POST":
            form = evtForm(request.POST)
            form.fields['person'].queryset = Employee.objects.filter(org=orgId)
            if form.is_valid():
                evt = Events(type = form.cleaned_data["type"], date = form.cleaned_data["date"],
                             org = Org.objects.get(id=orgId), person = form.cleaned_data["person"], description = form.cleaned_data["description"])
                evt.save()
                return HttpResponseRedirect("/internship/org" + orgId + "/#events")
            else:
                return render(request, "evt.html", {"evt": request.POST, "message": form.errors, "form": form.as_p(),
                                                    "backlink": request.POST.get('backlink'), "org": orgtitle})
        else:
            f = evtForm()
            if type != "":
                f.fields['type'].initial = EventType.objects.get(css=type)
            f.fields['date'].initial = datetime.now().strftime("%d.%m.%Y")
            f.fields['person'].queryset = Employee.objects.filter(org=orgId)
            if empid != "":
                f.fields['person'].initial = Employee.objects.get(id=empid)
            return render(request, "evt.html", {"form": f.as_p(), "backlink": request.META['HTTP_REFERER'], "org": orgtitle})
    elif action == "edit":
        # изменение события
        orgtitle = Org.objects.get(id=orgId).title
        if request.method == "POST":
            form = evtForm(request.POST)
            form.fields['person'].queryset = Employee.objects.filter(org=orgId)
            if form.is_valid():
                evt = Events.objects.get(id=evtId)
                evt.type = form.cleaned_data["type"]
                evt.date = form.cleaned_data["date"]
                evt.person = form.cleaned_data["person"]
                evt.description = form.cleaned_data["description"]
                evt.save()
                return HttpResponseRedirect("/internship/org" + orgId + "/#events")
            else:
                return render(request, "evt.html", {"message": "Значения не прошли проверку.", "form": form.as_p(),
                                                    "backlink": request.POST.get('backlink'), "org": orgtitle})
        else:
            try:
                form = evtForm(instance=Events.objects.get(id=evtId))
                form.fields['person'].queryset = Employee.objects.filter(org=orgId)
                return render(request, "evt.html", {"form": form.as_p(), "backlink": request.META['HTTP_REFERER'], "org": orgtitle})
            except ObjectDoesNotExist:
                return HttpResponse("Событие не найдено")
    elif action == "delete":
        # удаление события
        try:
            evt = Events.objects.get(id=evtId)
            evt.delete()
            return HttpResponseRedirect("/internship/org" + orgId + "/#events")
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/internship/org" + orgId + "/#events")


@login_required
def tasks(request):
    action = request.GET.get("action", "")
    taskid = request.GET.get("id", "")
    if action == "create" or action == "edit":
        if request.method == "POST":
            form = tskForm(request.POST)
            if form.is_valid():
                if action == "create":
                    task = Tasks(deadline=form.cleaned_data['deadline'], org=form.cleaned_data['org'],
                                 description=form.cleaned_data['description'])
                    task.status = TaskStatus.objects.get(status='В работе')
                    task.statuschangedate = timezone.now().date()
                elif action == "edit":
                    task = Tasks.objects.get(id=taskid)
                    task.deadline = form.cleaned_data['deadline']
                    task.org = form.cleaned_data['org']
                    task.description=form.cleaned_data['description']
                task.save()
                orgid = str(form.cleaned_data['org'].id) if form.cleaned_data['org'] else ''
                return HttpResponseRedirect(request.POST.get('backlink'))
            else:
                return render(request, "tsk.html", {"message": form.errors, "form": form.as_p(), "backlink": request.POST.get('backlink')})
        else:
            form = tskForm() if action == "create" else tskForm(instance=Tasks.objects.get(id=taskid))
            return render(request, "tsk.html", {"form": form.as_p(), "backlink": request.META['HTTP_REFERER']})
    elif action == "delete":
        try:
            task = Tasks.objects.get(id=taskid)
            task.delete()
            #task.status = TaskStatus.objects.get(status='Удалено')
            #task.save()
        finally: return HttpResponseRedirect(request.META['HTTP_REFERER'])
    elif action == "status_done":
        task = Tasks.objects.get(id=taskid)
        task.status = TaskStatus.objects.get(status='Выполнено')
        task.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

