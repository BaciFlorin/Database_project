import cx_Oracle
import logging
import traceback, sys

#logger
logger = logging.getLogger("gui_log")

# global variables
movie_id = 1
user_id = 2
director_id = 3
actor_id = 4

# database variables
def connect():
    global cursor
    dsn_tns = cx_Oracle.makedsn('127.0.0.1', 1521, service_name='XE')
    print("Introduceti user-ul si parola bazei de date de pe acest computer:")
    user = input("user=")
    password = input("password=")
    try:
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
        cursor = conn.cursor()
    except:
        print("Parola sau user gresit")
        exit(-1)

def initialize_database():
    try:
        cursor.execute("select * from accounts")
    except:
        f = open('scriptCreareTabele.sql')
        full_sql = f.read()
        sql_commands = ((full_sql.replace("\n", "")).replace("\t", "")).split(';')
        for sql_command in sql_commands:
            if sql_command[0:2] != "--" and sql_command != "":
                cursor.execute(sql_command)

        f = open('populareTabele.sql')
        full_sql = f.read()
        sql_commands = ((full_sql.replace("\n", "")).replace("\t", "")).split(';')
        for sql_command in sql_commands:
            if sql_command[0:2] != "--" and sql_command != "":
                cursor.execute(sql_command)
                commit()

def delete_database():
    f = open('stergeTabele.sql')
    full_sql = f.read()
    sql_commands = ((full_sql.replace("\n", "")).replace("\t", "")).split(';')
    for sql_command in sql_commands:
        if sql_command[0:2] != "--" and sql_command != "":
            cursor.execute(sql_command)
            commit()

# functions for user's table
def check_if_user_in_database(user, password):
    logger.info("Cauta pe " + user + "!")
    cursor.execute("select username, password from accounts where username='" + user + "' and password='" + password + "'")
    val = cursor.fetchall()
    if val == []:
        return False
    else:
        return True


def check_if_user_exist(user):
    logger.info("Cauta pe " + user + "!")
    cursor.execute("select username " +
                   "from accounts " +
                   "where username='" + user + "'")
    if cursor.fetchall() == []:
        return False
    else:
        return True


def get_user_id(user):
    cursor.execute("select id_user " +
                   "from accounts " +
                   "where username='" + user + "'")
    result = cursor.fetchall()
    return int(result[0][0])


def add_user_in_datase(user, password):
    logger.info("Adauga cont: " + user + "!")
    global user_id
    try:
        cursor.execute("insert into accounts values(" + str(get_next_indice(user_id)) + ", '" + user + "', '" + password + "')")
    except cx_Oracle.DatabaseError:
        logger.info("Campuri incorect completate!")
        logger.info("Adaugare nereusita!")
        return -1
    logger.info("Adaugare reusita!")
    commit()
    return 0


def delete_user_from_database(user, password):
    logger.info("Sterge cont: " + user + "!")
    id_user = get_user_id(user)
    delete_reviews_of(id_user)
    cursor.execute("delete from accounts where username='" + user + "'")
    commit()
    logger.info("Stergere reusita!")


def getUserName(id):
    cursor.execute("select username " +
                   "from accounts " +
                   "where id_user=" + str(id))
    result = cursor.fetchall()
    return result[0][0]


# functions for movie's table
def check_if_movie_exist(name):
    logger.info("Cauta filmul: " + name)
    cursor.execute("select id_film " +
                   "from movies " +
                   "where name='" + name + "'")
    result = cursor.fetchall()
    if result == []:
        return False
    else:
        return True


def get_movie_id(name):
    cursor.execute("select id_film " +
                   "from movies " +
                   "where name='" + name + "'")
    result = cursor.fetchall()
    return int(result[0][0])


def add_movie(name, date, description, gendre, note, director_id):
    logger.info("Adaugam un film nou!")
    global movie_id
    try:
        cursor.execute("insert into movies values(" + str(get_next_indice(movie_id)) + ", '" + name + "', '" + str(date) + "', '" +
                   description + "', '" + gendre + "', " + str(director_id) + ", 1, " + str(note) + ")")
    except cx_Oracle.DatabaseError:
        logger.info("Camp data gresit introdus!")
        logger.info("Adaugare nereusita!")
        return -1
    commit()
    logger.info("Adaugare reusita!")
    return 0


