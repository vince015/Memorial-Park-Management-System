from django.conf.urls import url
from memorial_park_mgmnt_app import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    #####
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contract/list$', views.ContractListView.as_view(), name='contract_list'),
    url(r'^contract/read/(?P<contract_id>[\d]+)$', views.ContractReadView.as_view(), name='contract_read'),
    url(r'^contract/update/(?P<contract_id>[\d]+)$', views.ContractUpdateView.as_view(), name='contract_update'),
    url(r'^contract/create$', views.ContractCreateView.as_view(), name='contract_create'),
    url(r'^downpayment/create/(?P<contract_id>[\d]+)$', views.DownpaymentCreateView.as_view(), name='downpayment_create'),
    url(r'^commission/create/(?P<contract_id>[\d]+)$', views.CommissionCreateView.as_view(), name='commission_create'),
    url(r'^client/update/(?P<client_id>[\d]+)$', views.ClientUpdateView.as_view(), name='client_update'),
    url(r'^client/create$', views.ClientCreateView.as_view(), name='client_create'),
    url(r'^client/list$', views.ClientListView.as_view(), name='client_list'),
    url(r'^agent/update/(?P<agent_id>[\d]+)$', views.AgentUpdateView.as_view(), name='agent_update'),
    url(r'^agent/create$', views.AgentCreateView.as_view(), name='agent_create'),
    url(r'^agent/list$', views.AgentListView.as_view(), name='agent_list'),
    ### lookups ###
    url(r'^lookup/lot$', views.lot_lookup, name='lot_lookup'),
    url(r'^lookup/client$', views.client_lookup, name='client_lookup'),
    url(r'^lookup/agent$', views.agent_lookup, name='agent_lookup'),
    ### json ###
    url(r'^json/contract$', views.ContractJson.as_view(), name='contract_json'),
    url(r'^json/agent$', views.AgentJson.as_view(), name='agent_json'),
    url(r'^json/client$', views.ClientJson.as_view(), name='client_json'),
]