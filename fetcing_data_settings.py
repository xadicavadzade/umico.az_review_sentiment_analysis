import json
import requests
import time


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://birmarket.az/"
}

CATALOG_BASE = "https://mp-catalog.umico.az/api/v1" #catalog base of umico.az
REVIEW_BASE = "https://mp-assessment.birmarket.az/api/v1/public/products"#review base of umico.az

class LoadData:
    '''this class is about fetching and loading data'''
    def __init__(self):
        self.first_base = CATALOG_BASE
        self.second_base = REVIEW_BASE
        self.per_page = 24
        self.session = requests.Session()     
        self.session.headers.update(HEADERS)


    def get_category_ids(self) -> list:
        '''collect all categories ids'''
        data = self.session.get(f"{self.first_base}/categories").json()
        categories = data['categories']
        return [cat['id'] for cat in categories]
    

    def get_product_ids(self,category_id:int ) -> list:
        '''collect all products ids through one category id'''
        all_ids = []
        page = 1



        while True:
            params = {
            'page' : page,
            'category_id' : category_id,
            'per_page' : self.per_page,
            'sort' : 'category_popular_score'
            }


            data = self.session.get(f'{self.first_base}/products',params=params).json()
            

            products = data.get('products') or data.get('data') or []
            if not products:
                break

            for p in products:
                all_ids.append(p['id'])

            total_pages = data.get('meta',{}).get('total_pages') or data.get('meta', {}).get('pages') or 1
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)

        return all_ids
    

    def get_product_reviews(self,product_id: int) ->list:
        '''collect all reviews through product id'''
        all_reviews = []
        page = 1

        while True:
            params = {
            'page': page,
            'per_page' : self.per_page,
            'sort_by' : 'created_at',
            'sort_order' : 'DESC'
            }


            data = self.session.get(f'{self.second_base}/{product_id}/reviews',params=params).json()
            

            reviews = data.get('data',[])
            if not reviews:
                break

            for review in reviews:
                all_reviews.append({
                    "id": review["id"],
                    "customer_name": review["customer_name"],
                    "score": review["score"],
                    "message": review["message"],
                    "created_at": review["created_at"]                       

                })


            total_pages = data.get('meta',{}).get('total_pages',1)
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)

        return all_reviews




            

