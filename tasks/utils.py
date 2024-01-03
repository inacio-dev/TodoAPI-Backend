import jwt
from user.models import Account

def get_user_from_token(access_token):
    try:
        token_data = jwt.decode(access_token, options={"verify_signature": False})
        user_id = token_data.get('user_id')
        user = Account.objects.get(pk=user_id)
        return user
    except jwt.ExpiredSignatureError:
        # Trate o erro de token expirado, se necessário
        return None
    except jwt.InvalidTokenError:
        # Trate outros erros de token inválido, se necessário
        return None
    except Account.DoesNotExist:
        # Trate o caso em que o usuário não existe, se necessário
        return None
