from waveman import waveman, transcode, to_string, cleanup
import timeit


def main():
  fn = transcode('Mars.mp3')
  # print(output)
  canvas = waveman(fn)
  f = open("mars.svg", "w+")
  f.write(to_string(canvas))
  cleanup(fn)
  

if __name__ == "__main__":
  timeit.timeit('main()', number=1)