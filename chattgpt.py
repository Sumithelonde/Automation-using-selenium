from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
import random
import requests
from bs4 import BeautifulSoup
import json

class EdgeAutomation:
    def __init__(self):
        # Enhanced Edge WebDriver setup
        self.options = webdriver.EdgeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-notifications")
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Edge(options=self.options)

    def wait_for_element(self, by, value, timeout=15):
        """Enhanced wait function with better error handling"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None

    def get_trending_topics(self):
        """Fetch trending topics from multiple sources"""
        trending_topics = set()  # Using set to avoid duplicates

        try:
            # Twitter Trends (Top 50 worldwide)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            # Method 1: Twitter Trending
            try:
                response = requests.get('https://trends24.in/', headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                trends = soup.select('.trend-card__list li a')
                trending_topics.update([trend.text.strip() for trend in trends[:20]])
            except Exception as e:
                print(f"Error fetching Twitter trends: {e}")

            # Method 2: Google Trends
            try:
                response = requests.get(
                    'https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=-480&geo=US',
                    headers=headers
                )
                json_data = json.loads(response.text[5:])  # Remove ")]}'" from the beginning
                for trend in json_data['default']['trendingSearchesDays'][0]['trendingSearches']:
                    trending_topics.add(trend['title']['query'])
            except Exception as e:
                print(f"Error fetching Google trends: {e}")

            # Method 3: Reddit Popular
            try:
                response = requests.get(
                    'https://www.reddit.com/r/popular.json',
                    headers=headers
                )
                json_data = response.json()
                for post in json_data['data']['children'][:10]:
                    trending_topics.add(post['data']['title'])
            except Exception as e:
                print(f"Error fetching Reddit trends: {e}")

        except Exception as e:
            print(f"Error in get_trending_topics: {e}")

        # Add some general interest topics as fallback
        fallback_topics = [
            "Latest technology news",
            "Popular movies 2024",
            "Trending music artists",
            "Latest gaming news",
            "Popular books 2024",
            "Tech gadgets review",
            "Viral social media trends",
            "Popular TV shows",
            "Latest science discoveries",
            "Trending fashion styles"
        ]
        trending_topics.update(fallback_topics)

        return list(trending_topics)

    def check_for_cookies(self):
        """Comprehensive check for different types of cookie popups"""
        try:
            # List of common cookie popup indicators - both footer and center popups
            cookie_indicators = [
                # Center popup indicators
                "//div[contains(@class, 'bnp_rich_div')]",  # Rich dialog popup
                "//div[@id='bnp_ttc_div']",  # Consent dialog
                "//div[@id='bnp_container']",  # Cookie container
                "//div[contains(@class, 'cc_banner')]",  # Common cookie banner class
                # Footer popup indicators
                "//div[@id='cookie-banner']",
                "//div[contains(@class, 'cookie-banner')]",
                # Additional Bing-specific selectors
                "//div[@id='thp_notf_div']",  # Notification popup
                "//div[contains(@class, 'thp_notify_div')]",  # Another notification div
                # Edge-specific consent popup
                "//div[@id='consent-modal']",
                "//div[contains(@class, 'consent-dialog')]"
            ]

            for indicator in cookie_indicators:
                elements = self.driver.find_elements(By.XPATH, indicator)
                if elements:
                    print(f"Detected cookie popup: {indicator}")
                    return True
            return False
        except Exception as e:
            print(f"Error checking for cookies: {e}")
            return False

    def handle_cookies(self):
        """Enhanced cookie popup handler for multiple types of popups"""
        cookie_buttons = [
            # Center popup reject buttons
            "//button[contains(@id, 'bnp_btn_reject')]",
            "//button[@id='reject-all']",
            "//button[contains(@class, 'reject-all')]",
            "//button[text()='Reject all']",
            "//button[contains(text(), 'Reject all')]",
            "//button[contains(text(), 'Reject')]",

            # Specific selectors for the middle page popup
            "//div[contains(@class, 'bnp_rich_div')]//button[contains(@class, 'reject')]",
            "//div[@id='bnp_ttc_div']//button[contains(@class, 'reject')]",
            "//div[@id='bnp_container']//button[contains(@title, 'Reject')]",

            # Footer banner reject buttons
            "//div[@id='cookie-banner']//button[contains(text(), 'Reject')]",
            "//div[contains(@class, 'cookie-banner')]//button[contains(text(), 'Reject')]",

            # Additional Bing-specific buttons
            "//button[@id='bnp_hfly_cntl']",
            "//button[@id='bnp_btn_nope']",
            "//button[@id='bnp_ttc_close']",

            # Generic reject buttons with different text variations
            "//button[contains(text(), 'No, thanks')]",
            "//button[contains(text(), 'Not now')]",
            "//button[contains(text(), 'Decline')]",
            "//button[contains(text(), 'Don't allow')]",

            # Fallback to accept buttons if reject is not available
            "//button[contains(text(), 'Accept')]",
            "//button[contains(text(), 'Allow')]",
            "//button[contains(text(), 'I agree')]"
        ]

        # Try to handle popups multiple times as they might appear sequentially
        max_attempts = 3
        popups_handled = 0

        for attempt in range(max_attempts):
            found_popup = False

            # Check each button pattern
            for xpath in cookie_buttons:
                try:
                    # Find all matching buttons (might be multiple popups)
                    buttons = self.driver.find_elements(By.XPATH, xpath)

                    for button in buttons:
                        if button.is_displayed():
                            try:
                                # Scroll to the button
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                    button
                                )
                                time.sleep(0.5)

                                # Try multiple click methods
                                try:
                                    button.click()
                                except:
                                    try:
                                        self.driver.execute_script("arguments[0].click();", button)
                                    except:
                                        continue

                                print(f"Successfully clicked cookie button: {xpath}")
                                found_popup = True
                                popups_handled += 1
                                time.sleep(1)  # Wait for popup to disappear

                            except Exception as e:
                                print(f"Failed to click button {xpath}: {str(e)}")
                                continue

                except Exception as e:
                    continue

            if not found_popup:
                print(f"No more cookie popups found after handling {popups_handled} popups")
                break

            time.sleep(1)  # Wait before next attempt

        return popups_handled > 0

    def check_for_cookies(self):
        """Quick check if cookie popup exists"""
        try:
            cookie_indicators = [
                "//button[contains(@id, 'bnp_btn_reject')]",
                "//div[@id='cookie-banner']",
                "//*[@id='bnp_container']",
                "//div[contains(@class, 'cookie-banner')]"
            ]

            for indicator in cookie_indicators:
                element = self.driver.find_elements(By.XPATH, indicator)
                if element:
                    return True
            return False
        except:
            return False

    def search_and_click(self, search_term):
        """Perform search and click first result with enhanced error handling"""
        try:
            # Navigate to Bing
            self.driver.get("https://www.bing.com")
            time.sleep(2)

            # Only handle cookies if popup is detected
            if self.check_for_cookies():
                print("Cookie popup detected, handling it...")
                self.handle_cookies()
                time.sleep(1)
            else:
                print("No cookie popup detected, proceeding with search...")

            # Find and fill search box
            search_box = self.wait_for_element(By.NAME, "q")
            if not search_box:
                raise Exception(f"Could not find search box for term: {search_term}")

            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)  # Increased wait time for results to load

            # Enhanced click functionality with multiple attempts and methods
            max_retries = 5  # Increased retry attempts
            for attempt in range(max_retries):
                try:
                    # Try different XPath patterns for the first result
                    xpath_patterns = [
                        "(//li[@class='b_algo']//a)[1]",
                        "//div[@id='b_results']//li[contains(@class, 'b_algo')]//h2/a",
                        "//div[@class='b_title']//h2/a",
                        "//li[contains(@class, 'b_algo')]//cite/..",  # Parent of cite element
                        "//div[@id='b_results']//h2/a"
                    ]

                    for xpath in xpath_patterns:
                        try:
                            # Wait for element with both presence and clickable conditions
                            first_result = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, xpath))
                            )

                            # Scroll element into view
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                first_result
                            )
                            time.sleep(1)

                            # Try multiple click methods
                            try:
                                # First attempt: Regular click
                                first_result.click()
                            except Exception as click_error:
                                print(f"Regular click failed, trying JavaScript click...")
                                try:
                                    # Second attempt: JavaScript click
                                    self.driver.execute_script("arguments[0].click();", first_result)
                                except Exception as js_error:
                                    print(f"JavaScript click failed, trying direct navigation...")
                                    try:
                                        # Third attempt: Direct navigation
                                        href = first_result.get_attribute('href')
                                        if href:
                                            print(f"Navigating directly to: {href}")
                                            self.driver.get(href)
                                        else:
                                            print("Failed to get href attribute")
                                            continue
                                    except Exception as href_error:
                                        print(f"Direct navigation failed: {str(href_error)}")
                                        continue

                            time.sleep(2)
                            return True

                        except Exception as e:
                            continue

                    print(f"Attempt {attempt + 1}: Could not click result, retrying...")
                    time.sleep(1)

                except Exception as e:
                    print(f"Click attempt {attempt + 1} failed: {str(e)}")
                    time.sleep(1)

            print(f"Failed to click result for: {search_term} after all attempts")
            return False

        except Exception as e:
            print(f"Error during search for {search_term}: {str(e)}")
            return False

    def random_search_automation(self, num_searches=10):
        """Perform random searches using trending topics"""
        try:
            print("\n🔍 Fetching trending topics...")
            trending_topics = self.get_trending_topics()

            if not trending_topics:
                print("❌ No trending topics found. Using fallback topics.")
                trending_topics = [
                    "Latest news",
                    "Popular movies",
                    "Technology trends",
                    "Sports updates",
                    "Music hits"
                ]

            # Randomly select and search topics
            selected_topics = random.sample(
                trending_topics,
                min(num_searches, len(trending_topics))
            )

            print(f"\n✨ Selected {num_searches} random trending topics to search:")
            for i, topic in enumerate(selected_topics, 1):
                print(f"{i}. {topic}")

            for topic in selected_topics:
                self.driver.execute_script("window.open('', '_blank')")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                print(f"\n🔎 Searching for: {topic}")
                if not self.search_and_click(topic):
                    print(f"⚠️ Failed to process topic: {topic}")
                time.sleep(random.uniform(2, 4))  # Random delay between searches

        except Exception as e:
            print(f"❌ Error in random search automation: {str(e)}")

    def run_automation(self):
        """Main automation function"""
        try:
            # Ask user for automation type
            print("\n🤖 Select Automation Type:")
            print("1. Manual trend input")
            print("2. Random trending searches")
            choice = input("Enter your choice (1 or 2): ").strip()

            if choice == "1":
                # Original manual trend input flow
                self.search_and_click("Copilot.ai")
                self.handle_cookies()

                print("\n🔹 Enter the top 10 trends (each trend will be searched in a new tab)")
                trends_list = []
                for i in range(1, 11):
                    trend = input(f"Enter Trend {i}: ").strip()
                    if trend:
                        trends_list.append(f'"{trend}"')

                print("\n✅ Captured Trends:")
                for trend in trends_list:
                    print(trend)

                for trend in trends_list:
                    self.driver.execute_script("window.open('', '_blank')")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    if not self.search_and_click(trend):
                        print(f"⚠️ Failed to process trend: {trend}")

            elif choice == "2":
                # Random trending searches
                num_searches = int(input("\nEnter number of random searches to perform (1-20): ").strip())
                num_searches = max(1, min(20, num_searches))  # Limit between 1 and 20
                self.random_search_automation(num_searches)

            else:
                print("❌ Invalid choice. Exiting...")

            input("\nPress Enter to close the browser...")

        except Exception as e:
            print(f"❌ Error in automation: {str(e)}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    automation = EdgeAutomation()
    automation.run_automation()