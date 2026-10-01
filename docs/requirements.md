Requirements Specification



Projeto: Go Backend Test

Norma: ISO 13485:2016 - SOP 7.3.2

Versão: 1.0



1\. Requisitos Funcionais

| ID | Requisito | Prioridade | Estado |

|----|-----------|-----------|--------|

| REQ-001 | A função Soma(a, b int) int devolve a soma de dois inteiros | Alta | Implementado |

| REQ-002 | A função Subtrai(a, b int) int devolve a diferença de dois inteiros | Alta | Implementado |

| REQ-003 | O main() imprime os resultados no stdout | Alta | Implementado |



2\. Requisitos Não Funcionais

| ID | Requisito | Métrica | Estado |

|----|-----------|---------|--------|

| NFR-001 | Cobertura de testes >= 80% | SonarQube | 100% |

| NFR-002 | Quality Gate Passed | SonarQube | OK |

| NFR-003 | 0 Issues | SonarQube | OK |

| NFR-004 | 0 Vulnerabilities | SonarQube | OK |

| NFR-005 | Tempo de pipeline < 5 min | Jenkins | \~1.5 min |

| NFR-006 | Lint sem erros | golangci-lint | 0 issues |



3\. Requisitos Regulamentares

| ID | Requisito | Norma | Estado |

|----|-----------|-------|--------|

| REG-001 | Rastreabilidade de testes | ISO 13485 sec. 7.3.5 | OK |

| REG-002 | Quality Gate obrigatório | FDA (SaMD) | OK |

| REG-003 | Registos de auditoria | ISO 13485 sec. 4.2.5 | OK |

| REG-004 | Controlo de versões | ISO 13485 sec. 4.2.4 | OK |

| REG-005 | Análise estática | OWASP Top 10 | Parcial |



4\. Requisitos de Segurança

| ID | Requisito | Categoria OWASP | Estado |

|----|-----------|----------------|--------|

| SEC-001 | Sem injeções | A03 | Community não deteta |

| SEC-002 | Sem credenciais hardcoded | A02 | OK |

| SEC-003 | Dependências atualizadas | A06 | Não verificado |



5\. Fora do Âmbito

Interface gráfica, persistência de dados, comunicação em rede, autenticação de utilizadores.



6\. Referências

ISO 13485:2016 sec. 7.3.2

Quality Manual GlobeStar v01.47

OWASP Top 10 (2021)

