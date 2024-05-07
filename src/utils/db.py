import aiosqlite


async def init_db():
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS posts(
                    user_id INT,
                    message_id INT
        )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS user_lefts(
                        user_id INT,
                        count INT
        )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS user_messages_count(
                            user_id INT,
                            user_first_name STR,
                            count INT,
                            day INT,
                            week INT,
                            month INT
        )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS admins(
                                    user_id INT
                )""")

        await db.commit()


async def get_admins(user_id: int) -> list[int]:
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(
            "SELECT * FROM admins WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
    return result


async def add_admins(user_id: int) -> None:
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("INSERT INTO admins VALUES (?)", (user_id,))
        await db.commit()


async def del_admins(user_id: int) -> None:
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
        await db.commit()


async def get_clicked_user(user_id: int, message_id: int) -> bool:
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute(
            "SELECT * FROM posts WHERE user_id = ? AND message_id = ?",
            (user_id, message_id)
        ) as cursor:
            result = await cursor.fetchone()
    return result


async def add_clicked_user(user_id: int, message_id: int) -> None:
    async with aiosqlite.connect("database/database.db") as db:
        await db.execute("INSERT INTO posts VALUES (?, ?)", (user_id, message_id))
        await db.commit()


async def user_left_chat(user_id: int) -> int:
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT * FROM user_lefts WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            if not result:
                await db.execute("INSERT INTO user_lefts VALUES (?, ?)", (user_id, +1))
                result = 1
            else:
                await db.execute("UPDATE user_lefts SET count = ? WHERE user_id = ?", (result[1]+1, user_id))
                result = result[1]+1

            await db.commit()
    return result


async def get_user_left_count(user_id: int) -> int:
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT * FROM user_lefts WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
        return result


async def message_counter(user_id: int, user_first_name: str) -> None:
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT * FROM user_messages_count WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            if not result:
                await db.execute(
                    "INSERT INTO user_messages_count VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, user_first_name, 1, 1, 1, 1)
                )
            else:
                await db.execute(
                    "UPDATE user_messages_count SET user_first_name = ?, count = ?, day = ?, week =?, month = ? WHERE user_id = ?",
                    (user_first_name, result[2] + 1, result[3] + 1, result[4] + 1, result[5] + 1, user_id)
                )

        await db.commit()


async def get_messages_stat(period: str = None) -> list:
    async with aiosqlite.connect("database/database.db") as db:
        if period == "day":
            async with db.execute(
                "SELECT user_id, user_first_name, day FROM user_messages_count ORDER BY day DESC LIMIT 10"
            ) as cursor:
                result = await cursor.fetchall()
        elif period == "week":
            async with db.execute(
                "SELECT user_id, user_first_name, week FROM user_messages_count ORDER BY week DESC LIMIT 10"
            ) as cursor:
                result = await cursor.fetchall()
        elif period == "month":
            async with db.execute(
                "SELECT user_id, user_first_name, month FROM user_messages_count ORDER BY month DESC LIMIT 10"
            ) as cursor:
                result = await cursor.fetchall()
        else:
            async with db.execute(
                "SELECT user_id, user_first_name, count FROM user_messages_count ORDER BY count DESC LIMIT 10"
            ) as cursor:
                result = await cursor.fetchall()

    return result


async def get_me_messages_stat(user_id: int, period: str) -> list:
    async with aiosqlite.connect("database/database.db") as db:
        if period == "s_all":
            async with db.execute(
                "SELECT count FROM user_messages_count WHERE user_id = ?", (user_id,)
            ) as cursor:
                result = await cursor.fetchone()
        if period == "s_day":
            async with db.execute(
                "SELECT day FROM user_messages_count WHERE user_id = ?", (user_id,)
            ) as cursor:
                result = await cursor.fetchone()
        if period == "s_week":
            async with db.execute(
                "SELECT week FROM user_messages_count WHERE user_id = ?", (user_id,)
            ) as cursor:
                result = await cursor.fetchone()
        if period == "s_month":
            async with db.execute(
                "SELECT month FROM user_messages_count WHERE user_id = ?", (user_id,)
            ) as cursor:
                result = await cursor.fetchone()

    return result


async def cleanup_messages_count(period: str) -> None:
    async with aiosqlite.connect("database/database.db") as db:
        if period == "day":
            await db.execute("UPDATE user_messages_count SET day = 0")
        if period == "week":
            await db.execute("UPDATE user_messages_count SET week = 0")
        if period == "month":
            await db.execute("UPDATE user_messages_count SET month = 0")

        await db.commit()


async def get_random_users_at_post_reaction(post_id: int) -> list | bool:
    # 560403
    async with aiosqlite.connect("database/database.db") as db:
        async with db.execute("SELECT user_id FROM posts WHERE message_id = ?", (post_id,)) as cursor:
            result = await cursor.fetchall()
        if not result:
            return False
        return result
