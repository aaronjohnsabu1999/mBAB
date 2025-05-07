import re, sqlite3
from django.shortcuts import render
from django.http import HttpResponse
from .bibledata import testaments, testament_map, books, versions, sql_select, sql_order


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def keyword_splitter(input_words):
    keywords = re.split(r"[,+]", input_words)
    delimiters = re.findall(r"[,+]", input_words)
    return keywords, delimiters


def find_version(version_name):
    version = next(item for item in versions if item["name"] == version_name)
    return version["expansion"], version["wiki"]


def update_selection(selected_books, testaments):
    selected = set(selected_books.split())
    for book in books:
        if book["testament"] in testaments:
            selected.symmetric_difference_update({book["num"]})
    return " ".join(sorted(selected))


def result_sorter(rows):
    return sorted(
        rows, key=lambda row: (row["Book"], row["Chapter"], row["Versecount"])
    )


def index(request, *args, **kwargs):
    for book in books:
        book["selected"] = True
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


def update_testament(request, test, *args, **kwargs):
    return db_refresh(request, flip_test=test)


def book_select(request, *args, **kwargs):
    book_name = request.GET.get("book")
    for book in books:
        if book["text"] == book_name:
            return db_refresh(request, flip_book=book["num"])


def book_update(input_words, case_sensitive, selected_books, rows):
    updated_rows = []
    for row in rows:
        exact_match = any(word in row["verse"] for word in input_words)
        if f"{row['Book']:02}" in selected_books and (
            not case_sensitive or exact_match
        ):
            book_text = next(b for b in books if b["id"] == row["Book"])["text"]
            updated_rows.append(
                {
                    "Book": book_text,
                    "Chapter": row["Chapter"],
                    "Versecount": row["Versecount"],
                    "verse": row["verse"],
                }
            )
    return updated_rows


def sql_row_gen(keywords, version_name, delimiters):
    sql_command = sql_select
    conditions = []

    for i, word in enumerate(keywords):
        if word.strip() == "":
            continue
        conditions.append(f"LOWER(verse) LIKE LOWER('%{word}%')")
        if i < len(delimiters):
            if delimiters[i] == ",":
                conditions.append("OR")
            elif delimiters[i] == "+":
                conditions.append("AND")

    while conditions and conditions[-1] in ("AND", "OR"):
        conditions.pop()

    if not conditions:
        sql_command = sql_select + "1=0 " + sql_order
    else:
        sql_command += " ".join(conditions) + " " + sql_order

    db = sqlite3.connect(f"./databases/{version_name}Bible_Database.db")
    db.row_factory = dict_factory
    cur = db.cursor()
    cur.execute(sql_command)
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
    }


def db_refresh(request, *args, **kwargs):
    input_words = kwargs.get("input_words", "")
    version_name = kwargs.get("version_name", "")
    input_w = kwargs.get("input_w", False)
    blank = kwargs.get("blank", False)
    flip_case = kwargs.get("flip_case", False)
    flip_book = kwargs.get("flip_book", "")
    flip_test = kwargs.get("flip_test", "")

    response = HttpResponse()

    if not blank and version_name == "":
        version_name = request.COOKIES.get("version_name", "ESV")
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
        response.set_cookie("case_sensitive", "False")
        response.set_cookie("version_name", version_name)
        response.set_cookie("selected_books", selected_books)
        return response

    case_sensitive = request.COOKIES.get("case_sensitive", "False") == "True"
    if not input_w:
        input_words = request.COOKIES.get("search_input", "")
    if flip_case:
        case_sensitive = not case_sensitive

    selected_books = request.COOKIES.get("selected_books", "")

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

    keywords, delimiters = keyword_splitter(input_words)
    rows = book_update(
        keywords,
        case_sensitive,
        selected_books,
        result_sorter(sql_row_gen(keywords, version_name, delimiters)),
    )

    for row in rows:
        if input_words:
            regex = "|".join(re.escape(word) for word in keywords)
            row["verse"] = re.split(f"({regex})", row["verse"], flags=re.IGNORECASE)

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
            keywords=keywords,
        ),
    )

    response.set_cookie("case_sensitive", str(case_sensitive))
    response.set_cookie("search_input", input_words)
    response.set_cookie("version_name", version_name)
    response.set_cookie("selected_books", selected_books)
    return response
