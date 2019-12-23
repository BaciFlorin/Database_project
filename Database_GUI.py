from tkinter import *
import logging
from Database_functions import *
import ScrolledTextHandler
from tkinter import scrolledtext

logger = logging.getLogger("gui_log")
logger.setLevel(logging.DEBUG)

class Database_GUI():
    def __init__(self, master):
        self.master = master
        self.id = 0
        self.first_frame = Frame(self.master, width=200, height=200)
        self.user_frame = Frame(self.master, width=60, height=120)
        self.admin_frame = Frame(self.master, width=60, height=150)
        self.first_frame.grid(row=0, column=0, sticky=(W, E, S, N), ipady=10)
        self.initLogInWindow()
        self.initUserWindow()
        self.initAdminWindow()

    def initLogInWindow(self):
        self.master.title("Database Project")
        Label(self.first_frame, text="Baze de date - Proiect", font="Arial").grid(row=0, column=0)

        login_frame = LabelFrame(self.first_frame, text="Log In:", width=60, height=20)
        login_frame.grid(row=1, column=0, sticky=(W, E, S, N), ipadx=10, ipady=10, padx=10, pady=10)

        Label(login_frame, text="User:").grid(row=0, column=0, sticky=E)
        self.user_entry = Entry(login_frame, width=30)
        self.user_entry.grid(row=0, column=1)

        Label(login_frame, text="Password:").grid(row=1, column=0, sticky=E)
        self.password_entry = Entry(login_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1)

        Button(login_frame, text="Log in", width=10, command=self.login_user).grid(row=0, column=2, padx=30, pady=5)
        Button(login_frame, text="Create user", width=10, command=self.create_user).grid(row=1, column=2, padx=30)
        Button(login_frame, text="Delete user", width=10, command=self.delete_user).grid(row=2, column=2, padx=30, pady=5)

        scroll_frame = LabelFrame(self.first_frame, text="Info:", width=60, height=20)
        scroll_frame.grid(row=2, column=0, sticky=(W, E, S, N), ipadx=10, ipady=10, padx=10)

        self.log_scrolled_text_login = ScrolledTextHandler.ScrolledTextHandler(scroll_frame, 50, 10)
        self.log_scrolled_text_login.place_widget(row=0, column=0, padx=10)

    def initUserWindow(self):
        Label(self.user_frame, text="Welcome " + getUserName(self.id) + "!", font="Arial").grid(row=0, column=0, padx=10, pady=10)

        review_frame = LabelFrame(self.user_frame, text="Adding review:", width=100, height=30)
        review_frame.grid(row=1, column=0, padx=20, pady=10)

        Label(review_frame, text="Movie:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.movie_name_entry = Entry(review_frame, width=30)
        self.movie_name_entry.grid(row=0, column=1, padx=10, sticky=E)

        Label(review_frame, text="Note:").grid(row=1, column=0, padx=5, pady=5)
        self.note_entry = Entry(review_frame, width=3)
        self.note_entry.grid(row=1, column=1, padx=10, sticky=W)

        Label(review_frame, text="Review:").grid(row=0, column=2, padx=10, pady=5)
        self.review = scrolledtext.ScrolledText(review_frame, width=40, height=5)
        self.review.grid(row=0, column=3, padx=10, pady=5, rowspan=2, sticky=W)

        Button(review_frame, text="Add review", command=self.add_review, width=10).grid(row=0, column=4, padx=20)
        Button(review_frame, text="Update review", command=self.update_review, width=10).grid(row=1, column=4, padx=20)

        display_frame = LabelFrame(self.user_frame, text="Display:")
        display_frame.grid(row=2, column=0, sticky=(W, E, S, N), padx=20)

        Label(display_frame, text="Filme:").grid(row=0, column=0, padx=10, pady=5)
        self.filtre_buttions_value = IntVar()
        Radiobutton(display_frame, text="Cronologic crescator", variable=self.filtre_buttions_value, value=1).grid(
            row=0, column=1, padx=5)
        Radiobutton(display_frame, text="Cronologic descrescator", variable=self.filtre_buttions_value, value=2).grid(
            row=0, column=2, padx=5)
        Radiobutton(display_frame, text="Dupa nota criticilor", variable=self.filtre_buttions_value, value=3).grid(
            row=0, column=3, padx=5)
        Radiobutton(display_frame, text="Facute de:", variable=self.filtre_buttions_value, value=4).grid(
            row=1, column=1, sticky=W, padx=5)
        self.filtre_regisor = Entry(display_frame, width=40)
        self.filtre_regisor.grid(row=1, column=2, sticky=W, padx=2)

        Label(display_frame, text="Actori:").grid(row=2, column=0, padx=10, pady=5)

        Radiobutton(display_frame, text="Din filmul:", variable=self.filtre_buttions_value, value=5).grid(
            row=2, column=1, sticky=W, padx=5)
        self.filtre_movie = Entry(display_frame, width=40)
        self.filtre_movie.grid(row=2, column=2, sticky=W)

        Label(display_frame, text="Reviews:").grid(row=3, column=0, padx=10, pady=5)
        Radiobutton(display_frame, text="Toate facute de mine:", variable=self.filtre_buttions_value, value=6).grid(
            row=3, column=1, sticky=W, padx=5)
        Radiobutton(display_frame, text="La filmul:", variable=self.filtre_buttions_value, value=7).grid(
            row=3, column=2, sticky=E, padx=5)
        self.filtre_review_movie = Entry(display_frame, width=40)
        self.filtre_review_movie.grid(row=3, column=3)

        Button(display_frame, text="Arata!", command=self.show_from_tables).grid(row=3, column=4, padx=20, pady=10)

        log_frame = LabelFrame(self.user_frame, text="Rezultatele afisarii si erori daca apar:")
        log_frame.grid(row=3, column=0, padx=20, pady=10, sticky=W)

        self.log_scrolled_text_user = ScrolledTextHandler.ScrolledTextHandler(log_frame, 100, 15)
        self.log_scrolled_text_user.place_widget(row=0, column=0, padx=10, sticky=W)

        Button(self.user_frame, text="Log off", width=10, command=self.changeFromUserToLogin).grid(row=4, column=0, pady=10, padx=20)

    def initAdminWindow(self):
        Label(self.admin_frame, text="Welcome admin!", font="Arial").grid(row=0, column=0, padx=30)

        movie_frame = LabelFrame(self.admin_frame, text="Detalii film:")
        movie_frame.grid(row=1, column=0, padx=20, pady=5, sticky=(W, E, S, N), ipadx=20, ipady=10)

        Label(movie_frame, text="Nume:").grid(row=0, column=0)
        self.admin_movie_entry = Entry(movie_frame, width=40)
        self.admin_movie_entry.grid(row=0, column=1, sticky=W, padx=5)

        Label(movie_frame, text="Data de aparitie:").grid(row=0, column=2, padx=10)
        self.admin_date_entry = Entry(movie_frame, width=20)
        self.admin_date_entry.grid(row=0, column=3)

        Label(movie_frame, text="Descriere:").grid(row=1, column=0)
        self.admin_descriprion = scrolledtext.ScrolledText(movie_frame, width=60, height=5)
        self.admin_descriprion.grid(row=1, column=1, columnspan=4, pady=15, sticky=W)

        Label(movie_frame, text="Gen:").grid(row=2, column=0)
        self.admin_movie_gendre = Entry(movie_frame, width=20)
        self.admin_movie_gendre.grid(row=2, column=1, sticky=W)

        Label(movie_frame, text="Nota critici (1-10):").grid(row=2, column=2)
        self.admin_critics_note = Entry(movie_frame, width=8)
        self.admin_critics_note.grid(row=2, column=3, padx=5, sticky=W)

        Label(movie_frame, text="Regizor:").grid(row=3, column=0, pady=10)
        self.admin_regisor = Entry(movie_frame, width=30)
        self.admin_regisor.grid(row=3, column=1, sticky=W)

        Label(movie_frame, text="Actors:").grid(row=4, column=0, pady=10)
        self.admin_actors = scrolledtext.ScrolledText(movie_frame, width=60, height=5)
        self.admin_actors.grid(row=4, column=1, sticky=W, columnspan=4)
        Label(movie_frame, text="*Numele actorilor sa fie despartite prin virgula!").grid(
            row=5, column=0, pady=2, columnspan=2, padx=20)

        Button(movie_frame, text="Adauga film", command=self.add_movie).grid(row=5, column=3, pady=20)

        log_frame = LabelFrame(self.admin_frame, text="Erori si informatii:")
        log_frame.grid(row=2, column=0, sticky=(W, E, S, N), padx=20)

        self.log_scrolled_text_admin = ScrolledTextHandler.ScrolledTextHandler(log_frame, 70, 10)
        self.log_scrolled_text_admin.place_widget(row=0, column=0, padx=10)
        Button(self.admin_frame, text="Log off", width=10, command=self.changeFromAdminToLogIn).grid(row=3, column=0, padx=10)

    def login_user(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        if user != "" and password != "":
            if check_if_user_in_database(user, password):
                self.id = get_user_id(user)
                if self.id == 1:
                    # init window for admin usage
                    self.changeFromLogInToAdmin()
                else:
                    # init window for ordinary user usage
                    self.changeFromLogInToUser()
            else:
                logger.info("User is not in database!")

    def create_user(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        if user != "" and password != "":
            if not check_if_user_exist(user):
                add_user_in_datase(user, password)
                self.id = get_user_id(user)
                self.changeFromLogInToUser()
            else:
                logger.info("User is already in database!")

    def delete_user(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        if user != "" and password != "":
            if check_if_user_in_database(user, password):
                if user != "admin":
                    delete_user_from_database(user, password)
                else:
                    logger.info("Admin user can't be remove from database!")
            else:
                logger.info("User is not in database!")

    def add_review(self):
        name = self.movie_name_entry.get()
        try:
            note = int(self.note_entry.get())
        except:
            return
            pass
        review = self.review.get("1.0", END)
        print(review)

    def update_review(self):
        pass

    def show_from_tables(self):
        pass

    def add_movie(self):
        pass

    def changeFromLogInToUser(self):
        self.first_frame.grid_forget()
        self.user_frame.grid(row=0, column=0)
        logger.removeHandler(self.log_scrolled_text_login)
        logger.addHandler(self.log_scrolled_text_user)
        self.master.geometry("890x660")

    def changeFromUserToLogin(self):
        self.user_frame.grid_forget()
        self.first_frame.grid(row=0, column=0)
        logger.removeHandler(self.log_scrolled_text_user)
        logger.addHandler(self.log_scrolled_text_login)
        self.master.geometry("490x400")

    def changeFromLogInToAdmin(self):
        self.first_frame.grid_forget()
        self.admin_frame.grid(row=0, column=0)
        logger.removeHandler(self.log_scrolled_text_login)
        logger.addHandler(self.log_scrolled_text_admin)
        self.master.geometry("640x640")

    def changeFromAdminToLogIn(self):
        self.admin_frame.grid_forget()
        self.first_frame.grid(row=0, column=0)
        logger.removeHandler(self.log_scrolled_text_admin)
        logger.addHandler(self.log_scrolled_text_login)
        self.master.geometry("490x400")