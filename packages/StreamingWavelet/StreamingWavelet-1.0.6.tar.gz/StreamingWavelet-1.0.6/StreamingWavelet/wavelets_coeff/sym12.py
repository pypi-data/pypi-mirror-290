""" Symlet 12 wavelet """


class Symlet12:
    """
    Properties
    ----------
     near symmetric, orthogonal, biorthogonal

    All values are from http://wavelets.pybytes.com/wavelet/sym12/
    """
    __name__ = "Symlet Wavelet 12"
    __motherWaveletLength__ = 24  # length of the mother wavelet
    __transformWaveletLength__ = 2  # minimum wavelength of input signal

    # decomposition filter
    # low-pass
    decompositionLowFilter = [
        0.00011196719424656033,
        -1.1353928041541452e-05,
        -0.0013497557555715387,
        0.00018021409008538188,
        0.007414965517654251,
        -0.0014089092443297553,
        -0.024220722675013445,
        0.0075537806116804775,
        0.04917931829966084,
        -0.03584883073695439,
        -0.022162306170337816,
        0.39888597239022,
        0.7634790977836572,
        0.46274103121927235,
        -0.07833262231634322,
        -0.17037069723886492,
        0.01530174062247884,
        0.05780417944550566,
        -0.0026043910313322326,
        -0.014589836449234145,
        0.00030764779631059454,
        0.002350297614183465,
        -1.8158078862617515e-05,
        -0.0001790665869750869,
    ]

    # high-pass
    decompositionHighFilter = [
        0.0001790665869750869,
        -1.8158078862617515e-05,
        -0.002350297614183465,
        0.00030764779631059454,
        0.014589836449234145,
        -0.0026043910313322326,
        -0.05780417944550566,
        0.01530174062247884,
        0.17037069723886492,
        -0.07833262231634322,
        -0.46274103121927235,
        0.7634790977836572,
        -0.39888597239022,
        -0.022162306170337816,
        0.03584883073695439,
        0.04917931829966084,
        -0.0075537806116804775,
        -0.024220722675013445,
        0.0014089092443297553,
        0.007414965517654251,
        -0.00018021409008538188,
        -0.0013497557555715387,
        1.1353928041541452e-05,
        0.00011196719424656033,
    ]

    # reconstruction filters
    # low pass
    reconstructionLowFilter = [
        -0.0001790665869750869,
        -1.8158078862617515e-05,
        0.002350297614183465,
        0.00030764779631059454,
        -0.014589836449234145,
        -0.0026043910313322326,
        0.05780417944550566,
        0.01530174062247884,
        -0.17037069723886492,
        -0.07833262231634322,
        0.46274103121927235,
        0.7634790977836572,
        0.39888597239022,
        -0.022162306170337816,
        -0.03584883073695439,
        0.04917931829966084,
        0.0075537806116804775,
        -0.024220722675013445,
        -0.0014089092443297553,
        0.007414965517654251,
        0.00018021409008538188,
        -0.0013497557555715387,
        -1.1353928041541452e-05,
        0.00011196719424656033,
    ]

    # high-pass
    reconstructionHighFilter = [
        0.00011196719424656033,
        1.1353928041541452e-05,
        -0.0013497557555715387,
        -0.00018021409008538188,
        0.007414965517654251,
        0.0014089092443297553,
        -0.024220722675013445,
        -0.0075537806116804775,
        0.04917931829966084,
        0.03584883073695439,
        -0.022162306170337816,
        -0.39888597239022,
        0.7634790977836572,
        -0.46274103121927235,
        -0.07833262231634322,
        0.17037069723886492,
        0.01530174062247884,
        -0.05780417944550566,
        -0.0026043910313322326,
        0.014589836449234145,
        0.00030764779631059454,
        -0.002350297614183465,
        -1.8158078862617515e-05,
        0.0001790665869750869,
    ]
