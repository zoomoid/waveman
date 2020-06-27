"""
Absolute maximum mode:

For a given range, compute the absolute maximum sample
@param y - sample array
@param j - step index: means we compute for the j'th step
@param delta - range length
@return maximum absolute sample value
"""
def max_in_area(y):
  return max([abs(y[i]) for i in range(y)])

"""
Average mode:

For a given range, compute the average sample
@param y - sample array
@param j - step index: means we compute for the j'th step
@param delta - range length
@return average sample value
"""
def avg_in_area(y):
  return sum([abs(y[i]) for i in range(y)]) / len(y) 

"""
Normalizes a given list of numbers

@param y - list of numbers
"""
def normalize(y):
  max_val = max([abs(x) for x in y])
  return list(map(lambda v: v / max_val, y))