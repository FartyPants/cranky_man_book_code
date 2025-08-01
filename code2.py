import requests
from bs4 import BeautifulSoup
import re

# List of Wikipedia novel links
novel_links = [
    "https://en.wikipedia.org/wiki/Nineteen_Eighty-Four",
    "https://en.wikipedia.org/wiki/Earth_Abides",
    "https://en.wikipedia.org/wiki/The_Martian_Chronicles",
    "https://en.wikipedia.org/wiki/The_Puppet_Masters",
    "https://en.wikipedia.org/wiki/The_Day_of_the_Triffids",
    "https://en.wikipedia.org/wiki/The_Demolished_Man",
    "https://en.wikipedia.org/wiki/Fahrenheit_451",
    "https://en.wikipedia.org/wiki/Childhood%27s_End",
    "https://en.wikipedia.org/wiki/The_Paradox_Men",
    "https://en.wikipedia.org/wiki/Bring_the_Jubilee",
    "https://en.wikipedia.org/wiki/The_Space_Merchants",
    "https://en.wikipedia.org/wiki/Ring_Around_the_Sun_(novel)",
    "https://en.wikipedia.org/wiki/More_Than_Human",
    "https://en.wikipedia.org/wiki/Mission_of_Gravity",
    "https://en.wikipedia.org/wiki/A_Mirror_for_Observers",
    "https://en.wikipedia.org/wiki/The_End_of_Eternity",
    "https://en.wikipedia.org/wiki/The_Long_Tomorrow_(novel)",
    "https://en.wikipedia.org/wiki/The_Inheritors_(William_Golding)",
    "https://en.wikipedia.org/wiki/The_Stars_My_Destination",
    "https://en.wikipedia.org/wiki/The_Death_of_Grass",
    "https://en.wikipedia.org/wiki/The_City_and_the_Stars",
    "https://en.wikipedia.org/wiki/The_Door_into_Summer",
    "https://en.wikipedia.org/wiki/The_Midwich_Cuckoos",
    "https://en.wikipedia.org/wiki/Non-Stop_(novel)",
    "https://en.wikipedia.org/wiki/A_Case_of_Conscience",
    "https://en.wikipedia.org/wiki/Have_Space_Suit%E2%80%94Will_Travel",
    "https://en.wikipedia.org/wiki/Time_Out_of_Joint",
    "https://en.wikipedia.org/wiki/Alas,_Babylon",
    "https://en.wikipedia.org/wiki/A_Canticle_for_Leibowitz",
    "https://en.wikipedia.org/wiki/The_Sirens_of_Titan",
    "https://en.wikipedia.org/wiki/Rogue_Moon",
    "https://en.wikipedia.org/wiki/Venus_Plus_X",
    "https://en.wikipedia.org/wiki/Hothouse_(novel)",
    "https://en.wikipedia.org/wiki/The_Drowned_World",
    "https://en.wikipedia.org/wiki/A_Clockwork_Orange_(novel)",
    "https://en.wikipedia.org/wiki/The_Man_in_the_High_Castle",
    "https://en.wikipedia.org/wiki/Journey_Beyond_Tomorrow",
    "https://en.wikipedia.org/wiki/Way_Station_(novel)",
    "https://en.wikipedia.org/wiki/Cat%27s_Cradle",
    "https://en.wikipedia.org/wiki/Greybeard",
    "https://en.wikipedia.org/wiki/Nova_Express",
    "https://en.wikipedia.org/wiki/Martian_Time-Slip",
    "https://en.wikipedia.org/wiki/The_Three_Stigmata_of_Palmer_Eldritch",
    "https://en.wikipedia.org/wiki/The_Wanderer_(Fritz_Leiber_novel)",
    "https://en.wikipedia.org/wiki/Norstrilia",
    "https://en.wikipedia.org/wiki/Dr._Bloodmoney",
    "https://en.wikipedia.org/wiki/Dune_(novel)",
    "https://en.wikipedia.org/wiki/The_Crystal_World",
    "https://en.wikipedia.org/wiki/Make_Room!_Make_Room!",
    "https://en.wikipedia.org/wiki/Flowers_for_Algernon",
    "https://en.wikipedia.org/wiki/The_Dream_Master",
    "https://en.wikipedia.org/wiki/Stand_on_Zanzibar",
    "https://en.wikipedia.org/wiki/Nova_(novel)",
    "https://en.wikipedia.org/wiki/Do_Androids_Dream_of_Electric_Sheep%3F",
    "https://en.wikipedia.org/wiki/Camp_Concentration",
    "https://en.wikipedia.org/wiki/The_Final_Programme",
    "https://en.wikipedia.org/wiki/Pavane_(novel)",
    "https://en.wikipedia.org/wiki/Heroes_and_Villains_(novel)",
    "https://en.wikipedia.org/wiki/The_Left_Hand_of_Darkness",
    "https://en.wikipedia.org/wiki/Bug_Jack_Barron",
    "https://en.wikipedia.org/wiki/Tau_Zero",
    "https://en.wikipedia.org/wiki/Downward_to_the_Earth",
    "https://en.wikipedia.org/wiki/The_Year_of_the_Quiet_Sun",
    "https://en.wikipedia.org/wiki/334_(novel)",
    "https://en.wikipedia.org/wiki/The_Fifth_Head_of_Cerberus",
    "https://en.wikipedia.org/wiki/The_Dancers_at_the_End_of_Time",
    "https://en.wikipedia.org/wiki/Crash_(J._G._Ballard_novel)",
    "https://en.wikipedia.org/wiki/Walk_to_the_End_of_the_World",
    "https://en.wikipedia.org/wiki/The_Centauri_Device",
    "https://en.wikipedia.org/wiki/The_Dispossessed",
    "https://en.wikipedia.org/wiki/Inverted_World",
    "https://en.wikipedia.org/wiki/High-Rise_(novel)",
    "https://en.wikipedia.org/wiki/Galaxies_(novel)",
    "https://en.wikipedia.org/wiki/The_Female_Man",
    "https://en.wikipedia.org/wiki/Orbitsville",
    "https://en.wikipedia.org/wiki/The_Alteration",
    "https://en.wikipedia.org/wiki/Woman_on_the_Edge_of_Time",
    "https://en.wikipedia.org/wiki/Man_Plus",
    "https://en.wikipedia.org/wiki/Michaelmas_(novel)",
    "https://en.wikipedia.org/wiki/The_Ophiuchi_Hotline",
    "https://en.wikipedia.org/wiki/Engine_Summer",
    "https://en.wikipedia.org/wiki/On_Wings_of_Song_(novel)",
    "https://en.wikipedia.org/wiki/Timescape",
    "https://en.wikipedia.org/wiki/Wild_Seed_(Octavia_Butler_novel)",
    "https://en.wikipedia.org/wiki/Riddley_Walker",
    "https://en.wikipedia.org/wiki/Roderick_(novel)",
    "https://en.wikipedia.org/wiki/The_Shadow_of_the_Torturer",
    "https://en.wikipedia.org/wiki/Oath_of_Fealty_(novel)",
    "https://en.wikipedia.org/wiki/No_Enemy_But_Time",
    "https://en.wikipedia.org/wiki/Neuromancer"
]


# Output file to save the page content
output_file = "wikipedia_content_markup.txt"

def extract_full_text_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the main content div
        main_content_div = soup.find("div", {"id": "mw-content-text"})

        if main_content_div:
            # Get all text from main content, preserving structure
            text_content = ""
            for element in main_content_div.descendants:
                if element.name == 'h2':
                    text_content += "\n\n## " + element.get_text(strip=True) + "\n"
                elif element.name == 'h3':
                    text_content += "\n\n### " + element.get_text(strip=True) + "\n"
                elif element.name in ['p', 'li', 'dd']:
                    text = element.get_text()
                    text = re.sub(r'\s+', ' ', text).strip()
                    text_content += text + "\n"
                    
            return text_content
        else:
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


# Main script to iterate over links and save content
with open(output_file, "w", encoding="utf-8") as file:
    for link in novel_links:
        print(f"Processing: {link}")
        content = extract_full_text_content(link)

        if content:
            file.write(f"URL: {link}\n")
            file.write("Content:\n")
            file.write(content + "\n\n")
        else:
            file.write(f"URL: {link}\n")
            file.write("Content: Not found or unable to process.\n\n")

print(f"Wikipedia text content with markup has been written to {output_file}.")