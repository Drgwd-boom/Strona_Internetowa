import requests
from bs4 import BeautifulSoup

# URL strony do scrapowania
URL = "https://warcraft.wiki.gg/wiki/Icecrown_Citadel_(instance)"

favourite_bosses = ["Lord Marrowgar", "Professor Putricide", "Sindragosa", "The Lich King"]

# Pobieranie strony
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Znalezienie sekcji z bossami
boss_table = soup.find("table", class_="infobox")  # Infobox często zawiera listę bossów
bosses = []

if boss_table:
    links = boss_table.find_all("a")
    for link in links:
        name = link.text.strip()
        if name in favourite_bosses and not any(b["name"] == name for b in bosses):
            href = link["href"] if "href" in link.attrs else ""
            if name and href.startswith("/wiki/"):
                bosses.append({
                    "name": name,
                    "url": f"https://warcraft.wiki.gg{href}"
                })

my_description = {
    "Lord Marrowgar": "Lord Marrowgar and his spikes are a blast! He was the first boss I downed in ICC, and I’ll never forget the joy of hearing those spikes go *crunch*. Also, he's the first boss I’ve ever had the pleasure of ‘adopting’ (he might not agree though).",

    "Professor Putricide": "Putricide's mechanics always left me scratching my head. I’m convinced my raid team survived mostly because of pure luck and the slime gods smiling upon us. Half the time, I didn’t even know what was going on. Spoiler: we still managed to win.",

    "Sindragosa": "Ah, Sindragosa. We wiped on her more times than I’d like to admit, and probably more than on the final boss of the game. Honestly, I think I had a better chance of beating her if I spent more time dodging her *frost breaths* and less time making memes about how much we wiped.",

    "The Lich King": "The Lich King was the final test. Beat him with a bunch of randoms, and the cutscene in the middle was so epic it almost made me forget I was about to get obliterated. Almost."
}
# Tworzenie głównej strony markdown
to_markdown = "# My favourite Icecrown Citadel Bosses\n\n"
for boss in bosses:
    to_markdown += (f"## [{boss['name']}]({boss['name'].replace(' ', '_')}.md)\n"
                    f"{my_description[boss['name']]}\n\n")

with open("index.md", "w", encoding="utf-8") as f:
    f.write(to_markdown)

# Tworzenie plików dla każdego bossa
for boss in bosses:
    boss_page = requests.get(boss["url"])
    boss_soup = BeautifulSoup(boss_page.text, "html.parser")

    p_tags = boss_soup.find_all('p')
    paragraphs = []

    if boss["name"] == "The Lich King":
        paragraphs = [p.get_text() for p in p_tags[2:5]]
    elif boss["name"] == "Professor Putricide":
        paragraphs = [p.get_text() for p in p_tags[4:5]]
    elif boss["name"] == "Sindragosa":
        paragraphs = [p.get_text() for p in p_tags[2:3]]
    else:
        paragraphs = [p.get_text() for p in p_tags[2:3]]


    # Pobranie dodatkowych informacji
    infobox = boss_soup.find("table", class_="infobox")
    race = affiliation = location = "Unknown"

    if infobox:
        for row in infobox.find_all("tr"):
            header = row.find("th")
            data = row.find("td")
            if header and data:
                header_text = header.text.strip()
                data_text = data.text.strip()
                if "Race" in header_text:
                    race = data_text
                elif "Affiliation" in header_text:
                    affiliation = data_text
                elif "Location" in header_text:
                    location = data_text

    # Tworzenie markdowna dla bossa
    boss_markdown = f"# {boss['name']}\n\n"
    boss_markdown += f"![{boss['name']}](images/{boss['name'].replace(' ', '_').lower()}.jpg)\n\n"
    boss_markdown += f"## Race\n\n{race}\n\n"
    boss_markdown += f"## Affiliation(s)\n\n{affiliation}\n\n"
    boss_markdown += f"## Location\n\n{location}\n\n"
    boss_markdown += "## Description\n\n\n\n"

    # Tworzenie listy wypunktowanej z akapitów
    for paragraph in paragraphs:
        boss_markdown += f"- {paragraph}\n"

    boss_markdown += f"[Wiki Source]({boss['url']})\n"

    with open(f"{boss['name'].replace(' ', '_')}.md", "w", encoding="utf-8") as f:
        f.write(boss_markdown)
