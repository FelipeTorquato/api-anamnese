# ==============================================================================
# TEMPLATE DE CONFIGURAÇÃO DE AMBIENTE (.env)
# ==============================================================================
# Instruções:
# 1. Copie este arquivo e renomeie para '.env'
# 2. Preencha os valores abaixo conforme o seu ambiente.
# 3. NUNCA envie o arquivo '.env' real para o repositório (o .gitignore já cuida disso).
# ==============================================================================

# --- BANCO DE DADOS (DATABASE) ---
# Se estiver usando Docker, o host deve ser o nome do serviço no docker-compose (ex: db)
# Exemplo Postgres: postgresql://usuario:senha@host:5432/nome_do_banco
# Exemplo SQLite: sqlite:///./clinica.db
# DATABASE_URL=postgresql://admin:admin_password@db:5432/clinica_db

# Password específico para o container do banco (usado pelo docker-compose)
DB_PASSWORD=admin_password

# --- SEGURANÇA (JWT AUTH) ---
# Gere uma chave forte usando: openssl rand -hex 32
SECRET_KEY=insira_uma_chave_secreta_aqui_muito_longa_e_aleatoria

# Algoritmo de criptografia (Padrão: HS256)
ALGORITHM=HS256

# Tempo de expiração do token em minutos (Padrão: 60)
ACCESS_TOKEN_EXPIRE_MINUTES=60

# --- LOGS / DEBUG (OPCIONAL) ---
# DEBUG=True
# LOG_LEVEL=debug