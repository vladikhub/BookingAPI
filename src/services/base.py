from src.utils.db_manager import BDManager


class BaseService:
    def __init__(self, db: BDManager | None = None) -> None:
        self.db = db


