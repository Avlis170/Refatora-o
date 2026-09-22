# METRICS.md

| Indicador | Antes | Depois |
| :--- | :--- | :--- |
| Testes passando | 0 | |
| Cobertura de testes | 0% | |
| Complexidade da função principal | 18 | |
| Complexidade média | 18.00 | |
| Índice de manutenibilidade | 41.28 (A) | |
| Problemas identificados pelo Ruff | 14 | |
| Quantidade de testes | 0 | |

## DIAGNÓSTICO INICIAL

1. **A função `process_order` possui excesso de responsabilidades:** Agrupa num único bloco de código múltiplos domínios de negócio (cálculo de subtotal, regras de descontos de cliente, validação e aplicação de cupons, cálculo de frete regional e peso, impostos estaduais, geração de pontos de fidelidade e identificação de produtos duplicados).
2. **Existência de duplicação de código e cálculo redundante:** O subtotal do pedido é calculado duas vezes em laços `for` separados (`total1` e `subtotal`).
3. **Variável morta no código:** A variável `total1` é processada no início da função, mas nunca é utilizada em nenhuma etapa posterior do fluxo.
4. **Algoritmo de deteção de duplicados ineficiente:** Utiliza uma verificação com dois laços aninhados ($O(N^2)$) e `range(len())` para encontrar itens repetidos, impactando o desempenho desnecessariamente.
5. **Elevado acoplamento e valores "hardcoded":** Regras fixas de negócio (como alíquotas de impostos por estado, taxas de frete e tipos de clientes) estão declaradas diretamente dentro de estruturas `if/elif/else`, dificultando a manutenção e a reutilização.
6. **Avisos de linter e maus hábitos de sintaxe:** Presença de comparações booleanas redundantes (como `express == False` e `express == True`) e concatenações manuais de strings em vez do uso de *f-strings*.
7. **Ausência de tipagem e testes unitários:** O código não possui anotações de tipos (*type hints*) nem qualquer suíte de testes automatizados para garantir a estabilidade e a prevenção de regressões durante alterações.
