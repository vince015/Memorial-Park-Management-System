from django.conf.urls import url
from expense_report import views

urlpatterns = [
    url(r'^expense/list$', views.ExpenseListView.as_view(), name='expense_list'),
    url(r'^expense/create$', views.ExpenseCreateView.as_view(), name='expense_create'),
    url(r'^expense/update/(?P<expense_id>[\d]+)$', views.ExpenseUpdateView.as_view(), name='expense_update'),
    ### json ###
    url(r'^json/expense$', views.ExpenseJson.as_view(), name='expense_json'),
]