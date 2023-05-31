import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pprint

WORD = "上田市　戸建て"
LOADIMGS=150

# フルスクリーンにする
options = webdriver.ChromeOptions()
options.add_argument("--start-fullscreen")
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # headlessモードで暫定的に必要なフラグ(そのうち不要になる)
options.add_argument('--disable-extensions')  # すべての拡張機能を無効にする。ユーザースクリプトも無効にする
options.add_argument('--proxy-server="direct://"')  # Proxy経由ではなく直接接続する
options.add_argument('--proxy-bypass-list=*')  # すべてのホスト名
options.add_argument('--start-maximized')  # 起動時にウィンドウを最大化する

# 最新のchromeドライバーをインストールして、インストール先のローカルパスを取得
driver_path = ChromeDriverManager().install()
# chromeドライバーのあるパスを指定して、起動
driver = webdriver.Chrome(service=Service(executable_path=driver_path),options=options)
# 要素がなかった場合10秒間は要素を探し続ける
driver.implicitly_wait(10)
# 最小化
driver.minimize_window()


# 検索からの画像検索を開く
driver.get(f'https://www.google.com/search?q={WORD}&tbm=isch')


imgs = driver.find_elements(By.CSS_SELECTOR,"#islmp h3+a img")
while len(imgs) < LOADIMGS:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    print(f"{len(imgs)}枚Load完了")
    time.sleep(2)
    imgs = driver.find_elements(By.CSS_SELECTOR,"#islmp h3+a img")
print(f"{len(imgs)}枚Load完了")

try:
    for index,img in enumerate(imgs):
        time.sleep(1)
        print(f"{index}/{len(imgs)}番目 取得")
        # どこかのタイミングでリンクがなくなる！？ので再取得

        if imgs[index].get_attribute("class") != "GRN7Gc":
            with open(f"./img/{WORD}{index}.png","wb")as f:
                f.write(imgs[index].screenshot_as_png)
except Exception as e:
    print(e)
print("End")