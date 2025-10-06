from flask import Blueprint, request, jsonify
from src.models.user import User
from src.utils.helpers import create_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        if not all([email, password, name]):
            return jsonify({'error': 'Missing required fields'}), 400
        user = User.create(email, password, name)
        token = create_token(user['id'])
        return jsonify({'user': user, 'token': token}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not all([email, password]):
            return jsonify({'error': 'Missing email or password'}), 400
        user = User.verify_credentials(email, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        token = create_token(user['id'])
        return jsonify({'user': user, 'token': token}), 200
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    from src.utils.helpers import require_auth
    @require_auth
    def _get_user():
        user = User.find_by_id(request.user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': user}), 200
    return _get_user()
