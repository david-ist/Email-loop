import requests
import time
import os
import random
import tkinter as tk
import tkinter.messagebox

root = tk.Tk(className="Email loop app")

#Create an initial connection towards CIC.
def connection():
    global server
    global proxy
    server = server_entry.get()
    proxy = proxy_entry.get()
    username = usern_entry.get()
    pwd = pwd_entry.get()
    url = (proxy + server + '/icws/connection')
    body = {"__type":"urn:inin.com:connection:icAuthConnectionRequestSettings",
        "applicationName":"Email loop app",
        "userID": username,
        "password": pwd} 
    try:
        connection = requests.post(url, json = body, headers = {"Accept-Language": "en-us"})
    except requests.exceptions.Timeout:
        text_box.insert("1.0", "Timeout during server connection"  + "\n")
    except requests.exceptions.TooManyRedirects:
        text_box.insert("1.0", "Too many redirects"  + "\n")
    except requests.exceptions.MissingSchema:
        text_box.insert("1.0", "Not all the necessery information is filled out!"  + "\n")
    except requests.exceptions.ConnectionError:
        text_box.insert("1.0", F"Failed to establish a new connection to {proxy}"  + "\n")
    else:
        if connection.status_code >= 200 and  connection.status_code <= 299:
            jsonresult=connection.json()
            global sessionID
            sessionID = jsonresult['sessionId']
            text_box.insert("1.0", F"Session was created on {server} with sessionID : {sessionID} \n")
            global token
            token = jsonresult['csrfToken']
            global cookie
            cookie = connection.cookies.get_dict()
            root.after(2,createemail)
        else:
            text_box.insert("1.0", "An error occurred. Error details: \n" + connection.text + "\n")

# Start creating e-mail interactions depending on the timeout specified. 
def createemail():   
    timeo = int(timeo_entry.get()) * 1000 
    wg = wg_entry.get()
    email = email_entry.get()
    url = (proxy + server + F'/icws/{sessionID}/interactions')
    body = {"emailContent":
            {"sender":
            {"displayName":"Test e-mail","address":F"{email}"},
            "bodies":[{"body":"​Example e-mail body","bodyType":0},{"body":"<html><body><div></div></body></html>",
            "bodyType":1}],
            "__type":"urn:inin.com:interactions.email:emailContent"},
            "workgroup":F"{wg}", "__type":"urn:inin.com:interactions.email:createEmailParameters"}
    connection = requests.post(url, json = body, headers = {"ININ-ICWS-CSRF-Token" : token}, cookies = cookie)
    if connection.status_code >= 200 and  connection.status_code <= 299:
        jsonresult=connection.json()
        interactionID = jsonresult['interactionId']
        text_box.insert("2.0", "Created new interaction {} \n".format(interactionID))
        root.after(timeo,createEMAIL)
    else:
        text_box.insert("1.0", "An error occurred. Error details: \n" + connection.text + "\n")
        
# Exit the application function
def exitAPP():
    result = tk.messagebox.askquestion("Exit", "Are You Sure?", icon='warning')
    if result == 'yes':
        exit()
    else:
        pass

# Tkinter design below
frame = tk.Frame(root, width = 50, height = 160)
frame.grid(column = 0, row = 0)

proxy_label = tk.Label(master = frame, text = "Proxy (<proxy url>/)")
proxy_label.grid(column = 0, row = 0, sticky="N")

proxy_entry = tk.Entry(master = frame, width = 35)
proxy_entry.grid(column = 0, row = 1, sticky="W", padx = 50)
proxy = tk.Entry(master=proxy_entry)

server_label = tk.Label(master = frame, text = "Server (<servername>:<port>)")
server_label.grid(column = 0, row = 2, sticky="N")

server_entry = tk.Entry(master = frame, width = 35)
server_entry.grid(column = 0, row = 3, sticky="W", padx = 50)
server = tk.Entry(master=server_entry)

usern_label = tk.Label(master = frame, text = "CIC username")
usern_label.grid(column = 0, row = 4, sticky="N")

usern_entry = tk.Entry(master = frame, width = 35)
usern_entry.grid(column = 0, row = 5, sticky="W", padx = 50)
username = tk.Entry(master=usern_entry)

pwd_label = tk.Label(master = frame, text = "CIC password")
pwd_label.grid(column = 0, row = 6, sticky="N")

pwd_entry = tk.Entry(master = frame, width = 35, show = "*")
pwd_entry.grid(column = 0, row = 7, sticky="W", padx = 50)
pwd = tk.Entry(master=pwd_entry)

timeo_label = tk.Label(master = frame, text = "Timeout (s)")
timeo_label.grid(column = 1, row = 0, sticky="N")

timeo_entry = tk.Entry(master = frame, width = 35)
timeo_entry.grid(column = 1, row = 1, sticky="W", padx = 50)
timeo = tk.Entry(master=timeo_entry)

wg_label = tk.Label(master = frame, text = "Workgroup")
wg_label.grid(column = 1, row = 2, sticky="N")

wg_entry = tk.Entry(master = frame, width = 35)
wg_entry.grid(column = 1, row = 3, sticky="W", padx = 50)
wg = tk.Entry(master=wg_entry)

email_label = tk.Label(master = frame, text = "Email address")
email_label.grid(column = 1, row = 4, sticky="N")

email_entry = tk.Entry(master = frame, width = 35)
email_entry.grid(column = 1, row = 5, sticky="W", padx = 50)
email = tk.Entry(master=email_entry)

button = tk.Button(master=frame, text="OK", command=connection, width = 20)
button.grid(column = 0, row = 9, sticky="E")

button_exit = tk.Button(master=frame, text="EXIT", command=exitAPP, width = 20)
button_exit.grid(column = 1, row = 9, sticky="W", pady = 30)

text_box = tk.Text()
text_box.grid(column = 0, row = 11, sticky="W", pady = 30)

root.mainloop()
