from seed_data import recipes, inventory, orders, restock, status
import json
from datetime import date, datetime


def build_inventory_map(inventory_data):
    """Create a mapping of ingredient names to inventory records."""
    return {item["ingredient"]: item for item in inventory_data}


def build_inventory_qty_map(inventory_data):
    """Create a mapping of ingredient names to available quantity in grams."""
    return {item["ingredient"]: item["qty_grams"] for item in inventory_data}


def build_remaining_inventory_qty_map(original_qty_map, cumulative_used_map):
    """Compute current remaining quantities: original quantity - cumulative used."""
    remaining_qty_map = {}
    for ingredient_name, original_qty in original_qty_map.items():
        used_qty = cumulative_used_map.get(ingredient_name, 0)
        remaining_qty_map[ingredient_name] = max(original_qty - used_qty, 0)
    return remaining_qty_map


def find_recipe(recipe_name):
    """Find a recipe by name."""
    for recipe in recipes:
        if recipe["name"] == recipe_name:
            return recipe
    return None


def calculate_required_ingredients(order):
    """Calculate total ingredients required for an order."""
    required = {}
    for ordered_item in order["items"]:
        recipe = find_recipe(ordered_item["item"])
        if not recipe:
            continue
        qty_multiplier = ordered_item["qty"]
        for ingredient in recipe["ingredients"]:
            ingredient_name = ingredient["name"]
            required[ingredient_name] = required.get(ingredient_name, 0) + (
                ingredient["qty_grams"] * qty_multiplier
            )
    return required


def check_inventory(required, inventory_qty_map):
    """Check which ingredients are missing from inventory."""
    missing = {}
    for ingredient_name, qty_needed in required.items():
        available_qty = inventory_qty_map.get(ingredient_name, 0)
        if available_qty < qty_needed:
            missing[ingredient_name] = qty_needed - available_qty
    return missing


def get_or_create_status_record(order_id):
    """Get or create a status record for an order."""
    for record in status:
        if record["order_id"] == order_id:
            return record
    new_record = {"order_id": order_id, "delivered": False, "remark": "Not Delivered"}
    status.append(new_record)
    return new_record


def deduct_inventory(required, original_qty_map, cumulative_used_map):
    """Update cumulative used and return remaining quantities based on original stock."""
    remaining_quantities = {}
    for ingredient_name, qty_needed in required.items():
        if ingredient_name in original_qty_map:
            cumulative_used_map[ingredient_name] = cumulative_used_map.get(ingredient_name, 0) + qty_needed
            remaining_quantities[ingredient_name] = max(
                original_qty_map[ingredient_name] - cumulative_used_map[ingredient_name],
                0,
            )
    return remaining_quantities


def add_to_restock(missing_ingredients, remaining_inventory_qty_map):
    """Add missing ingredients to restock table with reason."""
    restock_map = {item["item"]: item for item in restock}

    for ingredient_name, qty_short in missing_ingredients.items():
        if ingredient_name in restock_map:
            existing = restock_map[ingredient_name]
            existing["qty_needed_grams"] = max(existing["qty_needed_grams"], qty_short)
            existing["reason"] = "Insufficient stock for order"
        else:
            restock.append({
                "item": ingredient_name,
                "qty_needed_grams": qty_short,
                "reason": "Insufficient stock for order",
            })


def is_expiring_soon(expiry_date_str, current_date):
    """Return True if expiry date is within the next 5 days (including day 5 and day 0)."""
    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
    days_to_expiry = (expiry_date - current_date).days
    return 0 <= days_to_expiry <= 5


def apply_inventory_health_restock_rules(inventory_data):
    """
    Update restock reasons based on final inventory:
    1) Expiring soon if today is within 5 days of expiry.
    2) Out of stock if final qty is 0 grams (qty needed 10000 grams).
    3) Running low on stock if final qty is <= 1000 grams (qty needed 10000 - qty).
    """
    current_date = date.today()
    filtered_restock = []
    inventory_health_reasons = {
        "Expiring soon in 5 days",
        "Out of stock",
        "Running low on stock",
    }
    for restock_item in restock:
        if restock_item.get("reason") in inventory_health_reasons:
            continue
        filtered_restock.append(restock_item)
    restock[:] = filtered_restock

    restock_map = {item["item"]: item for item in restock}

    for inventory_item in inventory_data:
        ingredient_name = inventory_item["ingredient"]
        qty_left = inventory_item["qty_grams"]
        expiry_date_str = inventory_item["expiry_date"]

        expiring_soon = is_expiring_soon(expiry_date_str, current_date)
        out_of_stock = qty_left == 0
        running_low = 0 < qty_left <= 1000

        if not expiring_soon and not out_of_stock and not running_low:
            continue

        if expiring_soon:
            reason = "Expiring soon"
            qty_needed = 10000
        elif out_of_stock:
            reason = "Out of stock"
            qty_needed = 10000
        else:
            reason = "Running low on stock"
            qty_needed = 10000 - qty_left

        if ingredient_name in restock_map:
            existing = restock_map[ingredient_name]
            existing["reason"] = reason
            existing["qty_needed_grams"] = max(existing["qty_needed_grams"], qty_needed)
        else:
            restock.append({
                "item": ingredient_name,
                "qty_needed_grams": qty_needed,
                "reason": reason,
            })


