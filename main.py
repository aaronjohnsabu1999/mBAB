from flask import Flask, request, make_response, render_template as render
import sqlite3
import re

sqlSelect = "SELECT * FROM bible WHERE "
sqlOrder  = "ORDER BY Book, Chapter, Versecount"

versions = [
            {'expansion': "King James Version",           'name': "KJV",  'db': '../bible-databases/DB/KJVBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/King_James_Version '},
            {'expansion': "English Standard Version",     'name': "ESV",  'db': '../bible-databases/DB/ESVBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/English_Standard_Version'},
            {'expansion': "American King James Version",  'name': "AKJV", 'db': '../bible-databases/DB/AKJVBible_Database.db', 'wiki': 'https://studybible.info/version/AKJV'},
            {'expansion': "Berean Study Bible",           'name': "BSB",  'db': '../bible-databases/DB/BSBBible_Database.db',  'wiki': 'https://bereanbible.com/'},
            {'expansion': "New King James Version",       'name': "NKJV", 'db': '../bible-databases/DB/NKJVBible_Database.db', 'wiki': 'https://en.wikipedia.org/wiki/New_King_James_Version'},
            {'expansion': "American Standard Version",    'name': "ASV",  'db': '../bible-databases/DB/ASVBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/American_Standard_Version'},
            {'expansion': "New American Standard Bible",  'name': "NASB", 'db': '../bible-databases/DB/NASBBible_Database.db', 'wiki': 'https://en.wikipedia.org/wiki/New_American_Standard_Bible'},
            {'expansion': "Young's Literal Translation",  'name': "YLT",  'db': '../bible-databases/DB/YLTBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/Young\'s_Literal_Translation'},
            {'expansion': "Geneva Bible",                 'name': "GEN",  'db': '../bible-databases/DB/GENBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/Geneva_Bible'},
            {'expansion': "Updated King James Version",   'name': "UKJV", 'db': '../bible-databases/DB/UKJVBible_Database.db', 'wiki': 'http://www.bible-discovery.com/bible-license-ukjv.php'},
            {'expansion': "Darby English Bible",          'name': "DBY",  'db': '../bible-databases/DB/DBYBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/Darby_Bible'},
            {'expansion': "Webster's Revision",           'name': "WBT",  'db': '../bible-databases/DB/WBTBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/Webster%27s_Revision'},
            {'expansion': "World English Bible",          'name': "WEB",  'db': '../bible-databases/DB/WEBBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/World_English_Bible'},
            {'expansion': "Amplified Bible",              'name': "AMP",  'db': '../bible-databases/DB/AMPBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/Amplified_Bible'},
            {'expansion': "Contemporary English Version", 'name': "CEV",  'db': '../bible-databases/DB/CEVBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/Contemporary_English_Version'},
            {'expansion': "Bible in Basic English",       'name': "BBE",  'db': '../bible-databases/DB/BBEBible_Database.db',  'wiki': 'https://en.wikipedia.org/wiki/Bible_in_Basic_English'}
            ]
