import requests
import string
from bs4 import BeautifulSoup
import datetime
import re
import wikipedia
import gender_guesser.detector as gender
import warnings
from bs4 import GuessedAtParserWarning

# Surpress unnecessary warnings
warnings.filterwarnings(action="ignore", category=GuessedAtParserWarning)

# Global variables
# List of possible endings for Wikipedia URLs
global possible_endings 
possible_endings = ['_(band)', '_(singer)', '_(rapper)', '_(drummer)', '_(musician)', '_(music_group)', '_(duo)', '_(trio)', '_(solo)', '_(group)', '_(artist)', '_(singer-songwriter)', '_(producer)', '_(record_producer)', '_(dj)', '_(writer)']
# List of possible genres
global possible_genres
possible_genres = ['rock', 'electro', 'pop', 'rap', 'hip hop', 'country', 'r&b', 'rhythm and blues', 'jazz', 'blues', 'folk', 'soul', 'punk', 'metal', 'classical', 'dance', 'reggae', 'latin', 'indie', 'funk', 'disco', 'gospel', 'christian', 'opera', 'new age', 'trap', 'instrumental', 'ska', 'grunge', 'emo', 'techno', 'house', 'dubstep', 'trance', 'dub', 'drum and bass', 'ambient', 'reggaeton', 'salsa', 'samba', 'bossa nova', 'tango', 'flamenco', 'fado', 'bhangra', 'bollywood', 'k-pop', 'j-pop', 'j-rock', 'jazz fusion', 'alt']

# Function that returns url of Wikipedia page as a string given an artist name
def prepare_url(artist_name : string) -> string:
    url = None
    try:
        url = wikipedia.page(artist_name, auto_suggest=False).url
    except wikipedia.exceptions.DisambiguationError as e:
        for ending in possible_endings:
            try:
                url = wikipedia.page(artist_name + ending, auto_suggest=False).url
                break
            except wikipedia.exceptions.PageError as e:
                continue
            except wikipedia.exceptions.DisambiguationError:
                continue
    except wikipedia.exceptions.PageError as e:
        try:
            url = wikipedia.page(artist_name, auto_suggest=True).url
        except wikipedia.exceptions.PageError as e:
            return None
        except wikipedia.exceptions.DisambiguationError:
            return None
    return url
    
# Function that returns a dictionary of the infobox of a Wikipedia page given a url of Wikipedia page as a string
def prepare_infobox(url : string) -> dict[str, str]:
    if url is None:
        return None
    dict = {}
    url_open = requests.get(url)
    soup = BeautifulSoup(url_open.content, features='html.parser')
    details = soup('table', {'class': 'infobox'})
    for i in details:
        h = i.find_all('tr')
        for j in h:
            heading = j.find_all('th')
            detail = j.find_all('td')
            if heading is not None and detail is not None:
                for x,y in zip(heading,detail):
                    dict[x.text] = y.text  
    return dict

# Function that returns information about an artist as a dictionary given an infobox as a fictionary and an artist name as a string
def extract_info(infobox: dict[str,str]) -> dict[str, dict[str, str]]:
    if infobox is None:
        return None
    new_dict = {}
    new_dict['Age'] = get_age(infobox)
    new_dict['Country'] = get_country(infobox)
    if get_genres(infobox) is not None:
        new_dict['Genres'], new_dict['Number of genres'] = get_genres(infobox)
    else:
        new_dict['Genres'] = None
        new_dict['Number of genres'] = None
    new_dict['Years Active'] = get_years_active(infobox)
    new_dict['Gender'] = get_gender(infobox)
    return new_dict

# Function that returns age of an artist as an integer given an infobox as a dictionary
# Returns None if age cannot be found
def get_age(infobox : dict[str,str]) -> int:
    age = None
    if 'Born' in infobox:
        try:
            age = int(datetime.date.today().year) - int(re.findall(r'\((.*?)\)', infobox['Born'])[0][0:4])
        except IndexError:
            return None
        except ValueError:
            age = int(datetime.date.today().year) - int(re.findall(r'\d{4}', infobox['Born'])[0][0:4])
        if 'Died' in infobox:
            age = age - (int(datetime.datetime.today().year) - int(re.findall(r'\((.*?)\)', infobox['Died'])[0][0:4]))
    return age

# Function that returns birth country of an artist as a string given an infobox as a dictionary
# Returns None if birth country cannot be found
def get_country(infobox : dict[str,str]) -> str:
    country = None
    if 'Origin' in infobox:
        country = infobox['Origin'].split(',')[-1]
    else:
        if 'Born' in infobox:
            country = infobox['Born'].split(',')[-1]
    if country is not None:
        if country.startswith(' '):
            country = country[1:]
        if country.endswith('\n'):
            country = country[:-2]
        while country.endswith(']') is True:
            country = country[:-3]
        if country == 'United States':
            country = 'U.S.'
    return country

# Function that returns genres of an artist as a list of strings and the number of genres as an integer given an infobox as a dictionary
# Returns None if genres cannot be found    
def get_genres(infobox : dict[str,str]) -> tuple[list[str], int]:
    genres = []
    if 'Genres' in infobox:
        infobox['Genres'] = infobox['Genres'].lower()
        for genre in possible_genres:
            if genre in infobox['Genres']:
                if genre == 'rhythm and blues':
                    genre = 'r&b'
                genres.append(genre)
        return genres, len(genres)
    return None

# Function that returns years active of an artist as an integer given an infobox as a dictionary
# Returns None if years active cannot be found
def get_years_active(infobox : dict[str,str]) -> int:
    years_active = None
    key = ""
    if 'Years active' in infobox:
        key = 'Years active'
    elif 'Years\xa0active' in infobox:
        key = 'Years\xa0active'
    else:
        return None
    try:
        years_active = int(datetime.datetime.today().year) - int(re.findall(r'\d{4}', infobox[key])[0])
    except ValueError:
        return None
    if years_active is not None and 'Died' in infobox:
        years_active = years_active - (int(datetime.datetime.today().year) - int(re.findall(r'\((.*?)\)', infobox['Died'])[0][0:4]))
    return years_active

# Function that returns gender of an artists as a string given an infobox as a dictionary
# Returns None if gender cannot be found
def get_gender(infobox: dict[str,str]) -> str:
    name = ""
    if 'Birth name' in infobox:
        name = infobox['Birth name'].split(' ')[0]
    elif "Born" in infobox:
        name = infobox['Born'].split(' ')[0]
    if name.endswith('a') or name.split(' ')[0].endswith('a'):
        return 'female'
    if name != "":
        d = gender.Detector()
        sex = d.get_gender(name)
        return sex 
    return None

if __name__ == '__main__':
    prepare_url('David Kushner')