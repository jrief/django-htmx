import pytest
from playwright.sync_api import Page, expect


@pytest.mark.django_db
def test_example(page: Page) -> None:
    page.goto("http://localhost:8001/")
    page.get_by_role("textbox", name="Next todo item").click()
    page.get_by_role("textbox", name="Next todo item").fill("First Todo Item")
    page.get_by_role("button", name="Add").click()
    expect(page.locator("b")).to_contain_text("First Todo Item")
