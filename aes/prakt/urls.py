from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^internship/org(?P<orgId>\d+)/evt(?P<evtId>\d{0,3})/', views.internship_evt),
    url(r'^internship/org(?P<orgId>\d+)/emp(?P<empId>\d{0,3})/', views.internship_emp),
    url(r'^internship/org(?P<orgId>\d+)/doc(?P<docId>\d{0,3})/', views.documents),
    url(r'^internship/org(?P<orgId>\d{0,3})/', views.internship_org),
    url(r'^tasks/', views.tasks),
    url(r'^internship', views.internship_org),
    url(r'^download/(?P<filename>.+)$', views.file_view),
    url(r'^login/', views.log_in),
    url(r'^logout/', views.log_out),
    url(r'^$', views.index)
]
