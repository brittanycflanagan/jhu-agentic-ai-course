from datetime import date
import unittest

from expense_tracker import EXPENSE_FIELDS, Expense, create_expense


class TestExpenseTracker(unittest.TestCase):
    def test_create_expense_stores_expected_values(self):
        expense = create_expense(
            amount=12.50,
            category="Food",
            description="Lunch",
            expense_date=date(2026, 5, 13),
        )

        print("\nTEST 1: Create expense stores expected values")
        print("Expected amount: 12.5")
        print("Actual amount:", expense.amount)
        print("Expected category: Food")
        print("Actual category:", expense.category)
        print("Expected description: Lunch")
        print("Actual description:", expense.description)
        print("Expected date: 2026-05-13")
        print("Actual date:", expense.date)

        self.assertEqual(expense.amount, 12.50)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Lunch")
        self.assertEqual(expense.date, date(2026, 5, 13))

    def test_expense_display_format_is_easy_to_read(self):
        expense = Expense(
            amount=12.50,
            category="Food",
            description="Lunch",
            date=date(2026, 5, 13),
        )

        expected_display = "2026-05-13 | Food | Lunch | $12.50"
        actual_display = expense.display()

        print("\nTEST 2: Expense display format")
        print("Expected display:", expected_display)
        print("Actual display:", actual_display)

        self.assertEqual(actual_display, expected_display)

    def test_expense_fields_match_required_columns(self):
        expected_fields = ("amount", "category", "description", "date")

        print("\nTEST 3: Expense field names")
        print("Expected fields:", expected_fields)
        print("Actual fields:", EXPENSE_FIELDS)

        self.assertEqual(EXPENSE_FIELDS, expected_fields)


if __name__ == "__main__":
    unittest.main()
