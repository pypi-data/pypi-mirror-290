import numpy as np
import scipy.fft as fft
import scipy.signal.windows as window
import scipy.signal as scisig
from scipy.sparse.linalg import spsolve
import scipy.stats as scistats
import statistics
from typing import Optional, Tuple, List, Union


import numpy as np
from scipy import fft, signal
from typing import Optional, Tuple

def get_FFT(
    time_signal: np.ndarray,
    sampling_freq: float,
    scaling_factor: float,
    shift_bool: Optional[bool] = True,
    window_func: Optional[str] = 'hann',
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get FFT Function: find the Fast Fourier Transform (FFT) for a specific time signal

    Inputs:
        time_signal: (numpy array)
            time signal of interest.
        sampling_freq: (float)
            sampling frequency corresponding to the time signal of interest.
        scaling_factor: (float)
            scaling factor for the FFT
        shift_bool: (boolean, optional, default = True)
            boolean if the FFT should be shifted with fftshift or not.
        window_func: (str, optional, default = 'hann')
            string specifying the window function to apply. Options include 'hann', 'hamming', 'blackman', etc.

    Returns:
        FFT_Freq: (array like)
            FFT frequency array.
        FFT_signal: (array like)
            Absolute Value of the FFT of the time signal of interest.
    Notes:
        This function returns the absolute value of the FFT signal.
    """

    # Function:
    N = len(time_signal)
    T = 1 / sampling_freq

    # Dictionary to map window function names to scipy.signal window functions
    window_functions = {
        'hann': signal.windows.hann,
        'hamming': signal.windows.hamming,
        'blackman': signal.windows.blackman,
        'bartlett': signal.windows.bartlett,
        'flattop': signal.windows.flattop,
        'parzen': signal.windows.parzen,
        'bohman': signal.windows.bohman,
        'blackmanharris': signal.windows.blackmanharris,
        'nuttall': signal.windows.nuttall,
        'barthann': signal.windows.barthann,
        'cosine': signal.windows.cosine,
        'exponential': signal.windows.exponential,
        'tukey': signal.windows.tukey,
        'taylor': signal.windows.taylor,
    }

    if window_func in window_functions:
        hw = window_functions[window_func](N)
        A = len(hw) / sum(hw)
    else:
        hw = 1
        A = 1

    FFT_signal = fft.fft(time_signal * hw) * A * scaling_factor / N
    FFT_freq = fft.fftfreq(len(time_signal), T)

    # Initializing Output Variables
    output1 = None
    output2 = None

    if shift_bool:
        output1 = fft.fftshift(FFT_freq)
        output2 = abs(fft.fftshift(FFT_signal))
    else:
        output1 = FFT_freq
        output2 = abs(FFT_signal)

    return output1, output2


def spectral_kurtosis(
    time_signal: np.ndarray,
    sampling_freq: float,
    Nw: int,
    No: int,
    window_stft: Optional[str] = "hann",
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Spectral kurtosis function: Find the spectural kurtosis for a specific time signal and sampling frequency for a given window and overlap length.

    Inputs:
        time_signal: (numpy array)
            time signal of interest.
        sampling_freq: (float)
            sampling frequency corresponding to the time signal of interest.
        Nw: (int)
            Window Length.
        No: (int)
            Window Overlap Length.
        window_stft: (string, optional, default = 'hann')
            window type to be applied. This variable should not be set to "None"

    Returns:
        freq: (array like)
            STFT frequency array
        t_stft: (array like)
            STFT time points (from scipy.signal.stft function) corresponding to the time signal of interest
        signal_stft: (array like)
            STFT (from scipy.signal.stft function) corresponding to the time signal of interest
    Notes:
        Signal windowing is always applied
    """

    # Function:
    freq, t_stft, signal_stft = scisig.stft(
        x=time_signal, fs=sampling_freq, window=window_stft, nperseg=Nw, noverlap=No
    )
    SK_list = []
    for i in range(len(freq)):
        # SK = (1/len(t) * np.sum(np.abs(signal_stft[i,:])**4)) / ((  1/len(t) * np.sum(np.abs(signal_stft[i,:]))**2  )**2) - 2
        SK = (
            np.mean(np.abs(signal_stft[i, :]) ** 4)
            / (np.mean(((np.abs(signal_stft[i, :]) ** 2))) ** 2)
            - 2
        )  # Formula from MEV781 course
        SK_list.append(SK)
    return freq, t_stft, signal_stft, SK_list


def spectral_kurtosis_plot(  # this function is incomplete
    signal_array: np.ndarray,
    time_array: np.ndarray,
    sampling_freq: float,
    Nw: int,
    No: int,
    window_stft: Optional[str] = "hann",
) -> None:
    """
    this function is incomplete

    Get FFT Function

    Inputs:


    Returns:
        freq: (array like)
            STFT frequency array
        t_stft: (array like)
            STFT time points (from scipy.signal.stft function) corresponding to the time signal of interest
        signal_stft: (array like)
            STFT (from scipy.signal.stft function) corresponding to the time signal of interest
    Notes:
        Signal windowing is always applied
    """

    # Imports:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import cm

    Nw_list = 2 ** np.arange(2, Nw)
    No_list = Nw_list[1] / 2
    fig = plt.figure(figsize=(10, 10))
    fig.tight_layout()
    ax = plt.axes(projection="3d")
    ax.set_title(
        "Spectral Kurtosis Contour For Varying Window Lengths and Overlap Lengths"
    )
    ax.set_box_aspect(aspect=None, zoom=0.95)
    res = int(5e3)
    x_mat = np.zeros(shape=(len(Nw_list), res))
    y_mat = np.zeros(shape=(len(Nw_list), res))
    z_mat = np.zeros(shape=(len(Nw_list), res))

    for i in range(len(Nw_list)):
        # for i in range(len(No_list)):
        freq, t_stft, signal_stft, SK_i = spectral_kurtosis(
            signal=signal_array,
            sample_freq=len(signal_array) / time_array[-1],
            Nw=Nw_list[i],
            No=No_list,
        )

        ax[i, 0].set_title(
            "Window Length of {}, With Overlap Length {}".format(Nw_list[i], No_list[i])
        )
        # plt.plot(*abs(x_stft_damaged), color = 'green', label = 'Hanning Windowed Healthy FFT')#, alpha = 0.5)
        # plt.show()
        vmin_stft = 0
        vmax_stft = (np.max(signal_array) - np.min(signal_array)) / ((i * 7) + 20)
        # print(vmax_stft)
        ax[i, 0].pcolormesh(
            t_stft,
            freq,
            abs(signal_stft),
            shading="gouraud",
            vmin=vmin_stft,
            vmax=vmax_stft,
        )
        ax[i, 0].set_xlabel("Time [seconds]")
        ax[i, 0].set_ylabel("Frequency [Hz]")

        ax[i, 1].set_title(
            "Window Length of {}, With Overlap Length {}".format(Nw_list[i], No_list[i])
        )
        ax[i, 1].plot(SK_i, freq)
        ax[i, 1].set_xlabel("Spectural Kurtosis Magnitude")
        ax[i, 1].set_ylabel("Frequency [Hz]")
        # ax[j, i].plot(freq, SK_i, color = 'red')
        # ax[j, i].pcolormesh(t_stft_i, freqs_stft_i, abs(x_stft_damaged_i), shading='gouraud')

        # ax[j, i].set_ylim(None, 15000)
        # ax[j, i].set_xlim(None, 0.5)
    X = x_mat
    Y = y_mat
    Z = z_mat
    # Normalize to [0,1]
    norm = plt.Normalize(Z.min(), Z.max())
    colors_contour = cm.viridis_r(norm(Z))
    ax.plot_surface(X, Y, Z, cmap="viridis_r", lw=3, rstride=1, cstride=1, alpha=0.5)
    # ax.plot_wireframe(X, Y, Z, rstride = 3, cstride = 100)#, alpha=0.5)
    ax.contour(
        X, Y, Z, zdir="z", stride=5, cmap="viridis_r", linestyles="solid", offset=0
    )
    ax.contour(X, Y, Z, zdir="z", stride=5, colors="k", linestyles="solid")

    ax.set_xlabel("Frequency [Hz]", labelpad=20)
    ax.set_ylabel("Window Length", labelpad=20)
    ax.set_zlabel("SK Magnitude", labelpad=5)


def PerformBayesianGeometryCompensation(
    t: np.ndarray,
    N: int,
    M: int,
    e: np.ndarray = [],
    beta: Optional[float] = 10.0e10, #I actually think paper says the default value for beta is 1E10 not 10E10
    sigma: Optional[float] = 10.0,
) -> np.ndarray:
    # def PerformBayesianGeometryCompensation(t, N,M,e=[],beta=10.0e10,sigma=10.0):
    """
    Perform geometry compensation on an incremental shaft encoder with N sections measured over M revolutions.
    An algorithm that performs shaft encoder geometry compensation for arbitrary shaft speeds using Bayesian Geometry Compensation.
    Please reference the paper discussing the algorithm as described in the "References" section.

    Parameters
    ----------
    t :     1D numpy array of zeros crossing times.  The first zero crossing time indicates
            the start of the first section.  This array should therefore have exactly M*N + 1 elements.
    N:      The number of sections in the shaft encoder.
    M:      The number of complete revolutions over which the compensation must be performed.
    e:      An initial estimate for the encoder geometry.  If left an empty array, all sections are assumed equal.
    beta:   Precision of the likelihood function.
    sigma:  Standard deviation of the prior probability.

    Returns
    -------
    epost : An array containing the circumferential distances of all N sections.

    References:
    This function is adapted from the following paper,
    [1] D. H. Diamond, P. S. Heyns, and A. J. Oberholster, “Online Shaft Encoder Geometry Compensation for Arbitrary Shaft Speed Profiles Using Bayesian Regression,” Mechanical Systems and Signal Processing, vol. 81, pp. 402–418, Dec. 2016, doi: 10.1016/j.ymssp.2016.02.060.
    Copyright (C) 2016 Dawie Diamond, dawie.diamond@yahoo.com

    www.up.ac.za/caim
    www.caimlabs.co.za

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/gpl.html.

    """
    import sympy as sp
    from scipy.sparse.linalg import spsolve
    
    if len(t) != M * N + 1:
        print(
            "Input Error: The vector containing the zero-crossing times should contain exactly N*M + 1 values"
        )
        # print('test')
        raise SystemExit
    if len(e) != 0 and len(e) != N:
        print(
            "Input Error The encoder input should either be an empty list or a list with N elements"
        )
        raise SystemExit
    # Initialize matrices
    A = np.zeros((2 * M * N - 1, N + 2 * M * N))
    B = np.zeros((2 * M * N - 1, 1))
    # A = np.empty((2 * M * N - 1, N + 2 * M * N)) # Use empty and not zeros to save on memory usage
    # B = np.empty((2 * M * N - 1, 1)) # Use empty and not zeros to save on memory usage
    # Calculate zero-crossing periods
    T = np.ediff1d(t)

    # Insert Equation (11)
    A[0, :N] = np.ones(N)
    B[0, 0] = 2 * np.pi
    # Insert Equation (9) into A
    deduct = 0
    for m in range(M):
        if m == M - 1:
            deduct = 1
        for n in range(N - deduct):
            nm = m * N + n
            A[1 + nm, n] = 3.0
            A[1 + nm, N + nm * 2] = -1.0 / 2 * T[nm] ** 2
            A[1 + nm, N + nm * 2 + 1] = -2 * T[nm]
            A[1 + nm, N + (nm + 1) * 2 + 1] = -1 * T[nm]
    # Insert Equation (10) into A
    deduct = 0
    for m in range(M):
        if m == M - 1:
            deduct = 1
        for n in range(N - deduct):
            nm = m * N + n
            A[M * N + nm, n] = 6.0
            A[M * N + nm, N + nm * 2] = -2 * T[nm] ** 2
            A[M * N + nm, N + (nm + 1) * 2] = -1 * T[nm] ** 2
            A[M * N + nm, N + nm * 2 + 1] = -6 * T[nm]
    # Initialize prior vector
    m0 = np.zeros((N + 2 * M * N, 1))
    # Initialize and populate covariance matrix of prior
    Sigma0 = np.identity(N + 2 * M * N) * sigma**2
    # Populate prior vector
    if len(e) == 0:
        eprior = np.ones(N) * 2 * np.pi / N
    else:
        eprior = np.array(e) * 1.0
    m0[:N, 0] = eprior * 1.0
    for m in range(M):
        for n in range(N):
            nm = m * N + n
            m0[N + nm * 2 + 1, 0] = m0[n, 0] / T[nm]
    # Solve for mN (or x)

    # l1 = len(A) # Commented out as this variable is not used anywhere
    # l2 = len(A.T) # Commented out as this variable is not used anywhere
    # l3 = len(B) # Commented out as this variable is not used anywhere

    SigmaN = Sigma0 + beta * A.T.dot(A)
    BBayes = Sigma0.dot(m0) + beta * A.T.dot(B)

    mN = np.array([spsolve(SigmaN, BBayes)]).T
    # Normalize encoder increments to add up to 2 pi
    epost = mN[:N, 0] * 2 * np.pi / (np.sum(mN[:N, 0]))
    # Return encoder geometry
    return epost


def maketime(X: np.ndarray, Fs: float) -> np.ndarray:
    """
    X = Signal
    Fs = sampling frequency

    Returns:
        time
    """
    t0 = 0
    t1 = len(X) / Fs
    t = np.arange(t0, t1 + 1 / Fs, 1 / Fs)
    return t


def getrpm(
    Tacho: np.ndarray,
    Fs: float,
    TrigLevel: float,
    Slope: int,
    PPRM: int,
    NewSampleFreq: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    1. tacho = Tachometer Signal
    2. Fs = Sampling Frequency in
    3. triglevel =  trigger level defined by author for a pulse
    4. Slope = Positive or negative value for positive or negative pulses
    5. pprm = Tachometer pulses per revolution
    6. NewSampleFreq = Reinterpolation sampling frequency

    """

    if type(Tacho) == list:
        Tacho = np.array(Tacho)

    y = np.sign(Tacho - TrigLevel)
    dy = np.diff(y)

    tt = maketime(dy, Fs)
    Pos = []
    cnt = 0
    if Slope > 0:
        for i in dy > 0.8:
            if i == True:
                Pos.append(cnt)
            cnt += 1
        # ZC_times = tt[dy > 0.8]
    if Slope < 0:
        for i in dy < -0.8:
            if i == True:
                Pos.append(cnt)
            cnt += 1
        # ZC_times = tt[dy < 0.8]
    yt = tt[Pos]

    dt = np.diff(yt)
    dt = np.hstack([dt, np.array([dt[-1]])])

    Spacing = 2 * np.pi * np.ones(len(dt)) / PPRM  # Basic Spacing - radians

    rpm = (60 / (2 * np.pi)) * ((Spacing) / dt)
    b = [0.25, 0.5, 0.25]
    a = 1
    rpm = scisig.filtfilt(b, a, rpm)
    # print(rpm.shape)
    N = int(np.max(tt) * (NewSampleFreq) + 1)

    trpm = np.linspace(0, np.max(tt), N)

    rpm = np.interp(trpm, yt, rpm)
    Pos = []
    cnt = 0
    for i in np.isnan(rpm):
        if i == False:
            Pos.append(cnt)
        cnt += 1

    return trpm[Pos], rpm[Pos], yt  # yt = zero crossing times (i think?)


def getrpm_BCG(
    Tacho: np.ndarray,
    Fs: float,
    TrigLevel: float,
    Slope: int,
    PPRM: int,
    NewSampleFreq: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    1. tacho = Tachometer Signal
    2. Fs = Sampling Frequency in
    3. triglevel =  trigger level defined by author for a pulse
    4. Slope = Positive or negative value for positive or negative pulses
    5. pprm = Tachometer pulses per revolution
    6. NewSampleFreq = Reinterpolation sampling frequency

    References:
    This function is adapted from the following paper,
    [1] D. H. Diamond, P. S. Heyns, and A. J. Oberholster, “Online Shaft Encoder Geometry Compensation for Arbitrary Shaft Speed Profiles Using Bayesian Regression,” Mechanical Systems and Signal Processing, vol. 81, pp. 402–418, Dec. 2016, doi: 10.1016/j.ymssp.2016.02.060.
    Copyright (C) 2016 Dawie Diamond, dawie.diamond@yahoo.com

    www.up.ac.za/caim
    www.caimlabs.co.za

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/gpl.html .
    """

    if type(Tacho) == list:
        Tacho = np.array(Tacho)

    y = np.sign(Tacho - TrigLevel)
    dy = np.diff(y)

    tt = maketime(dy, Fs)
    Pos = []
    cnt = 0
    if Slope > 0:
        for i in dy > 0.8:
            if i == True:
                Pos.append(cnt)
            cnt += 1

    if Slope < 0:
        for i in dy < -0.8:
            if i == True:
                Pos.append(cnt)
            cnt += 1

    yt = tt[Pos]  # zero crossings term

    dt = np.diff(yt)
    dt = np.hstack([dt, np.array([dt[-1]])])
    # print(dt, dt.shape)
    # Spacing = 2 * np.pi * np.ones(len(dt))/PPRM #Basic Spacing - radians
    """
    Bayesian Geometric Compensation - Modification To getrpm -------------------------------------------------------
    """
    N_BGC = int(PPRM)
    M_BGC = int(len(yt) // N_BGC)
    epost_BGC = PerformBayesianGeometryCompensation(
        t=yt[0 : int(M_BGC * N_BGC + 1)], N=N_BGC, M=M_BGC, e=[]
    )  # [Radians]
    Spacing = (np.tile(epost_BGC, M_BGC + 1))[0 : len(yt)]  # [Radians]
    """
    Displacement With Respect To Time Variables For Ploting:
    """
    disp = np.cumsum(Spacing)  # angular displacment [Radians]
    t_disp = np.cumsum(dt)  # associated time for angular displacement
    # disp = np.cumsum(epost_BGC)
    # for i in range(0, len(Spacing)):
    # for i in range(0, len(epost_BGC)):
    #     # disp.append(np.sum(Spacing[0:i]/dt[i]))
    #     disp.append(np.sum(epost_BGC[0:i]))
    """
    --------------------------------------------------------------------------------------------------------------
    """
    rpm = (60 / (2 * np.pi)) * ((Spacing) / dt)
    b = [0.25, 0.5, 0.25]
    a = 1
    rpm = scisig.filtfilt(b, a, rpm)
    # print(rpm.shape)
    N = int(np.max(tt) * (NewSampleFreq) + 1)

    trpm = np.linspace(0, np.max(tt), N)

    rpm = np.interp(trpm, yt, rpm)
    Pos = []
    cnt = 0
    for i in np.isnan(rpm):
        if i == False:
            Pos.append(cnt)
        cnt += 1

    # return Spacing, trpm[Pos], rpm[Pos]
    return (
        t_disp,
        disp,
        trpm[Pos],
        rpm[Pos],
    )  # angular time, angular displacement, time for speed graph, rotational speed


def filter(order: int, F_cutoff: np.ndarray, Fs: float, x: np.ndarray) -> np.ndarray:
    """
    Input:
    filter order: (integer), cutoff limits, Sampling frequency, signal
    """
    F_cutoff = np.array(F_cutoff)
    nyq = 0.5 * Fs
    F_c = F_cutoff / nyq
    sos = scisig.butter(N=order, Wn=F_c, btype="bandpass", analog=False, output="sos")
    filtered = scisig.sosfilt(sos, x)
    return filtered


# filter_low, filter_high = [5500, 9000] #From SK contour
# # filter_low, filter_high = [6000, 9500] #From SK contour


def get_statistics(
    data: np.ndarray, round_to: Optional[int] = 4
) -> Tuple[float, float, float, float, float, float, float, float]:
    """
    Input:
    data (array)
    round_to (int, optional)

    Returns:
    minimum, maximum, mean, variance, skewness, kurtosis, Root Mean Square (RMS), Crest Factor (CF)
    """
    minn = np.round(np.min(data), round_to)
    maxx = np.round(np.max(data), round_to)

    mean = np.round(np.mean(data), round_to)
    var = np.round(statistics.variance(data), round_to)
    skew = np.round(scistats.skew(data), round_to)
    kurtosis = np.round(scistats.kurtosis(data), round_to)
    RMS = np.round(np.sqrt(np.sum(data**2)), round_to)
    CF = np.round(np.max(data) / np.sqrt(np.sum(data**2)), round_to)

    return minn, maxx, mean, var, skew, kurtosis, RMS, CF


def get_displacement_signal(
    zero_crossings: np.ndarray, time_signal: np.ndarray
) -> tuple[np.ndarray, int]:
    """
    Calculate the displacement signal based on the zero crossings and time signal.

    Args:
        zero_crossings (np.ndarray): An array of zero crossings.
        time_signal (np.ndarray): An array of time values corresponding to the raw signal of interest.

    Returns:
        tuple[np.ndarray, int]: A tuple containing the displacement signal corresponding to the signal of interest and the number of rotations.

    Note:
        This code is written for a Once Per Revolution (OPR) tacho signal. See getrpm_BCG for a Multiple
        Pulse per Revolution (MPR) tacho signal.
    """
    num_rotations = len(zero_crossings) - 1
    ones_array = np.ones(len(zero_crossings))
    ones_array[0] = 0  # cumulative displacement is zero at the beginning
    cumulative_displacement = np.cumsum(ones_array * np.pi * 2)  # Radians

    displacement_signal = np.interp(
        time_signal, zero_crossings, cumulative_displacement
    )

    return displacement_signal, num_rotations


def order_tracking(
    num_shaft_rot: int,
    disp_signal: np.ndarray,
    signal: np.ndarray,
    num_added_interp_points: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Perform order tracking on a signal of interest.

    Args:
        num_shaft_rot (int): Total number of shaft rotations corresponding to the signal of interest.
        disp_signal (np.ndarray): Displacement signal obtained from tachometer speed signal. Use BGC tachometer speed signal if applicable.
        signal (np.ndarray): Signal of interest. Signal you want to order track
        num_added_interp_points (int): Number of interpolated points per shaft revolution.

    Returns:
        Tuple[np.ndarray, np.ndarray]: A tuple containing the signal orders and the order tracked signal.

    Raises:
        None

    Examples:
        >>> num_shaft_rot = 10
        >>> disp_signal = np.array([0.1, 0.2, 0.3, 0.4])
        >>> signal = np.array([1, 2, 3, 4])
        >>> num_added_interp_points = 5
        >>> order_tracking(num_shaft_rot, disp_signal, signal, num_added_interp_points)
        (array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.]), array([1., 2., 3., 4., 1., 2., 3., 4., 1., 2., 3.]))
    Note:
        Note that if you would like to take the FFT of the order tracked signal you need to account for the updated sampling frequency corresponding to the order tracked signal. Thus can use Fs = 1/(signal_orders[1] - signal_orders[0])
    """
    points_per_rot = int(
        (num_added_interp_points + len(disp_signal) / num_shaft_rot) * num_shaft_rot
    )

    signal_orders = np.linspace(0, num_shaft_rot, points_per_rot)
    signal_OT = np.interp(signal_orders, disp_signal / (2 * np.pi), signal)

    return signal_orders, signal_OT


def TSA(
    raw_signal: np.ndarray,
    Nr: int,
    speed: float,
    sampling_frequency: float,
    Ns: Optional[int] = None,
) -> np.ndarray:
    """
    Time Synchronous Averaging (TSA) is a signal processing method used to reduce noise and extract periodic components from a signal.

    THIS FUNCTION ASSUMES CONSTANT SPEED!!!

    Parameters
    ----------
    raw_signal : np.ndarray
        The raw input signal to be processed. This signal should contain more revolutions than the specified Nr value.
    Nr : int
        The number of rotations to be be considered from the time signal. The length of the signal should be perfectly divisible by Nr
    speed: float
        The rotational speed of the shaft in RPM corresponding to the input signal.
    sampling_frequency: float
        The sampling frequency of the signal.

    Optional Parameters
    -------------------
    Ns : int, optional
        The number of points per shaft rotation. This is usually set to the number of points per shaft rotation. If not provided, Ns is calculated from the speed and sampling frequency.
        One might want to provide this variable if an interpolated signal is provided where the number of points per shaft rotation does not correspond to the calculated value from the speed and sampling frequency.

    Returns
    -------
    np.ndarray
        The processed signal after applying TSA.
    """
    if Ns is None:
        Ns = int(
            1 / (speed / 60) * sampling_frequency
        )  # Number of points per shaft rotation

    # Ns = len(signal) // Nr # number of points for averaging. This is usually set to the number of points per shaft rotation - THIS ISNT A CLEVER WAY TO DO IT

    signal = raw_signal[
        : Nr * Ns
    ]  # contracting the signal to the correct length for the number of rotations considered

    sig_list = np.zeros(shape=(Nr, Ns))
    for i in range(0, Nr):
        sig_list[i, :] = signal[i * Ns : Ns + i * Ns]

    return np.resize((1 / Nr) * np.sum(sig_list, axis=0), len(signal))
