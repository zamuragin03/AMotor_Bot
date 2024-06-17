from Config import DB
class ResponsibleService:
    def GetAllResponsibles():
        storages = DB.getAllResponsibles()
        text_to_send = ''
        for stor in storages:
            text_to_send+=f'{stor[0]}. {stor[1]} @{stor[2]}\n'
        return text_to_send if text_to_send else 'Ответственных нет'

    def getResponsibleNames():
        names = DB.getAllResponsibles()
        return [f'{el[0]} – {el[1]}' for el in names]
        
    def getResponsiblesIDs():
        resp = DB.getAllResponsibles()
        return [int(el[0]) for el in resp]
        
    def GetResponsibleById(id:int):
        resp =  DB.getAllResponsibleById(id)
        return f'{resp[0]}. {resp[1]} @{resp[2]}'
    
    def DeleteResponsibleById(id):
        DB.deleteResponsibleById(id)
    
    def AddResponsible(name, tg_username):
        DB.AddResponsible(name, tg_username)