books    = [ {
      'num': "00", 'type': "Pentateuch", 'selected': True, 'testament': "OT1", 'id': 0,  'text': "Genesis" }, {
      'num': "01", 'type': "Pentateuch", 'selected': True, 'testament': "OT1", 'id': 1,  'text': "Exodus" }, {
      'num': "02", 'type': "Pentateuch", 'selected': True, 'testament': "OT1", 'id': 2,  'text': "Leviticus" }, {
      'num': "03", 'type': "Pentateuch", 'selected': True, 'testament': "OT1", 'id': 3,  'text': "Numbers" }, {
      'num': "04", 'type': "Pentateuch", 'selected': True, 'testament': "OT1", 'id': 4,  'text': "Deuteronomy" }, {
      'num': "05", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 5,  'text': "Joshua" }, {
      'num': "06", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 6,  'text': "Judges" }, {
      'num': "07", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 7,  'text': "Ruth" }, {
      'num': "08", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 8,  'text': "1 Samuel" }, {
      'num': "09", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 9,  'text': "2 Samuel" }, {
      'num': "10", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 10, 'text': "1 Kings" }, {
      'num': "11", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 11, 'text': "2 Kings" }, {
      'num': "12", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 12, 'text': "1 Chronicles" }, {
      'num': "13", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 13, 'text': "2 Chronicles" }, {
      'num': "14", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 14, 'text': "Ezra" }, {
      'num': "15", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 15, 'text': "Nehemiah" }, {
      'num': "16", 'type': "OTHistory",  'selected': True, 'testament': "OT1", 'id': 16, 'text': "Esther" }, {
      'num': "17", 'type': "OTWisdom",   'selected': True, 'testament': "OT1", 'id': 17, 'text': "Job" }, {
      'num': "18", 'type': "OTWisdom",   'selected': True, 'testament': "OT1", 'id': 18, 'text': "Psalms" }, {
      'num': "19", 'type': "OTWisdom",   'selected': True, 'testament': "OT1", 'id': 19, 'text': "Proverbs" }, {
      'num': "20", 'type': "OTWisdom",   'selected': True, 'testament': "OT2", 'id': 20, 'text': "Ecclesiastes" }, {
      'num': "21", 'type': "OTWisdom",   'selected': True, 'testament': "OT2", 'id': 21, 'text': "Song of Songs" }, {
      'num': "22", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 22, 'text': "Isaiah" }, {
      'num': "23", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 23, 'text': "Jeremiah" }, {
      'num': "24", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 24, 'text': "Lamentations" }, {
      'num': "25", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 25, 'text': "Ezekiel" }, {
      'num': "26", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 26, 'text': "Daniel" }, {
      'num': "27", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 27, 'text': "Hosea" }, {
      'num': "28", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 28, 'text': "Joel" }, {
      'num': "29", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 29, 'text': "Amos" }, {
      'num': "30", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 30, 'text': "Obadiah" }, {
      'num': "31", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 31, 'text': "Jonah" }, {
      'num': "32", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 32, 'text': "Micah" }, {
      'num': "33", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 33, 'text': "Nahum" }, {
      'num': "34", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 34, 'text': "Habakkuk" }, {
      'num': "35", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 35, 'text': "Zephaniah" }, {
      'num': "36", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 36, 'text': "Haggai" }, {
      'num': "37", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 37, 'text': "Zechariah" }, {
      'num': "38", 'type': "OTProphet",  'selected': True, 'testament': "OT2", 'id': 38, 'text': "Malachi" }, {
      'num': "39", 'type': "Gospel",     'selected': True, 'testament': "NT1", 'id': 39, 'text': "Matthew" }, {
      'num': "40", 'type': "Gospel",     'selected': True, 'testament': "NT1", 'id': 40, 'text': "Mark" }, {
      'num': "41", 'type': "Gospel",     'selected': True, 'testament': "NT1", 'id': 41, 'text': "Luke" }, {
      'num': "42", 'type': "Gospel",     'selected': True, 'testament': "NT1", 'id': 42, 'text': "John" }, {
      'num': "43", 'type': "NTHistory",  'selected': True, 'testament': "NT1", 'id': 43, 'text': "Acts of the Apostles" }, {
      'num': "44", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 44, 'text': "Romans" }, {
      'num': "45", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 45, 'text': "1 Corinthians" }, {
      'num': "46", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 46, 'text': "2 Corinthians" }, {
      'num': "47", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 47, 'text': "Galatians" }, {
      'num': "48", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 48, 'text': "Ephesians" }, {
      'num': "49", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 49, 'text': "Philippians" }, {
      'num': "50", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 50, 'text': "Colossians" }, {
      'num': "51", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 51, 'text': "1 Thessalonians" }, {
      'num': "52", 'type': "Epistle",    'selected': True, 'testament': "NT1", 'id': 52, 'text': "2 Thessalonians" }, {
      'num': "53", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 53, 'text': "1 Timothy" }, {
      'num': "54", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 54, 'text': "2 Timothy" }, {
      'num': "55", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 55, 'text': "Titus" }, {
      'num': "56", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 56, 'text': "Philemon" }, {
      'num': "57", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 57, 'text': "Hebrews" }, {
      'num': "58", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 58, 'text': "James" }, {
      'num': "59", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 59, 'text': "1 Peter" }, {
      'num': "60", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 60, 'text': "2 Peter" }, {
      'num': "61", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 61, 'text': "1 John" }, {
      'num': "62", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 62, 'text': "2 John" }, {
      'num': "63", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 63, 'text': "3 John" }, {
      'num': "64", 'type': "Epistle",    'selected': True, 'testament': "NT2", 'id': 64, 'text': "Jude" }, {
      'num': "65", 'type': "NTProphet",  'selected': True, 'testament': "NT2", 'id': 65, 'text': "Revelation" }
    ]

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def keywordSplitter(inputWords):
    keywords = re.split(r'[,+]*', inputWords)
    delimit  = []
    for char in inputWords:
        if (char == ',') or (char == '+'):
            delimit.append(char)
    return keywords, delimit

