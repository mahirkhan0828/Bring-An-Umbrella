import requests
from bs4 import BeautifulSoup
import smtplib
import time

# This program uses weather.com to send daily umbrella updates on a chosen gmail. 
# It is currently set to Houston, Texas as the area and a Mac apple device for the user agent. 
# Both of these can be easily changed by altering the URL and headers objects below. 

# Start this program at the exact time you wish to get your daily updates.

# This URL is for Houston, Texas Weather Updates. For this program to work on other areas, insert the 
# URL of that area on weather.com
URL = "https://weather.com/weather/today/l/110a124808308e4fc03ee2b75754a7e06e9334b6d23d6fa317f1bb84b5f8a65e"

sending_email = "umbrella.updates@gmail.com"
mail_password = "muaafqsnxirscdpx"

#recieving_email = str(input("Please enter your gmail: "))
recieving_email = 'mahirkhan0828@gmail.com'
# This user agent is specific to the device used. To find your specific user agent, search up "My
# User Agent in searchbar"
headers = {
     "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}

def check_rain(weather_url):
    page = requests.get(weather_url, headers = headers)

    soup = BeautifulSoup(page.content,"html.parser")
    
    rain_chance_perc = soup.find("span", {"class" : "precip-val"}).get_text()
    rain_chance_num = float(rain_chance_perc.split("%")[0])
    
    return rain_chance_num

def send_mail(rain_chance_num):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sending_email, mail_password)

    umbrella = ""
    if rain_chance_num <= 20:
        umbrella = "Probably will not need umbrella :)"
    elif  20 < rain_chance_num <= 50:
        umbrella = "Let's bring an umbrella just to be safe!"
    elif 50 < rain_chance_num <= 70:
        umbrella = "You should probably take an umbrella unless you're feeling very lucky!"
    elif 70 < rain_chance_num <= 100:
        umbrella = "Take an umbrella!!!"
    
    subject = "Do we need an Umbrella?"
    body = "The chance that it will rain today is {}%. {}\nClick on this link to check for a more in depth weather analysis: {}".format(rain_chance_num,umbrella,URL)

    message = "Subject: {}\n\n\n{}".format(subject,body)
    server.sendmail(
        sending_email,
        recieving_email,
        message
    )

    print("Email has been sent!")
    server.quit()

#check once a day for updates
while (True):
    send_mail(check_rain(URL))
    time.sleep(60*60*24)
