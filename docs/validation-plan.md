Design Validation Plan



Projeto: Go Backend Test

Norma: ISO 13485:2016 - SOP 7.3.6



1\. Objetivo

Validar que o software cumpre os requisitos do utilizador em ambiente simulado. O ambiente clínico real está fora do âmbito.



2\. Ambiente de Validação

| Item | Descrição |

|------|-----------|

| Sistema operativo | Windows 11 |

| Runtime | Go 1.27 |

| Utilizador | Desenvolvedor / QA |

| Cenário | Execução do binário e verificação do output |



3\. Testes E2E

| ID | Teste | Cenário | Critério de Aceitação |

|----|-------|---------|----------------------|

| E2E-001 | Compilação | go build | Binário gerado sem erros |

| E2E-002 | Execução | ./app.exe | Output contém "Soma 2+3 = 5" |

| E2E-003 | Execução | ./app.exe | Output contém "Subtrai 10-4 = 6" |



4\. Limitações

A validação em ambiente clínico real não é aplicável a este projeto de teste de pipeline.

