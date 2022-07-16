import json
import requests
from bs4 import BeautifulSoup

#https://gist.github.com/bcahue/4eae86ae1d10364bb66d thanks for ur code Blair Cahue, helped me a lot :P
steamid64ident = 76561197960265728

settings = json.load(open("settings.json"))

split_sid_start = settings["steamid_start"].split(":")
split_sid_end = settings["steamid_end"].split(":")

def get_username(steamid64):
    sc_request = requests.get("https://steamcommunity.com/profiles/" + steamid64).text
    soup = BeautifulSoup(sc_request, "html.parser")

    username = soup.find("div", {"class": "persona_name"}).get_text().split().pop(0)

    return username

def check_profile(steamid64):
    sc_request = requests.get("https://steamcommunity.com/profiles/" + steamid64).text
    soup = BeautifulSoup(sc_request, "html.parser")

    check_div = soup.find("div", {"class": "profile_private_info"}).get_text().split("\n")
    check_fix_spacing = [l.replace("\t", "") for l in check_div]
    check = check_fix_spacing.pop(1)

    return check

def log_output(username, steamid, steamid64):
    if middle_shit == 1: #probably the worst way of checking this shit lmao
        with open("output.txt", "a") as output:
            output.write(uname + "\n")
            output.write("STEAM_0:1:" + steamid + "\n")
            output.write("https://steamcommunity.com/profiles/" + steamid64 + "\n")
            output.write("\n")
    else:
        with open("output.txt", "a") as output:
            output.write(uname + "\n")
            output.write("STEAM_0:0:" + steamid + "\n")
            output.write("https://steamcommunity.com/profiles/" + steamid64 + "\n")
            output.write("\n")

for i in range(int(split_sid_start[2]), (int(split_sid_end[2]) + 1)):
    print("Checking STEAM_0:0:" + str(i), "...")
    middle_shit = 0
    convert_to_64 = i * 2
    convert_to_64 += steamid64ident

    try:
        if "This user has not yet set up their Steam Community profile." in check_profile(str(convert_to_64)):
            uname = get_username(str(convert_to_64))
            print("Found account:", uname)
            log_output(uname, str(i), str(convert_to_64))
    except:
        pass

    print("Checking STEAM_0:1:" + str(i), "...")
    middle_shit = 1
    convert_to_64_1 = (i * 2) + 1
    convert_to_64_1 += steamid64ident

    try:
        if "This user has not yet set up their Steam Community profile." in check_profile(str(convert_to_64_1)):
            uname = get_username(str(convert_to_64_1))
            print("Found account:", uname)
            log_output(uname, str(i), str(convert_to_64_1))
    except:
        pass

print("\nDone.")