topmovies

Note: topmovies is a Python script that uses the TMDb API to retrieve information about the top 250 movies of all time.

Requirements:
python >= 3.6

Installation:
pip install topmovies

Usage:
import topmovies as tm

top_movies = tm.fetch_douban_top_movies(0, 9)

for movie in top_movies[:5]:
    print(movie)
