import pymysql


# 初始化表格
def init(db, cursor):
    sql = """
        DROP TABLE IF EXISTS users
        """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    # 删除表
    sql = """
    DROP TABLE IF EXISTS Scores
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    sql = """
    DROP TABLE IF EXISTS Punishtime
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    sql = """
    DROP TABLE IF EXISTS Prizetime
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    sql = """
    DROP TABLE IF EXISTS Students 
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    sql = """
    DROP TABLE IF EXISTS Classes
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return




    # 创建表
    sql = """
        CREATE TABLE users (
    username CHAR(10),
	password CHAR(64)
);


ALTER TABLE users
ADD PRIMARY KEY (username);
        """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

    sql = """
    CREATE TABLE Students (
    StudentID CHAR(10),
    Name VARCHAR(64) NOT NULL,
    Age INT NOT NULL,
    Major VARCHAR(64) NOT NULL,
    Photo LONGBLOB,
    PRIMARY KEY (StudentID)
    )
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

    sql = """
    CREATE TABLE Classes (
    ClassID CHAR(10),
    Name VARCHAR(64) NOT NULL,
    Point INT NOT NULL,
    PRIMARY KEY (ClassID)
    )
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

    sql = """
    CREATE TABLE Scores (
    StudentID CHAR(10),
    ClassID CHAR(10),
    Score INT,
    PRIMARY KEY (StudentID, ClassID),
    CONSTRAINT Scores_sforeign FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    CONSTRAINT Scores_cforeign FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
    )
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

    sql = """
    CREATE TABLE Punishtime (
    StudentID CHAR(10),
    PunishName VARCHAR(64) NOT NULL,
    Date DATE,
    PRIMARY KEY (StudentID, PunishName),
    CONSTRAINT Punishtime_sforeign FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
    )
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

    sql = """
    CREATE TABLE Prizetime (
    StudentID CHAR(10),
    PrizeName VARCHAR(64) NOT NULL,
    Date DATE,
    PRIMARY KEY (StudentID, PrizeName),
    CONSTRAINT Prizetime_sforeign FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
    )
    """
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return









    # 存储过程：修改学号
    sql = "DROP PROCEDURE IF EXISTS updateStudentID"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
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
        return


    # 存储过程：修改课程号
    sql = "DROP PROCEDURE IF EXISTS updateClassID"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
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
        return

    sql = "DROP Function IF EXISTS GetTotalPoints"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return
    sql = "DROP Function IF EXISTS GetAvgPoints"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

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
        return

    #函数 统计总学分
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
        return



    # 触发器：删除学生，课程时自动删除相关成绩
    sql = "DROP TRIGGER IF EXISTS trg_delete_student"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

    # 触发器 删除
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
        return

    sql = "DROP TRIGGER IF EXISTS trg_delete_class"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(f"发生错误：{e}")
        db.rollback()
        return

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
        return
