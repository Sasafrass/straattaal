from app.api import bp

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Get a single user given its ID."""
    pass


@bp.route('/users', methods=['GET'])
def get_users():
    """Get all users from the database."""
    pass


@bp.route('/users', methods=['POST'])
def create_user():
    """Create a single new user."""
    pass