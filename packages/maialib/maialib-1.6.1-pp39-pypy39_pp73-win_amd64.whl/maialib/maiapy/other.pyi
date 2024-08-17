import maialib.maiacore as mc
from enum import Enum

__all__ = ['getSampleScorePath', 'SampleScore', 'setScoreEditorApp', 'getScoreEditorApp', 'openScore', 'getXmlSamplesDirPath']

def setScoreEditorApp(executableFullPath: str) -> None: ...
def getScoreEditorApp() -> str: ...
def openScore(score: mc.Score) -> None: ...

class SampleScore(Enum):
    Bach_Cello_Suite_1 = 'Bach_Cello_Suite_1'
    Beethoven_Symphony_5th = 'Beethoven_Symphony_5th'
    Chopin_Fantasie_Impromptu = 'Chopin_Fantasie_Impromptu'
    Dvorak_Symphony_9_mov_4 = 'Dvorak_Symphony_9_mov_4'
    Mahler_Symphony_8_Finale = 'Mahler_Symphony_8_Finale'
    Mozart_Requiem_Introitus = 'Mozart_Requiem_Introitus'
    Strauss_Also_Sprach_Zarathustra = 'Strauss_Also_Sprach_Zarathustra'

def getSampleScorePath(sampleEnum: SampleScore) -> str: ...
def getXmlSamplesDirPath() -> str: ...
