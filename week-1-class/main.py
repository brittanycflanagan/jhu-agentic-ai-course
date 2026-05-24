from seed_data import inventory, orders, recipes, restock, status


def load_recipes():
    return recipes


def load_inventory():
    return inventory


def load_orders():
    return orders


def load_restock():
    return restock


def load_status():
    return status


def print_recipes(recipe_data):
    print("\nRecipes")
    print("-" * 80)
    for recipe in recipe_data:
        print(f"Recipe ID: {recipe['recipe_id']}")
        print(f"Name: {recipe['name']}")
        print("Ingredients:")
        for ingredient in recipe["ingredients"]:
            print(f"  - {ingredient['name']}: {ingredient['qty_grams']}g")
        print()


def print_inventory(inventory_data):
    print("\nInventory")
    print("-" * 80)
    for item in inventory_data:
        print(
            f"{item['ingredient']}: "
            f"{item['qty_grams']}g, "
            f"expires {item['expiry_date']}"
        )


def print_orders(order_data):
    print("\nOrders")
    print("-" * 80)
    for order in order_data:
        print(f"Order ID: {order['order_id']}")
        print(f"Brand: {order['brand']}")
        print("Items:")
        for item in order["items"]:
            print(f"  - {item['item']}: qty {item['qty']}")
        print()


def print_restock(restock_data):
    print("\nRestock")
    print("-" * 80)
    for item in restock_data:
        print(
            f"{item['item']}: "
            f"{item['qty_needed_grams']}g needed "
            f"({item['reason']})"
        )


def print_status(status_data):
    print("\nStatus")
    print("-" * 80)
    for record in status_data:
        delivery_status = "Delivered" if record["delivered"] else "Not Delivered"
        print(
            f"Order ID {record['order_id']}: "
            f"{delivery_status} - {record['remark']}"
        )


def find_recipe(recipe_name, recipe_data):
    for recipe in recipe_data:
        if recipe["name"] == recipe_name:
            return recipe
    return None


def build_inventory_lookup(inventory_data):
    inventory_lookup = {}
    for item in inventory_data:
        inventory_lookup[item["ingredient"]] = item
    return inventory_lookup


def calculate_required_ingredients(order, recipe_data):
    required_ingredients = {}

    for ordered_item in order["items"]:
        recipe = find_recipe(ordered_item["item"], recipe_data)

        if recipe is None:
            print(f"  Recipe not found for {ordered_item['item']}")
            continue

        order_quantity = ordered_item["qty"]
        for ingredient in recipe["ingredients"]:
            ingredient_name = ingredient["name"]
            total_grams = ingredient["qty_grams"] * order_quantity
            required_ingredients[ingredient_name] = (
                required_ingredients.get(ingredient_name, 0) + total_grams
            )

    return required_ingredients


def check_inventory_availability(required_ingredients, inventory_data):
    inventory_lookup = build_inventory_lookup(inventory_data)
    missing_ingredients = {}

    for ingredient_name, required_qty in required_ingredients.items():
        inventory_item = inventory_lookup.get(ingredient_name)
        available_qty = 0 if inventory_item is None else inventory_item["qty_grams"]

        if available_qty < required_qty:
            missing_ingredients[ingredient_name] = {
                "required_qty": required_qty,
                "available_qty": available_qty,
                "short_by": required_qty - available_qty,
            }

    return missing_ingredients


def print_required_ingredients(required_ingredients):
    print("Required Ingredients:")
    for ingredient_name, required_qty in required_ingredients.items():
        print(f"  - {ingredient_name}: {required_qty}g")


def print_inventory_check(missing_ingredients):
    if not missing_ingredients:
        print("Inventory Check: all required ingredients are available.")
        return

    print("Inventory Check: missing or insufficient ingredients found.")
    for ingredient_name, details in missing_ingredients.items():
        print(
            f"  - {ingredient_name}: "
            f"required {details['required_qty']}g, "
            f"available {details['available_qty']}g, "
            f"short by {details['short_by']}g"
        )


def process_orders(order_data, recipe_data, inventory_data):
    print("\nOrder Processing")
    print("-" * 80)

    for order in order_data:
        print(f"\nOrder ID: {order['order_id']}")
        print(f"Brand: {order['brand']}")

        required_ingredients = calculate_required_ingredients(order, recipe_data)
        missing_ingredients = check_inventory_availability(
            required_ingredients,
            inventory_data,
        )

        print_required_ingredients(required_ingredients)
        print_inventory_check(missing_ingredients)


def main():
    recipe_data = load_recipes()
    inventory_data = load_inventory()
    order_data = load_orders()
    restock_data = load_restock()
    status_data = load_status()

    print_recipes(recipe_data)
    print_inventory(inventory_data)
    print_orders(order_data)
    print_restock(restock_data)
    print_status(status_data)
    process_orders(order_data, recipe_data, inventory_data)


if __name__ == "__main__":
    main()
