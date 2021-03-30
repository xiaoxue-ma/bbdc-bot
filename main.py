import json
import telegram
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

browser = webdriver.Chrome()
# browser = webdriver.Chrome(executable_path='/path/to/webdriver') 

# Read cookie from cookie.json
with open('cookie.json') as f:
  cookies = json.load(f)

# Navigate to a dummy url on the same domain to setup cookie
dummy_url = '/404error'
browser.get('http://www.bbdc.sg' + dummy_url)
for cookie in cookies:
    browser.add_cookie(cookie)

while True:
    browser.get('http://www.bbdc.sg/bbdc/b-mainframe.asp')

    # Switching to Left Frame and accessing element by text
    browser.switch_to.default_content()
    frame = browser.find_element_by_name('leftFrame')
    browser.switch_to.frame(frame)

    # Click "Booking without Fixed Instructor"
    nonFixedInstructor = browser.find_element_by_link_text('Booking without Fixed Instructor')
    nonFixedInstructor.click()

    # Switching back to Main Frame and pressing 'I Accept'
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 300)
    wait.until(EC.frame_to_be_available_and_switch_to_it(browser.find_element_by_name('mainFrame')))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn"))).click()

    # Selection menu
    browser.switch_to.default_content()
    wait = WebDriverWait(browser, 300)
    wait.until(EC.frame_to_be_available_and_switch_to_it(browser.find_element_by_name('mainFrame')))
    wait.until(EC.visibility_of_element_located((By.ID, "checkMonth")))
    
    # Tick months
    # 0 refers to first month shown in page, 1 refers to second month, and so on...
    months = browser.find_elements_by_id('checkMonth')
    months[0].click() # Current Month
    months[1].click() # Next Month
    months[2].click() # Next next month

    # Tick sessions
    # 0 refers to first session, 1 refers to second session, and so on...
    sessions = browser.find_elements_by_id('checkSes')
    sessions[8].click() # all sessions

    # Tick days
    # 0 refers to first day, 1 refers to second day, and so on...
    days = browser.find_elements_by_id('checkDay')
    days[7].click() # all days

    # Click Search
    browser.find_element_by_name('btnSearch').click()

    # Dismissing Prompt
    wait = WebDriverWait(browser, 300)
    wait.until(EC.alert_is_present())
    alert_obj = browser.switch_to.alert
    alert_obj.accept()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn")))

    # 0 refers to first slot, 1 refers to second slot, and so on...
    slots = browser.find_elements_by_name('slot')
    # Parse slot information
    times=[]
    for slot in slots:
        td = slot.find_element_by_xpath('..')
        text = td.get_attribute("onmouseover")
        parts = text.split(",")
        session = parts[3]
        session = session.replace('"', '')
        date = parts[2]
        start = parts[4]
        end = parts[5]
        current = date + ", " + start + "-" + end + ", session: " + session
        current = current.strip().replace('"', '') # Example: 03/02/2021 (Wed), 0730-09:10, session: 1
        times.append(current)
    message = 'No slots available :(\n' if len(times) == 0 else "Found slots: \n"+'\n'.join(times)

    # Send to telegram and print in console
    telegram.send_message(message)
    print(message)

    time.sleep(60 * 5) # 5min: 60s * 5
