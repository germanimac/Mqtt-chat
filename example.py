import sqlite3

con = sqlite3.connect("memory.db")
cur = con.cursor()
cur.execute("create table lang (name, first_appeared)")

# This is the qmark style:
cur.execute("insert into lang values (?, ?)", ("C", 1972))

# The qmark style used with executemany():
lang_list = [
    ("Fortran", 1957),
    ("Python", 1991),
    ("Go", 2009),
]
cur.executemany("insert into lang values (?, ?)", lang_list)
n=1991*2
n=n/2
nam = "Python"
# And this is the named style:
cur.execute("select * from lang where first_appeared=:year and name=:nam", {"year":n,"nam":nam})
print(cur.fetchall())

con.close()