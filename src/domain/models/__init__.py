"""
Only the database representation models should be add on this all file path.
The support models like, create, update, should not be included here.
"""

__all__ = ["Hero", "Team"]

from .hero import Hero
from .team import Team
