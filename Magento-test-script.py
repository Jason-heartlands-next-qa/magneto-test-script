import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import subprocess
import pkgutil

# Check if selenium is installed, if not, install it
if not pkgutil.find_loader("selenium"):
    subprocess.check_call(["pip3", "install", "selenium"])

# Check if webdriver_manager is installed, if not, install it
if not pkgutil.find_loader("webdriver_manager"):
    subprocess.check_call(["pip3", "install", "webdriver_manager"])

def setup_driver():
    ### Initialize and return the webdriver
    return webdriver.Chrome()

def navigate_to_website(driver):
    ### Navigate to the target website
    driver.get("https://magento.softwaretestingboard.com/")
    WebDriverWait(driver, 10)

def select_men_category(driver, wait):
    ### Select the 'Men' category
    men_category_button = wait.until(EC.element_to_be_clickable((By.ID, "ui-id-5")))
    men_category_button.click()

def select_tees_subcategory(driver, wait):
    ### Select the 'Tees' sub-category
    tees_subcategory_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Tees")))
    tees_subcategory_button.click()

def select_color_filter(driver, wait):
    ### Expand the 'Color' section and select the 'Black' option
    color_section = driver.find_element(By.XPATH, "/html/body/div[2]/main/div[3]/div[2]/div/div[2]/div/div[4]/div[1]")
    color_section.click()
    black_color_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[3]/div[2]/div/div[2]/div/div[4]/div[2]/div/div/a[1]/div")))
    black_color_filter.click()

def select_first_product(driver, wait):
    ### Click on the first product after applying the filter
    first_product_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//ol[@class='products list items product-items']/li[1]//a[contains(@class, 'product-item-link')]")))
    first_product_link.click()

def select_product_options(driver, wait):
    ### Select size, color, and quantity for the product
    size_option = wait.until(EC.element_to_be_clickable((By.ID, 'option-label-size-143-item-166')))
    size_option.click()
    color_option = wait.until(EC.element_to_be_clickable((By.ID, 'option-label-color-93-item-49')))
    color_option.click()
    quantity_amount = wait.until(EC.element_to_be_clickable((By.ID, 'qty')))
    quantity_amount.clear()
    quantity_amount.send_keys(random.randint(1,9))

def add_to_cart_and_checkout(driver, wait):
    ### Add the selected product to cart and proceed to checkout
    add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "product-addtocart-button")))
    add_to_cart_button.click()
    time.sleep(2)
    click_cart = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'minicart-wrapper')))    
    click_cart.click()
    checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "top-cart-btn-checkout")))
    checkout_button.click()

def enter_user_details(driver, wait):
    ### Enter user details during the checkout process
    enter_email = wait.until(EC.element_to_be_clickable((By.ID, "customer-email")))
    enter_email.send_keys("sample@test.com")

    enter_first_name = wait.until(EC.element_to_be_clickable((By.NAME, "firstname")))
    enter_first_name.send_keys('Peter')

    enter_last_name = wait.until(EC.element_to_be_clickable((By.NAME, "lastname")))
    enter_last_name.send_keys('Parker')

    enter_street_name = wait.until(EC.element_to_be_clickable((By.NAME, "street[0]")))
    enter_street_name.send_keys('20 Ingram St.')

    enter_city = wait.until(EC.element_to_be_clickable((By.NAME, "city")))
    enter_city.send_keys('Queens')

    enter_state = driver.find_element(By.NAME, "region_id")
    select = Select(enter_state)
    select.select_by_index(43)

    enter_zip = wait.until(EC.element_to_be_clickable((By.NAME, "postcode")))
    enter_zip.send_keys('11375')
    
    enter_phone_number = wait.until(EC.element_to_be_clickable((By.NAME, "telephone")))
    enter_phone_number.send_keys("18008675309")

    choose_shipping_method = wait.until(EC.element_to_be_clickable((By.NAME, 'ko_unique_3')))
    choose_shipping_method.click()

    time.sleep(2)

    next_page = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[2]/div/div[2]/div[4]/ol/li[2]/div/div[3]/form/div[3]/div/button')
    next_page.click()
    
    time.sleep(10)

    place_order = driver.find_element(By.XPATH, '//*[@id="checkout-payment-method-load"]/div/div/div[2]/div[2]/div[4]/div/button') 
    place_order.click()

def verify_purchase_success(driver, wait):
    ### Verify that the purchase was successful
    success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@data-ui-id='page-title-wrapper' and text()='Thank you for your purchase!']")))
    assert success_message.is_displayed(), "Purchase was not successful!"
    if success_message.is_displayed():
        print("Test passed successfully")
    else:
        print("Purchase was not successful!")

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    navigate_to_website(driver)
    select_men_category(driver, wait)
    select_tees_subcategory(driver, wait)
    select_color_filter(driver, wait)
    select_first_product(driver, wait)
    select_product_options(driver, wait)
    add_to_cart_and_checkout(driver, wait)
    enter_user_details(driver, wait)
    verify_purchase_success(driver, wait)
    driver.quit()

if __name__ == "__main__":
    main()
