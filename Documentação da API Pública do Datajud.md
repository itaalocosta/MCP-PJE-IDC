# Documentação da API Pública do Datajud

## Endpoints

A API Pública do Datajud oferece várias rotas para pesquisa de informações processuais devido à natureza e organização do Judiciário brasileiro.

A URL principal de acesso é a URL `https://api-publica.datajud.cnj.jus.br/` e deverá ser seguida de um alias correspondente ao Tribunal que deseja obter os dados processuais.

**Exemplo:**
O endpoint do Tribunal Regional Federal da 1ª Região é `https://api-publica.datajud.cnj.jus.br/api_publica_trf1/`.

### Relação de tribunais/aliases para pesquisa processual:

#### Tribunais Superiores

| Tribunal | URL |
|---|---|
| Tribunal Superior do Trabalho | `tst` |
| Superior Tribunal de Justiça | `stj` |
| Supremo Tribunal Federal | `stf` |
| Tribunal Superior Eleitoral | `tse` |
| Superior Tribunal Militar | `stm` |

#### Justiça Federal

| Tribunal | URL |
|---|---|
| Tribunal Regional Federal da 1ª Região | `trf1` |
| Tribunal Regional Federal da 2ª Região | `trf2` |
| Tribunal Regional Federal da 3ª Região | `trf3` |
| Tribunal Regional Federal da 4ª Região | `trf4` |
| Tribunal Regional Federal da 5ª Região | `trf5` |
| Tribunal Regional Federal da 6ª Região | `trf6` |

#### Justiça Estadual

| Tribunal | URL |
|---|---|
| Tribunal de Justiça do Acre | `tjac` |
| Tribunal de Justiça de Alagoas | `tjal` |
| Tribunal de Justiça do Amapá | `tjap` |
| Tribunal de Justiça do Amazonas | `tjam` |
| Tribunal de Justiça da Bahia | `tjba` |
| Tribunal de Justiça do Ceará | `tjce` |
| Tribunal de Justiça do Distrito Federal e dos Territórios | `tjdft` |
| Tribunal de Justiça do Espírito Santo | `tjes` |
| Tribunal de Justiça de Goiás | `tjgo` |
| Tribunal de Justiça do Maranhão | `tjma` |
| Tribunal de Justiça de Minas Gerais | `tjmg` |
| Tribunal de Justiça de Mato Grosso do Sul | `tjms` |
| Tribunal de Justiça de Mato Grosso | `tjmt` |
| Tribunal de Justiça do Pará | `tjpa` |
| Tribunal de Justiça da Paraíba | `tjpb` |
| Tribunal de Justiça do Paraná | `tjpr` |
| Tribunal de Justiça de Pernambuco | `tjpe` |
| Tribunal de Justiça do Piauí | `tjpi` |
| Tribunal de Justiça do Rio de Janeiro | `tjrj` |
| Tribunal de Justiça do Rio Grande do Norte | `tjrn` |
| Tribunal de Justiça do Rio Grande do Sul | `tjrs` |
| Tribunal de Justiça de Rondônia | `tjro` |
| Tribunal de Justiça de Roraima | `tjrr` |
| Tribunal de Justiça de Santa Catarina | `tjsc` |
| Tribunal de Justiça de São Paulo | `tjsp` |
| Tribunal de Justiça de Sergipe | `tjse` |
| Tribunal de Justiça do Tocantins | `tjto` |

#### Justiça do Trabalho

| Tribunal | URL |
|---|---|
| Tribunal Regional do Trabalho da 1ª Região | `trt1` |
| Tribunal Regional do Trabalho da 2ª Região | `trt2` |
| Tribunal Regional do Trabalho da 3ª Região | `trt3` |
| Tribunal Regional do Trabalho da 4ª Região | `trt4` |
| Tribunal Regional do Trabalho da 5ª Região | `trt5` |
| Tribunal Regional do Trabalho da 6ª Região | `trt6` |
| Tribunal Regional do Trabalho da 7ª Região | `trt7` |
| Tribunal Regional do Trabalho da 8ª Região | `trt8` |
| Tribunal Regional do Trabalho da 9ª Região | `trt9` |
| Tribunal Regional do Trabalho da 10ª Região | `trt10` |
| Tribunal Regional do Trabalho da 11ª Região | `trt11` |
| Tribunal Regional do Trabalho da 12ª Região | `trt12` |
| Tribunal Regional do Trabalho da 13ª Região | `trt13` |
| Tribunal Regional do Trabalho da 14ª Região | `trt14` |
| Tribunal Regional do Trabalho da 15ª Região | `trt15` |
| Tribunal Regional do Trabalho da 16ª Região | `trt16` |
| Tribunal Regional do Trabalho da 17ª Região | `trt17` |
| Tribunal Regional do Trabalho da 18ª Região | `trt18` |
| Tribunal Regional do Trabalho da 19ª Região | `trt19` |
| Tribunal Regional do Trabalho da 20ª Região | `trt20` |
| Tribunal Regional do Trabalho da 21ª Região | `trt21` |
| Tribunal Regional do Trabalho da 22ª Região | `trt22` |
| Tribunal Regional do Trabalho da 23ª Região | `trt23` |
| Tribunal Regional do Trabalho da 24ª Região | `trt24` |

#### Justiça Eleitoral

| Tribunal | URL |
|---|---|
| Tribunal Regional Eleitoral do Acre | `treac` |
| Tribunal Regional Eleitoral de Alagoas | `treal` |
| Tribunal Regional Eleitoral do Amapá | `treap` |
| Tribunal Regional Eleitoral do Amazonas | `tream` |
| Tribunal Regional Eleitoral da Bahia | `treba` |
| Tribunal Regional Eleitoral do Ceará | `trece` |
| Tribunal Regional Eleitoral do Distrito Federal | `tredf` |
| Tribunal Regional Eleitoral do Espírito Santo | `trees` |
| Tribunal Regional Eleitoral de Goiás | `trego` |
| Tribunal Regional Eleitoral do Maranhão | `trema` |
| Tribunal Regional Eleitoral de Minas Gerais | `tremg` |
| Tribunal Regional Eleitoral de Mato Grosso do Sul | `trems` |
| Tribunal Regional Eleitoral de Mato Grosso | `tremt` |
| Tribunal Regional Eleitoral do Pará | `trepa` |
| Tribunal Regional Eleitoral da Paraíba | `trepb` |
| Tribunal Regional Eleitoral do Paraná | `trepr` |
| Tribunal Regional Eleitoral de Pernambuco | `trepe` |
| Tribunal Regional Eleitoral do Piauí | `trepi` |
| Tribunal Regional Eleitoral do Rio de Janeiro | `trerj` |
| Tribunal Regional Eleitoral do Rio Grande do Norte | `trern` |
| Tribunal Regional Eleitoral do Rio Grande do Sul | `trers` |
| Tribunal Regional Eleitoral de Rondônia | `trero` |
| Tribunal Regional Eleitoral de Roraima | `trerr` |
| Tribunal Regional Eleitoral de Santa Catarina | `tresc` |
| Tribunal Regional Eleitoral de São Paulo | `tresp` |
| Tribunal Regional Eleitoral de Sergipe | `trese` |
| Tribunal Regional Eleitoral do Tocantins | `treto` |

#### Justiça Militar

| Tribunal | URL |
|---|---|
| Tribunal de Justiça Militar de Minas Gerais | `tjmmg` |
| Tribunal de Justiça Militar do Rio Grande do Sul | `tjmrs` |
| Tribunal de Justiça Militar de São Paulo | `tjmsp` |