def delete_movie_from_database(name):
    logger.info("Sterge filmul " + name + "!")
    id_film = get_movie_id(name)
    cursor.execute("select id_actor from stars " +
                   "where id_film=" + str(id_film))
    actors = cursor.fetchall()
    cursor.execute("delete from stars " +
                   "where id_film=" + str(id_film))
    for actor in actors:
        if not check_if_actor_is_in_another_movie(actor[0]):
            delete_actor(actor[0])

    cursor.execute("delete from user_reviews " +
                   "where id_film=" + str(id_film))

    cursor.execute("select id_director from movies where id_film=" + str(id_film))
    director = cursor.fetchall()
    director = int(director[0][0])
    cursor.execute("delete from movies " +
                   "where name='" + name + "'")
    if not check_if_director_has_another_movie(director):
        delete_director(director)
    commit()
    logger.info("Stergere reusita!")


# director table


def check_if_director_exist(director):
    logger.info("Cautam regizorul " + director + "!")
    cursor.execute("select id_director " +
                   "from directors " +
                   "where name='" + director + "'")
    result = cursor.fetchall()
    if result == []:
        return False
    else:
        return True


def get_director_id(director):
    cursor.execute("select id_director " +
                   "from directors " +
                   "where name='" + director + "'")
    result = cursor.fetchall()
    return int(result[0][0])


def add_director(director):
    global director_id
    logger.info("Adaugam un nou director:" + director + "!")
    try:
        cursor.execute("insert into directors values (" + str(get_next_indice(director_id)) + ", '" + director + "')")
    except cx_Oracle.DatabaseError:
        logger.info("Campuri incorect completate!")
        logger.info("Adaugare nereusita!")
        return -1
    commit()
    logger.info("Adaugare reusita!")
    return 0


def check_if_director_has_another_movie(id_director):
    cursor.execute("select id_film from movies where id_director=" + str(id_director))
    result = cursor.fetchall()
    if result == []:
        return False
    else:
        return True


def delete_director(director):
    cursor.execute("delete from directors where id_director=" + str(director))
    commit()


# actor table
def check_actor_exist(actor):
    logger.info("Cautam actorul " + actor + "!")
    cursor.execute("select id_actor " +
                   "from actors " +
                   "where name='" + actor + "'")
    result = cursor.fetchall()
    if result == []:
        return False
    else:
        return True


def get_actor_id(actor):
    cursor.execute("select id_actor " +
                   "from actors " +
                   "where name='" + actor + "'")
    result = cursor.fetchall()
    return int(result[0][0])


def add_actor(actor):
    global actor_id
    logger.info("Adaugam un nou actor:" + actor + "!")
    try:
        cursor.execute("insert into actors values (" + str(get_next_indice(actor_id)) + ", '" + actor + "')")
    except cx_Oracle.DatabaseError:
        logger.info("Campuri incorect completate!")
        logger.info("Adaugare nereusita!")
        return -1
    commit()
    logger.info("Adaugare reusita!")
    return 0


def check_if_actor_is_in_another_movie(id_actor):
    cursor.execute("select id_film from stars where id_actor=" + str(id_actor))
    result = cursor.fetchall()
    if result == []:
        return False
    else:
        return True


def delete_actor(id_actor):
    cursor.execute("delete from actors where id_actor=" + str(id_actor))
    commit()


# functions for review table
def check_if_review_exist(id, name):
    logger.info("Cautam review-ul la filmul " + name + "!")
    id_film = get_movie_id(name)
    cursor.execute("select id_user, id_film " +
                   "from user_reviews " +
                   "where id_user=" + str(id) + " and id_film=" + str(id_film))
    result = cursor.fetchall()
    if result == []:
        return False
    else:
        return True


