from sqlalchemy.orm import Session
from app.models.Setting import Setting

class SettingRepository:
    """! SettingRepository class for data access.
    This class contains methods to interact with the DB model of Setting.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_setting(self, **kwargs):
        """! Get a setting by type or name or value or all settings.
        @param type: Setting type.
        @param name: Setting name.
        @param value: Setting value.
        @return: Setting object or list of Setting objects.
        """
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
        """! Create a setting.
        @param type: Setting type.
        @param name: Setting name.
        @param value: Setting value.
        @param description: Setting description.
        @return: Setting object.
        """
        setting = Setting(
            type=kwargs.get('type'),
            name=kwargs.get('name'),
            value=kwargs.get('value'),
            description=kwargs.get('description')
        )
        self.db_session.add(setting)
        self.db_session.commit()
        return setting