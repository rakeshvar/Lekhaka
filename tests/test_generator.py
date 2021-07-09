import sys
import numpy as np
from PIL import Image

sys.path.append("..")
import telugu as lang
from Lekhaka import Scribe, Deformer, DataGenerator, Noiser

# Initialize
gray = .3
bsz_cols, bsz_rows = 3, 10
batch_size = bsz_cols * bsz_rows
slab_ht = 96
elastic_args0 = {
    'translation': 0,
    'zoom': .0,
    'elastic_magnitude': 0,
    'sigma': 1,
    'angle': 0,
    'nearest': True}
elastic_args1 = {
    'translation': 5,
    'zoom': .15,
    'elastic_magnitude': 0,
    'sigma': 30,
    'angle': 3,
    'nearest': True}
noise_args1 = {
    'num_blots': slab_ht // 3,
    'erase_fraction': .9,
    'minsize': 4,
    'maxsize': 9}
scribe_args = {
    'height': slab_ht,
    'hbuffer': 5,
    'vbuffer': 0,
    'nchars_per_sample': 10,
}

lang.select_labeler('cv')
alphabet_size = len(lang.symbols)

scriber = Scribe(lang, **scribe_args)
deformer = Deformer(**elastic_args1)
noiser = Noiser(**noise_args1)
gen = DataGenerator(scriber, deformer, noiser, batch_size)

# Generate Data
image, labels, image_lengths, label_lengths = gen.get()

# Print
print(scriber)
print(f"Image Shape:{image.shape}")
print(f"Max:{image.max()} Mean:{image.mean():.3f} Min:{image.min()}")
print(f"Type:{image.dtype}")
print(f"image_lengths: {image_lengths}")
print(f"label_lengths: {label_lengths}")
for i, l in enumerate(label_lengths):
    print(f"{i}: {labels[i][:l]}")

img = image.transpose((0, 2, 1, 3)).squeeze()
img[:, 0, :] = gray
img[:, :, 0] = gray
for (i, l) in enumerate(image_lengths):
    img[i, :, l] = gray

img = np.hstack([np.vstack(img[i:(i + bsz_rows)]) for i in range(0, batch_size, bsz_rows)])
print(f"Final Image Shape: {img.shape}")
print(f"Final Image Max:{img.max()} Mean:{img.mean():.3f} Min:{img.min()}")

Image.fromarray((255*(1-img)).astype('uint8')).show()
