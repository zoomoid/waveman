from soundfile import SoundFile


class WaveTransformer:
    """
    Transformer instances transform a list of channels with associated samples using a given
    mode, that is, either 'average', 'rounded average', or 'max' into smaller samples
    """

    def __init__(
        self,
        audio_file: SoundFile,
        block_length,
        steps,
        chunk_window=4096,
        step_size=16,
        mode="rounded_avg",
        mono=True,
    ):
        if not block_length or block_length < 1:
            raise AttributeError
        if not steps or steps < 1:
            raise AttributeError
        self.steps = steps
        self.block_length = block_length
        self.mode = mode
        self.audio_file = audio_file
        self.chunk_window = chunk_window
        self.step_size = step_size
        if mono:
            self.channels = 1
        else:
            self.channels = 2
        self.chunks = [[] for i in range(self.channels)]

    def transform(self):
        i = 0
        while i < self.steps and self.audio_file.tell() < self.audio_file.frames:
            block = self.audio_file.read(self.chunk_window * self.step_size)[
                :: self.step_size
            ]
            if self.channels == 1:
                block = self.preflight_mono(block)
            elif self.channels == 2:
                block = self.preflight_stereo(block)
            else:
                raise AttributeError
            chunk = 0
            if self.mode == "max":
                chunk = list(map(lambda a: max(a), block))
            elif self.mode == "avg":
                chunk = list(map(lambda a: sum(a) / self.chunk_window, block))
            elif self.mode == "rounded_avg":
                chunk = list(map(lambda a: round(sum(a) / self.chunk_window, 3), block))
            else:
                raise RuntimeError
            self.chunks = [
                self.chunks[i] + [chunk[i]] for i in range(self.channels)
            ]  # Concatenates channel lists component-wise
            self.audio_file.seek(i * self.block_length)
            i += 1
        return normalize(self.chunks)

    def preflight_mono(self, block):
        """
        Converts a given stereo signal to a mono channel signal
        by averaging both channels
        Returns: List(List(Number)) (to preserve generality)
        The outer list contains the channels (here: 1) and the inner list contains all
        samples
        """
        return [[abs((s1 + s2) / 2) for (s1, s2) in block]]

    def preflight_stereo(self, channels):
        """
        Transforms (frames x channels) matrix into (channels x frames) i.e.
        [[1,0],[0,1],...,[0,1]] -> [[1,0,...,0],[0,1,...,1]]
        which makes processing the two channels separately much easier
        """
        left = [s[0] for s in channels]
        right = [s[1] for s in channels]
        return [left, right]


def normalize(l):
    """
    Normalizes a given list of numbers, i.e., in this context, a channel of samples
    """
    m = max([abs(x) for x in l])
    return [x / m for x in l]
