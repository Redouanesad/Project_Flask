from flask import jsonify, request
from bson.objectid import ObjectId
from models import Product
from datetime import datetime

def create_product():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "you didn't send any data in body"}), 400
        
        product = Product(
            title=data.get('title'),
            user=data.get('user',"Unknown"),
            description=data.get('description'),
        )
        product.save()
        return jsonify({"message": "Product created", "product": data}), 201
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500


def get_all_products():
    try:    
        user = getattr(request, 'current_user', None)
        if not user:
            return jsonify({"message": "User not authenticated"}), 401
        
        print("user: 🛑🛑🛑🛑🛑🛑🛑🛑 user data 🛑🛑🛑🛑🛑🛑🛑🛑 ", user)
        
        products = Product.objects()
        print("list: ", products)
        
        # Convert MongoEngine objects to dictionaries
        product_list = []
        for product in products:
            product_dict = {
                "id": str(product.id),
                "_id": str(product.id),  # For compatibility
                "title": product.title,
                "description": product.description,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
                "completed_at": product.completed_at.isoformat() if product.completed_at else None
            }
            product_list.append(product_dict)
        
        return jsonify({"message": "Products", "products": product_list})
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def get_product(product_id):
    try:
        product = Product.objects(id=product_id).first()
        if not product:
            return jsonify({"message": "Product not found"}), 404
            
        product_dict = {
            "id": str(product.id),
            "_id": str(product.id),
            "title": product.title,
            "description": product.description, 
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            "completed_at": product.completed_at.isoformat() if product.completed_at else None
        }
        
        return jsonify({"message": "product", "product": product_dict}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def update_product(product_id):
    try:
        data = request.get_json()
        product = product.objects(id=product_id).first()
        
        if not product:
            return jsonify({"message": "product not found"}), 404
        
        # Update fields if provided
        if 'title' in data:
            product.title = data['title']
        if 'description' in data:
            product.description = data['description']
        if 'status' in data:
            product.status = data['status']
        if 'priority' in data:
            product.priority = data['priority']
        if 'user' in data:
            product.user = data['user']
            
        # Update timestamp
        product.updated_at = datetime.utcnow()
        product.save()
        
        # Return updated product
        product_dict = {
            "id": str(product.id),
            "_id": str(product.id),
            "title": product.title,
            "description": product.description,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            "completed_at": product.completed_at.isoformat() if product.completed_at else None
        }
        
        return jsonify({"message": "product updated", "product": product_dict}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
    
def delete_product(product_id):
    try:
        product = product.objects(id=product_id).first()
        
        if not product:
            return jsonify({"message": "product not found"}), 404
            
        product.delete()
        return jsonify({"message": "product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

    
    