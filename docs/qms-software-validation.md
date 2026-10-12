QMS Software Validation



Standard: ISO 13485:2016 — SOP 4.1.6

Responsible: Joana Rego



1\. Validated Software

| Software | Version | Purpose | Validation |

| Jenkins | LTS | CI/CD orchestration | Tested on every build |

| SonarQube Community | 26.9 | Static analysis | Quality Gate configured |

| SonarScanner CLI | 8.1.0.6389 | Scanner | Tested locally |

| Git | 2.55 | Version control | Used in production |

| Go | 1.27 | Language | Unit tests |

| go-bcov | 1.0.4 | Coverage conversion | Tested locally |

| Python | 3.14 | Report scripts | Manual validation |



2\. Integrity

| Software | Integrity check |

| Jenkins | Authentication via credentials |

| SonarQube | Token read from local file |

| Git | HTTPS + token |

| Go | go.sum verifies dependencies |



3\. Risks

| Risk | Mitigation |

| SonarQube Community does not detect injections | Complementary tools |

| Scanner 6.x has known bug | Use scanner 8.1.0 |

| Outdated dependencies | Periodic review |



4\. References

\- ISO 13485:2016 sec. 4.1.6

\- Quality Manual GlobeStar v01.47

