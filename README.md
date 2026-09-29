# REFactor Race Python

## EQUIPE
- Integrante 1
- Integrante 2
- Integrante 3

## DESCRIÇÃO
Projeto de refatoração do sistema de processamento de checkout de pedidos. O objetivo principal foi transformar um código legado monolítico e de difícil manutenção em uma arquitetura limpa, modular, otimizada e coberta por testes unitários sem alterar o comportamento esperado de negócio.

## DIAGNÓSTICO INICIAL
Antes da refatoração, o sistema apresentava:
- Função monolítica ("God Function") acumulando múltiplas responsabilidades de negócio.
- Complexidade ciclomática elevada e baixo índice de manutenibilidade.
- Algoritmo ineficiente de busca de produtos duplicados $O(N^2)$.
- Ausência total de testes unitários automatizados para garantir regressões.
- Falta de tipagem estática e presencia de variáveis mortas/não utilizadas.

## CODE SMELLS ENCONTRADOS
- **Long Method / Large Class:** A função principal gerenciava regras de cupom, frete, impostos, fidelidade e duplicatas em um único bloco.
- **Duplicate Code:** Lógicas de acréscimo de taxas e descontos repetidas em vários pontos.
- **Dead Code:** Variável `total1` declarada no código sem qualquer leitura ou utilidade no retorno.
- **Primitive Obsession:** Tipos de dados passados de forma genérica sem validações explícitas de entrada.
- **Algoritmo Ineficiente:** Laços aninhados executando comparações quadráticas para identificar duplicatas.

## REFATORAÇÕES REALIZADAS
- **Extração de Funções (Extract Method):** Divisão da lógica em funções especialistas (`calculate_subtotal`, `calculate_discount`, `calculate_tax`, `calculate_shipping`, `calculate_loyalty_points` e `find_duplicate_products`).
- **Otimização de Algoritmo:** Substituição dos laços aninhados $O(N^2)$ por verificação linear $O(N)$ utilizando a estrutura de dados `set`.
- **Eliminação de Dead Code:** Remoção da variável não utilizada `total1`.
- **Adição de Type Hints:** Tipagem estática em todas as funções para reforçar a segurança do código e suporte dos linters.

## TESTES ADICIONADOS
Suíte de testes desenvolvida com **Pytest** cobrindo os seguintes cenários:
1. `test_customer_regular_with_discount`: Desconto por atuar limite mínimo de valor.
2. `test_customer_vip_with_vip50_coupon`: Regra de cliente VIP acumulando cupom fixo.
3. `test_customer_employee_discount`: Aplicação de taxa de desconto fixa para funcionários.
4. `test_state_outside_southeast_and_express_shipping`: Cálculo de impostos fora do Sudeste e frete expresso.
5. `test_maximum_discount_limit`: Garantia do teto máximo de desconto permitido (25%).
6. `test_free_shipping_conditions`: Regra de isenção de frete vs frete expresso pago.
7. `test_duplicate_products_detection`: Identificação de itens duplicados no carrinho.
8. *Testes preparados para os Tickets 1 e 2 (quantidade inválida e cupons case-insensitive).*

## MÉTRICAS ANTES E DEPOIS
- **Complexidade Ciclomática (Radon):** Reduzida de nível crítico para **Classe A** em todas as funções.
- **Manutenibilidade (Maintainability Index):** Elevação para a pontuação máxima de **Classe A**.
- **Cobertura de Testes (Pytest-Cov):** Atingido o nível de **99% de cobertura de código**.
- **Análise Estática (Ruff):** Redução de múltiplos alertas de linter para **0 avisos**.

## DECISÕES TÉCNICAS
- **Manutenção da Assinatura:** A função pública `process_order` manteve seus parâmetros e estrutura de retorno idênticos para garantir compatibilidade retroativa.
- **Uso de Sets para Duplicatas:** Escolha da estrutura `set` para garantir complexidade de busca $O(1)$ por elemento.
- **Isolamento de Regras:** Modularização baseada no princípio da responsabilidade única (SRP), facilitando testes unitários isolados por regra de negócio.

## USO DE INTELIGÊNCIA ARTIFICIAL
- **Ferramenta utilizada:** Gemini
- **Finalidade:** Apoio na identificação de code smells, estruturação das funções especialistas, criação dos cenários de testes unitários no Pytest e formatação da documentação.
- **Exemplo de sugestão recebida:** Otimização da função de duplicatas para $O(N)$ com uso de conjuntos.
- **A sugestão foi aceita, modificada ou rejeitada?** Aceita e modificada para manter a estrutura exata do dicionário de retorno do código original.
- **Como a equipe validou a solução?** Validação local via execução do Pytest (99% de cobertura), análise estática com Ruff e medição de complexidade com Radon.

## MELHORIAS FUTURAS
- **Parametrização Externa de Regras:** Mover as alíquotas de impostos por estado e valores de cupons de desconto para arquivos de configuração (JSON/YAML) ou banco de dados.
- **Tratamento de Exceções Customizadas:** Criar classes de exceção específicas para erros de checkout (ex: `InvalidQuantityError`, `ExpiredCouponError`).
- **Aprimoramento do Ticket de Validação:** Ativar e integrar completamente as validações estritas de quantidade e formatação de cupom.
