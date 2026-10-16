from sqlalchemy import create_engine, text, MetaData
from sqlalchemy import Table, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, CheckConstraint
from datetime import datetime
from sqlalchemy import DateTime



import urllib.parse

def testConnection():
    # Format: mariadb+mariadbconnector://<user>:<password>@<host>:<port>/<db_name>
    # To simulate the connection at Columbia using a testcol username along with
    # the L30n@rd0Blu3 password
    # But since the L30n@rd0Blu3 has special characters we need to encode it.
    username = "testcol"
    password = urllib.parse.quote_plus("L30n@rd0Blu3")
    #password = "L30n@rd0Blu3"
    database = "scrabbledb"
    DATABASE_URL = f"mariadb+mariadbconnector://{username}:{password}@localhost:3306/{database}"
    engine = create_engine(DATABASE_URL, echo=True)


    # Test the connectionZ
    with engine.connect() as connection:
        print("Successfully connected to MariaDB via native connector!")
        for row in connection.execute(text("select * from scrabble_games_initial where winnerid = :winnerid"), {"winnerid": 59}):
            print(f"{row.gameid}, {row.tourneyid}, {row.winnername}, {row.losername},{row.winnerscore},{row.loserscore} ")





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')
    testConnection()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
