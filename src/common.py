#!/usr/bin/env python3

M = 943     # number of users
N = 1682    # number of movies

def create_dict():
    '''
    Creates a dictionary between id and movie title.
    '''
    dct = {}
    with open('../data/movies.txt','r',encoding='latin1') as f:
        for line in f:
            lst = line.split()

            if len(lst) == 0:
                continue

            idx = int(lst[0])
            
            movie = ' '.join(lst[1:]).rsplit(')')[:-1]
            movie = ') '.join(movie) + ')'

            if movie[0] == '"':
                movie += '"'

            dct[idx] = movie

    return dct

def import_data():
    '''
    Imports entire dataset.
    
    Returns a list of tuples with movie id and ratings.
    '''

    ranks = [(i+1, []) for i in range(N)]
    with open('../data/data.txt','r') as f:
        for line in f:
            lst = line.split()

            if len(lst) == 0:
                continue

            movie = int(lst[1]) - 1 # Zero-indexing
            rating = int(lst[2])

            ranks[movie][1].append(rating)

    return ranks

def import_genres(genres):
    '''
    Imports data for a specific genre of movie.
    '''

    # Genre names mapped to location in data.
    dct = {
        'Unknown' : 0,
        'Action' : 1,
        'Adventure' : 2,
        'Animation' : 3,
        'Childrens' : 4,
        'Comedy' : 5,
        'Crime' : 6,
        'Documentary' : 7,
        'Drama' : 8,
        'Fantasy' : 9,
        'Film-Noir' : 10,
        'Horror' : 11,
        'Musical' : 12,
        'Mystery' : 13,
        'Romance' : 14,
        'Sci-Fi' : 15,
        'Thriller' : 16,
        'War' : 17,
        'Western' : 18
    }

    g_list = [[0 for i in range(19)] for j in range(1682)]
    with open('../data/movies.txt','r',encoding='latin1') as f:
        for line in f:
            lst = line.split()

            if len(lst) == 0:
                continue

            movie = int(lst[0]) - 1

            line = ''.join(lst[1:]).rsplit(')')[-1] # Remove everything before catagories
            for i in range(19):
                if line[i] == '1':
                    g_list[movie][i] = 1

    ranks = [(i+1, []) for i in range(1682)]
    ranks = [(i+1, []) for i in range(N)]
    with open('../data/data.txt','r') as f:
        for line in f:
            lst = line.split()

            if len(lst) == 0:
                continue

            movie = int(lst[1]) - 1 # Zero-indexing
            rating = int(lst[2])

            cont = 1
            for genre in genres:
                if g_list[movie][dct[genre]] == 1:
                    cont = 0
            if cont == 1:
                continue

            ranks[movie][1].append(rating)

    ranks = [x for x in ranks if len(x[1]) > 0]
    return ranks