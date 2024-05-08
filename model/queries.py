from model.models import User, SpotiClient

def get_spoti_client(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        spoti_client = SpotiClient.query.filter_by(user_id=user.id).first()
        if spoti_client:
            return spoti_client
    return None