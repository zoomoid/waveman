from pathlib import Path
import soundfile
import os
import uuid
import logging
from pydub import AudioSegment
from .config import ConfigurationDecl, ConfigurationManager
from .artist import WavePainter
from .transformer import WaveTransformer


class Waveman:
    """
    Waveman is the main management class for generating waveform from audio.
    Pass in an audio file, a configuration manager or a path to a config file.
    """

    audio_file: Path
    intermediate_wave_filename: str
    reduced_artifacts: list[tuple[str, ConfigurationDecl, list[float]]]
    artifacts: list[tuple[str, str]]

    def __init__(
        self,
        audio_file: str,
        config_manager=ConfigurationManager | None,
        path: str | None = "config.json",
    ):
        if not config_manager:
            if not path:
                raise ValueError("neither configuration manager nor path given")
            else:
                self.config_manager = ConfigurationManager(path=path)
        else:
            self.config_manager = config_manager

        self.audio_file = Path(audio_file)
        self.intermediate_wave_filename = ".{}.wav".format(str(uuid.uuid4())[0:8])

    def transcode(self):
        """
        Transcodes an mp3 file located at vol/fn to a waveform which we can process using streams
        """
        sound = AudioSegment.from_mp3(self.audio_file.as_posix())
        sound.export("./{}".format(self.intermediate_wave_filename), format="wav")
        logging.info(
            "Finished transcoding {} mp3 to wav (at {})".format(
                self.audio_file, self.intermediate_wave_filename
            )
        )
        return self

    def transform_all(self):
        """
        tranform_all produces sample chunks for all given artifacts
        """
        logging.info(
            "Creating stream from {}".format(fn=self.intermediate_wave_filename)
        )
        self.reduced_artifacts = []
        for name, config in self.config_manager.artifacts.values():
            self.reduced_artifacts += [self.transform(name=name, configuration=config)]
        return self

    def transform(self, name: str, configuration: ConfigurationDecl):
        """
        transform produces sample chunks for one given artifact configuration
        """
        with soundfile.SoundFile(self.intermediate_wave_filename, "rb") as f:
            chunks = WaveTransformer(
                audio_file=f,
                block_length=(f.frames // configuration.get("steps")),
                steps=configuration.get("steps"),
                step_size=16,
                mode=configuration.get("mode"),
                mono=configuration.get("mono"),
                chunk_window=2048,
            ).transform()
            return name, configuration, chunks

    def draw_all(self):
        """
        draw_all calls the painter implementation for each artifact
        """
        self.artifacts = []
        for name, config, chunks in self.reduced_artifacts:
            self.artifacts += [self.draw(name, config, chunks)]
        return self

    def draw(self, name: str, configuration: ConfigurationDecl, chunks: list[float]):
        """
        draw takes a particular artifact (decomposed) and its corresponding audio chunks,
        creates a drawing context and outputs a PDF for a particular name
        """
        svg = WavePainter(chunks, configuration).to_string()
        return name, svg

    def cleanup(self):
        """
        cleanup removes a file located at fn
        """
        os.unlink(self.intermediate_wave_filename)
        return True
