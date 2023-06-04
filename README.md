# addlyrics
Searches various websites and tags lyrics to local mp3 files.  Currently searches 4 websites: musixmatch, animelyrics, vocaloidlyrics, and note.

Work in progress.

## Requirements
Python, selenium with the geckodriver, eyed3, and romkan (if using animelyrics.com).

## Usage
Edit `config.py` and point to your geckodriver and directory of mp3 files.  Enabling interactive mode in the config will make the program ask you if you want to search a website before searching, and will ask you if you want to write the lyrics found.  After editing the config, run `main.py`.
