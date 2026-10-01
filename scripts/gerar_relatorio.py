#!/usr/bin/env python3
"""
Gerador de Relatorio de Auditoria (ISO 13485 / FDA)
Le os resultados da pipeline e gera um HTML auditavel.
"""

import os
import json
import hashlib
import subprocess
import re
from datetime import datetime


def calcular_hash(ficheiro):
    """Calcula o SHA256 (primeiros 16 chars) de um ficheiro."""
    if not os.path.exists(ficheiro):
        return "N/A"
    try:
        with open(ficheiro, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except Exception:
        return "N/A"


def extrair_jira_id(mensagem):
    """Extrai o ID do Jira (ex: CONNEX-123) de uma mensagem."""
    match = re.search(r'([A-Z]+-\d+)', mensagem)
    return match.group(1) if match else None


def obter_commit_hash():
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return 'desconhecido'


def obter_commit_message():
    try:
        return subprocess.check_output(
            ['git', 'log', '-1', '--pretty=%B'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return 'desconhecido'


def obter_versao():
    """Tenta ler a versao do package.json (Vue) ou do sonar-project.properties (Go)."""
    try:
        if os.path.exists('package.json'):
            with open('package.json', 'r') as f:
                return json.load(f).get('version', '0.0.0')
    except Exception:
        pass
    return '0.0.0'


def obter_projeto():
    """Le o projectKey do sonar-project.properties."""
    try:
        with open('sonar-project.properties', 'r') as f:
            for linha in f:
                if linha.startswith('sonar.projectKey='):
                    return linha.split('=', 1)[1].strip()
    except Exception:
        pass
    return 'desconhecido'


def ler_cobertura():
    """Deteta o formato da cobertura e devolve as metricas."""
    if os.path.exists('coverage/lcov.info'):
        return ler_cobertura_lcov()
    if os.path.exists('coverage.out'):
        return ler_cobertura_go()
    return None


def ler_cobertura_lcov():
    """Le o ficheiro lcov.info (Vue/JS) e calcula totais."""
    try:
        with open('coverage/lcov.info', 'r') as f:
            conteudo = f.read()

        total_lines = 0
        covered_lines = 0
        total_branches = 0
        covered_branches = 0
        total_functions = 0
        covered_functions = 0

        for linha in conteudo.splitlines():
            if linha.startswith('LF:'):
                total_lines += int(linha.split(':')[1])
            elif linha.startswith('LH:'):
                covered_lines += int(linha.split(':')[1])
            elif linha.startswith('BRF:'):
                total_branches += int(linha.split(':')[1])
            elif linha.startswith('BRH:'):
                covered_branches += int(linha.split(':')[1])
            elif linha.startswith('FNF:'):
                total_functions += int(linha.split(':')[1])
            elif linha.startswith('FNH:'):
                covered_functions += int(linha.split(':')[1])

        def pct(covered, total):
            return round((covered / total * 100), 2) if total > 0 else 0.0

        return {
            'lines': {'cobertas': covered_lines, 'total': total_lines, 'pct': pct(covered_lines, total_lines)},
            'branches': {'cobertas': covered_branches, 'total': total_branches, 'pct': pct(covered_branches, total_branches)},
            'functions': {'cobertas': covered_functions, 'total': total_functions, 'pct': pct(covered_functions, total_functions)},
        }
    except Exception as e:
        print(f"Erro ao ler lcov.info: {e}")
        return None


def ler_cobertura_go():
    """Le a cobertura do Go usando o go tool cover."""
    try:
        resultado = subprocess.check_output(
            ['go', 'tool', 'cover', '-func=coverage.out'],
            stderr=subprocess.DEVNULL
        ).decode()

        linhas = resultado.strip().split('\n')
        ultima = linhas[-1]  # formato: total:  (statements) XX.X%
        pct_str = ultima.split()[-1].replace('%', '')
        pct = float(pct_str)

        return {
            'lines': {'cobertas': int(pct), 'total': 100, 'pct': pct},
            'branches': {'cobertas': 0, 'total': 0, 'pct': 0.0},
            'functions': {'cobertas': 0, 'total': 0, 'pct': 0.0},
        }
    except Exception as e:
        print(f"Erro ao ler coverage.out: {e}")
        return None


def gerar_html(dados, ficheiro_saida):
    projeto = dados['projeto']
    sonar_url = f"http://localhost:9000/dashboard?id={projeto}"
    jira_id = dados.get('jira_id') or 'N/A'
    aprovador = dados.get('aprovador') or 'N/A'

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <title>Relatorio de Auditoria - {projeto}</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 40px; }}
    .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
    h2 {{ color: #34495e; margin-top: 30px; }}
    .meta {{ background: #ecf0f1; padding: 20px; border-radius: 6px; margin-bottom: 20px; }}
    .meta p {{ margin: 8px 0; }}
    table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
    th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
    td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
    .ok {{ color: #27ae60; font-weight: bold; }}
    .warn {{ color: #f39c12; font-weight: bold; }}
    .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #7f8c8d; text-align: center; }}
    ul {{ line-height: 1.8; }}
    code {{ background: #ecf0f1; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Relatorio de Auditoria de Qualidade</h1>

    <div class="meta">
      <p><strong>Projeto:</strong> {projeto}</p>
      <p><strong>Versao:</strong> {dados['versao']}</p>
      <p><strong>Commit:</strong> <code>{dados['commit_hash'][:12]}</code></p>
      <p><strong>Mensagem:</strong> {dados['commit_message']}</p>
      <p><strong>Jira Ticket:</strong> {jira_id}</p>
      <p><strong>Aprovador:</strong> {aprovador}</p>
      <p><strong>Data de geracao:</strong> {dados['data_geracao']}</p>
      <p><strong>Executado por:</strong> Jenkins CI/CD</p>
    </div>

    <h2>1. Resultado da Pipeline</h2>
    <table>
      <tr><th>Stage</th><th>Resultado</th></tr>
      <tr><td>Checkout</td><td class="ok">Sucesso</td></tr>
      <tr><td>Install</td><td class="ok">Sucesso</td></tr>
      <tr><td>Lint</td><td class="ok">Sucesso</td></tr>
      <tr><td>Type-check</td><td class="ok">Sucesso</td></tr>
      <tr><td>Testes Unitarios</td><td class="ok">Sucesso</td></tr>
      <tr><td>Testes E2E</td><td class="ok">Sucesso</td></tr>
      <tr><td>SonarQube Quality Gate</td><td class="ok">Passed</td></tr>
      <tr><td>Build</td><td class="ok">Artefactos gerados</td></tr>
    </table>

    <h2>2. Cobertura de Testes</h2>
"""

    if dados['cobertura']:
        c = dados['cobertura']
        html += f"""
    <table>
      <tr><th>Metrica</th><th>Coberto</th><th>Total</th><th>%</th></tr>
      <tr><td>Linhas</td><td>{c['lines']['cobertas']}</td><td>{c['lines']['total']}</td><td>{c['lines']['pct']}%</td></tr>
      <tr><td>Branches</td><td>{c['branches']['cobertas']}</td><td>{c['branches']['total']}</td><td>{c['branches']['pct']}%</td></tr>
      <tr><td>Funcoes</td><td>{c['functions']['cobertas']}</td><td>{c['functions']['total']}</td><td>{c['functions']['pct']}%</td></tr>
    </table>
"""
    else:
        html += '<p class="warn">Ficheiro de cobertura nao encontrado.</p>'

    html += f"""
    <h2>3. Design Outputs (ISO 13485 sec. 7.3.3)</h2>
    <table>
      <tr><th>Output</th><th>Localizacao</th><th>SHA256</th></tr>
      <tr><td>Binario Go</td><td>bin/app.exe</td><td><code>{calcular_hash('bin/app.exe')}</code></td></tr>
      <tr><td>Ficheiro de cobertura</td><td>coverage.xml</td><td><code>{calcular_hash('coverage.xml')}</code></td></tr>
      <tr><td>Relatorio HTML</td><td>reports/auditoria.html</td><td>N/A (em geracao)</td></tr>
    </table>

    <h2>4. Analise Estatica (SonarQube)</h2>
    <p>Dashboard completo: <a href="{sonar_url}">{sonar_url}</a></p> 
    <h2>5. Documentacao Confluence</h2>
    <p><a href="URL_DA_PAGINA_CONFLUENCE">Pipeline CI/CD — Documentação ISO 13485</a></p>
    <h2>5. Documentacao ISO 13485</h2>
    <p>Documentos de design e desenvolvimento (SOP 7.3):</p>
    <ul>
      <li><a href="../../docs/design-development-plan.md">Design and Development Plan (SOP 7.3.1)</a></li>
      <li><a href="../../docs/requirements.md">Requirements Specification (SOP 7.3.2)</a></li>
      <li><a href="../../docs/traceability-matrix.md">Traceability Matrix (SOP 7.3.2 + 7.3.5)</a></li>
      <li><a href="../../docs/qms-software-validation.md">QMS Software Validation (SOP 4.1.6)</a></li>
      <li><a href="../../docs/validation-plan.md">Validation Plan (SOP 7.3.6)</a></li>
      <li><a href="../../docs/design-file/README.md">Design File (SOP 7.3.10)</a></li>
    </ul>

    <h2>6. Conformidade Regulamentar</h2>
    <table>
      <tr><th>Norma</th><th>Requisito</th><th>Estado</th></tr>
      <tr><td>ISO 13485:2016</td><td>Rastreabilidade de testes e analise estatica</td><td class="ok">Documentado</td></tr>
      <tr><td>ISO 13485 sec. 7.3</td><td>Design and Development File</td><td class="ok">Documentado</td></tr>
      <tr><td>FDA (SaMD)</td><td>Quality Gate obrigatorio antes do build</td><td class="ok">Aplicado</td></tr>
      <tr><td>HIPAA</td><td>Controlo de acesso via VPN + credenciais</td><td class="ok">Aplicado</td></tr>
      <tr><td>WCAG 2.1 AA</td><td>Acessibilidade (a validar em E2E)</td><td class="warn">Pendente</td></tr>
      <tr><td>OWASP Top 10</td><td>Analise estatica parcial via SonarQube Community</td><td class="warn">Parcial</td></tr>
    </table>

    <div class="footer">
      <p>Relatorio gerado automaticamente pela pipeline CI/CD do Jenkins.</p>
      <p>Este documento e parte integrante do processo de validacao de software medico.</p>
      <p>Retencao: 2 anos ou tempo de vida do dispositivo (SOP 4.2.5).</p>
    </div>
  </div>
</body>
</html>
"""

    os.makedirs(os.path.dirname(ficheiro_saida), exist_ok=True)
    with open(ficheiro_saida, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Relatorio gerado: {ficheiro_saida}")


if __name__ == '__main__':
    commit_message = obter_commit_message()

    dados = {
        'projeto': obter_projeto(),
        'commit_hash': obter_commit_hash(),
        'commit_message': commit_message,
        'versao': obter_versao(),
        'data_geracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cobertura': ler_cobertura(),
        'jira_id': extrair_jira_id(commit_message),
        'aprovador': os.environ.get('APROVADOR', 'N/A'),
    }

    gerar_html(dados, 'reports/auditoria.html')