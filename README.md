# Cents

Cents is a simple CLI for managing your finances. It allows you to add, list, edit, and delete transactions.

## Installation

To install Cents, run the following command in your terminal:

```sh
git clone https://github.com/brandonpilane/cents.git
```

```sh
pip install .
```

## Usage

To use Cents, open your terminal and type `cents`.

### Add a transaction

To add a new transaction, use the `add` command. You can specify the description, amount, and type of the transaction.

```sh
cents add "Groceries" 100
```

```sh
cents add "Salary" 2000 -t income
```

### List transactions

To list all transactions, use the `list` command. You can filter the output by type.

```sh
cents list
```

```sh
cents list -t income
```

### Edit a transaction

To edit a transaction, use the `edit` command. You can specify the ID of the transaction, the new description, amount, and type.

```sh
cents edit 1 --desc "New description"
```

```sh
cents edit 1 --amount 1000 --type income
```

### Delete a transaction

To delete a transaction, use the `delete` command. You can specify the ID of the transaction.

```sh
cents delete 1
```

## Contributing

Contributions are welcome! If you find a bug or have a suggestion, please open an issue or submit a pull request.

## License

Cents is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
