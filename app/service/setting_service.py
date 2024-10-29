from app.data_access.setting_repository import SettingRepository

class SettingService:
    """! SettingService class for business logic.
    This class contains methods to interact with the SettingRepository class.
    """
    def __init__(self, setting_repository: SettingRepository):
        self.setting_repository = setting_repository

    def get_setting(self, **kwargs):
        """! Get a setting by type or name or value or all settings. paser the setting value to a list of dictionary."""
        rlt = self.setting_repository.get_setting(**kwargs)
        if kwargs.get('type') == 'Premadebox':
            premadeboxes = []
            for x in rlt:
                name = x.name.split('_')
                value = x.value.split('_')
                premadebox = {}
                for i in range(len(name)):
                    premadebox[name[i]] = value[i]
                premadeboxes.append(premadebox)
            return premadeboxes
        elif kwargs.get('type') == 'Product_form':
            if kwargs.get('name').startswith('Premadebox_'):
                boxitem = []
                for x in rlt:
                    temp = x.value.split('_')
                    item = {}
                    item['type'] = temp[2]
                    item['name'] = temp[0]
                    item['quantity'] = temp[1]
                    item['price'] = temp[3]
                    boxitem.append(item)
                return boxitem
            else:
                nest_premadeboxes = []
                for x in rlt:
                    premadeboxes = x.value.split('_')
                    nest_premadeboxes.append(premadeboxes)
                return nest_premadeboxes
        else:
            rlt_sort = sorted(rlt, key=lambda x: x.name)
            return rlt_sort
    
    def create_setting(self, **kwargs):
        """! Create a setting."""
        return self.setting_repository.create_setting(**kwargs)