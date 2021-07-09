import numpy as np
from scipy import ndimage as nd
from scipy.special import cosdg, sindg


def _summary(mat, name):
    print(f"{name}\tshape:{mat.shape}\tmax:{mat.max():.2f} min:{mat.min():.2f}")
    pass


class Deformer:
    def __init__(self, translation=0, zoom=0, elastic_magnitude=0, sigma=1, angle=0, nearest=False, debug=False):
        self.translation = translation
        self.zoom = zoom
        self.elastic_magnitude = elastic_magnitude
        self.sigma = sigma
        self.angle = angle
        self.nearest = nearest

        # Build a gaussian filter for elastic distortion
        if elastic_magnitude:
            self.nrounds = 2
            nsds = 2
            sigma //= self.nrounds
            filt = np.exp(-.5 * np.linspace(-nsds, nsds, int(2*nsds*sigma+1)) ** 2)
            filt /= filt.sum()
            if debug:
                print(f"Gaussian Filter Range: {filt.max():.4f}-{filt.min():.4f} "
                      f"Ratio:{filt.max()/filt.min():.2f} Sum:{filt.sum()}")
            self.filt = filt

        self.summary = _summary if debug else lambda _, __: None

    def __str__(self):
        print('Elastic Translation:{:} Zoom:{} Mag:{:d} Sig:{:d} Angle:{} Interpolation:{}'.format(
            self.translation, self.zoom, self.elastic_magnitude, self.sigma, self.angle,
            'Nearest' if self.nearest else 'Linear'))

    def __call__(self, inpt):
        # Degenerate Case
        if not (self.elastic_magnitude or self.translation or self.angle or self.zoom):
            return inpt

        b, h, w = inpt.shape
        _hwidx = np.indices((h, w)).astype('float')
        target = np.stack([_hwidx for _ in range(b)])
        self.summary(target, "initial traget")

        if self.elastic_magnitude:
            # Elastic
            elast = self.elastic_magnitude * np.random.normal(size=(b, 2, h, w))
            for _ in range(self.nrounds):
                for ax in (-1, -2):
                    nd.correlate1d(elast, self.filt, axis=ax, output=elast)
            target += elast
            self.summary(elast, "elastic")

        # Zoom and Rotate
        if self.zoom or self.angle:
            # Center at 'about' half way
            origin = np.random.uniform(.4, .6, size=(b, 2, 1, 1)) * np.array((h, w)).reshape((1, 2, 1, 1))
            target -= origin
            self.summary(origin, "origin")

            # Zoom
            if self.zoom:
                zoomer = np.exp(self.zoom * np.random.uniform(-1, size=(b, 2, 1, 1)))
                target *= zoomer
                self.summary(zoomer, "zoom")

            # Rotate
            if self.angle:
                theta = self.angle * np.random.uniform(-1, size=b)
                c, s = cosdg(theta), sindg(theta)
                rotate = np.array([[c, -s], [s, c]])
                rotate = np.moveaxis(rotate, -1, 0)  # b x 2 x 2
                for i in range(b):
                    target[i] = np.tensordot(rotate[i], target[i], axes=(0, 0))
                self.summary(rotate, "rotate")

            # Uncenter
            target += origin

        # Make sure you do not go below zero along the width (vertical axis because of Transpose)
        least_vert_disp = target[:, 0, 0].min(axis=-1)
        self.summary(least_vert_disp[:, None, None], "least_vert_disp")
        target[:, 0] -= least_vert_disp[:, None, None]

        if self.translation:
            transln = self.translation * np.random.uniform(-1, size=(b, 2, 1, 1))
            transln[:, 0] = -2 * np.abs(transln[:, 0])          # Along slab width translation is (0, 2translation)
            target += transln
            self.summary(transln, "translation")

        for i in range(b):
            self.summary(target[i, 0], f"{i} final traget y")
            self.summary(target[i, 1], f"{i} final traget x")
        transy = np.clip(target[:, 0], 0, h - 1 - .001)
        transx = np.clip(target[:, 1], 0, w - 1 - .001)

        output = np.empty_like(inpt)

        if self.nearest:
            vert = np.rint(transy).astype(int)
            horz = np.rint(transx).astype(int)
            for i in range(b):
                output[i] = inpt[i, vert[i], horz[i]]
        else:
            topp = np.floor(transy)
            left = np.floor(transx)
            fraction_y = transy - topp
            fraction_x = transx - left
            topp = topp.astype('int32')
            left = left.astype('int32')

            for i in range(b):
                output[i] = inpt[i, topp, left] * (1 - fraction_y) * (1 - fraction_x) + \
                            inpt[i, topp, left + 1] * (1 - fraction_y) * fraction_x + \
                            inpt[i, topp + 1, left] * fraction_y * (1 - fraction_x) + \
                            inpt[i, topp + 1, left + 1] * fraction_y * fraction_x

        self.summary(inpt, "input")
        self.summary(output, "output")
        return output


class Noiser:
    def __init__(self, num_blots=0, erase_fraction=.5, minsize=0, maxsize=0):
        self.num_blots = num_blots
        self.erase_fraction = erase_fraction
        self.minsize = minsize
        self.maxsize = maxsize

    def __call__(self, inpt):
        batch_sz, h, w = inpt.shape
        size = batch_sz, self.num_blots
        colors = np.random.binomial(n=1, p=1-self.erase_fraction, size=size)
        xs = np.random.randint(h, size=size)
        dxs = np.random.randint(self.minsize, self.maxsize, size=size)
        ys = np.random.randint(w, size=size)
        dys = np.random.randint(self.minsize, self.maxsize, size=size)
        for i in range(batch_sz):
            for x, dx, y, dy, c in zip(xs[i], dxs[i], ys[i], dys[i], colors[i]):
                inpt[i, x:(x+dx), y:(y+dy)] = c
        return inpt
