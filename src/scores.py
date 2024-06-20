import pymysql

# 创建成绩
def add_score(db, cursor, sID, cID, Score):
    sql = "INSERT INTO Scores (StudentID, ClassID, Score) VALUES (%s, %s, %s)"
    try:
        cursor.execute(sql, (sID, cID, Score))
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return


# 删除成绩
def delete_score(db, cursor, sID, cID):
    sql = "DELETE FROM Scores WHERE StudentID = %s AND ClassID = %s"
    try:
        cursor.execute(sql, (sID, cID))
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return


# 查询已获得总学分
def get_total_points(db, cursor, ID):
    sql = "SELECT GetTotalPoints(%s) as TotalCredits"
    try:
        cursor.execute(sql, (ID, ))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"发生错误：{e}")
        return

def get_avg_points(db, cursor, ID):
    sql = ("SELECT GetAvgPoints(%s) as AvgCredits")
    try:
        cursor.execute(sql, (ID, ))
        result = cursor.fetchone()

        return result
    except Exception as e:
        print(f"发生错误：{e}")
        return


def get_points(db, cursor, ID):
    sql = ("SELECT GetPoints(%s) as Credits")
    try:
        cursor.execute(sql, (ID, ))
        result = cursor.fetchone()

        return result
    except Exception as e:
        print(f"发生错误：{e}")
        return