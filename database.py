import sqlite3

def delete_movie_from_list(user_id):
    conn = sqlite3.connect('movie_bot.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()