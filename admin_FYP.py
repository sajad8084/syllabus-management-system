from datetime import datetime
from tkinter import *
import sqlite3
from tkinter import ttk
from tksheet import Sheet
from tkinter import Menu
import psycopg2
from twilio.rest import Client
import tkinter.messagebox as msb
from functools import partial
import tkcalendar
from PIL import Image, ImageTk

root = Tk()

frame = Frame(root)
frame.pack()
#
uni_name_label = Label(frame, text="Information Technology department", bg='#003B6D', fg='#bfc7c5',
                       font=("Times", "24", "bold italic"))
uni_name_label.pack(anchor=CENTER, side=TOP)
#
# status_label = Label(frame, text="                            ", font=("Times", "24", "bold italic"),bg='white')
# status_label.pack(anchor=CENTER, side=TOP)
#
root.config(bg="#003B6D")
# root.iconify("uni_log/arred_logo.ico")
root.iconbitmap('uni_logo/Hazara_University_logo.ico')

root.title("Hazara University ")

root.geometry('1600x900')
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
font_family = ("arial", 15, 'bold')
style = ttk.Style()

session_id = []

selection_class_list = []
# back button image use in all pages
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

#
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
'''
msb.showerror("Error", "Not Connected to Database")
ask_db_var = msb.askyesno("", "Do You want to create a database?")
if ask_db_var == 1:

        database_toplevel = Toplevel(root,width=600,height=500)

        host_label = Label(database_toplevel, text="username", bg='#bfc7c5', fg="#1a1309",
                                         font=('', 10, 'bold'))
        host_label.grid(row=0,column=1)
        database_label = Label(database_toplevel, text="password", bg='#bfc7c5', fg="#1a1309",
                                    font=('arial', 10, 'bold'), )
        database_label.grid(row=1,column=1)

        user_label = Label(database_toplevel, text="username", bg='#bfc7c5', fg="#1a1309",
                                         font=('', 10, 'bold'))
        user_label.grid(row=2,column=1)
        password_label = Label(database_toplevel, text="password", bg='#bfc7c5', fg="#1a1309",
                                    font=('arial', 10, 'bold'), )
        password_label.grid(row=3,column=1)

        # entries
        host_entry = Entry(database_toplevel, width=15, font=font_family)
        host_entry.grid(row=0,column=2, )
        host_entry.focus()

        database_entry = Entry(database_toplevel, width=15, font=font_family)
        database_entry.grid(row=1,column=2,)

        database_entry = Entry(database_toplevel, width=15, font=font_family)
        database_entry.grid(row=2,column=2,)

        database_entry = Entry(database_toplevel, width=15, font=font_family)
        database_entry.grid(row=3,column=2)


'''

# lists to store data of program  ***************** **********
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

# database tables     ************* ******************


