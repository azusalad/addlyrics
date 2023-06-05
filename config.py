import sys
sys.path.insert(0, 'utils')
from musixmatch import musixmatch
from animelyrics import animelyrics
from vocaloidlyrics import vocaloidlyrics
from genius import genius
from note import note

# path to all your mp3 files
music_dir = ""
# use geckodriver
driver_path = ""
# path to xpi file of ublock origin.  If you don't have put False as a boolean.
ublock_path = ""

# if you want the program to ask you every time a website should be used
interactive_mode = True
# if you want to search for lyrics even though lyrics already exist in the tag
overwrite_existing = False

# website order
search_order = [
musixmatch,
animelyrics,
vocaloidlyrics,
genius,
note
]
