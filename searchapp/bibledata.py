testaments = ["Old Testament", "New Testament"]

testament_map = {
    "ot": ["Old Testament"],
    "nt": ["New Testament"],
    "bib": ["Old Testament", "New Testament"],
}

versions = [
    {
        "name": "ESV",
        "expansion": "English Standard Version",
        "wiki": "https://en.wikipedia.org/wiki/English_Standard_Version",
    },
    {
        "name": "KJV",
        "expansion": "King James Version",
        "wiki": "https://en.wikipedia.org/wiki/King_James_Version",
    },
    {
        "name": "NKJV",
        "expansion": "New King James Version",
        "wiki": "https://en.wikipedia.org/wiki/New_King_James_Version",
    },
    {
        "name": "NASB",
        "expansion": "New American Standard Bible",
        "wiki": "https://en.wikipedia.org/wiki/New_American_Standard_Bible",
    },
    {
        "name": "AMP",
        "expansion": "Amplified Bible",
        "wiki": "https://en.wikipedia.org/wiki/Amplified_Bible",
    },
    {
        "name": "ASV",
        "expansion": "American Standard Version",
        "wiki": "https://en.wikipedia.org/wiki/American_Standard_Version",
    },
    {
        "name": "YLT",
        "expansion": "Young's Literal Translation",
        "wiki": "https://en.wikipedia.org/wiki/Young%27s_Literal_Translation",
    },
    {
        "name": "BBE",
        "expansion": "Bible in Basic English",
        "wiki": "https://en.wikipedia.org/wiki/Bible_in_Basic_English",
    },
    {
        "name": "DBY",
        "expansion": "Darby Bible",
        "wiki": "https://en.wikipedia.org/wiki/Darby_Bible",
    },
    {
        "name": "WEB",
        "expansion": "World English Bible",
        "wiki": "https://en.wikipedia.org/wiki/World_English_Bible",
    },
    {
        "name": "BSB",
        "expansion": "Berean Study Bible",
        "wiki": "https://www.bereanbible.com/",
    },
    {
        "name": "AKJV",
        "expansion": "Authorized King James Version",
        "wiki": "https://en.wikipedia.org/wiki/King_James_Version",
    },
    {
        "name": "UKJV",
        "expansion": "Updated King James Version",
        "wiki": "https://en.wikipedia.org/wiki/King_James_Version",
    },
    {
        "name": "WBT",
        "expansion": "Webster's Bible Translation",
        "wiki": "https://en.wikipedia.org/wiki/Webster%27s_Revision",
    },
    {
        "name": "GEN",
        "expansion": "Geneva Bible",
        "wiki": "https://en.wikipedia.org/wiki/Geneva_Bible",
    },
]

books = [
    {"id": i, "num": f"{i:02}", "text": name, "testament": test}
    for i, (name, test) in enumerate(
        [
            # Old Testament
            ("Genesis", "Old Testament"),
            ("Exodus", "Old Testament"),
            ("Leviticus", "Old Testament"),
            ("Numbers", "Old Testament"),
            ("Deuteronomy", "Old Testament"),
            ("Joshua", "Old Testament"),
            ("Judges", "Old Testament"),
            ("Ruth", "Old Testament"),
            ("1 Samuel", "Old Testament"),
            ("2 Samuel", "Old Testament"),
            ("1 Kings", "Old Testament"),
            ("2 Kings", "Old Testament"),
            ("1 Chronicles", "Old Testament"),
            ("2 Chronicles", "Old Testament"),
            ("Ezra", "Old Testament"),
            ("Nehemiah", "Old Testament"),
            ("Esther", "Old Testament"),
            ("Job", "Old Testament"),
            ("Psalms", "Old Testament"),
            ("Proverbs", "Old Testament"),
            ("Ecclesiastes", "Old Testament"),
            ("Song of Solomon", "Old Testament"),
            ("Isaiah", "Old Testament"),
            ("Jeremiah", "Old Testament"),
            ("Lamentations", "Old Testament"),
            ("Ezekiel", "Old Testament"),
            ("Daniel", "Old Testament"),
            ("Hosea", "Old Testament"),
            ("Joel", "Old Testament"),
            ("Amos", "Old Testament"),
            ("Obadiah", "Old Testament"),
            ("Jonah", "Old Testament"),
            ("Micah", "Old Testament"),
            ("Nahum", "Old Testament"),
            ("Habakkuk", "Old Testament"),
            ("Zephaniah", "Old Testament"),
            ("Haggai", "Old Testament"),
            ("Zechariah", "Old Testament"),
            ("Malachi", "Old Testament"),
            # New Testament
            ("Matthew", "New Testament"),
            ("Mark", "New Testament"),
            ("Luke", "New Testament"),
            ("John", "New Testament"),
            ("Acts", "New Testament"),
            ("Romans", "New Testament"),
            ("1 Corinthians", "New Testament"),
            ("2 Corinthians", "New Testament"),
            ("Galatians", "New Testament"),
            ("Ephesians", "New Testament"),
            ("Philippians", "New Testament"),
            ("Colossians", "New Testament"),
            ("1 Thessalonians", "New Testament"),
            ("2 Thessalonians", "New Testament"),
            ("1 Timothy", "New Testament"),
            ("2 Timothy", "New Testament"),
            ("Titus", "New Testament"),
            ("Philemon", "New Testament"),
            ("Hebrews", "New Testament"),
            ("James", "New Testament"),
            ("1 Peter", "New Testament"),
            ("2 Peter", "New Testament"),
            ("1 John", "New Testament"),
            ("2 John", "New Testament"),
            ("3 John", "New Testament"),
            ("Jude", "New Testament"),
            ("Revelation", "New Testament"),
        ]
    )
]

sql_select = "SELECT * FROM bible WHERE "
sql_order = "ORDER BY Book, Chapter, Versecount"
