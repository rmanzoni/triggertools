import sympy
import numpy as np
import scipy.spatial.distance as ds
import matplotlib.pyplot as plt


def sampleCovarianceMatrix(pars, cov, ntoys=-1, ci=68., plot=False):
    '''
    Generates a multivariate gaussian distribution starting from the 
    covariance matrix.
    Returns an array of sampling points contained in the confidence interval
    specified by the user (in percent units i.e. 68% --> 68.). 
    By default as many toys are tossed as are necessary to have at least
    100 points outside the confidence interval. Otherwise specify ntoys.
    
    pars and cov must be numpy arrays.
    '''
    # get problem's dimensionality, cov matrix should and must be NxN
    dim = cov.shape[0]
    
    # convert the cov matrix to symbolic to make operations easier
    _cov = sympy.Matrix(cov)
    
    # fix the random number generator seed for reproducibility
    rng = np.random.RandomState(1986)

    # toss the toys
    if ntoys < 0:
        ntoys = int(100. * 100. / (100. - float(ci)))
    
    mvg = rng.multivariate_normal(pars, cov, ntoys)

    # define transformation matrices 
    transformMatrix     = _cov**-0.5 
    transformBackMatrix = _cov**0.5
    
    # transform
    _newpoints = []
    
    for point in mvg:
        newpoint = transformMatrix * point
        _newpoints.append([newpoint[0], newpoint[1]])
    
    newpoints = np.array(_newpoints, dtype=float)
    
    # normalize and centre on 0,0
    newmeans = []
    newstds  = []
    newaxes  = []
    
    for j in range(dim):
        newmeans.append(np.mean(newpoints[:,j])) 
        newstds .append(np.std (newpoints[:,j])) 
        newaxes .append((newpoints[:,j] - newmeans[j]) / newstds[j])
        
    newpoints = np.array(zip(*newaxes), dtype=float)
    
    # select points in hypersphere    
    nelements = int(float(ci)/100. * float(len(mvg)))
    
    poi = np.array([[0. for i in range(dim)]], dtype=float)
    
    savedpoints = newpoints[np.argsort(ds.cdist(poi, newpoints))][0][:nelements]

    # apply the inverse translation and scale
    savedaxes  = []

    for j in range(dim):
        savedaxes.append(savedpoints[:,j] * newstds[j] + newmeans[j])
    
    savedpoints = np.array(zip(*savedaxes), dtype=float)
    
    # transform back to original coordinate
    _finalpoints = []
    
    for point in savedpoints:
        newpoint = transformBackMatrix * point
        _finalpoints.append([newpoint[i] for i in range(dim)])
    
    finalpoints = np.array(_finalpoints)
    
    # plot, if 2D
    if plot:
        if dim == 2:
            plt.scatter(mvg[:,0]        , mvg[:,1]        , c='r')
            plt.scatter(finalpoints[:,0], finalpoints[:,1], c='g')
            
            plt.show()
        else:
            print 'too many dimensions, cannot plot'
    
    return savedpoints
    


if __name__ == '__main__':
    
    pars = np.array([-0.03618131112990319, 0.538770365688826])
    cov  = np.array([[ 0.00291171,  0.00163387],
                     [ 0.00163387,  0.00148482]])


    sampled = sampleCovarianceMatrix(pars, cov, ci=68, plot=True)
#     sampled = sampleCovarianceMatrix(pars, cov, plot=True)




  