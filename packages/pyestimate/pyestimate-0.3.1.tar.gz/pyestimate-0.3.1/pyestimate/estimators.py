# Author: Alexis Humblet
# 2024

import numpy as np
from scipy.signal import detrend, periodogram
from scipy import optimize

def sin_param_estimate(x, freq=None, use_fft=False, nfft=4096, brute_Ns=1000, detrend_type='constant'):
    """
    Estimate the parameters of a sinusoid (amplitude, frequency and phase). The sinusoid model is :math:`s[n] = A \cos(2 \pi f n + \phi)`.

    In the presence of white gaussian noise, the estimator implemented is the maximum likelihood estimator if `use_fft` is set to `False`.

    Parameters
    ----------
    x : array_like 
        A 1-D input sequence of real numbers.
    freq : float, optional
        Digital frequency of the input sinusoid (`freq = F/Fs` if `F` is the analog frequency and `Fs` is the sampling frequency). If `freq` is None or is not given, the frequency is estimated.
    use_fft: bool, optional
        If `True`, use a periodogram to estimate frequency. This should be used if the digital frequency is known to be in `[2/N, 1/2-2/N]`, with `N = len(x)` otherwise, set to `False`.
    nfft: int, optional
        Length of the FFT used if use_fft is `True`. 
    brute_Ns: int, optional
        Number of points to be used for the brute force search used if `use_fft` is `False`. Increase if frequency resolution is too coarse.
    detrend_type: {'linear', 'constant'}, optional
        Specifies how to detrend the input sequence. It is passed as the type argument to the `scipy.signal.detrend` function. Default to `constant`.

    Returns
    -------
    A: float
        Estimated amplitude of the sinusoid (> 0).
    f: float
        Estimated digital frequency of the sinusoid (or input frequency if `freq` was given as input parameter), in `]0, 0.5[`.
    phi: float
        Estimated phase of the sinusoid, in `[-pi, pi]`.

    Notes
    -----
    If `use_fft` is set to `False`, the estimator is the maximum likelihood estimator (MLE) for a sinusoid in white gaussian noise. If `use_fft` is set to `True`, the estimator is close to MLE (if the digital frequency is in `[2/N, 1/2-2/N]`) and is faster to compute.

    Examples
    --------
    Generate a noisy sinusoid for which we want to estimate amplitude, frequency and phase

    .. plot::
        :format: doctest
        :include-source: True

        >>> from pyestimate.estimators import sin_param_estimate
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> N = 20 # number of samples
        >>> f = 0.123456 # frequency to be estimated
        >>> A = 1.23456 # amplitude to be estimated
        >>> phi = np.pi/7 # phase to be estimated
        >>> sigma = 1 # standard deviation of WGN
        >>> n = np.arange(N)
        >>> s = A * np.cos(2*np.pi*f*n+phi) # original signal
        >>> w = np.random.default_rng(seed=0).normal(scale=sigma, size=N) # white gaussian noise
        >>> x = s+w # input signal for estimation: sine + noise

        Estimate sinusoid parameters
        
        >>> A_hat, f_hat, phi_hat = sin_param_estimate(x) # parameters estimation

        Reconstruct original signal from estimated parameters

        >>> s_hat = A_hat * np.cos(2*np.pi*f_hat*n+phi_hat) # estimated signal

        Plot the original signal, the input signal corrupted with noise and the reconstructed signal
        
        >>> plt.plot(n, s, linewidth=3.0, label='original signal')
        >>> plt.plot(n, x, label='corrupted signal')
        >>> plt.plot(n, s_hat, 'k--', label='estimated signal')
        >>> plt.xlabel('$n$')
        >>> plt.ylabel('$x[n]$')
        >>> plt.title('Sinusoidal frequency, amplitude and phase estimation in WGN')
        >>> plt.legend()
        >>> plt.grid()
        >>> plt.show()

    References
    ----------
    .. [1] Kay, S. M. (1997). Fundamentals of Statistical Signal Processing: Estimation Theory. Prentice Hall.

    
    """
    if detrend_type in {'linear', 'constant'}:
        x = detrend(x, type=detrend_type)
    
    N = len(x)
    n = np.arange(N)
    x = np.array(x).reshape((N,1))

    if freq is None:
        if use_fft:
            f, Pxx = periodogram(x.reshape(-1), nfft=nfft)
            freq = f[np.argmax(Pxx)]
        else:
            def J_func(f):
                f = f[0]
                c = np.cos(2*np.pi*f*n)
                s = np.sin(2*np.pi*f*n)
                H = np.vstack([c, s]).T
                return (-x.T @ H @ np.linalg.inv(H.T @ H) @ H.T @ x)[0,0]
            freq = optimize.brute(J_func, ((1e-12, 0.5-1e-12),), Ns=brute_Ns, finish=optimize.fmin)[0]
    
    c = np.cos(2*np.pi*freq*n)
    s = np.sin(2*np.pi*freq*n)
    H = np.vstack([c, s]).T
    alpha_hat = np.linalg.inv(H.T @ H) @ H.T @ x
    amp = np.linalg.norm(alpha_hat)
    phase = np.arctan2(-alpha_hat[1], alpha_hat[0])[0]

    return amp, freq, phase

