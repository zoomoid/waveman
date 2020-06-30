from waveman import waveman, transcode, to_string, cleanup

def main():
  fn = transcode("https://files.zoomoid.de/artemis/Hale-Bopp.mp3")
  # print(output)
  canvas = waveman(fn)
  f = open("demo.svg", "w+")
  f.write(to_string(canvas))
  cleanup(fn)
  

if __name__ == "__main__":
  main()