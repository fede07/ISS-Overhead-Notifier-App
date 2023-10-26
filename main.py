import smtplib
import time
import requests
from datetime import datetime

MY_LAT = -39.603950 # Your latitude
MY_LONG = -58.381666 # Your longitude

my_email = "dummy@gmail.com"
password = "testingpass"

def iss_in_range():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(iss_latitude)
    print(iss_longitude)
    in_range = False

    #Your position is within +5 or -5 degrees of the ISS position.
    if int(MY_LAT) in range(int(iss_latitude)-5, int(iss_latitude)+5):
        print("YES!")
        in_range = True
    return in_range

def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour = time_now.hour

    is_dark = False

    if hour < sunrise or hour > sunset:
        is_dark = True

    return is_dark

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

while True:
    time.sleep(60)
    if iss_in_range() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="dummy2@gmail.com",
                msg="Subject:LOOK UP!\n\nThe ISS is here!"
            )

