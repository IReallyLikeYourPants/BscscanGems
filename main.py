from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from concurrent import futures
import time


def info_crypto(address):
    try:
        driver = webdriver.Chrome()
        driver.set_window_position(-10000,0)
        driver.get("https://poocoin.app/tokens/" + address)
        timeout = 20
        element_present1 = EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1'''))
        element_present2 = EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span'''))
        element_present3 = EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/span'''))
        element_present4 = EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]'''))
        element_present5 = EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]'''))
        WebDriverWait(driver, timeout).until(element_present1)
        WebDriverWait(driver, timeout).until(element_present2)
        WebDriverWait(driver, timeout).until(element_present3)
        WebDriverWait(driver, timeout).until(element_present4)
        WebDriverWait(driver, timeout).until(element_present5)
        a = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/h1''').text.split("/")[0]+")"
        b = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div[1]/div/span''').text
        c = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/span''').text[1:-1]
        d = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]''').text.split("\n")[1]
        e = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]''').text
        f = e[1:].replace(",","")
        g = c[1:].replace(",","")
        h = d.replace(",","")
        if address not in check_esistenza and int(f) < 1000001 and int(g)> 10000 and int(h) > 1000000000:
            cryptos.append((a, b, e, d, c, address))
        if address not in check_esistenza:
            check_esistenza.add(address)
        driver.quit()
    except TimeoutException as inst:
        print("La crypto " + address + " non è listata su pancake:).")
        check_esistenza.add(address)
    except ValueError as inst2:
        print("La crypto " + address + " è morta:).")
        check_esistenza.add(address)
    except Exception as inst3:
        print(type(inst3))
        print(inst3.args)
        print("errore nell'address: " + address)


def find_gems_bscscan():
    driver = webdriver.Chrome()
    driver.set_window_position(-10000,0)
    driver.get("https://bscscan.com/tokentxns")
    timeout = 8000
    element_present1 = EC.presence_of_element_located((By.XPATH, '''//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[49]/td[9]/a/img'''))
    element_present2 = EC.presence_of_element_located((By.XPATH, '''//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[49]/td[9]/a'''))
    WebDriverWait(driver, timeout).until(element_present1)
    WebDriverWait(driver, timeout).until(element_present2)
    for e in range(1 , 51):
        b = driver.find_element(By.XPATH, '''//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[''' + str(e) + ''']/td[9]/a/img''').get_attribute("src")
        c = driver.find_element(By.XPATH, '''//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[''' + str(e) + ''']/td[9]/a''').get_attribute("href").split("/")[-1]
        if b == "https://bscscan.com/images/main/empty-token.png" and c not in links and c not in check_esistenza:
            links.append(c)
    driver.quit()


val = 1
cryptos = []
check_esistenza= set()
links = []

while (True):
    print("####################### " + str(val) + " #######################")
    print("")
    find_gems_bscscan()
    print("Analizzo i seguenti indirizzi:")
    print("")
    for e in links:
        print(e)
    print("")
    with futures.ThreadPoolExecutor() as executor:
      titles = list(executor.map(info_crypto, links))
    if len(cryptos) > 0:
        print("")
        print("Gemme trovate:")
        print("")
        for e in cryptos:
            print(e)
    links = []
    print("")
    if val%10 == 0:
        print("Crypto analizzate: " + str(val*50))
        print("")
    val +=1