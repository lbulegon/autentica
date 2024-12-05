import psycopg

try:
    # Conectar ao banco de dados

    conn = psycopg.connect(
        dbname='lbulegon',
        user='lbulegon',
        host='localhost',
        password='ljb#215195'
    )
    
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")