def update_review_in_database(id, name, note, review):
    logger.info("Updatam review-ul la filmul " + name + "!")
    id_film = get_movie_id(name)
    cursor.execute(
        "update user_reviews " +
        "set note=" + str(note) + ", review='" + review + "' " +
        "where id_user=" + str(id) + " and id_film=" + str(id_film))

    cursor.execute(
        "select avg(note) " +
        "from user_reviews " +
        "where id_film=" + str(id_film) + " " +
        "group by id_film"
    )
    result = cursor.fetchall()
    note = result[0][0]
    cursor.execute(
        "update movies " +
        "set user_rating=" + str(note) + " " +
        "where id_film=" + str(id_film)
    )
    commit()
    logger.info("Update reusit!")


def add_review_in_database(id, name, note, review):
    logger.info("Adaugam review la filmul " + name + "!")
    global review_id
    id_film = get_movie_id(name)
    try:
        cursor.execute(
            "insert into user_reviews values(" + str(id) + ", " + str(id_film) + ", " + str(note) + ", '" +
            review + "')"
        )
    except cx_Oracle.DatabaseError:
        traceback.print_exc(file=sys.stdout)
        logger.info("Campuri incorect completate!")
        logger.info("Adaugare nereusita!")
        return -1
    cursor.execute(
        "select avg(note) " +
        "from user_reviews " +
        "where id_film=" + str(id_film) + " " +
        "group by id_film"
    )
    result = cursor.fetchall()
    note = result[0][0]
    cursor.execute(
        "update movies " +
        "set user_rating=" + str(note) + " " +
        "where id_film=" + str(id_film)
    )
    commit()
    logger.info("Adaugare reusita!")
    return 0


def delete_reviews_of(id_user):
    logger.info("Sterge toate review-urile user-ului!")
    cursor.execute("delete from user_reviews where id_user=" + str(id_user))
    commit()


# select functions

def show_all_movies():
    afisare = ""
    cursor.execute("select m.name, m.debut, m.description, m.gender, d.name, m.user_rating, m.critics_rating " +
                   "from movies m, directors d " +
                   "where m.id_director = d.id_director"
    )
    result = cursor.fetchall()
    afisare += "Afisare filme:\n"
    for col in result:
        afisare += "\tNumele filmului: " + str(col[0]) + "\n"
        afisare += "\tDebut: " + str(col[1]) + "\n"
        afisare += "\tDescriere: " + str(col[2]) + "\n"
        afisare += "\tGen: " + str(col[3]) + "\n"
        afisare += "\tNume regizor: " + str(col[4]) + "\n"
        afisare += "\tNota user: " + str(col[5]) + "\n"
        afisare += "\tNota critici: " + str(col[6]) + "\n\n"
    return afisare

def show_in_cronological_order_asc():
    afisare = ""
    cursor.execute("select m.name, m.debut, m.description, m.gender, d.name, m.user_rating, m.critics_rating " +
                   "from movies m, directors d " +
                   "where m.id_director = d.id_director " +
                   "order by m.debut asc"
                   )
    result = cursor.fetchall()
    afisare += "Afisare filme cronologic crescator:\n"
    for col in result:
        afisare += "\tNumele filmului: " + str(col[0]) + "\n"
        afisare += "\tDebut: " + str(col[1]) + "\n"
        afisare += "\tDescriere: " + str(col[2]) + "\n"
        afisare += "\tGen: " + str(col[3]) + "\n"
        afisare += "\tNume regizor: " + str(col[4]) + "\n"
        afisare += "\tNota user: " + str(col[5]) + "\n"
        afisare += "\tNota critici: " + str(col[6]) + "\n\n"
    return afisare



def show_in_cronological_order_desc():
    afisare = ""
    cursor.execute("select m.name, m.debut, m.description, m.gender, d.name, m.user_rating, m.critics_rating " +
                   "from movies m, directors d " +
                   "where m.id_director = d.id_director " +
                   "order by m.debut desc"
                   )
    result = cursor.fetchall()
    afisare += "Afisare filme cronologic descrescator:\n"
    for col in result:
        afisare += "\tNumele filmului: " + str(col[0]) + "\n"
        afisare += "\tDebut: " + str(col[1]) + "\n"
        afisare += "\tDescriere: " + str(col[2]) + "\n"
        afisare += "\tGen: " + str(col[3]) + "\n"
        afisare += "\tNume regizor: " + str(col[4]) + "\n"
        afisare += "\tNota user: " + str(col[5]) + "\n"
        afisare += "\tNota critici: " + str(col[6]) + "\n\n"
    return afisare


