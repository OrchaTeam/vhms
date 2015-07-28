from  django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _

class VHMSShowroomCategoryView(View):
    """

    """

    template_name = "showroom/category.html"
    title = _("Category")

    def get(self, request):
