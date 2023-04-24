import pandas as pd
import os
from tkinter.filedialog import askopenfilename
import soundfile as sf
from mutagen.wave import WAVE
from tinytag import TinyTag
import eyed3
# import main

# Create an empty DataFrame to store music information
music_df = pd.DataFrame(columns=['filename', 'album', 'title', 'length', 'artist', 'lyrics', 'album_art'])

online_df = pd.DataFrame(columns=['filename', 'album', 'title', 'length', 'artist', 'lyrics', 'album_art'])

database_path = os.path.join(os.path.dirname(__file__), 'music_database.csv')

# Function to add a music to the DataFrame
def add_music(filename, title, album, length, artist, lyrics=None, album_art=None):
    global music_df

    if title == None or title == "":
        title = os.path.basename(filename)
        title = os.path.splitext(title)[0]

    if album == None or album == "":
        album = "none"
    
    if artist == None or artist == "":
        artist = "none"

    if not music_df[music_df['title'] == title].empty:
        print(f"A song with the title '{title}' already exists in the database.")
    else:
        if lyrics == None:
            lyrics = "No lyrics found."

        if album_art == None:
            album_art = "null"
        print(album_art)

        music_info_row = {'filename': filename,
                          'album': album,
                          'title': title,
                          'length': length,
                          'artist': artist,
                          'lyrics': lyrics,
                          'album_art': album_art
                          }
        list_of_music_info = music_df.to_dict('records')
        list_of_music_info.append(music_info_row)

        music_df = pd.DataFrame.from_records(list_of_music_info)
        save_to_csv(database_path)

# Function to update a music in the DataFrame
def update_music(filename, title, album, artist, lyrics=None):
    global music_df

    if title == None or title == "":
        title = os.path.basename(filename)
        title = os.path.splitext(title)[0]

    if album == None or album == "":
        album = "none"
    
    if artist == None or artist == "":
        artist = "none"

    if lyrics == None:
        lyrics = "No lyrics found."

    music_info_row = {'filename': filename,
                        'album': album,
                        'title': title,
                        'length': get_length(filename),
                        'artist': artist,
                        'lyrics': lyrics,
                        'album_art': get_album_art(filename)
                        }
    music_df = music_df[music_df['filename'] != filename]
    list_of_music_info = music_df.to_dict('records')
    list_of_music_info.append(music_info_row)

    music_df = pd.DataFrame.from_records(list_of_music_info)
    save_to_csv(database_path)

# Function to remove a music from the DataFrame
def remove_music(title):
    global music_df
    music_df = music_df[music_df['title'] != title]
    save_to_csv(database_path)

# Function to search for music and display them in a playlist
def search_music(filename=None, title=None, album=None, min_length=None, max_length=None, artist=None, all=False):
    global music_df
    global online_df
    
    if not online_df.empty:
        results  = pd.concat([music_df, online_df], ignore_index=True).drop_duplicates(subset=['filename'], keep='first')
    else:
        results = music_df

    if filename:
        results = results[results['filename'].str.contains(filename, case=False)]
    if title:
        results = results[results['title'].str.contains(title, case=False)]
    if album:
        results = results[results['album'].str.contains(album, case=False)]
    if min_length:
        results = results[results['length'] >= min_length]
    if max_length:
        results = results[results['length'] <= max_length]
    if artist:
        results = results[results['artist'].str.contains(artist, case=False)]
    
    if all:
        if not results.empty:
            return results
        return None

    print("Search result:")
    print(results.to_string(index=False))
    print()
    

def search(target):
    global music_df

    # print("Search result:")

    filename_search_result = search_music(filename=target, all=True)
    title_search_result = search_music(title=target, all=True)
    album_search_result = search_music(album=target, all=True)
    artist_search_result = search_music(artist=target, all=True)

    results = pd.DataFrame(columns=['filename', 'album', 'title', 'length', 'artist'])

    results = pd.concat([results, filename_search_result], ignore_index=True)
    results = pd.concat([results, title_search_result], ignore_index=True)
    results = pd.concat([results, album_search_result], ignore_index=True)
    results = pd.concat([results, artist_search_result], ignore_index=True)

    results = results.drop_duplicates(subset=['filename'], keep='first')
    results = results.sort_values(by = 'filename')

    return results

# Function to save the music information to a CSV file
def save_to_csv(filename):
    global music_df
    music_df.to_csv(filename, index=False)

# Function to load the music information from a CSV file
def load_from_csv(filename):
    global music_df
    if not os.path.isfile(filename):
        print(f"The file '{filename}' does not exist. Creating an empty file.")
        music_df.to_csv(filename, index=False)
    music_df = pd.read_csv(filename)

def load_from_online_csv():
    global online_df
    if not os.path.isfile("getdata.csv"):
        online_df.to_csv("getdata.csv", index=False)
    online_df = pd.read_csv("getdata.csv")

# let user to upload a wav file
def upload_wav():
    
    global music_df
    file_path = askopenfilename()
    if file_path == "":
        return ""
    
    if file_path.endswith('.mp3'):
        audio = TinyTag.get(file_path)

        filename = os.path.basename(file_path)
        artist = audio.artist
        title = audio.title
        album = audio.album
        length = audio.duration
        lyrics = get_lyrics_from_file(file_path)
        album_art = get_album_art_from_file(file_path)

    audio = sf.SoundFile(file_path)

    filename = os.path.basename(file_path) 
    artist = audio.__getattr__('artist')
    title = audio.__getattr__('title')
    album = audio.__getattr__('album')
    length = audio.frames / audio.samplerate
    lyrics = get_lyrics_from_file(file_path)
    album_art = get_album_art_from_file(file_path)

    add_music(filename, title, album, length, artist, lyrics, album_art)
    return file_path

# get length in mm:ss format
def get_format_length(length):
    minutes = int(length / 60)
    seconds = int(length % 60)
    if seconds < 10:
        return f"{minutes}:0{seconds}"
    return f"{minutes}:{seconds}"

def get_lyrics_from_file(filename):
    try:
        if not filename.endswith('.wav'):
            track = eyed3.load(filename)
            tag = track.tag
            lyrics = tag.lyrics[0].text
            return None

        audio = WAVE(filename)
        lyrics = audio.tags['TXXX:LYRICS']
        if lyrics == '':
            lyrics = None
    except:
        lyrics = None
    return lyrics

def get_album_art_from_file(filename):
    try:
        if not filename.endswith('.wav'):
            return None

        audio = WAVE(filename)
        album_art = repr(audio.tags['APIC:'].data)
    except:
        album_art = None
    return album_art

# get filename from title
def get_filename(title):
    global music_df
    filename = music_df[music_df['title'] == title]['filename'].values[0]
    return filename

def get_title(filename):
    global music_df
    title = music_df[music_df['filename'] == filename]['title'].values[0]
    return title

def get_artist(filename):
    global music_df
    artist = music_df[music_df['filename'] == filename]['artist'].values[0]
    return artist

def get_album(filename):
    global music_df
    album = music_df[music_df['filename'] == filename]['album'].values[0]
    return album

def get_length(filename):
    global music_df
    length = music_df[music_df['filename'] == filename]['length'].values[0]
    return length

def get_lyrics(filename):
    global music_df
    lyrics = music_df[music_df['filename'] == filename]['lyrics'].values[0]
    return lyrics

def get_album_art(filename):
    global music_df
    album_art = music_df[music_df['filename'] == filename]['album_art'].values[0]
    return album_art