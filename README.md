# Open Schedule API

# Introdução

Este repositório é um dos módulos do projeto Open Schedule.
O módulo atual trata se de ums REST API desenvolvida em Python com o framework Flask e é responsável pelo gerenciamento de agendamentos, horários e profissionais. Este módulo é deveras importante pois o front-end e o chatbot depende dele para o funcionamento.


# Pré-requisitos
- *Python*: Versão 3.10 ou superior e Pip instalado para gerenciamento de dependências.
- *Git*: Necessário para clonar o repositório e gerenciar o código fonte.
- *MySql*: O módulo depende de um banco dados como MySql ou MariaDB.

# Instalação
Está sessão possui o passo a passo para configuração e instalação desse módulo
1. **Clonar repositório**
    ```bash 
    git clone https://github.com/OpenScheduleOrg/openschedule-api.git
    cd openschedule-api
    ```

2. **Instalar dependências**

    Antes do próximo passo de preferência crie um ambiente virtual de python [venv - Criação de ambientes virtuais](https://docs.python.org/pt-br/3/library/venv.html)

    ```bash 
    pip install -r requirements.txt
    ```
    ```bash 
    pip install -e .
    ```

3. **Configurar Variáveis de Ambiente**

    Com base no arquivo .env.example crie uma copia chamada .env para a configuração variáveis de ambiente.

    Você verá que todas as váriaveis já possuem valores definidos como exemplo, para funcionar no ambiente de desenvolvimento apenas as alteração das váriaveis de banco de dados é necessário:
    - **DATABASE_USERNAME**: Nome de usário para conexão com banco
    - **DATABASE_PASSWORD**: Senha do usuário
    - **DATABASE_HOST**: Endereço do banco de dados
    - **DATABASE_PORT**: Porta para conexão com o banco de dados
    - **DATABASE**: Nome do banco de dados(schema) já criado


4. **Executar Aplicação**

    Utilize o comando abaixo para iniciar a aplicação, na primeira execução seram criados as tabelas e usuários no banco de dados
    ```bash 
    python3 -m flask run
    ```

5. Abra seu navegador e acesse `http://localhost:5000/apidocs`, a documentação gerada pelo Swagger deve aparecer. 
