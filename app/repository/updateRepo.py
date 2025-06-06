
from sqlalchemy.orm import Session
from app.domain.model.update import Update
from typing import Any, Tuple

def _wrap_return(result: Any) -> Tuple[Any, None]:
    return result, None
def _wrap_error(e: Exception) -> Tuple[None, Exception]:
    return None, e

class UpdateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_update_count(self, user_id: str):
        try:
            update = self.db.query(Update).filter(Update.user_id == user_id).first()
            count = update.update_count if update else 0
            return _wrap_return(count)
        except Exception as e:
            self.db.rollback()
            return _wrap_error(e)

    def create_or_increment_update(self, user_id: str):
        try:
            update = self.db.query(Update).filter(Update.user_id == user_id).first()
            if update:
                update.update_count += 1
            else:
                update = Update(user_id=user_id, update_count=1)
                self.db.add(update)
            self.db.commit()
            self.db.refresh(update)
            return _wrap_return(update)
        except Exception as e:
            self.db.rollback()
            return _wrap_error(e)

    def reset_update_count(self, user_id: str):
        try:
            update = self.db.query(Update).filter(Update.user_id == user_id).first()
            if update:
                update.update_count = 0
                self.db.commit()
                self.db.refresh(update)
            return _wrap_return(update)
        except Exception as e:
            self.db.rollback()
            return _wrap_error(e)
