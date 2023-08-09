import firebase_admin
from firebase_admin import credentials, db

class Firebase():
    def __init__(self) -> None:
        self.initialize_firebase()

    def initialize_firebase(self):
        cred = credentials.Certificate(r"./programming-1b4e1-firebase-adminsdk-bh2x1-09ef909109.json")
        firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://programming-1b4e1-default-rtdb.asia-southeast1.firebasedatabase.app'
                })

    def get_all_products(self):
        return db.reference('products').get()
    
    def get_product(self,product_id):
        # print(f"Firebase:  {product_id=}")
        return db.reference('products').child(product_id).get()
    
    def get_product_names(self):
        products = self.get_all_products()
        product_names = {}
        for i in products.keys():
            product_names[i]=products[i]['title']
        return product_names

    def __str__(self) -> str:
        return str(self.get_products())

# fb = Firebase()
# print(fb.get_product_names())

featured_products = ['product1','product2','product3']
