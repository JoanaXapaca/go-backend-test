Traceability Matrix



Projeto: Go Backend Test

Norma: ISO 13485:2016 — SOP 7.3.2 + 7.3.5



Matriz Requisito -> Teste

| Requisito | Descrição | Teste | Ficheiro | Estado |

|-----------|-----------|-------|----------|--------|

| REQ-001 | Soma de inteiros | TestSoma | main\_test.go | OK |

| REQ-001 | Edge cases soma | TestSomaEdgeCases | main\_test.go | OK |

| REQ-002 | Subtração de inteiros | TestSubtrai | main\_test.go | OK |

| REQ-002 | Edge cases subtração | TestSubtraiEdgeCases | main\_test.go | OK |

| REQ-003 | Execução do main | TestMain | main\_test.go | OK |

| NFR-001 | Cobertura >= 80% | go test -coverprofile | Pipeline | 100% |

| NFR-002 | Quality Gate | SonarQube | Pipeline | OK |

| REG-001 | Rastreabilidade | Relatório HTML | gerar\_relatorio.py | OK |

| REG-003 | Registos de auditoria | archiveArtifacts | Jenkinsfile | OK |





Referências

ISO 13485:2016 sec. 7.3.2 (Inputs) e sec. 7.3.5 (Verification)

Quality Manual GlobeStar v01.47

