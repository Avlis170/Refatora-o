from codigo_refatorado import process_order

def test_process_order_vip_with_promo():
    customer = {"name": "Maria", "type": "vip"}
    items = [
        {"name": "Notebook", "price": 1000.0, "qty": 1, "weight": 2.0},
        {"name": "Mouse", "price": 50.0, "qty": 1, "weight": 0.5},
    ]
    result = process_order(customer, items, coupon="PROMO10", state="MG", express=False)

    assert result["customer"] == "Maria"
    assert result["subtotal"] == 1050.0
    assert result["discount"] == 262.5  # Limite de 25% aplicado
    assert result["shipping"] == 0.0  # Frete grátis (subtotal >= 500 e não express)
    assert result["tax"] == 55.12  # (1050 - 262.5) * 0.07 = 55.125 -> round 55.12
    assert result["total"] == 842.62
    assert result["points"] == 168  # vip div por 5


def test_process_order_duplicate_products():
    customer = {"name": "João", "type": "regular"}
    items = [
        {"name": "Caneta", "price": 10.0, "qty": 1, "weight": 0.1},
        {"name": "Caneta", "price": 10.0, "qty": 2, "weight": 0.1},
    ]
    result = process_order(customer, items, state="SP")

    assert result["duplicate_products"] == ["Caneta"]
