"""
Connecting a Python application to a database with SQLAlchemy.

The examples use MariaDB.

Every application that talks to a database must:
1. Use a library that can communicate with databases from your language (here, SQLAlchemy for Python).
2. Have a driver that knows how to talk to a specific database server (here, a MariaDB/MySQL driver).
3. Establish a connection. A connection needs the same information you give DBeaver:
       username, password, host (localhost or 127.0.0.1), port (3306), and database name.
   Tip: DBeaver shows its drivers under Database -> Driver Manager.
Then the application can:
4. Make requests of the database (run SQL) and work with the results.
"""
import configparser

# ---------------------------------------------------------------------------
# Install the packages
# ---------------------------------------------------------------------------
# Packages are installed once per project (virtual environment), not in the code.
#
# We need to add the following packages:
#
# PyCharm Package Manager (preferred):
#   Left Click the interpreter label in the lower right of the PyCharm window
#   (for example "venv [Python 3.x]"), then click Manage Packages. See Fig. 1
#   Search for each package below and install the latest version.
#   (See the figures in the accompanying documentation.)  See Fig. 2
#       sqlalchemy
#       pymysql
#       mariadb
#
# Terminal (same result):
#   Left click on the "Hamburger" Menu and then go to View->Tool Windows->Terminal and Left Click See.Fig 3
#   pip install sqlalchemy pymysql
#
#   sqlalchemy - the library that builds and runs database requests
#   pymysql    - the driver that speaks to MariaDB/MySQL servers
#
# Standard-library modules such as getpass and sqlite3 come with Python and are
# never installed with pip.
#
# Using the MariaDB native connector
#   pip install mariadb  (this needs the MariaDB C connector on your computer first)
#   then change DRIVER below to "mariadb+mariadbconnector".

# ---------------------------------------------------------------------------
# Section 2 - Imports
# ---------------------------------------------------------------------------
# "from X import Y" and "import X" both work with any module, whether it ships
# with Python or was installed with pip. The only difference is how you name
# things afterward:
#     from getpass import getpass   ->  getpass("Password: ")
#     import getpass                ->  getpass.getpass("Password: ")
from sqlalchemy import create_engine, text, TextClause
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError, ProgrammingError



# create_engine - creates the engine that manages connections to the database
# text          - marks a string as SQL so the engine can send it to the database
# URL           - builds the connection information from separate named pieces
# OperationalError / ProgrammingError - errors we expect to see in this lesson
#     (can't connect / bad SQL such as a misspelled table name)


