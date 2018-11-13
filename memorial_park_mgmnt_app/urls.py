from django.conf.urls import url
from memorial_park_mgmnt_app.views import (login,
                                           home,
                                           contract,
                                           client,
                                           agent,
                                           bill,
                                           receipt,
                                           payment,
                                           commission,
                                           service,
                                           lookup)

urlpatterns = [
    url(r'^$', home.HomeView.as_view(), name='home'),
    url(r'^home/due$', home.DueBillsView.as_view(), name='home_due'),
    url(r'^home/commissions$', home.CommisionRecentView.as_view(), name='home_commissions'),
    #####
    url(r'^login/$', login.LoginView.as_view(), name='login'),
    url(r'^branch$', login.BranchView.as_view(), name='branch'),
    url(r'^logout$', login.LogoutView.as_view(), name='logout'),
    #####
    url(r'^$', home.HomeView.as_view(), name='home'),
    url(r'^contract/list$', contract.ContractListView.as_view(), name='contract_list'),
    url(r'^contract/json$', contract.ContractJson.as_view(), name='contract_json'),
    url(r'^contract/create$', contract.ContractCreateView.as_view(), name='contract_create'),
    url(r'^contract/read/(?P<contract_id>[\d]+)$', contract.ContractReadView.as_view(), name='contract_read'),
    url(r'^contract/update/(?P<contract_id>[\d]+)$', contract.ContractUpdateView.as_view(), name='contract_update'),
    url(r'^contract/(?P<contract_id>[\d]+)/spot$', contract.ContractSpotView.as_view(), name='contract_spot'),
    url(r'^contract/(?P<contract_id>[\d]+)/installment$', contract.ContractInstallmentView.as_view(), name='contract_installment'),
    url(r'^contract/(?P<contract_id>[\d]+)/installment/compute$', contract.ContractInstallmentComputeView.as_view(), name='contract_installment_compute'),
    url(r'^contract/(?P<contract_id>[\d]+)/service$', service.ServiceCreateView.as_view(), name='service_create'),
    url(r'^contract/(?P<contract_id>[\d]+)/forfeit$', contract.contract_forfeit, name='contract_forfeit'),
    url(r'^contract/(?P<contract_id>[\d]+)/bills$', contract.ContractBillListView.as_view(), name='contract_bills'),
    ###
    url(r'^client/list$', client.ClientListView.as_view(), name='client_list'),
    url(r'^client/json$', client.ClientJson.as_view(), name='client_json'),
    url(r'^client/create$', client.ClientCreateView.as_view(), name='client_create'),
    url(r'^client/update/(?P<client_id>[\d]+)$', client.ClientUpdateView.as_view(), name='client_update'),
    ###
    url(r'^agent/list$', agent.AgentListView.as_view(), name='agent_list'),
    url(r'^agent/json$', agent.AgentJson.as_view(), name='agent_json'),
    url(r'^agent/create$', agent.AgentCreateView.as_view(), name='agent_create'),
    url(r'^agent/update/(?P<agent_id>[\d]+)$', agent.AgentUpdateView.as_view(), name='agent_update'),
    ###
    url(r'^bill/(?P<bill_id>[\d]+)/payment/create$', payment.PaymentCreateView.as_view(), name='payment_create'),
    url(r'^bill/json$', bill.BillJson.as_view(), name='bill_json'),
    url(r'^bill/read/(?P<bill_id>[\d]+)$', bill.BillReadView.as_view(), name='bill_read'),
    url(r'^bill/(?P<bill_id>[\d]+)/status$', bill.bill_update_status, name='bill_status'),
    url(r'^bill/(?P<bill_id>[\d]+)/commission$', bill.BillCommmisionList.as_view(), name='bill_commission'),
    ### payments ###
    url(r'^payment/receipt/create$', receipt.ReceiptCreateView.as_view(), name='receipt_create'),
    url(r'^payment/receipt/(?P<receipt_id>[\d]+)/contract$', receipt.ReceiptContactView.as_view(), name='receipt_contract'),
    url(r'^payment/receipt/(?P<receipt_id>[\d]+)/create$', receipt.ReceiptPaymentView.as_view(), name='receipt_payment'),
    ### commission ###
    url(r'^commission/(?P<commission_id>[\d]+)/read$', commission.CommissionReadView.as_view(), name='commission_read'),
    ### lookups ###
    url(r'^lookup/lot$', lookup.lot_lookup, name='lot_lookup'),
    url(r'^lookup/client$', lookup.client_lookup, name='client_lookup'),
    url(r'^lookup/agent$', lookup.agent_lookup, name='agent_lookup'),
]