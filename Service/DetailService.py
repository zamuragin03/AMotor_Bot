from .StorageService import StorageService
import requests
import pandas as pd
import io

class BazonService:
    def __init__(self) -> None:
        self.dataframes = []
        self.UpdatedDB()
        
    def UpdatedDB(self,):
        all_links = StorageService.GetBazonLinksWithInfo()
        for obj in all_links:
            response = requests.get(obj[0])
            data = io.BytesIO(response.content)
            self.dataframes.append({
                'info':obj[1],
                'df':pd.read_csv(data, encoding='cp1251', delimiter=';')
                })
    
    def FindInBazon(self,findBy):
        return_obj ={
            'text':[],
            'photos':[]
        }
        total_obj = 1
        for stor in self.dataframes:
            contains_string = stor.get('df').map(lambda cell: str(findBy).lower() in str(cell).lower())
            rows_with_string_disma = stor.get('df')[contains_string.any(axis=1)]
            for index, row in rows_with_string_disma.iterrows():
                if total_obj>5:
                    break
                return_obj['photos'].append(str(row['Фото']).split(',')[0])
                return_obj['text'].append(f"{total_obj}.{row['Наименование']}\n{row['Марка']} {row['Модель']}\nОЕМ: {row['Номер']}\n\n{row['Цена']}₽\nКонтакты:\n{stor.get('info')}\n\n")
                total_obj+=1
        return return_obj
            
            
class DismaService:
    def __init__(self) -> None:
        self.dataframes = []
        self.UpdatedDB()
        
    def UpdatedDB(self,):
        all_links = StorageService.GetDismaLinksWithInfo()
        for obj in all_links:
            response = requests.get(obj[0])
            data = io.BytesIO(response.content)
            self.dataframes.append({
                'info':obj[1],
                'df':pd.read_excel(data)
                })
    
    
    def FindInDisma(self,findBy):
        return_obj ={
            'text':[],
            'photos':[]
        }
        total_obj = 1
        for stor in self.dataframes:
            contains_string = stor.get('df').map(lambda cell: str(findBy).lower() in str(cell).lower())
            rows_with_string_disma = stor.get('df')[contains_string.any(axis=1)]
            for index, row in rows_with_string_disma.iterrows():
                if total_obj>5:
                    break
                return_obj['photos'].append(str(row['Фотографии']).split(',')[0])
                return_obj['text'].append(f"{total_obj}. {row['Название']}\nПрименимость:{row['Применимость'][:25]}...\nОЕМ:{row['Номер OEM']}\n{row['Цена']}₽\nКонтакты:\n{stor.get('info')}\n\n")
                total_obj+=1
        return return_obj
        
        
        