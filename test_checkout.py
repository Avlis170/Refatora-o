from codigo_refatorado import process_order


# 1. Cliente Regular com desconto por atingir R$ 800
def test_customer_regular_with_discount():
    customer = {"name": "Carlos", "type": "regular"}
    items = [{"name": "Telemóvel", "price": 800.0, "qty": 1, "weight": 1.0}]
    result = process_order(customer, items, state="SP")

    assert result["subtotal"] == 800.0
    assert result["discount"] == 40.0  # 5% de desconto
    assert result["tax"] == 68.4  # (800 - 40) * 0.09
    assert result["points"] == 82  # Pontos calculados sobre o total final


# 2. Cliente VIP com cupom VIP50
def test_customer_vip_with_vip50_coupon():
    customer = {"name": "Ana", "type": "vip"}
    items = [{"name": "Monitor", "price": 400.0, "qty": 1, "weight": 3.0}]
    result = process_order(customer, items, coupon="VIP50", state="MG")

    assert result["subtotal"] == 400.0
    assert result["discount"] == 90.0  # 10% base (40) + 50 fixo
    assert result["tax"] == 21.7  # (400 - 90) * 0.07
    assert result["points"] == 70  # Pontos calculados sobre o total final


# 3. Funcionário (Employee) com desconto fixo de 20%
def test_customer_employee_discount():
    customer = {"name": "Lucas", "type": "employee"}
    items = [{"name": "Cadeira", "price": 300.0, "qty": 1, "weight": 5.0}]
    result = process_order(customer, items, state="RJ")

    assert result["subtotal"] == 300.0
    assert result["discount"] == 60.0
    assert result["tax"] == 19.2


# 4. Estado fora do Sudeste (Taxa Padrão e Frete Maior)
def test_state_outside_southeast_and_express_shipping():
    customer = {"name": "Beatriz", "type": "regular"}
    items = [{"name": "Teclado", "price": 100.0, "qty": 1, "weight": 2.0}]
    result = process_order(customer, items, state="BA", express=True)

    assert result["tax"] == 12.0
    assert result["shipping"] == 65.16


# 5. Validação do Limite Máximo de Desconto (Teto de 25%)
def test_maximum_discount_limit():
    customer = {"name": "Pedro", "type": "employee"}
    items = [{"name": "Mesa", "price": 1000.0, "qty": 1, "weight": 10.0}]
    result = process_order(customer, items, coupon="PROMO20", state="MG")

    assert result["discount"] == 250.0


# 6. Frete Grátis vs Frete Expresso Pago
def test_free_shipping_conditions():
    customer = {"name": "Sofia", "type": "regular"}
    items = [{"name": "Item Caro", "price": 600.0, "qty": 1, "weight": 1.0}]

    result_free = process_order(customer, items, express=False)
    assert result_free["shipping"] == 0.0

    result_express = process_order(customer, items, express=True)
    assert result_express["shipping"] > 0.0


# 7. Identificação de Produtos Duplicados na Lista
def test_duplicate_products_detection():
    customer = {"name": "Tiago", "type": "regular"}
    items = [
        {"name": "Rato", "price": 50.0, "qty": 1},
        {"name": "Rato", "price": 50.0, "qty": 1},
        {"name": "Tênis", "price": 200.0, "qty": 1},
    ]
    result = process_order(customer, items)

    assert result["duplicate_products"] == ["Rato"]
