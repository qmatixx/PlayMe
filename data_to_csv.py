import datetime
from artists_names import filter_artists, get_top_artists_from_year_range
import csv
import artists_names as artists_names
import wikipedia_info as wikipedia_info
import preprocessing
from spotify_artists import get_artists_spotify
import wikipedia

# Function that creates a dictionary with information about each artist a list of artists
def create_dict(artists : list[str]) -> dict[str, dict[str, str]]:
    dict_artists = {}
    for artist in artists:
        dict_artists[artist] = wikipedia_info.extract_info(wikipedia_info.prepare_infobox(wikipedia_info.prepare_url(artist)))
    return dict_artists

def mix_artists(artists1 : set[str], artists2 : set[str]) -> list[str]:
    return sorted(list(artists1.union(artists2)))

# Function that returns a fixed dictionary of artists given a start year and an end year
def prepare_dict(startYear : int, endYear : int) -> dict[str, dict[str, str]]:
    dict = create_dict(mix_artists(artists_names.filter_artists(startYear, endYear), get_artists_spotify()))
    dict = preprocessing.preprocessing_dict(dict)
    dict = preprocessing.erase_leftovers(dict)
    return dict

# Script that creates a csv file with the information of the artists

if __name__ == '__main__':
    header = ['', 'Age', 'Country', 'Genres', 'Number of genres', 'Years active', 'Gender']
    dict = prepare_dict(2006,datetime.datetime.now().year)
    places = get_top_artists_from_year_range(2006, datetime.datetime.now().year)
    data = []
    for key in dict:
        list = []
        list.append(key)
        ranks = []
        for place in places:
            if place[1] == key:
                ranks.append(place[0])
        list.append(min(ranks))
        for value in dict[key].values():
            list.append(value)
        data.append(list)

    with open('artists.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)