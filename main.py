import tkinter as tk
import time
import requests
import os 
from dotenv import load_dotenv

#https://api.airplanes.live/v2/point/lat/lon/radius
airplanesUrl = "https://api.airplanes.live/v2/point/38.727929544614305/-121.145174979809/50"
geoUrl = "https://api.geoapify.com/v1/geocode/reverse"

cleanedPlaneData = []
planeHistory = {}
frames = []

load_dotenv()
geoKey = os.getenv("GEOAPIFY_API_KEY")

def update_data():
    try:
        response = requests.get(airplanesUrl)

        if response.status_code == 200:

            data = response.json()
            print(data)
            sortedData = (sorted(data["ac"], key=lambda x: x["dst"]))

            counter = 0
            for x in sortedData:
                tempData = {}
                check = x.get("flight")
                if not check:
                    continue
                #make sure that only planes in air are showing up
                if x.get("alt_baro") == "ground" or int(x.get("alt_baro")) < 200:
                    continue
                #get the 'tail number' and strip any spaces
                tempData["flight"] = (x.get("flight")).strip()
                tempData["lat"] = (x.get("lat"))
                tempData["lon"] = (x.get("lon"))
                tempData["dst"] = (x.get("dst"))
                tempData["desc"] = (x.get("desc") or x.get("t") or "Unknown Aircraft")

                planeHex = x.get("hex")
                planeLocation = {}
                if planeHistory.get(planeHex):
                    planeLocation = planeHistory[planeHex]

                else:
                    planeLocation = coordToCity(x.get("lat"), x.get("lon"))
                    planeHistory[planeHex] = planeLocation

                tempData["location"] = planeLocation

                cleanedPlaneData.append(tempData)
                counter = counter + 1

                if counter == 3:
                    break

            print("Success")
            print(cleanedPlaneData)
        else:
            print(f"Fail: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")

    
#check to see if time has updated
def update_time():
        current_time = time.strftime("%H:%M")
        time_label.config(text=current_time)
        root.after(1000, update_time)  

def refresh():
    cleanedPlaneData.clear()
    update_data()
    count = 0
    for j in cleanedPlaneData:
        frames[count]["flight"].config(text=j["flight"])
        frames[count]["lat"].config(text=j["lat"])
        frames[count]["lon"].config(text=j["lon"])
        frames[count]["dst"].config(text=j["dst"])
        frames[count]["desc"].config(text=j["desc"])

        location = j["location"]

        city = location.get("city")
        county = location.get("county")
        state = location.get("state")
        state_code = location.get("state_code")
        country = location.get("country")
        country_code = location.get("country_code")

        displayLocation = "Unknown Location"

        if city:
            if state_code:
                displayLocation = city, state_code
            elif state:
                displayLocation = city, state
        elif state:
            if country_code:
                displayLocation = state, country
            elif country_code:
                displayLocation = state, country_code
        elif county:
            
        count = count + 1

    root.after(5000, refresh)

def coordToCity(lat, lon):
    paramsDic = {}
    paramsDic["lat"] = lat
    paramsDic["lon"] = lon
    paramsDic["apiKey"] = geoKey

    fallbackLocation = {
    "country_code": None,
    "country": None,
    "state_code": None,
    "state": None,
    "county": None,
    "city": None,
    "postcode": None
}

    try: 
        response = requests.get(geoUrl, params=paramsDic)

        if response.status_code == 200:

            data = response.json()
            features = data.get("features") or []

            if features:
                properties = features[0].get("properties") or {}

            else:
                return fallbackLocation

            tempLocData = {}
            tempLocData["country_code"] = properties.get("country_code")
            tempLocData["country"] = properties.get("country")
            tempLocData["state_code"] = properties.get("state_code")
            tempLocData["state"] = properties.get("state")
            tempLocData["county"] = properties.get("county")
            tempLocData["city"] = properties.get("city")
            tempLocData["postcode"] = properties.get("postcode")
            return tempLocData
        else:
            print(response.status_code)
            return fallbackLocation

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
        return fallbackLocation



root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.configure(background='black')

root.geometry("%dx%d+0+0" % (w, h))
root.title("Planes")

header = tk.Frame(root)
header.configure(background='black')

mainFrame = tk.Frame(root)
mainFrame.configure(background='black')

#create the flight cards, 3 cards will be created
for i in range(0, 3):
    tempData = {}
    card = tk.Frame(mainFrame)
    flightLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff')
    flightLabel.pack()
    latLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff')
    latLabel.pack()
    longLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff')
    longLabel.pack()
    distLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff')
    distLabel.pack()
    locationLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff')
    locationLabel.pack()
    typeLabel = tk.Label(card, text = "", font=('Arial', 18), bg = '#000000', fg='#ffffff')
    typeLabel.pack()
    card.configure(background='black')
    card.pack(pady=50)
    tempData["flight"] = flightLabel
    tempData["lat"] = latLabel
    tempData["lon"] = longLabel
    tempData["dst"] = distLabel
    tempData["location"] = locationLabel
    tempData["desc"] = typeLabel
    frames.append(tempData)
    
#label for the time
time_label = tk.Label(header, text="", font=('Arial', 24), bg = '#000000', fg='#ffffff', highlightbackground='#000000' )
time_label.pack(padx=(0, 50), pady=50, side="right")
#label for the title
title_label = tk.Label(header, text="\tFlights in Bound\t", font=('Arial', 32), bg = '#000000', fg='#ffffff', highlightbackground='#000000' )
title_label.pack(padx=0, pady=50, side="top")

header.pack(fill='x')
mainFrame.pack()

update_time()
refresh()
root.mainloop()