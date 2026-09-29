# Projeto de Refatoração do Checkout Legado

1. **A função `process_order` possui excesso de responsabilidades:** Agrupa num único bloco de código múltiplos domínios de negócio (cálculo de subtotal, regras de descontos, validação de cupons, cálculo de frete regional e peso, impostos estaduais, pontos de fidelidade e identificação de produtos duplicados).
2. **Duplicação de código:** O subtotal do pedido é calculado duas vezes em laços `for` separados (`total1` e `subtotal`).
3. **Variável morta:** A variável `total1` é processada, mas nunca utilizada.
4. **Algoritmo ineficiente de duplicados:** Utiliza dois laços aninhados ($O(N^2)$) para encontrar itens repetidos.
5. **Elevado acoplamento e valores "hardcoded":** Regras fixas de negócio (impostos por estado, taxas de frete) declaradas diretamente em blocos `if/elif/else`.
6. **Avisos de linter e sintaxe inadequada:** Comparações booleanas redundantes (`express == False`) e falta de formatação moderna.
7. **Ausência de testes automatizados:** Nenhuma cobertura de testes unitários para prevenção de regressões.

---

## JUSTIFICATIVA DAS DECISÕES DE REFATORAÇÃO

### 1. Aplicação do Padrão "Extract Function" e Separação de Responsabilidades
* **PROBLEMA ENCONTRADO:** A função `process_order` realizava todas as operações de validação, cálculo e formatação em um único bloco monolítico, tornando a leitura complexa (complexidade ciclomática = 18).
* **ALTERAÇÃO REALIZADA:** Extração de funções especializadas e com responsabilidade única: `calculate_subtotal`, `calculate_discount`, `calculate_shipping`, `calculate_tax`, `calculate_loyalty_points` e `find_duplicate_products`.
* **JUSTIFICATIVA:** A separação isola os domínios de negócio, permitindo testar cada cálculo individualmente, reduzindo a complexidade da função principal para 3 e facilitando reusabilidade e manutenção futura.

---

### 2. Eliminação de Código Duplicado e Variáveis Inúteis
* **PROBLEMA ENCONTRADO:** O cálculo do subtotal era executado duas vezes seguidas através de laços `for` redundantes, armazenando o primeiro resultado em uma variável não utilizada (`total1`).
* **ALTERAÇÃO REALIZADA:** Remoção da variável `total1` e do primeiro laço `for`, concentrando toda a lógica de subtotal na função especialista `calculate_subtotal`.
* **JUSTIFICATIVA:** Elimina desperdício de processamento, simplifica o fluxo de execução e remove código morto que causava confusão na leitura.

---

### 3. Remoção de "Magic Numbers" e Uso de Mapeamentos (Replace Conditional with Mapping)
* **PROBLEMA ENCONTRADO:** Alíquotas de imposto estaduais e multiplicadores de frete expresso estavam inseridos diretamente em estruturas `if/elif/else` extensas e sem contextualização.
* **ALTERAÇÃO REALIZADA:** Criação de constantes explicativas (`EXPRESS_SHIPPING_MULTIPLIER = 1.8`, `FREE_SHIPPING_THRESHOLD = 500.0`) e substituição das condicionais de imposto pelo dicionário `TAX_RATES`.
* **JUSTIFICATIVA:** Torna o código autodocumentado, elimina números mágicos espalhados e permite atualizar alíquotas ou estados sem a necessidade de modificar estruturas condicionais complexas.

---

### 4. Otimização do Algoritmo de Produtos Duplicados
* **PROBLEMA ENCONTRADO:** A busca por produtos duplicados utilizava um laço duplo ($O(N^2)$) sobre a lista de itens.
* **ALTERAÇÃO REALIZADA:** Reescrita do algoritmo utilizando a estrutura de dados `set` para rastrear itens vistos em uma única passagem ($O(N)$).
* **JUSTIFICATIVA:** Melhora significativamente a eficiência de execução e reduz a complexidade algorítmica de processamento do carrinho.

---

### 5. Criação de Suíte de Testes Automatizados com Pytest
* **PROBLEMA ENCONTRADO:** O projeto possuía 0% de cobertura de testes, tornando qualquer alteração propensa a regressões e falhas não detectadas.
* **ALTERAÇÃO REALIZADA:** Implementação de 7 testes unitários cobrindo cenários com diferentes tipos de clientes (regular, VIP, funcionário), cupons de desconto, taxas de frete por estado/expresso e detecção de duplicados.
* **JUSTIFICATIVA:** Garante a estabilidade do sistema, atinge 99% de cobertura de código e assegura que as regras de negócio permaneçam intactas após as refatorações.


---

## USO DE INTELIGÊNCIA ARTIFICIAL

**Ferramenta utilizada:**
Gemini

**Finalidade:**
Apoio na identificação de maus cheiros de código (*code smells*), auxílio na estruturação das funções refatoradas, apoio na elaboração dos cenários de testes unitários com Pytest e formatação dos relatórios de métricas em Markdown.

**Exemplo de sugestão recebida:**
Substituição do algoritmo de verificação de produtos duplicados de um laço duplo $O(N^2)$ por um algoritmo com estrutura de dados `set` com complexidade $O(N)$.

**A sugestão foi aceita, modificada ou rejeitada?**
Aceita e modificada. A sugestão do algoritmo foi adotada e ajustada para retornar uma lista com os nomes únicos dos produtos duplicados, respeitando a estrutura de resposta esperada pelo código legado.

**Como a equipe validou a solução?**
A solução foi validada localmente através da execução da suíte de testes unitários no `pytest` (alcançando 99% de cobertura), além da verificação de métricas com `radon` (complexidade e manutenibilidade) e análise estática com `ruff` (zero avisos).
