from django.conf.urls import url
from memorial_park_mgmnt_app import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contract/list$', views.ContractListView.as_view(), name='contract_list'),
    url(r'^contract/read/(?P<contract_id>[\d]+)$', views.ContractReadView.as_view(), name='contract_read'),
    url(r'^json/contract$', views.ContractJson.as_view(), name='contract_json'),
]