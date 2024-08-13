""" Symlet 10 wavelet """


class Symlet10:
    """
    Properties
    ----------
     near symmetric, orthogonal, biorthogonal

    All values are from http://wavelets.pybytes.com/wavelet/sym2/
    """
    __name__ = "Symlet Wavelet 10"
    __motherWaveletLength__ = 20  # length of the mother wavelet
    __transformWaveletLength__ = 2  # minimum wavelength of input signal

    # decomposition filter
    # low-pass
    decompositionLowFilter = [
        0.0007701598091144901,
        9.563267072289475e-05,
        -0.008641299277022422,
        -0.0014653825813050513,
        0.0459272392310922,
        0.011609893903711381,
        -0.15949427888491757,
        -0.07088053578324385,
        0.47169066693843925,
        0.7695100370211071,
        0.38382676106708546,
        -0.03553674047381755,
        -0.0319900568824278,
        0.04999497207737669,
        0.005764912033581909,
        -0.02035493981231129,
        -0.0008043589320165449,
        0.004593173585311828,
        5.7036083618494284e-05,
        -0.0004593294210046588,
    ]

    # high-pass
    decompositionHighFilter = [
        0.0004593294210046588,
        5.7036083618494284e-05,
        -0.004593173585311828,
        -0.0008043589320165449,
        0.02035493981231129,
        0.005764912033581909,
        -0.04999497207737669,
        -0.0319900568824278,
        0.03553674047381755,
        0.38382676106708546,
        -0.7695100370211071,
        0.47169066693843925,
        0.07088053578324385,
        -0.15949427888491757,
        -0.011609893903711381,
        0.0459272392310922,
        0.0014653825813050513,
        -0.008641299277022422,
        -9.563267072289475e-05,
        0.0007701598091144901,
    ]

    # reconstruction filters
    # low pass
    reconstructionLowFilter = [
        -0.0004593294210046588,
        5.7036083618494284e-05,
        0.004593173585311828,
        -0.0008043589320165449,
        -0.02035493981231129,
        0.005764912033581909,
        0.04999497207737669,
        -0.0319900568824278,
        -0.03553674047381755,
        0.38382676106708546,
        0.7695100370211071,
        0.47169066693843925,
        -0.07088053578324385,
        -0.15949427888491757,
        0.011609893903711381,
        0.0459272392310922,
        -0.0014653825813050513,
        -0.008641299277022422,
        9.563267072289475e-05,
        0.0007701598091144901,
    ]

    # high-pass
    reconstructionHighFilter = [
        0.0007701598091144901,
        -9.563267072289475e-05,
        -0.008641299277022422,
        0.0014653825813050513,
        0.0459272392310922,
        -0.011609893903711381,
        -0.15949427888491757,
        0.07088053578324385,
        0.47169066693843925,
        -0.7695100370211071,
        0.38382676106708546,
        0.03553674047381755,
        -0.0319900568824278,
        -0.04999497207737669,
        0.005764912033581909,
        0.02035493981231129,
        -0.0008043589320165449,
        -0.004593173585311828,
        5.7036083618494284e-05,
        0.0004593294210046588,
    ]