def show_after_critics_note():
    afisare = ""
    cursor.execute("select m.name, m.debut, m.description, m.gender, d.name, m.user_rating, m.critics_rating " +
                   "from movies m, directors d " +
                   "where m.id_director = d.id_director " +
                   "order by m.critics_rating asc"
                   )
    result = cursor.fetchall()
    afisare += "Afisare filme dupa notele criticilor:\n"
    for col in result:
        afisare += "\tNumele filmului: " + str(col[0]) + "\n"
        afisare += "\tDebut: " + str(col[1]) + "\n"
        afisare += "\tDescriere: " + str(col[2]) + "\n"
        afisare += "\tGen: " + str(col[3]) + "\n"
        afisare += "\tNume regizor: " + str(col[4]) + "\n"
        afisare += "\tNota user: " + str(col[5]) + "\n"
        afisare += "\tNota critici: " + str(col[6]) + "\n\n"
    return afisare


def show_made_by(name):
    afisare = ""
    cursor.execute("select m.name, m.debut, m.description, m.gender, d.name, m.user_rating, m.critics_rating " +
                   "from movies m, directors d " +
                   "where m.id_director = d.id_director and d.name='" + name + "'"
                   )
    result = cursor.fetchall()
    afisare += "Afisare filme facute de " + name + ":\n"
    for col in result:
        afisare += "\tNumele filmului: " + str(col[0]) + "\n"
        afisare += "\tDebut: " + str(col[1]) + "\n"
        afisare += "\tDescriere: " + str(col[2]) + "\n"
        afisare += "\tGen: " + str(col[3]) + "\n"
        afisare += "\tNume regizor: " + str(col[4]) + "\n"
        afisare += "\tNota user: " + str(col[5]) + "\n"
        afisare += "\tNota critici: " + str(col[6]) + "\n\n"
    return afisare


def show_actors_from(movie):
    afisare = ""
    id_film = get_movie_id(movie)
    cursor.execute("select a.name " +
                   "from stars s, actors a " +
                   "where a.id_actor = s.id_actor and s.id_film=" + str(id_film)
                   )
    result = cursor.fetchall()
    afisare += "Cast:" + "\n"
    for col in result:
        afisare += "\tActor: " + str(col[0]) + "\n"
    return afisare + "\n"


def show_all_reviews(id_user):
    afisare = ""
    cursor.execute("select m.name, u.note, u.review " +
                   "from movies m, user_reviews u " +
                   "where m.id_film = u.id_film and u.id_user=" + str(id_user)
                   )
    result = cursor.fetchall()
    afisare += "Review-uri facute de utilizator:\n"
    for col in result:
        afisare += "\tNumele filmului: " + str(col[0]) + "\n"
        afisare += "\tNota: " + str(col[1]) + "\n"
        afisare += "\tReview: " + str(col[2]) + "\n\n"
    return afisare


def show_review_of(id_user, movie):
    afisare = ""
    id_film = get_movie_id(movie)
    cursor.execute("select note, review " +
                   "from user_reviews  " +
                   "where id_user=" + str(id_user) + " and id_film="+str(id_film)
                   )
    result = cursor.fetchall()

    afisare += "Review-ul filmului " + movie + ":\n"
    for col in result:
        afisare += "\tNota: " + str(col[0]) + "\n"
        afisare += "\tReview: " + str(col[1]) + "\n\n"
    return afisare


# Usage

def add_in_cast(actor_id, id):
    cursor.execute("insert into stars values(" + str(id) + ", " + str(actor_id) + ")")
    commit()

def commit():
    cursor.execute("commit")

def get_next_indice(table_id):
    cursor.execute("select valoare from indices where id=" + str(table_id))
    result = cursor.fetchall()
    result = int(result[0][0])
    cursor.execute("update indices set valoare=" + str(result + 1) + " where id=" + str(table_id))
    commit()
    return result