def findVersion(versionName):
    version = next(item for item in versions if item['name'] == versionName)
    return (version['expansion'], version['wiki'])

def updateSelection(selBooks, list):
    for book in books:
        if book['testament'] in list:
            if book['num'] in selBooks:
                selBooks = ''.join(selBooks.split(book['num']+" "))
            elif selBooks == "None":
                selBooks = book['num'] + " "
            else:
                selBooks = selBooks + book['num'] + " "
    return selBooks

def bookNum2Str(bookNum):
    if bookNum<10:
        return "0"+str(bookNum)
    return str(bookNum)

def sqlRowGen(keywords, versionName, delimit):
    sqlCommand = sqlSelect
    for wordNum in range(len(keywords)):
        sqlCommand += "LOWER(verse) LIKE LOWER('%" + keywords[wordNum] + "%') "
        if (wordNum == len(delimit)):
            sqlCommand += sqlOrder
        elif (delimit[wordNum] == ','):
            sqlCommand += "OR "
        elif (delimit[wordNum] == '+'):
            sqlCommand += "AND "

    db = sqlite3.connect(next(item for item in versions if item['name'] == versionName)['db'])
    db.row_factory = dict_factory
    cur  = db.cursor()
    cur.execute(sqlCommand)
    rows = cur.fetchall()
    cur.close()
    return rows

# resultSorted() idea incorporated from https://web.archive.org/web/20150222160237/stygianvision.net/updates/python-sort-list-object-dictionary-multiple-key/
def resultSorter(rows=[]):
    return sorted(rows, key = lambda row: (row['Book'], row['Chapter'], row['Versecount']))


app = Flask(__name__)


def bookUpdate(inputWords, caseSns, selBooks, rows=[]):
    editRows = []
    for row in rows:
        exactMatch = False
        for word in inputWords:
            if (word in row['verse']):
                exactMatch = True
                break
        if (bookNum2Str(row['Book']) in selBooks) and (not caseSns or exactMatch):
            book = next(item for item in books if item['id'] == row['Book'])['text']
            editRows.append({'Book': book, 'Chapter': row['Chapter'], 'Versecount': row['Versecount'], 'verse': row['verse']})
    return editRows


