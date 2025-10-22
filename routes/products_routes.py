from flask import Blueprint
from controllers.products_controllers import (get_all_products,
create_product, get_product, update_product, 
delete_product)
from middlewares.auth_middlewares import auth_required, admin_required

products_bp = Blueprint('products', __name__)


@products_bp.route('/', methods=['GET'])
@auth_required
@admin_required
def products():
    return get_all_products()

@products_bp.route('/', methods=['POST'])
@auth_required
def create_product_route():
    return create_product()

@products_bp.route('/<string:product_id>', methods=['GET'])
@auth_required
def get_product_route(product_id):
    return get_product(product_id)

@products_bp.route('/<string:product_id>', methods=['PUT'])
@auth_required
def update_product_route(product_id):
    return update_product(product_id)

@products_bp.route('/<string:product_id>', methods=['DELETE'])
@auth_required
def delete_product_route(product_id):
    return delete_product(product_id)