class admin:
    def __init__(self):
        self.login()
        self.database_tables()


    def database_tables(self):
        # cursor.execute("CRETE TABLE IF NOT EXISTS database_credentials (db_name TEXT ,host TEXT ,database TEXT,user TEXT,password TEXT )")


        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY , full_name TEXT ,mobile TEXT, email TEXT , gender TEXT, password TEXT ,signup_date DATE NOT NULL,time TEXT) ")

        # cursor.execute("ALTER TABLE users ADD address TEXT")
        # cursor.execute("ALTER TABLE users ADD department TEXT")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS subjects_created(id SERIAL PRIMARY KEY , subject_name TEXT,subject_code TEXT,subject_author TEXT,subject_program TEXT,subject_standard TEXT, course_type TEXT)")
        # lists of subjects

        # schedules for courses
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS schedules(id SERIAL PRIMARY KEY,session_id INTEGER,schedule_type TEXT,course_name TEXT,subject_class TEXT,subject_code TEXT,date TEXT ,content TEXT,status TEXT)")
        # classes
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS classes_list(id SERIAL PRIMARY KEY,edu_level TEXT,class_standard TEXT ,section_name TEXT,name TEXT,lastname TEXT,rollno INTEGER )")

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS courses(id SERIAL PRIMARY KEY, name TEXT,code TEXT,author TEXT,program TEXT,class TEXT, type TEXT ,content TEXT)')

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS assigned_subjects_teachers(id SERIAL PRIMARY KEY,teacher_id INTEGER,institute_level TEXT, class_standard TEXT , "
            "section_selected TEXT, subject_selected TEXT , teacher_selected TEXT  )")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS students_attendence_done(id SERIAL PRIMARY KEY, teacher_id TEXT ,institute_level TEXT,class_standard TEXT,section_selected  TEXT,student_firstname TEXT,student_lastname TEXT,rollno TEXT ,date TEXT ,time TEXT,status TEXT)")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS sent_schedules_list(id SERIAL PRIMARY KEY,schedule_id TEXT,fulll_name TEXT,mobile TEXT,subject TEXT,date TEXT,content TEXT)")

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Announcements(id SERIAL PRIMARY KEY,heading TEXT ,date TEXT , body TEXT, show_ann TEXT)""")

        db.commit()

    # login function ************************************************************************************************
    def login(self):

        self.login_frame = LabelFrame(root, text="Login ", bg='#bfc7c5', width=400, height=300,
                                      font=("arial", 15, "bold"))
        self.login_frame.place(relx=.5, rely=.5, anchor=CENTER)


        # create the login icons===========================================================
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
        self.login_usernameentery.insert(0, "nsaba")

        self.login_passwordentery = Entry(self.login_frame, font=font_family)
        self.login_passwordentery.place(anchor=E, relheight=0.10, relwidth=0.50, relx=0.8, rely=0.4)
        self.login_passwordentery.config(show="*")
        self.login_passwordentery.insert(0, "1122")

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

    # sign up function ************************************************************************************************
    def signup(self):
        self.signup_frame = LabelFrame(root, text="Signup", bg='#bfc7c5')
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


        #  new changes
        self.address_of_user = Label(self.signup_frame, text="Address", fg="#1a1309", bg="#bfc7c5",
                                        font=('', 10, 'bold'))
        self.address_of_user.place(anchor=W, relx=0.25, rely=0.8)

        self.dept_of_user = Label(self.signup_frame, text="Department", fg="#1a1309", bg="#bfc7c5",
                                     font=('', 10, 'bold'))
        self.dept_of_user.place(anchor=W, relx=0.25, rely=0.9)




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

        self.address_entery = Entry(self.signup_frame, font=font_family)
        self.address_entery.place(anchor=E, relx=0.7, rely=0.8)
        self.dept_entry = Entry(self.signup_frame, font=font_family)
        self.dept_entry.place(anchor=E, relx=0.7, rely=0.9)

        signupimage = PhotoImage(file=r"button_images/sign_up_image.png")
        exitimage = PhotoImage(file=r"button_images/exit.png")
        self.sign_up_button = Button(self.signup_frame, image=signupimage, bd=0, bg='#bfc7c5', borderwidth=0,
                                     activebackground="#bfc7c5",
                                     command=self.register_user)
        self.sign_up_button.image = signupimage
        self.sign_up_button.place(anchor=E, relx=0.6, rely=1)

        self.Exit_button = Button(self.signup_frame, image=exitimage, bd=0, bg='#bfc7c5', borderwidth=0,
                                  activebackground="#bfc7c5",
                                  command=self.exit_signup)
        self.Exit_button.image = exitimage
        self.Exit_button.place(anchor=E, relx=0.45, rely=1)

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
                    # print(session_id)

        if len(session_id) > 0:

            self.main_manu_widgets()

        else:
            msb.showerror("error", "Wrong Username or password")

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
        address=self.address_entery.get()
        department=self.dept_entry.get()
        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.fullmatch(regex, email)):
            print("Valid Email")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY , full_name TEXT ,mobile TEXT, email TEXT , gender TEXT, password TEXT ,signup_date DATE NOT NULL,time TEXT) ")
        db.commit()
        if fullname == "" or mobile == ""  or gender == "" or gender == "Select a gender" or password == "" or confirm_password == "" or password != confirm_password:

            msb.showerror("Alert", "Something went wrong")
        elif len(password) < 4:
            msb.showerror("Alert", "Input at least four digits for password")
        elif not  re.fullmatch(regex, email):
            msb.showerror("Alert", "wrong email")



        else:

            # now = datetime.now()
            current_time = datetime.now().strftime("%I:%M %p")

            query = "INSERT INTO users(full_name,mobile ,email, gender,password,signup_date,time,address,department)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,
                           (fullname, mobile, email, gender, password, str(datetime.today().date()), str(current_time),address,department))
            db.commit()
            msb.showinfo("Congratulation", "You have been registered successfully")
            self.signup_frame.destroy()
            self.login()

    # make change on size of buttons while hoverover main manu

    # making GUI for the main menu ,buttons to perfrom main actions

    def main_manu_widgets(self):

        self.login_frame.destroy()

        self.main_menu_buttons_frame = LabelFrame(root, bg="#bfc7c5", bd=0, width=screenwidth,
                                                  height=screenheight - 300,
                                                  font=("arial", 15, "bold"))
        self.main_menu_buttons_frame.pack(padx=50, pady=100, anchor=CENTER, expand=1, fill=BOTH)
        self.add_syllabus_img_origanl = Image.open("main_menu_buttons/add_syllabus_menu_btn.png")

        self.add_syllabus_img = ImageTk.PhotoImage(self.add_syllabus_img_origanl)

        self.add_syllabus_btn = Button(self.main_menu_buttons_frame, image=self.add_syllabus_img, bd=0,
                                       bg="#bfc7c5", activebackground="#bfc7c5", command=self.add_syllabus)
        self.add_syllabus_btn.place(relx=0.2, rely=0.09)
        self.add_syllabus_btn.image = self.add_syllabus_img

        self.viwe_syllabus_img = PhotoImage(file=r"main_menu_buttons/view_syllabus.png")

        self.view_syllabus_btn = Button(self.main_menu_buttons_frame, bd=0, image=self.viwe_syllabus_img,
                                        bg="#bfc7c5", activebackground="#bfc7c5",
                                        command=self.view_syllabus_by_professors)
        self.view_syllabus_btn.place(relx=0.50, rely=0.09)
        self.view_syllabus_btn.image = self.viwe_syllabus_img

        tchr_sub_cls_img = PhotoImage(file=r"main_menu_buttons/sub_cls_teacher.png")

        self.view_teachers_btn = Button(self.main_menu_buttons_frame, bd=0, command=self.view_techers_list,
                                        bg="#bfc7c5", activebackground="#bfc7c5", image=tchr_sub_cls_img)
        self.view_teachers_btn.place(relx=0.8, rely=0.09)
        self.view_teachers_btn.image = tchr_sub_cls_img

        # ROW 2
        tchr_sub_cls_img = PhotoImage(file=r"main_menu_buttons/view_attendence.png")

        self.student_attendence_btn = Button(self.main_menu_buttons_frame, bd=0, image=tchr_sub_cls_img,
                                             bg="#bfc7c5", activebackground="#bfc7c5",
                                             command=self.view_attendence_by_professors)
        self.student_attendence_btn.place(relx=0.2, rely=0.5)
        self.student_attendence_btn.image = tchr_sub_cls_img

        announcements_btn = PhotoImage(file=r"main_menu_buttons/view_announcement_1.png")
        self.announcement_btn = Button(self.main_menu_buttons_frame, image=announcements_btn, bd=0, bg="#bfc7c5",
                                       command=self.send_announcements,
                                       activebackground="#bfc7c5")
        self.announcement_btn.place(relx=0.5, rely=0.5)
        self.announcement_btn.image = announcements_btn

        check_schedule = PhotoImage(file=r"main_menu_buttons/sms_notifications.png")
        self.main_settings_btn = Button(self.main_menu_buttons_frame, image=check_schedule, bd=0, bg="#bfc7c5",
                                        activebackground="#bfc7c5",
                                        command=self.send_sms_today_function)
        self.main_settings_btn.place(relx=0.8, rely=0.5)
        self.main_settings_btn.image = check_schedule

    ######################################################################################################################     view syllabus #################

    def open_this(self, i):

        try:
            for widget in self.scrollable_frame_for_class_add_right.winfo_children():
                widget.destroy()
        except:
            pass

        frames_list = []
        # wid = self.scrollable_frame_for_class_add_right.winfo_reqwidth()
        #
        cursor.execute(
            f"SELECT date,content,status,id FROM schedules WHERE subject_class='{i[0]}' AND course_name='{i[1]}' AND subject_code='{i[2]}' ORDER BY id ASC ")
        result = cursor.fetchall()
        for i in range(len(result)):
            frames_list.append(Frame(self.scrollable_frame_for_class_add_right, width=800))
        for j in range(len(frames_list)):
            if j % 2 == 0:
                pass
                # frames_list[j]['bg'] = '#b8b4a9'
            # frames_list[j].grid(row=j,column=0,padx=(10, 50),sticky='we',ipadx=100)
            frames_list[j].pack(fill='x', expand=True,ipadx=350)
        for k in range(len(frames_list)):

            label_date = Label(frames_list[k], text=str(result[k][0]) )
            label_date.pack(side=LEFT)
            label_content = Label(frames_list[k],  text= str(result[k][1]),wraplength=400)
            label_content.pack(padx=10)

            if k % 2 != 0:
                frames_list[k]['bg'] = '#b8b4a9'
                label_date.config(bg="#b8b4a9")
            if result[k][2]=='selected':
                # label_content = 'green'
                label_content.config(bg="green")

            # label_content = Label(frames_list[k], text=result[k][1],bg='white' )
            # label_content.pack(anchor=CENTER)

    def view_syllabus_by_professors(self):

        self.main_menu_buttons_frame.destroy()
        self.viwe_syllabus_frame = LabelFrame(root, highlightbackground="black", highlightcolor="black",
                                              highlightthickness=2, bg='#FFFFFF', bd=0, width=screenwidth - 500,
                                              height=screenheight - 250,
                                              font=("arial", 15, "bold"))

        self.viwe_syllabus_frame.pack(anchor=CENTER, expand=1, fill=BOTH)

        self.view_syllabus_back = Button(root, text="Back <-", relief=FLAT, bg='white', bd=0,
                                         command=self.back_from_syllabus_view, )
        self.view_syllabus_back.place(x=5, y=7)

        ################# left side frame to view syllabus covered

        view_syllabus_frame_width = self.viwe_syllabus_frame.winfo_reqwidth()
        remaining_after_left = view_syllabus_frame_width - (view_syllabus_frame_width)

        add_subject_container_ = ttk.Frame(self.viwe_syllabus_frame)
        canvas_classes_create = Canvas(add_subject_container_, width=view_syllabus_frame_width / 3,
                                       height=screenheight - 200, bg='#bfc7c5')
        scrollbar_for_classes_create = ttk.Scrollbar(add_subject_container_, orient="vertical",
                                                     command=canvas_classes_create.yview)
        scrollable_frame_for_class_add = ttk.Frame(canvas_classes_create)
        scrollable_frame_for_class_add.bind("<Configure>", lambda e: canvas_classes_create.configure(
            scrollregion=canvas_classes_create.bbox("all")))
        canvas_classes_create.create_window((0, 0), window=scrollable_frame_for_class_add, anchor="nw")
        canvas_classes_create.configure(yscrollcommand=scrollbar_for_classes_create.set)
        add_subject_container_.place(relx=0, rely=0.05)
        canvas_classes_create.pack(side="left", fill="both", expand=True)
        scrollbar_for_classes_create.pack(side="right", fill="y")

        cursor.execute(f"SELECT subject_class,course_name, subject_code  FROM schedules ")

        result = cursor.fetchall()
        subjects_lists = set(result)
        for i in subjects_lists:
            btn = Button(scrollable_frame_for_class_add, width=50,
                         text=f"{'Institute: ' + i[0] + ' Subject: ' + i[1] + ' Code: ' + i[2]}",
                         command=partial(self.open_this, i))
            btn.pack(fill=X)
            btn.config(relief=GROOVE)

        ################# right side frame to view syllabus covered

        view_syllabus_frame_width = self.viwe_syllabus_frame.winfo_reqwidth()
        remaining_after_left = view_syllabus_frame_width - (view_syllabus_frame_width)

        add_subject_container_right = ttk.Frame(self.viwe_syllabus_frame)
        canvas_classes_create_right = Canvas(add_subject_container_right, width=900,
                                             height=screenheight - 200, bg='#bfc7c5')
        scrollbar_for_classes_create = ttk.Scrollbar(add_subject_container_right, orient="vertical",
                                                     command=canvas_classes_create_right.yview)
        self.scrollable_frame_for_class_add_right = ttk.Frame(canvas_classes_create_right)
        self.scrollable_frame_for_class_add_right.bind("<Configure>", lambda e: canvas_classes_create_right.configure(
            scrollregion=canvas_classes_create_right.bbox("all")))
        canvas_classes_create_right.create_window((0, 0), window=self.scrollable_frame_for_class_add_right, anchor="nw")
        canvas_classes_create_right.configure(yscrollcommand=scrollbar_for_classes_create.set)
        add_subject_container_right.place(relx=0.25, rely=0.05)
        canvas_classes_create_right.pack(side="left", fill="both", expand=True)
        scrollbar_for_classes_create.pack(side="right", fill="y")

        # 2

        ######################################################################################################################     view attendence #################

        # function called by attendance button

    def back_from_syllabus_view(self):
        self.viwe_syllabus_frame.destroy()
        self.main_manu_widgets()
        self.view_syllabus_back.destroy()

    def destroy_attendence(self):
        self.viwe_attendance_frame.destroy()
        self.main_manu_widgets()
        self.back_button_attendence.destroy()

    def view_attendence_by_professors(self):
        self.main_menu_buttons_frame.destroy()
        self.viwe_attendance_frame = LabelFrame(root, highlightbackground="red", highlightcolor="blue",
                                                highlightthickness=2, bg='#FFFFFF', bd=0, width=screenwidth - 500,

                                                height=screenheight - 300,
                                                font=("arial", 15, "bold"))

        self.viwe_attendance_frame.pack(anchor=CENTER, expand=1, fill=BOTH)
        self.back_button_attendence = Button(root, text="Back <- ", relief=FLAT, bg='white', bd=0,
                                             command=self.destroy_attendence)
        self.back_button_attendence.place(x=5, y=7)

        ################# left side frame to view syllabus covered

        view_syllabus_frame_width = self.viwe_attendance_frame.winfo_reqwidth()
        remaining_after_left = view_syllabus_frame_width - (view_syllabus_frame_width)

        view_syllabus_container_ = ttk.Frame(self.viwe_attendance_frame)
        canvas_classes_create = Canvas(view_syllabus_container_, width=view_syllabus_frame_width / 3,
                                       height=screenheight - 100, bg='#bfc7c5')
        scrollbar_for_classes_create = ttk.Scrollbar(view_syllabus_container_, orient="vertical",
                                                     command=canvas_classes_create.yview)
        self.scrollabel_frame_list_classes = ttk.Frame(canvas_classes_create)
        self.scrollabel_frame_list_classes.bind("<Configure>", lambda e: canvas_classes_create.configure(
            scrollregion=canvas_classes_create.bbox("all")))
        canvas_classes_create.create_window((0, 0), window=self.scrollabel_frame_list_classes, anchor="nw")
        canvas_classes_create.configure(yscrollcommand=scrollbar_for_classes_create.set)
        view_syllabus_container_.place(relx=0, rely=0.02)
        canvas_classes_create.pack(side="left", fill="both", expand=True)
        scrollbar_for_classes_create.pack(side="right", fill="y")

        # cursor.execute(f"SELECT teacher_id ,institute_level ,class_standard ,section_selected,(select full_name from users b where b.id = '{(a.teacher_id)}'   FROM students_attendence_done a ")
        # writing query to filter out attendence subjects
        list_to_store_attendence_temp = []

        ids_to_find_teachers_name = []
        found_teachers_name = []
        final_list_prepared_to_store_attendence = []
        cursor.execute(
            f"SELECT teacher_id ,institute_level ,class_standard ,section_selected FROM students_attendence_done")
        result = cursor.fetchall()
        print('---------------------------',result)


        classes_lists = set(result)


        for i in classes_lists:
            ids_to_find_teachers_name.append(i[0])
        for i in range(len(ids_to_find_teachers_name)):
            cursor.execute(f"SELECT full_name FROM users WHERE id ={ids_to_find_teachers_name[i]}")
            res = cursor.fetchall()
            found_teachers_name.append(res)

        for i, (j, k) in enumerate(zip(classes_lists, found_teachers_name)):
            final_list_prepared_to_store_attendence.append((j[1], j[2], j[3], k[0]))

        self.search_attendence_date = tkcalendar.DateEntry(self.scrollabel_frame_list_classes, selectmode='day',
                                                           date_pattern='dd-mm-y')

        self.search_attendence_date.pack(fill=X)
        for i in range(len(final_list_prepared_to_store_attendence)):
            btn = Button(self.scrollabel_frame_list_classes, width=50, bd=1,
                         text=f"{str(final_list_prepared_to_store_attendence[i][0]) + ' ' + str(final_list_prepared_to_store_attendence[i][1]) + ' ' + str(final_list_prepared_to_store_attendence[i][2]) + ' ' + str(final_list_prepared_to_store_attendence[i][3][0])}",
                         command=partial(self.open_attendence, final_list_prepared_to_store_attendence[i]))
            btn.pack(fill=X, pady=10, )
            btn.config(relief='ridge')

        ## right side frame to view syllabus covered

        view_syllabus_frame_width = self.viwe_attendance_frame.winfo_reqwidth()
        remaining_after_left = view_syllabus_frame_width - (view_syllabus_frame_width)

        add_subject_container_right = ttk.Frame(self.viwe_attendance_frame)
        canvas_classes_create_right = Canvas(add_subject_container_right, width=900,
                                             height=screenheight - 100, bg='#bfc7c5')
        scrollbar_for_classes_create = ttk.Scrollbar(add_subject_container_right, orient="vertical",
                                                     command=canvas_classes_create_right.yview)
        self.scrollable_frame_to_show_attendence = ttk.Frame(canvas_classes_create_right)
        self.scrollable_frame_to_show_attendence.bind("<Configure>", lambda e: canvas_classes_create_right.configure(
            scrollregion=canvas_classes_create_right.bbox("all")))
        canvas_classes_create_right.create_window((0, 0), window=self.scrollable_frame_to_show_attendence, anchor="nw")
        canvas_classes_create_right.configure(yscrollcommand=scrollbar_for_classes_create.set)
        add_subject_container_right.place(relx=0.25, rely=0.02)
        canvas_classes_create_right.pack(side="left", fill="both", expand=True)
        scrollbar_for_classes_create.pack(side="right", fill="y")

    def open_attendence(self, i):
        try:
            for widget in self.scrollable_frame_to_show_attendence.winfo_children():
                widget.destroy()
        except:
            pass
        cursor.execute(
            f"SELECT student_firstname,student_lastname,rollno ,status FROM students_attendence_done WHERE institute_level='{i[0]}' AND class_standard='{i[1]}' AND section_selected='{i[2]}' AND date='{self.search_attendence_date.get()}'")
        result = cursor.fetchall()

        firsname_label = Label(self.scrollable_frame_to_show_attendence, text="First Name", bd=0)
        firsname_label.grid(row=0, column=0, padx=(100, 30), pady=(30, 0))

        last_label = Label(self.scrollable_frame_to_show_attendence, text="Last Name", )
        last_label.grid(row=0, column=1, padx=(60, 30), pady=(30, 0))

        rollno_label = Label(self.scrollable_frame_to_show_attendence, text="Roll Name", )
        rollno_label.grid(row=0, column=2, padx=(60, 30), pady=(30, 0))

        precence_status_label = Label(self.scrollable_frame_to_show_attendence, text="Status", )
        precence_status_label.grid(row=0, column=3, padx=(75, 30), pady=(30, 0))
        # entris to show table for attendence ****************************

        for i in range(len(result)):
            firsname_entery = Entry(self.scrollable_frame_to_show_attendence, bd=0, )
            firsname_entery.grid(row=i + 1, column=0, padx=(75, 30), pady=(30, 0))
            firsname_entery.insert(0, result[i][0])

            last_name_enery = Entry(self.scrollable_frame_to_show_attendence, bd=0, )
            last_name_enery.grid(row=i + 1, column=1, padx=(75, 30), pady=(30, 0))
            last_name_enery.insert(0, result[i][1])
            last_name_enery.config(state='readonly')

            rollno_enery = Entry(self.scrollable_frame_to_show_attendence, bd=0, )
            rollno_enery.grid(row=i + 1, column=2, padx=(75, 30), pady=(30, 0))
            rollno_enery.insert(0, result[i][2])
            rollno_enery.config(state='readonly')

            precence_status_entery = Entry(self.scrollable_frame_to_show_attendence, bd=0, )
            precence_status_entery.grid(row=i + 1, column=3, padx=(60, 30), pady=(30, 0))
            precence_status_entery.insert(0, result[i][3])

            if i % 2 == 0:
                firsname_entery.config(state='readonly', readonlybackground="#bfc7c5")
                last_name_enery.config(state='readonly', readonlybackground="#bfc7c5")
                rollno_enery.config(state='readonly', readonlybackground="#bfc7c5")
                precence_status_entery.config(state='readonly', readonlybackground="#bfc7c5")
            else:
                firsname_entery.config(state='readonly', readonlybackground="#FFFFFF")
                last_name_enery.config(state='readonly', readonlybackground="#FFFFFF")
                rollno_enery.config(state='readonly', readonlybackground="#FFFFFF")
                precence_status_entery.config(state='readonly', readonlybackground="#FFFFFF")

    ######################################################################################################################

    # ======================================= add syllabus to database ===============================
    def destroy_syllabus_add(self):
        self.add_syllabus_frame.destroy()
        self.main_manu_widgets()
        self.add_syllabus_backbtn.destroy()

    def add_syllabus(self):

        self.main_menu_buttons_frame.destroy()

        self.add_syllabus_frame = LabelFrame(root, highlightbackground="black", highlightcolor="black",
                                             highlightthickness=1, bg='#bfc7c5', bd=0, width=screenwidth - 500,
                                             height=screenheight - 250,
                                             font=("arial", 15, "bold"))

        self.add_syllabus_frame.pack(padx=50, pady=50, anchor=CENTER, expand=1, fill=BOTH)
        self.add_syllabus_backbtn = Button(root, text="Back", relief=FLAT, bg='white', bd=0,
                                           command=self.destroy_syllabus_add)
        self.add_syllabus_backbtn.place(x=5, y=7)

        # definig internal frame

        self.add_syllabus_frame_internal = LabelFrame(self.add_syllabus_frame, highlightbackground="black",
                                                      highlightcolor="black",
                                                      highlightthickness=2, bg="#bfc7c5", bd=0, width=screenwidth - 500,
                                                      height=screenheight - 700, font=("arial", 15, "bold"))
        self.add_syllabus_frame_internal.pack(padx=20, pady=10, expand=1, anchor=N)

        # =============================================     search course id

        # ==============================================defining buttons
        addcourse_img = PhotoImage(file=r"button_images/add_course1.png")
        self.add_course_btn = Button(self.add_syllabus_frame_internal, image=addcourse_img, bd=0, bg="#bfc7c5",
                                     activebackground="#bfc7c5",
                                     command=self.get_results_of_subjects_course_add)
        self.add_course_btn.place(relx=0.7, rely=0.4)
        self.add_course_btn.image = addcourse_img

        # clear_img = PhotoImage(file=r"button_images/clear_all.png")
        # self.clear_course_btn = Button(self.add_syllabus_frame_internal, bd=0, bg="#bfc7c5", image=clear_img)
        # self.clear_course_btn.place(relx=0.65, rely=0.6)
        # self.clear_course_btn.image = clear_img

        cancel_img = PhotoImage(file=r"button_images/cancel.png")
        self.quit_course_btn = Button(self.add_syllabus_frame_internal, image=cancel_img, bd=0, bg="#bfc7c5",
                                      activebackground="#bfc7c5", )
        self.quit_course_btn.place(relx=0.85, rely=0.55)
        self.quit_course_btn.image = cancel_img

        # making entries for syllabus
        self.degree_program_syllabus_create = ttk.Combobox(self.add_syllabus_frame_internal, state="readonly", width=12,
                                                           font=("arial", 12))
        self.degree_program_syllabus_create['values'] = ("Select a program", "University")
        self.degree_program_syllabus_create.current(0)
        self.degree_program_syllabus_create.bind("<<ComboboxSelected>>",
                                                 lambda _: self.get_results_of_institute_course_add())
        self.degree_program_syllabus_create.place(relx=0.02, rely=0.1)
        #
        self.class_selectoin_syllabus_create = ttk.Combobox(self.add_syllabus_frame_internal, state="readonly",
                                                            width=10,
                                                            font=("arial", 12))
        self.class_selectoin_syllabus_create.place(relx=0.2, rely=0.1)

        self.class_selectoin_syllabus_create.bind("<<ComboboxSelected>>",
                                                  lambda _: self.get_results_of_class_standard_course_add())

        self.list_subjects_syllabus_create = ttk.Combobox(self.add_syllabus_frame_internal, state="readonly", width=10,
                                                          font=("arial", 12))

        self.list_subjects_syllabus_create.bind("<<ComboboxSelected>>",
                                                lambda _: self.show_further_info())
        self.list_subjects_syllabus_create.place(relx=0.4, rely=0.1)

        self.syllabus_box = Text(self.add_syllabus_frame, width=135, height=45, wrap=WORD, highlightbackground="black",
                                 highlightcolor="black",
                                 highlightthickness=1)

        self.syllabus_box.pack(padx=30, pady=50)
        self.syllabus_box.bind('<FocusIn>', lambda e: self.get_focusin_of_syllabus_textbox(e))
        self.syllabus_box.bind('<FocusOut>', lambda e: self.get_focusout_of_syllabus_textbox(e))

        self.syllabus_box.insert("1.0",
                                 "Separate the chapter with # , e.g Chapter#1,Chapter#2 Separate the topics with a comma.")

        # function to select class level from drop down.

    def get_focusin_of_syllabus_textbox(self, e):

        test = 'Separate the chapter with # , e.g Chapter#1,Chapter#2 Separate the topics with a comma.'
        current = self.syllabus_box.get("1.0", END)
        if self.syllabus_box.focus_get():
            if current.startswith("Separate the chapter"):
                self.syllabus_box.delete("1.0", END)

    def get_focusout_of_syllabus_textbox(self, e):
        pass

    def get_results_of_institute_course_add(self):

        isntitute_level = self.degree_program_syllabus_create.get()

        cursor.execute(
            f"SELECT DISTINCT  id, subject_standard FROM subjects_created WHERE subject_program='{isntitute_level}' ORDER BY id DESC")
        got_standard = cursor.fetchall()
        statndard_list = ["Select a class"]
        for i in got_standard:
            if i[1] not in statndard_list:
                statndard_list.append(i[1])
        print(statndard_list)
        self.class_selectoin_syllabus_create['values'] = (statndard_list)
        self.class_selectoin_syllabus_create.current(0)

        # select subject from drop down

    def get_results_of_class_standard_course_add(self):

        class_standard_for_program = self.class_selectoin_syllabus_create.get()
        print("this is it")

        cursor.execute(
            f"SELECT subject_name FROM subjects_created WHERE subject_standard='{class_standard_for_program}' ORDER BY cast(id as int)")
        got_classes = cursor.fetchall()
        print("got_classes==",got_classes)
        classes_list = ["Select a Subject"]
        for i in got_classes:
            classes_list.append(i[0])

        self.list_subjects_syllabus_create['values'] = (classes_list)
        self.list_subjects_syllabus_create.current(0)

        # show remaining details of subject.

    def show_further_info(self):
        isntitute_level = self.degree_program_syllabus_create.get()
        class_standard_for_program = self.class_selectoin_syllabus_create.get()
        subject_selected = self.list_subjects_syllabus_create.get()
        cursor.execute(
            f"SELECT subject_code, subject_author,course_type FROM subjects_created WHERE  subject_program='{isntitute_level}' AND subject_standard='{class_standard_for_program}' AND subject_name='{subject_selected}'   ")
        self.results_of_subject_to_add_syllabus = cursor.fetchall()

        if len(self.results_of_subject_to_add_syllabus) >= 1:
            try:

                self.course_code_label_course_insert.config(text='')
                self.course_auther_label_course_insert.config(text='')
                self.course_type_label_course_insert.config(text='')
            except:
                pass

            self.course_code_label_course_insert = Label(self.add_syllabus_frame_internal,
                                                         text=f"Course Code :{self.results_of_subject_to_add_syllabus[0][0]}")
            self.course_code_label_course_insert.place(relx=0.55, rely=0.2)

            self.course_auther_label_course_insert = Label(self.add_syllabus_frame_internal,
                                                           text=f"Auther :{self.results_of_subject_to_add_syllabus[0][1]}")
            self.course_auther_label_course_insert.place(relx=0.7, rely=0.2)

            self.course_type_label_course_insert = Label(self.add_syllabus_frame_internal,
                                                         text=f"Rec/Ref :{self.results_of_subject_to_add_syllabus[0][2]}")
            self.course_type_label_course_insert.place(relx=0.8, rely=0.2)
        else:
            msb.showerror("", " Something happened wrong")
            self.course_code_label_course_insert.config(text='')
            self.course_auther_label_course_insert.config(text='')
            self.course_type_label_course_insert.config(text='')

        cursor.execute(
            f"SELECT content  FROM courses WHERE name='{self.list_subjects_syllabus_create.get()}' AND program='{self.degree_program_syllabus_create.get()}' AND class='{self.class_selectoin_syllabus_create.get()}'")

        data = cursor.fetchall()
        print(data)
        if data:
            try:
                self.syllabus_box.delete("1.0", END)
                self.syllabus_box.insert("1.0", data[0])

                # update button
                update_image = PhotoImage(file=r"button_images/update_image.png")
                self.clear_course_btn = Button(self.add_syllabus_frame_internal, bd=0, bg="#bfc7c5", image=update_image,
                                               command=self.update_syllabus)
                self.clear_course_btn.place(relx=0.7, rely=0.6)
                self.clear_course_btn.image = update_image
                self.add_course_btn.destroy()
            except:
                pass

        else:
            try:
                self.clear_course_btn.destroy()
                self.add_course_btn.destroy()
            except:
                pass

            addcourse_img = PhotoImage(file=r"button_images/add_course1.png")
            self.add_course_btn = Button(self.add_syllabus_frame_internal, image=addcourse_img, bd=0, bg="#bfc7c5",
                                         activebackground="#bfc7c5", command=self.get_results_of_subjects_course_add)
            self.add_course_btn.place(relx=0.5, rely=0.6)
            self.add_course_btn.image = addcourse_img
            test = 'Separate the chapter with # , e.g Chapter#1,Chapter#2 Separate the topics with a comma.'
            self.syllabus_box.delete("1.0", END)
            self.syllabus_box.insert("1.0", test)


    def update_syllabus(self):
        query = f"""UPDATE courses SET content= '{self.syllabus_box.get("1.0", END)}'  WHERE name='{self.list_subjects_syllabus_create.get()}' AND program='{self.degree_program_syllabus_create.get()}' AND class='{self.class_selectoin_syllabus_create.get()}'"""

        cursor.execute(query)
        db.commit()
        msb.showinfo("Conratulations", "Your syllabus has been updated")

    # function to insert data to database in of syallabus
    def get_results_of_subjects_course_add(self):

        class_standard_for_program = self.class_selectoin_syllabus_create.get()
        isntitute_level = self.degree_program_syllabus_create.get()
        subject = self.list_subjects_syllabus_create.get()
        code = self.results_of_subject_to_add_syllabus[0][0]
        auther = self.results_of_subject_to_add_syllabus[0][1]
        cors_type = self.results_of_subject_to_add_syllabus[0][2]
        syllabus = self.syllabus_box.get('1.0', END)

        query = "INSERT INTO courses(name,code,author,program,class,type,content )VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (subject, code, auther, isntitute_level, class_standard_for_program, cors_type, syllabus))

        db.commit()
        msb.showinfo("Congratulations", "Syllabus for the subject has been successfully added.")

    # ============================================================================================================================ create class

    def add_students_classes_to_db(self):

        self.main_menu_buttons_frame.destroy()

        self.add_syllabus_attendence_frame = Toplevel(root,
                                                      width=screenwidth - 300, bg="#bfc7c5",
                                                      height=screenheight - 250, )
        self.add_syllabus_attendence_frame.grab_set()

        self.add_syllabus_attendence_frame.group(root)

        # adding content on attendence frame
        self.degree_program_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=15,
                                                      font=("arial", 12))
        self.degree_program_attendence['values'] = ("Select a program","University")
        style.configure("TCombobox", fieldbackground="orange", background="white")

        self.degree_program_attendence.current(0)

        # self.degree_program_attendence.bind("<<ComboboxSelected>>", lambda _: self.select_class_standard_for_class())

        self.degree_program_attendence.place(relx=0.1, rely=0.05)
        # class dumy made

        self.class_standard_attendence = ttk.Entry(self.add_syllabus_attendence_frame, width=15, font=font_family)

        self.class_standard_attendence.insert(0, "Class Standard")
        self.class_standard_attendence.place(relx=0.25, rely=0.05)
        self.class_standard_attendence.bind('<FocusIn>', lambda e: self.chek_focusin_create_class_1(e))
        self.class_standard_attendence.bind('<FocusOut>', lambda e: self.chek_focusout_create_class_1(e))

        # select class standard and set here

        # section dumy made
        self.section_attendence = ttk.Entry(self.add_syllabus_attendence_frame, width=15, font=font_family)
        self.section_attendence.place(relx=0.4, rely=0.05)
        self.section_attendence.insert(0, "Section")
        self.section_attendence.bind('<FocusIn>', lambda e: self.chek_focusin_create_class_2(e))
        self.section_attendence.bind('<FocusOut>', lambda e: self.chek_focusout_create_class_2(e))

        self.no_of_students = Entry(self.add_syllabus_attendence_frame, width=15, font=font_family)
        self.no_of_students.place(relx=0.55, rely=0.05)
        self.no_of_students.insert(0, "No. Of Students")
        self.no_of_students.bind('<FocusIn>', lambda e: self.chek_focusin_create_class_3(e))
        self.no_of_students.bind('<FocusOut>', lambda e: self.chek_focusout_create_class_3(e))
        okbtn = PhotoImage(file=r"button_images/ok_btn1.png")
        self.okbtn_attendence = Button(self.add_syllabus_attendence_frame, image=okbtn, bg="#bfc7c5", bd=0,
                                       command=self.add_students_details)
        self.okbtn_attendence.place(relx=0.7, rely=0.05)

        self.okbtn_attendence.image = okbtn

    # function to work on further values selection in attendence frame

    # handel focus events for add class

    def chek_focusin_create_class_1(self, e):
        if self.class_standard_attendence.focus_get():
            if self.class_standard_attendence.get() == "Class Standard":
                self.class_standard_attendence.delete(0, END)

    def chek_focusout_create_class_1(self, e):

        if self.class_standard_attendence.get() == "":
            self.class_standard_attendence.insert(0, "Class Standard")

    def chek_focusin_create_class_2(self, e):
        if self.section_attendence.focus_get():
            if self.section_attendence.get() == "Section":
                self.section_attendence.delete(0, END)

    def chek_focusout_create_class_2(self, e):

        if self.section_attendence.get() == "":
            self.section_attendence.insert(0, "Section")

    def chek_focusin_create_class_3(self, e):
        if self.no_of_students.focus_get():
            if self.no_of_students.get() == "No. Of Students":
                self.no_of_students.delete(0, END)

    def chek_focusout_create_class_3(self, e):

        if self.no_of_students.get() == "":
            self.no_of_students.insert(0, "No. Of Students")

    def add_students_details(self):
        # self.no_of_students.config(state="normal")
        if type(self.no_of_students.get()) == int or not self.no_of_students.get() == "No. Of Students":
            self.sheet_demo = Sheet(self.add_syllabus_attendence_frame,
                                    height=500, expand_sheet_if_paste_too_big=True,
                                    enable_edit_cell_auto_resize=True,
                                    width=600)
            self.sheet_demo.enable_bindings(("single",
                                             "drag_select",
                                             "column_drag_and_drop",
                                             "row_drag_and_drop",
                                             "column_select",
                                             "row_select",
                                             "column_width_resize",
                                             "double_click_column_resize",
                                             "row_width_resize",
                                             "column_height_resize",
                                             "arrowkeys",
                                             "row_height_resize",
                                             "double_click_row_resize",
                                             "right_click_popup_menu",
                                             "rc_insert_column",
                                             "rc_delete_column",
                                             "rc_insert_row",
                                             "rc_delete_row",
                                             "copy",
                                             "cut",
                                             "paste",
                                             "delete",
                                             "undo",
                                             "edit_cell"))

            self.sheet_demo.place(relx=0.3, rely=0.2)

            self.sheet_demo.headers(["name", "last name", "roll no"])

            self.data = [[f"" for c in range(3)] for r in range(int(self.no_of_students.get()))]
            self.sheet_demo.data_reference(self.data)
            self.sheet_demo.column_width(0, 150)
            self.sheet_demo.column_width(1, 200)
            self.sheet_demo.column_width(2, 150)
            self.sheet_demo.row_height(1, 20)

            apply_btn = PhotoImage(file=r"button_images/save_btn.png")
            self.addtodb_attendence = Button(self.add_syllabus_attendence_frame, image=apply_btn, bd=0, bg="#bfc7c5",
                                             command=self.add_students_details_db)
            self.addtodb_attendence.image = apply_btn
            self.addtodb_attendence.place(relx=0.9, rely=0.9)

            cancelbtn = PhotoImage(file=r"button_images/cancel.png")
            self.okbtn_attendence = Button(self.add_syllabus_attendence_frame, image=cancelbtn, bg="#bfc7c5", bd=0,
                                           command=self.destroy_attendence_frame)
            self.okbtn_attendence.place(relx=0.8, rely=0.9)

            self.okbtn_attendence.image = cancelbtn

        else:
            msb.showinfo("Alert", "Please input Number of students. ")

    # add details of studenst like name roll and last name in db from sheet .
    def destroy_attendence_frame(self):
        self.add_syllabus_attendence_frame.destroy()

    def add_students_details_db(self):

        column1 = self.sheet_demo.get_column_data(0, return_copy=True)
        column2 = self.sheet_demo.get_column_data(1, return_copy=True)
        column3 = self.sheet_demo.get_column_data(2, return_copy=True)

        degree_level = self.degree_program_attendence.get()
        class_standard = self.class_standard_attendence.get()
        section = self.section_attendence.get()
        no_of_students = int(self.no_of_students.get())
        if len(column3) != no_of_students or len(column2) != no_of_students or len(column1) != no_of_students:
            msb.showerror("", "Required Number of students are not filled. ")
        if degree_level == "" or class_standard == "" or section == "":
            msb.showerror("", "Required Number of students are not filled. ")

        qry = "INSERT INTO classes_list(edu_level ,class_standard  ,section_name ,name ,lastname ,rollno )VALUES(%s,%s,%s,%s,%s,%s)"
        for i in range(len(column1)):
            cursor.execute(qry, (degree_level, class_standard, section, column1[i], column2[i], column3[i]))
            db.commit()
        msb.showinfo("Congratulation", "class has been Successfully added ")

    # ============================================================================================================================

    # this function is used to view the teachers and their credantials.
    def destroy_view_teachers(self):
        self._assign_classes_frame.destroy()
        self.tabControl.destroy()
        self.main_manu_widgets()
        self.assign_class_backbtn.destroy()

    def view_techers_list(self):

        # add scrollabel frame to see the teachers

        self.main_menu_buttons_frame.destroy()
        # self._assign_classes_frame=Frame(self.tabControl,bg='cyan',height=50,width=screenwidth)
        self._assign_classes_frame = Frame(root, bg='#bfc7c5', height=50, width=screenwidth)
        self._assign_classes_frame.place(relx=0, rely=0)
        self.assign_class_backbtn = Button(root, text="Back <-", relief=FLAT, bg='white', bd=0,
                                           command=self.destroy_view_teachers)
        self.assign_class_backbtn.place(x=5, y=7)
        # create subjects
        self.create_subject_btn = ttk.Button(self._assign_classes_frame, text="Create Subjects",
                                             command=self.add_subjects_function_top_level)
        self.create_subject_btn.place(relx=0.1, rely=0.5, anchor=CENTER)
        # create classes
        self.assign_class_btn = ttk.Button(self._assign_classes_frame, text="Create class",
                                           command=self.add_students_classes_to_db)
        self.assign_class_btn.place(relx=0.2, rely=0.5, anchor=CENTER)

        self.assign_class_btn = ttk.Button(self._assign_classes_frame, text="Assign class",
                                           command=self.assign_class_to_teacher)
        self.assign_class_btn.place(relx=0.3, rely=0.5, anchor=CENTER)

        # self.cancel_button = Button(self._assign_classes_frame, text="Cancel", bg='white', relief=GROOVE, width=10,
        #                             font=('American typewriter', 12))
        #
        # self.cancel_button.place(relx=0.4, rely=0.5, anchor=CENTER)

        self.tabControl = ttk.Notebook(root, width=(screenwidth - (int(screenwidth / 3))))
        self.tabControl.place(relx=0.2, rely=0.15)

        # list of assigned classses to teachers
        # tab 1

        # self.view_assigned_subjest1 = ttk.Frame(self.tabControl)
        #
        # self.view_assigned_subjest.pack()

        self.view_assigned_subjest1 = ttk.Frame(self.tabControl)
        canvas_classes_create = Canvas(self.view_assigned_subjest1, width=800, height=500, bg='#bfc7c5')
        scrollbar_for_classes_create = ttk.Scrollbar(self.view_assigned_subjest1, orient="vertical",
                                                     command=canvas_classes_create.yview)
        self.view_assigned_subjest = ttk.Frame(canvas_classes_create)
        self.view_assigned_subjest.bind("<Configure>", lambda e: canvas_classes_create.configure(
            scrollregion=canvas_classes_create.bbox("all")))
        canvas_classes_create.create_window((0, 0), window=self.view_assigned_subjest, anchor="nw")
        canvas_classes_create.configure(yscrollcommand=scrollbar_for_classes_create.set)
        self.view_assigned_subjest1.place(relx=0.1, rely=0.2)
        canvas_classes_create.pack(side="left", fill="both", expand=True)
        scrollbar_for_classes_create.pack(side="right", fill="y")
        self.tabControl.add(self.view_assigned_subjest1, text='Assigned Classes')

        cursor.execute(
            # "SELECT * FROM assigned_subjects_teachers")
            "SELECT teacher_selected,institute_level , class_standard ,section_selected , subject_selected   FROM assigned_subjects_teachers")
        result = cursor.fetchall()
        temp_results = []
        for i in result:
            temp_results.append((str(i[0]).split(" ")[1], i[1], i[2], i[3]))
        values = ["Teacher", "Edu Level", "Class", "Section"]
        for i in range(4):
            entery = Entry(self.view_assigned_subjest, font=("arial", 13, 'bold'), bd=0)
            entery.grid(row=0, column=i)
            entery.insert(0, str(values[i]))
            entery.config(state='readonly', readonlybackground="#b8b4a9")

        for i in range(len(temp_results)):

            name_entry = Entry(self.view_assigned_subjest, font=("arial", 13), bd=0, width=20)
            name_entry.grid(row=i + 1, column=0)
            name_entry.insert(0, temp_results[i][0])

            edu_level = Entry(self.view_assigned_subjest, font=("arial", 13), bd=0, width=20)
            edu_level.grid(row=i + 1, column=1)
            edu_level.insert(0, temp_results[i][1])

            name_entry1 = Entry(self.view_assigned_subjest, font=("arial", 13), bd=0, width=20)
            name_entry1.grid(row=i + 1, column=2)
            name_entry1.insert(0, temp_results[i][2])

            name_entry2 = Entry(self.view_assigned_subjest, font=("arial", 13), bd=0, width=20)
            name_entry2.grid(row=i + 1, column=3)
            name_entry2.insert(0, temp_results[i][3])
            if i % 2 != 0:
                name_entry.config(state='readonly', readonlybackground="#b8b4a9")
                edu_level.config(state='readonly', readonlybackground="#b8b4a9")
                name_entry1.config(state='readonly', readonlybackground="#b8b4a9")
                name_entry2.config(state='readonly', readonlybackground="#b8b4a9")
            else:
                name_entry.config(state='readonly', )
                edu_level.config(state='readonly', )
                name_entry1.config(state='readonly', )
                name_entry2.config(state='readonly', )

        # tab 2 view subject

        add_subject_container = ttk.Frame(self.tabControl)
        canvas_classes_create = Canvas(add_subject_container, width=800, height=500, bg='#bfc7c5')
        scrollbar_for_classes_create = ttk.Scrollbar(add_subject_container, orient="vertical",
                                                     command=canvas_classes_create.yview)
        scrollable_frame_for_class_add_subject = ttk.Frame(canvas_classes_create)
        scrollable_frame_for_class_add_subject.bind("<Configure>", lambda e: canvas_classes_create.configure(
            scrollregion=canvas_classes_create.bbox("all")))
        canvas_classes_create.create_window((0, 0), window=scrollable_frame_for_class_add_subject, anchor="nw")
        canvas_classes_create.configure(yscrollcommand=scrollbar_for_classes_create.set)
        add_subject_container.place(relx=0.1, rely=0.2)
        canvas_classes_create.pack(side="left", fill="both", expand=True)
        scrollbar_for_classes_create.pack(side="right", fill="y")
        self.tabControl.add(add_subject_container, text='Viw Subject')

        values = ["Degree Program", "Class Standard", "Subject", "Subject-code", "Auther", "Rec/Ref"]
        for i in range(6):
            entery = Entry(scrollable_frame_for_class_add_subject, font=("arial", 13, 'bold'), bd=0)
            entery.grid(row=0, column=i)
            entery.insert(0, str(values[i]))
            entery.config(state='readonly', readonlybackground="#b8b4a9")

        cursor.execute(
            "SELECT subject_program ,subject_standard ,subject_name,subject_code ,subject_author ,course_type FROM subjects_created")
        temp_results = cursor.fetchall()

        for i in range(len(temp_results)):
            program = Entry(scrollable_frame_for_class_add_subject, font=("arial", 13), bd=0, width=20)
            program.grid(row=i + 1, column=0)
            program.insert(0, temp_results[i][0])

            standard = Entry(scrollable_frame_for_class_add_subject, font=("arial", 13), bd=0, width=20)
            standard.grid(row=i + 1, column=1)
            standard.insert(0, temp_results[i][1])

            subject_name = Entry(scrollable_frame_for_class_add_subject, font=("arial", 13), bd=0, width=20)
            subject_name.grid(row=i + 1, column=2)
            subject_name.insert(0, temp_results[i][2])

            subject_code = Entry(scrollable_frame_for_class_add_subject, font=("arial", 13), bd=0, width=20)
            subject_code.grid(row=i + 1, column=3)
            subject_code.insert(0, temp_results[i][3])

            subject_auther = Entry(scrollable_frame_for_class_add_subject, font=("arial", 13), bd=0, width=20)
            subject_auther.grid(row=i + 1, column=4)
            subject_auther.insert(0, temp_results[i][4])

            subject_type = Entry(scrollable_frame_for_class_add_subject, font=("arial", 13), bd=0, width=20)
            subject_type.grid(row=i + 1, column=5)
            subject_type.insert(0, temp_results[i][5])

            if i % 2 != 0:
                standard.config(state='readonly', readonlybackground="#b8b4a9")
                program.config(state='readonly', readonlybackground="#b8b4a9")
                subject_name.config(state='readonly', readonlybackground="#b8b4a9")
                subject_code.config(state='readonly', readonlybackground="#b8b4a9")
                subject_auther.config(state='readonly', readonlybackground="#b8b4a9")
                subject_type.config(state='readonly', readonlybackground="#b8b4a9")
            else:
                standard.config(state='readonly', )
                program.config(state='readonly', )
                subject_name.config(state='readonly', )
                subject_code.config(state='readonly', )
                subject_auther.config(state='readonly', )
                subject_type.config(state='readonly', )

        # adding subjects here

        # tab 3

        style.theme_use('alt')
        style.configure('TButton', font=('American typewriter', 14), background='blue', foreground='white')
        style.map('TButton', background=[('active', '#ff0000')])
        # cancel button

        container = ttk.Frame(self.tabControl)
        canvas = Canvas(container, width=800, height=500, bg="#bfc7c5")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.place(relx=0.1, rely=0.2)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # fetch the data from db

        cursor.execute("SELECT id,full_name,mobile ,email, gender,signup_date FROM users  ")
        results = cursor.fetchall()

        values = ["Id", "Name", "Mobile", "E-Mail", "Gender", "SignUp Date"]
        for i in range(6):
            entery0 = Entry(scrollable_frame, font=("arial", 13, 'bold'), bd=0, bg="#b8b4a9", )
            entery0.grid(row=0, column=i)
            entery0.insert(0, str(values[i]))
            entery0.config(state='readonly', readonlybackground="#b8b4a9")

        for i in range(len(results)):
            entery1 = Entry(scrollable_frame, font=("arial", 13), bd=0)
            entery1.grid(row=i + 1, column=0)
            entery1.insert(0, results[i][0])

            entery2 = Entry(scrollable_frame, font=("arial", 13), bd=0)
            entery2.grid(row=i + 1, column=1)
            entery2.insert(0, results[i][1])

            entery3 = Entry(scrollable_frame, font=("arial", 13), bd=0)
            entery3.grid(row=i + 1, column=2)
            entery3.insert(0, results[i][2])

            entery4 = Entry(scrollable_frame, font=("arial", 13), bd=0)
            entery4.grid(row=i + 1, column=3)
            entery4.insert(0, results[i][3])

            entery5 = Entry(scrollable_frame, font=("arial", 13), bd=0)
            entery5.grid(row=i + 1, column=4)
            entery5.insert(0, results[i][4])

            entery6 = Entry(scrollable_frame, font=("arial", 13), bd=0)
            entery6.grid(row=i + 1, column=5)
            entery6.insert(0, results[i][5])
            if i % 2 != 0:

                entery1.config(state='readonly', readonlybackground="#b8b4a9")
                entery2.config(state='readonly', readonlybackground="#b8b4a9")
                entery3.config(state='readonly', readonlybackground="#b8b4a9")
                entery4.config(state='readonly', readonlybackground="#b8b4a9")
                entery5.config(state='readonly', readonlybackground="#b8b4a9")
                entery6.config(state='readonly', readonlybackground="#b8b4a9")
            else:
                entery1.config(state='readonly', )
                entery2.config(state='readonly', )
                entery3.config(state='readonly', )
                entery4.config(state='readonly', )
                entery5.config(state='readonly', )
                entery6.config(state='readonly', )

        self.tabControl.add(container, text='View Teachers')

    def on_key(self, event):
        pass

    # add subject in Button 3 pop  up window                        add subject to database
    def add_subjects_function_top_level(self):
        self.subject_top_level = Toplevel()
        self.subject_top_level.geometry(f"{int(screenwidth / 2)}x{int(screenheight / 1.5)}+200+100")
        self.subject_top_level_width = int(screenwidth / 3)
        self.subject_top_level_height = int(screenheight / 2)
        self.subject_top_level.config(bg='#bfc7c5')
        self.subject_top_level.grab_set()

        # making entries for subject

        self.syllabus_name_insert = ttk.Entry(self.subject_top_level, width=15, font=font_family)
        self.syllabus_name_insert.place(relx=0.1, rely=0.1)
        self.syllabus_name_insert.insert(0, "Course Name")

        self.syllabus_name_insert.bind('<FocusIn>', lambda e: self.check_focusesin_and_place_holders_of_add_course_1(e))
        self.syllabus_name_insert.bind('<FocusOut>',
                                       lambda e: self.check_focusesout_and_place_holders_of_add_course_1(e))

        self.code_insert = Entry(self.subject_top_level, width=15, font=font_family)
        self.code_insert.place(relx=0.35, rely=0.1)
        self.code_insert.insert(0, "Course Code")
        self.code_insert.bind('<FocusIn>', lambda e: self.check_focusesin_and_place_holders_of_add_course_2(e))
        self.code_insert.bind('<FocusOut>', lambda e: self.check_focusesout_and_place_holders_of_add_course_2(e))

        self.author_insert = Entry(self.subject_top_level, width=15, font=font_family)
        self.author_insert.place(relx=0.1, rely=0.2)
        self.author_insert.bind('<FocusIn>', lambda e: self.check_focusesin_and_place_holders_of_add_course_3(e))
        self.author_insert.bind('<FocusOut>', lambda e: self.check_focusesout_and_place_holders_of_add_course_3(e))
        self.author_insert.insert(0, "Auther")

        # degree program
        self.degree_program_insert = ttk.Combobox(self.subject_top_level, state="readonly", width=15, height=10,
                                                  font=("arial", 12))
        self.degree_program_insert['values'] = ("Select a program","University")

        self.degree_program_insert.current(0)

        self.degree_program_insert.place(relx=0.35, rely=0.2)
        # class selection
        self.class_selectoin_insert = ttk.Combobox(self.subject_top_level, state="readonly", width=15, height=10,
                                                   font=("arial", 12))
        cursor.execute(f"SELECT class_standard FROM classes_list ORDER BY id")

        result = cursor.fetchall()
        result1 = ["Select a Class "]
        for i in result:
            if i not in result1:
                result1.append(i)

        self.class_selectoin_insert['values'] = (result1)
        self.class_selectoin_insert.current(0)

        self.class_selectoin_insert.place(relx=0.1, rely=0.3)

        # course type

        self.rec_or_ref_insert = ttk.Combobox(self.subject_top_level, state="readonly", width=15, height=10,
                                              font=("arial", 12))
        self.rec_or_ref_insert['values'] = ("Course Type", 'Recomended', 'Reference')
        self.rec_or_ref_insert.current(0)
        self.rec_or_ref_insert.place(relx=0.35, rely=0.3)
        #

        # row3
        save_img = PhotoImage(file=r"button_images/save_btn.png")
        self.save_btn_add_course = Button(self.subject_top_level, image=save_img, command=self.add_subject_database,
                                          bd=0, bg='#bfc7c5')
        self.save_btn_add_course.place(relx=0.4, rely=0.4)

        clear_all_img = PhotoImage(file=r"button_images/clear_all.png")

        self.clear_all_btn_add_course = Button(self.subject_top_level, image=clear_all_img,
                                               command=self.clear_syllabus_form, bd=0, bg='#bfc7c5')
        self.clear_all_btn_add_course.place(relx=0.25, rely=0.4)

        cancel_img = PhotoImage(file=r"button_images/cancel.png")
        self.cancel_btn_add_course = Button(self.subject_top_level, image=cancel_img, command=self.destroy_subject_add,
                                            bd=0, bg='#bfc7c5')
        self.cancel_btn_add_course.place(relx=0.1, rely=0.4)

        self.subject_top_level.resizable(False, False)

        self.subject_top_level.mainloop()

    def destroy_subject_add(self):
        self.subject_top_level.destroy()

    def clear_syllabus_form(self):
        self.rec_or_ref_insert.current(0)
        self.degree_program_insert.current(0)

        self.class_selectoin_insert.current(0)
        # self.class_selectoin_insert.insert(0, "Class Standard")

        self.author_insert.delete(0, END)
        self.author_insert.insert(0, "Auther")

        self.code_insert.delete(0, END)
        self.code_insert.insert(0, "Course code")

        self.syllabus_name_insert.delete(0, END)
        self.syllabus_name_insert.insert(0, "Course Name")

    def check_focusesin_and_place_holders_of_add_course_1(self, e):
        if self.syllabus_name_insert.focus_get():
            if self.syllabus_name_insert.get() == "Course Name":
                self.syllabus_name_insert.delete(0, END)

    def check_focusesin_and_place_holders_of_add_course_2(self, e):

        if self.code_insert.focus_get():
            if self.code_insert.get() == "Course Code":
                self.code_insert.delete(0, END)

    def check_focusesin_and_place_holders_of_add_course_3(self, e):

        if self.author_insert.focus_get():
            if self.author_insert.get() == "Auther":
                self.author_insert.delete(0, END)

    def check_focusesin_and_place_holders_of_add_course_4(self, e):

        if self.class_selectoin_insert.focus_get():
            if self.class_selectoin_insert.get() == "Class Standard":
                self.class_selectoin_insert.delete(0, END)

    def check_focusesout_and_place_holders_of_add_course_1(self, e):

        if self.syllabus_name_insert.get() == "":
            self.syllabus_name_insert.insert(0, "Course Name")

    def check_focusesout_and_place_holders_of_add_course_2(self, e):

        if self.code_insert.get() == "":
            self.code_insert.insert(0, "Course Code")

    def check_focusesout_and_place_holders_of_add_course_3(self, e):

        if self.author_insert.get() == "":
            self.author_insert.insert(0, "Auther")

    def check_focusesout_and_place_holders_of_add_course_4(self, e):

        if self.class_selectoin_insert.get() == "":
            self.class_selectoin_insert.insert(0, "Class Standard")
        # add subject to database

    def add_subject_database(self):
        syl_name = self.syllabus_name_insert.get()
        syl_code = self.code_insert.get()
        syl_auth = self.author_insert.get()
        syl_degree_program = self.degree_program_insert.get()
        syl_standard = self.class_selectoin_insert.get()
        syl_course_type = self.rec_or_ref_insert.get()

        if syl_name == "" or syl_name == "Course Name" or syl_code == "" or syl_code == "Course Code" or syl_auth == "" or syl_auth == "Auther" or syl_degree_program == "Select a program" or syl_standard == "Class Standard" or syl_course_type == "Course Type":
            msb.showerror("", "Something went wrong")
        else:
            query = "INSERT INTO subjects_created(subject_name, subject_code, subject_author,subject_program,subject_standard,course_type) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (syl_name, syl_code, syl_auth, syl_degree_program, syl_standard, syl_course_type))
            db.commit()
            msb.showinfo("Congrats", "Congratulation subject has been successfully added")

    # add classes for students ====================================================================================
    def attendence_system(self):

        # self.main_menu_buttons_frame.destroy()
        self.add_syllabus_attendence_frame = Toplevel(root,
                                                      width=screenwidth - 100,
                                                      height=screenheight - 250, bg='purple')
        self.add_syllabus_attendence_frame.grab_set()

        # self.add_syllabus_attendence_frame = LabelFrame()

        # self.add_syllabus_attendence_frame.place(relx=0.2, rely=0.15)

        # adding content on attendence frame
        self.degree_program_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                                      font=("arial", 12))
        self.degree_program_attendence['values'] = ("Select a program",  "University")

        self.degree_program_attendence.current(0)
        self.degree_program_attendence.bind("<<ComboboxSelected>>", lambda _: self.select_standard_attendence_())
        self.degree_program_attendence.place(relx=0.1, rely=0.05)

        self.class_standard_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                                      font=("arial", 12))
        self.class_standard_attendence['values'] = ("Select a program",)

        self.class_standard_attendence.current(0)
        self.class_standard_attendence.place(relx=0.2, rely=0.05)
        # section dumy made
        self.section_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                               font=("arial", 12))
        self.section_attendence['values'] = ("Select a section",)
        self.section_attendence.current(0)
        self.section_attendence.place(relx=0.3, rely=0.05)
        self.no_of_students = Entry(self.add_syllabus_attendence_frame, width=15,
                                    )
        self.no_of_students.place(relx=0.4, rely=0.05)

        self.okbtn_attendence = ttk.Button(self.add_syllabus_attendence_frame, text="OK",
                                           command=self.got_students_details_fromdb)
        self.okbtn_attendence.place(relx=0.55, rely=0.05)

    # function to work on further values selection in attendence frame
    def select_standard_attendence_(self):
        self.class_standard_attendence.destroy()
        # class name
        degree_level = self.degree_program_attendence.get()
        # storing level in list to work with attendence
        institude_level_for_attendence.append(degree_level)

        data = cursor.execute(f"SELECT class_standard FROM students_details WHERE edu_level='{degree_level}'")

        ls = []
        for i in data:
            if i in ls:
                pass
            else:
                ls.append(i)

        self.class_standard_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                                      font=("arial", 12))
        self.class_standard_attendence['values'] = (ls)
        self.class_standard_attendence.current(0)
        self.class_standard_attendence.bind("<<ComboboxSelected>>", lambda _: self.select_section_attendence_())

        self.class_standard_attendence.place(relx=0.2, rely=0.05)

    # define the section
    def select_section_attendence_(self):
        # class name
        name_of_class_for_attendence.append(self.class_standard_attendence.get())

        # self.section_attendence.destroy()
        class_standard = self.class_standard_attendence.get()
        # storing level in list to work with attendence
        # students_details_about_section.append(class_standard)
        data = cursor.execute(f"SELECT section_name FROM students_details WHERE class_standard='{class_standard}'")
        ls = []
        for i in data:
            if i in ls:
                pass
            else:
                ls.append(i)

        self.section_attendence = ttk.Combobox(self.add_syllabus_attendence_frame, state="readonly", width=12,
                                               font=("arial", 12))
        self.section_attendence['values'] = (ls)
        self.section_attendence.current(0)
        self.section_attendence.bind("<<ComboboxSelected>>", lambda _: self.add_students_details_forclass())

        self.section_attendence.place(relx=0.3, rely=0.05)

    def add_students_details_forclass(self):

        students_details_about_section.append(self.section_attendence.get())

    def makingvars(self):
        self.varslst = []
        degree_level = self.degree_program_attendence.get()
        class_standard = self.class_standard_attendence.get()
        section_standard = self.section_attendence.get()

        data = cursor.execute(
            f"SELECT name,lastname,rollno FROM students_details WHERE class_standard='{class_standard}' AND edu_level='{degree_level}' AND section_name= '{section_standard}'")

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

        container.place(relx=0.2, rely=0.3)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # fetching data from db to apply attendence ======================================================
        degree_level = self.degree_program_attendence.get()
        class_standard = self.class_standard_attendence.get()
        section_standard = self.section_attendence.get()

        data = cursor.execute(
            f"SELECT name,lastname,rollno FROM students_details WHERE class_standard='{class_standard}' AND edu_level='{degree_level}' AND section_name= '{section_standard}'")

        ls = []

        for i in data:
            if i in ls:
                pass
            else:
                ls.append(i)

        self.variables = []
        # Create the command using partial
        for self.i in range(len(ls)):
            self.variable = StringVar()
            self.variables.append(self.variable)

            Label(scrollable_frame, text=ls[self.i][0], bg='green', fg='white').grid(padx=10, pady=10, row=self.i,
                                                                                     column=0)
            Label(scrollable_frame, text=ls[self.i][1], bg='green').grid(padx=20, pady=10, row=self.i, column=1)
            Label(scrollable_frame, text=ls[self.i][2], bg='green').grid(padx=20, pady=10, row=self.i, column=2)
            roll_numbers_to_presrnt.append(ls[self.i][2])
            # names_of_studenst_for_attendence.clear()
            # lastnames_of_studenst_for_attendence.clear()
            names_of_studenst_for_attendence.append(ls[self.i][0])
            lastnames_of_studenst_for_attendence.append(ls[self.i][1])

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

            self.okbtn = Button(scrollable_frame, text="check present", command=command).grid(row=0, column=10)
            self.okbtn1 = Button(scrollable_frame, text="check final", command=self.ok_fun).grid(row=1, column=10)

    def function(self, i):
        self.got = [var.get() for var in self.variables]

    def ok_fun(self):
        pass

    #               ==============================   assign classes to teachers===========================

    def assign_class_to_teacher(self):

        self.assign_class_to_teacher_frame = Toplevel(root,
                                                      width=600,
                                                      height=500, bg='#bfc7c5')
        self.assign_class_to_teacher_frame.grab_set()

        # slecting degree progeam
        self.degree_program_assigntecher = ttk.Combobox(self.assign_class_to_teacher_frame, state="readonly", width=12,
                                                        font=("arial", 12))
        self.degree_program_assigntecher['values'] = ("Select a program",  "University")

        self.degree_program_assigntecher.current(0)
        self.degree_program_assigntecher.bind("<<ComboboxSelected>>",
                                              lambda _: self.select_class_standard_onbasesof_institute())
        self.degree_program_assigntecher.place(relx=0.15, rely=0.15)

    def select_class_standard_onbasesof_institute(self):
        try:

            cursor.execute(
                f"SELECT DISTINCT class_standard ,id FROM classes_list where edu_level='{self.degree_program_assigntecher.get().strip()}' ORDER BY id DESC")
            data = cursor.fetchall()

            final_data = ["Select a Class"]
            for i in data:
                if i[0] not in final_data:
                    final_data.append(i[0])

            # set data to drop down to select class
            self.select_class_standard_assigntecher = ttk.Combobox(self.assign_class_to_teacher_frame, state="readonly",
                                                                   width=12,
                                                                   font=("arial", 12))
            self.select_class_standard_assigntecher['values'] = (final_data)

            self.select_class_standard_assigntecher.current(0)
            self.select_class_standard_assigntecher.bind("<<ComboboxSelected>>",
                                                         lambda _: self.asign_subject_final_to_teacher())
            self.select_class_standard_assigntecher.place(relx=0.4, rely=0.15)
        except:
            msb.showinfo("", "No Class found.")

    def asign_subject_final_to_teacher(self):
        try:
            cursor.execute(
                f"SELECT section_name FROM classes_list where edu_level='{self.degree_program_assigntecher.get().strip()}' AND class_standard='{self.select_class_standard_assigntecher.get()}'")
            data = cursor.fetchall()

            data1 = []

            # sort the data to show in dropdown
            for i in data:
                if i not in data1:
                    data1.append(i[0])
            data1 = set(data1)
            data1 = [i for i in data1]
            final_data = ["Select a Section"]
            for i in data1:
                final_data.append(i)

            self.select_sction_assigntecher = ttk.Combobox(self.assign_class_to_teacher_frame, state="readonly",
                                                           width=12,
                                                           font=("arial", 12))
            self.select_sction_assigntecher['values'] = (final_data)
            self.select_sction_assigntecher.current(0)
            self.select_sction_assigntecher.bind("<<ComboboxSelected>>",
                                                 lambda _: self.fetch_subjects_and_teachers())
            self.select_sction_assigntecher.place(relx=0.15, rely=0.3)
        except:
            msb.showinfo("", "No section found for this class")

    def fetch_subjects_and_teachers(self):
        # subject select
        cursor.execute(
            f"SELECT subject_name ,id FROM subjects_created WHERE subject_program='{self.degree_program_assigntecher.get().strip()}' ORDER BY id DESC ")
        data = cursor.fetchall()

        final_data = ["Select a Subject"]
        for i in data:
            if i[0] not in final_data:
                final_data.append(i[0])

        self.select_subject_assigntecher = ttk.Combobox(self.assign_class_to_teacher_frame, state="readonly",
                                                        width=12, font=("arial", 12))
        self.select_subject_assigntecher['values'] = (final_data)
        self.select_subject_assigntecher.current(0)
        self.select_subject_assigntecher.bind("<<ComboboxSelected>>", )
        self.select_subject_assigntecher.place(relx=0.4, rely=0.3)

        # techer select
        cursor.execute(f"SELECT id , full_name  FROM users ORDER BY id DESC")
        data = cursor.fetchall()

        final_data = ["Select a Teacher"]
        for i in data:
            final_data.append(str(i[0]) + " " + str(i[1]))

        self.select_teacher_assigntecher = ttk.Combobox(self.assign_class_to_teacher_frame, state="readonly",
                                                        width=12,
                                                        font=("arial", 12))
        self.select_teacher_assigntecher['values'] = (final_data)
        self.select_teacher_assigntecher.current(0)
        self.select_teacher_assigntecher.bind("<<ComboboxSelected>>", )

        self.select_teacher_assigntecher.place(relx=0.15, rely=0.45)

        # adding images to buttons to save and cancel
        saveimg = PhotoImage(file=r"button_images/save_btn.png")
        cancelimg = PhotoImage(file=r"button_images/cancel.png")
        self.assign_cls_btn = Button(self.assign_class_to_teacher_frame, image=saveimg, bg="#bfc7c5",
                                     activebackground="#bfc7c5", bd=0,
                                     command=self.insert_assigned_subject)
        self.assign_cls_btn.place(relx=0.4, rely=0.6)
        self.assign_cls_btn.image = saveimg

        self.cancel_cls_btn = Button(self.assign_class_to_teacher_frame, image=cancelimg, bg="#bfc7c5",
                                     activebackground="#bfc7c5", bd=0,
                                     command=self.cancel_assign_class)
        self.cancel_cls_btn.place(relx=0.15, rely=0.6)
        self.cancel_cls_btn.image = cancelimg

    def cancel_assign_class(self):
        self.assign_class_to_teacher_frame.destroy()

    # function to sort a string based on numbers TO sort teachers with id
    def num_sort(test_string):
        import re
        return list(map(int, re.findall(r'\d+', test_string)))[0]

    def insert_assigned_subject(self):

        institute = self.degree_program_assigntecher.get()
        class_assigned = self.select_class_standard_assigntecher.get()
        section_assigned = self.select_sction_assigntecher.get()
        teacher_assigned = self.select_teacher_assigntecher.get()
        t_id = teacher_assigned.split(" ")[0]
        # print(t_id)
        subject_assigned = self.select_subject_assigntecher.get()
        try:
            qry = " INSERT INTO assigned_subjects_teachers(teacher_id,institute_level , class_standard ,section_selected , subject_selected  , teacher_selected)VALUES(%s,%s,%s,%s,%s,%s) "
            cursor.execute(qry, (t_id, institute, class_assigned, section_assigned, subject_assigned, teacher_assigned))
            db.commit()
            msb.showinfo("", "Subject has been successfully assigned ")

        except:
            msb.showinfo("", "Not added, Retry ")

        # sms system to send schdule ===================================================================================

    def create_top_level_to_show_sms_schedule(self, i):
        temp = Toplevel(root, width=800, height=500)
        temp.grab_set()

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
        self.send_schedule_for_today_btn.destroy()
        self.send_schedule_backbtn.destroy()
        self.scrollable_frame_for_sms_schedule.destroy()
        self.main_manu_widgets()

    def send_sms_today_function(self):

        self.main_menu_buttons_frame.destroy()
        send_sms_img = PhotoImage(file=r"button_images/send_schedule_for_today.png")
        self.send_schedule_for_today_btn = Button(root, image=send_sms_img, bd=0, bg='#003B6D',
                                                  activebackground='#003B6D',
                                                  command=self.send_sms_today_function1)
        self.send_schedule_for_today_btn.image = send_sms_img
        self.send_schedule_for_today_btn.pack(padx=0, pady=0)

        # cancel_and_exit = PhotoImage(file=r"button_images/cancel_and_exit.png")
        self.send_schedule_backbtn = Button(root, text="Back <-", bd=1, bg='white', command=self.cance_and_exit)
        # self.cancel_and_exit_btn.image = cancel_and_exit
        self.send_schedule_backbtn.place(x=5, y=7)

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

        cursor.execute(f"select * from sent_schedules_list ")
        data = cursor.fetchall()

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

    def send_sms_today_function1(self):

        user_ids = []
        subjects = []
        selected_dates = []
        course_of_today = []
        # list of phone and emails from table to send
        mobile_number_list = []
        emails_list = []
        full_name = []
        gender_list = []

        # message_lists
        messages_list = []

        today = datetime.today().date()
        print(today)

        cursor.execute(f" SELECT * FROM  schedules WHERE date='{today}'")
        temp_data = cursor.fetchall()
        print(temp_data)

        for i in temp_data:
            user_ids.append(i[1])
            subjects.append(i[3])
            selected_dates.append(i[6])
            course_of_today.append(i[7])
        print("user id",user_ids)
        print("subject",subjects)
        print("date",selected_dates)
        print("course",course_of_today)

        # select phone and e mail for further function below to send sms and email
        for k in user_ids:

            cursor.execute(f"SELECT  mobile ,email,full_name,gender from users where id ={k}")
            data = cursor.fetchall()
            for phn in data:
                mobile_number_list.append(phn[0])
                emails_list.append(phn[1])
                full_name.append(phn[2])
                gender_list.append(phn[3])

        message_body = ","

        for i, (user_id, gender, name, sub, date, content) in enumerate(
                zip(user_ids, gender_list, full_name, subjects, selected_dates, course_of_today)):

            if gender == 'Female':
                message_body += " Dear Miss. " + name
            elif gender == "Male":
                message_body += " Dear Mr. " + name
            message_body += f"  Your schedule for the subject: {sub} of  date: {date} is as follows:   {content}"
            messages_list.append(message_body)


            cursor.execute(f"""INSERT INTO sent_schedules_list(schedule_id ,fulll_name ,mobile ,subject ,date ,content)VALUES('{user_id}', '{name}', '{mobile_number_list[i]}', '{sub}', '{str(date)}', '{str(content).replace("'","")}')""")
            print((user_id, name, mobile_number_list[i], sub, str(date), content))
            db.commit()

        acc_id = "AC18b9a56798200796bf4c76f9a96fef51"
        accunt_token = "f3afbf238c689b91e2dff0dab58e8c2a"
        client = Client(acc_id, accunt_token)
        for i in range(len(messages_list)):
            client.messages.create(to="+92312212882828", from_="+12135831372", body=messages_list[i])

        user_ids.clear()
        subjects.clear()
        selected_dates.clear()
        course_of_today.clear()
        mobile_number_list.clear()
        emails_list.clear()
        full_name.clear()
        gender_list.clear()
        messages_list.clear()

        msb.showinfo("Congratulation", f"Your schedule for {datetime.today().date()} has been successfully sent.")


        # send sms on phone numbers

    def send_announcements(self):
        self.back_button_from_announcements = Button(root, text="Back <-", relief=FLAT, bg='white', bd=0,
                                                     command=self.destroy_announcments)
        self.back_button_from_announcements.place(x=5, y=7)

        self.main_menu_buttons_frame.destroy()
        self.parentframe_announcement = Frame(root, bg="#bfc7c5", bd=0, width=screenwidth - 200,
                                              height=screenheight - 200, )
        self.parentframe_announcement.pack(padx=50, pady=100, anchor=CENTER)

        self.announcements_frame = LabelFrame(self.parentframe_announcement, bg="#bfc7c5", bd=0, width=500, height=300)
        self.announcements_frame.place(x=150, y=20)

        #############################################################################################################
        self.back_button_from_announcements_ = ttk.Button(self.parentframe_announcement, text="Create Announcement",
                                                          command=self.create_announcement_top)
        self.back_button_from_announcements_.place(x=10, y=10)

        canvas = Canvas(self.announcements_frame, width=1100, height=550)
        scrollbar = ttk.Scrollbar(self.announcements_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # variable for checkbox below
        self.checkvar = StringVar()
        # add content to scrollable frame
        self.date_of_announcement = Label(scrollable_frame, text="Date")
        self.date_of_announcement.grid(row=0, column=0, padx=(20, 20))

        self.heading_of_announcement = Label(scrollable_frame, text="Heading")
        self.heading_of_announcement.grid(row=0, column=1, padx=(100, 100))

        self.body_of_announcement = Label(scrollable_frame, text="Body")
        self.body_of_announcement.grid(row=0, column=2, padx=(100, 100))

        self.status_of_announcement = Label(scrollable_frame, text="Status")
        self.status_of_announcement.grid(row=0, column=3, padx=(50, 50))

        # checkbox list
        self.list_for_announcement_checkboxes = []

        self.views_list_values = []
        self.cbVariables = {}
        cursor.execute("select * from Announcements")
        data = cursor.fetchall()
        for k in data:
            self.views_list_values.append(k[4])

        for i in range(len(data)):

            self.cbVariables[i] = StringVar()
            # self.cbVariables.append(StringVar())
            self.date_of_announcement_value = Label(scrollable_frame, text=str(data[i][2]))
            self.date_of_announcement_value.grid(row=i + 1, column=0, padx=(20, 20))

            self.heading_of_announcement_value = Label(scrollable_frame, text=str(data[i][1]))
            self.heading_of_announcement_value.grid(row=i + 1, column=1, padx=(100, 100), )

            self.body_of_announcement_value = Label(scrollable_frame, text=str(data[i][3]), wraplength=200)
            self.body_of_announcement_value.grid(row=i + 1, column=2, padx=(100, 100))

            self.list_for_announcement_checkboxes.append(ttk.Checkbutton(scrollable_frame, variable=self.cbVariables[i]
                                                                         , onvalue='check' + str(i),
                                                                         offvalue='uncheck' + str(i),
                                                                         command=partial(
                                                                             self.update_announcement_status, i)))
            self.list_for_announcement_checkboxes[i].grid(row=i + 1, column=3, padx=(50, 50))

            if self.views_list_values[i] == 'selected':
                self.list_for_announcement_checkboxes[i].state(['selected'])

            # self.lineberak = Label(scrollable_frame, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            #                        bg="#bfc7c5")
            # self.lineberak.grid(row=i+1, column=0,columnspan=4,  pady=(150, 150))

        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")

        #############################################################################################################

    def create_announcement_top(self):
        self.announcements_toplvel = Toplevel(self.announcements_frame,
                                              width=screenwidth - 400, bg="#bfc7c5",
                                              height=screenheight - 250, )
        self.announcements_toplvel.geometry('550x600')
        self.announcements_toplvel.grab_set()
        self.announcements_toplvel.resizable(0, 0)
        # dumy labels

        # heading for announce

        self.heading_of_announcement_label = Label(self.announcements_toplvel, bg="#bfc7c5",
                                                   text="Heading for announcement")
        self.heading_of_announcement_label.grid(row=0, column=0, padx=(20, 0), pady=(15, 15))
        self.heading_of_announcement_entry = ttk.Entry(self.announcements_toplvel, width=43)

        self.heading_of_announcement_entry.grid(row=0, column=1, padx=(30, 0))
        # date for announcement
        self.date_for_announcement_label = Label(self.announcements_toplvel, bg="#bfc7c5", text="Date for announcement")
        self.date_for_announcement_label.grid(row=1, column=0)

        self.date_for_announcement_entry = tkcalendar.DateEntry(self.announcements_toplvel, selectmode='day',
                                                                date_pattern='dd-mm-y', width=43)
        self.date_for_announcement_entry.grid(row=1, column=1, padx=(10, 0))

        self.announcements_body = Text(self.announcements_toplvel, wrap="word", width=60)
        self.lineberak = Label(self.announcements_toplvel, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                               bg="#bfc7c5")
        self.lineberak.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # separator = ttk.Separator(self.announcements_toplvel, orient='horizontal')
        # separator.grid(row=2,column=0,columnspan=2)

        self.announcements_body.grid(row=3, column=0, columnspan=2, padx=(40, 30), pady=(20, 20))

        self.savebtn_for_announcement = ttk.Button(self.announcements_toplvel, text="Save",
                                                   command=self.save_announcement_todb)
        self.savebtn_for_announcement.grid(row=4, column=1, padx=(30, 0))

    def save_announcement_todb(self):
        query = 'INSERT INTO Announcements(heading ,date , body )VALUES(%s,%s,%s)'
        cursor.execute(query, (self.heading_of_announcement_entry.get(), self.date_for_announcement_entry.get(),
                               self.announcements_body.get('1.0', END)))
        db.commit()
        msb.showinfo("", "Announcement has been added ")

    def update_announcement_status(self, i):

        # print(self.checkvar.get())
        print(i)
        print("entrd this section")
        print(self.cbVariables[i].get())

        if self.cbVariables[i].get().startswith('c'):
            cursor.execute(f"UPDATE Announcements  SET  show_ann = 'selected' WHERE id = '{i + 1}'")
            db.commit()
            # self.checkvar.set('')
            print(" i am checkd for", i)
            # msb.showinfo("", "Conratulations ! Status has been updated")
        if self.cbVariables[i].get().startswith('u'):
            cursor.execute(f"UPDATE Announcements  SET  show_ann = 'unselected' WHERE id = '{i + 1}'")
            db.commit()
            # self.checkvar.set('')
            print("i am not checkedout")
            # msb.showinfo("", "Conratulations ! Status has been updated")

    def destroy_announcments(self):
        self.announcements_frame.destroy()
        self.main_manu_widgets()
        self.back_button_from_announcements.destroy()
        self.back_button_from_announcements_.destroy()
        self.parentframe_announcement.destroy()


obj = admin()
root.mainloop()
