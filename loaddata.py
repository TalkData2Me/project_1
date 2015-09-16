"""loaddata is a module for accessing scraped data about movies from
BoxOfficeMojo and Metacritic.
It's built specifically to work with the data collected for the
CapitalOne Metis Data Science Python Bootcamp Pilot Extravaganza 2K15.
"""

# imports
import os
import json
import pprint
import datetime
import operator
from pprint import pprint

# constants
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))
MOJO_DIR = os.path.join(DATA_DIR, 'boxofficemojo')
META_DIR = os.path.join(DATA_DIR,'metacritic')

def get_boxofficemojo_movies(dirname):
    file_contents = os.listdir(dirname)

    movie_list = []

    for filename in file_contents:
        filepath = os.path.join(dirname, filename)

        with open(filepath, 'r') as movie_file:
            movie_data = json.load(movie_file)

        movie_list.append(movie_data)
         
        #removing the lists
        movie_list = [mv for mv in movie_list if isinstance(mv, dict) and 'title' in mv.keys()]

    print "Parsed %i movies from %i files" % (len(movie_list),
                                              len(file_contents))
    return movie_list

def datetime_func(date_string):
    if date_string:
        return datetime.date(*(int(dstr) for dstr in date_string.split('-')))

def merge_source(src1,src2):

    meta_movies = [meta for meta in src2 if isinstance(meta, dict) and 'title' in meta.keys()]
    mojo_movies = [mojo for mojo in src1 if isinstance(mojo, dict) and 'title' in mojo.keys()]

    for meta_movie in meta_movies:
        for mojo_movie in mojo_movies:
            if meta_movie['title'] == mojo_movie['title']:
                meta_movie.update(mojo_movie)
    return meta_movies
#        sorting_key = operator.itemgetter("title")
#        if sorting_key:
#            meta = sorted(src1,key=sorting_key)
#            mojo = sorted(src2,key=sorting_key)

#            for meta_m,mojo_m in zip(meta,mojo):
#                meta_m.update(mojo_m)

#            return meta_m


if __name__ == "__main__":
    mojo_movies = get_boxofficemojo_movies(MOJO_DIR)

    for movie in mojo_movies:
        parsed_date_wide = datetime_func(movie['release_date_wide'])
        parsed_date_limited = datetime_func(movie['release_date_limited'])
        movie['release_date_wide'] = parsed_date_wide
        movie['release_date_limited'] = parsed_date_limited

    meta_movies = get_boxofficemojo_movies(META_DIR)

    # import collections
    # types = collections.Counter()
    # for movies in meta_movies:
    #     types.update([type(movies)])
    #mojo_movies[:2]
    #print meta_movies[:2]
    # print types
    meta_mojo_movies_merged=merge_source(mojo_movies, meta_movies)

    #x=open('/','w')


    pprint(meta_mojo_movies_merged[:3])
