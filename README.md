# performance-colaboradores-api
A função dessa API é receber notas de avaliações comportamentais e desafios enviados pelos colaboradores, calcular médias dessas avaliações e uma média final e salvar todos esses dados.

## Ideia de arquitetura inicial:
<img width="1365" height="747" alt="image" src="https://github.com/user-attachments/assets/ac7b61f1-8647-462f-a253-ad99fa42c6b5" />

  
---
  
## Ideia de arquitetura do banco de dados:
<img width="788" height="743" alt="db_performance_colaboradores_v2" src="https://github.com/user-attachments/assets/c6a68ad5-4179-43f8-b114-569edcee60d6" />


### Como funciona o banco de dados:
- Os colaboradores são armazenados na tabela tb_colaborador.
### "avaliacao_comportamental" e "avaliacao_comportamental_item":
A tabela "avaliacao_comportamental_item" ou "avaliacao_desafio_item" guarda cada uma das notas das respectivas avaliações. Exemplo:
```
"desafios": [
  {"numero_desafio": 1, "descricao": "Desafio A", "nota": 1},
  {"numero_desafio": 2, "descricao": "Desafio B", "nota": 1},
  {"numero_desafio": 3, "descricao": "Desafio C", "nota": 1},
  {"numero_desafio": 4, "descricao": "Desafio f", "nota": 2}
]

```
<img width="604" height="109" alt="image" src="https://github.com/user-attachments/assets/4e9f773b-f9b9-4bdb-846b-13c37a85f904" />
  
- avalicao_comportamental_id é uma chave estrangeira que referencia o ID da avaliação em questão, unindo todas as notas dos desafios em um grupo.
- Assim os dados ficam mais organizados e facilitados para consulta.
<img width="392" height="80" alt="image" src="https://github.com/user-attachments/assets/d4bdac7b-d102-4ba0-a8ce-03aec65d4a09" />




--- 

## payload para cadastrar dados
```
POST /avaliacoes
{
  "colaborador_id": 123,
  "data_avaliacao": "2025-10-24",
  "comportamental": [
    {"numero_questao": 1, "descricao": "Você promove um ambiente colaborativo?", "nota": 5},
    {"numero_questao": 2, "descricao": "Você se atualiza e aprende o tempo todo?", "nota": 4},
    {"numero_questao": 3, "descricao": "Você utiliza dados para tomar suas decisões?", "nota": 5},
    {"numero_questao": 4, "descricao": "Você trabalha com autonomia?", "nota": 4}
  ],
  "desafios": [
    {"numero_desafio": 1, "descricao": "Desafio A", "nota": 5},
    {"numero_desafio": 2, "descricao": "Desafio B", "nota": 4},
    {"numero_desafio": 3, "descricao": "Desafio C", "nota": 5}
  ]
}


```


