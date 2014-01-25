from django.db.models import Sum, Count
from django.views.generic import TemplateView
from contributions.models import Contribution


class IndexView(TemplateView):
    # tell our view which template to use
    template_name = "contributions/index.html"

    def get_context_data(self, **kwargs):
        # grab our context, so we can add to it
        context = super(IndexView, self).get_context_data(**kwargs)
        return context        