def main():
    print("Start database connection test")

    # -----------------------------------------------------------------------
    # Section 3 - Define the connection
    # -----------------------------------------------------------------------
    # Never type a password into your code: code gets shared, emailed, and
    # uploaded. getpass() asks for it when the program runs and does not echo it.

    # Initialize parser and read the file
    config = configparser.RawConfigParser()
    config.read('config.ini',encoding='utf-8')

    # Access credentials
    USERNAME = config.get('credentials', 'username')
    password = config.get('credentials', 'password')


    print(f"Username: {USERNAME}, Password: {password}")


    DRIVER = "mariadb+pymysql" # the database type + the driver
    #USERNAME = "root"  # in class we use root; real applications use a limited account
    HOST = "localhost"  # check your connection settings in DBeaver to confirm host and port
    PORT = 3306
    DATABASE = "scrabbledb"


    # URL.create has one argument for each field in DBeaver's connection dialog.
    # It also handles special characters in the password (like @), so you do
    # not have to escape anything yourself.
    database_url = URL.create(
        DRIVER,
        username=USERNAME,
        password=password,
        host=HOST,
        port=PORT,
        database=DATABASE,
    )

    # The engine holds the connection information. It does not connect yet.
    # echo=True prints every SQL statement the engine sends, which is useful for
    # comparing against what DBeaver runs. Start with False so the output is easy
    # to read, then switch it to True and run again.
    engine = create_engine(database_url, echo=False)

    minimum_score = input("Enter the lowest winner score: ")
    if minimum_score.isnumeric():
        minimum_score = int(minimum_score)
    else:
        minimum_score = 0

    # -----------------------------------------------------------------------
    # Section 4 - Connect and run a query
    # -----------------------------------------------------------------------
    # Try this first: run the program as is. Then break it on purpose by
    # changing the password, port, host, or database name and read the error.
    # For example, a wrong port produces something like:
    #   sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
    #   (2003, "Can't connect to MySQL server on 'localhost'")
    try:
        # "with" opens the connection and guarantees it is closed when the
        # indented block ends, even if an error happens.
        with engine.connect() as connection:
            print("Successfully connected to MariaDB!")


            # Retrieve all games where the winning score is at least some value.
            # :minimum_winnerscore is a placeholder. The value is passed separately, so
            # it is always treated as data and never as SQL. This is what
            # protects an application from SQL injection. Never build SQL by
            # gluing user input into the string.
            statement = text(
                "SELECT gameid, tourneyid, winnerSysId, loserSysId, winnerscore, loserscore "
                "FROM scrabble_games_initial "
                "WHERE winnerscore >= :minimum_winnerscore Limit 2"
            )

            # The print statement is useful so we can copy the generated SQL Select command from the Condole area
            # and paste it into a SQL Console panel in DBeaver, in order to test the statement.
            print(statement)
            # The second argument supplies the placeholder values as a dictionary.
            result = connection.execute(statement, {"minimum_winnerscore": minimum_score})

            for row in result:
                print(
                    f"{row.gameid}, {row.tourneyid}, {row.winnerSysId}, {row.winnerscore}, "
                    f"{row.loserSysId}, {row.loserscore}"
                )

            # Running the second query to include the winners and losers names
            statement = text(
                "SELECT gameid, tourneyid, winnerSysId, loserSysId, winnerscore, loserscore, "
                " p1.FullName as WinnerName, p2.FullName as LoserName "
                "FROM scrabble_games_initial sgi Join Person p1 on sgi.winnerSysId = p1.id "
                "Join Person p2 on sgi.loserSysId = p2.id "
                "WHERE winnerscore >= :minimum_winnerscore LIMIT 5"
            )

            print(statement)
            print("\n")

            print("GameID, TourneyID, WinnerName, LoserName, WinnerScore, LoserScore\n")
            # The second argument supplies the placeholder values as a dictionary.
            result = connection.execute(statement, {"minimum_winnerscore": minimum_score})

            # Each row lets you read columns by name.
            for row in result:
                print(
                    f"{row.gameid}, {row.tourneyid}, {row.WinnerName}, {row.LoserName}, {row.winnerscore}, {row.loserscore}"
                )

                ans = input(f"Want a rematch between {row.WinnerName} and {row.LoserName} (Y/N)?")
                if ans.upper() == "Y":
                    statement = text("Insert into matches (PlayerA_Id, PlayerB_Id) values (:playerA, :playerB)")
                    result = connection.execute(statement, {"playerA": {row.winnerSysId}, "playerB": {row.loserSysId}})
                    connection.commit()
                    print(result)

                print("\n")



    except OperationalError as e:
        # Could not connect: wrong credentials, host, port, or the server is not running.
        print(f"Connection error: {e}")
    except ProgrammingError as e:
        # Connected, but the SQL was rejected: misspelled table or column name, etc.
        print(f"SQL error: {e}")

    print("End database connection test")



# This line means "run main() only when this file is run directly".
# Without it, importing this file from another program would also run the test.
if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# Section 5 (optional) - The same idea with SQLite
# ---------------------------------------------------------------------------
# SQLite has no server, username, password, host, or port. The "database" is a
# single file, so the only thing that changes is the URL. Python includes SQLite
# support, so there is nothing to install.
#
#     engine = create_engine("sqlite:///scrabble.db", echo=False)
#
# Everything after that (connect, text(), execute, loop over the rows) is
# exactly the same code. That is the point of using SQLAlchemy: one way of
# working, many databases.
