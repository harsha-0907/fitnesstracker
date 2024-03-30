#!bin/python3
import _tkinter
from tkinter import ttk
import mysql.connector as sql
import tkinter as tk

# Definitions
try:
    cnx = sql.connect(host="localhost", port=3306, username="root", password="Password1", database="fitnessdb")
    cursor = cnx.cursor()
except sql.Error:
    print("Unable TO Connect to Database")
    exit(0)


def end():
    cnx.close()
    exit(0)


# noinspection PyArgumentList,PyTypeChecker,PyMethodMayBeStatic,PySimplifyBooleanCheck,PyRedundantParentheses,
# PyShadowingNames
# noinspection PyShadowingNames,PyRedundantParentheses,PySimplifyBooleanCheck,PyUnusedLocal,SqlNoDataSourceInspection,PyMethodMayBeStatic
class FitnessTracker:
    nextPage = False

    def __init__(self, _cnx, _cursor):
        self.api_export_button = None
        self.api_exit_button = None
        self.api_workout_button = None
        self.timedFieldLTextLabel = None
        self.timedFieldRoot = None
        self.api_goal_button = None
        self.api_nutrition_button = None
        self.api_workout_name_label = None
        self.username = None
        self.api_Root = None
        self.login_page_note_label = None
        self.login_username_entry = None
        self.login_register_button = None
        self.login_login_button = None
        self.login_password_entry = None
        self.login_username_label = None
        self.login_password_label = None
        self.loginPageRoot = None
        self.exitPageButton = None
        self.exit_registration_button = None
        self.registration_display_notice_label = None
        self.registration_reset_button = None
        self.registration_submit_button = None
        self.registration_re_type_passwd_entry = None
        self.registration_passwd_entry = None
        self.registration_age_entry = None
        self.registration_name_entry = None
        self.registration_re_type_passwd_label = None
        self.registration_passwd_label = None
        self.registration_age_label = None
        self.registration_display_label = None
        self.registration_name_label = None
        self.registration_page_root = None
        self.cnx = _cnx
        self.cursor = _cursor
        self.registration_button = None
        self.login_button = None
        self.opening_page_root = None
        self.openingLabel = None
        self.buttons = None
        print("Welcome to Fitness Tracker")
        self.cursor.execute("use fitnessdb;")
        self.openingPage()
        if FitnessTracker.nextPage:
            print("User")
            self.applicationInterface()
        else:
            pass

    def exitOpeningPage(self):
        self.opening_page_root.destroy()

    def openingPage(self):

        self.opening_page_root = tk.Tk()
        self.opening_page_root.title("Welcome To Group-11")
        self.opening_page_root.geometry("1000x600")
        self.buttons = []
        self.openingLabel = tk.Label(self.opening_page_root, text="Welcome to MVGR Tracker", font=("Arial", 20))
        self.openingLabel.place(x=365, y=100)
        self.registration_button = tk.Button(self.opening_page_root, text="Register Here!", width=10, height=1,
                                             command=self.registrationPage)
        self.login_button = tk.Button(self.opening_page_root, text="Login Here!", width=10, height=1,
                                      command=self.loginPage)
        self.exitPageButton = tk.Button(self.opening_page_root, text="Exit", width=10, height=1,
                                        command=self.exitOpeningPage)
        self.buttons.extend([self.registration_button, self.login_button, self.exitPageButton])
        for button in self.buttons:
            button.pack()
        self.registration_button.place(x=500, y=200)
        self.login_button.place(x=500, y=250)
        self.exitPageButton.place(x=500, y=300)
        self.opening_page_root.mainloop()

    # Now We Proceed to The Next Page(USer)

    def registrationPage(self):  # 600x500
        def exitRegistrationForm():
            self.registration_page_root.destroy()

        def validateRegistrationSubmitData():
            name = self.registration_name_entry.get()
            age = self.registration_age_entry.get()
            passwd = self.registration_passwd_entry.get()
            retype_passswd = self.registration_re_type_passwd_entry.get()

            if name == "" or age == "" or passwd == "" or retype_passswd == "":
                # Incomplete Form
                print("Form Incomplete..")
                self.registration_display_notice_label.config(text="Notice : All Fields Have To Be Filled")
                return 0

            elif passwd != retype_passswd:
                print("Password Mismatch..")
                self.registration_re_type_passwd_entry.delete(0, tk.END)
                self.registration_display_notice_label.config(text="Notice: Password Mismatch")
                return 0
            else:
                try:
                    age = int(age)
                    print(age)
                    return 1
                except ValueError:
                    self.registration_display_notice_label.config(text="Age is Wrong Enter it in Integers!")
                    self.registration_age_entry.delete(0, tk.END)
                    return 0

        def submitRegistrationData():
            if validateRegistrationSubmitData():
                name = self.registration_name_entry.get()
                username = name.replace(" ", '')
                age = int(self.registration_age_entry.get())
                passwd = self.registration_passwd_entry.get()
                try:
                    # Query-1
                    query = "insert into Credentials values(%s,%s)"
                    self.cursor.execute(query, (username, passwd))
                    # Query-2
                    query = f"insert into user values ('{username}', '{name}', {age})"
                    self.cursor.execute(query)
                    self.cnx.commit()
                    print("Registration Complete...")
                    self.registration_display_notice_label.config(
                        text="Notice : Your Account Has Been Created Successfully")
                    TimedField(
                        f"Registration Successfull...\n You may Login Now\n Username : {username}\nPassword : {passwd}",
                        None)
                # exitRegistrationForm()
                except sql.errors.IntegrityError:
                    TimedField("UserName Already Taken\n Try With Another One...", None)
                except sql.errors.ProgrammingError:
                    TimedField("Internal Error Occured", None)

        def resetRegistrationForm():
            print("REset Registration Form")
            self.registration_name_entry.delete(0, tk.END)
            self.registration_age_entry.delete(0, tk.END)
            self.registration_passwd_entry.delete(0, tk.END)
            self.registration_re_type_passwd_entry.delete(0, tk.END)

        print("Welcome to Registration Page")
        self.registration_page_root = tk.Tk()
        self.registration_page_root.title("Registrations")
        self.registration_page_root.geometry("600x500")
        # Labels
        self.registration_display_label = tk.Label(self.registration_page_root, text="REGISTRATION PORTAL",
                                                   font=("Arial", 20))
        self.registration_display_notice_label = tk.Label(self.registration_page_root, text="Notice : ")
        self.registration_display_notice_label.place(x=200, y=450)
        self.registration_display_label.place(x=205, y=60)
        self.registration_name_label = tk.Label(self.registration_page_root, text="Name : ")
        self.registration_age_label = tk.Label(self.registration_page_root, text="Age : ")
        self.registration_passwd_label = tk.Label(self.registration_page_root, text="Password : ")
        self.registration_re_type_passwd_label = tk.Label(self.registration_page_root, text="Re-Type Password : ")
        self.registration_name_label.place(x=225, y=110)
        self.registration_age_label.place(x=225, y=130)
        self.registration_passwd_label.place(x=225, y=150)
        self.registration_re_type_passwd_label.place(x=225, y=170)
        # Entries
        self.registration_name_entry = tk.Entry(self.registration_page_root)
        self.registration_age_entry = tk.Entry(self.registration_page_root)
        self.registration_passwd_entry = tk.Entry(self.registration_page_root)
        self.registration_re_type_passwd_entry = tk.Entry(self.registration_page_root)
        self.registration_name_entry.place(x=350, y=110)
        self.registration_age_entry.place(x=350, y=130)
        self.registration_passwd_entry.place(x=350, y=150)
        self.registration_re_type_passwd_entry.place(x=350, y=170)
        # Buttons
        self.registration_submit_button = tk.Button(self.registration_page_root, text="Submit",
                                                    command=submitRegistrationData)
        self.registration_reset_button = tk.Button(self.registration_page_root, text=" Reset ",
                                                   command=resetRegistrationForm)
        self.exit_registration_button = tk.Button(self.registration_page_root, text="   Exit   ",
                                                  command=exitRegistrationForm)
        self.exit_registration_button.place(x=300, y=250)
        self.registration_submit_button.place(x=260, y=210)
        self.registration_reset_button.place(x=345, y=210)
        self.registration_page_root.mainloop()

    def loginPage(self):  # 650x500
        def exitLoginPage():
            self.loginPageRoot.destroy()

        def LoginValidateUserAccount():
            username = self.login_username_entry.get()
            password = self.login_password_entry.get()
            query = "select username,password from Credentials where username=%s and password=%s"
            self.cursor.execute(query, (username, password))
            results = self.cursor.fetchall()
            print(results)
            try:
                (valid_username, valid_password) = results[0]
                if valid_username == username and valid_password == password:
                    print("Authenticated User")
                    self.username = username
                    self.password = password
                    self.loginPageRoot.destroy()
                    self.opening_page_root.destroy()
                    # self.timedField(f"You are Authenticated : {username}", 1)
                    FitnessTracker.nextPage = True
            except IndexError:
                print("Wrong Credentials")
                self.login_page_note_label.config(text="Note : Credentials Not Found")
                self.login_password_entry.delete(0, tk.END)

        print("Welcome to Login Page")
        self.loginPageRoot = tk.Tk()
        self.loginPageRoot.geometry("650x500")
        self.loginPageRoot.title("Login Page")
        # Labels
        self.login_username_label = tk.Label(self.loginPageRoot, text="Username : ")
        self.login_password_label = tk.Label(self.loginPageRoot, text="Password : ")
        self.login_page_note_label = tk.Label(self.loginPageRoot, text="")
        loginPageLabels = [self.login_username_label, self.login_password_label, self.login_page_note_label]
        for label in loginPageLabels:
            label.pack()
        self.login_username_label.place(x=230, y=200)
        self.login_password_label.place(x=230, y=230)
        self.login_page_note_label.place(x=240, y=350)
        # Entries
        self.login_username_entry = tk.Entry(self.loginPageRoot)
        self.login_password_entry = tk.Entry(self.loginPageRoot)
        self.login_username_entry.place(x=300, y=200)
        self.login_password_entry.place(x=300, y=230)
        # Buttons
        self.login_login_button = tk.Button(self.loginPageRoot, text="Login", command=LoginValidateUserAccount)
        self.login_register_button = tk.Button(self.loginPageRoot, text="Register", command=exitLoginPage)
        self.login_login_button.place(x=280, y=270)
        self.login_register_button.place(x=370, y=270)

    def timedField(self, message, timne=None):
        print(message)
        self.timedFieldRoot = tk.Tk()
        self.timedFieldRoot.geometry("400x400")
        self.timedFieldLTextLabel = tk.Label(self.timedFieldRoot, text=message)
        self.timedFieldLTextLabel.place(x=100, y=100)
        if timne is not None:
            print('rgg')
            self.timedFieldRoot.after(timne * 1000, self.destroyTimedFieldWindow())
        self.timedFieldRoot.mainloop()

    def destroyTimedFieldWindow(self):
        self.timedFieldRoot.destroy()

    def applicationInterface(self):
        def exportData():
            def getData():
                print("Hi")
                query = f"SELECT * FROM user_performs_workout WHERE user_USerID = '{self.username}';"
                self.cursor.execute(query)
                data = self.cursor.fetchall()
                if data == []:
                    print("No Data Available..")
                else:
                    new_root1 = tk.Tk()
                    with open(rf"C:\Users\Harsha\Desktop\Export Data\{self.username}", mode='w') as h:
                        h.write("USERID\tWORKOUTID\tCALORIESBURNT\tDAY\n")
                        for row in data:
                            h.write(row[0]+'\t'+str(row[1])+'\t'+str(row[2])+'\t'+str(row[3])+'\n')
            getData()
        def destroyPage():
            self.api_Root.destroy()

        def updateWorkoutData():
            def resetAPIData():
                self.api_update_day_entry.delete(0, tk.END)
                self.api_update_workoutId_entry.delete(0, tk.END)
                self.api_update_caloriesBurnt_entry.delete(0, tk.END)

            def validateData():
                day = self.api_update_day_entry.get()
                workoutId = self.api_update_workoutId_entry.get()
                caloriesBurnt = self.api_update_caloriesBurnt_entry.get()
                if day == "" or workoutId == "":
                    self.api_update_label.config(text="Note : All Fields Are Mandatory")
                    return (0, 0, 0, 0)
                try:
                    workoutId = int(workoutId)
                    __query = f"select WorkoutID from workout where WorkoutID = {workoutId}"
                    self.cursor.execute(__query)
                    day = int(day)
                    workoutId = self.cursor.fetchall()
                    # noinspection PySimplifyBooleanCheck
                    if workoutId == []:
                        self.api_update_label.config(text="Note : Invalid Workout Data")
                        return (0, 0, 0, 0)
                    else:
                        workoutId = workoutId[0][0]
                        if caloriesBurnt == "":
                            _query = "select DefaultCaloriesBurned from workout where workoutId=%d"
                            self.cursor.execute(_query, (workoutId))
                            caloriesBurnt = self.cursor.fetchall()[0][0]
                        else:
                            caloriesBurnt = int(caloriesBurnt)

                        return (1, workoutId, caloriesBurnt, day)
                except (sql.errors.DataError, sql.errors.InternalError):
                    self.api_update_label.config(text="Note : Unknown Error Has Occured")
                    return (0, 0, 0, 0)
                except ValueError:
                    self.api_update_label.config(text="Note : Fields are all Integer")
                    return (0, 0, 0, 0)

            def updateData():
                res = validateData()
                if res[0]:
                    workoutId = res[1]
                    caloriesBurnt = res[2]
                    day = res[3]
                    query_ = r"INSERT INTO user_performs_workout(user_UserID, workout_WorkoutID, CaloriesBurnt, Day) VALUES (%s, %s, %s, %s)"
                    try:
                        print(self.username, workoutId, caloriesBurnt, day)
                        self.cursor.execute(query_, (self.username, workoutId, caloriesBurnt, day))
                        self.cnx.commit()
                        self.api_update_label.config(text="Note : Successful...")
                    except sql.errors.IntegrityError:
                        self.api_update_label.config(text="Note : Duplicate Entries Found")

            # Labels
            self.api_update_Root = tk.Tk()
            self.api_update_Root.geometry("650x350")
            self.api_update_Root.title("Today's Workout")
            self.api_update_day = tk.Label(self.api_update_Root, text="    Day ")
            self.api_update_workoutId = tk.Label(self.api_update_Root, text="WorkOut Id  ")
            self.api_update_caloriesBurnt = tk.Label(self.api_update_Root, text="Calories Burnt ")
            self.api_update_label = tk.Label(self.api_update_Root, text="")
            labels = [self.api_update_caloriesBurnt, self.api_update_day, self.api_update_workoutId,
                      self.api_update_label]
            for label in labels:
                label.pack()
            # Entries
            self.api_update_day_entry = tk.Entry(self.api_update_Root)
            self.api_update_workoutId_entry = tk.Entry(self.api_update_Root)
            self.api_update_caloriesBurnt_entry = tk.Entry(self.api_update_Root)
            # Button
            self.api_update_submit_button = tk.Button(self.api_update_Root, text="Submit ", command=updateData)
            self.api_update_reset_button = tk.Button(self.api_update_Root, text=" Reset ", command=resetAPIData)
            # Place
            self.api_update_label.place(x=250, y=270)
            self.api_update_day.place(x=220, y=100)
            self.api_update_workoutId.place(x=220, y=130)
            self.api_update_caloriesBurnt.place(x=220, y=160)
            self.api_update_day_entry.place(x=330, y=100)
            self.api_update_workoutId_entry.place(x=330, y=130)
            self.api_update_caloriesBurnt_entry.place(x=330, y=160)
            self.api_update_submit_button.place(x=270, y=200)
            self.api_update_reset_button.place(x=350, y=200)

            self.api_update_Root.mainloop()

        def manageWorkoutData():  # 650x350
            def getALlWorkoutData():
                print("Fetching ALl Workout Data")
                query1 = f"SELECT * FROM user_performs_workout WHERE user_USerID = '{self.username}';"
                self.cursor.execute(query1)
                data = self.cursor.fetchall()
                if data == []:
                    self.api_statistics_label.config(text="Note : No Data Found")
                else:
                    new_root1 = tk.Tk()
                    headers = ["USER_ID", "WORKOUT_ID", "CALORIESBURNT", "DAY"]
                    self.create_dynamic_table(new_root1, headers, data)

            def resetManageWorkoutData():
                self.api_statistics_day_entry.delete(0, tk.END)
                self.api_statistics_workoutID_entry.delete(0, tk.END)

            def getWorkoutData():
                day = self.api_statistics_day_entry.get()
                workoutId = self.api_statistics_workoutID_entry.get()
                if day == '' and workoutId == '':
                    self.api_statistics_label.config(text="NOte : No Parameter Passed")
                    return 0

                try:
                    base_query = f"SELECT * FROM fitnessdb.user_performs_workout WHERE user_USerID = %s"
                    params = (self.username,)
                    if workoutId != '' and day == '':
                        base_query += "  AND workout_WorkoutID = %s;"
                        print("Hi")
                        params += (int(workoutId),)
                        print(workoutId, type(workoutId))
                    elif day != '' and workoutId == '':
                        base_query += " AND Day = %s;"
                        params += (int(day),)
                    else:
                        base_query = base_query + " AND  workout_WorkoutID = %s AND Day IN (SELECT Day FROM user_performs_workout WHERE Day = %s);"
                        params += (int(workoutId), int(day))
                    print(base_query, params)
                    self.cursor.execute(base_query, params)
                    data = self.cursor.fetchall()
                    if data == []:
                        self.api_statistics_label.config(text="No Data Found...")
                    else:
                        headers = ["USER_ID", "WORKOUT_ID", "CALORIESBURNT", "DAY"]
                        self.api_statistics_label.config(text="Note : Data Fetch Successful")
                        self.new_root = tk.Tk()
                        self.create_dynamic_table(self.new_root, headers, data)
                        self.new_root.mainloop()
                except ValueError:
                    self.api_statistics_label.config(text="Note : Data Un-Identifiable(Check Data)")
                    return 0

            self.api_manageRoot = tk.Tk()
            self.api_manageRoot.geometry("650x350")
            self.api_manageRoot.title("MAnage Data")
            # Labels
            self.api_statistics_day = tk.Label(self.api_manageRoot, text="   Day   ")
            self.api_statistics_workoutID = tk.Label(self.api_manageRoot, text="Workout ID ")
            self.api_statistics_label = tk.Label(self.api_manageRoot, text="")
            labels = [self.api_statistics_workoutID, self.api_statistics_workoutID]
            for label in labels:
                label.pack()
            # Entries
            self.api_statistics_day_entry = tk.Entry(self.api_manageRoot)
            self.api_statistics_workoutID_entry = tk.Entry(self.api_manageRoot)
            # Buttons
            self.api_manage_getData_button = tk.Button(self.api_manageRoot, text="Get Data", command=getWorkoutData)
            self.api_manage_reset_button = tk.Button(self.api_manageRoot, text=" Reset ",
                                                     command=resetManageWorkoutData)
            self.api_getAllData = tk.Button(self.api_manageRoot, text="Show All Data", command=getALlWorkoutData)
            # Placement
            self.api_statistics_day.place(x=195, y=50)
            self.api_statistics_day_entry.place(x=270, y=50)
            self.api_statistics_workoutID.place(x=195, y=75)
            self.api_statistics_workoutID_entry.place(x=270, y=75)
            self.api_manage_getData_button.place(x=245, y=110)
            self.api_manage_reset_button.place(x=330, y=110)
            self.api_getAllData.place(x=250, y=170)
            self.api_statistics_label.place(x=250, y=220)
            self.api_manageRoot.mainloop()

        self.api_Root = tk.Tk()
        self.api_Root.title("USER PAGE")
        self.api_Root.geometry("750x500")
        # Labels
        self.api_workout_name_label = tk.Label(self.api_Root, text="Welcome " + self.username, font=("Arial", 20))
        self.api_workout_name_label.pack()
        self.api_workout_name_label.place(x=500, y=50)
        # Buttons
        BUTTONS = []
        font_style = ("Arial", 14)
        self.api_workout_button = tk.Button(self.api_Root, text=" Today's WorkOut ", font=font_style,
                                            command=updateWorkoutData)
        self.api_goal_button = tk.Button(self.api_Root, text="   Manage Activity   ", font=font_style,
                                         command=manageWorkoutData)
        self.api_export_button = tk.Button(self.api_Root, text="      Export      ", font=font_style,
                                           command=exportData)
        self.api_exit_button = tk.Button(self.api_Root, text="   Exit   ", font=font_style, command=destroyPage)
        BUTTONS.extend([self.api_goal_button, self.api_workout_button, self.api_exit_button, self.api_export_button])
        for button in BUTTONS:
            button.pack()
        self.api_goal_button.place(x=275, y=260)
        self.api_workout_button.place(x=275, y=210)
        self.api_exit_button.place(x=325, y=365)
        self.api_export_button.place(x=300, y=310)
        self.api_Root.mainloop()

        print()

    def create_dynamic_table(self, root, headers, data):
        # Create a Treeview widget
        tree = ttk.Treeview(root, columns=headers, show="headings")

        # Configure the Treeview style
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

        # Define column headings based on the provided headers
        for header in headers:
            tree.heading(header, text=header)

        # Insert data into the table
        for row_data in data:
            tree.insert("", "end", values=row_data)

        # Pack the Treeview widget
        tree.pack()


class TimedField:
    def __init__(self, message, timne=None):
        print(message)
        self.timedFieldRoot = tk.Tk()
        self.timedFieldRoot.geometry("400x400")
        self.timedFieldLTextLabel = tk.Label(self.timedFieldRoot, text=message)
        self.timedFieldLTextLabel.place(x=100, y=100)

        def destroy_window():
            self.timedFieldRoot.destroy()

        if timne is not None:
            print('rgg')
            self.timedFieldRoot.after(timne * 1000, destroy_window)

        self.timedFieldRoot.mainloop()


try:
    f1 = FitnessTracker(cnx, cursor)
except _tkinter.TclError:
    print("Tkinter Exception Occured ")
except KeyboardInterrupt:
    print("Exit Succesful")
