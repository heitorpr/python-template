"""
Define the models related to the domain of the project.

It specifies operations related to the object that defines an abstraction of the
real world, like user.

It concerns only in operating with the data, not how it is stored or presented.
"""

__all__ = ["HeroRepository", "TeamRepository"]

from .hero import HeroRepository
from .team import TeamRepository
