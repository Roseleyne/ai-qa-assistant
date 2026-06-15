# ai/test_generator.py
"""
Gerador de casos de teste usando LLM (Claude/OpenAI).
Recebe uma user story e gera casos de teste em pytest + Playwright.

Uso:
    python ai/test_generator.py \
        --story "Como usuário, quero fazer login com email e senha" \
        --output tests/ai_generated/
"""

import argparse
import os
import re
from pathlib import Path
from datetime import datetime


def generate_with_claude(user_story: str) -> str:
    """Gera casos de teste usando Claude (Anthropic)."""
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    prompt = f"""Você é uma Senior QA Engineer especialista em automação com Playwright e pytest.

User Story:
{user_story}

Gere casos de teste em Python com pytest e Playwright seguindo estas regras:
1. Use fixtures do pytest (não setup/teardown de classe)
2. Nomes de funções descritivos com prefixo test_
3. Cubra: happy path, edge cases e cenários negativos
4. Use Page Object Model — importe de 'pages.' mas não implemente a classe
5. Inclua docstrings em cada teste
6. Use apenas a biblioteca padrão do Playwright (sync_api)
7. Retorne APENAS o código Python, sem markdown, sem explicações

Estrutura esperada:
- imports
- @pytest.mark decorators relevantes
- funções de teste com docstring
"""

    message = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2000,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return message.content[0].text


def generate_with_openai(user_story: str) -> str:
    """Gera casos de teste usando GPT-4 (OpenAI)."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'system',
                'content': 'Você é uma Senior QA Engineer especialista em Python, pytest e Playwright. Retorne APENAS código Python válido, sem markdown.'
            },
            {
                'role': 'user',
                'content': f'Gere casos de teste pytest/Playwright para esta user story:\n\n{user_story}'
            }
        ],
        temperature=0.2,
        max_tokens=2000,
    )
    return response.choices[0].message.content


def extract_function_names(code: str) -> list[str]:
    """Extrai nomes das funções de teste geradas."""
    return re.findall(r'def (test_\w+)', code)


def save_generated_tests(code: str, output_dir: str, story_slug: str) -> str:
    """Salva o código gerado em arquivo."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename  = f"test_{story_slug}_{timestamp}_ai_raw.py"
    filepath  = Path(output_dir) / filename

    header = f'''# ⚠️  GERADO POR IA — NÃO REVISADO
# User Story: {story_slug.replace("_", " ").title()}
# Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}
# STATUS: Aguardando revisão humana
#
# IMPORTANTE: Revisar antes de usar em CI/CD:
#   [ ] Seletores corretos para o projeto
#   [ ] Dados de teste contextualizados
#   [ ] Asserções de negócio adequadas
#   [ ] Remover testes duplicados ou sem valor
# ─────────────────────────────────────────────────

'''
    filepath.write_text(header + code, encoding='utf-8')
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description='Gerar testes com IA')
    parser.add_argument('--story',    required=True, help='User story para gerar testes')
    parser.add_argument('--output',   default='tests/ai_generated/', help='Diretório de saída')
    parser.add_argument('--provider', choices=['claude', 'openai'], default='claude')
    args = parser.parse_args()

    print(f"\n🧠 Gerando casos de teste com {args.provider.upper()}...")
    print(f"📖 User Story: {args.story}\n")

    if args.provider == 'claude':
        code = generate_with_claude(args.story)
    else:
        code = generate_with_openai(args.story)

    slug     = re.sub(r'\W+', '_', args.story[:40]).lower().strip('_')
    filepath = save_generated_tests(code, args.output, slug)
    tests    = extract_function_names(code)

    print(f"✅ {len(tests)} casos de teste gerados:")
    for t in tests:
        print(f"   • {t}")
    print(f"\n📁 Arquivo salvo em: {filepath}")
    print(f"\n⚠️  PRÓXIMO PASSO: Revisar e mover para tests/human_reviewed/ após validação.")


if __name__ == '__main__':
    main()
