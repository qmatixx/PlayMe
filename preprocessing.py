import artists_names as artists_names
import wikipedia_info as wikipedia_info
import gender_guesser.detector as gender
import warnings
from bs4 import GuessedAtParserWarning
import wikipedia

global main_genres
main_genres = ['pop', 'hip hop', 'rock', 'rap', 'r&b', 'alt', 'trap', 'country', 'soul']

# Surpress unnecessary warnings
warnings.filterwarnings(action="ignore", category=GuessedAtParserWarning)

# Function that calculates the age of a band given an infobox as a dictionary
# Returns None if the age cannot be calculated
def preprocessing_age_bands(infobox : dict[str,str]) -> int:
    if 'Members' not in infobox:
        return None
    list = infobox['Members'].split('\n')
    list = list[1:-1]
    age = 0
    age_b4 = 0
    for member in list:
        try:
            age += wikipedia_info.get_age(wikipedia_info.prepare_infobox(wikipedia_info.prepare_url(member)))
            age_b4 = age - age_b4
        except TypeError:
            age += age_b4
        except wikipedia.exceptions.PageError:
            age += age_b4
        except wikipedia.exceptions.DisambiguationError:
            age += age_b4
        except UnboundLocalError:
            age += age_b4
        except KeyError:
            age += age_b4
    try:
        age = age / len(list)
    except:
        return None
    if age == 0:
        return None
    return int(age)
    
# Function that fix the country of an artist name given a country as a string
# Returns None if the country is None
def preprocessing_country(country : str) -> str:
    if country is None:
        return None
    if country.startswith(' '):
        country = country[1:]
    if country.endswith('\n'):
        country = country[:-2]
    while country.endswith(']') is True:
        country = country[:-3]
    if country == 'United States' or country == 'U.S' or country == 'US':
        country = 'U.S.'
    return country

# Function that fix the genres by choosing the most common genre from a list
def preprocessing_genres(genres : list[str]) -> str:
    if genres is None or len(genres) == 0:
        return None
    for genre in genres:
        if genre in main_genres:
            return genre
    return genres[0]

# Function that fix the gender of an artist given a gender as a string
def preprocessing_gender(sex : str) -> str:
    if sex == 'unknown':
        sex = 'male'
    if sex == 'mostly_male':
        sex = 'male'
    if sex == 'mostly_female':
        sex = 'female'
    if sex == 'andy':
        sex = 'male'
    return sex

# Function that guesses the gender of a band given an infobox as a dictionary
# Returns None if gender cannot be guessed
def preprocessing_gender_bands(infobox : dict[str,str]) -> str:
    if 'Members' not in infobox:
        return None
    list = infobox['Members'].split('\n')
    list = list[1:-1]
    gender_list = []
    for member in list:
        d = gender.Detector()
        sex = d.get_gender(preprocessing_gender(member))
        gender_list.append(sex)
    try:
        sex = max(set(gender_list), key = gender_list.count)
    except ValueError:
        return None
    return sex

# Function that fix information in the dictionary of artists
def preprocessing_dict(dict : dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    for artist in dict:
        if dict[artist]['Age'] is None:
            dict[artist]['Age'] = preprocessing_age_bands(wikipedia_info.prepare_infobox(wikipedia_info.prepare_url(artist)))
        dict[artist]['Country'] = preprocessing_country(dict[artist]['Country'])
        dict[artist]['Genres'] = preprocessing_genres(dict[artist]['Genres'])
        if dict[artist]['Gender'] is None:
            dict[artist]['Gender'] = preprocessing_gender_bands(wikipedia_info.prepare_infobox(wikipedia_info.prepare_url(artist)))
        dict[artist]['Gender'] = preprocessing_gender(dict[artist]['Gender'])
    return dict

# Function that erases the artists that have None values in their dictionary
def erase_leftovers(dict : dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    new_dict = {}
    for artists in dict:
        if any(dict[artists][key] is None for key in dict[artists]):
            continue
        else:
            new_dict[artists] = dict[artists]
    return new_dict