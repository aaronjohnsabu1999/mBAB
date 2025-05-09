import re, sqlite3
from django.shortcuts import render
from .bibledata import testaments, book_sections, books, versions, sql_select, sql_order

try:
    from .gtag_secret import GTAG_ID
except ImportError:
    GTAG_ID = None


def index(request, *args, **kwargs):
    """Render the homepage with default version and all books preselected (blank search)."""
    return db_refresh(
        request,
        blank=True,
    )


def search(request, *args, **kwargs):
    """Handle the search form submission and render filtered search results."""
    return db_refresh(
        request,
        input_words=request.GET.get("keyword", ""),
        version_name=request.GET.get("version", ""),
    )


def dict_factory(cursor, row):
    """Convert database rows into dictionaries keyed by column name."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def find_version(version_name):
    """Return the version expansion and wiki link for a given short version name."""
    version = next(item for item in versions if item["name"] == version_name)
    return version["expansion"], version["wiki"]


def sort_rows(rows):
    """Sort search result rows by book, chapter, and verse order."""
    return sorted(
        rows, key=lambda row: (row["Book"], row["Chapter"], row["Versecount"])
    )


def tokenize_expr(expr):
    """Split a Boolean keyword expression into tokens (words and operators)."""
    return re.findall(r"\w+|[(),+]", expr)


def to_postfix(tokens):
    """
    Convert infix Boolean tokens into postfix (Reverse Polish Notation).

    Uses + as AND, , as OR, and supports parentheses.
    """
    precedence = {"+": 2, ",": 1}
    output = []
    stack = []
    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token in ("+", ","):
            while (
                stack
                and stack[-1] in precedence
                and precedence[stack[-1]] >= precedence[token]
            ):
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
    while stack:
        output.append(stack.pop())
    return output


def build_sql_from_postfix(postfix_tokens, case_sensitive=False):
    """
    Build a safe SQL WHERE clause from postfix Boolean tokens.

    Args:
        postfix_tokens: list of tokens in postfix order.
        case_sensitive: if True, performs case-sensitive search.

    Returns:
        A tuple of SQL WHERE clause string and list of values for binding.
    """
    stack = []
    values = []
    for token in postfix_tokens:
        if token.isalnum():
            if case_sensitive:
                stack.append(("verse LIKE ?", [f"%{token}%"]))
            else:
                stack.append(("LOWER(verse) LIKE LOWER(?)", [f"%{token}%"]))
        elif token in ("+", ","):
            op = "AND" if token == "+" else "OR"
            right_expr, right_vals = stack.pop()
            left_expr, left_vals = stack.pop()
            combined_expr = f"({left_expr} {op} {right_expr})"
            stack.append((combined_expr, left_vals + right_vals))
    return stack[0] if stack else ("1=0", [])


def sql_row_gen(expression, version_name, case_sensitive=False):
    """
    Execute the SQL query for a given search expression and Bible version.

    Args:
        expression: the Boolean search expression (user input).
        version_name: short name of the Bible version (e.g., "ESV").
        case_sensitive: whether to perform a case-sensitive search.

    Returns:
        A list of result rows as dictionaries.
    """
    tokens = tokenize_expr(expression)
    postfix = to_postfix(tokens)
    where_clause, values = build_sql_from_postfix(postfix, case_sensitive)

    sql_command = f"{sql_select} {where_clause} {sql_order}"

    db = sqlite3.connect(f"./databases/{version_name}Bible_Database.db")
    db.row_factory = dict_factory
    cur = db.cursor()

    if case_sensitive:
        cur.execute("PRAGMA case_sensitive_like = true;")

    cur.execute(sql_command, values)
    rows = cur.fetchall()
    cur.close()
    return rows


def build_context(
    rows,
    version_name,
    version_exp,
    version_wiki,
    input_words,
    selected_books,
    case_sensitive,
    keywords=None,
):
    """
    Build the Django template context dictionary for rendering results.

    Args:
        rows: list of search results (dicts).
        version_name: short version identifier (e.g., "ESV").
        version_exp: full name of the version.
        version_wiki: link to the version's wiki page.
        input_words: the original search expression.
        selected_books: string of selected book numbers.
        case_sensitive: whether search is case-sensitive.
        keywords: optional list of words for highlighting.

    Returns:
        A dictionary suitable for rendering the template.
    """
    if keywords is None:
        keywords = input_words.split()
    return {
        "testaments": testaments,
        "books": books,
        "versions": versions,
        "book_sections": book_sections,
        "rows": rows,
        "version_name": version_name,
        "version_exp": version_exp,
        "version_wiki": version_wiki,
        "case_sensitive": case_sensitive,
        "keywords": keywords,
        "keyword": input_words,
        "selBooks": selected_books,
        "gtag_id": GTAG_ID,
    }


def db_refresh(request, *args, **kwargs):
    """
    Core dispatcher for handling search and filter logic.

    Args:
        request: Django request object.
        kwargs may include:
          - input_words: search query string
          - version_name: short version name
          - blank: whether to initialize empty context
          - flip_case: toggle case sensitivity
          - flip_book: book number to toggle
          - flip_test: testament key to toggle (ot, nt, bib)

    Returns:
        HttpResponse rendered with `index.html` and appropriate context.
    """
    blank = kwargs.get("blank", False)

    input_words = kwargs.get("input_words", "")
    version_name = kwargs.get("version_name") or request.GET.get(
        "version", versions[0]["name"]
    )
    version_exp, version_wiki = find_version(version_name)

    if blank:
        return render(
            request,
            "index.html",
            build_context(
                rows=[],
                version_name=version_name,
                version_exp=version_exp,
                version_wiki=version_wiki,
                input_words=input_words,
                selected_books=" ".join(book["num"] for book in books),
                case_sensitive=False,
            ),
        )

    case_sensitive = request.GET.get("case", "False") == "True"
    books_param = request.GET.get("books", "")
    selected_books = ""

    if books_param.isdigit():
        bits = f"{int(books_param):066b}"[::-1]
        selected_books = " ".join(f"{i:02}" for i, bit in enumerate(bits) if bit == "1")

    highlight_words = re.findall(r"\w+", input_words) if input_words else []

    raw_rows = sort_rows(sql_row_gen(input_words, version_name, case_sensitive))
    rows = []
    for row in raw_rows:
        if f"{row['Book']:02}" in selected_books:
            book_text = next(b for b in books if b["id"] == row["Book"])["text"]
            rows.append(
                {
                    "Book": book_text,
                    "Chapter": row["Chapter"],
                    "Versecount": row["Versecount"],
                    "verse": row["verse"],
                }
            )

    for row in rows:
        if input_words:
            regex = "|".join(re.escape(word) for word in highlight_words)
            verse_text = row["verse"]
            matches = list(
                re.finditer(
                    regex, verse_text, flags=0 if case_sensitive else re.IGNORECASE
                )
            )

            parts = []
            last_idx = 0
            for match in matches:
                start, end = match.span()
                if start > last_idx:
                    parts.append({"text": verse_text[last_idx:start]})
                parts.append({"highlight": verse_text[start:end]})
                last_idx = end
            if last_idx < len(verse_text):
                parts.append({"text": verse_text[last_idx:]})

            row["verse"] = parts
        else:
            row["verse"] = [{"text": row["verse"]}]

    response = render(
        request,
        "index.html",
        build_context(
            rows=rows,
            version_name=version_name,
            version_exp=version_exp,
            version_wiki=version_wiki,
            input_words=input_words,
            selected_books=selected_books,
            case_sensitive=case_sensitive,
            keywords=highlight_words,
        ),
    )

    return response
