import pandas as pd
import os
from tkinter.filedialog import askopenfilename
import mutagen

# Create an empty DataFrame to store music information
music_df = pd.DataFrame(columns=['filename', 'album', 'title', 'length', 'artist'])

database_path = os.path.join(os.path.dirname(__file__), 'music_database.csv')

# Function to add a music to the DataFrame
def add_music(filename, title, album, length, artist):
    global music_df

    if not music_df[music_df['title'] == title].empty:
        print(f"A song with the title '{title}' already exists in the database.")
    else:
        music_info_row = {'filename': filename, 'album': album, 'title': title, 'length': length, 'artist': artist}
        list_of_music_info = music_df.to_dict('records')
        list_of_music_info.append(music_info_row)

        music_df = pd.DataFrame.from_records(list_of_music_info)

# Function to remove a music from the DataFrame
def remove_music(title):
    global music_df
    music_df = music_df[music_df['title'] != title]

# Function to search for music and display them in a playlist
def search_music(filename=None, title=None, album=None, min_length=None, max_length=None, artist=None, all=False):
    global music_df
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
    


def search_all(target):
    global music_df

    print("Search result:")

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

    if len(results):
        print(results.to_string(index=False))
    else:
        print(f"No search result for \"{target}\".")
    print()

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

# let user to upload a wav file
def upload_wav():
    
    global music_df
    file_path = askopenfilename()
    # print(filename)
    audio = mutagen.File(file_path)
    filename = os.path.basename(file_path)
    title = audio.tags['TIT2']
    album = audio.tags['TALB']
    length = audio.info.length
    artist = audio.tags['TPE1']
    add_music(filename, title, album, length, artist)
    return file_path

# get length in mm:ss format
def get_format_length(length):
    minutes = int(length / 60)
    seconds = int(length % 60)
    if seconds < 10:
        return f"{minutes}:0{seconds}"
    return f"{minutes}:{seconds}"

# Example usage

# load_from_csv(database_path)

# add_music('song1.wav', 'Thriller', 'Billie Jean', 294, 'Michael Jackson')
# add_music('song2.wav', 'Back in Black', 'Hells Bells', 312, 'AC/DC')
# add_music('song3.wav', 'Rumours', 'Dreams', 257, 'Fleetwood Mac')
# add_music('song4.wav', 'The Dark Side of the Moon', 'Time', 421, 'Pink Floyd')
# add_music('song5.wav', 'Purple Rain', 'When Doves Cry', 346, 'Prince')

# search_music(filename='song')
# search_music(title='Thriller')
# search_music(album='time')
# search_music(artist='AC/DC')
# search_music(min_length=300)

# search_music(filename='music')
# search_all("in")

# while(1):
#     user_input = input("Choose action(A for add music, R for remove music, F for find music, S for Save and quit program): ")

#     if user_input == "A":
#         upload_wav()
        
#     elif user_input == "R":
#         title = input("Input title to remove: ")
#         remove_music(title)
#     elif user_input == "F":
#         search_target = input("Input keyword: ")
#         search_all(search_target)
#     elif user_input == "S":
#         break
#     else:
#         print("Invalid input, please input again.")

# save_to_csv(database_path)
# print("Saved.")