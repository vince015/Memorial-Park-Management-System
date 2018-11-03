from django.apps import AppConfig


class ExpenseReportConfig(AppConfig):
    name = 'expense_report'

    def ready(self):
        from expense_report import signals