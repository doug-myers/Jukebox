import eyed3
import os

search_path = input("Enter directory to search: ")
with open("songs.db", "a") as song_db:
    for root, _, files in os.walk(search_path):
        for filename in files:
            if filename.endswith(".mp3"):
                path = os.path.join(root, filename)
                audio = eyed3.load(path)
                song_db.write("{}|{}|{}\n".format(audio.tag.title, audio.tag.artist, path))