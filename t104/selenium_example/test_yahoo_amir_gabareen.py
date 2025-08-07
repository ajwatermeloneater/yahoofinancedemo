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

        # Wait for the price element to be visible (after performing the search)
        price_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-testid='qsp-price']"))
        )

        # Get the price text from the element
        price = price_element.text.strip()

        # Assert that the price is not empty
        assert price != "", "Stock price is empty"

        # Assert that the price is a valid number and greater than 0
        assert float(price.replace(",", "")) > 0, f"Stock price is not a valid number: {price}"

        print(f"AAPL live stock price after search: {price}")

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
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-testid='qsp-price-change-percent']"))
        )
        change_AAPL = change_element_AAPL.text.strip()
        print(f"AAPL 24h change: {change_AAPL}")

        # Simple assertion to check if AAPL change is not empty
        assert change_AAPL != "", "AAPL 24h change is empty"

        # Now, search for GOOG and get its 24h change value
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Quote Lookup']"))
        )
        search_box.clear()  # Clear the search box
        search_box.send_keys("GOOG")
        search_box.send_keys(Keys.RETURN)

        # Wait for the 24h change element to be visible (GOOG)
        change_element_GOOG = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-testid='qsp-price-change-percent']"))
        )
        change_GOOG = change_element_GOOG.text.strip()
        print(f"GOOG 24h change: {change_GOOG}")

        # Simple assertion to check if GOOG change is not empty
        assert change_GOOG != "", "GOOG 24h change is empty"

        # Clean the 24h change values for comparison
        change_AAPL_value = change_AAPL.replace('(', '').replace(')', '').replace('%', '').replace(',', '').strip()
        change_GOOG_value = change_GOOG.replace('(', '').replace(')', '').replace('%', '').replace(',', '').strip()

        # Convert to float for proper numerical comparison
        change_AAPL_value = float(change_AAPL_value)
        change_GOOG_value = float(change_GOOG_value)

        # Simple assertion to check if the 24h change values are valid numbers
        assert change_AAPL_value > 0, "AAPL 24h change is not valid"
        assert change_GOOG_value > 0, "GOOG 24h change is not valid"

        # Compare the two stock changes
        print(f"Comparing AAPL 24h change: {change_AAPL_value}% with GOOG 24h change: {change_GOOG_value}%")

        if change_AAPL_value > change_GOOG_value:
            print("AAPL had a higher change than GOOG.")
        elif change_AAPL_value < change_GOOG_value:
            print("GOOG had a higher change than AAPL.")
        else:
            print("AAPL and GOOG had the same change.")

        print("Test over")

    def test_page_load_time(self):
        import time

        # Start the timer
        start_time = time.time()

        # Reuse reject_cookies method and search for FTNT
        self.reject_cookies()
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label='Quote Lookup']"))
        )
        search_box.send_keys("FTNT")
        search_box.send_keys(Keys.RETURN)

        # Wait for the price element to be visible (FTNT)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-testid='qsp-price']"))
        )

        # Measure the time it took to load
        load_time = time.time() - start_time
        print(f"Page load time: {load_time:.2f} seconds")

        # Adjust the load time threshold if necessary
        assert load_time < 20, f"Page load took too long: {load_time:.2f} seconds"
        print("done")

    def test_top_loser(self):
        # Reuse reject_cookies method before performing stock search
        self.reject_cookies()

        # Navigate to the 'Top Losers' section
        market_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Market"))
        )
        market_button.click()
        print("Navigated to the Market section.")

        stocks_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Stocks: Losers"))
        )
        stocks_button.click()
        print("Navigated to the loser Stocks section.")

        # Step 1: Wait for the table of top losers to load
        first_row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr:nth-child(1)"))
        )

        # Step 2: Extract the stock symbol from the first row
        symbol_element = first_row.find_element(By.CSS_SELECTOR, "span.symbol")  # Find the symbol in the row
        stock_symbol = symbol_element.text.strip()

        # Print the stock symbol
        print(f"Top Loser Symbol: {stock_symbol}")

        # Simple assertion to check that we have the data
        assert stock_symbol != "", "Stock symbol is empty"

    def test_top_Gainger(self):
        # Reuse reject_cookies method before performing stock search
        self.reject_cookies()

        # Navigate to the 'Top Losers' section
        market_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Market"))
        )
        market_button.click()
        print("Navigated to the Market section.")

        stocks_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Stocks: Gainers"))
        )
        stocks_button.click()
        print("Navigated to the loser Stocks section.")

        # Step 1: Wait for the table of top losers to load
        first_row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr:nth-child(1)"))
        )

        # Step 2: Extract the stock symbol from the first row
        symbol_element = first_row.find_element(By.CSS_SELECTOR, "span.symbol")  # Find the symbol in the row
        stock_symbol = symbol_element.text.strip()

        # Print the stock symbol
        print(f"Top Gainer Symbol: {stock_symbol}")

        # Simple assertion to check that we have the data
        assert stock_symbol != "", "Stock symbol is empty"


    print("Test Is Over")