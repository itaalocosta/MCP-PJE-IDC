# Manual para Leigo: Seu Sistema de Consulta de Tribunais Online

Olá! Este manual foi feito especialmente para você, que não entende de programação, mas quer ter seu próprio sistema de consulta de processos judiciais online e integrado com o Claude. Vamos juntos, passo a passo, de forma bem simples e didática!

---

## O que vamos fazer?

Vamos colocar um sistema super legal na internet que faz o seguinte:

1.  **Consulta Processos:** Ele consegue buscar informações de processos em vários tribunais do Brasil (como PJE, eproc, eSAJ, etc.).
2.  **É Online:** Você vai ter um link na internet para acessar seu sistema de qualquer lugar.
3.  **Conecta com o Claude:** O mais legal! Você vai poder pedir para o Claude (seu assistente de IA) consultar processos para você, usando a sua voz ou texto simples.

E o melhor: vamos fazer isso de um jeito que não custa quase nada (uns R$15-35 por mês, que é bem barato para um sistema assim!).

---

## Parte 1: Preparando o Terreno (Seu Projeto no GitHub)

Para colocar seu sistema na internet, precisamos primeiro que ele esteja em um lugar que a internet 


entenda: o GitHub. Pense no GitHub como uma "nuvem" onde você guarda os arquivos do seu projeto de forma organizada.

### Passo 1.1: Baixar os Arquivos do Projeto

Primeiro, você precisa ter os arquivos do sistema no seu computador. Eu já criei todos eles para você! Eles estão em um arquivo compactado chamado `tribunal-api-complete.tar.gz` que eu te enviei. Você precisa descompactar esse arquivo em uma pasta no seu computador. Por exemplo, crie uma pasta chamada `meu_sistema_tribunais` e coloque os arquivos lá dentro.

Dentro dessa pasta, você verá outras pastas e arquivos, como `tribunal-api` (que é o coração do sistema) e `tribunal-mcp-server.py` (que faz a conexão com o Claude).

### Passo 1.2: Criar uma Conta no GitHub

Se você ainda não tem, crie uma conta gratuita no GitHub:

