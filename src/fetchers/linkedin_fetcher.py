from fake_useragent import UserAgent
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WebsiteExtractor:
    def __init__(self):
        self.driver = self.generate_driver()
        self.headers = self.generate_headers()

    def get_user_agent(self):
        return UserAgent().random

    def generate_headers(self):
        headers = {
            "User-Agent" : self.get_user_agent()
        }
        return headers

    def get_request(self,URL):
        response = requests.get(URL,headers=self.headers)

        if response.status_code == 200:
            print("Req Successful")
            return response

        else:
            raise Exception("Request Failed")

    def generate_driver(self):
        chrome_options = Options()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=chrome_options)


    def quit_driver(self):
        self.driver.quit()

    def driver_scroll(self, MAX_SCROLLS=5, MIN_SCROLL_PIXELS=6000, MAX_SCROLL_PIXELS=9000):
        print("🖱️ Starting human-like scrolling...")
        button_found = False

        for i in range(MAX_SCROLLS):
            if button_found:
                scroll_amount = random.randint(1000, 2000)
            else:
                scroll_amount = random.randint(MIN_SCROLL_PIXELS, MAX_SCROLL_PIXELS)

            print(f"Scroll {i + 1}/{MAX_SCROLLS} → Scrolling by {scroll_amount}px")
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

            if button_found:
                delay = random.uniform(2, 5)
            else:
                delay = random.uniform(5, 15)

            print(f"⏱️ Waiting {delay:.2f} sec before next scroll...")
            time.sleep(delay)

            # Check if 'Show More' button is visible and click it
            show_more_clicked = self.click_show_more_button_if_exists()
            if show_more_clicked:
                button_found = True
                # Give time for new jobs to load
                time.sleep(random.uniform(2.0, 4.0))


    def extract_from_linkedin_job_page(self):
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        job_cards = soup.select(".jobs-search__results-list li")

        job_data = []

        for card in job_cards:
            title = card.select_one(".base-search-card__title")
            company = card.select_one(".base-search-card__subtitle")
            location = card.select_one(".job-search-card__location")

            job_data.append({
                "Title": title.text.strip() if title else "",
                "Company": company.text.strip() if company else "",
                "Location": location.text.strip() if location else ""
            })
        print(len(job_data))
        return job_data

    def click_show_more_button_if_exists(self, timeout=10):
        try:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button.infinite-scroller__show-more-button')

            for btn in buttons:
                class_attr = btn.get_attribute("class")
                if "infinite-scroller__show-more-button--visible" in class_attr:
                    print("✅ 'Show More' button found. Clicking it...")
                    self.driver.execute_script("arguments[0].click();", btn)

                    # Wait until this specific button disappears
                    WebDriverWait(self.driver, timeout).until(
                        EC.invisibility_of_element(btn)
                    )
                    print("✅ 'Show More' button is now gone.")
                    return True

            print("❌ 'Show More' button not visible.")
            return False

        except TimeoutException:
            print("⚠️ Waited too long for 'Show More' button to disappear.")
            return False

        except Exception as e:
            print(f"⚠️ Error in show more logic: {e}")
            return False



if __name__ == "__main__":
    URL = "https://www.linkedin.com/jobs/search?keywords=&location=India&f_TPR=r86400"

    extractor = WebsiteExtractor()

    try:
        extractor.driver.get(URL)
        time.sleep(3)

        extractor.driver_scroll()
        print(extractor.extract_from_linkedin_job_page())

    finally:
        extractor.quit_driver()
