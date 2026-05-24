from dataclasses import dataclass
from datetime import date


#assumption: These four fields are the complete expense record for this version.
#verify: Check PROJECT_SPEC.md and future requirements for fields like payment method, merchant, or notes.
#todo: Update every dependent constant, test, CSV row, and display method if fields change.
EXPENSE_FIELDS = ("amount", "category", "description", "date")
#assumption: CSV persistence should use this exact order and these exact column names.
#verify: Confirm whether the spec prefers this name over EXPENSE_FIELDS everywhere.
#todo: Replace duplicate field constants with one canonical constant before implementing CSV logic.
CSV_FIELD_NAMES = ["amount", "category", "description", "date"]
#assumption: Dates will be stored and displayed using ISO-style YYYY-MM-DD.
#verify: Confirm users will not need locale-specific formats like MM/DD/YYYY.
#todo: Use this constant consistently when parsing and writing dates.
DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Expense:
    #assumption: A dataclass is enough for the data model and validation will live outside it.
    #verify: Confirm validation should not happen inside __post_init__.
    #todo: Add validation calls in the manager or creation flow once validation is implemented.
    amount: float
    #assumption: Amounts can be represented as float for this learning project.
    #verify: Check whether Decimal is needed to avoid money rounding issues.
    #todo: Revisit amount type before adding calculations and CSV persistence.
    category: str
    #assumption: Category is free-form text entered by the user.
    #verify: Confirm whether categories should be unrestricted or selected from a fixed list.
    #todo: Normalize category spelling/casing if grouped totals should merge similar entries.
    description: str
    #assumption: Description is required free-form text.
    #verify: Confirm whether blank descriptions should be rejected or allowed.
    #todo: Enforce this in validate_description.
    date: date
    #assumption: A Python date object is the internal representation for dates.
    #verify: Confirm loaded CSV rows should be converted from strings into date objects.
    #todo: Parse date strings during input and CSV loading.

    def display(self) -> str:
        #assumption: This simple pipe-separated display is readable enough for the CLI.
        #verify: Confirm whether the app needs aligned table columns instead.
        #todo: Update tests if the display format changes.
        return (
            f"{self.date.isoformat()} | "
            f"{self.category} | "
            f"{self.description} | "
            f"${self.amount:.2f}"
        )


def create_expense(
    amount: float,
    category: str,
    description: str,
    expense_date: date,
) -> Expense:
    #assumption: This helper only creates an Expense and does not validate input yet.
    #verify: Confirm whether create_expense should call validate_expense before returning.
    #todo: Add validation here or in ExpenseManager.add_expense after the validation component is implemented.
    return Expense(
        amount=amount,
        category=category,
        description=description,
        date=expense_date,
    )


# TODO Component 2: Core Manager / ExpenseManager
# TODO 2.1: Create an ExpenseManager class to manage the expense collection.
# TODO 2.2: Store expenses in an in-memory list.
# TODO 2.3: Add a method for adding a validated Expense object.
# TODO 2.4: Add a method for returning all expenses.
# TODO 2.5: Add a method for calculating totals grouped by category.
class ExpenseManager:
    #assumption: A manager class is the right place for collection operations and summaries.
    #verify: Confirm the project should stay single-file but still use this class.
    #todo: Decide whether file loading/saving belongs inside this manager or remains separate functions.
    def __init__(self):
        #assumption: Expenses will be stored in memory while the program is running.
        #verify: Confirm no database or automatic file write is expected after every change.
        #todo: Create self.expenses as a list of Expense objects.
        # TODO 2.2: Initialize the in-memory expense list.
        pass

    def add_expense(self, expense: Expense) -> None:
        #assumption: Only valid Expense objects should enter the manager.
        #verify: Confirm whether this method should reject invalid types as well as invalid field values.
        #todo: Call validate_expense before appending the expense.
        # TODO 2.3: Add a validated expense to the in-memory list.
        pass

    def get_all_expenses(self) -> list[Expense]:
        #assumption: Returning all stored expenses is acceptable for this small CLI app.
        #verify: Confirm whether callers should receive a copy to prevent accidental mutation.
        #todo: Decide whether to return self.expenses directly or a copied list.
        # TODO 2.4: Return all stored expenses.
        pass

    def get_totals_by_category(self) -> dict[str, float]:
        #assumption: Totals should be grouped by exact category text.
        #verify: Check whether "Food", "food", and " FOOD " should be treated as the same category.
        #todo: Normalize category values before grouping if needed.
        # TODO 2.5: Group expenses by category and calculate total amount.
        pass


