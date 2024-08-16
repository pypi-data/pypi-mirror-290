from enum import Enum


class Coins(Enum):



    @property
    def Open(self) -> str:
        return f"{self.value}_Open"

    @property
    def High(self) -> str:
        return f"{self.value}_High"

    @property
    def Low(self) -> str:
        return f"{self.value}_Low"

    @property
    def Close(self) -> str:
        return f"{self.value}_Close"

    @property
    def Volume(self) -> str:
        return f"{self.value}_Volume"

    @property
    def OHLCV(self):
        return [f"{self.Open}", f"{self.High}", f"{self.Low}", f"{self.Close}", f"{self.Volume}"]





