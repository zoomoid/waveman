import soundfile


f = open("test.wav", "rb")
with soundfile.SoundFile("test.wav", "rb") as f:
  block_length = int(f.frames // 64)
  chunks = Transformer(f, block_length, 64, chunk_window=2048, interpolation=16, mode="avg", mono=True).transform()