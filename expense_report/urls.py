from django.conf.urls import url
from expense_report import views

urlpatterns = [
    url(r'^expense/list$', views.ExpenseListView.as_view(), name='expense_list'),
    url(r'^expense/json$', views.ExpenseJson.as_view(), name='expense_json'),
    url(r'^expense/create$', views.ExpenseCreateView.as_view(), name='expense_create'),
    url(r'^expense/update/(?P<expense_id>[\d]+)$', views.ExpenseUpdateView.as_view(), name='expense_update'),
    url(r'^pettycash/list$', views.PettyCashListView.as_view(), name='pettycash_list'),
    url(r'^pettycash/create$', views.PettyCashCreateView.as_view(), name='pettycash_create')
]