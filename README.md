# The Multi-Book Advanced Bible Search (mBAB)

## Table of Contents

- [Introduction](#introduction)
- [For the Developer...](#for-the-developer)
  * [Useful Links](#useful-links)
  * [Installation of Necessary Packages](#installation-of-necessary-packages)
- [Contributors](#contributors)
- [Possible additions and modifications](#possible-additions-and-modifications)
- [License](#license)

## Introduction

This web application allows users to search for word sequences—either case-sensitive or case-insensitive—across a user-specified set of Bible books.  

**Features**
- Multi-book and multi-version search
- Case-sensitive or insensitive toggling
- Custom book selection with OT/NT toggles
- Clean, dark-mode friendly UI
- Logical AND (+) and OR (,) search operators

Hosted live at [aaronjs.pythonanywhere.com](http://aaronjs.pythonanywhere.com/).

Originally built with Flask, **rebuilt using Django** for better scalability, maintainability, and extensibility.

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

### Installation Steps

```bash
# Clone the codebase repository
git clone https://github.com/aaronjohnsabu1999/mBAB.git ~/mBAB
cd ~/mBAB

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply Django migrations (none required yet, but necessary for Django setup)
python manage.py migrate
```

### Setting Up the Bible Databases
To keep the main repo lightweight, the SQLite Bible databases are hosted separately.
Download or clone them from Bible Databases and place the .db files inside a folder named databases/ at the root of this project.

```bash
# Clone the database repository
mkdir ~/mBAB/databases/
git clone https://github.com/aaronjohnsabu1999/bible-databases.git ~/bible-databases/

# Move databases to codebase directory
cp ~/bible-databases/DB/*.db ~/mBAB/databases/
```

### Running the Application
Start the Django development server:

```bash
# Run the application locally
python manage.py runserver
```

Then open your browser and navigate to: [http://localhost:8000/](http://localhost:8000/).  
You should see the mBAB interface ready for searches and exploration.

## Contributors

Formatting and design feedback have been generously provided by my parents, Sabu John and Jessy Sabu John, along with several other users.
Flask development support was offered extensively by [@hbhoyar](https://github.com/hbhoyar).
The searchable Bible content is based on SQL databases originally published by [@scrollmapper](https://github.com/scrollmapper) and later cleaned and reorganized by me. To keep this repository lightweight and easy to clone, those databases have been moved to a separate repository: [Bible Databases](https://github.com/aaronjohnsabu1999/bible-databases).

## Roadmap & Potential Contributions

- [ ] Make the UI fully responsive for mobile screens
- [ ] Support copyrighted Bible versions (NIV, NLT, BSI, etc.)
- [ ] Add pagination for search results
- [ ] Enable logical grouping and parentheses in search syntax
- [ ] Move controls into a collapsible sidebar
- [ ] Improve styling with more theme options
- [ ] Add optional user accounts with saved history
- [ ] Subdivide books by genre (Law, Gospels, etc.)

## License

This project has been licensed under [![The GNU General Public License v3.0](https://www.gnu.org/graphics/gplv3-88x31.png "The GNU General Public License v3.0")](https://www.gnu.org/licenses/gpl-3.0.en.html)
