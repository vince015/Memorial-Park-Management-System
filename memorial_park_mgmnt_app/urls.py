from django.conf.urls import url
from memorial_park_mgmnt_app import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contract/list$', views.ContractListView.as_view(), name='contract_list'),
    url(r'^contract/read/(?P<contract_id>[\d]+)$', views.ContractReadView.as_view(), name='contract_read'),
    url(r'^contract/update/(?P<contract_id>[\d]+)$', views.ContractUpdateView.as_view(), name='contract_update'),
    url(r'^contract/create$', views.ContractCreateView.as_view(), name='contract_create'),
    url(r'^json/contract$', views.ContractJson.as_view(), name='contract_json'),
    url(r'^downpayment/create/(?P<contract_id>[\d]+)$', views.DownpaymentCreateView.as_view(), name='downpayment_create'),
    url(r'^commission/create/(?P<contract_id>[\d]+)$', views.CommissionCreateView.as_view(), name='commission_create'),
    url(r'^client/update/(?P<contract_id>[\d]+)/(?P<client_id>[\d]+)$', views.ClientUpdateView.as_view(), name='client_update'),
    url(r'^client/create$', views.ClientCreateView.as_view(), name='client_create'),
    url(r'^agent/update/(?P<contract_id>[\d]+)/(?P<agent_id>[\d]+)$', views.AgentUpdateView.as_view(), name='agent_update'),
    url(r'^agent/create$', views.AgentCreateView.as_view(), name='agent_create'),
]