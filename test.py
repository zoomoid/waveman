from src.waveman import WaveMan

def main():
    with open("demo-waveform.svg", "w") as f:
        svg = WaveMan("soy/Malhereux En Amour.mp3").to_string()
        f.write(svg)
        f.close()

if __name__ == "__main__":
    main()
