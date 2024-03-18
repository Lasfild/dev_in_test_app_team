import pytest
import logging
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(filename='test.log', level=logging.INFO,filemode='w')
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def driver_setup():
    desired_caps = {
        "platformName": "Android",
        "platformVersion": "14.0",
        "deviceName": "Android",
        "app": "/Users/denys/AppData/Local/Android/Sdk/platforms/android-34/data/ajax-security-system-3-0.apk",
        "automationName": "UIAutomator2",
        "appPackage": "com.ajaxsystems",
        "appActivity": "com.ajaxsystems.ui.activity.LauncherActivity"
    }
    capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723/wd/hub', options=capabilities_options)
    driver.implicitly_wait(30)
    yield driver
    driver.quit()


def test_allow_notifications(driver_setup):
    logger.info("Agreeing with notifications (* ^ ω ^)")
    driver_setup.find_element(By.ID, 'com.android.permissioncontroller:id/permission_allow_button').click()


def test_login_button(driver_setup):
    logger.info("Clicking on login button with credentials <(￣︶￣)>")
    driver_setup.find_element(By.XPATH, '//android.widget.TextView[@bounds="[480,2076][600,2137]"]').click()


@pytest.mark.parametrize("username, password", [
    ("incorrect_username", "qa_automation_password"),  # Wrong login
    ("qa.ajax.app.automation@gmail.com", "incorrect_password"),  # Wrong password
    ("incorrect_username", "incorrect_password")  # Wrong all
])
def test_login_with_invalid_credentials(driver_setup, username, password):
    logger.info(f"Attempting login with invalid credentials: username={username}, password={password}")
    driver_setup.find_element(By.XPATH, '//android.widget.EditText[@bounds="[0,273][1080,446]"]').send_keys(username)
    driver_setup.find_element(By.XPATH, '//android.widget.EditText[@bounds="[0,446][1080,619]"]').send_keys(password)
    driver_setup.find_element(By.XPATH, '//android.widget.TextView[@bounds="[480,2076][600,2137]"]').click()

    # Assert that there's an error message or login is not successful with invalid credentials ┐(シ)┌
    assert "error_message_element" in driver_setup.page_source, "Expected error message not found for invalid credentials"


def test_login_with_valid_credentials(driver_setup):
    logger.info("Logging in with valid credentials")
    username = "qa.ajax.app.automation@gmail.com"
    password = "qa_automation_password"

    driver_setup.find_element(By.XPATH, '//android.widget.EditText[@bounds="[0,273][1080,446]"]').send_keys(username)
    driver_setup.find_element(By.XPATH, '//android.widget.EditText[@bounds="[0,446][1080,619]"]').send_keys(password)
    driver_setup.find_element(By.XPATH, '//android.widget.TextView[@bounds="[480,2076][600,2137]"]').click()

    # Assert that login is successful by checking for some element after successful login ╮(￣～￣)╭
    assert "some_element_after_login" in driver_setup.page_source, "Login failed with valid credentials"


def test_press_login(driver_setup):
    logger.info("Pressing Log in ╰(▔∀▔)╯")
    driver_setup.find_element(By.XPATH, '//android.widget.TextView[@bounds="[480,2223][600,2284]"]').click()


def test_allow_location_tracking(driver_setup):
    logger.info("Allowing location tracking")
    # This app collects, bla bla bla... (╯_╰)
    driver_setup.find_element(By.XPATH, '//android.widget.TextView[@bounds="[452,2223][628,2284]"]').click()
    # Allow app to track ur location (or not) (←_←)
    driver_setup.find_element(By.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()


def test_open_sidebar(driver_setup):
    driver_setup.find_element(By.ID, 'com.ajaxsystems:id/menuDrawer').click()

    # Wait for the sidebar to be visible ＼(≧▽≦)／
    sidebar = WebDriverWait(driver_setup, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//xpath_of_sidebar_element')))

    # Now, you can find and assert properties of elements within the sidebar, this is one of them (ᓀ ᓀ)
    sidebar_elements = sidebar.find_elements(By.XPATH, '//androidx.compose.ui.platform.ComposeView[@resource-id="com.ajaxsystems:id/compose_menu"]/android.view.View/android.view.View/android.widget.ScrollView[1]')

    # Assert that the sidebar contains specific elements ▓▒░(°◡°)░▒▓
    assert len(sidebar_elements) > 0, "Sidebar is empty or not visible"
