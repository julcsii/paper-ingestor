from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Paper():
    """Paper class."""
    uniqueId: str
    title: str
    abstract: str
    authorNames: List[str]
    publicationYear: Optional[int]
    doi: Optional[str]
    citedByCount: int  = field(init=False) # equal length(inCitations)
    urls: List[str]
    outCitations: List[str] # ref to uniqueId of cited papers
    inCitations: List[str] # ref to uniqueId of citing papers
    
    def __post_init__(self):
        self.citedByCount = len(self.inCitations)
