import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from todoapp.models import TodoModel
from todoapp.views import add_todo_item, edit_todo_item, partial_rendering


@pytest.mark.django_db
def test_full_page_empty_table(htmx_rf):
    request = htmx_rf.get(reverse("list-todo-items"))
    response = partial_rendering(request)
    soup = BeautifulSoup(response.content, "html.parser")
    main_tag = soup.find(id="main")
    assert main_tag and main_tag.name == "main"
    td_tag = main_tag.select_one("#table-section table tbody tr td")
    expected = soup.new_tag(name="em", string="No todo items on this page.")
    assert td_tag.contents == [expected]


@pytest.mark.django_db
@pytest.mark.parametrize("partial", [False, True])
def test_table_section_one_entry(htmx_rf, partial):
    todo_item = TodoModel.objects.create(
        title="First Todo Item",
    )
    request = htmx_rf.get(reverse("list-todo-items"), hx_target="#table-section" if partial else None)
    response = partial_rendering(request)
    soup = BeautifulSoup(response.content, "html.parser")
    main_tag = soup.find(id="main")
    if partial:
        assert main_tag is None
    else:
        assert main_tag and main_tag.name == "main"
    td_tags = soup.select("#table-section table tbody tr td")
    assert len(td_tags) == 5
    assert td_tags[0].text == str(todo_item.id)
    assert td_tags[1].text == todo_item.title
    assert td_tags[2].text == todo_item.created_at.strftime("%b. %-d, %Y, %-H:%M")
    expected = soup.new_tag(
        name="a",
        attrs={"hx-put": f"/todo-item/{todo_item.id}", "hx-swap": "outerHTML", "hx-target": "#table-section"},
        string="✔️",
    )
    assert td_tags[3].contents == [expected]
    expected = soup.new_tag(
        name="a",
        attrs={"hx-delete": f"/todo-item/{todo_item.id}", "hx-swap": "outerHTML", "hx-target": "#table-section"},
        string="❌",
    )
    assert td_tags[4].contents == [expected]


@pytest.mark.django_db
def test_add_todo_item(htmx_rf):
    request = htmx_rf.post(
        reverse("add-todo-item"),
        hx_target="#table-section",
        data={"title": "New Todo Item"},
    )
    response = add_todo_item(request)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="main") is None
    td_tags = soup.select("#table-section table tbody tr td")
    assert len(td_tags) == 5
    todo_item = TodoModel.objects.get(id=td_tags[0].text)
    expected = soup.new_tag(name="b", string=todo_item.title)
    assert td_tags[1].contents == [expected]


@pytest.mark.django_db
def test_complete_todo_item(htmx_rf):
    todo_item = TodoModel.objects.create(
        title="Current Todo Item",
    )
    request = htmx_rf.put(
        reverse("edit-todo-item", args=[todo_item.id]),
        hx_target="#table-section",
    )
    response = edit_todo_item(request, todo_item.id)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="main") is None
    td_tags = soup.select("#table-section table tbody tr td")
    assert len(td_tags) == 5
    assert td_tags[0].text == str(todo_item.id)
    expected = soup.new_tag(name="s", string=todo_item.title)
    assert td_tags[1].contents == [expected]
    assert td_tags[2].text == todo_item.created_at.strftime("%b. %-d, %Y, %-H:%M")


@pytest.mark.django_db
def test_delete_todo_item(htmx_rf):
    todo_item = TodoModel.objects.create(
        title="Temporary Todo Item",
    )
    request = htmx_rf.delete(
        reverse("edit-todo-item", args=[todo_item.id]),
        hx_target="#table-section",
    )
    response = edit_todo_item(request, todo_item.id)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="main") is None
    td_tag = soup.select_one("#table-section table tbody tr td")
    expected = soup.new_tag(name="em", string="No todo items on this page.")
    assert td_tag.contents == [expected]
