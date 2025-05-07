# The Multi-Book Advanced Bible Search (mBAB)

## Table of Contents

- [Introduction](#introduction)  
- [Getting Started for Developers](#getting-started-for-developers)  
  - [Useful Resources](#useful-resources)  
  - [Requirements](#requirements)  
  - [Installation Steps](#installation-steps)  
  - [Setting Up the Bible Databases](#setting-up-the-bible-databases)  
  - [Running the Application](#running-the-application)  
- [Contributors](#contributors)  
- [Roadmap & Potential Contributions](#roadmap--potential-contributions)  
- [License](#license)

## Introduction

This web application allows users to search for word sequences—case-sensitive or case-insensitive—across a custom selection of Bible books.

**Features**
- Multi-book and multi-version search
- Logical AND (+) and OR (,) search syntax
- Case sensitivity toggle
- Responsive UI with collapsible book selector

Hosted live at [aaronjs.pythonanywhere.com](http://aaronjs.pythonanywhere.com/).

Originally built with Flask, now rebuilt using Django for better scalability and maintainability.

![A Search Example](./mBAB.png "Searching for 'spirit' and 'holy' and 'christ' within the non-Pauline New Testament books in the English Standard Version English Bible")

## Getting Started for Developers

This guide will help you set up and run the Multi-Book Advanced Bible Search (mBAB) project locally for development or customization.

### Useful Resources

- [Django Official Documentation](https://docs.djangoproject.com/en/stable/)
- [Jinja Template Syntax](https://jinja.palletsprojects.com/en/2.11.x/templates/) — used for templating
- [Python `sqlite3` Module](https://docs.python.org/3/library/sqlite3.html)
- [Tailwind CSS](https://tailwindcss.com/docs) — for utility-first styling

### Requirements

- Python 3.11 or higher
- `pip` and `venv` (usually bundled with Python)
- A Unix-like shell (Linux/macOS or WSL on Windows recommended)
- `make` (optional but recommended for easier setup and management)

### Installation Steps

```bash
# Clone the codebase repository
git clone https://github.com/aaronjohnsabu1999/mBAB.git ~/mBAB
cd ~/mBAB

# Set up a virtual environment
make venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install

# Apply Django migrations
make migrate
```

### Setting Up the Bible Databases
To keep the main repo lightweight, the SQLite Bible databases are hosted separately.
Download or clone them from Bible Databases and place the `.db` files inside a folder named `databases/` at the root of this project.

```bash
# Clone the database repository
mkdir ~/mBAB/databases/
git clone https://github.com/aaronjohnsabu1999/bible-databases.git ~/bible-databases/

# Move databases to codebase directory
cp ~/bible-databases/DB/*.db ~/mBAB/databases/
```

### Running the Application
Start the Django development server using make:

#### Default Localhost Run

```bash
make run
```
This will run the server at `127.0.0.1:8000`. Open your browser and navigate to [http://localhost:8000/](http://localhost:8000/).

#### Access on a Local Network (e.g., from your phone)

Override the host and/or port by passing variables:

```bash
make run HOST=0.0.0.0            # Binds to all interfaces
make run HOST=0.0.0.0 PORT=8080  # Custom port
```

Then visit in your mobile browser: `http://<your-computer-local-ip>:8000/`. To find your local IP:

```bash
# On Linux/macOS
hostname -I

# On Windows
ipconfig
```

Note: Ensure both devices are on the same Wi-Fi and that your firewall allows access on the selected port.

## Contributors

Formatting and design feedback have been generously provided by my parents, Sabu John and Jessy Sabu John, along with several other users.
Flask development support was offered extensively by [@hbhoyar](https://github.com/hbhoyar).
The searchable Bible content is based on SQL databases originally published by [@scrollmapper](https://github.com/scrollmapper) and later cleaned and reorganized by me. To keep this repository lightweight and easy to clone, those databases have been moved to a separate repository: [Bible Databases](https://github.com/aaronjohnsabu1999/bible-databases).

## Roadmap & Potential Contributions

- [x] Make the UI fully responsive for mobile screens
- [ ] Support copyrighted Bible versions (NIV, NLT, BSI, etc.)
- [ ] Add pagination for search results
- [x] Enable logical grouping and parentheses in search syntax
- [x] Move controls into a collapsible sidebar
- [ ] Improve styling with more theme options
- [ ] Add optional user accounts with saved history
- [ ] Subdivide books by genre (Law, Gospels, etc.)

## License

This project has been licensed under [![The GNU General Public License v3.0](https://www.gnu.org/graphics/gplv3-88x31.png "The GNU General Public License v3.0")](https://www.gnu.org/licenses/gpl-3.0.en.html)
