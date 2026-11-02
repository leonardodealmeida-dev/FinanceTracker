
from app.services.supabase_service import test_connection

try:
    result = test_connection()
    print("Conexão funcionando!")
    print("Transações encontradas:", len(result.data))
except Exception as error:
    print("Erro na conexão:")
    print(error)
