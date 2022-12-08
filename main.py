import requests
from bs4 import BeautifulSoup
import csv

if __name__ == '__main__':
    req = requests.get("https://www.jeuxvideo.com/tous-les-jeux/")
    soup = BeautifulSoup(req.text, 'html5lib')
    max_pages = int(soup.select("div[class^='pagination'] span:last-of-type")[0].text)
    with open("games.csv", 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'note rédaction', 'note utilisateurs', 'note moyenne'])
        writer.writeheader()
        for page in range(1, max_pages):
            games_list = []
            req = requests.get(f"https://www.jeuxvideo.com/tous-les-jeux/?p={page}")
            soup = BeautifulSoup(req.text, 'html5lib')
            game_soup = soup.select("ol.mainColumnWrapper li")
            for game in game_soup:
                note_chiffre = None
                note_avis = None
                note_moyenne = None
                if len(title := game.select("[class^='gameTitleLink']")):
                    if len(note := game.select("[class^='editorialRating']")):
                        if str.isdigit(note_chiffre := note[0].text.replace("/20", "").replace("\"", "")):
                            note_chiffre = int(note_chiffre)
                            note_moyenne = note_chiffre
                        else:
                            note_chiffre = None
                    if len(note := game.select("[class^='userRating']")):
                        if str.isdigit(note_avis := note[0].text.replace("/20", "").strip()):
                            note_avis = int(note_avis)
                            if note_moyenne is not None:
                                note_moyenne = (note_moyenne + note_avis) / 2
                        else:
                            note_avis = None
                    games_list.append({"name": title[0].text, "note rédaction": note_chiffre, "note utilisateurs":
                                       note_avis, "note moyenne": note_moyenne})
            writer.writerows(games_list)
