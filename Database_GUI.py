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
        self.user_frame.grid(row=0, column=0, sticky=(W, E, S, N), ipady=10)
        self.initUserWindow()

    def initLogInWindow(self):
        Label(self.first_frame, text="Baze de date - Proiect", font="Arial").grid(row=0, column=0)

        login_frame = LabelFrame(self.first_frame, text="Log In:", width=60, height=20)
        login_frame.grid(row=1, column=0, sticky=(W, E, S, N), ipadx=10, ipady=10, padx=10, pady=10)

        Label(login_frame, text="User:").grid(row=0, column=0, sticky=E)
        self.user_entry = Entry(login_frame, width=30)
        self.user_entry.grid(row=0, column=1)

        Label(login_frame, text="Password:").grid(row=1, column=0, sticky=E)
        self.password_entry = Entry(login_frame, width=30)
        self.password_entry.grid(row=1, column=1)

        Button(login_frame, text="Log in", width=10, command=self.login_user).grid(row=0, column=2, padx=30, pady=5)
        Button(login_frame, text="Create user", width=10, command=self.create_user).grid(row=1, column=2, padx=30)
        Button(login_frame, text="Delete user", width=10, command=self.delete_user).grid(row=2, column=2, padx=30, pady=5)

        scroll_frame = LabelFrame(self.first_frame, text="Info:", width=60, height=20)
        scroll_frame.grid(row=2, column=0, sticky=(W, E, S, N), ipadx=10, ipady=10, padx=10)

        log_scrolled_text = ScrolledTextHandler.ScrolledTextHandler(scroll_frame, 50, 10)
        log_scrolled_text.place_widget(row=0, column=0, padx=10)
        logger.addHandler(log_scrolled_text)

    def initUserWindow(self):
        self.master.geometry("1000x600")

        Label(self.user_frame, text="Welcome " + getUserName(self.id) + "!", font="Arial").grid(row=0, column=0, padx=10, pady=10)

        review_frame = LabelFrame(self.user_frame, text="Adding review:", width=60, height=30)
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

    def login_user(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        if user != "" and password != "":
            if check_if_user_in_database(user, password):
                self.id = get_user_id(user)
                if self.id == 1:
                    # init window for admin usage
                    pass
                else:
                    # init window for ordinary user usage
                    pass
            else:
                logger.info("User is not in database!")

    def create_user(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        if user != "" and password != "":
            if not check_if_user_exist(user):
                add_user_in_datase(user, password)
                id = get_user_id(user)
                # init window for that user
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

    def changeToUserInterface(self):
        self.first_frame.grid_forget()
        self.user_frame.grid(row=0, column=0)
        self.master.geometry("1000x600")
