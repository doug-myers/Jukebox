import time
import threading
from queue import Queue
from pygame import mixer


class Song:
    def __init__(self, title, artist, sound_file):
        self.title = title
        self.artist = artist
        self.sound_file = sound_file


class Jukebox:
    def __init__(self):
        self.songs = []
        self.play_queue = Queue()
        self.running = False  # Indicates the Jukebox is running
        self.skip = False  # For skipping to the next song
        self.now_playing = None  # Song currently playing
        mixer.init()

    def add(self, song):
        self.songs.append(song)

    def show_songs(self):
        i = 0
        for song in self.songs:
            print("{}: {} by {}".format(i, song.title, song.artist))
            i += 1
        return i

    def enqueue_song(self, song_index):
        self.play_queue.put(self.songs[song_index])

    def show_status(self):
        if jukebox.now_playing is None:
            print("Currently no song playing.")
        else:
            print("Currently playing: {}".format(jukebox.now_playing.title))
        print("Play Queue:")
        i = 0
        for song in list(self.play_queue.queue):
            print("  {}: {} by {}".format(i, song.title, song.artist))
            i += 1
        return i

    def start(self):
        play_thread = threading.Thread(target=self.play)
        play_thread.start()

    def stop(self):
        self.running = False

    def next(self):
        self.skip = True

    def play(self):
        self.running = True
        while self.running:
            song = self.play_queue.get()
            self.now_playing = song
            mixer.music.load(song.sound_file)  # Loading Music File
            mixer.music.play()  # Playing Music with Pygame
            while self.running and mixer.music.get_busy():
                if self.skip:
                    self.skip = False
                    break
                time.sleep(1)
            mixer.music.stop()
            self.now_playing = None


# Create and load and start the jukebox
jukebox = Jukebox()
song_db = open("songs.db")
for line in song_db:
    line = line.strip()
    (title, artist, filePath) = line.split(",")
    jukebox.add(Song(title, artist, filePath))
print("Welcome to Jukebox!")
while True:
    jukebox.show_status()
    print("What would you like to do?")
    print("  0) Exit program")
    if jukebox.running:
        print("  1) Stop the Jukebox")
    else:
        print("  1) Start the Jukebox")
    print("  2) Add a song to the queue")
    print("  3) Skip to the next song")
    cmd = input("Enter command number: ")
    if cmd == "0":
        jukebox.stop()
        break
    elif cmd == "1":
        if jukebox.running:
            jukebox.stop()
        else:
            jukebox.start()
    elif cmd == "2":
        i = jukebox.show_songs()
        n = input("Select song to add by number: ")
        if n.isnumeric() and int(n) < i:
            jukebox.enqueue_song(int(n))
        else:
            print("Error: Not a valid selection.")
    elif cmd == "3":
        jukebox.next()
        time.sleep(2)
    elif cmd != "":
        print("Error: Not valid command number.")
    print()
