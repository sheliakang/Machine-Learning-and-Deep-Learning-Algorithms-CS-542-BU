import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.io
from scipy import linalg


def feature_normalize(samples):
    """
    Feature-normalize samples
    :param samples: samples.
    :return: normalized feature
    """
    mu = np.mean(samples, axis = 0)
    samples_norm = samples-mu
    std = np.std(samples_norm, axis=0)
    samples_norm = samples_norm/std
    return samples_norm, mu, std
    #pass


def get_usv(samples_norm):
    no_samples = samples_norm.shape[0]
    #n = samples_norm.shape[1]
    #U = np.zeros(n)
    #S = np.zeros(n)
    sigma =  np.divide((np.dot((samples_norm.T),samples_norm)),no_samples)
    U, S, V = linalg.svd(sigma)
    
    return U, S, V
    
def project_data(samples, U, K):
    """
    Computes the reduced data representation when
    projecting only on to the top "K" eigenvectors
    """
    z = np.zeros((samples.shape[0], K))
    reduced_U = U[:,:K]
    z = np.dot(samples,reduced_U)
    return z


def recover_data(z, U, K):
    recovered_sample = np.zeros((z.shape[0], U.shape[0]))
    reduced_U = U[:,:K]
    recovered_sample = np.dot(z, (reduced_U.T))
    return recovered_sample


def main():
    datafile = 'data/data1.mat'
    mat = scipy.io.loadmat(datafile)
    samples = mat['X']

    plt.figure(figsize=(7, 7))
    plt.scatter(samples[:, 0], samples[:, 1], s=30, facecolors='none', edgecolors='b')
    plt.title("Example Dataset", fontsize=18)
    plt.grid(True)
    # Feature normalize

    samples_norm, mu, std = feature_normalize(samples)

    # Run SVD

    U, S, V = get_usv(samples_norm)

    # output the top principal component (eigen- vector) found
    # should expect to see an output of about [-0.707 -0.707]"
    print('Top principal component is ', U[:, 0])


    plt.figure(figsize=(7, 7))
    plt.scatter(samples[:, 0], samples[:, 1], s=30, facecolors='none', edgecolors='b')
    plt.title("Example Dataset: PCA Eigenvectors Shown", fontsize=18)
    plt.xlabel('x1', fontsize=18)
    plt.ylabel('x2', fontsize=18)
    plt.grid(True)
    # To draw the principal component, you draw them starting
    # at the mean of the data

    # IMPLEMENT PLOT
    plt.plot([mu[0], mu[0] + 1.5*S[0]*U[0,0]], 
         [mu[1], mu[1] + 1.5*S[0]*U[0,1]],
        color='red',linewidth=3,
        label='First Principal Component')
    plt.plot([mu[0], mu[0] + 1.5*S[1]*U[1,0]], 
         [mu[1], mu[1] + 1.5*S[1]*U[1,1]],
        color='fuchsia',linewidth=3,
        label='Second Principal Component')
    
    plt.legend(loc=4)

    # project the first example onto the first dimension
    # should see a value of about 1.481"

    z = project_data(samples_norm, U, 1)
    print('Projection of the first example is %0.3f.' % float(z[0]))
    recovered_sample = recover_data(z, U, 1)
    print('Recovered approximation of the first example is ', recovered_sample[0])

    plt.figure(figsize=(7, 7))
    plt.scatter(samples_norm[:, 0], samples_norm[:, 1], s=30, facecolors='none',
                edgecolors='b', label='Original Data Points')
    plt.scatter(recovered_sample[:, 0], recovered_sample[:, 1], s=30, facecolors='none',
                edgecolors='r', label='PCA Reduced Data Points')

    plt.title("Example Dataset: Reduced Dimension Points Shown", fontsize=14)
    plt.xlabel('x1 [Feature Normalized]', fontsize=14)
    plt.ylabel('x2 [Feature Normalized]', fontsize=14)
    plt.grid(True)

    for x in range(samples_norm.shape[0]):
        plt.plot([samples_norm[x, 0], recovered_sample[x, 0]], [samples_norm[x, 1], recovered_sample[x, 1]], 'k--')

    plt.legend(loc=4)
    plt.xlim((-2.5, 2.5))
    plt.ylim((-2.5, 2.5))
    plt.show()


if __name__ == '__main__':
    main()
