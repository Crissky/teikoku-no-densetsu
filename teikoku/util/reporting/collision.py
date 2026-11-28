from teikoku.entity.world.world_entity import WorldEntity
from teikoku.util.reporting.base import ReportingBase


class ReportingCollision(ReportingBase):
    x: int
    y: int
    entity: WorldEntity
