'''
Repository Class
'''
from dataclasses import dataclass
from typing import List


@dataclass
class Repository:
    """GitHub repository"""

    login: str
    repo: str
    stars_in_period: int
    brief: str
    href: str
    stars: int
    forks: int

    def to_csv(self) -> List:
        """Return CSV style list for all attributes"""
        return [
            self.login,
            self.repo,
            self.stars_in_period,
            self.stars,
            self.brief,
            self.href,
            self.forks,
        ]
