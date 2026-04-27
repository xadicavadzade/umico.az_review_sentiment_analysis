import requests
import json
import time 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://birmarket.az/"
}

CATALOG_BASE = "https://mp-catalog.umico.az/api/v1"
REVIEW_BASE = "https://mp-assessment.birmarket.az/api/v1/public/products"

def get_category_ids() -> list:
    '''getting all categories id'''
    data = requests.get(f"{CATALOG_BASE}/categories", headers=HEADERS).json()
    categories = data["categories"]
    return [cat['id'] for cat in categories]
    



def get_product_ids(category_id: int) ->list :
    '''Getting product id with category id'''
    page = 1
    per_page = 24
    all_ids = []


    while True:
        params = {
            "page": page,
            "category_id": category_id,
            "per_page": per_page,
            "sort": "category_popular_score"

        }
    
        data = requests.get(f"{CATALOG_BASE}/products",params=params,headers=HEADERS).json()
        
        products = data.get("products") or data.get("data") or []
        if not products:
            break

        for p in products:
            all_ids.append(p["id"])

        
        total_pages = data.get('meta', {}).get('total_pages') or data.get('meta', {}).get('pages') or 1
        if page >= total_pages:
            break
        page += 1

    return all_ids




def get_reviews(product_id: int) -> list: 
    '''Having all comments of a product'''

    base_url = f"https://mp-assessment.birmarket.az/api/v1/public/products/{product_id}/reviews"
    page = 1
    per_page = 20
    all_reviews = []


    while True:
        params = {
            'page': page,
            'per_page' : per_page,
            'sort_by' : 'created_at',
            'sort_order' : 'DESC'
        }


        response = requests.get(base_url,params=params)
        data = response.json()
        reviews = data['data']
        total_pages = data.get('meta', {}).get('total_pages', 1)
        total_count = data.get('meta', {}).get('total_count', 0)
        

        for review in reviews:
            all_reviews.append({
                "id": review["id"],
                "customer_name": review["customer_name"],
                "score": review["score"],
                "message": review["message"],
                "created_at": review["created_at"]
            })

        if page >= total_pages:
            break
        page += 1
    
    return all_reviews
    

# collect all products ids
category_ids = get_category_ids()
all_products_ids = set() #avoiding dublicates
for cat_id in category_ids:
    ids = get_product_ids(cat_id)
    all_products_ids.update(ids)
    time.sleep(0.3)



#collect reviews
all_reviews = []
all_products_ids = list(all_products_ids)

for pid in all_products_ids:
    reviews = get_reviews(pid)
    if reviews:
        all_reviews.extend(reviews) # all in one list

    time.sleep(0.2)

#write json file

with open("all_reviews.json", "w", encoding="utf-8") as f:
    json.dump(all_reviews, f, ensure_ascii=False, indent=2)