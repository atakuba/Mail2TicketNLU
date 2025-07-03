from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.create_ticket_page_locators import CreateTicketPageLocators
from automation.utils.driver_setup import get_driver
from selenium.common.exceptions import TimeoutException
import time
from pathlib import Path
import pandas as pd
import os


@given("the automation is started and browser is open")
def step_start_browser(context):
    context.driver = get_driver()  # Assuming get_driver() is defined elsewhere
    context.driver.get("https://ellucian.service-now.com/navpage.do")

@when("the tech user logs in manually")
def step_wait_for_manual_login(context):
    try:
        WebDriverWait(context.driver, 580).until(
            lambda d: CreateTicketPageLocators.get_favorites_button(context)
        )
    except TimeoutException:
        raise Exception("❌ 'Favorites' button not found after manual login. Login may not be completed.")
    
@given("the Excel file is loaded into context")
def step_load_excel_file(context):
    excel_folder = Path("excels")
    latest_file = max(excel_folder.glob("summarized_output_*.xlsx"), key=os.path.getmtime)

    print(f"📂 Loading latest file: {latest_file}")
    df = pd.read_excel(latest_file)
    context.df = df
    context.record_index = 0
    
@when("the user navigates to the favorites page")
def step_navigate_to_favorites(context):

    time.sleep(7) # Wait for 5 minutes to allow manual review if needed
    # Get the actual WebElement from Shadow DOM
    favorites_button = CreateTicketPageLocators.get_favorites_button(context)
    
    if favorites_button:
        favorites_button.click()
    else:
        raise Exception("❌ Could not find Favorites button to click.")

    WebDriverWait(context.driver, 20).until(
        EC.element_to_be_clickable(CreateTicketPageLocators.get_case_my_cases_item(context))
    ).click()
    time.sleep(3)

@then("each record from the Excel file is submitted as a new ticket")
def step_submit_each_ticket(context):
    while context.record_index < len(context.df):
        row = context.df.iloc[context.record_index]
        context.record_index += 1

        print(f"🚀 Processing ticket {context.record_index} of {len(context.df)}")

        # Click New button
        CreateTicketPageLocators.page_reset_focus(context)
        CreateTicketPageLocators.click_on_tab(context)
        CreateTicketPageLocators.click_on_enter_key(context)
        time.sleep(2)

        # Get fields from the Excel row
        assigned_to = row.get("User Email", "akubanychbek@nl.edu")
        assignment_group = "National-Louis - Desktop Services"
        business_service = row.get("Business Service", "Help Desk")
        category = row.get("Category", "General Inquiry")
        short_description = row.get("short_description", "Missing short desc")
        description = row.get("description", "Missing description")
        resolution_notes = row.get("Body Summary", "Auto-generated resolution notes")
        state = "Solved - Fixed by Support/Guidance provided"

        # Fill ticket form using tab and key navigation
        time.sleep(1)
        CreateTicketPageLocators.click_on_tab(context, tab_count=2, delay=0.5).send_keys(assigned_to)
        time.sleep(2)
        CreateTicketPageLocators.click_on_enter_key(context)
        time.sleep(1)

        CreateTicketPageLocators.click_on_tab(context, tab_count=2, delay=0.5).send_keys("N/A")  # This is user's best contact number
        time.sleep(1)
        CreateTicketPageLocators.click_on_tab(context, tab_count=2, delay=0.5).send_keys("Gage")
        time.sleep(1)
        CreateTicketPageLocators.click_on_tab(context, tab_count=2, delay=0.5).send_keys(assignment_group)
        time.sleep(1)

        CreateTicketPageLocators.click_on_tab(context, tab_count=5, delay=0.5)
        time.sleep(1)
        CreateTicketPageLocators.click_arrow_button(context, "down", 1)
        time.sleep(1)
        CreateTicketPageLocators.click_on_key(context, "s")
        time.sleep(1)
        CreateTicketPageLocators.click_on_enter_key(context)
        time.sleep(1)

        CreateTicketPageLocators.click_on_tab(context, tab_count=2, delay=0.1).send_keys(business_service)
        time.sleep(2)
        CreateTicketPageLocators.click_on_enter_key(context)
        time.sleep(1)

        CreateTicketPageLocators.click_on_tab(context, tab_count=1, delay=0.1).send_keys(category)
        time.sleep(1)
        CreateTicketPageLocators.click_on_tab(context, tab_count=9, delay=0.1).send_keys(short_description)
        time.sleep(1)
        CreateTicketPageLocators.click_on_tab(context, tab_count=1, delay=0.1).send_keys(description)
        time.sleep(1)

        CreateTicketPageLocators.click_on_tab(context, tab_count=1, delay=0.1)
        time.sleep(5)
        CreateTicketPageLocators.click_on_enter_key(context)
        time.sleep(1)
        CreateTicketPageLocators.click_on_tab(context, tab_count=1, delay=0.1)
        time.sleep(1)
        CreateTicketPageLocators.click_arrow_button(context, "right", 1)
        time.sleep(1)

        CreateTicketPageLocators.click_on_tab(context, tab_count=4, delay=0.1).send_keys(state)
        time.sleep(1)
        CreateTicketPageLocators.click_on_enter_key(context)
        time.sleep(1)

        CreateTicketPageLocators.click_on_tab(context, tab_count=5, delay=0.1).send_keys(resolution_notes)
        time.sleep(1)
        CreateTicketPageLocators.click_on_tab(context, tab_count=1, delay=0.1)
        time.sleep(1)

        # Submit the form
        # CreateTicketPageLocators.click_on_enter_key(context)

        print(f"✅ Ticket {context.record_index} submitted.")
        time.sleep(4000)