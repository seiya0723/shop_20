from .models import CategoryParent


#サイドバーに表示させるコンテキスト
def sidebar(request):

    context             = {}
    context["SIDEBAR"]  = {}

    context["SIDEBAR"]["category_parents"]  = CategoryParent.objects.order_by("-dt")

    return context