# TODO Component 3: File I/O
# TODO 3.1: Create save_to_csv to save expenses using CSV_FIELD_NAMES.
# TODO 3.2: Convert Expense objects into CSV rows.
# TODO 3.3: Format dates as YYYY-MM-DD when saving.
# TODO 3.4: Create load_from_csv to load expenses on startup.
# TODO 3.5: Skip or reject malformed CSV rows.
# TODO 3.6: Return loaded expenses as Expense objects.
def save_to_csv(expenses: list[Expense], file_path: str) -> None:
    #assumption: The caller provides a valid file path and write permission exists.
    #verify: Confirm the default CSV filename and whether directories should be created automatically.
    #todo: Use csv.DictWriter with CSV_FIELD_NAMES and handle file write errors.
    # TODO 3.1-3.3: Save expenses to a CSV file.
    pass


def load_from_csv(file_path: str) -> list[Expense]:
    #assumption: Missing CSV files should start the app with an empty expense list.
    #verify: Confirm whether malformed rows should be skipped, reported, or stop the program.
    #todo: Use csv.DictReader, parse dates, convert amounts, and validate each loaded row.
    # TODO 3.4-3.6: Load expenses from a CSV file.
    pass


# TODO Component 4: Input Validation
# TODO 4.1: Validate that amount is numeric.
# TODO 4.2: Validate that amount is greater than zero.
# TODO 4.3: Validate that category is not blank.
# TODO 4.4: Validate that description is not blank.
# TODO 4.5: Validate that date uses YYYY-MM-DD format.
# TODO 4.6: Raise ValueError with clear messages for invalid input.
def validate_amount(amount: float) -> None:
    #assumption: Valid amounts must be numeric and greater than zero.
    #verify: Confirm whether zero-dollar expenses, refunds, or negative adjustments should be allowed.
    #todo: Raise ValueError with a clear message for non-numeric or non-positive amounts.
    # TODO 4.1-4.2: Validate expense amount.
    pass


def validate_category(category: str) -> None:
    #assumption: Category must contain non-whitespace text.
    #verify: Confirm whether category names should have a maximum length or allowed character rules.
    #todo: Strip whitespace and raise ValueError for blank categories.
    # TODO 4.3: Validate expense category.
    pass


def validate_description(description: str) -> None:
    #assumption: Description must contain non-whitespace text.
    #verify: Confirm whether description is truly required or can be optional.
    #todo: Strip whitespace and raise ValueError for blank descriptions.
    # TODO 4.4: Validate expense description.
    pass


def validate_expense_date(expense_date: date) -> None:
    #assumption: The internal date value should already be a date object.
    #verify: Confirm whether this validator should also parse strings from user input.
    #todo: Raise ValueError for invalid date types or invalid date strings if string input is allowed.
    # TODO 4.5: Validate expense date.
    pass


def validate_expense(expense: Expense) -> None:
    #assumption: Central validation should call each field-level validator.
    #verify: Confirm whether errors should stop at the first invalid field or collect all errors.
    #todo: Raise ValueError with clear messages for invalid expense data.
    # TODO 4.6: Run all expense validation checks.
    pass


# TODO Component 5: Main Application Loop
# TODO 5.1: Load expenses from CSV on startup.
# TODO 5.2: Display command-line menu options.
# TODO 5.3: Prompt the user to add an expense.
# TODO 5.4: Prompt the user to view all expenses.
# TODO 5.5: Prompt the user to view totals grouped by category.
# TODO 5.6: Save expenses to CSV.
# TODO 5.7: Exit the app cleanly after saving.
def display_menu() -> None:
    #assumption: A text menu is sufficient for the command-line interface.
    #verify: Confirm the exact menu options and numbering before implementation.
    #todo: Print options for add, view, summarize, save, and exit.
    # TODO 5.2: Show command-line menu options.
    pass


def prompt_for_expense() -> Expense:
    #assumption: User input will be collected with input() in the terminal.
    #verify: Confirm whether this should work in Jupyter as well as a normal terminal.
    #todo: Prompt for amount, category, description, and date, then validate before returning.
    # TODO 5.3: Collect expense input from the user.
    pass


def display_expenses(expenses: list[Expense]) -> None:
    #assumption: Each expense can be printed using Expense.display().
    #verify: Confirm how empty expense lists should be shown.
    #todo: Print a friendly empty-state message or each expense line.
    # TODO 5.4: Display all expenses in a readable format.
    pass


def display_totals_by_category(totals: dict[str, float]) -> None:
    #assumption: Totals can be displayed as category and dollar amount pairs.
    #verify: Confirm whether totals should be sorted alphabetically or by highest spend.
    #todo: Format totals consistently as currency.
    # TODO 5.5: Display category totals in a readable format.
    pass


def main() -> None:
    #assumption: main will own the app startup, loop, and shutdown sequence.
    #verify: Confirm whether expenses should autosave after every add or only on explicit save/exit.
    #todo: Load CSV, create ExpenseManager, process menu choices, save before exit.
    # TODO 5.1-5.7: Coordinate startup, menu loop, save, and exit.
    pass


if __name__ == "__main__":
    #assumption: The program should not start until main is implemented.
    #verify: Confirm when to replace this pass with main().
    #todo: Call main() once the command-line loop is ready.
    # TODO 5.7: Call main after the application loop is implemented.
    pass
