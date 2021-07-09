import numpy as np
from scipy import ndimage as nd


class VerticalAlign:
    def __init__(self, imght):
        self.img_mid = imght//2
        sigma = imght / 16
        radius = int(2 * sigma + 0.5)
        gaussian_kernel = np.exp((-1 / 2*sigma*sigma) * np.arange(-radius, radius+1) ** 2)
        self.gaussian_kernel = gaussian_kernel / gaussian_kernel.sum()
        self.close_struct = np.ones((1, imght // 4))

    def __call__(self, imgarr):
        closed = nd.binary_closing(imgarr, structure=self.close_struct)
        hist = np.sum(closed, axis=1).astype('float')
        gauss_hist = nd.filters.correlate1d(hist, self.gaussian_kernel, mode='constant', cval=0)
        d_gauss_hist = nd.filters.convolve(gauss_hist, [-1, 0, 1])
        base = np.argmax(d_gauss_hist)
        top = np.argmin(d_gauss_hist[:base])
        midline = (top+base)//2

        # print(f">>> {top}-{base} xht({base-top}) mid({midline})")
        absdiff = abs(midline - self.img_mid)
        if absdiff < 5:
            return imgarr

        zeros = np.zeros((absdiff, imgarr.shape[1]))
        if midline > self.img_mid:
            return np.vstack((imgarr[absdiff:], zeros))
        else:
            return np.vstack((zeros, imgarr[:-absdiff]))
