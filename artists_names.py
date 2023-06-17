import billboard

# Function that returns a list of top artists from a given year with their rank
def get_top_artists_from_year(year : int) -> list[str]:
    chart = billboard.ChartData('top-artists', year=year)
    top_artists = list()
    for artist in chart:
        top_artists.append(artist.artist)
    return top_artists

# Function that returns a list of top artists from a given year range with their rank
def get_top_artists_from_year_range(start_year : int, end_year : int) -> list[str]:
    top_artists = list()
    for year in range(start_year, end_year):
        top_artists.append(get_top_artists_from_year(year))
    return top_artists

# Function that returns a list of names of the artists without any duplicates in alphabetical order
def filter_artists(start_year : int, end_year : int) -> list[str]:
    top_artists = get_top_artists_from_year_range(start_year, end_year)
    names = [artist for list in top_artists for artist in list]
    return set(names)

if __name__ == '__main__':
    print(filter_artists(2006, 2021))
    
    