from app import db
from model.models import User, SpotiClient

def add_user(username, password):
    user = User(
            username=username,
            password=password
            )
    db.session.add(user)
    db.session.commit()

def update_spoti_client(spoti_client, client_id, client_secret, client_name, user_id=-1):
    if spoti_client:
        spoti_client.client_id = client_id
        spoti_client.client_secret = client_secret
        spoti_client.client_name = client_name
    else:
        client = SpotiClient(
            client_id=client_id,
            client_secret=client_secret,
            client_name =client_name,
            user_id = user_id
            )
        db.session.add(client)
    db.session.commit()