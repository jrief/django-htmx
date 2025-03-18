import pytest
import time
from playwright.sync_api import expect
from django.urls import reverse

from todoapp.models import TodoModel


def test_full_page_empty_table(live_server, page):
    page.goto(f'{live_server.url}{reverse("list-todo-items")}')
    main_locator = page.locator('main')
    expect(main_locator).to_be_visible()
    td_locator = main_locator.locator("#table-section table tbody tr td")
    expect(td_locator).to_be_visible()
    expect(td_locator).to_have_attribute('colspan', '5')
    expect(td_locator).to_have_text('No todo items on this page.')
    page.screenshot(path='test_full_page_empty_table.png')


@pytest.mark.django_db
def test_table_section_one_entry(live_server, page):
    todo_item = TodoModel.objects.create(
        title="First Todo Item",
    )
    page.goto(f'{live_server.url}{reverse("list-todo-items")}')
    td_locator = page.locator("#table-section table tbody tr td")
    expect(td_locator).to_have_count(5)
    expect(td_locator.nth(0)).to_have_text(str(todo_item.id))
    expect(td_locator.nth(1)).to_have_text(todo_item.title)
    expect(td_locator.nth(2)).to_have_text(todo_item.created_at.strftime("%b. %-d, %Y, %-H:%M"))
    expect(td_locator.nth(3).locator('a')).to_have_text('✔️')
    expect(td_locator.nth(4).locator('a')).to_have_text('❌')
    page.screenshot(path='test_table_section_one_entry.png')


def test_add_todo_item(live_server, page):
    page.goto(f'{live_server.url}{reverse("list-todo-items")}')
    input_locator = page.locator('main form input[name="title"]')
    expect(input_locator).to_be_visible()
    input_locator.fill("New Todo Item")
    add_button_locator = input_locator.locator("+ button")
    expect(add_button_locator).to_have_text("Add")
    add_button_locator.click()
    td_locator = page.locator("#table-section table tbody tr td")
    expect(td_locator).to_have_count(5)
    expect(td_locator.nth(1)).to_have_text("New Todo Item")


@pytest.mark.django_db
def test_complete_todo_item(live_server, page):
    todo_item = TodoModel.objects.create(
        title="Current Todo Item",
    )
    assert todo_item.completed is False
    page.goto(f'{live_server.url}{reverse("list-todo-items")}')
    td_locator = page.locator("main #table-section table tbody tr td")
    td_locator.nth(3).locator('a').click()
    todo_item.refresh_from_db()
    assert todo_item.completed is True


@pytest.mark.django_db
def test_delete_todo_item(live_server, page):
    TodoModel.objects.create(
        title="Temporary Todo Item",
    )
    assert TodoModel.objects.count() == 1
    page.goto(f'{live_server.url}{reverse("list-todo-items")}')
    td_locator = page.locator("main #table-section table tbody tr td")
    td_locator.nth(4).locator('a').click()
    time.sleep(0.2)  # test sometimes fails, because the server app didn't process the delete request
    assert TodoModel.objects.count() == 0