def dbRefresh(inputWords = "", versionName = "", inputW = False, blank = False, flipCase = False, flipBook = "", flipTest = ""):
    if not blank and versionName == "":
        versionName = request.cookies.get('version_name')
    (versionExp, versionWiki)  = findVersion(versionName)

    if blank:
        selBooks = ""
        for book in books:
            selBooks = selBooks + book['num'] + " "
        resp = make_response(render('index.html', rows = [], version_name = versionName, version_exp = versionExp, version_wiki = versionWiki, versions = versions, books = books, caseSns = False, keywords = "", keyword = inputWords, selBooks = selBooks))
        resp.set_cookie('case_sense',  "False")
        resp.set_cookie('searchInput', "")
        resp.set_cookie('version_name', versions[0]['name'])
        resp.set_cookie('selectedBooks', selBooks)
        return resp
    
    caseSns = True if (request.cookies.get('case_sense') == "True") else False
    if not inputW:
        inputWords = request.cookies.get('searchInput')
    if flipCase:
        caseSns = not caseSns

    selBooks = request.cookies.get('selectedBooks')
    if not (flipBook == ""):
        if flipBook in selBooks:
            selBooks = ''.join(selBooks.split(flipBook))
        elif selBooks == "None":
            selBooks = flipBook + " "
        else:
            selBooks = selBooks + flipBook + " "

    if not (flipTest == ""):
        if   flipTest == "ot":
            selBooks = updateSelection(selBooks, ["OT1", "OT2"])
        elif flipTest == "nt":
            selBooks = updateSelection(selBooks, ["NT1", "NT2"])
        elif flipTest == "bib":
            if all((book['num'] in selBooks) for book in books):
                selBooks = updateSelection(selBooks, ["OT1", "OT2", "NT1", "NT2"])
            else:
                selBooks = ""
                for book in books:
                    selBooks = selBooks + book['num'] + " "
        else:
            selBooks = selBooks
    
    keywords, delimit = keywordSplitter(inputWords)
    # try:
    rows = bookUpdate(keywords, caseSns, selBooks, resultSorter(sqlRowGen(keywords, versionName, delimit)))
    # except Exception:
        # rows = [{'Book': "-", 'Chapter': "-", 'Versecount': "-", 'verse': "!!! ERROR !!! Check your input!"}]
    for row in rows:
        wordSeq = "( )"
        if not (inputWords == ""):
            wordSeq = ["("]
            for word in keywords:
                wordSeq.append(word)
                wordSeq.append("|")
            wordSeq.pop()
            wordSeq.append(")")
            wordSeq = ''.join(wordSeq)
        row['verse'] = re.split(wordSeq, row['verse'], flags=re.IGNORECASE)

    pastSearches = request.cookies.get('past_searches')
    if (pastSearches == None):
        pastSearches = inputWords + " :: "
    else:
        lenPast = 8
        if (pastSearches.count(" :: ") == lenPast):
            index = pastSearches.find(" :: ")
            pastSearches = pastSearches[index+4:]
        if (pastSearches.count(" :: ") > lenPast):
            pastSearches =  ""
        pastSearches = pastSearches + (inputWords + " :: ")

    resp = make_response(render('index.html', rows = rows, version_name = versionName, version_exp = versionExp, version_wiki = versionWiki, versions = versions, books = books, caseSns = caseSns, keywords = keywords, keyword = inputWords, selBooks = selBooks))
    resp.set_cookie('case_sense',    str(caseSns))
    resp.set_cookie('searchInput',   inputWords)
    resp.set_cookie('version_name',  versionName)
    resp.set_cookie('selectedBooks', selBooks)
    resp.set_cookie('past_searches', pastSearches)
    return resp

@app.route('/', methods=['GET'])
def index():
    for book in books:
        book['selected'] = True
    return dbRefresh("", versions[0]['name'], False, True, False)

@app.route('/result', methods=['GET'])
def search():
    inputWords  = request.args.get('keyword')
    versionName = request.args.get('version')
    return dbRefresh(inputWords, versionName, True)

@app.route('/case', methods=['GET'])
def caseFlip():
    return dbRefresh("", "", False, False, True)

@app.route('/testChoose/<test>', methods=['GET'])
def updateTestament(test):
    return dbRefresh("", "", False, False, False, "", test)

@app.route('/bookChoose', methods=['GET'])
def bookSelect():
    bkName  = request.args.get("book")
    for book in books:
        if book['text'] == bkName:
            return dbRefresh("", "", False, False, False, book['num'])

# utility_functions() incorporated from https://stackoverflow.com/a/42888467/6539635
@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))
    return dict(mdebug=print_in_console)

if __name__ == '__main__':
    app.run(debug=True)
