from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils import find_element, sign_into_youtube_channel, new_driver
from typing import Optional
import time

def create_community_post(
    community_post_title: str,
    schedule: Optional[dict] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    cookies: Optional[str] = None,
    absolute_chromium_profile_path: Optional[str] = None,
):
    if not cookies and not email and not password and not absolute_chromium_profile_path:
        raise ValueError("You need to provide either cookies, chromium profile path, or email and password")

    print("1. Instantiating driver...")
    driver = new_driver()

    try:
        print("2. Signing into YouTube channel...")
        driver = sign_into_youtube_channel(driver, cookies=cookies, email=email, password=password, absolute_chromium_profile_path=absolute_chromium_profile_path)
        if not driver:
            return {
                "status": "error",
                "message": "Driver invalid"
            }

        print("3. Going to community page...")
        avatar_button = find_element(driver, By.CSS_SELECTOR, "button[id='avatar-btn']")
        avatar_button.click()

        view_channel_link = find_element(driver, By.XPATH, "//a[contains(text(), 'View your channel')]")
        view_channel_link.click()

        community_tab = find_element(driver, By.CSS_SELECTOR, "yt-tab-shape[tab-title='Community']")
        community_tab.click()

        channel_id = driver.current_url.split("youtube.com/")[1].split("/")[0]
        print(f"Channel ID: {channel_id}")
        
        print("4. Creating community post...")
        
        # Input community post title
        print(f"4.1. Inputting community post title: {community_post_title}...")
        community_post_title_input = find_element(driver, By.CSS_SELECTOR, "yt-formatted-string[id='commentbox-placeholder']")
        community_post_title_input.click()
        input_container = find_element(driver, By.CSS_SELECTOR, "div[id='contenteditable-root']")
        input_container.send_keys(community_post_title)

        if schedule:
            print(f"5. Scheduling post for {schedule['date']} at {schedule['time']} in {schedule['GMT_timezone']} timezone...")

            # row down button next to post button.
            print("5.1. Clicking on post additional options button...")
            post_additional_options_button = find_element(driver, By.CSS_SELECTOR, "button[aria-label='Action menu'][class='yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--call-to-action yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-button yt-spec-button-shape-next--segmented-end']")
            post_additional_options_button.click()

            print("5.2. Clicking on schedule post menu opener button...")
            schedule_post_menu_opener_button = find_element(driver, By.CSS_SELECTOR, "ytd-menu-service-item-renderer")
            schedule_post_menu_opener_button.click()
            
            print("5.3. Clicking on date picker button...")
            date_picker = find_element(driver, By.CSS_SELECTOR, "tp-yt-paper-button[id='date-picker']")
            date_picker.click()

            print("5.4. Inputting date...")
            date_input = find_element(driver, By.CSS_SELECTOR, "input[id='textbox']") 
            date_input.click()
            date_input.clear()
            # date_input.send_keys(Keys.CONTROL + "a")
            # date_input.send_keys(Keys.BACKSPACE)
            date_input.send_keys(schedule["date"])
            date_input.send_keys(Keys.ENTER)

            print("5.5. Clicking on time picker button...")
            time_picker = find_element(driver, By.CSS_SELECTOR, "tp-yt-paper-button[id='time-picker']")
            time_picker.click()

            print("5.6. Selecting time...")
            time_listbox = find_element(driver, By.CSS_SELECTOR, "tp-yt-paper-listbox[id='time-listbox']")
            # Get all the tp-yt-paper-item in the time_listbox.
            all_times = time_listbox.find_elements(By.CSS_SELECTOR, "tp-yt-paper-item")
            
            for time_listitem in all_times:
                if time_listitem.text.strip() == schedule["time"].replace(" ", " "):
                    time_listitem.click()
                    break

            print("5.7. Selecting timezone...")
            timezone_picker = find_element(driver, By.CSS_SELECTOR, "tp-yt-paper-button[id='timezone-picker']")
            timezone_picker.click()

            timezone_listbox = find_element(driver, By.CSS_SELECTOR, "tp-yt-paper-listbox[id='timezone-listbox']")
            all_timezones_items = timezone_listbox.find_elements(By.CSS_SELECTOR, "tp-yt-paper-item")

            for timezone_list_item in all_timezones_items:
                timezone_GMT_format = timezone_list_item.text.strip().split("(")[1].split(")")[0]

                if timezone_GMT_format == schedule["GMT_timezone"]:
                    timezone_list_item.click()
                    break

            print("5.8. Clicking on schedule button...")
            schedule_button = find_element(driver, By.CSS_SELECTOR, "button[aria-label='Schedule']")
            schedule_button.click()

            try:
                print("5.9. Clicking on Got it button...")
                got_it_button = find_element(driver, By.CSS_SELECTOR, "button[aria-label='Got it']")
                got_it_button.click()

                schedule_button = find_element(driver, By.CSS_SELECTOR, "button[aria-label='Schedule']")
                schedule_button.click()
            except:
                print("Not needed to click on Got it button.")

        else:
            print("5. Posting community post...")
            post_button = find_element(driver, By.CSS_SELECTOR, "ytd-button-renderer[id='submit-button']")
            post_button.click()
    
        time.sleep(10)
        driver.quit()
        return {
            "status": "success", 
            "message": "Community post created successfully", 
        }

    except Exception as e:
        print('Error:', e)
        with open("error.txt", "w") as f:
            f.write(str(e))

        return {
            "status": "error",
            "message": str(e),
        }
