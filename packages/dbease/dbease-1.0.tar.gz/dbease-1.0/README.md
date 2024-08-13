# DBEase

DBEase is a Python module designed to simplify working with SQLite databases. It provides an easy-to-use interface for creating and managing tables based on a configuration file, without needing to write SQL commands.

## Features

- Automatically creates SQLite tables based on a `database.ini` configuration file.
- Supports basic CRUD (Create, Read, Update, Delete) operations.
- Infers column types from the configuration file.

## Installation

No installation is required beyond ensuring you have Python and SQLite. Simply include the `Database` class in your project.

## Configuration

The `database.ini` file defines the tables and columns for the database. If this file does not exist, it will be created with default content.

### Example `database.ini`

```ini
[user]
first_name = Mohammad
last_name = Mohammadi
username = Aytola
password = TestPassword
age = 21
register = 08/12/2024,12:16:11

[admin]
first_name = Mohammad
last_name = Mohammadi
username = Aytola
password = TestPassword
```
## Adding New Tables or Columns
To add new tables or columns:

Edit `database.ini`: Open the `database.ini` file and add your new tables or columns. Ensure the syntax is correct.
Delete the Existing Database File: Delete the existing `DataBase.db` file if it exists. This is necessary because the database will be recreated based on the updated `database.ini` file.
Re-run the Script: When you run the script again, the `DataBase.db` file will be recreated with the new tables and columns defined in `database.ini`.

## Usage

### Importing and Connecting

```python
    from DBEase import database  # Replace `DBEase` with the actual module name

    # Create a Database instance and connect
    db = database()
```

## Creating Tables

Tables will be created automatically based on the `database.ini` file when you connect to the database. If tables already exist, they will not be recreated

## Performing CRUD Operations

### Inserting Data

```python
    table = db.nametable
    db.table = table.user
    db.data = {'first_name': 'Mehran', 'last_name': 'Mohammadi', 'username': 'YarNovin', 'password': 'Testpassword', 'age': 29, 'register': '08/12/2024,12:16:11'}
    row_id = db.insert
    print(f"Inserted row ID: {row_id}")
```

### Querying Data

```python
db.query = {'username': 'YarNovin'}
records = db.get
for record in records:
    print(record)
```

### Checking for Records

```python
exists = db.check
print(f"Records exist: {exists}")
```

### Retrieving All Data

```python
all_records = db.all
for record in all_records:
    print(record)
```

### Updating Data

```python
db.query = {'username': 'YarNovin'}
db.data = {'password': 'NewPassword'}
db.set
```
 
### Deleting Data

```python
db.query = {'username': 'YarNovin'}
db.delete
```

## Notes

- Ensure the `database.ini` file is correctly configured before running the script.
- To apply changes to the database schema, modify the `database.ini` file and delete the existing `DataBase.db` file. Re-run the script to recreate the database with the updated schema.

## License

This project is licensed under the MIT License.
