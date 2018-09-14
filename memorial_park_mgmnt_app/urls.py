from django.conf.urls import url
from memorial_park_mgmnt_app.views import (login,
                                           contract,
                                           client,
                                           agent,
                                           lookup)

urlpatterns = [
    url(r'^login/$', login.LoginView.as_view(), name='login'),
    url(r'^branch$', login.BranchView.as_view(), name='branch'),
    url(r'^logout$', login.LogoutView.as_view(), name='logout'),
    #####
    url(r'^$', contract.ContractListView.as_view(), name='home'),
    url(r'^contract/list$', contract.ContractListView.as_view(), name='contract_list'),
    url(r'^contract/json$', contract.ContractJson.as_view(), name='contract_json'),
    url(r'^contract/create$', contract.ContractCreateView.as_view(), name='contract_create'),
    # url(r'^contract/read/(?P<contract_id>[\d]+)$', views.ContractReadView.as_view(), name='contract_read'),
    # url(r'^contract/update/(?P<contract_id>[\d]+)$', views.ContractUpdateView.as_view(), name='contract_update'),
    # url(r'^downpayment/create/(?P<contract_id>[\d]+)$', views.DownpaymentCreateView.as_view(), name='downpayment_create'),
    # url(r'^commission/create/(?P<contract_id>[\d]+)$', views.CommissionCreateView.as_view(), name='commission_create'),
    url(r'^client/list$', client.ClientListView.as_view(), name='client_list'),
    url(r'^client/json$', client.ClientJson.as_view(), name='client_json'),
    url(r'^client/create$', client.ClientCreateView.as_view(), name='client_create'),
    url(r'^client/update/(?P<client_id>[\d]+)$', client.ClientUpdateView.as_view(), name='client_update'),
    url(r'^agent/list$', agent.AgentListView.as_view(), name='agent_list'),
    url(r'^agent/json$', agent.AgentJson.as_view(), name='agent_json'),
    url(r'^agent/create$', agent.AgentCreateView.as_view(), name='agent_create'),
    url(r'^agent/update/(?P<agent_id>[\d]+)$', agent.AgentUpdateView.as_view(), name='agent_update'),
    ### lookups ###
    url(r'^lookup/lot$', lookup.lot_lookup, name='lot_lookup'),
    url(r'^lookup/client$', lookup.client_lookup, name='client_lookup'),
    url(r'^lookup/agent$', lookup.agent_lookup, name='agent_lookup'),
    ### json ###
]