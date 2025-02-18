from __future__ import annotations

from django.core.paginator import Paginator
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from django_htmx.middleware import HtmxDetails

from todoapp.forms import TodoForm
from todoapp.models import TodoModel


# Typing pattern recommended by django-stubs:
# https://github.com/typeddjango/django-stubs#how-can-i-create-a-httprequest-thats-guaranteed-to-have-an-authenticated-user
class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


@require_GET
def favicon(request: HtmxHttpRequest) -> HttpResponse:
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            + '<text y=".9em" font-size="90">✅</text>'
            + "</svg>"
        ),
        content_type="image/svg+xml",
    )


def partial_rendering(request: HtmxHttpRequest) -> HttpResponse:
    # Standard Django pagination
    todos = TodoModel.objects.all().order_by("-created_at")
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=todos, per_page=10).get_page(page_num)

    # The htmx magic - render just the `#table-section` partial for htmx
    # requests, allowing us to skip rendering the unchanging parts of the
    # template.
    template_name = "todoapp.html"
    if request.htmx:
        template_name += "#table-section"

    return render(
        request,
        template_name,
        {
            "page": page,
        },
    )


@require_POST
def add_todo_item(request: HtmxHttpRequest) -> HttpResponse:
    form = TodoForm(request.POST)
    if form.is_valid():
        form.save()
    return partial_rendering(request)


def edit_todo_item(request: HtmxHttpRequest, id: int) -> HttpResponse:
    return partial_rendering(request)
