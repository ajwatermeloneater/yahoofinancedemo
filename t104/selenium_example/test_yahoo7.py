from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestYahooPytest:

    def setup_method(self):
        print("Test Start")
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get("https://finance.yahoo.com/")

    def teardown_method(self):
        self.driver.quit()
        print("Test End")

    def reject_cookies(self):
        # Wait for the scroll button to be clickable and then click it
        scroll_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "scroll-down-btn"))
        )
        scroll_button.click()
        print("Scroll button clicked.")

        # Wait for the reject button to be clickable and then click it
        reject_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "reject"))
        )
        reject_button.click()
        print("Cookies rejected successfully.")

    def test_reject_cookies_and_navigate(self):
        # Reuse reject_cookies method to reject cookies
        self.reject_cookies()
        print("Cookies rejected on the lander page.")

    def test_AAPL_stock(self):
        # Reuse reject_cookies method before performing stock search
        self.reject_cookies()

        search_box = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Quote Lookup']"))
        )

        search_box.send_keys("AAPL")

        search_box.send_keys(Keys.RETURN)
        price_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-testid='qsp-post-price']"))
        )

        price = price_element.text
        assert price != "", "Stock price is empty"
        print("AAPL live stock price:", price)

        print("now lets compare between goog and AAPL %change in the last 24 hours")

    def test_compare_AAPL_with_GOOG_change(self):
           # Reuse reject_cookies method before performing stock search
        self.reject_cookies()

        # Search for AAPL and get its 24h change value
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Quote Lookup']"))
        )
        search_box.send_keys("AAPL")
        search_box.send_keys(Keys.RETURN)

        # Wait for the 24h change element to be visible (AAPL)
        change_element_AAPL = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-testid='qsp-post-price-change-percent']"))  # Adjust the selector based on the actual element on Yahoo Finance
        )
        change_AAPL = change_element_AAPL.text
        print(f"AAPL 24h change: {change_AAPL}")

        # Now, search for GOOG and get its 24h change value
        search_box = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Quote Lookup']"))
        )
        search_box.clear()  # Clear the search box
        search_box.send_keys("GOOG")
        search_box.send_keys(Keys.RETURN)

        # Wait for the 24h change element to be visible (GOOG)
        change_element_GOOG = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-testid='qsp-post-price-change-percent']"))  # Adjust the selector based on the actual element on Yahoo Finance
        )
        change_GOOG = change_element_GOOG.text
        print(f"GOOG 24h change: {change_GOOG}")

        # Compare the two stock changes
        print(f"Comparing AAPL 24h change: {change_AAPL} with GOOG 24h change: {change_GOOG}")
        change_AAPL_value = change_AAPL.replace('(', '').replace(')', '').replace('%', '').replace(',', '').strip()
        change_GOOG_value = change_GOOG.replace('(', '').replace(')', '').replace('%', '').replace(',', '').strip()

           # Convert to float for proper numerical comparison
        change_AAPL_value = float(change_AAPL_value)
        change_GOOG_value = float(change_GOOG_value)

           # Compare the two stock changes
        print(f"Comparing AAPL 24h change: {change_AAPL_value}% with GOOG 24h change: {change_GOOG_value}%")

        if change_AAPL_value > change_GOOG_value:
           print("AAPL had a higher change than GOOG.")
        elif change_AAPL_value < change_GOOG_value:
           print("GOOG had a higher change than AAPL.")
        else:
           print("AAPL and GOOG had the same change.")
        print("test over")

