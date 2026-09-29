MAX_DISCOUNT_PERCENTAGE = 0.25
EXPRESS_SHIPPING_MULTIPLIER = 1.8
FREE_SHIPPING_THRESHOLD = 500.0

SOUTHEAST_STATES = {"MG", "SP", "RJ", "ES"}

TAX_RATES = {
    "MG": 0.07,
    "ES": 0.07,
    "RJ": 0.08,
    "SP": 0.09,
}
DEFAULT_TAX_RATE = 0.12

ORDERS_PROCESSED = []


# Extract Function: Funções Especializadas
def calculate_subtotal(items):
    subtotal = 0.0
    for item in items:
        qty = item.get("qty", 1)
        if qty <= 0:
            raise ValueError("A quantidade do item deve ser maior que zero.")
        subtotal += item.get("price", 0.0) * qty
    return subtotal


def calculate_discount(customer, subtotal, coupon):
    """Calcula o desconto por tipo de cliente e cupom, respeitando o limite máximo."""
    discount = 0
    customer_type = customer.get("type", "")

    # Desconto por tipo de cliente
    if customer_type == "vip":
        discount = subtotal * 0.15 if subtotal >= 1000 else subtotal * 0.10
    elif customer_type == "employee":
        discount = subtotal * 0.20
    elif customer_type == "regular" and subtotal >= 800:
        discount = subtotal * 0.05

    # Aplicação de cupons
    if coupon == "PROMO10":
        discount += subtotal * 0.10
    elif coupon == "PROMO20" and subtotal >= 500:
        discount += subtotal * 0.20
    elif coupon == "VIP50" and customer_type == "vip":
        discount += 50

    # Aplicação do limite máximo de desconto
    max_discount = subtotal * MAX_DISCOUNT_PERCENTAGE
    return min(discount, max_discount)


def calculate_shipping(subtotal, items, state, express):
    """Calcula o valor do frete com base no peso, região e tipo de envio."""
    if subtotal >= FREE_SHIPPING_THRESHOLD and not express:
        return 0

    total_weight = sum(item.get("weight", 0) * item["qty"] for item in items)

    # Simplify Conditional
    if state in SOUTHEAST_STATES:
        shipping = 20 + total_weight * 0.4
    else:
        shipping = 35 + total_weight * 0.6

    if express:
        shipping *= EXPRESS_SHIPPING_MULTIPLIER

    return shipping


def calculate_tax(discounted_value, state):
    """Calcula a taxa de imposto com base no estado de destino (Replace Conditional with Mapping)."""
    # Rename Variable (taxa -> tax_rate)
    tax_rate = TAX_RATES.get(state, DEFAULT_TAX_RATE)
    return discounted_value * tax_rate


def calculate_loyalty_points(customer, total_amount):
    """Calcula os pontos de fidelidade do cliente."""
    if customer.get("type") == "vip":
        return int(total_amount / 5)
    return int(total_amount / 10)


def find_duplicate_products(items):
    """Identifica produtos com nomes duplicados de forma eficiente em O(N)."""
    seen = set()
    duplicates = []
    for item in items:
        name = item["name"]
        if name in seen and name not in duplicates:
            duplicates.append(name)
        seen.add(name)
    return duplicates


# Separate Responsibilities: Função Principal apenas coordena o fluxo
def process_order(customer, items, coupon="", state="MG", express=False):
    # Remove Duplicate Code & Remove Unused Variable (removido total1 e cálculo duplicado)
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(customer, subtotal, coupon)
    discounted_value = subtotal - discount

    shipping = calculate_shipping(subtotal, items, state, express)
    tax = calculate_tax(discounted_value, state)

    order_total = discounted_value + shipping + tax
    points = calculate_loyalty_points(customer, order_total)
    duplicates = find_duplicate_products(items)

    total_final = round(order_total, 2)

    resultado = {
        "customer": customer["name"],
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "shipping": round(shipping, 2),
        "tax": round(tax, 2),
        "total": total_final,
        "points": points,
        "duplicate_products": duplicates,
    }

    ORDERS_PROCESSED.append(resultado)

    print(f"Pedido processado para {customer['name']}")
    print(f"Subtotal: {subtotal}")
    print(f"Desconto: {discount}")
    print(f"Frete: {shipping}")
    print(f"Imposto: {tax}")
    print(f"TOTAL: {total_final}")

    return resultado
