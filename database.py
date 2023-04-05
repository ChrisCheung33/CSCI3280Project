import pandas as pd
import os

# Create an empty DataFrame to store music information
music_df = pd.DataFrame(columns=['filename', 'album', 'title', 'length', 'creator'])

# Function to add a music to the DataFrame
def add_music(filename, title, album, length, creator):
    global music_df

    if not music_df[music_df['title'] == title].empty:
        print(f"A song with the title '{title}' already exists in the database.")
    else:
        music_info_row = {'filename': filename, 'album': album, 'title': title, 'length': length, 'creator': creator}
        list_of_music_info = music_df.to_dict('records')
        list_of_music_info.append(music_info_row)

        music_df = pd.DataFrame.from_records(list_of_music_info)

# Function to remove a music from the DataFrame
def remove_music(title):
    global music_df
    music_df = music_df[music_df['title'] != title]

# Function to search for music and display them in a playlist
def search_music(filename=None, title=None, album=None, min_length=None, max_length=None, creator=None):
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
    if creator:
        results = results[results['creator'].str.contains(creator, case=False)]
    
    print("Playlist:")
    if results.empty:
        print("No search result")
    else:
        print(results.to_string(index=False))
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

# Example usage

load_from_csv('music.csv')

# add_music('song1.wav', 'Thriller', 'Billie Jean', 294, 'Michael Jackson')
# add_music('song2.wav', 'Back in Black', 'Hells Bells', 312, 'AC/DC')
# add_music('song3.wav', 'Rumours', 'Dreams', 257, 'Fleetwood Mac')
# add_music('song4.wav', 'The Dark Side of the Moon', 'Time', 421, 'Pink Floyd')
# add_music('song5.wav', 'Purple Rain', 'When Doves Cry', 346, 'Prince')

search_music(filename='song')
search_music(album='time')
search_music(title='Thriller')
search_music(creator='AC/DC')
search_music(min_length=300)

search_music(filename='music')

save_to_csv('music.csv')