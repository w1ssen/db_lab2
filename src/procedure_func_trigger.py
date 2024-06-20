import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="Zw335024@",
    database="lab2"
)
cursor = db.cursor()

# 存储过程：修改ID的同时修改其他表
sql = "DROP PROCEDURE IF EXISTS updateStudentID"
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

sql = """
    CREATE PROCEDURE updateStudentID(IN old_id CHAR(10), IN new_id CHAR(10))
    BEGIN
        ALTER TABLE Scores
        DROP FOREIGN KEY Scores_sforeign;

        UPDATE Scores
        SET StudentID = new_id
        WHERE StudentID = old_id;

        ALTER TABLE Punishtime
        DROP FOREIGN KEY Punishtime_sforeign;

        UPDATE Punishtime
        SET StudentID = new_id
        WHERE StudentID = old_id;

        ALTER TABLE Prizetime
        DROP FOREIGN KEY Prizetime_sforeign;

        UPDATE Prizetime
        SET StudentID = new_id
        WHERE StudentID = old_id;

        UPDATE Students
        SET StudentID = new_id
        WHERE StudentID = old_id;

        UPDATE users
        SET password = new_id
        WHERE username = old_id;

        UPDATE users
        SET username = new_id
        WHERE username = old_id;

        ALTER TABLE Scores
        ADD CONSTRAINT Scores_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);

        ALTER TABLE Punishtime
        ADD CONSTRAINT Punishtime_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);

        ALTER TABLE Prizetime
        ADD CONSTRAINT Prizetime_sforeign FOREIGN KEY (StudentID) REFERENCES Students (StudentID);
    END
    """
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()


sql = "DROP PROCEDURE IF EXISTS updateClassID"
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

sql = """
    CREATE PROCEDURE updateClassID(IN old_id CHAR(10), IN new_id CHAR(10))
    BEGIN
        ALTER TABLE Scores
        DROP FOREIGN KEY Scores_cforeign;

        UPDATE Scores
        SET ClassID = new_id
        WHERE ClassID = old_id;

        UPDATE Classes
        SET ClassID = new_id
        WHERE ClassID = old_id;

        ALTER TABLE Scores
        ADD CONSTRAINT Scores_cforeign FOREIGN KEY (ClassID) REFERENCES Classes (ClassID);

    END
    """
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

sql = "DROP Function IF EXISTS GetTotalPoints"
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

sql = "DROP Function IF EXISTS GetAvgPoints"
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

# 函数 统计平均分
sql = """
    CREATE FUNCTION GetAvgPoints(student_id CHAR(10)) 
    RETURNS FLOAT
    DETERMINISTIC
    BEGIN
        DECLARE avg_grade FLOAT;

        SELECT AVG(score) INTO avg_grade
        FROM Scores
        WHERE student_id = StudentID;

        RETURN avg_grade;
    END 
    """
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()


sql = """
    CREATE FUNCTION GetTotalPoints (student_id CHAR(10)) RETURNS INT
    DETERMINISTIC
    BEGIN
        DECLARE total_points INT;
        SELECT SUM(Classes.Point) INTO total_points
        FROM Classes
        WHERE ClassID IN (SELECT ClassID FROM Scores WHERE Scores.StudentID = student_id);
        RETURN total_points;
    END
    """
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

# 触发器：删除学生，课程，惩罚，奖项时自动删除相关成绩，日期
sql = "DROP TRIGGER IF EXISTS trg_delete_student"
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

# 触发器 删除所有表中的相关项
sql = """
    CREATE TRIGGER trg_delete_student
    BEFORE DELETE ON Students
    FOR EACH ROW
    BEGIN
        SELECT COUNT(*) INTO @count FROM Scores WHERE StudentID = OLD.StudentID;

        IF @count > 0 THEN
            DELETE FROM Scores WHERE StudentID = OLD.StudentID;
        END IF;

        SELECT COUNT(*) INTO @count FROM Punishtime WHERE StudentID = OLD.StudentID;

        IF @count > 0 THEN
            DELETE FROM Punishtime WHERE StudentID = OLD.StudentID;
        END IF;

        SELECT COUNT(*) INTO @count FROM Prizetime WHERE StudentID = OLD.StudentID;

        IF @count > 0 THEN
            DELETE FROM Prizetime WHERE StudentID = OLD.StudentID;
        END IF;
    END
    """
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

sql = "DROP TRIGGER IF EXISTS trg_delete_class"
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()

sql = """
    CREATE TRIGGER trg_delete_class
    BEFORE DELETE ON Classes
    FOR EACH ROW
    BEGIN
        SELECT COUNT(*) INTO @count FROM Scores WHERE ClassID = OLD.ClassID;

        IF @count > 0 THEN
            DELETE FROM Scores WHERE ClassID = OLD.ClassID;
        END IF;
    END
    """
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print(f"发生错误：{e}")
    db.rollback()
