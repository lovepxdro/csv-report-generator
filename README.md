# CSV Report Generator

Ferramenta CLI em Python que analisa arquivos CSV e gera relatórios Excel adaptativos.

O projeto identifica automaticamente a estrutura do dataset, classifica seus tipos de dados e escolhe uma estratégia de análise adequada antes de gerar o arquivo `.xlsx`.

---

## Funcionalidades

- Detecção automática de colunas:
  - numéricas;
  - categóricas;
  - temporais.
- Classificação do perfil do dataset:
  - `mixed`;
  - `numeric`;
  - `categorical`;
  - `temporal`.
- Geração de:
  - aba com os dados originais;
  - resumo estatístico;
  - dashboard adaptado ao perfil detectado.
- Análises como:
  - estatísticas numéricas;
  - correlações;
  - variabilidade;
  - cardinalidade;
  - distribuições categóricas;
  - séries temporais.
- Tratamento básico de arquivos inválidos ou vazios.

---

## Estrutura

```text
csv-report-generator/
├── src/
│   ├── analyzer.py
│   ├── dashboard.py
│   ├── main.py
│   └── report.py
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

`analyzer.py` - Analisa o dataset, detecta tipos de colunas, calcula estatísticas e determina seu perfil.

`dashboard.py` - Seleciona e gera visualizações de acordo com o perfil identificado.

`report.py` - Responsável pela geração e formatação do arquivo Excel.

`main.py` - Interface de linha de comando e tratamento da entrada.

---

## Fluxo

```text
CSV
 ↓
Leitura e validação
 ↓
Detecção dos tipos de dados
 ↓
Classificação do perfil
 ↓
Análise estatística
 ↓
Geração do Excel
 ├── Dados
 ├── Resumo
 └── Dashboard
```

Cada perfil utiliza uma estratégia diferente de análise:

```text
numeric     → estatísticas, variabilidade e correlações
categorical → cardinalidade e distribuições
temporal    → evolução e eventos ao longo do tempo
mixed       → combinação de métricas, categorias e datas
```

---

## Uso

1. Instale as dependências:
```bash
uv sync
```

2. Gerar um relatório:
```bash
uv run python -m src.main arquivo.csv
```

3. Gerar um dashboard:
```bash
uv run python -m src.main arquivo.csv --mode dashboard
```

4. Definir o arquivo de saída:
```bash
uv run python -m src.main arquivo.csv \
  --mode dashboard \
  --output output/report.xlsx
```

5. Testes:
```bash
uv run pytest
```

> O projeto possui testes para detecção de tipos, classificação dos perfis, métricas estatísticas e validação de arquivos CSV.

---

## Limitações

A análise é baseada na estrutura e nos nomes das colunas. A ferramenta não possui conhecimento semântico completo sobre o domínio do dataset.

Arquivos com formatos incomuns, grandes volumes de dados, delimitadores diferentes ou encodings específicos podem exigir tratamento adicional.

---

## Futuras melhorias

- detecção automática de delimitador e encoding;
- processamento de arquivos grandes em chunks;
- suporte a outros formatos, como Parquet;
- configuração manual de métricas e dimensões;
- heurísticas mais avançadas para seleção de indicadores e gráficos.
