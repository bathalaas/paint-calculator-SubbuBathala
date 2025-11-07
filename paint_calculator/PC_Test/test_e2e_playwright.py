# test_e2e_playwright.py

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_paint_calculator_ui(page: Page):
    """Verify the user flow of calculating paint requirements."""

    # Go to home page
    page.goto("http://localhost:5000")

    # Verify title or heading
    expect(page.locator("h1, h2, h3")).to_contain_text(["Paint", "Calculator"])

    # Input room details
    page.fill('input[name="length"]', "10")
    page.fill('input[name="width"]', "12")
    page.fill('input[name="height"]', "8")

    # Click calculate (button text or id may differ)
    page.click('button[type="submit"]')

    # Wait for results page
    expect(page).to_have_url(lambda url: "results" in url)

    # Validate result content
    expect(page.locator("body")).to_contain_text("Gallons")
    expect(page.locator("body")).to_contain_text("Total")

    # Optionally, check that total gallons value appears numeric
    text = page.locator("body").inner_text()
    assert any(char.isdigit() for char in text), "No numeric paint result found"


@pytest.mark.e2e
def test_multiple_room_entries(page: Page):
    """(Optional) Extend to multiple room entries if UI supports adding rooms."""

    page.goto("http://localhost:5000")

    # Add first room
    page.fill('input[name="length"]', "12")
    page.fill('input[name="width"]', "10")
    page.fill('input[name="height"]', "9")

    # If there’s an 'Add Room' or similar button, click it
    if page.locator("text=Add Room").is_visible():
        page.click("text=Add Room")

    # Fill another set (example if dynamic forms are used)
    if page.locator('input[name="length-2"]').is_visible():
        page.fill('input[name="length-2"]', "8")
        page.fill('input[name="width-2"]', "10")
        page.fill('input[name="height-2"]', "8")

    page.click('button[type="submit"]')

    expect(page).to_have_url(lambda url: "results" in url)
    expect(page.locator("body")).to_contain_text("Total Gallons")
