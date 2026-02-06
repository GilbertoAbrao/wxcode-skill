# Análise de Gaps: Impacto no WXCODE

**Data:** 2026-02-05
**Baseado em:**
- `deep-dive-knowledge-graph-ast-llm.md`
- `docs/analise-comparativa-knowledge-graph-ast-llm.md`

---

## Sumário Executivo

Esta análise avalia como a implementação dos gaps identificados no wxcode-cli impactaria o **WXCODE** (sistema de workflows para Claude Code). A conclusão é clara: **o maior gap é a ausência do Pipeline de Compreensão** — a etapa onde o LLM enriquece o grafo com explicações semânticas ANTES de fazer conversão.

---

## 1. Os 3 Gaps Críticos

| Gap | WXCODE-CLI Atual | Proposto | Impacto no WXCODE |
|-----|------------------|----------|-------------------|
| **Embeddings Vetoriais** | Busca por texto/regex | Busca semântica | Perguntas em linguagem natural |
| **Pipeline de Compreensão** | LLM recebe código bruto | LLM recebe código + explicações | Conversões muito mais precisas |
| **Business Rules como Nós** | Regras implícitas no código | Regras extraídas e navegáveis | Rastreabilidade requisitos ↔ código |

---

## 2. Como Cada Gap Melhoraria o WXCODE

### 2.1 Gap 1: Embeddings Vetoriais

**Situação atual no WXCODE:**
```
/wxcode:trace PAGE_Login  → Precisa saber o nome exato
mcp__wxcode-kb__search_code "ValidaCPF"  → Busca literal
```

**Com embeddings:**
```
mcp__wxcode-kb__semantic_search "onde valida o CPF do cliente?"
→ Encontra ValidaCPF, ValidaCNPJ, ValidaDocumento (semanticamente similares)
```

**Benefício para WXCODE:**
- `/wxcode:research-phase` poderia perguntar "como o sistema lida com autenticação?" e obter contexto rico
- `wxcode-legacy-analyzer` encontraria código relacionado por intenção, não apenas por nome
- `search_converted_similar` seria muito mais preciso (similaridade semântica + estrutural)

**Nova MCP Tool:**
```python
@mcp.tool
async def semantic_search(query: str, element_types: list[str] = None, limit: int = 10):
    """Busca elementos semanticamente similares à query em linguagem natural."""
```

---

### 2.2 Gap 2: Pipeline de Compreensão Bottom-Up (O MAIS IMPORTANTE)

**Situação atual no WXCODE:**

```
wxcode-executor recebe:
├─ Código bruto da PAGE
├─ Controles (lista)
├─ Procedures (código cru)
└─ Dependências (nomes)

→ LLM precisa entender TUDO do zero a cada conversão
→ Conversões menos precisas
→ Contexto desperdiçado
```

**Com Pipeline de Compreensão:**

```
wxcode-executor recebe:
├─ Código da PAGE
├─ explanation: "Página de login com autenticação por CNPJ/CPF"
├─ Procedures COM explicações:
│   ├─ Local_Acessar: "Autentica usuário, gera sessão, redireciona"
│   ├─ Local_EsqueceuSenha: "Envia email SMTP com link de reset"
│   └─ businessRules: [
│       "CPF deve ter 11 dígitos válidos",
│       "Senha expira em 90 dias",
│       "3 tentativas incorretas bloqueia conta"
│   ]
├─ capabilities: ["Autenticação", "Recuperação de Senha"]
└─ userJourney: "Usuário → Login → Dashboard ou Erro"

→ LLM recebe contexto pré-digerido
→ Conversões muito mais precisas
→ Menos tokens gastos re-entendendo código
```

**Benefícios concretos para comandos/agentes WXCODE:**

