import urllib.request
import re

url = "https://raw.githubusercontent.com/jnk22/kodinerds-iptv/master/iptv/kodi/kodi_tv.m3u"
tv_programs = [
    "ARD.de",
    "ZDF.de",
    "3sat.de",
    "ARTE.de",
    "ServusHD.de",
    "ARD-alpha.de",
    "One.de",
    "ZDFneo.de",
    "ZDFinfo.de",
    "Kika.de",
    "tagesschau24.de",
    "n24.de",
    "phoenix.de",
    "WDR.de",
    "SWR.de",
    "SWR-rp.de",
    "ndr.de",
    "BR.de",
    "MDRSachsen.de",
    "MDRS-Anhalt.de",
    "MDRThuringen.de",
    "HR.de",
    "rbbBerlin.de",
    "rbbBrandenburg.de",
    "SRFernsehen.de",
    "DeutscheWelleDE.de",
    "DeutscheWelleEN.de"
]

group_title = "Vollprogramm"


def load_iptv_list(list_url):
    data = urllib.request.urlopen(list_url).read().decode("utf-8")
    print("   [List loaded]")
    return data


def save_to_file(list):
    list_as_string = "\n".join(list)
    with open("iptv.m3u", "w") as text_file:
        text_file.write(list_as_string)
    print("   [File iptv.m3u saved]")
    
def parse_list(data):
    lines = data.split("\n")
    list = ["#EXTM3U"]
    add_next_line = False

    for line in lines:
        # one entry consists of two lines
        if add_next_line:
            list.append(line)
            add_next_line = False
            continue

        # iterate over tv programs and check availability
        for program in tv_programs:
            if program in line:
                list.append(line)
                add_next_line = True
                break
    print("   [Favorite channels parsed]")
    return list


def unify_group_title(list):
    regex_search = r"group-title=\"(.+?)\""
    replace_value = f"group-title=\"{group_title}\""
    unified_list = []

    for entry in list:
        # filter first entry and url entries
        if entry.find("group-title") == -1:
            unified_list.append(entry)
            continue

        # replace group-title value
        unified_entry = re.sub(regex_search, replace_value, entry)
        unified_list.append(unified_entry)
    print("   [Group titles unified]")
    return unified_list


# load the list from the provided URL
print("1) Loading IPTV list from Url...")
data = load_iptv_list(url)

# parse the loaded list
print("2) Find favorite channels...")
parsed_list = parse_list(data)

# change group-title
print("3) Add channels to same program list...")
result = unify_group_title(parsed_list)


# save the parsed list to file
print("4) Save new channel list...")
save_to_file(result)
