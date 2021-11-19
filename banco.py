import sqlite3

def adicionar(vnome, vtipo):
    vsql = "INSERT INTO dados VALUES('"+vnome+"', '"+vtipo+"', '', '')"
    cursor.execute(vsql)
    banco.commit()

    banco.close()

banco = sqlite3.connect("movies-plan.db", timeout=10)
cursor = banco.cursor()