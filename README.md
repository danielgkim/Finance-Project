# PersonalFinanceTracker

A Python-based personal finance tracking tool using SQLite for managing and analyzing financial transactions. This project provides functionalities for adding, categorizing, and summarizing transactions to help you monitor your income, expenses, and savings.

## Features

- **Transaction Management**: Add transactions with details such as date, category, description, amount, and type (income or expense).
- **Category Management**: Add and customize categories for transactions.
- **Balance Calculation**: Calculate your current balance based on income and expenses.
- **Monthly Summary**: Get a summary of income, expenses, and net savings for a specified month.
- **Transaction Filtering**: Filter and view transactions based on date range and category.

## Requirements

- Python 3
- SQLite3
- Pandas

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Install Pandas:
   ```bash
   pip install pandas
   ```

## Usage

1. **Initialize the Tracker**:
   ```python
   from PersonalFinanceTracker import PersonalFinanceTracker
   tracker = PersonalFinanceTracker()
   ```

2. **Add a Transaction**:
   ```python
   tracker.add_transaction('2024-10-01', 'Salary', 'Monthly salary', 5000, 'income')
   ```

3. **Add a Category**:
   ```python
   tracker.add_category('Freelance', 'income')
   ```

4. **Get Current Balance**:
   ```python
   balance = tracker.get_balance()
   print(f"Current balance: ${balance:.2f}")
   ```

5. **Monthly Summary**:
   ```python
   summary = tracker.get_monthly_summary(2024, 10)
   print("Monthly Summary:", summary)
   ```

6. **View Transactions**:
   ```python
   transactions = tracker.get_transactions(start_date='2024-10-01', end_date='2024-10-31')
   print(transactions)
   ```

7. **Close the Tracker**:
   ```python
   tracker.close()
   ```

## Example

An example usage of this tool can be found in the `main()` function in `PersonalFinanceTracker.py`. It demonstrates how to add transactions, get balance, and view monthly summaries.

```python
if __name__ == "__main__":
    main()
```

## Database Structure

The SQLite database contains two tables:

- **transactions**:
  - `id`: Transaction ID
  - `date`: Transaction date
  - `category`: Transaction category
  - `description`: Transaction description
  - `amount`: Transaction amount
  - `type`: Type of transaction (`income` or `expense`)

- **categories**:
  - `id`: Category ID
  - `name`: Category name
  - `type`: Type of category (`income` or `expense`)

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit pull requests for enhancements or bug fixes.

---

Enjoy managing your finances!
