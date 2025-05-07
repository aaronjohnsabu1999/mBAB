import re, sqlite3
from django.shortcuts import render
from .bibledata import testaments, testament_map, books, versions, sql_select, sql_order
try:
    from .gtag_secret import GTAG_ID
except ImportError:
    GTAG_ID = None

def index(request, *args, **kwargs):
    return db_refresh(
        request,
        input_words="",
        version_name=versions[0]["name"],
        input_w=False,
        blank=True,
    )


def search(request, *args, **kwargs):
    return db_refresh(
        request,
        input_words=request.GET.get("keyword", ""),
        version_name=request.GET.get("version", ""),
        input_w=True,
    )


def case_flip(request, *args, **kwargs):
    return db_refresh(request, flip_case=True)


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def find_version(version_name):
    version = next(item for item in versions if item["name"] == version_name)
    return version["expansion"], version["wiki"]


def update_selection(selected_books, testaments):
    selected = set(selected_books.split())
    for book in books:
        if book["testament"] in testaments:
            selected.symmetric_difference_update({book["num"]})
    return " ".join(sorted(selected))


def sort_rows(rows):
    return sorted(
        rows, key=lambda row: (row["Book"], row["Chapter"], row["Versecount"])
    )


def update_testament(request, test, *args, **kwargs):
    return db_refresh(request, flip_test=test)


def book_select(request, *args, **kwargs):
    book_name = request.GET.get("book")
    for book in books:
        if book["text"] == book_name:
            return db_refresh(request, flip_book=book["num"])


# Boolean query helpers
def tokenize_expr(expr):
    return re.findall(r"\w+|[(),+]", expr)


def to_postfix(tokens):
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
    tokens = tokenize_expr(expression)
    postfix = to_postfix(tokens)
    where_clause, values = build_sql_from_postfix(postfix, case_sensitive)

    sql_command = f"{sql_select} {where_clause} {sql_order}"

    db = sqlite3.connect(f"./databases/{version_name}Bible_Database.db")
    db.row_factory = dict_factory
    cur = db.cursor()

    # 🔥 Add this line to enforce case-sensitive LIKE
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
    if keywords is None:
        keywords = input_words.split()
    return {
        "testaments": testaments,
        "books": books,
        "versions": versions,
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
    input_words = kwargs.get("input_words", "")
    version_name = kwargs.get("version_name") or request.GET.get("version", "ESV")
    input_w = kwargs.get("input_w", False)
    blank = kwargs.get("blank", False)
    flip_case = kwargs.get("flip_case", False)
    flip_book = kwargs.get("flip_book", "")
    flip_test = kwargs.get("flip_test", "")

    version_exp, version_wiki = find_version(version_name)

    if blank:
        selected_books = " ".join(book["num"] for book in books)
        response = render(
            request,
            "index.html",
            build_context(
                rows=[],
                version_name=version_name,
                version_exp=version_exp,
                version_wiki=version_wiki,
                input_words=input_words,
                selected_books=selected_books,
                case_sensitive=False,
            ),
        )
        return response

    case_sensitive = request.GET.get("case", "False") == "True"
    books_param = request.GET.get("books", "")
    selected_books = ""

    if books_param.isdigit():
        bits = f"{int(books_param):066b}"[::-1]
        selected_books = " ".join(f"{i:02}" for i, bit in enumerate(bits) if bit == "1")

    if flip_case:
        case_sensitive = not case_sensitive

    if flip_book:
        selected_books = (
            selected_books.replace(flip_book, "")
            if flip_book in selected_books
            else selected_books + flip_book + " "
        )
    if flip_test:
        selected_books = update_selection(
            selected_books, testament_map.get(flip_test, [])
        )

    # ✅ extract words once, use everywhere
    highlight_words = re.findall(r"\w+", input_words) if input_words else []

    # ✅ safe boolean-parsed SQL query + sorting
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
                    # Capture plain text before match, as string
                    parts.append({"text": verse_text[last_idx:start]})
                # Capture the match
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