def process_order_step_by_step(order, original_qty_map, cumulative_used_map):
    """Process order following the workflow steps."""
    order_id = order["order_id"]
    brand = order["brand"]
    
    print(f"\n{'=' * 80}")
    print(f"PROCESSING ORDER #{order_id}")
    print(f"{'=' * 80}")
    
    # STEP 1: Take order from Orders table
    print(f"\nSTEP 1: TAKE ORDER FROM ORDERS TABLE")
    print(f"{'─' * 80}")
    print(f"Order ID: {order_id}")
    print(f"Brand: {brand}")
    print(f"Items Ordered:")
    for item in order["items"]:
        print(f"  • {item['item']} (Qty: {item['qty']})")
    
    # STEP 2: Check recipe and verify inventory
    print(f"\nSTEP 2: CHECK RECIPE & VERIFY INVENTORY")
    print(f"{'─' * 80}")
    
    required_ingredients = calculate_required_ingredients(order)
    print(f"Required Ingredients:")
    for ingredient_name, qty_needed in required_ingredients.items():
        print(f"  • {ingredient_name}: {qty_needed} grams")
    
    remaining_inventory_qty_map = build_remaining_inventory_qty_map(
        original_qty_map,
        cumulative_used_map,
    )
    missing_ingredients = check_inventory(required_ingredients, remaining_inventory_qty_map)
    
    print(f"\nInventory Check:")
    if missing_ingredients:
        print(f"❌ MISSING INGREDIENTS:")
        for ingredient_name, qty_short in missing_ingredients.items():
            print(f"  • {ingredient_name}: SHORT by {qty_short} grams")
    else:
        print(f"✓ ALL INGREDIENTS AVAILABLE IN INVENTORY")
    
    # STEP 3 & 4: Process order based on availability
    print(f"\nSTEP 3 & 4: PREPARE ORDER & UPDATE STATUS/INVENTORY")
    print(f"{'─' * 80}")
    
    status_record = get_or_create_status_record(order_id)
    
    if not missing_ingredients:
        # All ingredients available - prepare order
        print(f"✓ PREPARING ORDER...")
        remaining_inventory = deduct_inventory(
            required_ingredients,
            original_qty_map,
            cumulative_used_map,
        )
        status_record["delivered"] = True
        status_record["remark"] = "Delivered"
        print(f"✓ Status Updated: DELIVERED")
        print(f"✓ Inventory Updated:")
        for ingredient_name, remaining_qty in remaining_inventory.items():
            print(f"  • {ingredient_name}: {remaining_qty} grams remaining")
    else:
        # Missing ingredients - cannot prepare
        print(f"❌ CANNOT PREPARE ORDER - Ingredients Missing")
        status_record["delivered"] = False
        status_record["remark"] = "Not Delivered"
        print(f"✓ Status Updated: NOT DELIVERED")
        print(f"✓ Restock Table Updated:")
        add_to_restock(missing_ingredients, remaining_inventory_qty_map)
        for ingredient_name, qty_short in missing_ingredients.items():
            print(f"  • {ingredient_name}: Need {qty_short} grams")


def update_final_inventory(inventory_data, original_qty_map, cumulative_used_map):
    """Write final remaining quantities back to inventory table."""
    final_remaining_qty_map = build_remaining_inventory_qty_map(
        original_qty_map,
        cumulative_used_map,
    )
    for item in inventory_data:
        ingredient_name = item["ingredient"]
        if ingredient_name in final_remaining_qty_map:
            item["qty_grams"] = final_remaining_qty_map[ingredient_name]


def process_all_orders():
    """Process all orders and update inventory at the end."""
    original_qty_map = build_inventory_qty_map(inventory)
    cumulative_used_map = {}
    for order in orders:
        process_order_step_by_step(order, original_qty_map, cumulative_used_map)
    update_final_inventory(inventory, original_qty_map, cumulative_used_map)
    apply_inventory_health_restock_rules(inventory)


def print_final_summary():
    """Print final summary of all processing."""
    print(f"\n\n{'=' * 80}")
    print("FINAL SUMMARY")
    print(f"{'=' * 80}")
    
    print(f"\nDelivery Status Report:")
    for record in status:
        status_icon = "✓" if record["delivered"] else "❌"
        print(f"  {status_icon} Order ID {record['order_id']}: {record['remark']}")
    
    print(f"\nFinal Inventory:")
    print(json.dumps(inventory, indent=2))
    
    print(f"\nRestock Recommendations:")
    print(json.dumps(restock, indent=2))


if __name__ == "__main__":
    process_all_orders()
    print_final_summary()