def sin2d_param_estimate(x, freq=None, use_fft=False, nfft=[1024, 1024], brute_Ns=100):
    """
    Estimate the parameters of a 2D sinusoid (amplitude, frequencies and phase). The 2D sinusoid model is :math:`s[n,m] = A \cos(2 \pi (f_n n + f_m m) + \phi)`.

    In the presence of white gaussian noise, the estimator implemented is the maximum likelihood estimator if `use_fft` is set to `False`.

    Parameters
    ----------
    x : array_like 
        A 2-D input sequence of real numbers.
    freq : sequence of 2 floats, optional
        Digital frequencies of the input 2D sinusoid (`freq[i] = F[i]/Fs` if `F[i]` is the ith analog frequency and `Fs` is the sampling frequency). If `freq` is None or is not given, the frequency is estimated.
    use_fft: bool, optional
        If `True`, use a periodogram to estimate frequency. This is faster, but might be less accurate for frequencies close to 0 or 0.5.
    nfft: sequence of 2 ints, optional
        Length of the FFT used along each axis, if use_fft is `True`. 
    brute_Ns: int, optional
        Number of points to be used for the brute force search used if `use_fft` is `False`. Increase if frequency resolution is too coarse.
    
    Returns
    -------
    A: float
        Estimated amplitude of the sinusoid (> 0).
    f: list of 2 floats
        Estimated digital frequencies of the sinusoid (or input frequencies if `freq` was given as input parameter), in `]0, 0.5[`. The first frequency is the one corresponding to the row indexing.
    phi: float
        Estimated phase of the sinusoid, in `[-pi, pi]`.

    Notes
    -----
    If `use_fft` is set to `False`, the estimator is the maximum likelihood estimator (MLE) for a sinusoid in white gaussian noise. If `use_fft` is set to `True`, the estimator is close to MLE and is faster to compute.

    Examples
    -------- 
    
    .. plot::
        :format: doctest
        :include-source: True

        >>> from pyestimate import sin2d_param_estimate
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt

        Define a 2D sinusoidal signal, corrupted by white gaussian noise

        >>> N = 20
        >>> M = 80
        >>> fn0 = 0.089
        >>> fm0 = 0.05
        >>> A = 1.23454
        >>> phi = 0.5789
        >>> n, m = np.meshgrid(np.arange(N), np.arange(M), indexing='ij')
        >>> sigma2 = 0.2
        >>> x = A * np.cos(2*np.pi*(fn0*n+fm0*m) + phi) + np.random.default_rng(seed=0).normal(scale=np.sqrt(sigma2), size=(N,M)) # Noisy 2D sinusoid

        Estimate sinusoidal parameters and plot estimation

        >>> A_hat, f_hat, phi_hat = sin2d_param_estimate(x, brute_Ns=100) # parameters estimation
        >>> print(f'Estimated amplitude: {A_hat: .3f} (true value: {A: .3f})')
        >>> print(f'Estimated frequencies: {f_hat[0]: .3f}, {f_hat[1]: .3f} (true values: {fn0: .3f}, {fm0: .3f})')
        >>> print(f'Estimated phase: {phi_hat: .3f} (true values: {phi: .3f})')   
        >>> plt.subplot(121)
        >>> plt.imshow(x, vmin=np.min(x), vmax=np.max(x))
        >>> plt.title('Noisy input 2D sinusoid')
        >>> plt.subplot(122)
        >>> plt.imshow(A_hat * np.cos(2*np.pi*(f_hat[0]*n+f_hat[1]*m) + phi_hat), vmin=np.min(x), vmax=np.max(x))
        >>> plt.title('Estimated 2D sinusoid')
        >>> plt.show()

    """
    x = x - np.mean(x)
    N = x.shape[0]
    M = x.shape[1]
    n, m = np.meshgrid(np.arange(N), np.arange(M), indexing='ij')

    if freq is None:
        if use_fft:
            X = np.fft.fft2(x.reshape(N,M), s=nfft)
            imax = np.unravel_index(np.argmax(np.abs(X[:nfft[0]//2,:nfft[1]//2])**2), [nfft[0]//2,nfft[1]//2])
            fn = np.fft.fftfreq(nfft[0])[:nfft[0]//2][imax[0]]
            fm = np.fft.fftfreq(nfft[1])[:nfft[1]//2][imax[1]]
            freq = [fn, fm]
        else:
            x = np.array(x).reshape((N*M,1))
            def J_func(f):
                fn = f[0]
                fm = f[1]
                c = np.cos(2*np.pi*(fn*n+fm*m)).reshape(-1)
                s = np.sin(2*np.pi*(fn*n+fm*m)).reshape(-1)
                H = np.vstack([c, s]).T
                return (-x.T @ H @ np.linalg.inv(H.T @ H) @ H.T @ x)[0,0]
            freq = optimize.brute(J_func, ((1e-12, 0.5-1e-12),(1e-12, 0.5-1e-12),), Ns=brute_Ns, finish=optimize.fmin)

    fn = freq[0]
    fm = freq[1]
    c = np.cos(2*np.pi*(fn*n+fm*m)).reshape(-1)
    s = np.sin(2*np.pi*(fn*n+fm*m)).reshape(-1)
    H = np.vstack([c, s]).T
    x = np.array(x).reshape((N*M,1))
    alpha_hat = np.linalg.inv(H.T @ H) @ H.T @ x
    amp = np.linalg.norm(alpha_hat)
    phase = np.arctan2(-alpha_hat[1], alpha_hat[0])[0]

    return amp, freq, phase

def multiple_sin_param_estimate(x, p, freq=None, brute_Ns=100, detrend_type='constant'):
    """
    Estimate the parameters of multiple sinusoids (amplitudes, frequencies and phases). The signal model is :math:`s[n] = \sum_{i=1}^{p} A_i \cos(2 \pi f_i n + \phi_i)`.

    In the presence of white gaussian noise, the estimator implemented is the maximum likelihood estimator.

    Parameters
    ----------
    x : array_like 
        A 1-D input sequence of real numbers.
    p : int
        Number of sinusoids to be estimated.
    freq : sequence of p floats, optional
        Digital frequency of the input sinusoids (`freq = F/Fs` if `F` are the analog frequencies and `Fs` is the sampling frequency). If `freq` is None or is not given, the frequencies are estimated.
    brute_Ns: int, optional
        Number of points to be used for the brute force search. Increase if frequency resolution is too coarse, decrease to speed-up.
    detrend_type: {'linear', 'constant'}, optional
        Specifies how to detrend the input sequence. It is passed as the type argument to the `scipy.signal.detrend` function. Default to `constant`.

    Returns
    -------
    A: list of floats
        Estimated amplitude of the sinusoids (> 0).
    f: list of floats
        Estimated digital frequencies of the sinusoids (or input frequencies if `freq` was given as input parameter), in `]0, 0.5[`.
    phi: list of floats
        Estimated phases of the sinusoids, in `[-pi, pi]`.

    Notes
    -----
    The estimator is the maximum likelihood estimator (MLE) for sinusoids in white gaussian noise. Due to the use of a brute force optimization, it can only be used for a limited number of sinusoids (typically up to 5).

    Examples
    --------
    Generate a sum of noisy sinusoids for which we want to estimate amplitudes, frequencies and phases

    .. plot::
        :format: doctest
        :include-source: True

        >>> from pyestimate.estimators import multiple_sin_param_estimate
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> N = 40 # number of samples
        >>> f = [0.123456, 0.103456] # frequencies to be estimated
        >>> A = [1.23456, 1.34567] # amplitude to be estimated
        >>> phi = [0.0, np.pi/4] # phase to be estimated
        >>> p = len(A) # number of sinusoids
        >>> sigma = 1.0 # standard deviation of WGN
        >>> n = np.arange(N)
        >>> s = 0.0
        >>> for i in range(p):
        >>>     s += A[i] * np.cos(2*np.pi*f[i]*n+phi[i]) # original signal
        >>> w = np.random.default_rng(seed=0).normal(scale=sigma, size=N) # white gaussian noise
        >>> x = s+w # input signal for estimation: sine + noise

        Estimate sinusoid parameters
        
        >>> A_hat, f_hat, phi_hat = multiple_sin_param_estimate(x, p) # parameters estimation

        Reconstruct original signal from estimated parameters

        >>> s_hat = 0.0
        >>> for i in range(p):
        >>>     s_hat += A_hat[i] * np.cos(2*np.pi*f_hat[i]*n+phi_hat[i]) # estimated signal

        Plot the original signal, the input signal corrupted with noise and the reconstructed signal
        
        >>> plt.plot(n, s, linewidth=3.0, label='original signal')
        >>> plt.plot(n, x, label='corrupted signal')
        >>> plt.plot(n, s_hat, 'k--', label='estimated signal')
        >>> plt.xlabel('$n$')
        >>> plt.ylabel('$x[n]$')
        >>> plt.title('Sum of sinusoids: frequencies, amplitudes and phases estimation in WGN')
        >>> plt.legend()
        >>> plt.grid()
        >>> plt.show()

    References
    ----------
    .. [1] Kay, S. M. (1997). Fundamentals of Statistical Signal Processing: Estimation Theory. Prentice Hall.

    
    """
    if detrend_type in {'linear', 'constant'}:
        x = detrend(x, type=detrend_type)
    
    N = len(x)
    n = np.arange(N)
    x = np.array(x).reshape((N,1))

    if freq is None:
        def J_func(f):
            if not all(f[i] > f[i+1] for i in range(len(f) - 1)):
                return np.inf
            HH = []
            for ff in f:
                c = np.cos(2*np.pi*ff*n)
                s = np.sin(2*np.pi*ff*n)
                HH.append(c)
                HH.append(s)
            H = np.vstack(HH).T
            return (-x.T @ H @ np.linalg.inv(H.T @ H) @ H.T @ x)[0,0]
        freq = optimize.brute(J_func, ((1e-12, 0.5-1e-12),)*p, Ns=brute_Ns, finish=optimize.fmin)

    p = len(freq)
    HH = []
    for ff in freq:
        c = np.cos(2*np.pi*ff*n)
        s = np.sin(2*np.pi*ff*n)
        HH.append(c)
        HH.append(s)
    H = np.vstack(HH).T

    alpha_hat = np.linalg.inv(H.T @ H) @ H.T @ x
    amp = []
    phase = []
    for i in range(p):
        amp.append(np.linalg.norm(alpha_hat[2*i:2*i+2]))
        phase.append(np.arctan2(-alpha_hat[2*i+1], alpha_hat[2*i])[0])

    return amp, freq, phase

def pc_ar_estimator(x, p, detrend_type='constant'):
    """
    Principal component AR estimator: estimate the parameters of multiple sinusoids (amplitudes, frequencies and phases). The signal model is :math:`s[n] = \sum_{i=1}^{p} A_i \cos(2 \pi f_i n + \phi_i)`. This is faster than the MLE estimator implemented in `multiple_sin_param_estimate`, but less resilient to noise.

    Parameters
    ----------
    x : array_like 
        A 1-D input sequence of real numbers.
    p : int
        Number of sinusoids to be estimated.
    detrend_type: {'linear', 'constant'}, optional
        Specifies how to detrend the input sequence. It is passed as the type argument to the `scipy.signal.detrend` function. Default to `constant`.

    Returns
    -------
    A: list of floats
        Estimated amplitude of the sinusoids (> 0).
    f: list of floats
        Estimated digital frequencies of the sinusoids (or input frequencies if `freq` was given as input parameter), in `]0, 0.5[`.
    phi: list of floats
        Estimated phases of the sinusoids, in `[-pi, pi]`.

    Notes
    -----
    This optimator is suboptimal, but practical for a larger number of sinusoids than the MLE estimator implemented in `multiple_sin_param_estimate`.

    Examples
    --------
    Generate a sum of noisy sinusoids for which we want to estimate amplitudes, frequencies and phases

    .. plot::
        :format: doctest
        :include-source: True

        >>> from pyestimate.estimators import pc_ar_estimator
        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> N = 40 # number of samples
        >>> f = [0.12345, 0.10345, 0.05234, 0.05, 0.0351] # frequencies to be estimated
        >>> A = [1.23456, 1.34567, 1.0, 1.0, 1.0] # amplitude to be estimated
        >>> phi = [0.0, np.pi/4, 0.0, 0.0, 0.0] # phase to be estimated
        >>> p = len(A) # number of sinusoids
        >>> sigma = 0.01 # standard deviation of WGN
        >>> n = np.arange(N)
        >>> s = 0.0
        >>> for i in range(p):
        >>>     s += A[i] * np.cos(2*np.pi*f[i]*n+phi[i]) # original signal
        >>> w = np.random.default_rng(seed=0).normal(scale=sigma, size=N) # white gaussian noise
        >>> x = s+w # input signal for estimation: sine + noise

        Estimate sinusoid parameters
        
        >>> A_hat, f_hat, phi_hat = pc_ar_estimator(x, p) # parameters estimation

        Reconstruct original signal from estimated parameters

        >>> s_hat = 0.0
        >>> for i in range(p):
        >>>     s_hat += A_hat[i] * np.cos(2*np.pi*f_hat[i]*n+phi_hat[i]) # estimated signal

        Plot the original signal, the input signal corrupted with noise and the reconstructed signal
        
        >>> plt.plot(n, s, linewidth=3.0, label='original signal')
        >>> plt.plot(n, x, label='corrupted signal')
        >>> plt.plot(n, s_hat, 'k--', label='estimated signal')
        >>> plt.xlabel('$n$')
        >>> plt.ylabel('$x[n]$')
        >>> plt.title('Sum of sinusoids: frequencies, amplitudes and phases estimation in WGN')
        >>> plt.legend()
        >>> plt.grid()
        >>> plt.show()

    References
    ----------
    .. [1] Kay, S. M. (2013). Fundamentals of statistical signal processing. Volume III, Practical algorithm development. Prentice Hall.

    
    """
    if detrend_type in {'linear', 'constant'}:
        x = detrend(x, type=detrend_type)
    else:
        x = np.array(x)

    N = len(x)
    L = int(np.floor(3/4*N))
    Hf = np.vstack([x[i:i+N-L] for i in range(L-1, -1, -1)]).T
    Hb = np.vstack([x[i:i+N-L] for i in range(1, L+1, 1)]).T
    hf = x[L:]
    hb = x[:N-L]
    H = np.vstack([Hf, Hb])
    h = np.hstack([hf, hb])
    eigenvalues = np.flip(np.sort(np.linalg.eigvals(H.T @ H)))
    Hs = np.linalg.pinv(H, 0.5*(np.sqrt(eigenvalues[2*p-1])+np.sqrt(eigenvalues[2*p]))/eigenvalues[0])
    a_hat = -Hs @ h
    roots = np.polynomial.polynomial.polyroots(np.flip(np.hstack([[1], a_hat])))
    roots = roots[np.imag(roots)>=0]
    roots = roots[np.abs(np.angle(roots))/2/np.pi>1e-12]
    roots = roots[np.abs(np.angle(roots))/2/np.pi<0.5-1e-12]
    roots = roots[np.argsort(np.abs(np.abs(roots)-1))[:p]]
    freq = np.flip(np.sort(np.abs(np.angle(roots)/2/np.pi)))
    
    return multiple_sin_param_estimate(x, p, freq, detrend_type=None)