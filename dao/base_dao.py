from sqlalchemy.orm import Session
from sqlalchemy import select

class BaseDAO:

    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def create(self, *, instance=None, **kwargs):
        if instance is not None:
            obj = instance
        else:
            obj = self.model(**kwargs)

        self.session.add(obj)
        self.session.commit()

        return obj

    def get_all(self, skip: int, limit: int):  # пагинация
        query = select(self.model).offset(skip).limit(limit)
        result = self.session.execute(query)

        return result.scalars().all()

    def get_by_id(self, id: int):
        '''Возвращает экземпляр класса'''
        return self.session.get(self.model, id)

    def update(self, id: int, **data):
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.session.commit()
            return instance
        return None

    def delete(self, id: int):
        instance = self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
    
    # def save(self, model):
