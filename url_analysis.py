# Set the imports
from tkinter import *
from tkinter import filedialog
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time

# Disable warnings about insecure SSL requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Initialize variables
url = "http://"
agents_file = None
timer = 10
r1 = False
r2 = False
count_no_response = 0
count_matches = 0
count_different_result = 0
count_number_of_agents = 0


# Define the main window

interface = Tk()
interface.geometry('800x600')
# These lines may not be needed
Grid.rowconfigure(interface, 6, weight=1)
Grid.columnconfigure(interface, 1, weight=1)
#interface.grid_columnconfigure(0, weight=1)
#interface.grid_rowconfigure(0, weight=1)

#Create & Configure frame
frame=Frame(interface)
frame.grid(row=0, column=0, sticky=N+S+E+W)


def openfile():
    global agents_file

    agents_file = filedialog.askopenfilename()
    output_text = "\nAgents file to use: " + agents_file
    output.insert(END, output_text)

    return agents_file

def seturl():
    global url

    url = enter_url.get()
    output_text = "\nURL in function: " + url
    output.insert(END, output_text)

    return url

def starttest():
    global url
    global r1
    global r2
    global count_different_result
    global count_no_response
    global count_number_of_agents
    global count_matches
    global timer

    if url == None:
        output.insert(END, "Hey, set the dang url!")
    elif agents_file == None:
        output.insert(END, "Hey, set the frickin' agents file!")
    else:
        output.insert(END,"\nStarting the test...")
        output.update_idletasks()
        output.insert(END, "\n\nTrying the URL....")
        output.update_idletasks()
        try:
            output.insert(END, "\nSetting baseline with no user-agent set....\n")
            output.update_idletasks()
            r1 = requests.get(url, verify=False, timeout=timer)
            textoutput = ("\n------------ The Baseline Response ------------\n" + r1.text + "\n---------------------------------------------\n\n\n\n")
            output.insert(END, textoutput)
            output.update_idletasks()
        except requests.exceptions.ConnectionError:
            count_no_response += 1
            output.insert(END, "[!] Time-Out on this one \n--------------------------------------------- \n\n")
            output.update_idletasks()
        except requests.exceptions.ReadTimeout:
            count_no_response += 1
            output.insert(END,"[!] Time-Out on this one \n--------------------------------------------- \n\n")
            output.update_idletasks()
        except requests.exceptions.MissingSchema:
            output.insert(END, "You forgot to set the URL!!!")
            output.update_idletasks()
        except requests.exceptions.InvalidURL:
            output.insert(END, "You forgot to set the URL!!!")
            output.update_idletasks()

        if r1 is False:
            output.insert(END,"\n[!] The baseline did not have a valid response, exiting...")
            output.insert(END,"\n[i] Usually this means a timeout was reached or just no response at all.\n\n")
            output.insert(END,"[i] Close the window to exit.")
            output.update_idletasks()
            output.see("end")
            time.sleep(10000)
            exit()

        with open(agents_file) as agents:
            for each in agents:
                count_number_of_agents += 1
                header = {'User-Agent': str(each.strip())}
                output.insert(END,"User Agent Testing: " + str(each.strip()))
                output.update_idletasks()
                output.see("end")
                r2 = False

                try:
                    r2 = requests.get(url, headers=header, verify=False, timeout=timer)
                    # print(r2.text + "\n---------------------------------------------")
                except requests.exceptions.ConnectionError:
                    count_no_response += 1
                    output.insert(END, "[!] Time-Out on this one \n--------------------------------------------- \n\n")
                    output.update_idletasks()
                    output.see("end")
                    continue
                except requests.exceptions.ReadTimeout:
                    count_no_response += 1
                    output.insert(END,"[!] Time-Out on this one \n--------------------------------------------- \n\n")
                    output.update_idletasks()
                    output.see("end")
                    continue

                if r2 == False:
                    output.insert(END,"[i] No response on this one, moving on... \n--------------------------------------------- \n\n")
                    output.update_idletasks()
                    output.see("end")
                    count_no_response += 1
                    break
                elif r1.text == r2.text:
                    output.insert(END,"[i] This matches the baseline, moving on.... \n--------------------------------------------- \n\n")
                    output.update_idletasks()
                    output.see("end")
                    count_matches += 1
                else:
                    count_different_result += 1
                    newresult = "[*] This response is different from the baseline (Difference " + str(count_different_result) + "):  \n\n --------------------------------------------- \n" + r2.text + "\n--------------------------------------------- \n\n"
                    output.insert(END, newresult)
                    output.update_idletasks()
                    output.see("end")
                    #output.insert(END, "\n--------------------------------------------- \n\n")


    output.insert(END,"\n\n ----------------   Report ----------------\n")
    numagents = "\nNumber of agents tried: " + str(count_number_of_agents)
    output.insert(END, numagents)
    numtimeouts = "\nNumber of timeouts: " + str(count_no_response)
    output.insert(END, numtimeouts)
    numsame = "\nNumber of same responses: " + str(count_matches)
    output.insert(END, numsame)
    numdiff = "\nNumber of different responses: " + str(count_different_result)
    output.insert(END, numdiff)
    output.insert(END,"\n----------------------------------------\n\n")
    output.see("end")
    output.update_idletasks()


enter_url = Entry(interface)
#enter_url.pack(side=TOP)
enter_url.grid(row=0, column=1, sticky=S+E+W, padx=200)
button2 = Button(interface, text="Set URL", command = seturl)
button2.grid(row=1, column=1)

button1 = Button(interface, text="Open User-Agents File", command=openfile)
button1.grid(row=2, column=1)

button3 = Button(interface, text="START TEST", command=starttest)
button3.grid(row=4, column=1, sticky=E+W)


output = Text(master=interface)

#output.pack(side=BOTTOM, expand=YES, fill=BOTH)
output.columnconfigure(1, weight=2, pad=20)
output.rowconfigure(6, weight=3, pad=20)
output.grid(row=6, column=1, sticky=N+S+E+W)
scrollbar = Scrollbar(output)
scrollbar.grid(row=6, column=2, sticky=N+S)
output.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output.yview)

interface.mainloop()

