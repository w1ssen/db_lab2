import pymysql


def add_punishtime(db, cursor, sID, name, date):
    sql = "INSERT INTO Punishtime (StudentID, PunishName, Date) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql, (sID, name, date)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return


def delete_punishtime(db, cursor, sID, name):
    sql = "DELETE FROM Punishtime WHERE StudentID = %s AND PunishName = %s"
    try:
        cursor.execute(sql, (sID, name)) 
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return