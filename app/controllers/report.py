from sqlalchemy.exc import SQLAlchemyError
from ..repositories.managers import ReportManager


class ReportController:
    manager = ReportManager

    @classmethod
    def get_report(cls):
        try:
            return cls.manager.get_all_report(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)