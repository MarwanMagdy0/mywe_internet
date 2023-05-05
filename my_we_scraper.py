from selenium import webdriver
import time,os
import json,datetime
from selenium.webdriver.common.by import By
import warnings
user_name = "number 03.........."
password = "password"
warnings.filterwarnings("ignore", category=DeprecationWarning)
class JsonIt:
    def __init__(self,name):
        self.name = name
        try:
            f=open(f'{self.name}.json','r')
            data=json.load(f)
            f.close()
        except:
            data = {}
            dump =json.dumps(data)
            file = open(f'{name}.json','w')
            file.write(dump)
            file.close()
    def save_data(self,Data):
        with open(f'{self.name}.json','w') as f:
            dic=json.dumps(Data)
            f.write(dic)
    def read_data(self):
        f=open(f'{self.name}.json','r')
        data=json.load(f)
        f.close()
        return data
    def __getitem__(self,key):
        f=open(f'{self.name}.json','r')
        data=json.load(f)
        f.close()
        return data.get(key)
    def __repr__(self):
        f=open(f'{self.name}.json','r')
        f.close()
        return str(json.load(f))
        


def get_data():
    found = False
    i = 0
    while not found:
        time.sleep(3)
        try:
            data = driver.find_element(By.CSS_SELECTOR, "#pr_id_6 > div > div > div > div > div > app-gauge > div.usage > span.remaining-details.min-height-55.ng-star-inserted")
            return float(data.text.split()[0])
        except:
            i+=1
            if i==5:
                print("i tried 5 times and failed")
                print("trying again but try to exit")
                i=0


user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
options = webdriver.ChromeOptions()
options.headless=True
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-extentions")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--log-level=3')
# print(file_path)
driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)
driver.get("https://my.te.eg/")
while driver.title !="MyWE":
    time.sleep(0.1)
time.sleep(1)

print("connected")
input_field = driver.find_element(By.CSS_SELECTOR, "#login-service-number-et")
input_field.send_keys(user_name)
input_field = driver.find_element(By.CSS_SELECTOR, "body > app-root > div > div.top-relative.p-mt-5 > app-login > div > div > div > p-card:nth-child(2) > div > div > div > form > div > div.row > div.col.ng-star-inserted > app-service-number-type > div > p-dropdown > div > div.p-dropdown-trigger.ng-tns-c86-6 > span")
input_field.click()
time.sleep(0.5)
input_field = driver.find_element(By.CSS_SELECTOR, "body > app-root > div > div.top-relative.p-mt-5 > app-login > div > div > div > p-card:nth-child(2) > div > div > div > form > div > div.row > div.col.ng-star-inserted > app-service-number-type > div > p-dropdown > div > div.ng-trigger.ng-trigger-overlayAnimation.ng-tns-c86-6.p-dropdown-panel.p-component.ng-star-inserted > div > ul > p-dropdownitem:nth-child(1) > li")
input_field.click()
input_field = driver.find_element(By.CSS_SELECTOR, "#login-password-et")
input_field.send_keys(password)
time.sleep(0.5)
input_field = driver.find_element(By.CSS_SELECTOR, "#login-login-btn")
input_field.click()
print("Login Successfuly")
time.sleep(1)
amount = get_data()
print(amount , "GB Remaining")
driver.quit()

date = str(datetime.datetime.now())
file_path= os.path.dirname(__file__)+"\\"
os.chdir(file_path)
J = JsonIt("net")
recent_data = J.read_data()
recent_data[int(time.time())] = amount
J.save_data(recent_data)

flag = input("plot usage curve?(y/n)")
if flag!="y" or flag=="":
    os._exit(0)
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# Define your dictionary
data = recent_data

# Convert timestamps to datetime objects
timestamps = [datetime.fromtimestamp(int(ts)) for ts in data.keys()]

# Get values from dictionary
values = list(data.values())

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the values against timestamps
ax.plot(timestamps, values)

# Set x-axis format to show date and time
plt.xticks(rotation=45, ha='right', fontsize=5)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

# Add labels and title
ax.set_xlabel('Timestamp')
ax.set_ylabel('Value')
ax.set_title('Plot of values over time')

# Show the plot
plt.show()
os._exit(0)
