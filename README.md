# 📊 Análise de Feedbacks de Clientes

Este projeto automatiza o processo de coleta, tratamento e visualização de feedbacks de clientes com o objetivo de apoiar decisões em áreas de Customer Success e Operações. Os dados são extraídos de uma API pública, organizados com Python e exibidos visualmente no Google Sheets por meio de dashboards simples e funcionais.

## Funcionalidades:

- Consumo de dados via API pública (JSON).
- Processamento e limpeza dos dados com Python.
- Cálculo de indicadores como tempo médio de resposta, quantidade de resolução por analista, distribuição por categoria (positivo, negativo e neutro), entre outros.
- Exportação dos dados tratados para uma aba específica do Google Sheets (`Feedbacks`).
- Geração de gráficos automáticos na aba (`Gráficos`), configurados para atualizar-se automaticamente com base em intervalos nomeados que refletem as informações mais recentes. Dessa forma, os gráficos acompanham as atualizações dos dados sem necessidade de intervenção manual.
- Integração automatizada com Google Sheets, com estrutura preparada para futura adição de agendamentos e alertas, facilitando expansão do projeto.

## Tecnologias utilizadas:

- Python 3
- Bibliotecas: `requests`, `gspread`, `pandas`, `oauth2client`
- Google Sheets API

## 🔐 Autenticação

Este projeto requer credenciais do Google para acessar a API do Google Sheets.

Crie um arquivo chamado `credenciais-google.json` com suas credenciais e salve na raiz do projeto.

Você pode gerar esse arquivo seguindo o guia oficial da [Google Cloud](https://cloud.google.com/docs/authentication/getting-started).

> **Nota:** O arquivo `credenciais-google.json` está incluído no `.gitignore` e não é enviado ao GitHub, garantindo a segurança das informações sensíveis.

## Organização dos dados no Google Sheets:

- **Aba `Feedbacks`**: contém os dados tratados e atualizados via script Python.
- **Aba `Resumo por Analista`**: apresenta o tempo médio de resposta (em dias) de cada analista. Essa visualização facilita a identificação de padrões de atendimento e permite comparações de desempenho entre os membros da equipe.
- **Aba `Gráficos`**: contém gráficos automáticos com os principais indicadores do projeto.

### Exemplos visuais:

![Dashboard com feedbacks](imgs/dashboard-feedbacks.png)

![Tempo médio de resposta dos analistas](imgs/resumo-analista.png)

![Gráficos gerados automaticamente](imgs/graficos.png)

## Como executar:

1. Clone o repositório:  
```bash
git clone https://github.com/brunadgarcia/analise-feedbacks-clientes.git
cd analise-feedbacks-clientes
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Coloque seu arquivo `credenciais-google.json` na raiz do projeto.

4. Execute o script principal:
```bash
python script.py
```

`Importante:` Para executar o projeto, você deve criar um arquivo credenciais-google.json na raiz do projeto com as credenciais da sua conta de serviço do Google Cloud. Esse arquivo não está incluído no repositório por questões de segurança.
