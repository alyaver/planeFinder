import tkinter as tk
import os, sys
import time
import requests
import datetime

url = "https://api.airplanes.live/v2/point/37.619506/-122.374212/5"


cleanedData = []


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


root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.configure(background='black')

root.geometry("%dx%d+0+0" % (w, h))
root.title("Planes")

header = tk.Frame(root)
header.configure(background='black')

mainFrame = tk.Frame(root)
mainFrame.configure(background='black')

#create the flight cards, i = 3 so 3 cards will be created
for i in cleanedData:
     card = tk.Frame(mainFrame)
     flightLabel = tk.Label(card, text=i["flight"], font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
     flightLabel.pack()
     latLabel = tk.Label(card, text=i["lat"], font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
     latLabel.pack()
     longLabel = tk.Label(card, text=i["lon"], font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
     longLabel.pack()
     distLabel = tk.Label(card, text=i["dst"], font=('Arial', 18), bg = '#000000', fg='#ffffff', background='#000000' )
     distLabel.pack()
     card.configure(background='black')
     card.pack(pady=50)

#label for the time
time_label = tk.Label(header, text="", font=('Arial', 24), bg = '#000000', fg='#ffffff', highlightbackground='#000000' )
time_label.pack(padx=(0, 50), pady=50, side="right")
#label for the title
title_label = tk.Label(header, text="\tFlights in Bound\t", font=('Arial', 32), bg = '#000000', fg='#ffffff', highlightbackground='#000000' )
title_label.pack(padx=0, pady=50, side="top")

header.pack(fill='x')
mainFrame.pack()


update_time()
root.mainloop()