from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import re


def write_to_file(href_text):
    with open('links.txt', 'a') as file:
        file.write(href_text + '\n')


options = Options()
options.add_argument("--user-data-dir=C:\\Users\\albar\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument("--profile-directory=Person 1")
driver = webdriver.Chrome(options=options)

driver.get('https://web.facebook.com/friends/requests')

# Open Friend Requests Sent
friendRequest_path = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[3]/div/span'
button = driver.find_element(By.XPATH, friendRequest_path)
button.click()
time.sleep(3)


amountSent_path = "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[1]/span"
sent_requests = driver.find_element(By.XPATH, amountSent_path)
text_sent_requests = sent_requests.get_attribute("textContent")
amount_sent = int(re.findall(r'\d+', text_sent_requests)[0])
amount_sent += 2 # + 2 because increment starts at 2 as counting in fbLink_path variable
increment = 2
while (increment != amount_sent):
    # Get the link first
    time.sleep(0.3)

    fbLink_path =f"/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[{increment}]/div/a"
    element = driver.find_element(By.XPATH, fbLink_path)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    href = element.get_attribute('href')
    # href = href.replace("web", "mbasic")
    # href = href.replace("www", "mbasic")
    print(write_to_file(href))

    # Cancel the friend request
    cancel_path = f"/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[{increment}]/div/a/div[1]/div[2]/div/div[2]"
    button = driver.find_element(By.XPATH, cancel_path)
    button.click()
    increment += 1


with open('links.txt', 'r+') as file:
    link = file.readline().strip()
    while link != '':
        driver.get(link)
        addFriend_path = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[4]/div/div/div[1]/div/div/div/div[1]/div[2]/span/span"
        # addFriend_path_basic = "/html/body/div/div/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr/td[1]/a"
        while True:
            try:
                button = driver.find_element(By.XPATH, addFriend_path)
                time.sleep(1)
                if (button.get_attribute("textContent") == "Add friend"):
                    print(f"Clicked! {link}")
                    button.click()
                break
            except StaleElementReferenceException:
                print(f"Error {link}")
                continue
            except NoSuchElementException:
                break

        # Remove first line
        with open('links.txt', 'r') as texts:
            lines = texts.readlines()
        with open('links.txt', 'w') as remove:
            remove.writelines(lines[1:])

        link = file.readline().strip()


