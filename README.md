# Desafio 1 — Containers em Rede


- **server/server.py**: Servidor Flask que responde a requisições HTTP.
- **client/client.sh**: Script que realiza requisições HTTP para o servidor em loop.
- **Dockerfile (server)**: Configura a imagem do servidor com Python e Flask.
- **Dockerfile (client)**: Configura a imagem do cliente com Alpine e `curl`.

---

## Como Rodar

```bash
# 1. Criar a rede Docker customizada
docker network create desafio1-net

# 2. Build da imagem do servidor
docker build -t d1-server -f Dockerfile.server

# 3. Build da imagem do cliente
docker build -t d1-client -f Dockerfile.client .

# 4. Rodar o container do servidor
docker run -d --network desafio1-net --name server d1-server

# 5. Rodar o container do cliente
docker run -d --network desafio1-net --name client d1-client

# 6. Verificar logs do cliente
docker logs client
````

# Desafio 2 — Volumes e Persistência


- **app.py**: Script Python que cria um banco SQLite, insere dados aleatórios e imprime os registros.
- **Dockerfile**: Imagem Python configurada para rodar o `app.py`.

---

## Como Rodar

```bash
# 1. Criar um volume Docker para persistência
docker volume create desafio2-volume

# 2. Build da imagem do container
docker build -t d2-image .

# 3. Rodar o container com volume montado
docker run --name d2-db -v desafio2-vol:/data d2-image

# 4. Apagar o container
docker rm d2-db

# 4. Rodar novamente o container (mesmo volume)
docker run --name d2-db -v desafio2-vol:/data d2-image

````

# Desafio 3 — Docker Compose Orquestrando Serviços


- **web/app.py**: API Flask que consulta dados no PostgreSQL e usa Redis como cache.
- **web/requirements.txt**: Dependências do Python (`Flask`, `psycopg2-binary`, `redis`).
- **web/Dockerfile**: Imagem do serviço web.
- **docker-compose.yml**: Orquestração dos 3 serviços com rede interna e volumes.

---

## Como Rodar

```bash
# 1. Build e start dos serviços via Docker Compose
docker-compose up --build -d

# 2. Verificar logs do serviço web
docker-compose logs -f web

# 3. Testar endpoints da API
# Listar todos os alunos
curl http://localhost:5000/todos

# Consultar aluno específico
curl http://localhost:5000/aluno/1


