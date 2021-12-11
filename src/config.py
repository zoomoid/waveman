import json
from typing import Any, Dict, TypedDict


class ConfigurationDecl(TypedDict, total=False):
    step_width: float
    height: float
    rounded: float
    steps: int
    gap: float
    width: float

    mode: str
    align: str
    sr: float
    mono: bool

    scale: float
    dpi: float
    preserve_aspect_ratio: str
    color: str


class Artifact(TypedDict):
    name: str
    configuration: ConfigurationDecl


class AbstractConfiguration:
    """
    AbstractConfiguration contains the general config settings that both, full and small share
    """

    __raw_config: dict
    __raw_shared_config: dict

    name: str

    step_width: float
    height: float
    rounded: float
    steps: int
    gap: float
    width: float

    mode: str
    align: str
    sr: float
    mono: bool

    scale: float
    dpi: float
    preserve_aspect_ratio: str
    color: str

    def __init__(self, name: str, obj: ConfigurationDecl, shared: ConfigurationDecl):
        self.name = name
        self.__raw_config = obj
        self.__raw_shared_config = shared

    def or_shared(self, key: str, default: Any) -> Any:
        return self.__raw_config.get(key, self.__raw_shared_config.get(key, default))


class ConcreteConfiguration(AbstractConfiguration):
    """
    LargeConfiguration is a config type for full waveforms
    """

    def __init__(self, name: str, obj: ConfigurationDecl, shared: ConfigurationDecl):
        AbstractConfiguration.__init__(self, name, obj, shared)
        self.step_width = self.or_shared("step_width", 20)
        self.height = self.or_shared("height", 200)
        self.rounded = self.or_shared("rounded", 10)
        self.steps = self.or_shared("steps", 64)
        self.gap = self.or_shared("gap", 10)
        self.width = self.step_width * self.steps
        self.color = self.or_shared("color", "#f58b44")
        self.dpi = self.or_shared("dpi", 600)
        self.scale = self.or_shared("scale", 1)
        self.preserve_aspect_ratio = self.or_shared("preserveAspectRatio", "none")
        self.mode = self.or_shared("mode", "rounded_avg")
        self.align = self.or_shared("align", "center")
        self.sr = self.or_shared("sr", 48000)
        self.mono = self.or_shared("mono", True)


class ConfigurationManager:
    """
    Config contains both the large and the small config parsed from a given path to a json file
    """

    artifacts: Dict[str, Artifact] = {}

    def __init__(self, runtime_config: Artifact, path: str | None):
        if path:
            with open(path, "r") as f:
                d = dict(json.load(f))
            try:
                shared: ConfigurationDecl = d.get("shared")
                artifacts: list[Artifact] = d.get("artifacts", [])
                for a in artifacts:
                    self.artifacts[a.get("name")] = ConcreteConfiguration(
                        a.get("configuration"), shared
                    )
            except AttributeError:
                raise AttributeError
        # make this the last step to not accidentally override "cli" artifact from config file
        if runtime_config:
            artifacts[runtime_config.get("name")] = runtime_config.get("configuration")
