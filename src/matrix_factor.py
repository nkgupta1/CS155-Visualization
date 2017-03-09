#!/usr/bin/env python3
# creates and factors a matrix

import numpy as np
from prob2utils import train_model

def create_Y():
    '''
    returns an M x N matrix of users and movie ratings
    '''

    M = 943     # number of users
    N = 1682    # number of movies
    num_ratings = 100000    # number of ratings

    # Y = np.zeros((M, N))
    Y = np.zeros((num_ratings, 3), dtype=np.int)

    with open('../data/data.txt','r') as f:
        rating_count = 0
        for line in f:
            lst = line.split()

            if len(lst) == 0:
                continue

            user = int(lst[0]) - 1 # Zero-indexing
            movie = int(lst[1]) - 1 # Zero-indexing
            rating = int(lst[2])

            # Y[user][movie] = rating
            Y[rating_count][0] = user
            Y[rating_count][1] = movie
            Y[rating_count][2] = rating

            rating_count += 1

    return Y


if __name__ == '__main__':

    M = 943     # number of users
    N = 1682    # number of movies
    K = 20      # number of latent factors

    eta = .01   # step size
    reg = 10    # regularization strength

    Y = create_Y()

    print('training...\n')
    (U, V, err) = train_model(M, N, K, eta, reg, Y)
    print('done training...\n')

    print('calculating svd...')
    A, S, B = np.linalg.svd(V, full_matrices=False)
    print('done calculating svd...')

    np.save('models/{:6.5f}-U-{:.4f}-{:.4f}'.format(err, reg, eta), U)
    np.save('models/{:6.5f}-V-{:.4f}-{:.4f}'.format(err, reg, eta), V)
    np.save('models/{:6.5f}-A-{:.4f}-{:.4f}'.format(err, reg, eta), A[:, :2])