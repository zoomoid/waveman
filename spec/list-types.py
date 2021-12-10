def avg(l):
  return list(map(lambda x: sum(x) / len(x), l))

a = [[1,1,1,0,0,0]] # Mono array
b = [[1,0,1],[0,1,0]]
channels = len(b)
chunks = [[] for i in range(channels)]
chunk = avg(b)
chunks = [chunks[i] + [chunk[i]] for i in range(len(chunks))]
chunk = avg(c)
chunks = [chunks[i] + [chunk[i]] for i in range(len(chunks))]
