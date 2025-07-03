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
    def page_reset_focus(context):
        driver = context.driver
        driver.refresh()
        time.sleep(3)
        driver.execute_script("""
            if (document.activeElement) document.activeElement.blur();
            const tabbables = document.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            if (tabbables.length > 0) tabbables[0].focus();
        """)

    @staticmethod
    def click_on_key(context, key: str):
        driver = context.driver
        ActionChains(driver).send_keys(key).perform()

    @staticmethod
    def click_on_enter_key(context):
        driver = context.driver
        ActionChains(driver).send_keys(Keys.ENTER).perform()

    @staticmethod
    def click_arrow_button(context, direction: str, arrow_count: int):
        driver = context.driver
        actions = ActionChains(driver)
        # active = driver.switch_to.active_element
        # active.click()
        # time.sleep(20.2)

        # try:
        #     active_element = driver.switch_to.active_element
        #     active_element.click()
        #     time.sleep(0.2)
        # except Exception as e:
        #     print(f"⚠️ Could not click active element: {e}")

        for _ in range(arrow_count):
            time.sleep(1.1)
            if direction.lower() == "down":
                actions.send_keys(Keys.ARROW_DOWN).perform()
            elif direction.lower() == "up":
                actions.send_keys(Keys.UP).perform()
            elif direction.lower() == "right":
                actions.send_keys(Keys.RIGHT).perform()
            elif direction.lower() == "left":
                actions.send_keys(Keys.LEFT).perform()
            else:
                raise ValueError(f"Invalid direction: {direction}. Use 'up', 'down', 'right' or 'left'!")
            
    @staticmethod
    def click_on_tab(context, tab_count=24, delay=0.1):
        driver = context.driver

        ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(0.2)

        # Tab exactly from the top — total of tab_count times
        for _ in range(tab_count - 1):  # Already tabbed once above
            ActionChains(driver).send_keys(Keys.TAB).perform()
            print("🔄 TABBED")
            time.sleep(delay)
        return driver.switch_to.active_element
