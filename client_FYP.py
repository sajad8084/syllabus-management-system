from tkinter import *
from tkinter import ttk
from datetime import datetime


import tkcalendar
import dateutil.relativedelta as relativedelta
import dateutil.rrule as rrule
import numpy as np
import math
from functools import partial
import psycopg2
import tkinter.messagebox as msb

new_ls = []
from PIL import Image, ImageTk
from tkinter import PhotoImage

root = Tk()
# root.config(background='#daf2dc')
# root.attributes('zoomed', True)
root.iconify()
# root.config(bg='white')

# set up uni image on top

# back_button_image = PhotoImage(file=r"button_images/back_image_icon.png")
# # back_button_image_global = back_button_image.subsample(5)
# back_button_image_global = back_button_image
# # connect to database ******* *******
# image = Image.open("uni_logo/University_of_Sargodha.ico")
# render=image.resize((1600,900))
# render=ImageTk.PhotoImage(render)
# # render = ImageTk.PhotoImage(image)
# # render=render.resize((300, 205), Image.ANTIALIAS)
# img = Label(root, image=render)
# img.image = render
# img.place(x=0, y=0)


# create_bg()

root.iconbitmap('uni_logo/University_of_Sargodha.ico')
root.title("University of Sargodha")
uni_name_label = Label(root, text="University of Sargodha", bg='#003B6D', fg='#bfc7c5',
                       font=("Times", "24", "bold italic"))
uni_name_label.pack(pady=10)

m = root.maxsize()
root.geometry('{}x{}+0+0'.format(*m))
root.config(bg='#003B6D')

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
font_family = ("arial", 15, 'bold')

# sqlite 3 database

# with sqlite3.connect("syllabusdb.db") as db:
#     cursor = db.cursor()


# db = psycopg2.connect(
#     host="ec2-34-205-230-1.compute-1.amazonaws.com",
#     database="d5aga9t54atnmf",
#     user="dijnggusixsfpe",
#     password="2d998ef55f46239ff759726132c3ff8a2a7c697891ec1253070fbcd4dff76242")
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
cursor = db.cursor()

# global variables to be used
list_of_final_got_dates = []
syllabus_got_from_db = []
current_book = []
# to store roll no of persent_studensts_in_attndence
institude_level_for_attendence = []
name_of_class_for_attendence = []
names_of_studenst_for_attendence = []
lastnames_of_studenst_for_attendence = []
roll_numbers_to_presrnt = []
students_details_about_section = []

# session_id ==================
session_id = []
# print(session_id)
'''   
create tables for database


'''


# schedules table for syllabus


