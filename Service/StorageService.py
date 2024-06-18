from Config import DB
class StorageService:
    def GetAllStorages():
        storages = DB.getAllStoragesWithInnerJoin()
        text_to_send = ''
        for stor in storages:
            text_to_send+=f'''
{stor[0]}.{stor[1]}
Адрес: {stor[6]}
Контакты: {stor[7]}
Отвествтвенные: 

1. {stor[8] if stor[8] else 'Не установлен'}
2. {stor[9] if stor[9] else 'Не установлен'}
3. {stor[10] if stor[10] else 'Не установлен'}

Ссылка: {stor[2]}\n'''
        
        return text_to_send


    def GetDismaLinksWithInfo():
        disma_links = DB.GetAllDismaLinksWithInfo()
        return [(el[0], f'{el[1]}\n🏘{el[2]}\n📞{el[3]}') for el in disma_links]

    def GetBazonLinksWithInfo():
        bazon_links = DB.GetAllBazonLinksWithInfo()
        return [(el[0], f'{el[1]}\n🏘{el[2]}\n📞{el[3]}') for el in bazon_links]

    def getStorageNames():
        names = DB.GetAllStoragesNames()
        return [el[0] for el in names]
        

    def ChangeStorName(old_name, new_name):
        return DB.changeStoreName(old_name, new_name)
    
    def ChangeStorURL(old_name, new_url):
        return DB.changeStoreURL(old_name, new_url)
    
    def ChangeStorAddress(old_name, new_address):
        return DB.changeStoreAddress(old_name, new_address)
    
    def ChangeStorContacts(old_name, new_contacts):
        return DB.changeStoreContact(old_name, new_contacts)

    def GetStoreInfo(stor_name):
        stor = DB.GetStoreInfo(stor_name)
        return f'''
{stor[0]}.{stor[1]}
Адрес: {stor[6]}
Контакты: {stor[7]}
Отвествтвенные: 

1. {stor[8] if stor[8] else 'Не установлен'}
2. {stor[9] if stor[9] else 'Не установлен'}
3. {stor[10] if stor[10] else 'Не установлен'}

Ссылка: {stor[2]}\n'''

    def AddStorage(name, dump_url,address, contacts):
        DB.AddStorage(name, dump_url,address, contacts)
        
    def DeleteStorage(storName):
        DB.DeleteStoreByName(storName)
    
    def SetResponsiblForStorageIdById(number,respId, storageName):
        DB.SetResponsiblForStorageIdById(number,respId, storageName)
