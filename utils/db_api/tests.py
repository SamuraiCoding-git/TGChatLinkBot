from utils.db_api.sqlite import Database


def test():
    db = Database()
    db.create_table_users()
    db.add_user(1, "One", "email")
    db.add_user(2, "Vasya", "vv@gmail.com")
    db.add_user(3, 1, 1)
    db.add_user(4, 1, 1)
    db.add_user(5, "John", "john@mail.com")

    users = db.select_all_users()
    print(f"Получил всех пользователей: {users}")

    user = db.select_user(Name="John", id=5)
    print(f"Получил пользователя: {user}")

    users = db.select_all_users()
    print(f"Получил всех пользователей: {users}")


test()
