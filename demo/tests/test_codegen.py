import pytest
from playwright.sync_api import Page, expect


@pytest.mark.django_db
def test_example(page: Page) -> None:
    page.goto("http://localhost:8001/")
    page.get_by_role("textbox", name="Next todo item").click()
    page.get_by_role("textbox", name="Next todo item").fill("Do something")
    page.get_by_role("button", name="Add").click()
    page.screenshot(path="test1.png")
    page.get_by_text("▢").first.click()
    page.screenshot(path="test2.png")
    expect(page.locator("tbody")).to_contain_text("Do something")
