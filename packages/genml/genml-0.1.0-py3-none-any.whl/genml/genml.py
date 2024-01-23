"""
Generate realizations of Mittag-Leffler noise.
"""
import numpy as np
import warnings
import random
from tqdm import tqdm
from .mittag_leffler import ml

class MLN(object):
    """
    The MLN (Mittag-Leffler Noise) class.

    This class generates realizations of Mittag-Leffler noise.
    It is instantiated with T (total length of the noise trajectory), c (scale parameter),
    lamda (exponent parameter), and tau (time scale).
    """

    def __init__(self, T, c, lamda, tau):
        """
        Instantiate the MLN class.

        Parameters:
        - T: Total length of the noise trajectory (int).
        - c: Scale parameter (float).
        - lamda: Exponent parameter (0 < lamda < 2).
        - tau: Time scale parameter (0 < tau <= 10000).
        """
        if not isinstance(T, int) or T <= 0:
            raise TypeError("Length of trajectories must be a positive int.")
        if lamda <= 0 or lamda >= 2:
            raise ValueError("Lamda parameter must be in interval (0, 2).")
        if tau > 10000 or tau <= 0:
            raise ValueError("Tau parameter must be in interval (0, 10000].")       
        self.T = T
        self.c = c
        self.lamda = lamda
        self.tau = tau
        self.acvs = []


    def _mln(self):
        """
        Sample the Mittag-Leffler noise.

        Returns an array of noise values using the Davies-Harte method.
        """
        Z = np.random.normal(0.0, 1.0, 2 * self.T)
        return self.apply_Daviesharte(Z)


    def compute_autocovariance(self, lag):
        """
        Calculate the autocovariance of Mittag-Leffler noise.

        Parameters:
        - lag: Time lag for autocovariance computation (int).

        Returns the autocovariance value at the specified lag.
        """
        lag = -(abs(lag) / self.tau) ** self.lamda
        return self.c * ml(lag, alpha=self.lamda) / (self.tau ** self.lamda)
    

    def generate_A(self):
        """
        Generate the eigenvalues of a circulant matrix.

        This function is used in the Davies-Harte method for generating
        Mittag-Leffler noise. It computes and returns the eigenvalues of a
        circulant matrix formed from the autocovariance sequence.
        
        Returns an array of eigenvalues.
        """
        ls0 = list([int(25*i) for i in range(4, 40)]) 
        ls = list(range(1, 10)) + list([int(2.5 * i) for i in range(4, 40)]) + ls0 + list(np.array(ls0) * 10) \
            +list(np.array(ls0) * 100) + list(np.array(ls0) * 1000) + list(np.array(ls0) * 10000) + list(np.array(ls0) * 100000)             
        self.acvs = [self.compute_autocovariance(i) for i in range(self.T)]
        first_row = self.acvs + [self.compute_autocovariance(self.T)] + self.acvs[1:][::-1]
        A0 = np.fft.fft(first_row).real
        if np.any(A0 < 0):
            warnings.warn("Not meeting the nonnegativity condition,"
                  "trajectory will be extracted from longer trajectories.")
            ls_ = [x for x in ls if x > self.T]
            for i in ls_: 
                T1 = self.T
                self.T = i
                add_acvs = [self.compute_autocovariance(i) for i in range(T1,self.T)]
                self.acvs += add_acvs
                first_row = self.acvs + [self.compute_autocovariance(self.T)] + self.acvs[1:][::-1]
                A1 = np.fft.fft(first_row).real
                if not np.any(A1 < 0):
                    return A1  
            return None  
        else:
            return A0  


    def apply_Daviesharte(self, Z):
        """
        Generate Mittag-Leffler noise using the Davies-Harte method.
        This method uses Fourier techniques to generate noise with
        Mittag-Leffler autocorrelation.
        
        Parameters:
        - Z: Array of normal random variables.

        Returns an array representing generated noise.
        """    
        A = self.generate_A()    
        Z = np.random.normal(0.0, 1.0, 2*self.T)
        Y = np.zeros(2 * self.T, dtype=complex)
        for i in range(2 * self.T):
            A_sqrt = np.sqrt(A[i] / (4 * self.T))
            if i == 0:
                Y[i] = A_sqrt * 2 * Z[i]
            elif i < self.T:
                Y[i] = A_sqrt * (Z[2*i-1] + 1j * Z[2*i])
            elif i == self.T:
                Y[i] = A_sqrt * 2 * Z[2*self.T-1]
            else:
                Y[i] = Y[2 * self.T - i].conjugate()
        # Fourier transform of the combined noise sequence
        X = np.fft.fft(Y)
        return X[:self.T].real
        

def mln(N, T, c, lamda, tau):
    """
    Generate multiple realizations of Mittag-Leffler noise of the same length.

    This function generates N trajectories of Mittag-Leffler noise, each of length T.
    If the given T does not satisfy the condition for nonnegative definiteness of the
    eigenvalues, the function finds the shortest length TT that satisfies this condition.
    It then generates noise trajectories based on this length TT and truncates them to the desired length T.

    Parameters:
    - N: Number of trajectories to generate (int).
    - T: Total length of the noise trajectory (int).
    - c: Scale parameter (float).
    - lamda: Exponent parameter (0 < lamda < 2).
    - tau: Time scale parameter (0 < tau <= 10000).
        
    Returns:
    A 2D array of size (N, T) containing the generated Mittag-Leffler noise trajectories.
    """  
    if not isinstance(N, int) or N <= 0:
        raise TypeError("Number of trajectories must be a positive int.")
    m = np.zeros((N, T))
    for i in tqdm(range(N)):
        if i == 0:
            m0 = MLN(T, c, lamda, tau)._mln()
            TT = m0.shape[0]
            if TT > T:
                rd = random.randint(0, TT - T)
                m[i, :] = m0[rd:rd + T]
            else:
                m[i, :] = m0
        else:
            if TT > T:
                rd = random.randint(0, TT - T)
                m[i, :] = MLN(TT, c, lamda, tau)._mln()[rd:rd + T]
            else:
                m[i, :] = MLN(T, c, lamda, tau)._mln()
    return m
