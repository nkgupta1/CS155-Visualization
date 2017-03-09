#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from common import *


movie_names = create_dict()  # dict[movie_id: movie_name]
movie_ratings = import_data()  # movies[movie_id, ratings[rating]]


def twoD_viz(title, movie_ids, xy_coords, min_max=[0., 10.], off_set=0.05):
    '''
    param: movie_ids: 1d-list or numpy array of [movie_ids]
    param: xy_coords: 2d numpy array of [movie_x, movie_y] corresponding to 
    movie_id in movie_ids
    return: none: 
    '''
     # dict[movie_id: movie_name]
    # fig, ax = plt.subplots()
    ax = plt.subplot()
    plt.title(title)
    ax.axis((min_max[0], min_max[1], min_max[0], min_max[1]))
    mid = (min_max[0] + min_max[1]) / 2.
    interval = (min_max[1] - min_max[0])
    off_set *= interval
    ax.scatter(xy_coords[:, 0], xy_coords[:, 1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i, movie in enumerate(movie_ids):
        label_position = xy_coords[i] + np.sign(mid - xy_coords[i]) * off_set
        label_position -= [.12 * interval, .01 * interval]  # static offset
        ax.annotate(movie_names[movie], xy_coords[i], xytext=label_position)
    plt.savefig('../graphics/{0}.png'.format(title), bbox_inches='tight', 
               transparent=True)


def viz_tasks(V):
    '''
    param: V: 2-d numpy matrix as defined in guide as "V", V.shape = [2, n],
    V = movie_id[x, y]
    '''
    
    movie_ids = movie_names.keys()
    # 10 random movies
    rand_movies = np.random.randint(1, len(movie_ids) + 1, 10)

    # 10 most popular movies
    movie_sizes = []
    movie_avg_ratings = []
    for movie, ratings in movie_ratings:
        movie_sizes.append(len(ratings))
        movie_avg_ratings.append(sum(ratings) / len(ratings))    
    most_popular = np.array(list(zip(*sorted(zip(movie_sizes, movie_ids))))[1][-10:])

    # 10 best movies
    best_movies = np.array(list(zip(*sorted(zip(movie_avg_ratings, movie_ids))))[1][-10:])

    # first 10 movies from three genres
    animation, scifi, war = [np.array([x for x, y in genre][:10]) 
        for genre in [import_genres(['Animation']), import_genres(['Sci-Fi']), 
        import_genres(['War'])]]

    twoD_viz('10 Random Films', rand_movies, V[rand_movies - 1])
    twoD_viz('10 Most Popular Films', most_popular, V[most_popular - 1])
    twoD_viz('10 Most Rated Films', best_movies, V[best_movies - 1])
    twoD_viz('Top 10 Animation Films', animation, V[animation - 1])


# viz_tasks(np.zeros((1000, 2)))



