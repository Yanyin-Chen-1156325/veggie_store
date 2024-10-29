from sqlalchemy.orm import Session
from app.models.Setting import Setting

class SettingRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_setting(self, **kwargs):
        type = kwargs.get('type')
        name = kwargs.get('name')
        value = kwargs.get('value')

        query = self.db_session.query(Setting).filter_by(type=type)
        
        if name is not None:
            query = query.filter_by(name=name)
        
        if value is not None:
            query = query.filter_by(value=value)
        
        return query.all()
    
    def create_setting(self, **kwargs):
        setting = Setting(
            type=kwargs.get('type'),
            name=kwargs.get('name'),
            value=kwargs.get('value'),
            description=kwargs.get('description')
        )
        self.db_session.add(setting)
        self.db_session.commit()
        return setting