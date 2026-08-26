from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import keyboard
import getpass

LOGIN_URL: str = "https://s.rikkyo.ac.jp/shukkinbo"
MAIN_URL: str = "https://shukkinbo.rikkyo.ac.jp/TimePro-VG/page/Ovg80100t.aspx"
USER_ID: str = input("V-campus ID：")
PASSWORD: str = getpass.getpass("password：")
CONTENT: str = input("勤務内容を入力してください：")
WEBDRIVER: int = int(input("使いたいウェブドライバを選択してください\n1: Chrome 2: Edge 3: FireFox\n"))
WORK_START_TIME: str = "0900"
WORK_END_TIME: str = "1800"
REST_START_TIME = "1200"
REST_END_TIME: str = "1300"

if WEBDRIVER == 1:
    driver = webdriver.Chrome()
elif WEBDRIVER == 2:
    driver = webdriver.Edge()
elif WEBDRIVER == 3:
    driver = webdriver.Firefox()
else:
    exit()

try:
    driver.get(LOGIN_URL)
    
    # ID入力
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username_input"))).send_keys(USER_ID)

    # パスワード入力
    driver.find_element(By.ID, "password_input").send_keys(PASSWORD)
    
    # ログインボタン押下
    driver.find_element(By.ID, "login_button").click()

    wait = WebDriverWait(driver, 10)
    driver.switch_to.frame(wait.until(EC.presence_of_element_located((By.ID, "DataFrame"))))
    
    # ホバーメニューを出す
    parent_menu = driver.find_element(By.XPATH, "//td[text()='出勤簿入力']")
    ActionChains(driver).move_to_element(parent_menu).perform()

    # 出勤簿を出す
    wait = WebDriverWait(driver, 10)
    menu_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[text()='出勤簿(時給制・本人用)']")))
    menu_element.click()
    
    driver.switch_to.default_content()
    
    # ポップアップウィンドウのiframeに移動
    wait = WebDriverWait(driver, 10)
    driver.switch_to.frame(wait.until(EC.presence_of_element_located((By.CLASS_NAME, "UI_Dialog_Frame"))))
    
    # OKボタンを押下
    driver.find_element(By.ID, "SuperCalendar1_btnOK").click()
    
    driver.switch_to.default_content()
    
    wait = WebDriverWait(driver, 10)
    driver.switch_to.frame(wait.until(EC.presence_of_element_located((By.ID, "DataFrame"))))
    driver.switch_to.frame(wait.until(EC.presence_of_element_located((By.ID, "DisplayArea"))))
    driver.switch_to.frame(wait.until(EC.presence_of_element_located((By.ID, "ChangeView"))))
    
    wait = WebDriverWait(driver, 10)
    driver.switch_to.frame(wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'OVa80140tGridData.aspx')]"))))
    activator = driver.find_element(By.CLASS_NAME, "BsmActivor")

    last_top = None
    last_left = None

    while True:
        # 現在のカーソル位置を取得
        current_top = activator.value_of_css_property("top")
        current_left = activator.value_of_css_property("left")

        if (current_top, current_left) != (last_top, last_left):
            if keyboard.is_pressed('ctrl'):
                actions = ActionChains(driver)
                actions.send_keys(CONTENT)
                actions.perform()

                last_top = current_top
                last_left = current_left
            elif keyboard.is_pressed('s'):
                actions = ActionChains(driver)
                actions.send_keys(WORK_START_TIME)
                actions.perform()

                last_top = current_top
                last_left = current_left
            elif keyboard.is_pressed('e'):
                actions = ActionChains(driver)
                actions.send_keys(WORK_END_TIME)
                actions.perform()

                last_top = current_top
                last_left = current_left
            elif keyboard.is_pressed('b'):
                actions = ActionChains(driver)
                actions.send_keys(REST_START_TIME)
                actions.perform()

                last_top = current_top
                last_left = current_left
            elif keyboard.is_pressed('f'):
                actions = ActionChains(driver)
                actions.send_keys(REST_END_TIME)
                actions.perform()

                last_top = current_top
                last_left = current_left
                
        elif keyboard.is_pressed('q'):
            break

        time.sleep(0.2)
    
    
finally:
    driver.quit()