| Comando/Agente | Benefício |
|----------------|-----------|
| `wxcode-executor` | Recebe explicações prontas, converte com mais precisão |
| `wxcode-legacy-analyzer` | Não precisa re-analisar, consulta explicações do grafo |
| `wxcode-planner` | Pode agrupar fases por capability, não apenas por dependência |
| `/wxcode:discuss-phase` | Mostra business rules extraídas para validar com usuário |
| `/wxcode:audit-milestone` | Verifica se todas business rules foram preservadas |
| `/wxcode:new-milestone` | Sugere elementos por capability, não apenas por ordem topológica |

**Pipeline de Compreensão Proposto:**

```
Nível 0: Explicar cada PROCEDURE individual
    └─ Input: código da procedure + variáveis + queries embutidas
    └─ Output: "O que esta procedure faz" + "Regras de negócio identificadas"

Nível 1: Explicar cada WINDOW/PAGE
    └─ Input: summaries de todas procedures da window + controles + layout
    └─ Output: "O que esta tela faz" + "Jornada do usuário"

Nível 2: Explicar cada MÓDULO/SUBSISTEMA
    └─ Input: summaries de todas windows + queries compartilhadas + tabelas
    └─ Output: "Que capability de negócio este módulo implementa"

Nível 3: Explicar o SISTEMA
    └─ Input: summaries de todos módulos
    └─ Output: "Capability map completo" + "Fluxos de negócio end-to-end"
```

---

### 2.3 Gap 3: Business Rules como Nós

**Situação atual:**
- Regras de negócio ficam escondidas no código
- Sem rastreabilidade "requisito → código → conversão"
- BAs não conseguem participar

**Com Business Rules explícitas:**

```cypher
// Consulta Neo4j
MATCH (br:BusinessRule)-[:EXTRACTED_FROM]->(p:Procedure)
WHERE br.category = 'validation'
RETURN br.description, p.name

// Resultado:
// "CPF deve ter 11 dígitos válidos" ← ValidaCPF()
// "CNPJ deve ter 14 dígitos válidos" ← ValidaCNPJ()
// "Desconto máximo de 15% sem aprovação" ← CalculaDesconto()
```

**Nova MCP Tool para WXCODE:**
```python
@mcp.tool
async def get_business_rules(element_name: str, category: str = None):
    """Retorna regras de negócio extraídas de um elemento."""
    # Retorna regras com: descrição, confiança, linha no código
```

**Benefício para WXCODE:**

```markdown
## /wxcode:discuss-phase output (novo)

Analisando **PAGE_Pedido**...

### Business Rules Identificadas

| Regra | Confiança | Procedure |
|-------|-----------|-----------|
| Cliente deve ter crédito aprovado | 95% | VerificaCredito() |
| Pedido mínimo de R$ 50,00 | 90% | ValidaPedidoMinimo() |
| Desconto máximo 15% sem gerente | 85% | AplicaDesconto() |

**Estas regras devem ser preservadas na conversão?**
```

---

## 3. Novos Comandos/Agents Possíveis

### 3.1 `/wxcode:comprehend` (Novo Comando)

```markdown
/wxcode:comprehend [--project | --element <name>]

Executa pipeline de compreensão bottom-up:
1. Enriquece procedures com explicações
2. Enriquece pages com summaries das procedures
3. Extrai business rules
4. Gera capability map

Output:
- Atualiza grafo Neo4j com explicações
- Gera COMPREHENSION-REPORT.md
```

### 3.2 `/wxcode:capability-map` (Novo Comando)

```markdown
/wxcode:capability-map

Gera mapa hierárquico de capabilities do sistema:

Sistema SimetraCliente
├── Autenticação
│   ├── Login (PAGE_Login, PAGE_LoginMobile)
│   └── Recuperação de Senha (PAGE_RecuperaSenha)
├── Gestão de Clientes
│   ├── Cadastro (PAGE_CadCliente)
│   └── Consulta (PAGE_ConsultaCliente)
└── Faturamento
    ├── Emissão de NF (PAGE_EmiteNF)
    └── Consulta de Faturas (PAGE_ConsultaFaturas)
```

