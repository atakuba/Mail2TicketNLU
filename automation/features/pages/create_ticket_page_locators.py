from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class CreateTicketPageLocators:
    
    @staticmethod
    def get_favorites_button(context, timeout=30):
        try:
            return WebDriverWait(context.driver, timeout).until(
                lambda d: d.execute_script("""
                    const host = document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010");
                    if (!host) return null;
                    const shadow1 = host.shadowRoot;
                    const layout = shadow1?.querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout")?.shadowRoot;
                    const header = layout?.querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header")?.shadowRoot;
                    return header?.querySelector("#\\\\31 b682fe1c3133010cbd77096e940dd18") || null;
                """)
            )
        except TimeoutException:
            raise Exception("❌ 'Favorites' button not found in Shadow DOM within timeout.")


    # MY_CASES_OPTION = (By.XPATH, "//span[@class='label' and normalize-space(text())='Case - My Cases']")
    @staticmethod
    def get_case_my_cases_item(context, timeout=30):
        try:
            return WebDriverWait(context.driver, timeout).until(
                lambda d: d.execute_script("""
                    const host = document.querySelector("body > macroponent-f51912f4c700201072b211d4d8c26010");
                    if (!host) return null;

                    const shadow1 = host.shadowRoot;
                    const layout = shadow1?.querySelector("div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout")?.shadowRoot;
                    const header = layout?.querySelector("div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header")?.shadowRoot;
                    const menu = header?.querySelector("nav > div > div.starting-header-zone > sn-polaris-menu:nth-child(3)")?.shadowRoot;
                    const nav = menu?.querySelector("nav > div.sn-polaris-nav.\\\\31 b682fe1c3133010cbd77096e940dd18.can-animate > div.sn-tree-menu.sn-polaris-nav-content > div > div > sn-collapsible-list:nth-child(3)")?.shadowRoot;
                    return nav?.querySelector("#\\\\32 a1d5f451bb1ee1018fea933604bcbc2 > span > span") || null;
                """)
            )
        except TimeoutException:
            raise Exception("❌ 'Case - My Cases' item not found in Shadow DOM within timeout.")

    @staticmethod
    def reset_focus_to_start_and_tab(context, tab_count=24, delay=0.1):
        driver = context.driver

        # Refresh and wait
        driver.refresh()
        time.sleep(3)
        driver.execute_script("""
            if (document.activeElement) document.activeElement.blur();
            const tabbables = document.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            if (tabbables.length > 0) tabbables[0].focus();
        """)


        # Blur current focus if needed
        # driver.execute_script("if (document.activeElement) document.activeElement.blur();")
        # time.sleep(0.5)

        ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(0.2)

        # Tab exactly from the top — total of tab_count times
        for _ in range(tab_count - 1):  # Already tabbed once above
            ActionChains(driver).send_keys(Keys.TAB).perform()
            print("🔄 TABBED")
            time.sleep(delay)


        time.sleep(4)  # Wait a bit before sending ENTER
        # driver.execute_script("document.activeElement.click();")
        ActionChains(driver).send_keys(Keys.ENTER).perform()

        print(f"✅ Focus reset. TABBED {tab_count} times + ENTER.")



    CONTACT_INPUT_XPATH = (By.XPATH, "//input[contains(@name, 'sn_customerservice_case.contact')]")
    BEST_CONTACT_NUMBER_INPUT = (By.XPATH, "//input[@id='sn_customerservice_case.u_best_contact_number']")
    LOCATION_INPUT = (By.XPATH, "//input[@id='sys_display.sn_customerservice_case.location']")
    ASSIGNMENT_GROUP_INPUT = (By.XPATH, "//input[@id='sys_display.sn_customerservice_case.assignment_group']")
    SHORT_DESCRIPTION_INPUT = (By.XPATH, "//input[@id='sn_customerservice_case.short_description']")
    DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[@id='sn_customerservice_case.description']")
    STATE_SELECT = (By.XPATH, "//select[@id='sn_customerservice_case.state']")
    STATE_OPTION_SOLUTION_PROPOSED = (By.XPATH, "//select[@id='sn_customerservice_case.state']/option[@value='6']")
    BUSINESS_SERVICE_INPUT = (By.XPATH, "//input[@id='sys_display.sn_customerservice_case.u_business_service']")
    CATEGORY_SELECT = (By.XPATH, "//select[@id='sn_customerservice_case.category']")
    CATEGORY_OPTION_DYNAMIC = lambda value: (By.XPATH, f"//select[@id='sn_customerservice_case.category']/option[@value='{value}']")

    RESOLUTION_INFORMATION_TAB = (By.XPATH, "//span[@class='tab_caption_text' and normalize-space(text())='Resolution Information']")
    RESOLUTION_CODE_SELECT = (By.XPATH, "//select[@id='sn_customerservice_case.resolution_code']")
    RESOLUTION_CODE_OPTION_FIXED_BY_SUPPORT = (By.XPATH, "//select[@id='sn_customerservice_case.resolution_code']/option[@value='1']")
    CLOSE_NOTES_TEXTAREA = (By.XPATH, "//textarea[@id='sn_customerservice_case.close_notes']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@id='sysverb_insert_bottom']")

