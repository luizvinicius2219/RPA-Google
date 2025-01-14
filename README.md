Este projeto implementa uma automação RPA (Robotic Process Automation) para realizar a raspagem de notas no Google. A automação foi desenvolvida em Python, utilizando bibliotecas como schedulee integração com SQL para gerenciar e armazenar os dados encontrados.

Funcionalidades do Código
Raspagem de Dados do Google
O código automatiza a remoção de notas diretamente do Google, garantindo a coleta precisa e eficiente dos dados.

Agendamento Automático
Com a integração da biblioteca schedule, o código é programado para ser executado automaticamente em horários pré-determinados, eliminando a necessidade de execução manual.

Armazenamento em Banco de Dados
Os dados raspados são inseridos diretamente em uma tabela SQL. Esta tabela é utilizada como fonte de dados para relatórios no PowerBI, permitindo análises visuais e dinâmicas.

Integração com PowerBI
Uma tabela SQL gerada pelo código serve de base para a construção de relatórios interativos e gráficos detalhados, facilitando a tomada de decisões com base nos dados encontrados.

Como Funciona
Configuração Inicial

Clone este repositório e configure as dependências relacionadas no arquivo requirements.txt.
Configure as credenciais de acesso ao banco de dados SQL.
Execução e Agendamento

O código inicia automaticamente nos horários programados pela biblioteca schedule.
Durante a execução, ele acessa o Google, realiza a raspagem das notas e armazena os dados no banco de dados.
Resultados e Relatórios

Os dados armazenados podem ser usados ​​diretamente no PowerBI para gerar relatórios.
Tecnologias Utilizadas
Python
Para desenvolvimento da automação e integração com outras tecnologias.
Agendamento
Para agendamento e execução automática do código.
SQL
Para armazenamento e organização dos dados raspados.
PowerBI
Para visualização e análise dos dados coletados.
Como Executar
Instale as dependências do projeto:
bater

Copiar código
pip install -r requirements.txt
Configure suas credenciais de banco de dados no arquivo config.py.
Execute o código manualmente ou aguarde o agendamento:
bater

Copiar código
python main.py
Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma edição ou enviar um pull request com melhorias e sugestões.