### 3.3 `wxcode-comprehension-enricher` (Novo Agente)

```markdown
**Purpose:** Executa pipeline de compreensão bottom-up.

**Capabilities:**
- Travessia pós-ordem do grafo
- Geração de explicações por nível
- Extração de business rules
- Identificação de capabilities

**Output:** Atualiza nós no MongoDB/Neo4j com campo `explanation`
```

### 3.4 Melhoria no `wxcode-executor`

```markdown
## Contexto Enriquecido (novo)

Antes de converter, o executor agora recebe:

1. **Explicação do elemento** (gerada pelo comprehension pipeline)
2. **Business rules** a preservar
3. **Capability** que implementa
4. **Elementos similares já convertidos** (com embeddings semânticos)

Isso resulta em:
- Conversões mais precisas
- Menos re-trabalho
- Consistência entre conversões similares
```

---

## 4. Novas MCP Tools Propostas

### Categoria: Comprehension

```python
@mcp.tool
async def get_explanation(element_name: str, level: str = "element"):
    """Retorna explicação gerada pelo pipeline de compreensão.

    Args:
        element_name: Nome do elemento
        level: "element" | "procedures" | "business_rules" | "capability"
    """

@mcp.tool
async def get_business_rules(element_name: str, category: str = None):
    """Retorna regras de negócio extraídas do elemento.

    Args:
        element_name: Nome do elemento
        category: "validation" | "calculation" | "workflow" | "permission" | None
    """

@mcp.tool
async def get_capability_map(project_name: str, level: int = 2):
    """Retorna mapa hierárquico de capabilities do projeto.

    Args:
        project_name: Nome do projeto
        level: Profundidade da hierarquia (1-3)
    """
```

### Categoria: Semantic Search

```python
@mcp.tool
async def semantic_search(query: str, element_types: list[str] = None, limit: int = 10):
    """Busca elementos semanticamente similares à query.

    Args:
        query: Pergunta em linguagem natural
        element_types: Filtro por tipo (page, procedure, class, etc.)
        limit: Máximo de resultados

    Returns:
        Lista de elementos com score de similaridade
    """

@mcp.tool
async def find_similar_by_embedding(element_name: str, min_similarity: float = 0.7):
    """Encontra elementos semanticamente similares usando embeddings.

    Mais preciso que search_converted_similar (que usa apenas estrutura).
    """
```

---

## 5. Impacto Quantitativo Esperado

| Métrica | Atual | Com Gaps Implementados |
|---------|-------|------------------------|
| Precisão de conversão | ~70% | ~90% (LLM com contexto rico) |
| Tempo de análise/elemento | Alto (re-análise cada vez) | -50% (explicações pré-geradas) |
| Regras de negócio documentadas | 0% | 60%+ automático |
| Busca semântica | 0% | 100% |
| Onboarding de novos projetos | Semanas | Dias (docs automáticas) |
| Consistência entre conversões | Variável | Alta (embeddings + regras) |

---

## 6. Roadmap de Implementação

### Fase 1: Preparação (2-3 semanas)

**Objetivo:** Preparar estrutura para enriquecimento

1. **Adicionar campo `explanation` nos modelos**
   ```python
   # Element, Procedure, ClassDefinition
   explanation: Optional[str] = None
   explanation_generated_at: Optional[datetime] = None
   ```

2. **Criar modelo BusinessRule**
   ```python
   class BusinessRule(Document):
       description: str
       confidence: float
       source_procedure_id: ObjectId
       source_line_range: tuple[int, int]
       category: str  # validation, calculation, workflow, etc.
   ```

3. **Sincronizar com Neo4j**
   - Campo `explanation` nos nós
   - Nó `BusinessRule` com arestas `EXTRACTED_FROM`

### Fase 2: Comprehension Pipeline (3-4 semanas)

