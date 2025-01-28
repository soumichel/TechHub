from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Tentar obter o token do cabeçalho Authorization
        header = self.get_header(request)
        if header is None:
            # Caso o token não esteja no cabeçalho, tentar obter do cookie
            raw_token = request.COOKIES.get('access_token')
            if not raw_token:
                return None  # Se não encontrar o token em nenhum lugar, retorna None
        else:
            raw_token = self.get_raw_token(header)

        # Se o token não for encontrado, retorna None
        if raw_token is None:
            return None

        try:
            # Tenta validar o token
            validated_token = self.get_validated_token(raw_token)
        except AuthenticationFailed:
            raise AuthenticationFailed("Token inválido ou expirado. Verifique o cookie ou token de acesso.")

        # Retorna o usuário correspondente ao token
        return self.get_user(validated_token), validated_token
