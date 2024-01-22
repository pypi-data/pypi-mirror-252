from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle
import os


class YouTubeUploader:
    def __init__(self, chrome_driver_path, email, password, channel_name, video_path='', title_text='', description_text='', for_kids=False):
        self.chrome_driver_path = chrome_driver_path
        self.email = email
        self.password = password
        self.channel_name = channel_name
        self.video_path = video_path
        self.title_text = title_text
        self.description_text = description_text
        self.for_kids = for_kids

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        self.service = Service(executable_path=self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.maximize_window()

    def _saveCookies(self):
        # Get and store cookies after login
        cookies = self.driver.get_cookies()
        # Store cookies in a file
        pickle.dump(cookies, open('yt_cookies.pkl', 'wb'))


    def _loadCookies(self):
        # Check if cookies file exists
        if 'yt_cookies.pkl' in os.listdir():
            
            self.driver.delete_all_cookies()

            # Load cookies to a vaiable from a file
            cookies = pickle.load(open('yt_cookies.pkl', 'rb'))

            # Set stored cookies to maintain the session
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh() # Refresh Browser after login
        else:
            print('No cookies file found')

    def _login_without_cookies(self):
        self.driver.get('https://accounts.google.com/InteractiveLogin/signinchooser?continue=https%3A%2F%2Fstudio.youtube.com')

        email_input = self.driver.find_element(By.ID, 'identifierId')
        email_input.clear()
        email_input.send_keys(self.email)
        email_input.send_keys(Keys.ENTER)

        password_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "Passwd")))
        password_input.clear()
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)
        self._saveCookies()


    def _login_with_cookies(self):
        self.driver.get('https://www.youtube.com')

        self._loadCookies()

        self.driver.get('https://studio.youtube.com')


    def login(self):
        try:
            if 'yt_cookies.pkl' in os.listdir():
                self._login_with_cookies()
            else:
                self._login_without_cookies()
            time.sleep(2)

        except Exception as e:
            print(e)

    def select_channel(self):
        try:
            account = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "avatar-btn")))
            account.click()

            change_account_elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.ID, "endpoint")))
            desired_text = 'Сменить аккаунт'
            for element in change_account_elements:
                change_account_text = element.text
                if change_account_text == desired_text:
                    element.click()
                    break

            channel_elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.ID, "channel-title")))
            desired_text = self.channel_name
            for channel_element in channel_elements:
                channel_title_text = channel_element.text
                if channel_title_text == desired_text:
                    channel_element.click()
                    break
        except Exception as e:
            print(e)

    def upload_video(self):
        try:
            create_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "create-icon")))
            create_btn.click()

            add_video = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "text-item-0")))
            add_video.click()

            video_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            video_input.send_keys(self.video_path)

            title = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//ytcp-video-title//ytcp-social-suggestion-input/div')))
            # Convert text to send emoji because the web driver does not recognize emoji 
            self.driver.execute_script("arguments[0].innerHTML = '{}'".format(self.title_text),title)
            title.send_keys('.')
            title.send_keys(Keys.BACKSPACE)

            if self.description_text != '':
                description = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//ytcp-video-description//ytcp-social-suggestion-input/div")))
                # Convert text to send emoji because the web driver does not recognize emoji 
                self.driver.execute_script("arguments[0].innerHTML = '{}'".format(self.description_text),description)
                description.send_keys('.')
                description.send_keys(Keys.BACKSPACE)

            if self.for_kids:
                element_name = "VIDEO_MADE_FOR_KIDS_MFK"
            else:
                element_name = "VIDEO_MADE_FOR_KIDS_NOT_MFK"

            radio_btn_for_kids = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, element_name)))
            radio_btn_for_kids.click()

            next = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "next-button")))
            next.click()
            next.click()
            next.click()

            radio_btn_public = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "PUBLIC")))
            radio_btn_public.click()

            time.sleep(5)
            publish_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "done-button")))
            publish_btn.click()
            time.sleep(3)

            close_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//ytcp-uploads-still-processing-dialog//ytcp-button/div")))
            close_btn.click()

        except Exception as e: 
            print(e)

    def close_driver(self):
        self.driver.close()
        self.driver.quit()


def title_validation(title_text: str):
    if len(title_text) > 100:
        text = title_text[:97] + '...'

        return text
    
    else:
        
        return title_text


def upload_multiple_videos(login_data: dict, video_list: list):
    # YouTubeUploader class initialization
    uploader = YouTubeUploader(
        chrome_driver_path=login_data["chrome_driver_path"],
        email=login_data["email"],
        password=login_data["password"],
        channel_name=login_data["channel_name"]
    )

    try:
        # logging and selecting a channel for publication
        uploader.login()
        uploader.select_channel()

        # publication
        while video_list:
            video_info = video_list[0]
            video_info: dict
            
            uploader.video_path = video_info['video_path']
            uploader.title_text = title_validation(video_info['title_text'])

            description_text = video_info.get('description_text')
            if description_text:
                uploader.description_text = description_text
            uploader.upload_video()
            del video_list[0]
            time.sleep(5)

    finally:
        uploader.close_driver()
        return video_list