**Objetivo:** Implementar enriquecimento bottom-up

1. **Criar `BottomUpEnricher`**
   ```python
   class BottomUpEnricher:
       async def enrich_project(self, project_id: ObjectId):
           # Nível 0: Procedures
           # Nível 1: Pages/Windows
           # Nível 2: Módulos
           # Nível 3: Sistema
   ```

2. **Popular explicações automaticamente**
   - Integrar com `enrich` command
   - Flag `--with-comprehension`

3. **Extrair business rules**
   - Prompts especializados para WLanguage
   - Categorização automática

### Fase 3: Semantic Search (2-3 semanas)

**Objetivo:** Habilitar busca por linguagem natural

1. **Integrar biblioteca de embeddings**
   - sentence-transformers: `all-MiniLM-L6-v2` (768 dims)
   - Ou OpenAI embeddings

2. **Criar índice vetorial no Neo4j**
   ```cypher
   CREATE VECTOR INDEX code_embeddings
   FOR (n:Procedure) ON (n.embedding)
   OPTIONS {indexConfig: {`vector.dimensions`: 768, `vector.similarity_function`: 'cosine'}}
   ```

3. **Nova MCP tool: `semantic_search`**

### Fase 4: Integração WXCODE (2-3 semanas)

**Objetivo:** WXCODE usa os novos recursos

1. **Novo comando `/wxcode:comprehend`**
   - Dispara pipeline de compreensão
   - Gera relatório

2. **Novo comando `/wxcode:capability-map`**
   - Visualização de capabilities
   - Sugestão de ordem de conversão

3. **Atualizar `wxcode-executor`**
   - Buscar `explanation` antes de converter
   - Buscar `business_rules` para preservar
   - Usar `semantic_search` para contexto similar

4. **Atualizar `wxcode-legacy-analyzer`**
   - Usar explicações existentes
   - Não re-analisar se já enriquecido

---

## 7. Exemplo de Fluxo Melhorado

### Antes (Atual)

```
/wxcode:new-milestone --element=PAGE_Login

1. wxcode-legacy-analyzer analisa do zero
2. Contexto bruto passado para executor
3. LLM re-entende código durante conversão
4. Conversão pode perder regras de negócio
```

### Depois (Com Gaps Implementados)

```
/wxcode:new-milestone --element=PAGE_Login

1. Busca explicação pré-gerada: "Página de login CNPJ/CPF"
2. Busca business rules:
   - "CPF deve ter 11 dígitos"
   - "3 tentativas = bloqueio"
3. Busca capability: "Autenticação"
4. Busca similares convertidos (embedding):
   - PAGE_LoginMobile (85% similar) → já convertido
5. Contexto rico passado para executor
6. LLM converte com precisão
7. Verifica preservação das business rules
```

---

## 8. Conclusão

**O gap mais crítico é o Pipeline de Compreensão.** Implementá-lo traria:

1. **Conversões muito mais precisas** — LLM recebe código + explicações + regras
2. **Documentação automática** — explicações geradas servem como docs
3. **Planejamento por capability** — não apenas por dependência técnica
4. **Rastreabilidade completa** — requisito → regra → código → conversão
5. **Participação de BAs** — capability maps são compreensíveis por não-técnicos
6. **Consistência** — embeddings garantem conversões similares para código similar

O investimento de **~10-14 semanas** no wxcode-cli resultaria em um WXCODE **significativamente mais poderoso**, com conversões mais precisas e fluxo de trabalho mais inteligente.

---

## 9. Referências

- `deep-dive-knowledge-graph-ast-llm.md` — Estado da arte em engenharia reversa
- `docs/analise-comparativa-knowledge-graph-ast-llm.md` — Comparativo com implementação atual
- Papers: arXiv:2601.08773, arXiv:2601.10773, arXiv:2509.25257, arXiv:2512.12117
- Projetos: CodeGraph, code-graph-rag, Microsoft GraphRAG
