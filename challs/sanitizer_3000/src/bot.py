
import asyncio
from nis import cat
from warnings import catch_warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


async def visit(user_id, admin_token):
    url = f'http://web:8080/profile/{user_id}'
    print("Visiting", url)

    options = Options()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-infobars')
    options.add_argument('disable-background-networking')
    options.add_argument('disable-default-apps')
    options.add_argument('disable-extensions')
    options.add_argument('disable-gpu')
    options.add_argument('disable-sync')
    options.add_argument('disable-translate')
    options.add_argument('hide-scrollbars')
    options.add_argument('metrics-recording-only')
    options.add_argument('mute-audio')
    options.add_argument('no-first-run')
    options.add_argument('dns-prefetch-disable')
    options.add_argument('safebrowsing-disable-auto-update')
    options.add_argument('media-cache-size=1')
    options.add_argument('disk-cache-size=1')
    options.add_argument('user-agent=BugHTB/1.0')
   
    

    try:

        browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

    except Exception as e:
        print(e)
        return


    browser.get("http://web:8080/")
    browser.add_cookie({'name': 'admin_token', 'value': admin_token, 'url': 'http://web:8080', 'httpOnly': False, 'sameSite': 'Strict', 'secure': False,'expiry': 9999999999})
    
    try:
        browser.get(url)
        WebDriverWait(browser, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
        print("dela")
    except Exception as e:
        print(e)
        pass
    finally:
        browser.quit()
    

    print("Done visiting")
