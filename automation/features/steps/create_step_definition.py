from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.create_ticket_page_locators import CreateTicketPageLocators
from automation.utils.driver_setup import get_driver
from selenium.common.exceptions import TimeoutException
import time


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
    
    
@when("the user navigates to the favorites page")
def step_navigate_to_favorites(context):
    print("*********** Navigating to Favorites ***********")

    time.sleep(7) # Wait for 5 minutes to allow manual review if needed
    # Get the actual WebElement from Shadow DOM
    favorites_button = CreateTicketPageLocators.get_favorites_button(context)
    
    if favorites_button:
        favorites_button.click()
    else:
        raise Exception("❌ Could not find Favorites button to click.")

    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable(CreateTicketPageLocators.get_case_my_cases_item(context))
    ).click()


@when("clicks on \"new\" button")
def step_click_new_button(context):

    time.sleep(3) # Wait for 5 minutes to allow manual review if needed
    print("*********** Clicking on New Button ***********")
    CreateTicketPageLocators.reset_focus_to_start_and_tab(context)
    time.sleep(20)

@then("enters all the input information and clicks on submit button")
def step_fill_form_and_submit(context):
    # time.sleep(300) # Wait for 5 minutes to allow manual review if needed
    d = context.driver

    CreateTicketPageLocators.reset_focus_to_start_and_tab(context, tab_count=2, delay=0.1).send_keys("John Doe")
    CreateTicketPageLocators.reset_focus_to_start_and_tab(context, tab_count=4, delay=0.1).send_keys("312-555-7890")
    CreateTicketPageLocators.reset_focus_to_start_and_tab(context, tab_count=5, delay=0.1).send_keys("National-Louis - Desktop Services")
    CreateTicketPageLocators.reset_focus_to_start_and_tab(context, tab_count=7, delay=0.1).send_keys("Cannot access student portal")
    CreateTicketPageLocators.reset_focus_to_start_and_tab(context, tab_count=9, delay=0.1).send_keys("Cannot access student portal")
    CreateTicketPageLocators.reset_focus_to_start_and_tab(context, tab_count=16, delay=0.1).send_keys("Help Desk")
    CreateTicketPageLocators.reset_focus_to_start_and_tab(context, tab_count=2, delay=0.1).send_keys("User reported login issue with portal. Issue resolved after password reset")
    # d.find_element(*CreateTicketPageLocators.CONTACT_INPUT_XPATH).
    # d.find_element(*CreateTicketPageLocators.BEST_CONTACT_NUMBER_INPUT).send_keys("312-555-7890")
    # d.find_element(*CreateTicketPageLocators.LOCATION_INPUT).send_keys("Chicago Office")
    # d.find_element(*CreateTicketPageLocators.ASSIGNMENT_GROUP_INPUT).send_keys("National-Louis - Desktop Services")
    # d.find_element(*CreateTicketPageLocators.SHORT_DESCRIPTION_INPUT).send_keys("Cannot access student portal")
    # d.find_element(*CreateTicketPageLocators.DESCRIPTION_TEXTAREA).send_keys("User reported login issue with portal. Issue resolved after password reset.")
    # d.find_element(*CreateTicketPageLocators.STATE_SELECT).click()
    # d.find_element(*CreateTicketPageLocators.STATE_OPTION_SOLUTION_PROPOSED).click()
    # d.find_element(*CreateTicketPageLocators.BUSINESS_SERVICE_INPUT).send_keys("Help Desk")
    # d.find_element(*CreateTicketPageLocators.CATEGORY_SELECT).click()
    # d.find_element(*CreateTicketPageLocators.CATEGORY_OPTION_DYNAMIC("Drop Call")).click()

    # d.find_element(*CreateTicketPageLocators.RESOLUTION_INFORMATION_TAB).click()
    # d.find_element(*CreateTicketPageLocators.RESOLUTION_CODE_SELECT).click()
    # d.find_element(*CreateTicketPageLocators.RESOLUTION_CODE_OPTION_FIXED_BY_SUPPORT).click()
    # d.find_element(*CreateTicketPageLocators.CLOSE_NOTES_TEXTAREA).send_keys("Issue resolved by resetting password. User confirmed success.")
    time.sleep(300) # Wait for 5 minutes to allow manual review if needed
    # d.find_element(*FavoritesPage.SUBMIT_BUTTON).click()
