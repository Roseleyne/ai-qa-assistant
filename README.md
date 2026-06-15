# 🧠 AI-Assisted Testing

> Integração de Inteligência Artificial no processo de QA — geração de cenários de teste com LLMs, análise automática de requisitos, self-healing selectors com Playwright e prompts documentados.

![Playwright](https://img.shields.io/badge/Playwright-1.x-2EAD33?logo=playwright)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)
![AI](https://img.shields.io/badge/AI-LLM%20Powered-7B61FF)
![CI](https://github.com/Roseleyne/ai-qa-assistant/actions/workflows/ai-tests.yml/badge.svg)

---

## 📋 Sobre o Projeto

Projeto de referência que demonstra como integrar **Inteligência Artificial** ao processo de Quality Engineering — sem substituir o julgamento humano, mas amplificando a capacidade de cobertura e manutenção de testes.

> ⚠️ **Postura crítica:** AI gera sugestões, não garantias. Todos os outputs de IA neste projeto são revisados e validados por uma QA Engineer experiente antes de entrar em produção. O projeto documenta tanto os acertos quanto as limitações dos modelos.

### O que este projeto demonstra

- **Geração de casos de teste** a partir de requisitos e user stories via LLM
- **Self-healing selectors** com Playwright — recuperação automática de seletores quebrados
- **Análise de requisitos** para identificar cenários de edge case não cobertos
- **Comparativo documentado** entre output bruto de IA vs. versão revisada por QA humana
- Pipeline CI/CD com execução automática via **GitHub Actions**

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Automação Web | Playwright 1.x |
| Linguagem | Python 3.11 |
| LLM Integration | OpenAI API / Claude API |
| Test Runner | pytest |
| CI/CD | GitHub Actions |
| Prompt Management | LangChain (opcional) |

---

## 🏗️ Arquitetura

```
ai-qa-assistant/
│
├── ai/
│   ├── test_generator.py        # Geração de casos de teste via LLM
│   ├── requirement_analyzer.py  # Análise de requisitos e identificação de gaps
│   └── prompts/
│       ├── generate_test_cases.txt
│       ├── analyze_requirements.txt
│       └── review_coverage.txt
│
├── tests/
│   ├── ai_generated/            # Casos gerados por IA (não editados)
│   │   └── test_login_ai_raw.py
│   ├── human_reviewed/          # Casos revisados por QA humana
│   │   └── test_login_reviewed.py
│   └── self_healing/
│       └── test_with_healing.py # Exemplo de self-healing selector
│
├── comparisons/                 # Documentação de AI vs. Human review
│   └── login_flow_comparison.md
│
├── pages/
│   └── base_page.py
│
├── .github/
│   └── workflows/
│       └── ai-tests.yml
│
├── requirements.txt
└── README.md
```

---

## ⚡ Como Rodar

### Pré-requisitos
- Python 3.11+
- Chave de API OpenAI ou Anthropic (Claude)

### Instalação

```bash
git clone https://github.com/Roseleyne/ai-qa-assistant.git
cd ai-qa-assistant

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### Configuração

```bash
# Criar arquivo .env
cp .env.example .env

# Preencher suas chaves
OPENAI_API_KEY=sua_chave_aqui
# ou
ANTHROPIC_API_KEY=sua_chave_aqui
```

### Gerar casos de teste com IA

```bash
# Gerar casos de teste a partir de uma user story
python ai/test_generator.py \
  --story "Como usuário, quero fazer login com email e senha" \
  --output tests/ai_generated/

# Analisar requisitos e identificar gaps de cobertura
python ai/requirement_analyzer.py \
  --requirements docs/requirements.md \
  --existing-tests tests/human_reviewed/
```

### Executar testes

```bash
# Todos os testes
pytest tests/ -v --alluredir=reports/

# Apenas testes revisados por humano
pytest tests/human_reviewed/ -v

# Comparar AI vs. Human
pytest tests/ -v --tb=short
```

---

## 🧩 Exemplos de Código

### Gerador de Casos de Teste
```python
# ai/test_generator.py
import anthropic

def generate_test_cases(user_story: str) -> str:
    client = anthropic.Anthropic()

    prompt = f"""
    Você é uma QA Engineer Sênior especialista em automação.
    
    User Story:
    {user_story}
    
    Gere casos de teste em Python com pytest e Playwright cobrindo:
    1. Happy path (fluxo feliz)
    2. Edge cases (casos extremos)
    3. Cenários negativos (entradas inválidas)
    4. Acessibilidade básica
    
    Retorne APENAS o código Python, sem explicações.
    """

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

### Self-Healing Selector
```python
# tests/self_healing/test_with_healing.py
from playwright.sync_api import Page

SELECTORS = {
    "login_btn": [
        "[data-cy=login-btn]",        # Primário (data-cy)
        "[data-testid=login]",         # Fallback 1
        "button:has-text('Entrar')",   # Fallback 2 (texto)
        "#login-button",               # Fallback 3 (ID)
    ]
}

def find_with_healing(page: Page, element_name: str):
    """Tenta seletores em ordem até encontrar um funcional."""
    for selector in SELECTORS[element_name]:
        try:
            locator = page.locator(selector)
            if locator.count() > 0:
                print(f"✅ Seletor funcional: {selector}")
                return locator
        except Exception:
            continue
    raise Exception(f"Nenhum seletor funcionou para: {element_name}")
```

---

## 📊 Comparativo: AI vs. Human Review

| Aspecto | AI (bruto) | Revisado por QA |
|---|---|---|
| Cobertura happy path | ✅ Boa | ✅ Boa |
| Edge cases | ⚠️ Parcial | ✅ Completo |
| Seletores frágeis | ❌ Sim | ✅ Corrigido |
| Dados de teste realistas | ⚠️ Genérico | ✅ Contextualizado |
| Asserções de negócio | ❌ Superficial | ✅ Profundo |
| Pronto para CI/CD | ❌ Não | ✅ Sim |

> **Conclusão:** IA acelera em ~60% o tempo de escrita inicial dos testes, mas revisão humana é indispensável para qualidade de produção.

---

## 👩‍💻 Autora

**Roseleyne Duarte Silva** — Senior QA Engineer | SDET

- 🌐 [Portfolio](https://roseleyne.github.io/portfolio)
- 💼 [LinkedIn](https://www.linkedin.com/in/roseleyne-duarte-silva/)
- 🐙 [GitHub](https://github.com/Roseleyne)
- 📧 roseleyne.duarte@gmail.com