1.  Acesse [github.com](https://github.com/).
2.  Clique em `Sign up` (Registrar-se) e siga as instruções para criar sua conta. É como criar um e-mail ou qualquer outra conta online.

### Passo 1.3: Instalar o Git no seu Computador

O Git é uma ferramenta que nos ajuda a "conversar" com o GitHub. É como um programa que você instala no seu computador.

1.  Acesse [git-scm.com/downloads](https://git-scm.com/downloads).
2.  Baixe a versão para o seu sistema operacional (Windows, macOS ou Linux) e siga as instruções de instalação. Geralmente, é só clicar em "Next" (Próximo) várias vezes.

### Passo 1.4: Colocar seu Projeto no GitHub

Agora, vamos "subir" os arquivos do seu sistema para o GitHub. Abra o programa "Terminal" (no macOS/Linux) ou "Git Bash" (no Windows). Ele parece uma tela preta com letras brancas, onde você digita comandos.

1.  **Navegue até a pasta do seu projeto.** Digite o comando `cd` (change directory) seguido do caminho da pasta onde você descompactou os arquivos. Por exemplo:

    ```bash
    cd C:/Users/SeuUsuario/meu_sistema_tribunais  # No Windows
    # ou
    cd /home/SeuUsuario/meu_sistema_tribunais  # No Linux/macOS
    ```
    Pressione Enter. Se deu certo, a linha de comando vai mudar para mostrar que você está dentro da pasta.

2.  **Inicialize o Git na pasta:**

    ```bash
    git init
    ```
    Pressione Enter. Você verá uma mensagem como `Initialized empty Git repository in ...`.

3.  **Adicione todos os arquivos para serem "rastreados" pelo Git:**

    ```bash
    git add .
    ```
    Pressione Enter. Pode não aparecer nada, mas ele está trabalhando.

4.  **"Salvar" as mudanças (commit):**

    ```bash
    git commit -m "Primeira versão do sistema de tribunais"
    ```
    Pressione Enter. Você verá uma lista dos arquivos que foram "salvos".

5.  **Crie um repositório vazio no GitHub:**

    *   No site do GitHub, clique no sinal de `+` no canto superior direito e selecione `New repository` (Novo repositório).
    *   Dê um nome para o repositório (ex: `tribunal-online`).
    *   **Importante:** Não marque nenhuma opção (como `Add a README file` ou `Add .gitignore`). Deixe tudo em branco e clique em `Create repository`.

6.  **Conecte seu projeto local ao GitHub e envie os arquivos:**

    Na página do seu novo repositório no GitHub, você verá algumas instruções. Copie as duas últimas linhas que começam com `git remote add origin` e `git branch -M main` e `git push -u origin main`.

    Cole essas linhas no seu Terminal/Git Bash e pressione Enter após cada uma. Quando pedir seu nome de usuário e senha do GitHub, digite-os.

    ```bash
    git remote add origin https://github.com/SEU_USUARIO/tribunal-online.git
    git branch -M main
    git push -u origin main
    ```
    Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub e `tribunal-online.git` pelo nome do seu repositório. Após o `git push`, seus arquivos estarão no GitHub!

---

## Parte 2: Colocando seu Sistema Online com Railway

O Railway é uma plataforma que pega os arquivos do seu GitHub e os coloca para funcionar na internet. É bem fácil!

### Passo 2.1: Criar uma Conta no Railway

1.  Acesse [railway.app](https://railway.app/).
2.  Clique em `Login` e escolha `Login with GitHub`. Isso vai conectar sua conta do GitHub ao Railway, o que facilita muito o processo.

### Passo 2.2: Criar um Novo Projeto no Railway

1.  Após fazer login, você verá o painel do Railway.
2.  Clique em `New Project` (Novo Projeto).
3.  Selecione `Deploy from GitHub Repo` (Fazer Deploy de Repositório GitHub).
4.  Escolha o repositório que você acabou de criar no GitHub (ex: `tribunal-online`).
5.  O Railway vai começar a analisar seu projeto. Ele deve detectar que é um projeto Python.

### Passo 2.3: Configurar o Serviço (Seu Sistema)

Depois que o Railway detectar seu projeto, ele vai criar um "serviço" para ele. Clique nesse serviço para configurá-lo.

1.  **Aba `Settings` (Configurações):**
    *   **Build Command (Comando de Construção):** Aqui, você diz ao Railway como preparar seu sistema. Digite:
        ```
        pip install -r requirements.txt
        ```
    *   **Start Command (Comando de Início):** Aqui, você diz ao Railway como ligar seu sistema. Digite:
        ```
        python src/main.py
        ```
    *   **Root Directory (Diretório Raiz):** Se você colocou a pasta `tribunal-api` diretamente na raiz do seu repositório GitHub, deixe este campo vazio. Se você colocou todos os arquivos dentro de uma pasta `meu_sistema_tribunais` e depois subiu essa pasta para o GitHub, então o `Root Directory` deve ser `tribunal-api` (porque é onde o `src/main.py` está).

2.  **Aba `Variables` (Variáveis):**
    *   Aqui, precisamos informar algumas coisas importantes para o seu sistema funcionar corretamente. Clique em `New Variable` e adicione estas:
        *   **Nome:** `FLASK_ENV`
        *   **Valor:** `production`

        *   **Nome:** `PYTHONPATH`
        *   **Valor:** `/app` (Se o seu `src/main.py` estiver diretamente na raiz do projeto, use `/app`. Se estiver em `tribunal-api/src/main.py` e `tribunal-api` for o `Root Directory` no Railway, use `/app` também. Se o `Root Directory` for a raiz do seu repositório e `tribunal-api` for uma subpasta, use `/app/tribunal-api`)

        *   **Nome:** `PORT`
        *   **Valor:** `5001` (Essa é a porta que seu sistema usa internamente. O Railway vai cuidar de expor isso para a internet.)

### Passo 2.4: Aguardar o Deploy e Obter o Link

1.  Depois de configurar tudo, o Railway vai começar a "construir" e "ligar" seu sistema. Isso pode levar alguns minutos.
2.  Você pode acompanhar o progresso na aba `Deployments` (Implantações).
3.  Quando o deploy estiver completo, o Railway vai te dar um **link público** para o seu sistema. Ele estará na aba `Domains` (Domínios) ou no topo da página do seu serviço. Será algo parecido com `https://tribunal-api-xxxx.up.railway.app/`.

**Parabéns!** Seu sistema de consulta de tribunais está online! Você pode acessar esse link no seu navegador para ver a interface web funcionando.

---

## Parte 3: Conectando seu Sistema ao Claude (Integração MCP)

Agora que seu sistema está online, vamos fazer o Claude "conversar" com ele. Para isso, usaremos o que chamamos de MCP (Model Context Protocol). Pense nisso como um "tradutor" que permite que o Claude entenda e use seu sistema.

### Passo 3.1: Atualizar o Arquivo de Conexão (tribunal-mcp-server.py)

O arquivo `tribunal-mcp-server.py` é o que faz a ponte entre o Claude e o seu sistema online. Precisamos dizer a ele qual é o link do seu sistema no Railway.

1.  **Localize o arquivo `tribunal-mcp-server.py`** na pasta que você descompactou no seu computador.

2.  **Abra o arquivo com um editor de texto simples** (como Bloco de Notas no Windows, TextEdit no macOS, ou Notepad++ / VS Code se você tiver). **Cuidado para não mudar nada além do que eu vou te falar!**

3.  **Procure a linha que começa com `API_BASE_URL`**. Ela deve ser parecida com esta:

    ```python
    API_BASE_URL = "http://localhost:5001/api"
    ```

4.  **Mude essa linha para usar o link do seu Railway.** Substitua `http://localhost:5001` pelo link que o Railway te deu. Por exemplo:

    ```python
    API_BASE_URL = "https://tribunal-api-xxxx.up.railway.app/api"  # Use o SEU link do Railway aqui!
    ```

5.  **Salve o arquivo `tribunal-mcp-server.py`** após fazer a alteração.

### Passo 3.2: Instalar o Servidor MCP no seu Computador

O servidor MCP precisa rodar no seu computador para que o Claude Desktop (que também roda no seu computador) possa se comunicar com ele.

1.  **Abra o Terminal/Git Bash** novamente.

2.  **Instale as ferramentas necessárias:**

    ```bash
    pip install mcp httpx
    ```
    Pressione Enter. Isso vai instalar os programas que o servidor MCP precisa para funcionar.

3.  **Deixe o Servidor MCP Rodando:**

    ```bash
    python3 /caminho/para/tribunal-mcp-server.py  # Substitua pelo caminho correto do arquivo
    ```
    Pressione Enter. **Deixe essa janela do Terminal/Git Bash aberta e não feche!** Enquanto ela estiver aberta, seu servidor MCP estará funcionando e o Claude poderá se comunicar com ele.

### Passo 3.3: Configurar o Claude Desktop

Agora, vamos dizer ao Claude Desktop para usar o seu novo servidor MCP.

1.  **Localize o arquivo de configuração do Claude Desktop:**
    *   **No macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   **No Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2.  **Abra este arquivo com um editor de texto simples.**

3.  **Adicione a seguinte configuração dentro das chaves `{}` do arquivo.** Se já houver algo lá, adicione depois da última chave `}` e antes da chave `}` final do arquivo, separando com uma vírgula `,`.

    ```json
    {
      "mcpServers": {
        "tribunal-mcp": {
          "command": "python3",
          "args": ["/caminho/para/tribunal-mcp-server.py"]
        }
      }
    }
    ```
    **Importante:** Substitua `/caminho/para/tribunal-mcp-server.py` pelo caminho **completo e correto** do arquivo no seu computador. Por exemplo, no Windows, seria algo como `"C:\Users\SeuUsuario\meu_sistema_tribunais\tribunal-mcp-server.py"` (note as barras duplas `\\`).

4.  **Salve o arquivo `claude_desktop_config.json`**.

5.  **Reinicie o Claude Desktop.** Feche o programa e abra-o novamente. Isso fará com que ele leia as novas configurações.

**Pronto!** Agora o Claude Desktop está configurado para usar seu sistema de consulta de tribunais. Você pode testar pedindo coisas como:

*   "Consulte o processo número 1234567-89.0123.4.56.7890"
*   "Liste todos os tribunais disponíveis"
*   "Qual o status do sistema de tribunais?"

---

## Parte 4: Entendendo o Login e Senha dos Tribunais (PJE, eproc, eSAJ)

Essa é uma pergunta muito importante! No mundo das APIs (que são como "portas" para sistemas), existem dois tipos principais:

1.  **APIs Públicas:** São aquelas que qualquer um pode usar, sem precisar de login e senha. Elas geralmente fornecem informações que já são públicas.
2.  **APIs Restritas:** São aquelas que exigem login e senha (ou alguma outra forma de autenticação) para serem usadas. Elas dão acesso a informações mais detalhadas ou funcionalidades específicas.

### Como Funciona Neste Projeto (Versão Atual)

Este sistema que eu criei para você usa a **API Pública do Datajud do CNJ (Conselho Nacional de Justiça)**. Essa API é ótima porque ela já reúne informações de **muitos tribunais brasileiros** e, o melhor, **não exige login e senha** para consultar processos públicos.

Isso significa que, com este sistema, você consegue consultar uma vasta quantidade de processos sem se preocupar em digitar seu login e senha do PJE, eproc ou eSAJ a cada consulta. É mais simples, mais rápido e mais seguro para você, pois suas credenciais não são usadas no sistema.

### E se eu precisar de Login e Senha no Futuro?

Você mencionou que o PJE, eproc e eSAJ podem pedir login e senha. É verdade! Algumas funcionalidades ou informações muito específicas desses sistemas podem exigir que você esteja logado.

**A boa notícia é:** A arquitetura do sistema que eu construí foi pensada para que, no futuro, seja possível adicionar essa funcionalidade! Se um dia você precisar acessar informações que só estão disponíveis com login e senha, o sistema poderá ser expandido para:

1.  **Gerenciar suas Credenciais:** O sistema teria um lugar seguro (no "backend", que é a parte que roda no servidor) para guardar seu login e senha de forma criptografada.
2.  **Fazer o Login por Você:** Quando você pedisse para consultar algo que exige login, o sistema usaria suas credenciais guardadas para se "logar" no tribunal automaticamente e buscar a informação.
3.  **Interface para Credenciais:** Poderíamos adicionar uma nova parte na interface web onde você digitaria e gerenciaria seus logins e senhas para cada tribunal que exigir.

**Por que não fizemos isso agora?** Para manter o projeto simples, rápido de montar e com o menor custo possível. A API Pública do Datajud já atende a maioria das necessidades de consulta de processos públicos. Adicionar a complexidade de gerenciar logins e senhas para cada tribunal aumentaria o tempo de desenvolvimento e a manutenção.

Mas fique tranquilo(a)! Se essa necessidade surgir, o sistema está preparado para essa evolução.

---

## Dicas Importantes para o Leigo

*   **Não Feche o Terminal do Servidor MCP:** Lembre-se que a janela do Terminal/Git Bash onde você rodou `python3 /caminho/para/tribunal-mcp-server.py` precisa ficar aberta enquanto você quiser usar o Claude para consultar tribunais. Se você fechar, a conexão será perdida.
*   **Se Algo Der Errado:** Não se preocupe! A programação tem muitos detalhes. Se algo não funcionar, revise os passos com calma, prestando atenção aos caminhos dos arquivos e aos comandos. Pequenos erros de digitação são comuns.
*   **Atualizações:** Se você fizer alguma alteração nos arquivos do seu projeto e quiser que elas apareçam no seu sistema online, você precisará "subir" as mudanças para o GitHub (`git add .`, `git commit -m "sua mensagem"`, `git push origin main`) e o Railway fará o deploy automático.

---

**Parabéns!** Você acaba de dar um grande passo no mundo da tecnologia, colocando um sistema complexo online e integrando-o com inteligência artificial. Espero que este manual tenha sido útil e que você aproveite muito seu novo sistema!

