# autentica

Autenticação dos produtos **GlbHash**

Para configurar e rodar o ambiente, siga os passos abaixo:


```bash
- python -m venv .venv
- .venv\Scripts\activate  
- railway --version  
- pip freeze > requirements.txt
- pip install -r requirements.txt
- npm i -g @railway/cli
- railway login
- railway link -p 50594409-8ec3-4211-9cf7-6f4ef2f9afc8
- railway up
- .venv\Scripts\python manage.py migrate

https://autentica-desenvolvimento.up.railway.app/