import requests
import os

os.chdir(r"C:\users\jamfw\tmo")
url = input("\n\nEnter the full URL to test (include http:// or https:// as part of the URL): ")
#url = r"http://did.ijinshan.com/db/?v=2&p=db&u=d610e9e5b388ee40d220d4e1f73c4772&m=847beb0f419e0000&ip=167857930&s=bd2d0da6a8a3c04f4b4f697b33c88cc9"
timer = 10
r1 = False

count_no_response = 0
count_matches = 0
count_different_result = 0
count_number_of_agents = 0

print("\n\nThe URL being tested is: " + url)
print("\nTesting the URL with no user agent string (baseline test)...")

# Set the baseline
try:
    r1 = requests.get(url, verify=False, timeout = timer)
    print(r1.text + "\n---------------------------------------------\n\n")
except requests.exceptions.ConnectionError:
    print("[!] Time-Out on this one \n--------------------------------------------- \n\n")
except requests.exceptions.ReadTimeout:
    print("[!] Time-Out on this one \n--------------------------------------------- \n\n")

if r1 is False:
    print("[!] The baseline did not have a valid response, exiting...")
    print("[i] Usually this means a timeout was reached or just no response at all.\n\n")
    exit()

# Try each user-agent string
with open("agents.txt") as agents:
    for each in agents:
        count_number_of_agents += 1
        header = { 'User-Agent' : str(each.strip())}
        print("User Agent Testing: " + str(each.strip()))
        r2 = False
        try:
            r2 = requests.get(url, headers = header, verify=False, timeout = timer)
            #print(r2.text + "\n---------------------------------------------")
        except requests.exceptions.ConnectionError:
            count_no_response += 1
            print("[!] Time-Out on this one \n--------------------------------------------- \n\n")
            continue
        except requests.exceptions.ReadTimeout:
            count_no_response += 1
            print("[!] Time-Out on this one \n--------------------------------------------- \n\n")
            continue

        if r2 == False:
            print("[i] No response on this one, moving on... \n--------------------------------------------- \n\n")
            count_no_response += 1
            break
        elif r1.text == r2.text:
            print("[i] This matches the baseline, moving on.... \n--------------------------------------------- \n\n")
            count_matches += 1
        else:
            count_different_result += 1
            print("[*] This response is different from the baseline (Difference " + str(count_different_result) + "):  \n\n --------------------------------------------- \n" + r2.text + "\n--------------------------------------------- \n\n")
            print(r2.text + "\n--------------------------------------------- \n\n")


print("\n\n ----------------   Report ----------------\n\n")
print("Number of agents tried: " + str(count_number_of_agents))
print("Number of timeouts: " + str(count_no_response))
print("Number of same responses: " + str(count_matches))
print("Number of different responses: " + str(count_different_result))
print("\n----------------------------------------\n\n")
