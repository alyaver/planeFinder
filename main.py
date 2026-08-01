import tkinter as tk
import os, sys
import time
import requests
import datetime

url = "https://api.airplanes.live/v2/point/38.90875638071712/-121.5406827689271/50"

cleanedData = []
frames = []

def update_data():
    try:
        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()
            sortedData = (sorted(data["ac"], key=lambda x: x["dst"]))

            counter = 0
            for x in sortedData:
                tempData = {}
                check = x.get("flight")
                if not check:
                    continue
                tempData["flight"] = (x.get("flight")).strip()
                tempData["lat"] = (x.get("lat"))
                tempData["lon"] = (x.get("lon"))
                tempData["dst"] = (x.get("dst"))
                cleanedData.append(tempData)
                counter = counter + 1
                if counter == 3:
                    break

            print("Success")
            print(cleanedData)
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
    cleanedData.clear()
    update_data()
    count = 0
    for j in cleanedData:
        frames[count]["flight"].config(text=j["flight"])
        frames[count]["lat"].config(text=j["lat"])
        frames[count]["lon"].config(text=j["lon"])
        frames[count]["dst"].config(text=j["dst"])
        count = count + 1

    root.after(5000, refresh)

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
    flightLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
    flightLabel.pack()
    latLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
    latLabel.pack()
    longLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
    longLabel.pack()
    distLabel = tk.Label(card, text="", font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
    distLabel.pack()
    card.configure(background='black')
    card.pack(pady=50)
    tempData["flight"] = flightLabel
    tempData["lat"] = latLabel
    tempData["lon"] = longLabel
    tempData["dst"] = distLabel
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