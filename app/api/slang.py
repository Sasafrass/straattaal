from app.api import bp

@bp.route('/generate_slang', methods=['GET'])
def get_user(id):
    """Generate and return a new slang word."""
    pass