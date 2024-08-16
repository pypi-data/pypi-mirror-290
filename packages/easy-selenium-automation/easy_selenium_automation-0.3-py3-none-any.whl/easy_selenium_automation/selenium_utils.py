from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait until the element is present in the DOM by XPath
def wait_element_xpath(driver, xpath, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except:
        return False

# Wait until the element is present in the DOM by ID
def wait_element_id(driver, element_id, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        return element
    except:
        return False

# Wait until the element is present in the DOM by Name
def wait_element_name(driver, name, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.NAME, name))
        )
        return element
    except:
        return False

# Wait until the element is present in the DOM by Class Name
def wait_element_class(driver, class_name, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return element
    except:
        return False

# Wait until the element is present in the DOM by Tag Name
def wait_element_tag(driver, tag_name, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, tag_name))
        )
        return element
    except:
        return False

# Wait until the element is present in the DOM by CSS Selector
def wait_element_css(driver, css_selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return element
    except:
        return False

# Wait until the element is present in the DOM by Link Text
def wait_element_link_text(driver, link_text, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.LINK_TEXT, link_text))
        )
        return element
    except:
        return False

# Wait and click on an element identified by XPath
def click_element_xpath(driver, xpath, timeout=10):
    element = wait_element_xpath(driver, xpath, timeout)
    if element:
        element.click()
        return True
    return False

# Wait and click on an element identified by CSS Selector
def click_element_css(driver, css_selector, timeout=10):
    element = wait_element_css(driver, css_selector, timeout)
    if element:
        element.click()
        return True
    return False

# Wait and fill a text field identified by XPath
def fill_field_xpath(driver, xpath, text, timeout=10):
    element = wait_element_xpath(driver, xpath, timeout)
    if element:
        element.send_keys(text)
        return True
    return False

# Wait and fill a text field identified by Name
def fill_field_name(driver, name, text, timeout=10):
    element = wait_element_name(driver, name, timeout)
    if element:
        element.send_keys(text)
        return True
    return False

# Check if an element is present in the DOM by XPath
def is_element_present_xpath(driver, xpath, timeout=10):
    return wait_element_xpath(driver, xpath, timeout) is not False

# Check if an element is present in the DOM by CSS Selector
def is_element_present_css(driver, css_selector, timeout=10):
    return wait_element_css(driver, css_selector, timeout) is not False

# Check if an element is present in the DOM by ID
def is_element_present_id(driver, element_id, timeout=10):
    return wait_element_id(driver, element_id, timeout) is not False

# Check if an element is present in the DOM by Name
def is_element_present_name(driver, name, timeout=10):
    return wait_element_name(driver, name, timeout) is not False

# Check if an element is present in the DOM by Class Name
def is_element_present_class(driver, class_name, timeout=10):
    return wait_element_class(driver, class_name, timeout) is not False
