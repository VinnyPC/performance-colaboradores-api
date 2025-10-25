# performance-colaboradores-api
A função dessa API é receber notas de avaliações comportamentais e desafios enviados pelos colaboradores, calcular médias dessas avaliações e uma média final e salvar todos esses dados.

## Ideia de arquitetura inicial:
<img width="1365" height="747" alt="image" src="https://github.com/user-attachments/assets/ac7b61f1-8647-462f-a253-ad99fa42c6b5" />

  
---
  
## Ideia de arquitetura do banco de dados:
<img width="736" height="873" alt="db_performance_colaboradores" src="https://github.com/user-attachments/assets/3415e9f8-be36-45e8-8170-c9d9e7c24f75" />

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


