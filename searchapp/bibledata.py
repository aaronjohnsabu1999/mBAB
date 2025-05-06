sections = ["OT1", "OT2", "NT1", "NT2"]

testament_map = {
    "ot": ["OT1", "OT2"],
    "nt": ["NT1", "NT2"],
    "bib": ["OT1", "OT2", "NT1", "NT2"],
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
            ("Genesis", "OT1"),
            ("Exodus", "OT1"),
            ("Leviticus", "OT1"),
            ("Numbers", "OT1"),
            ("Deuteronomy", "OT1"),
            ("Joshua", "OT1"),
            ("Judges", "OT1"),
            ("Ruth", "OT1"),
            ("1 Samuel", "OT1"),
            ("2 Samuel", "OT1"),
            ("1 Kings", "OT1"),
            ("2 Kings", "OT1"),
            ("1 Chronicles", "OT1"),
            ("2 Chronicles", "OT1"),
            ("Ezra", "OT1"),
            ("Nehemiah", "OT1"),
            ("Esther", "OT1"),
            ("Job", "OT1"),
            ("Psalms", "OT1"),
            ("Proverbs", "OT2"),
            ("Ecclesiastes", "OT2"),
            ("Song of Solomon", "OT2"),
            ("Isaiah", "OT2"),
            ("Jeremiah", "OT2"),
            ("Lamentations", "OT2"),
            ("Ezekiel", "OT2"),
            ("Daniel", "OT2"),
            ("Hosea", "OT2"),
            ("Joel", "OT2"),
            ("Amos", "OT2"),
            ("Obadiah", "OT2"),
            ("Jonah", "OT2"),
            ("Micah", "OT2"),
            ("Nahum", "OT2"),
            ("Habakkuk", "OT2"),
            ("Zephaniah", "OT2"),
            ("Haggai", "OT2"),
            ("Zechariah", "OT2"),
            ("Malachi", "OT2"),
            # New Testament
            ("Matthew", "NT1"),
            ("Mark", "NT1"),
            ("Luke", "NT1"),
            ("John", "NT1"),
            ("Acts", "NT1"),
            ("Romans", "NT1"),
            ("1 Corinthians", "NT1"),
            ("2 Corinthians", "NT1"),
            ("Galatians", "NT1"),
            ("Ephesians", "NT1"),
            ("Philippians", "NT1"),
            ("Colossians", "NT1"),
            ("1 Thessalonians", "NT1"),
            ("2 Thessalonians", "NT2"),
            ("1 Timothy", "NT2"),
            ("2 Timothy", "NT2"),
            ("Titus", "NT2"),
            ("Philemon", "NT2"),
            ("Hebrews", "NT2"),
            ("James", "NT2"),
            ("1 Peter", "NT2"),
            ("2 Peter", "NT2"),
            ("1 John", "NT2"),
            ("2 John", "NT2"),
            ("3 John", "NT2"),
            ("Jude", "NT2"),
            ("Revelation", "NT2"),
        ]
    )
]

sql_select = "SELECT * FROM bible WHERE "
sql_order = "ORDER BY Book, Chapter, Versecount"
