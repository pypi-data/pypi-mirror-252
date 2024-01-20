

from typing import TypedDict
import typing

class TrackedIndexEntry(TypedDict, total=False):
    hashing : str
    lastPulled : float
    lastCommitChecked : float
    
class ScriptModel(TypedDict):
    hashing : str

class FileModel(TypedDict):
    file : str

class BucketIndexModel(TypedDict, total=False):
    branch : str
    name : str
    bucketDir : str
    gitUrl : str
    buckets : typing.Dict[str, dict]
    files : typing.Dict[str,FileModel]
    scripts : typing.Dict[str,ScriptModel]
