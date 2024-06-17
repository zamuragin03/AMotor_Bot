
from .DetailService import DismaService, BazonService
from random import shuffle
dismaService = DismaService()
bazonService = BazonService()

class SearchService:
    
    def FindDetail(findBy:str):
        total_res ={
            'text':[],
            'photos':[]
        }

        services = [bazonService.FindInBazon, dismaService.FindInDisma]
        shuffle(services)

        for service in services:
            res = service(findBy)
            total_res['photos'] += res.get('photos')
            total_res['text'] += res.get('text')

            if len(total_res['photos']) >= 5 and len(total_res['text']) >= 5:
                break

        total_res['photos'] = total_res['photos'][:5]
        total_res['text'] = total_res['text'][:5]
        return {
            'text':'\n'.join(total_res['text'])+f'https://allparts.tech/search/{findBy.replace(" " , "%20")}\n',
            'photos':total_res['photos']
        }
