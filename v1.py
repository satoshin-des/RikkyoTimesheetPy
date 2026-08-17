from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import time

LOGIN_URL = "http://150.93.196.183/login.asp?mode=1"                                            # ログインURL
MAIN_URL = "http://150.93.196.183/entry_B/entry_B.asp?id=&ym=&dept=&yosan="                     # 勤怠管理を行うURL
USER_ID = input("ユーザーIDを入力してください：")                                                   # ID
PASSWORD = input("パスワードを入力してください：")                                                  # パスワード
CONTENT = input("勤務内容を入力してください：")                                                     # 勤務内容
WEBDRIVER = int(input("使いたいウェブドライバを選択してください\n1: Chrome 2: Edge 3: FireFox"))    # ウェブドライバの選択
TIME1 = ["9", "12"]                                                                             # 勤務時間その１
TIME2 = ["13", "18"]                                                                            # 勤務時間その2

if WEBDRIVER == 1:
    driver = webdriver.Chrome()
elif WEBDRIVER == 2:
    driver = webdriver.Edge()
elif WEBDRIVER == 3:
    driver = webdriver.Firefox()
else:
    exit()


try:
    # ログインページを開く
    driver.get(LOGIN_URL)
    
    # ID入力
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userid"))).send_keys(USER_ID)

    # パスワード入力
    driver.find_element(By.ID, "passwd").send_keys(PASSWORD)

    # ログインボタン押下
    driver.find_element(By.ID, "btnLogin").click()

    # ログイン後のページがロードされるまで待機
    time.sleep(1)
    
    # 勤怠管理ページへ
    driver.get(MAIN_URL)
    
    # ログイン後のページがロードされるまで待機
    time.sleep(3)
    
    # iframeに移動
    iframe = driver.find_element(By.ID, "f01")
    driver.switch_to.frame(iframe)
    
    while True:
        # 勤務内容の入力
        driver.find_element(By.NAME, "inp27").send_keys(CONTENT)
        
        # 勤務時間の入力
        driver.find_element(By.NAME, "inp03").send_keys(TIME1[0])
        driver.find_element(By.NAME, "inp04").send_keys("00")
        driver.find_element(By.NAME, "inp05").send_keys(TIME1[1])
        driver.find_element(By.NAME, "inp06").send_keys("00")
        driver.find_element(By.NAME, "inp07").send_keys(TIME2[0])
        driver.find_element(By.NAME, "inp08").send_keys("00")
        driver.find_element(By.NAME, "inp09").send_keys(TIME2[1])
        driver.find_element(By.NAME, "inp10").send_keys("00")

        while True:
            try:
                # 毎回 iframe に入り直す
                driver.switch_to.default_content()
                iframe = driver.find_element(By.ID, "f01")
                driver.switch_to.frame(iframe)

                # 毎回要素を取り直す
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "inp27"))
                )
                value = element.get_property("value")

                if value == "":
                    element.clear()
                    break

            except UnexpectedAlertPresentException:
                try:
                    WebDriverWait(driver, 5).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    print("Alert text:", alert.text)
                    alert.accept()
                except TimeoutException:
                    print("アラートが表示されませんでした")

                # アラート処理後に再びiframeへ
                driver.switch_to.default_content()
                iframe = driver.find_element(By.ID, "f01")
                driver.switch_to.frame(iframe)

        time.sleep(0.666)

finally:
    driver.quit()
