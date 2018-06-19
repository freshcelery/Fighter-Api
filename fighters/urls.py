from django.conf.urls import url
from fighters import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view(), name=views.UserList.name),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name=views.UserDetail.name),
    url(r'^weightclasses/$', views.WeightclassList.as_view(), name=views.WeightclassList.name),
    url(r'^weightclasses/(?P<pk>[0-9]+)/$', views.WeightclassDetail.as_view(), name=views.WeightclassDetail.name),
    url(r'^fighters/$', views.FighterList.as_view(), name=views.FighterList.name),
    url(r'^fighters/(?P<pk>[0-9]+)/$', views.FighterDetail.as_view(), name=views.FighterDetail.name),
    url(r'^$', views.ApiRoot.as_view(), name=views.ApiRoot.name)
]