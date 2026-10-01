Design and Development Plan



Projeto: Go Backend Test

Norma: ISO 13485:2016 - SOP 7.3.1

Versão: 1.0

Autor: Joana Rego



&#x20;1. Objetivo

Este documento define o plano de design e desenvolvimento do projeto, incluindo etapas, responsabilidades, entradas e saídas de cada fase, conforme exigido pela ISO 13485:2016 secção 7.3.1.



2\. Ciclo de Vida

O ciclo de vida segue o modelo IEC 62304, adaptado para o âmbito deste projeto.

| Fase | Descrição | Responsável |

|------|-----------|-------------|

| 1. Planeamento | Definição de requisitos | Product Management |

| 2. Design | Arquitetura e especificação | R\&D |

| 3. Implementação | Codificação | R\&D |

| 4. Verificação | Testes unitários e análise estática | R\&D + QA |

| 5. Validação | Testes E2E e aceitação | QA |

| 6. Release | Tag Git e publicação | R\&D |

| 7. Manutenção | Suporte pós-release | Technical Support |



3\. Etapas da Pipeline

| Stage | Ferramenta | Fase ISO |

|-------|------------|----------|

| Checkout | Git | Todas |

| Install | go mod download | Implementação |

| Lint | golangci-lint | Verificação |

| Type-check | go vet | Verificação |

| Testes Unitários | go test + go-bcov | Verificação |

| SonarQube | SonarQube Community | Verificação |

| Build | go build | Release |

| Relatório Auditoria | Python | Todas |



4\. Critérios de Entrada e Saída

| Fase | Entrada | Saída | Critério |

|------|---------|-------|----------|

| Implementação | Requisito aprovado | Código commitado | Git push |

| Verificação | Código commitado | Testes passados + Quality Gate | Cobertura >= 80%, 0 Issues |

| Release | Verificação passada | Binário + Tag Git | Quality Gate Passed |

| Manutenção | Report de bug | Bug fix | Novo ciclo |



5\. Responsabilidades

| Papel | Responsabilidade |

|-------|-----------------|

| R\&D | Implementação, testes unitários, correção de bugs |

| QA | Validação, testes E2E, revisão de Quality Gate |

| Product Management | Definição de requisitos, aprovação de release |

| Management Representative | Aprovação final|



6\. Ferramentas Utilizadas

| Ferramenta | Versão | Propósito |

|-----------|--------|-----------|

| Go | 1.27 | Linguagem |

| Jenkins | LTS | Orquestração CI/CD |

| SonarQube | Community 13.7 | Análise estática |

| git | 2.55 | Controlo de versões |

| go-bcov | 1.0.4 | Cobertura de testes |



7\. Gestão de Interfaces

| Interface | Responsável | Como |

|-----------|-------------|------|

| R\&D <-> QA | Ambos | Pull Requests + Jenkins |

| QA <-> Product | QA lead | Management Review |

| Product <-> Cliente | Sales | Jira |



8\. Atualização do Plano

Este plano é revisto no início de cada nova feature, após cada release major, ou quando há mudanças significativas no QMS.



9\. Referências

ISO 13485:2016, secção 7.3.1

Quality Manual GlobeStar v01.47

