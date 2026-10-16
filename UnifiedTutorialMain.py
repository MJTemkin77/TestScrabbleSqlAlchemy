from sqlalchemy import create_engine, text
engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
# Using a Python context manager aka the with statement
with engine.connect() as conn:
#with engine.begin() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

    # Create Table and insert data
    conn.execute(text("create table some_table(x int, y int)"))
    conn.execute(text("insert into some_table (x,y) values (:x,:y)"),
                 [{"x": 3, "y": 5}, {"x": 7, "y": 2}])
    conn.commit()

    result = conn.execute(text("select * from some_table"))
    print("By integer index")
    for row in result:
        print(f"x:{row[0]}, y:{row[1]}")
    print("By tuple assignment")
    result = conn.execute(text("select * from some_table"))
    for x,y in result:
        print(f"x:{x}, y:{y}")
    print("By attribute name")
    result = conn.execute(text("select * from some_table"))
    for row in result:
        print(f"x:{row.x}, y:{row.y}")

    print("By mapping")
    result = conn.execute(text("select x, y from some_table"))

    for dict_row in result.mappings():
        x = dict_row["x"]
        y = dict_row["y"]
        print(f"x:{x}, y:{y}")