class admin:
    def __init__(self):
        self.login()
        # self.signup()

    def login(self):
        self.login_frame = LabelFrame(root, text="Login ", bg='#bfc7c5', width=400, height=300,
                                      font=("arial", 15, "bold"))
        self.login_frame.place(relx=.5, rely=.5, anchor=CENTER)
        # create the login icons===========================================================
        # self.usernamelabel=Label(self.login_frame,text="User Name",font=("arial",12))
        # self.usernamelabel.grid(x=)
        self.login_usernamelabel = Label(self.login_frame, text="username", bg='#bfc7c5', fg="#1a1309",
                                         font=('', 10, 'bold'))
        self.login_usernamelabel.place(anchor=E, relx=0.2, rely=0.2)
        self.login_password = Label(self.login_frame, text="password", bg='#bfc7c5', fg="#1a1309",
                                    font=('arial', 10, 'bold'), )
        self.login_password.place(anchor=E, relx=0.2, rely=0.4)
        # entries
        self.login_usernameentery = Entry(self.login_frame, width=15, font=font_family)
        self.login_usernameentery.place(anchor=E, relheight=0.10, relwidth=0.50, relx=0.8, rely=0.2)
        self.login_usernameentery.focus()
        

        # self.login_usernameentery.insert(0, 'gmail')
        self.login_passwordentery = Entry(self.login_frame, font=font_family)
        self.login_passwordentery.place(anchor=E, relheight=0.10, relwidth=0.50, relx=0.8, rely=0.4)
        self.login_passwordentery.config(show="*")
       

        # self.login_passwordentery.insert(0, '12')

        # login_btn

        login_image = PhotoImage(file="button_images/login_image.png")
        self.login_btn = Button(self.login_frame, image=login_image, bg="#bfc7c5", activebackground="#bfc7c5", bd=0,
                                command=self.check_login_constraints)
        self.login_btn.image = login_image
        self.login_btn.place(anchor=E, relheight=0.13, relwidth=0.20, relx=0.65, rely=0.6)
        # did not have an account

        self.didnot_haveana_ccount = Button(self.login_frame, text="Don't have an account?", bd=0, bg='#bfc7c5',
                                            fg='blue', font=('arial', 12), command=self.signup)
        self.didnot_haveana_ccount.place(anchor=E, relx=0.6, rely=0.8)

    def check_login_constraints(self):
        cursor.execute("select id,email,password from users")
        data = cursor.fetchall()
        ids = []
        email = []
        password = []
        for i in data:
            ids.append(i[0])
            email.append(i[1])
            password.append(i[2])
        inputmail = self.login_usernameentery.get()
        inputpwd = self.login_passwordentery.get()
        for index, k in enumerate(email):
            if inputmail == k:
                if inputpwd == password[index]:
                    session_id.append(index + 1)
                    # print(session_id[0])

        if len(session_id) > 0:

            # print(session_id[0])

            self.main_manu_widgets()


        else:
            msb.showerror("error", "Wrong Username or password")

    def signup(self):
        self.signup_frame = Frame(root, bg='#bfc7c5')
        self.signup_frame.place(relx=0.2, rely=0.2, relwidth=0.5, relheight=0.5)

        self.signup_username = Label(self.signup_frame, text="Full name", fg="#1a1309", bg="#bfc7c5",
                                     font=('', 10, 'bold'))
        self.signup_username.place(anchor=W, relx=0.25, rely=0.2)
        self.signup_mobile = Label(self.signup_frame, text="Mobile", fg="#1a1309", bg="#bfc7c5", font=('', 10, 'bold'))
        self.signup_mobile.place(anchor=W, relx=0.25, rely=0.3)
        self.signup_email = Label(self.signup_frame, text="e mail", fg="#1a1309", bg="#bfc7c5", font=('', 10, 'bold'))
        self.signup_email.place(anchor=W, relx=0.25, rely=0.4)
        self.signup_gender = Label(self.signup_frame, text="gender", fg="#1a1309", bg="#bfc7c5", font=('', 10, 'bold'))
        self.signup_gender.place(anchor=W, relx=0.25, rely=0.5)
        self.signup_password = Label(self.signup_frame, text="password", fg="#1a1309", bg="#bfc7c5",
                                     font=('', 10, 'bold'))
        self.signup_password.place(anchor=W, relx=0.25, rely=0.6)
        self.signup_confirmpass = Label(self.signup_frame, text="confirm password", fg="#1a1309", bg="#bfc7c5",
                                        font=('', 10, 'bold'))
        self.signup_confirmpass.place(anchor=W, relx=0.25, rely=0.7)

        # enteries for sign up
        self.signup_fullname_entery = Entry(self.signup_frame, font=font_family)
        self.signup_fullname_entery.place(anchor=E, relx=0.7, rely=0.2)
        self.signup_mobile_entery = Entry(self.signup_frame, font=font_family)
        self.signup_mobile_entery.place(anchor=E, relx=0.7, rely=0.3)
        self.signup_email_entery = Entry(self.signup_frame, font=font_family)
        self.signup_email_entery.place(anchor=E, relx=0.7, rely=0.4)
        self.gender_for_signup = ttk.Combobox(self.signup_frame, state="readonly", width=34, height=15)
        self.gender_for_signup['values'] = ("Select a gender", 'Male', 'Female', "Others")
        self.gender_for_signup.current(0)
        self.gender_for_signup.place(anchor=E, relx=0.7, rely=0.5)
        self.signup_password_entery = Entry(self.signup_frame, font=font_family)
        self.signup_password_entery.place(anchor=E, relx=0.7, rely=0.6)
        self.signup_confirmpassword_entery = Entry(self.signup_frame, font=font_family)
        self.signup_confirmpassword_entery.place(anchor=E, relx=0.7, rely=0.7)
        signupimage = PhotoImage(file=r"button_images/sign_up_image.png")
        exitimage = PhotoImage(file=r"button_images/exit.png")

        self.sign_up_button = Button(self.signup_frame, image=signupimage, bd=0, bg='#bfc7c5', borderwidth=0,
                                     activebackground="#bfc7c5",
                                     command=self.register_user)
        self.sign_up_button.image = signupimage
        self.sign_up_button.place(anchor=E, relx=0.6, rely=0.83)

        self.Exit_button = Button(self.signup_frame, image=exitimage, bd=0, bg='#bfc7c5', borderwidth=0,
                                  activebackground="#bfc7c5",
                                  command=self.exit_signup)
        self.Exit_button.image = exitimage
        self.Exit_button.place(anchor=E, relx=0.45, rely=0.83)

    def exit_signup(self):
        self.signup_frame.destroy()
        self.login()

    # making GUI for the main menu
    def register_user(self):
        fullname = self.signup_fullname_entery.get().strip()
        mobile = self.signup_mobile_entery.get().strip()
        email = self.signup_email_entery.get().strip()
        gender = self.gender_for_signup.get().strip()
        password = self.signup_password_entery.get().strip()
        confirm_password = self.signup_confirmpassword_entery.get().strip()
        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, email)):
            print("Valid Email")

        if fullname == "" or mobile == "" or email == "" or gender == "" or gender == "Select a gender" or password == "" or confirm_password == "" or password != confirm_password:

            msb.showerror("Alert", "Something went wrong")
        elif len(password) < 4:
            msb.showerror("Alert", "Input at least four digits for password")
        elif not re.fullmatch(regex, email):
            msb.showerror("Alert", "wrong email")

        else:

            # now = datetime.now()
            current_time = datetime.now().strftime("%I:%M %p")

            query = "INSERT INTO users(full_name,mobile ,email, gender,password,signup_date,time)VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,
                           (fullname, mobile, email, gender, password, str(datetime.today().date()), str(current_time)))
            db.commit()
            msb.showinfo("Congratulation", "You have been registered successfully")
            self.signup_frame.destroy()
            self.login()

    def main_manu_widgets(self):
        # print("entere here")
        self.login_frame.destroy()

        # Let us create a dummy button and pass the image
        # destroy_bg()
        self.main_menu_buttons_frame = LabelFrame(root,
                                                  highlightthickness=2, bg='#bfc7c5', bd=0, width=screenwidth - 600,
                                                  height=screenheight - 300,
                                                  )
        self.main_menu_buttons_frame.pack(padx=50, pady=100, anchor=CENTER, expand=1, fill=BOTH)

        add_syllabus_image = Image.open("main_menu_buttons/add_syllabus_menu_btn.png")
        resized_image = add_syllabus_image.resize((200,150))

        # Convert the image to a PhotoImage object
        add_syllabus_image = ImageTk.PhotoImage(resized_image)

        # add_syllabus_image_alter = add_syllabus_image.subsample(3, 3)

        self.add_syllabus_btn = Button(self.main_menu_buttons_frame, image=add_syllabus_image, bd=0, bg="#bfc7c5",
                                       activebackground="#bfc7c5",
                                       command=self.add_syllabus_to_list)
        self.add_syllabus_btn.image = add_syllabus_image
        self.add_syllabus_btn.place(relx=0.2, rely=0.09)

        #

        view_syllabus_image = PhotoImage(file=r"main_menu_buttons/view_syllabus.png")
        self.view_syllabus_btn = Button(self.main_menu_buttons_frame, image=view_syllabus_image, bd=0, bg="#bfc7c5",
                                        activebackground="#bfc7c5", command=self.view_syllabus_by_professors)
        self.view_syllabus_btn.image = view_syllabus_image
        self.view_syllabus_btn.place(relx=0.50, rely=0.09)

        # ROW 2
        attendence_image = PhotoImage(file=r"main_menu_buttons/call_attendence.png")
        self.student_attendence_btn = Button(self.main_menu_buttons_frame, image=attendence_image, bd=0, bg="#bfc7c5",
                                             activebackground="#bfc7c5",
                                             command=self.attendence_system)
        self.student_attendence_btn.image = attendence_image
        self.student_attendence_btn.place(relx=0.8, rely=0.09)

        view_announcements = PhotoImage(file=r"main_menu_buttons/view_announcements_new.png")
        self.main_settings_btn = Button(self.main_menu_buttons_frame, image=view_announcements,
                                        command=self.show_announcements, bd=0, bg="#bfc7c5",
                                        activebackground="#bfc7c5", )
        self.main_settings_btn.image = view_announcements
        self.main_settings_btn.place(relx=0.35, rely=0.4)

        view_announcements = PhotoImage(file=r"main_menu_buttons/view_sms_notifications.png")
        self.main_settings_btn = Button(self.main_menu_buttons_frame, image=view_announcements, bd=0, bg="#bfc7c5",
                                        activebackground="#bfc7c5", command=self.send_sms_today_function)
        self.main_settings_btn.image = view_announcements
        self.main_settings_btn.place(relx=0.6, rely=0.4)

        # settings_image = PhotoImage(file=r"main_menu_buttons/settings_2.png")
        # self.main_settings_btn = Button(self.main_menu_buttons_frame, bg="#bfc7c5", bd=0, activebackground="#bfc7c5",
        #                                 image=settings_image)
        # self.main_settings_btn.image = settings_image
        #
        # self.main_settings_btn.place(relx=0.8, rely=0.4)

    # ======================================= add syllabus from database ===============================
    def destroy_add_syllabus_tolist(self):
        self.add_syllabus_tolist_frame.destroy()
        self.main_manu_widgets()
        self.back_button_addsyl.destroy()

    def add_syllabus_to_list(self):

        self.main_menu_buttons_frame.destroy()
        self.add_syllabus_tolist_frame = LabelFrame(root, highlightthickness=1, bg='#bfc7c5', bd=0,
                                                    width=screenwidth - 500,
                                                    height=screenheight - 300,
                                                    font=("arial", 15, "bold"))
        self.back_button_addsyl = Button(root, text="Back <-", bd=1, bg='white',
                                         command=self.destroy_add_syllabus_tolist)
        self.back_button_addsyl.place(x=5, y=7)
        self.add_syllabus_tolist_frame.pack(padx=50, pady=50, anchor=CENTER, expand=1, fill=BOTH)

        self.degree_program = ttk.Combobox(self.add_syllabus_tolist_frame, state="readonly")
        self.degree_program['values'] = ("Select a program", "University")
        self.degree_program.current(0)
        self.degree_program.bind("<<ComboboxSelected>>", lambda _: self.selected_degree())

        self.degree_program.place(relx=0.1, rely=0.1)

    # handling with school section

    def school_attributes(self):

        self.class_selectoin_school = ttk.Combobox(self.add_syllabus_tolist_frame, state="readonly", width=12,
                                                   font=("arial", 12))
        self.class_selectoin_school['values'] = ("Select a class", '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',)
        self.class_selectoin_school.current(0)
        self.class_selectoin_school.bind("<<ComboboxSelected>>", lambda _: self.school_level_available_subjects())

        self.class_selectoin_school.place(relx=0.2, rely=0.1)

    # select further based on this below function  of uni colg and schools
    def selected_degree(self):
        value = self.degree_program.get()
        if value == "School":
            self.school_attributes()
        elif value == "College":
            self.college_attributes()
        elif value == "University":
            self.uni_attributes()

    # work with school attributes
    def school_level_available_subjects(self):
        self.school_books_list = ttk.Combobox(self.add_syllabus_tolist_frame, state="readonly", width=12,
                                              font=("arial", 12))
        self.school_books_list['values'] = ("Select books", 'book1', 'book2')

        self.school_books_list.current(0)
        # self.class_selectoin_school.bind("<<ComboboxSelected>>", lambda _: self.selection1())

        self.school_books_list.place(relx=0.3, rely=0.1)

    # handling with college section

    def college_attributes(self):
        self.class_selectoin_college = ttk.Combobox(self.add_syllabus_tolist_frame, state="readonly", width=12,
                                                    font=("arial", 12))
        self.class_selectoin_college['values'] = ("Select a class", '11', '12')
        self.class_selectoin_college.current(0)
        self.class_selectoin_college.bind("<<ComboboxSelected>>", lambda _: self.college_level_available_subjects())
        self.class_selectoin_college.place(relx=0.2, rely=0.1)

    def college_level_available_subjects(self):

        self.college_books_list = ttk.Combobox(self.add_syllabus_tolist_frame, state="readonly", width=12,
                                               font=("arial", 12))
        self.college_books_list['values'] = ("Select books", 'collge book1', 'college book2')
        self.college_books_list.current(0)
        self.college_books_list.place(relx=0.3, rely=0.1)

    # university handling below

    # here below in function uni_attributes we have a list of subjects from database  and two widgets entery and listbox to getvalues ,we use binding to insrt and get the values at runtime changing

    def uni_attributes(self):

        cursor.execute(
            f"SELECT class_standard from assigned_subjects_teachers WHERE teacher_id = '{session_id[0]}' ")
        filtered_subjects_on_id = cursor.fetchall()
        # print(filtered_subjects_on_id)
        if len(filtered_subjects_on_id) == 0:
            msb.showinfo("Sorry", "No subject has been assigned to you.")
        else:
            selected_subjects = []
            selected_subjects.append("Select a Class")
            for i in filtered_subjects_on_id:
                selected_subjects.append(i[0])

            # books select
            self.uni_books_list = ttk.Combobox(self.add_syllabus_tolist_frame, state="readonly", width=15,
                                               font=("arial", 12))
            # self.uni_books_list['values'] = (selected_subjects)
            # self.uni_books_list.current(0)
            self.uni_books_list.place(relx=0.3, rely=0.1)
            # self.uni_books_list.bind("<<ComboboxSelected>>", lambda _: self.classes_lists())
            # class
            self.uni_classes_list = ttk.Combobox(self.add_syllabus_tolist_frame, state="readonly", width=12,
                                                 font=("arial", 12))

            self.uni_classes_list['values'] = (selected_subjects)

            self.uni_classes_list.bind("<<ComboboxSelected>>", lambda _: self.classes_lists())
            self.uni_classes_list.current(0)
            self.uni_classes_list.place(relx=0.2, rely=0.1)

            self.okbtn_calling_scheduling = ttk.Button(self.add_syllabus_tolist_frame, text="OK",
                                                       command=self.got_details_of_books_university)
            self.okbtn_calling_scheduling.place(relx=0.43, rely=0.1)

        # handling univeristy level 2 like getting syllabus from db and show to user and get start and end date fom user

    def classes_lists(self):

        var = self.uni_classes_list.get()

        cursor.execute(
            f"SELECT subject_selected from assigned_subjects_teachers WHERE teacher_id = '{session_id[0]}' AND class_standard='{var}'")
        filtered_subjects_on_id = cursor.fetchall()

        selected_subjects = []
        selected_subjects.append("Select  a Subject")
        for i in filtered_subjects_on_id:
            selected_subjects.append(i[0])

        self.uni_books_list['values'] = (selected_subjects)
        self.uni_books_list.current(0)
        selected_subjects.clear()

    def got_details_of_books_university(self):
        # name,code,author,program,class,type,content

        local_list = []
        institute_level = self.degree_program.get()
        cur_subject = self.uni_books_list.get()
        cur_program = self.uni_classes_list.get()

        cursor.execute(
            f"SELECT * FROM courses WHERE name='{cur_subject}' AND program='{institute_level}' AND class='{cur_program}'")

        data = cursor.fetchall()

        for i in data:
            local_list.append(i[1:])

        if len(data) == 0:
            msb.showerror("Alert", "No Syllabus found for this Subject")
        else:
            try:

                self.name_value.config(text='')
                self.code_value.config(text='')
                self.auther_value.config(text='')
            except:
                pass
            self.name_label = Label(self.add_syllabus_tolist_frame, text="Course Name:", font=font_family)
            self.name_label.place(relx=0.1, rely=0.2)

            self.name_value = Label(self.add_syllabus_tolist_frame, text=local_list[0][0], font=font_family)
            self.name_value.place(relx=0.2, rely=0.2)
            current_book.append(local_list[0][0])

            self.code_label = Label(self.add_syllabus_tolist_frame, text="Course Code:", font=font_family)
            self.code_label.place(relx=0.3, rely=0.2)

            self.code_value = Label(self.add_syllabus_tolist_frame, text=local_list[0][1], font=font_family)
            self.code_value.place(relx=0.4, rely=0.2)

            self.auther_label = Label(self.add_syllabus_tolist_frame, text="Auther:", font=font_family)
            self.auther_label.place(relx=0.5, rely=0.2)

            self.auther_value = Label(self.add_syllabus_tolist_frame, text=local_list[0][2], font=font_family)
            self.auther_value.place(relx=0.6, rely=0.2)

            # row2
            self.study_level_label = Label(self.add_syllabus_tolist_frame, text="Level:", font=font_family)
            self.study_level_label.place(relx=0.1, rely=0.25)
            self.study_level_label.place(relx=0.1, rely=0.25)

            self.study_level_value = Label(self.add_syllabus_tolist_frame, text=local_list[0][3], font=font_family)
            self.study_level_value.place(relx=0.2, rely=0.25)

            self.class_label = Label(self.add_syllabus_tolist_frame, text="Class:", font=font_family)
            self.class_label.place(relx=0.3, rely=0.25)

            self.class_value = Label(self.add_syllabus_tolist_frame, text=local_list[0][4], font=font_family)
            self.class_value.place(relx=0.4, rely=0.25)

            self.rec_ref_label = Label(self.add_syllabus_tolist_frame, text="rec/ref:", font=font_family)
            self.rec_ref_label.place(relx=0.5, rely=0.25)

            self.rec_ref_value = Label(self.add_syllabus_tolist_frame, text=local_list[0][5], font=font_family)
            self.rec_ref_value.place(relx=0.6, rely=0.25)

            self.syllabus_box = Text(self.add_syllabus_tolist_frame, width=150, height=25, highlightbackground="red",
                                     wrap=WORD, highlightcolor="red", highlightthickness=2)
            syllabus_got_from_db.append(local_list[0][6])

            self.syllabus_box.place(relx=0.1, rely=0.4)
            self.syllabus_box.insert('1.0', local_list[0][6])

            # defining radio button of selction
            self.radiovar = StringVar()

            self.set_schedule_by = ttk.Label(self.add_syllabus_tolist_frame, text="Set Schedule by")
            self.set_schedule_by.place(relx=0.8, rely=0.35)

            self.dailyradio = ttk.Radiobutton(self.add_syllabus_tolist_frame, text="Day", variable=self.radiovar,
                                              value="daily", command=self.radio_results)
            self.dailyradio.place(relx=0.88, rely=0.35)

            self.weeklyradio = ttk.Radiobutton(self.add_syllabus_tolist_frame, text="Week", variable=self.radiovar,
                                               value="weekly", command=self.radio_results)
            self.weeklyradio.place(relx=0.93, rely=0.35)

            # making check boxes and find the days between the dates

            self.mondayvar = IntVar()
            self.monday = Checkbutton(self.add_syllabus_tolist_frame, text='Monday', variable=self.mondayvar, onvalue=1,
                                      offvalue=0, )
            self.monday.place(relx=0.1, rely=0.35)
            self.tuesdayvar = IntVar()
            self.tuesday = Checkbutton(self.add_syllabus_tolist_frame, text='Tuesday', variable=self.tuesdayvar,
                                       onvalue=1,
                                       offvalue=0, )
            self.tuesday.place(relx=0.15, rely=0.35)
            self.wednesdayvar = IntVar()
            self.wednesday = Checkbutton(self.add_syllabus_tolist_frame, text='Wednesday', variable=self.wednesdayvar,
                                         onvalue=1,
                                         offvalue=0, )
            self.wednesday.place(relx=0.2, rely=0.35)
            self.thursdayvar = IntVar()
            self.thursday = Checkbutton(self.add_syllabus_tolist_frame, text='Thursday', variable=self.thursdayvar,
                                        onvalue=1,
                                        offvalue=0, )
            self.thursday.place(relx=0.25, rely=0.35)
            self.fridayvar = IntVar()
            self.friday = Checkbutton(self.add_syllabus_tolist_frame, text='Friday', variable=self.fridayvar, onvalue=1,
                                      offvalue=0, )
            self.friday.place(relx=0.3, rely=0.35)
            self.saturdayvar = IntVar()
            self.saturday = Checkbutton(self.add_syllabus_tolist_frame, text='Saturday', variable=self.saturdayvar,
                                        onvalue=1,
                                        offvalue=0, )
            self.saturday.place(relx=0.35, rely=0.35)
            self.sundayvar = IntVar()
            self.sunday = Checkbutton(self.add_syllabus_tolist_frame, text='Sunday', variable=self.sundayvar, onvalue=1,
                                      offvalue=0, )
            self.sunday.place(relx=0.4, rely=0.35)

            # making date getter and find days between them
            self.datefromlabel = ttk.Label(self.add_syllabus_tolist_frame, text="Date From")
            self.datefromlabel.place(relx=0.45, rely=0.35)
            self.startdate = tkcalendar.DateEntry(self.add_syllabus_tolist_frame, selectmode='day',
                                                  date_pattern='dd-mm-y')
            self.startdate.place(relx=0.5, rely=0.35)
            self.datetolabel = ttk.Label(self.add_syllabus_tolist_frame, text="Date To")
            self.datetolabel.place(relx=0.6, rely=0.35)
            self.enddate = tkcalendar.DateEntry(self.add_syllabus_tolist_frame, selectmode='day',
                                                date_pattern='dd-mm-y')
            self.enddate.place(relx=0.65, rely=0.35)
            self.datebtn = ttk.Button(self.add_syllabus_tolist_frame, text="Find Dates", command=self.find_dates)
            self.datebtn.place(relx=0.72, rely=0.35)

    def find_dates(self):

        monlist = []
        tueslist = []
        wedist = []
        thurlist = []
        frilist = []
        satlist = []
        sunlist = []

        startdate = self.startdate.get_date()
        enddate = self.enddate.get_date()
        startdate = datetime.strftime(startdate, "%Y,%m,%d")
        enddate = datetime.strftime(enddate, "%Y,%m,%d")
        st = startdate.split(",")
        ed = enddate.split(",")

        before = datetime(int(st[0]), int(st[1]), int(st[2]))
        after = datetime(int(ed[0]), int(ed[1]), int(ed[2]))
        if self.mondayvar.get() == 1:
            rr1 = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.MO, dtstart=before)
            data1 = (rr1.between(before, after, inc=True))
            monlist.append(data1)

        if self.tuesdayvar.get() == 1:
            rr2 = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.TU, dtstart=before)
            data2 = (rr2.between(before, after, inc=True))
            tueslist.append(data2)

        if self.wednesdayvar.get() == 1:
            rr3 = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.WE, dtstart=before)
            data3 = (rr3.between(before, after, inc=True))
            wedist.append(data3)

        if self.thursdayvar.get() == 1:
            rr4 = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.TH, dtstart=before)
            data4 = (rr4.between(before, after, inc=True))
            thurlist.append(data4)

        if self.fridayvar.get() == 1:
            rr5 = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.FR, dtstart=before)
            data5 = (rr5.between(before, after, inc=True))
            frilist.append(data5)

        if self.saturdayvar.get() == 1:
            rr6 = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.SA, dtstart=before)
            data6 = (rr6.between(before, after, inc=True))
            satlist.append(data6)

        if self.sundayvar.get() == 1:
            rr7 = rrule.rrule(rrule.WEEKLY, byweekday=relativedelta.SU, dtstart=before)
            data7 = (rr7.between(before, after, inc=True))
            sunlist.append(data7)

        local_list = [monlist, tueslist, wedist, thurlist, frilist, satlist, sunlist]

        regular_list = local_list
        flat_list = [item for sublist in regular_list for item in sublist]
        flat_list1 = [item for sublist in flat_list for item in sublist]

        ls = []
        for i in flat_list1:
            ls.append(i)
            list_of_final_got_dates.append(str(i).split(" ")[0])

    def radio_results(self):

        # finding the splited corse here
        local_syllabus = syllabus_got_from_db
        local_syllabus1 = []

        # sort the dates we get from selection
        aa = list_of_final_got_dates
        lin = [i.strip().split(',') for i in aa]
        lin = sorted(lin)
        sorted_dates = [item for sublist in lin for item in sublist]

        # spliting the syllabus here
        # local_syllabus = [i.strip().split('chapter#') for i in local_syllabus]

        radiovalue = self.radiovar.get()
        if radiovalue == "daily":

            daily_syllabus = [str(i).split(",") for i in list(local_syllabus)]
            for i in daily_syllabus[0]:
                local_syllabus1.append(i)
            two_split = np.array_split(local_syllabus1, len(sorted_dates))

            final_list_of_syllabus_daily = []
            for i in two_split:
                if len(i) >= 1:
                    final_list_of_syllabus_daily.append(i)
                else:
                    final_list_of_syllabus_daily.append("Revision")
            final_list_of_syllabus_daily1 = []
            for i in final_list_of_syllabus_daily:
                final_list_of_syllabus_daily1.append(str(i).replace("[", "").replace("]", "").replace("\\n", ""))

            sub_code = self.code_value['text']
            sub_cls = self.class_value['text']
            newvariable = {key: value for key, value in zip(sorted_dates, final_list_of_syllabus_daily1)}

            store_or_not_daily = msb.askyesnocancel("Attention",
                                                    f"Your schedule is being sorted as follows: {newvariable}")
            if store_or_not_daily == 0:
                pass
            elif store_or_not_daily == 1:

                qurey = "INSERT INTO schedules (session_id ,schedule_type ,course_name,subject_class,subject_code ,date ,content  )VALUES(%s,%s,%s,%s,%s,%s,%s)"

                for dates, syl in zip(sorted_dates, final_list_of_syllabus_daily1):
                    cursor.execute(qurey,
                                   (int(session_id[0]), "daily", str(current_book[0]), sub_cls, sub_code, dates, syl))
                    db.commit()
                msb.showinfo("", "Congratulation your subject's Schedule has been added")
                final_list_of_syllabus_daily1.clear()
                final_list_of_syllabus_daily.clear()
                daily_syllabus.clear()
                sorted_dates.clear()
                local_syllabus1.clear()


        elif radiovalue == "weekly":

            # takes input from  db and store and split in with chapter# and store in weekly_syllabus
            weekly_syllabus = [i.split("chapter#") for i in syllabus_got_from_db]

            # split the syllabus accrd. to dates and store in other list as floored_valuetwo_split
            floored_valuetwo_split = np.array_split(weekly_syllabus[0], len(list_of_final_got_dates))
            floored_valuetwo_split = [i for i in floored_valuetwo_split]
            # here are final two lists that store dates and syllabus for week to isnert into db
            temp_dates = []
            temp_syllabus = []
            # use copy to remove duplications from list
            temp_syllabus_copy = []
            # check len of lists of date if it dates are more then len of schedules , then add rivision in db

            for dates, syl in zip(list_of_final_got_dates, floored_valuetwo_split):
                temp_dates.append(dates)
                if len(syl) <= 0:
                    temp_syllabus.append("Revision")

                else:
                    temp_syllabus.append(str(syl))

            sub_code = self.code_label['text']
            sub_cls = self.class_label['text']

            newvariable = {key: value for key, value in zip(temp_dates, list(temp_syllabus))}
            weekly = msb.askyesnocancel("Alert", "Are you sure you want to submit?")
            if weekly == 0:
                pass
            if weekly == 1:

                # itterate over stored lists of dates and schedule dates and store in db
                qurey = "INSERT INTO schedules (session_id ,schedule_type ,course_name ,subject_class,subject_code,date ,content )VALUES(%s,%s,%s,%s,%s,%s,%s)"
                for dates, syl in zip(temp_dates, list(temp_syllabus)):
                    cursor.execute(qurey, (
                        int(session_id[0]), "weekly", current_book[0], str(sub_cls), str(sub_code), str(dates),
                        str(syl)))
                    db.commit()

                temp_syllabus.clear()
                temp_dates.clear()
                weekly_syllabus.clear()
                floored_valuetwo_split.clear()
                current_book.clear()
                msb.showinfo("", "Congratulation your subject's Schedule has been added")

    # handling attendence of students ==================================================================================
    def destroy_and_back_attendence_system(self):
        self.add_syllabus_attendence_frame.destroy()
        self.main_manu_widgets()
        self.attendence_back_btn.destroy()

    def attendence_system(self):

        self.main_menu_buttons_frame.destroy()

        self.add_syllabus_attendence_frame = LabelFrame(root,
                                                        width=screenwidth - 400,
                                                        height=700, bg='#bfc7c5')

        self.add_syllabus_attendence_frame.pack(padx=50, pady=50, anchor=CENTER)
        self.attendence_back_btn = Button(root, text="Back <-", bd=1, bg='white',
                                          command=self.destroy_and_back_attendence_system)
        self.attendence_back_btn.place(x=5, y=7)
        # adding content on attendence frame
        self.degree_program_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                                      font=("arial", 12))
        self.degree_program_attendence['values'] = ("Select a program",  "University")

        self.degree_program_attendence.current(0)
        self.degree_program_attendence.bind("<<ComboboxSelected>>", lambda _: self.select_standard_attendence())
        self.degree_program_attendence.place(relx=0.1, rely=0.05)

        self.class_standard_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                                      font=("arial", 12))
        self.class_standard_attendence['values'] = ()

        self.class_standard_attendence.place(relx=0.25, rely=0.05)
        # section dumy made
        self.section_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                               font=("arial", 12))
        self.section_attendence['values'] = ()
        # self.section_attendence.current(0)
        self.section_attendence.place(relx=0.4, rely=0.05)

        self.okbtn_attendence = ttk.Button(self.add_syllabus_attendence_frame, text="Find Class",
                                           command=self.got_students_details_fromdb)
        self.okbtn_attendence.place(relx=0.55, rely=0.05)

    # function to work on further values selection in attendence frame
    def select_standard_attendence(self):
        self.class_standard_attendence.destroy()
        # class name
        degree_level = self.degree_program_attendence.get()
        # storing level in list to work with attendence
        institude_level_for_attendence.append(degree_level)

        cursor.execute(
            f"SELECT class_standard FROM assigned_subjects_teachers WHERE institute_level='{degree_level}' AND teacher_id={session_id[0]}")
        data = cursor.fetchall()
        ls = ["Select a class"]
        for i in data:
            if i in ls:
                pass
            else:
                ls.append(i)

        self.class_standard_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                                      font=("arial", 12))
        self.class_standard_attendence['values'] = (ls)
        self.class_standard_attendence.current(0)
        self.class_standard_attendence.bind("<<ComboboxSelected>>", lambda _: self.select_section_attendence())

        self.class_standard_attendence.place(relx=0.25, rely=0.05)

    # define the section
    def select_section_attendence(self):
        # class name
        name_of_class_for_attendence.append(self.class_standard_attendence.get())

        # self.section_attendence.destroy()
        class_standard = self.class_standard_attendence.get()
        # storing level in list to work with attendence
        # students_details_about_section.append(class_standard)
        cursor.execute(
            f"SELECT section_selected FROM assigned_subjects_teachers WHERE class_standard='{class_standard}' AND institute_level='{institude_level_for_attendence[0]}' AND teacher_id='{session_id[0]}'")
        data = cursor.fetchall()
        ls = ["Select a section"]
        for i in data:
            if i in ls:
                pass
            else:
                ls.append(i)

        self.section_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                               font=("arial", 12))
        self.section_attendence['values'] = (ls)
        self.section_attendence.current(0)
        self.section_attendence.bind("<<ComboboxSelected>>", lambda _: self.add_students_details())

        self.section_attendence.place(relx=0.4, rely=0.05)

    def add_students_details(self):

        # students_details_about_section.clear()
        students_details_about_section.append(self.section_attendence.get())

    def makingvars(self):
        self.varslst = []
        degree_level = self.degree_program_attendence.get()
        class_standard = self.class_standard_attendence.get()
        section_standard = self.section_attendence.get()

        cursor.execute(
            f"SELECT name,lastname,rollno FROM classes_list WHERE class_standard='{class_standard}' AND edu_level='{degree_level}' AND section_name= '{section_standard}'")

        data = cursor.fetchall()
        ls = []
        for i in data:
            if i in ls:
                pass
            else:
                ls.append(i)

        for self.i in range(len(ls)):
            d = {}

            self.dt = []
            for j in range(len(ls)):
                d[f"variable{j}"] = "Hello"
                self.dt.append(list(d.keys()))
            self.dt = self.dt[-1]

    def got_students_details_fromdb(self):

        self.makingvars()

        container = ttk.Frame(self.add_syllabus_attendence_frame)
        canvas = Canvas(container, width=800, height=500)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.place(relx=0.1, rely=0.2)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # fetching data from db to apply attendence ======================================================
        degree_level = self.degree_program_attendence.get()
        class_standard = self.class_standard_attendence.get()
        section_standard = self.section_attendence.get()

        cursor.execute(
            f"SELECT name,lastname,rollno FROM classes_list WHERE class_standard='{class_standard}' AND edu_level='{degree_level}' AND section_name= '{section_standard}'")

        data = cursor.fetchall()
        self.list_of_students_for_attendence = []

        for i in data:
            if i in self.list_of_students_for_attendence:
                pass
            else:
                self.list_of_students_for_attendence.append(i)

        self.variables = []
        # Create the command using partial
        try:
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
        except:
            pass
        print()
        for self.i in range(len(self.list_of_students_for_attendence)):
            self.variable = StringVar()
            self.variables.append(self.variable)

            Label(scrollable_frame, text=self.list_of_students_for_attendence[self.i][0], ).grid(padx=10, pady=10,
                                                                                                 row=self.i,
                                                                                                 column=0)
            Label(scrollable_frame, text=self.list_of_students_for_attendence[self.i][1], ).grid(padx=20, pady=10,
                                                                                                 row=self.i, column=1)
            Label(scrollable_frame, text=self.list_of_students_for_attendence[self.i][2], ).grid(padx=20, pady=10,
                                                                                                 row=self.i, column=2)
            roll_numbers_to_presrnt.append(self.list_of_students_for_attendence[self.i][2])
            # names_of_studenst_for_attendence.clear()
            # lastnames_of_studenst_for_attendence.clear()
            names_of_studenst_for_attendence.append(self.list_of_students_for_attendence[self.i][0])
            lastnames_of_studenst_for_attendence.append(self.list_of_students_for_attendence[self.i][1])

            command = partial(self.function, self.i)

            self.dailyradio1 = ttk.Radiobutton(scrollable_frame, text="Present", variable=self.variable, value="P",
                                               command=command)
            self.dailyradio1.grid(padx=30, pady=10, row=self.i, column=3)
            self.dailyradio2 = ttk.Radiobutton(scrollable_frame, text="Absent", variable=self.variable,
                                               command=command, value="A", )
            self.dailyradio2.grid(padx=30, pady=10, row=self.i, column=4)

            self.dailyradio3 = ttk.Radiobutton(scrollable_frame, text="Leave", variable=self.variable, value="L",
                                               command=command)
            self.dailyradio3.grid(padx=30, pady=10, row=self.i, column=5)
        submit_image = PhotoImage(file=r"button_images/submit_attendence.png")
        self.okbtn1 = Button(self.add_syllabus_attendence_frame, image=submit_image, command=self.submit_attendence,
                             bg="#bfc7c5", activebackground="#bfc7c5", bd=0)
        self.okbtn1.place(relx=0.8, rely=0.9)
        self.okbtn1.image = submit_image

        # self.okbtn = Button(scrollable_frame, text="Check and Submit ", command=command).grid(row=0, column=10)

    def function(self, i):
        self.got = [var.get() for var in self.variables]

    def submit_attendence(self):
        #  institute_level ,class_standard ,section_selected ,teacher_selected ,name ,lastname ,rollno ,status

        fname = []
        lname = []
        rnm = []
        for i in (self.list_of_students_for_attendence):
            fname.append(i[0])
            lname.append(i[1])
            rnm.append(i[2])
        res = msb.askokcancel("Alert", "Are you sure you want to submit the attendance?")
        if res == 1:
            id = str(session_id[0])
            dgre = str(self.degree_program_attendence.get())
            cls = str(self.class_standard_attendence.get())
            sctn = str(self.section_attendence.get())

            query = "INSERT INTO students_attendence_done(teacher_id  ,institute_level ,class_standard ,section_selected  ,student_firstname ,student_lastname ,rollno ,date ,time ,status )VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            for i in range(len(self.list_of_students_for_attendence)):
                cursor.execute(query, (
                    id, dgre, cls, sctn, fname[i], lname[i], rnm[i], datetime.now().strftime('%d-%m-%Y'),
                    datetime.now().strftime('%I:%M:%S %p'), self.got[i]))
                db.commit()
            msb.showinfo("Congratulation", "Success")
            fname.clear()
            lname.clear()
            rnm.clear()
            self.list_of_students_for_attendence.clear()
        else:
            pass

    #  let the teacher see the list of his subjects and the schedules =======================================================

    def show_schedules_selected(self, i):
        try:
            for widget in self.scrollable_frame_for_class_add_right.winfo_children():
                widget.destroy()
        except:
            pass
        frames_list = []

        # wid = self.scrollable_frame_for_class_add_right.winfo_reqwidth()
        self.list_for_announcement_checkboxes = []

        self.views_list_values = []
        self.cbVariables = {}

        cursor.execute(
            f"SELECT date,content,id FROM schedules WHERE subject_class='{i[0]}' AND course_name='{i[1]}' AND subject_code='{i[2]}' AND session_id={session_id[0]} ORDER BY id ASC ")
        result = cursor.fetchall()
        cursor.execute(
            f"SELECT subject_class ,course_name,subject_code,session_id FROM schedules WHERE subject_class='{i[0]}' AND course_name='{i[1]}' AND subject_code='{i[2]}' AND session_id={session_id[0]}")
        new_result = cursor.fetchall()
        self.course_details_for_upate_checkbox = []

        # select the status of all the syllabus of specific book to set up in checkboxes
        cursor.execute(
            f"SELECT status FROM schedules where subject_class='{i[0]}' AND course_name='{i[1]}' AND subject_code='{i[2]}' AND session_id={session_id[0]} ORDER BY id ASC")
        status = cursor.fetchall()
        self.states_of_checkboxes_for_syllabus_schedules = []
        for i in status:
            self.states_of_checkboxes_for_syllabus_schedules.append(i)
        print(self.states_of_checkboxes_for_syllabus_schedules, "length of status checkbox")

        for k in new_result:
            self.course_details_for_upate_checkbox.clear()

            if k not in self.course_details_for_upate_checkbox:
                self.course_details_for_upate_checkbox.append(k)
        print(self.course_details_for_upate_checkbox)
        for i in range(len(result)):
            frames_list.append(Frame(self.scrollable_frame_for_class_add_right, width=1000))
        for j in range(len(frames_list)):

            if j % 2 == 0:
                frames_list[j]['bg'] = '#6f7571'
            else:
                frames_list[j]['bg'] = '#6f7571'

            # frames_list[j].grid(row=j,column=0,padx=(10, 50),sticky='we',ipadx=100)
            frames_list[j].pack(fill='x', pady=5, ipadx=340)

        # print(len(frames_list),"len of frames list")
        ls = []
        for i in range(len(frames_list)):
            ls.append('selected')
        for k in range(len(frames_list)):
            print("this is k", k)

            self.cbVariables[k] = StringVar()
            self.list_for_announcement_checkboxes.append(
                ttk.Checkbutton(frames_list[k], variable=self.cbVariables[k]
                                , onvalue='check' + str(k), offvalue='uncheck' + str(k),
                                command=partial(self.get_check_values_syllabus, (self.cbVariables[k], k))))
            self.list_for_announcement_checkboxes[k].pack(side=RIGHT)

            if str(self.states_of_checkboxes_for_syllabus_schedules[k][0]).startswith("sel"):
                print("k=", k)
                self.list_for_announcement_checkboxes[k].state(['selected'])

            # print(self.states_of_checkboxes_for_syllabus_schedules[k])

            self.label_date = Label(frames_list[k], text=result[k][0], bg='#6f7571', fg='white')
            self.label_date.pack(side=LEFT, pady=5)

            self.label_content = Label(frames_list[k], text=result[k][1], wraplength=200, bg='#6f7571', fg='white')
            self.label_content.pack(anchor=CENTER, pady=5)

            self.label_date.config(bg='#6f7571')
            self.label_content.config(bg='#6f7571')
            cursor.execute(
                f"select id FROM schedules  WHERE  subject_class='{self.course_details_for_upate_checkbox[0][0]}' AND course_name='{self.course_details_for_upate_checkbox[0][1]}'AND subject_code='{self.course_details_for_upate_checkbox[0][2]}' AND session_id='{self.course_details_for_upate_checkbox[0][3]}' LIMIT 1")

            res = cursor.fetchone()
            print(res)
            self.res_id = []
            for i in res:
                self.res_id.clear()
                if i not in self.res_id:
                    # print(i[0],"///////////")
                    self.res_id.append(i)
            print("count is", self.res_id)

    def get_check_values_syllabus(self, i):
        print(i[0], i[1])
        print("result is ", self.res_id)
        print(self.course_details_for_upate_checkbox)
        if i[1] == 0:
            if str(i[0].get()).startswith('c'):
                cursor.execute(
                    f"UPDATE schedules  SET  status = 'selected' WHERE id = 1 AND subject_class='{self.course_details_for_upate_checkbox[0][0]}' AND course_name='{self.course_details_for_upate_checkbox[0][1]}'AND subject_code='{self.course_details_for_upate_checkbox[0][2]}' AND session_id='{self.course_details_for_upate_checkbox[0][3]}'")
                db.commit()
                print("updated success")
                print(int(i[1] - (i[1] / 2)) + 1, "checked")
            if i[0].get().startswith('u'):
                cursor.execute(
                    f"UPDATE schedules  SET  status = 'unselected' WHERE id = 1 AND subject_class='{self.course_details_for_upate_checkbox[0][0]}' AND course_name='{self.course_details_for_upate_checkbox[0][1]}'AND subject_code='{self.course_details_for_upate_checkbox[0][2]}' AND session_id='{self.course_details_for_upate_checkbox[0][3]}'")
                db.commit()

                print("updated")

        if i[1] > 0:

            if str(i[0].get()).startswith('c'):
                print(i[0].get())
                print("entring in c")
                print("id = ", int(i[1] / 2) + 1)
                cursor.execute(
                    f"UPDATE schedules  SET  status = 'selected' WHERE id = '{int(self.res_id[0]) + i[1]}' AND subject_class='{self.course_details_for_upate_checkbox[0][0]}' AND course_name='{self.course_details_for_upate_checkbox[0][1]}'AND subject_code='{self.course_details_for_upate_checkbox[0][2]}' AND session_id='{self.course_details_for_upate_checkbox[0][3]}'")
                print(int(i[1] / 2) + 1)
                db.commit()
                print("updated")
                print(int(i[1] - (i[1] / 2)) + 1, "checked")
            if i[0].get().startswith('u'):
                cursor.execute(
                    f"UPDATE schedules  SET  status = 'unselected' WHERE id = '{int(self.res_id[0]) + i[1]}' AND subject_class='{self.course_details_for_upate_checkbox[0][0]}' AND course_name='{self.course_details_for_upate_checkbox[0][1]}'AND subject_code='{self.course_details_for_upate_checkbox[0][2]}' AND session_id='{self.course_details_for_upate_checkbox[0][3]}'")
                db.commit()
                print(int(i[1] / 2) + 1)
                print("updated success uncheck")

            # print(self.cbVariables[i].get())
        # if (i>0):
        #     i=i-(i/2)
        #
        #     print(self.cbVariables[i].get())
        # if i==0:
        #     print(i)
        # if i>=3:
        #     i=i-1
        #     print(i)

    def destroy_syllabus_by_professors(self):
        self.viwe_syllabus_frame.destroy()
        self.main_manu_widgets()
        self.view_syllabus_backbtn.destroy()

    def view_syllabus_by_professors(self):

        self.main_menu_buttons_frame.destroy()
        self.viwe_syllabus_frame = LabelFrame(root, bg='#bfc7c5', bd=0, width=screenwidth - 500,
                                              height=screenheight - 250,
                                              font=("arial", 15, "bold"))

        self.viwe_syllabus_frame.pack(anchor=CENTER, expand=1, fill=BOTH)
        self.view_syllabus_backbtn = Button(root, text="Back <-", bd=1, bg='white',
                                            command=self.destroy_syllabus_by_professors)
        self.view_syllabus_backbtn.place(x=5, y=7)

        # adding internal frames to main_frame
        ######################################################################################################################

        #   left frame to show list of subjects

        view_syllabus_frame_width = self.viwe_syllabus_frame.winfo_reqwidth()
        # remaining_after_left = view_syllabus_frame_width - (view_syllabus_frame_width)

        add_subject_container_ = ttk.Frame(self.viwe_syllabus_frame)
        canvas_classes_create = Canvas(add_subject_container_, width=view_syllabus_frame_width / 3,
                                       height=screenheight - 100, bg='#bfc7c5')
        scrollbar_for_classes_create = ttk.Scrollbar(add_subject_container_, orient="vertical",
                                                     command=canvas_classes_create.yview)
        scrollable_frame_for_class_add = ttk.Frame(canvas_classes_create)
        scrollable_frame_for_class_add.bind("<Configure>", lambda e: canvas_classes_create.configure(
            scrollregion=canvas_classes_create.bbox("all")))
        canvas_classes_create.create_window((0, 0), window=scrollable_frame_for_class_add, anchor="nw")
        canvas_classes_create.configure(yscrollcommand=scrollbar_for_classes_create.set)
        add_subject_container_.place(relx=0, rely=0.02)
        canvas_classes_create.pack(side="left", fill="both", expand=True)
        scrollbar_for_classes_create.pack(side="right", fill="y")

        cursor.execute(
            f"SELECT subject_class,course_name, subject_code  FROM schedules WHERE session_id={session_id[0]} ")

        result = cursor.fetchall()
        subjects_lists = set(result)
        for i in subjects_lists:
            btn = Button(scrollable_frame_for_class_add, width=50, bd=0, bg="#bfc7c5",
                         text=f"{i[0] + ' ' + i[1] + ' ' + i[2]}",
                         command=partial(self.show_schedules_selected, i))
            btn.pack(fill=X, pady=5)
            btn.config(relief=GROOVE)

        #################
        view_syllabus_frame_width = self.viwe_syllabus_frame.winfo_reqwidth()
        remaining_after_left = view_syllabus_frame_width - (view_syllabus_frame_width)

        add_subject_container_right = ttk.Frame(self.viwe_syllabus_frame)
        canvas_classes_create_right = Canvas(add_subject_container_right, width=1000,
                                             height=screenheight - 100, bg='#bfc7c5')

        scrollbar_for_classes_create = ttk.Scrollbar(add_subject_container_right, orient="vertical",
                                                     command=canvas_classes_create_right.yview)

        self.scrollable_frame_for_class_add_right = ttk.Frame(canvas_classes_create_right)

        self.scrollable_frame_for_class_add_right.bind("<Configure>",
                                                       lambda e: canvas_classes_create_right.configure(
                                                           scrollregion=canvas_classes_create_right.bbox("all")))
        canvas_classes_create_right.create_window((0, 0), window=self.scrollable_frame_for_class_add_right,
                                                  anchor="nw")

        canvas_classes_create_right.configure(yscrollcommand=scrollbar_for_classes_create.set)

        add_subject_container_right.place(relx=0.25, rely=0.02)
        canvas_classes_create_right.pack(side="left", fill="both", expand=True)

        scrollbar_for_classes_create.pack(side="right", fill="y")

    # sms ====================================================================================================
    def create_top_level_to_show_sms_schedule(self, i):
        temp = Toplevel(root, width=800, height=500)
        temp.transient(root)

        entery3 = Entry(temp, font=("arial", 13), bd=1)
        entery3.grid(row=0, column=0, )
        entery3.insert(0, i[2])

        entery4 = Entry(temp, font=("arial", 13), bd=1)
        entery4.grid(row=0, column=1)
        entery4.insert(0, i[3])

        entery5 = Entry(temp, font=("arial", 13), bd=1)
        entery5.grid(row=2, column=0)
        entery5.insert(0, i[4])

        entery6 = Entry(temp, font=("arial", 13), bd=1)
        entery6.grid(row=2, column=1)
        entery6.insert(0, i[5])

        syl = Text(temp, wrap=WORD, bd=2)
        syl.grid(row=3, column=0, columnspan=2)
        syl.insert('1.0', i[6])

    def cance_and_exit(self):

        # self.cancel_and_exit_btn.destroy()
        self.cancel_and_exit_btn.destroy()
        self.scrollable_frame_for_sms_schedule.destroy()
        self.main_manu_widgets()

    def send_sms_today_function(self):

        self.main_menu_buttons_frame.destroy()

        # send_sms_img = PhotoImage(file=r"button_images/send_schedule_for_today.png")

        # cancel_and_exit = PhotoImage(file=r"button_images/cancel_and_exit.png")
        self.cancel_and_exit_btn = Button(root, text="Back <-", bd=1, bg='white', command=self.cance_and_exit)
        # self.cancel_and_exit_btn.image = cancel_and_exit
        self.cancel_and_exit_btn.place(x=5, y=7)

        container = ttk.Frame(root)
        canvas = Canvas(container, width=1000, height=500)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame_for_sms_schedule = ttk.Frame(canvas)

        self.scrollable_frame_for_sms_schedule.bind("<Configure>",
                                                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame_for_sms_schedule, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.place(relx=0.2, rely=0.2)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        cursor.execute(f"select * from sent_schedules_list WHERE schedule_id='{session_id[0]}'")
        data = cursor.fetchall()
        print(session_id[0])
        print(data)

        # dumy = Label(self.scrollable_frame_for_sms_schedule,text="", font=("arial", 13), bd=0,)
        # dumy.grid(row=0, column=0)

        name = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13, "bold"), bd=0)
        name.insert(END, "Name")
        name.config(state='readonly', )
        name.grid(row=0, column=1, )

        mobile = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13, "bold"), bd=0)
        mobile.insert(END, "Mobile")
        mobile.config(state='readonly', )
        mobile.grid(row=0, column=2)

        subject = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13, "bold"), bd=0)
        subject.insert(END, "Subject")
        subject.config(state='readonly', )
        subject.grid(row=0, column=3)

        # clas = Label(self.scrollable_frame_for_sms_schedule,text="Class", font=("arial", 13), bd=0)
        # clas.grid(row=0, column=4)

        clas = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13, "bold"), bd=0)
        clas.insert(END, "Date")
        clas.config(state='readonly', )
        clas.grid(row=0, column=4)

        course = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13, "bold"), bd=0)
        course.insert(END, "Schedule")
        course.config(state='readonly', )
        course.grid(row=0, column=5)

        for i in range(len(data)):

            entery1 = Button(self.scrollable_frame_for_sms_schedule, fg='blue', text="Details",
                             font=("arial 13 underline",), bd=0,
                             command=partial(self.create_top_level_to_show_sms_schedule, data[i]))
            entery1.grid(row=i + 1, column=0)

            entery3 = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13), bd=0)
            entery3.grid(row=i + 1, column=1)
            entery3.insert(0, data[i][2])

            entery4 = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13), bd=0)
            entery4.grid(row=i + 1, column=2)
            entery4.insert(0, data[i][3])

            entery5 = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13), bd=0)
            entery5.grid(row=i + 1, column=3)
            entery5.insert(0, data[i][4])

            entery6 = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13), bd=0)
            entery6.grid(row=i + 1, column=4)
            entery6.insert(0, data[i][5])

            entery7 = Entry(self.scrollable_frame_for_sms_schedule, font=("arial", 13), bd=0)
            entery7.grid(row=i + 1, column=5)
            entery7.insert(0, data[i][6])

            if i % 2 != 0:

                entery3.config(state='readonly', readonlybackground="#b8b4a9")
                entery4.config(state='readonly', readonlybackground="#b8b4a9")
                entery5.config(state='readonly', readonlybackground="#b8b4a9")
                entery6.config(state='readonly', readonlybackground="#b8b4a9")
                entery7.config(state='readonly', readonlybackground="#b8b4a9")

            else:

                entery3.config(state='readonly', )
                entery4.config(state='readonly', )
                entery5.config(state='readonly', )
                entery6.config(state='readonly', )
                entery7.config(state='readonly', )

    def show_announcements(self):

        self.main_menu_buttons_frame.destroy()
        self.back_button_from_announcements = Button(root, text="Back <-", bd=1, bg='white',
                                                     command=self.destroy_announcments)
        self.back_button_from_announcements.place(x=5, y=7)
        self.announcements_frame = LabelFrame(root, bg="#bfc7c5", bd=0, width=screenwidth - 300,
                                              height=screenheight - 300,
                                              font=("arial", 15, "bold"))

        #############################################################################################################

        canvas = Canvas(self.announcements_frame, width=1100, height=550)
        scrollbar = ttk.Scrollbar(self.announcements_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # variable for checkbox below
        # add content to scrollable frame
        self.date_of_announcement = Label(scrollable_frame, text="Date", font=("arial", "13", "bold"))
        self.date_of_announcement.grid(row=0, column=0, padx=(20, 20))

        self.heading_of_announcement = Label(scrollable_frame, text="Purpose", font=("arial", "13", "bold"))
        self.heading_of_announcement.grid(row=0, column=1, padx=(100, 100))

        self.body_of_announcement = Label(scrollable_frame, text="Body", font=("arial", "13", "bold"), wraplength=500)
        self.body_of_announcement.grid(row=0, column=2, padx=(100, 100))

        # checkbox list

        cursor.execute("select * from Announcements WHERE show_ann='selected' ")
        data = cursor.fetchall()
        print(data)
        for i in range(len(data)):
            self.date_of_announcement_value = Label(scrollable_frame, text=str(data[i][2]))
            self.date_of_announcement_value.grid(row=i + 1, column=0, padx=(20, 20))

            self.heading_of_announcement_value = Label(scrollable_frame, text=str(data[i][1]))
            self.heading_of_announcement_value.grid(row=i + 1, column=1, padx=(100, 100), )

            self.body_of_announcement_value = Label(scrollable_frame, text=str(data[i][3]), wraplength=200)
            self.body_of_announcement_value.grid(row=i + 1, column=2, padx=(100, 100))

        canvas.pack(side="left", fill="both", expand=True)
        self.announcements_frame.pack(padx=50, pady=100, anchor=CENTER, )

        scrollbar.pack(side="right", fill="y")

        #############################################################################################################

        # dumy labels

    def destroy_announcments(self):
        self.announcements_frame.destroy()
        self.main_manu_widgets()
        self.back_button_from_announcements.destroy()


obj = admin()
root.mainloop()
