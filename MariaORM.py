import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, CHAR,Table, Column, Integer, String
from sqlalchemy import Named, TypedColumns
from typing import List
from typing import Optional
from sqlalchemy.sql import select, func
import urllib.parse

other_meta = MetaData()

class Base(DeclarativeBase):
    pass

class ScrabbleView(Base):
    __tablename__ = "scrabble_games_initial"
    id: Mapped[int] = mapped_column(primary_key=True)
    winnername: Mapped[str] = mapped_column(String(50))
    losername: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"ScrabbleView(id={self.id!r}, winnername={self.winnername!r}, losername={self.losername!r})"

class user_cols(TypedColumns):
    id: Named[int] = Column (primary_key=True)
    winnername: Named[str|None] = Column (String(50))
    losername: Named[str|None] = Column (String(50))


def testConnection():
    # Format: mariadb+mariadbconnector://<user>:<password>@<host>:<port>/<db_name>
    # To simulate the connection at Columbia using a testcol username along with
    # the L30n@rd0Blu3 password
    # But since the L30n@rd0Blu3 has special characters we need to encode it.
    username = "testcol"
    password = urllib.parse.quote_plus("L30n@rd0Blu3")


    metadata = MetaData()




    sv = ScrabbleView(id=59, winnername=59, losername=59)

    scrabble_games_initial = Table(
        "scrabble_games_initial",
        metadata,
        Column("gameid", Integer),
        Column("tourneyid", Integer),
        Column("tie", CHAR(6)),
        Column("winnerid", Integer),
        Column("winnername", String(50)),
        Column("winnerscore", Integer),
        Column("winneroldrating", Integer),
        Column("winnernewrating", Integer),
        Column("winnerpos", Integer),
        Column("loserid", Integer),
        Column("losername", String(50)),
        Column("loserscore", Integer),
        Column("loseroldrating", Integer),
        Column("losernewrating", Integer),
        Column("loserpos", Integer),
        Column("round", Integer),
        Column("division", Integer),
        Column("date", String(50)),
        Column("lexicon", CHAR(6)),
        Column("Id", Integer, primary_key=True, autoincrement=True, nullable=False),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_uca1400_ai_ci",
    )

    #password = "L30n@rd0Blu3"
    database = "scrabbledb"
    DATABASE_URL = f"mariadb+mariadbconnector://{username}:{password}@localhost:3306/{database}"
    engine = create_engine(DATABASE_URL, echo=True)

    reflecView = Table("scrabble_games_initial", metadata, autoload=engine)
    typed_user_table = Table("scrabble_games_initial", other_meta, user_cols)
    stmt = text("select * from scrabble_games_initial where winnerid = :winnerid")

    metadata.create_all(engine)



    with Session(engine) as session:


        # Select all rows
        s1 = select(scrabble_games_initial.c.gameid, scrabble_games_initial.c.winnername)
        s1 = s1.where(scrabble_games_initial.c.gameid != None)
        s1 = s1.order_by(scrabble_games_initial.c.gameid)
        s1 = s1.limit(5)
        rows = session.execute(s1)

        s2 = select(func.min(scrabble_games_initial.c.winnerscore))
        rp2 = session.execute(s2)
        print(rp2.scalar())

        for row in rows:
            # print(f"{row.gameid}, {row.tourneyid}, {row.winnername}, {row.losername},{row.winnerscore},{row.loserscore} ")
            print(f"{row.gameid}, {row.winnername}")

        # INSERT ... SELECT
        #stmt = insert(target_table).from_select(
        #    ["gameid", "winnername"],
        #    select(scrabble_games_initial.c.gameid, scrabble_games_initial.c.winnername),
        #)

        # IN with a subquery
        #stmt = select(other).where(other.c.gameid.in_(select(scrabble_games_initial.c.gameid)))

        result = session.execute(stmt, {"winnerid": 59})
        ins = typed_user_table.insert().values(
            winnername="Test",
            losername="TestLoser"

        )
        print(str(ins))
        result = session.execute(ins)
        session.commit()
        print(str(result))

        # altstmt = select(reflecView).filter_by(reflecView.columns.winnerscore >= 59)

        #result = session.execute(altstmt)
        #objs = session.scalars(altstmt).all()

        #stmt2 = select(scrabble_games_initial.gameid,scrabble_games_initial.winnername);

        #rows = session.execute(stmt2).fetchall()

        #for row in rows:
        #   print(f"{row.gameid},{row.winnername}")


        #for row in result:
        #   print(f"{row.gameid}, {row.tourneyid}, {row.winnername}, {row.losername},{row.winnerscore},{row.loserscore} ")


    # Test the connectionZ
    '''
    with engine.connect() as connection:
        print("Successfully connected to MariaDB via native connector!")
        for row in connection.execute(text("select * from scrabble_games_initial where winnerid = :winnerid"), {"winnerid": 59}):
            print(f"{row.gameid}, {row.tourneyid}, {row.winnername}, {row.losername},{row.winnerscore},{row.loserscore} ")
    '''




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')
    testConnection()
