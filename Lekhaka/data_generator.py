import numpy as np
import threading
import queue

from .vertical_aligner import VerticalAlign
AVG_CHARS_PER_LABEL = 2.5

class DataGenerator:
    def __init__(self, scriber, deformer, noiser, batch_size=1, labelswidth=None):
        self.scriber = scriber
        self.deformer = deformer
        self.noiser = noiser
        self.batch_size = batch_size
        self.vertical_align = VerticalAlign(scriber.height)

        self.labelswidth = labelswidth if labelswidth is not None else \
            int(AVG_CHARS_PER_LABEL * scriber.nchars_per_sample)

    def get(self):
        scribe = self.scriber

        images = np.empty(dtype=np.float32, shape=(self.batch_size, scribe.width, scribe.height))  # Width should come first
        labels = np.empty(dtype=int, shape=(self.batch_size, self.labelswidth))
        label_lengths = np.empty(dtype=int, shape=(self.batch_size,))

        # Get the images and labels
        for i in range(self.batch_size):
            img, _, lbls = scribe()
            img = self.vertical_align(img)
            images[i, :, :] = img.T / 255.  # Transposing
            labels[i, :len(lbls)] = lbls
            label_lengths[i] = len(lbls)

        # Distort the Images
        images[:, -1, :] = 0                    # Set last column of slab to zero for interpolation
        images = self.deformer(images)

        # Calculate Image lengths
        image_lengths = [np.nonzero(np.sum(img, axis=-1))[0][-1] for img in images]
        image_lengths += 2*np.random.randint(1, scribe.hbuffer, size=(self.batch_size,))  # Add some buffer
        image_lengths = np.minimum(image_lengths, scribe.width-1)                         # Clamp it to width

        # Add noise now
        self.noiser(images)

        images = np.expand_dims(images, axis=-1)
        return images, labels, image_lengths, label_lengths


class ParallelDataGenerator(DataGenerator):
    def __init__(self, *args, **kwargs):
        super(ParallelDataGenerator, self).__init__(*args, **kwargs)
        self.queue = queue.Queue(maxsize=3)
        self._start_thread()

    def _start_thread(self):
        def _base_call_wrapper():
            self.queue.put(super(ParallelDataGenerator, self).get())

        self.thread = threading.Thread(target=_base_call_wrapper, daemon=True)
        self.thread.start()

    def get(self):
        self.thread.join()
        self._start_thread()
        return self.queue.get()
