from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

# 플라스크 앱 초기화 (初始化 Flask 应用)
app = Flask(__name__)
CORS(app)  # 프론트엔드와의 크로스 도메인 요청 허용 (允许前端跨域请求)

# 파이어베이스 초기화 (初始化 Firebase)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 샘플 데이터 초기화 (初始化示例数据，首次运行后注释)
def init_data():
    # 브랜드 데이터 (品牌数据)
    brands = [
        {"id": 1, "name": "BrandA", "history": "Founded in 2000", "features": "Organic", "logo": "https://example.com/brandA.jpg"},
        {"id": 2, "name": "BrandB", "history": "Founded in 2010", "features": "Vegan", "logo": "https://example.com/brandB.jpg"}
    ]
    for brand in brands:
        db.collection("brands").document(str(brand["id"])).set(brand)

    # 제품 데이터 (产品数据)
    products = [
        {"id": 1, "name": "Cleanser", "brand": "BrandA", "price": 20, "skin_type": "Oily", "official_url": "https://brandA.com/product/cleanser"},
        {"id": 2, "name": "Toner", "brand": "BrandB", "price": 15, "skin_type": "Dry", "official_url": "https://brandB.com/product/toner"}
    ]
    for product in products:
        db.collection("products").document(str(product["id"])).set(product)

# API: 모든 브랜드 가져오기 (获取所有品牌)
@app.route('/api/brands', methods=['GET'])
def get_brands():
    brands = []
    docs = db.collection("brands").stream()
    for doc in docs:
        brands.append(doc.to_dict())
    return jsonify(brands)

# API: 특정 브랜드 가져오기 (获取单个品牌)
@app.route('/api/brands/<int:brand_id>', methods=['GET'])
def get_brand(brand_id):
    doc = db.collection("brands").document(str(brand_id)).get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"error": "Brand not found"}), 404

# API: 제품 가져오기 (支持肤质过滤) (获取产品，支持肤质过滤)
@app.route('/api/products', methods=['GET'])
def get_products():
    skin_type = request.args.get('skin_type')
    products = []
    if skin_type:
        docs = db.collection("products").where("skin_type", "==", skin_type).stream()
    else:
        docs = db.collection("products").stream()
    for doc in docs:
        products.append(doc.to_dict())
    return jsonify(products)

# API: 특정 제품 가져오기 (获取单个产品)
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    doc = db.collection("products").document(str(product_id)).get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    init_data()  # 데이터 초기화 (首次运行后注释) (初始化数据，首次运行后注释)
    app.run(debug=True)