import tweepy, time, requests
from bs4 import BeautifulSoup

APP_KEY = ""
APP_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""

POST_TIME = "09:00:00" # 9AM local time

def get_time():
    return time.strftime("%H:%M:%S")

def get_case_number():
    r = requests.get("https://lsu.edu/roadmap/")
    soup = BeautifulSoup(r.text, "html.parser")
    tag = soup.find(string="Positive Test Results")
    parent = tag.parent.parent.find_all("p")
    casenum = int(parent[2].contents[1].string)
    return casenum

def get_prev_number():
    f = open("lsu_coronavirus_data.csv", "r")
    while True:
        tmpline = f.readline()
        if not tmpline:
            break
        line = tmpline
    f.close()
    return int(line.split(",")[1])

def save(date, casenum, dailychange):
    with open("lsu_coronavirus_data.csv", "a") as f:
        f.write(f"{date}, {casenum}, {dailychange}\n")
        
def post(date, casenum, dailychange):
    tweet = f"Yesterday, LSU confirmed {dailychange} new cases of COVID-19. The total number of confirmed cases is now {casenum}. lsu.edu/roadmap"
    api.update_status(tweet)
    print(date, get_time(), "i tweeted successfully.")

def main():
    date = time.strftime(r"%d/%m/%Y")
    casenum = get_case_number()
    prevnum = get_prev_number()
    dailychange = casenum - prevnum
    save(date, casenum, dailychange)
    post(date, casenum, dailychange)

# authenticate
auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
print("Successfully authenticated.")

# main loop
while True:
    while get_time() != POST_TIME:
        time.sleep(0.1)
    main()
    while get_time() == POST_TIME:
        time.sleep(0.1)
