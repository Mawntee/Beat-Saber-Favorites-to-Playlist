import json
import os
import tkinter as tk
from tkinter import filedialog

def select_input_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename(initialdir=f"C:/Users/{os.getlogin()}/AppData/LocalLow/Hyperbolic Magnetism/Beat Saber", title="Select input file", filetypes=(("PlayerData file", "*.dat"), ("all files", "*.*")))
    input_file_label.config(text=f"Input file: {input_file_path}")

def convert():
    playlist_title = playlist_title_entry.get()
    playlist_author = playlist_author_entry.get()
    output_file = output_file_entry.get()

    # Read data from input file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    # Get the "localPlayers" array from the input data, if it exists
    local_players = input_data.get('localPlayers', [])

    # Get the "favoritesLevelIds" array from the first player in the "localPlayers" array, if it exists
    favorites_level_ids = (local_players[0].get('favoritesLevelIds', []) if local_players else [])

    # Create a new "songs" array based on the "favoritesLevelIds" array
    new_songs = [{'hash': level_id.replace('custom_level_', ''), 'levelid': level_id} for level_id in favorites_level_ids]

    # Read existing data from output file, if it exists
    try:
        with open(output_file, 'r') as f:
            output_data_object = json.load(f)
    except FileNotFoundError:
        output_data_object = {}

    # Get the existing "songs" array, or create a new one if it doesn't exist
    existing_songs = output_data_object.get('songs', [])

    # Merge the new songs with the existing songs, avoiding duplicates based on the "hash" property
    merged_songs = existing_songs + [new_song for new_song in new_songs if not any(existing_song['hash'] == new_song['hash'] for existing_song in existing_songs)]

    # Update the output data object with the merged songs and additional sections
    output_data_object.update({'playlistTitle': playlist_title, 'playlistAuthor': playlist_author, 'songs': merged_songs, 'image': 'base64,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'})

    # Convert the output data object to a JSON string
    output_data = json.dumps(output_data_object)

    # Show the save file dialog and set the default filename to the contents of the output_file_entry widget
    default_filename = output_file_entry.get() + '.bplist'
    output_file = filedialog.asksaveasfilename(defaultextension='.bplist', initialfile=default_filename)

    # Write the output data to the output file
    with open(output_file, 'w') as f:
        f.write(output_data)
        
# Create the GUI
root = tk.Tk()
root.title("Beat Saber Playlist Converter")

# Input file selection
input_file_path = ""
input_file_button = tk.Button(root, text="Select input file", command=select_input_file)
input_file_button.pack(pady=10)
input_file_label = tk.Label(root, text="Input file: ")
input_file_label.pack()

# Output file name entry
output_file_label = tk.Label(root, text="Output file name:")
output_file_label.pack()
output_file_entry = tk.Entry(root)
output_file_entry.pack()

# Playlist title entry
playlist_title_label = tk.Label(root, text="Playlist title:")
playlist_title_label.pack()
playlist_title_entry = tk.Entry(root)
playlist_title_entry.pack()

# Playlist author entry
playlist_author_label = tk.Label(root, text="Playlist author:")
playlist_author_label.pack()
playlist_author_entry = tk.Entry(root)
playlist_author_entry.pack()

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.pack(pady=20,padx=169)

root.mainloop()