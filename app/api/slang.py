from app.api import bp

from app.ml_models.rnn.loaded_rnn_model import return_loaded_model

@bp.route('/generate_slang', methods=['GET'])
def generate_slang():
    """Generate and return a new slang word."""
    model = return_loaded_model()
    print(model)
    return "Hello!"