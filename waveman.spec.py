from waveman import waveman, transcode, to_string, cleanup

def main():
  fn = transcode("https://files.zoomoid.de/artemis/Hale-Bopp.mp3")
  # print(output)
  canvas = waveman(fn)
  print(to_string(canvas))
  cleanup(fn)
  

if __name__ == "__main__":
  main()