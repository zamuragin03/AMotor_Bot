import sqlite3
class DataBase:
    def __init__(self,path_to_db):
        self.db_name = path_to_db

    def getAllStorages(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"select * from storage")
            records = cursor.fetchall()
        return records

    def getAllStoragesWithInnerJoin(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'''SELECT s.*, r1.name as responsible_1_name, r2.name as responsible_2_name, r3.name as responsible_3_name
FROM storage s
LEFT JOIN responsible r1 ON s.responsible_1_id = r1.id
LEFT JOIN responsible r2 ON s.responsible_2_id = r2.id
LEFT JOIN responsible r3 ON s.responsible_3_id = r3.id;''')
            records = cursor.fetchall()
        return records
    
    def GetStoreInfo(self,stor_id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'''
                           SELECT s.*, 
                           r1.name as responsible_1_name,
                           r2.name as responsible_2_name,
                           r3.name as responsible_3_name FROM storage s
LEFT JOIN responsible r1 ON s.responsible_1_id = r1.id
LEFT JOIN responsible r2 ON s.responsible_2_id = r2.id
LEFT JOIN responsible r3 ON s.responsible_3_id = r3.id
where s.id="{stor_id}"
                           
                           ''')
            record = cursor.fetchone()
        return record
    
    def getAllResponsibles(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"select * from responsible")
            records = cursor.fetchall()
        return records
    
    def getAllResponsibleById(self, id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"select * from responsible where responsible.id={id}")
            record = cursor.fetchone()
        return record
    
    def deleteResponsibleById(self, id):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"delete from responsible where id={id}")
    
    def getAllResponsibles(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"select * from responsible")
            records = cursor.fetchall()
        return records
    
    def AddResponsible(self, name, tg_username):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'insert into responsible(id, name, tg_username) values (null, "{name}", "{tg_username}") ')
            connection.commit()
            
    def AddStorage(self, name, dump_url,address, contacts):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'insert into storage(id, name, dump_url, address,contacts) values (null, "{name}", "{dump_url}", "{address}","{contacts}" ) ')
            connection.commit()
    
    def DeleteStoreByName(self, storename):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'delete from storage where name="{storename}"')
    
    def SetResponsiblForStorageIdById(self, number,respId, storageId):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE storage set responsible_{number}_id = {respId} where storage.id={storageId} ')
    
    def GetAllDismaLinksWithInfo(self,):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT dump_url, name, address, contacts from storage where storage.dump_url like '%disma%' and storage.dump_url NOT like '%xml' ")
            records = cursor.fetchall()
        return records
    
    def GetAllStoragesNames(self,):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT id,name from storage ")
            records = cursor.fetchall()
        return records
    
    def GetAllBazonLinksWithInfo(self,):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT dump_url, name, address, contacts from storage where storage.dump_url like '%baz%'  and storage.dump_url NOT like '%xml'")
            records = cursor.fetchall()
        return records
    
    
    
    def changeStoreName(self, old_name, new_name):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE storage set name = "{new_name}" where storage.name="{old_name}" ')
        
    def changeStoreURL(self, old_name, new_link):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE storage set dump_url = "{new_link}" where storage.name="{old_name}" ')
        
    def changeStoreAddress(self, old_name, new_address):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE storage set address = "{new_address}" where storage.name="{old_name}" ')
        
    def changeStoreContact(self, old_name, contacts):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f'UPDATE storage set contacts = "{contacts}" where storage.name="{old_name}" ')
        