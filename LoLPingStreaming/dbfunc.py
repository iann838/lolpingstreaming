import sqlite3


class Db:
    def getip(code):
        conn = sqlite3.connect('testerdata.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT ip FROM Servers WHERE code = ?", (code,))
            return c.fetchone()
        conn.commit()
        conn.close()

    def getcurrent():
        conn = sqlite3.connect('testerdata.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT * FROM Settings")
            return c.fetchall()[0]
        conn.commit()
        conn.close()

    def updatecurrent(code, topmost, startup):
        conn = sqlite3.connect('testerdata.db')
        c = conn.cursor()
        with conn:
            c.execute("UPDATE Settings SET currentcode=?, topmost=?, startup=?", (code, topmost, startup,))
        conn.commit()
        conn.close()

    def getpos():
        conn = sqlite3.connect('testerdata.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT x_pos, y_pos FROM Winpos WHERE ind=1")
            return c.fetchone()
        conn.commit()
        conn.close()

    def updatepos(x, y):
        conn = sqlite3.connect('testerdata.db')
        c = conn.cursor()
        with conn:
            c.execute("UPDATE Winpos SET x_pos=?, y_pos=? WHERE ind=1", (x,y))
        conn.commit()
        conn.close()

    def getminn():
        conn = sqlite3.connect('testerdata.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT minn FROM Winpos WHERE ind=1")
            return c.fetchone()[0]
        conn.commit()
        conn.close()

    def updateminn(isminn):
        conn = sqlite3.connect('testerdata.db')
        c = conn.cursor()
        with conn:
            c.execute("UPDATE Winpos SET minn=? WHERE ind=1", (isminn,))
        conn.commit()
        conn.close()


    def startup():
        conn = sqlite3.connect('testerdata.db')

        c = conn.cursor()

        c.execute("""CREATE TABLE Servers (
                    code integer,
                    ip text
                    )""")

        c.execute("""INSERT INTO Servers VALUES (131, '104.160.131.1')""")
        c.execute("""INSERT INTO Servers VALUES (136, '104.160.136.3')""")
        c.execute("""INSERT INTO Servers VALUES (156, '104.160.156.1')""")
        c.execute("""INSERT INTO Servers VALUES (141, '104.160.141.3')""")
        c.execute("""INSERT INTO Servers VALUES (142, '104.160.142.3')""")
        c.execute("""INSERT INTO Servers VALUES (152, '104.160.152.3')""")
        c.execute("""INSERT INTO Servers VALUES (73, '162.249.73.2')""")
        c.execute("""INSERT INTO Servers VALUES (128, '122.11.128.127')""")
        c.execute("""INSERT INTO Servers VALUES (250, '112.216.250.242')""")
        c.execute("""INSERT INTO Servers VALUES (254, '122.200.254.203')""")
        c.execute("""INSERT INTO Servers VALUES (165, '200.111.165.236')""")
        c.execute("""INSERT INTO Servers VALUES (132, '203.116.132.132')""")
        c.execute("""INSERT INTO Servers VALUES (138, '124.108.138.7')""")
        c.execute("""INSERT INTO Servers VALUES (107, '119.147.107.25')""")
        c.execute("""INSERT INTO Servers VALUES (117, '137.59.117.68')""")
        c.execute("""INSERT INTO Servers VALUES (122, '119.59.122.210')""")
        c.execute("""INSERT INTO Servers VALUES (32, '216.240.32.74')""")
        c.execute("""INSERT INTO Servers VALUES (111, '111.161.111.44')""")

        conn.commit()

        c.execute("""CREATE TABLE Winpos(
                    ind integer,
                    x_pos integer,
                    y_pos integer,
                    minn integer
                    )""")

        c.execute('INSERT INTO Winpos VALUES (1, 20, 20, 0)')

        conn.commit()

        c.execute("""CREATE TABLE Settings(
                    currentcode integer,
                    topmost integer,
                    startup integer
                    )""")

        c.execute("INSERT INTO Settings VALUES (131, 1, 0)")

        conn.commit()
        conn.close()

    def startcloudcache():
        conn = sqlite3.connect('clouddata.db')

        c = conn.cursor()

        c.execute("""CREATE TABLE Version (
                    current text,
                    lastsync text,
                    lastversioninfo text
                    )""")

        conn.commit()

        c.execute("""INSERT INTO Version VALUES ('1.0', '1.0', '.')""")

        conn.commit()

        c.execute("""CREATE TABLE Sync (
                    checked_date text,
                    next_check text
                    )""")


        c.execute("""INSERT INTO Sync VALUES ('.','.')""")
        conn.commit()
        conn.close()

    def getsync():
        conn = sqlite3.connect('clouddata.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT * FROM Sync")
            return c.fetchone()
        conn.commit()
        conn.close()

    def getversionsync():
        conn = sqlite3.connect('clouddata.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT * FROM Version")
            return c.fetchone()
        conn.commit()
        conn.close()

    def syncversioninfo(newversion, newpatchnote):
        conn = sqlite3.connect('clouddata.db')
        c = conn.cursor()
        with conn:
            c.execute("UPDATE Version SET lastsync=?, lastversioninfo=?", (newversion, newpatchnote))
        conn.commit()
        conn.close()

    def updatesyncdate(checked, tocheck):
        conn = sqlite3.connect('clouddata.db')
        c = conn.cursor()
        with conn:
            c.execute("UPDATE Sync SET checked_date=?, next_check=?", (checked, tocheck))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    Db.startcloudcache()
