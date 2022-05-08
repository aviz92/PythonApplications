import logging
from tkinter import *
import datetime

from PythonApplications.Phone_DataBase.backend import Database
from PrivateInfrastructure.Files_Infrastructure.Folders.Path_folders_Infrastructure import PathFoldersClass


class PhoneDatabaseClass:

    def __init__(self):
        self.logger = \
            logging.getLogger('Infrastructure.Logger_Infrastructure.Projects_Logger.' + self.__class__.__name__)

    def phone_database_creator(self, user_domain, admin_mode):
        database_name = PathFoldersClass().return_to_username_path()
        if database_name:
            database_name = database_name + '\\Documents\\PhoneDataBase.db'
        else:
            database_name = 'PhoneDataBase.db'
        self.logger.info("The path to data base is: " + str(database_name))
        database = Database(database_name)

        def get_selected_row(event):
            global selected_tuple
            index = list1.curselection()
            if type(index) is tuple and index:
                selected_tuple = list1.get(index)
                # self.logger.debug(list1.get(index))
                e1.delete(0, END)
                e1.insert(END, str(selected_tuple[1]).replace("Title: ", ""))
                e2.delete(0, END)
                e2.insert(END, selected_tuple[2].replace("Owner: ", "").replace("Manual ", ""))
                e3.delete(0, END)
                e3.insert(END, selected_tuple[3].replace("Date: ", "").replace("Manual ", ""))
                e4.delete(0, END)
                e4.insert(END, selected_tuple[4].replace("S.N: ", ""))
            else:
                pass

        def view_command():
            list1.delete(0, END)
            for row in database.view():
                list1.insert(END, row)

        def search_command():
            list1.delete(0, END)
            # for row in database.search("Title: " + title_text.get(), "Owner: " + owner_text.get(),
            #                            "Date: " + date_text.get(), "S.N: " + serial_number_text.get()):
            for row in database.search(title_text.get(), owner_text.get(), date_text.get(), serial_number_text.get()):
                list1.insert(END, row)

        def add_command():
            global signature1

            current_date_and_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            # current_time = datetime.datetime.now().strftime("%H:%M:%S")

            if 'Select an action' not in title_text.get() and serial_number_text.get() != '':
                if admin_mode == 1:
                    if owner_text.get():
                        owner_name = "Manual Owner: " + owner_text.get()
                    else:
                        owner_name = "Owner: " + user_domain
                    if date_text.get():
                        date_and_time = "Manual Date: " + date_text.get()
                    else:
                        date_and_time = "Date: " + current_date_and_time

                else:
                    owner_name = "Owner: " + user_domain
                    date_and_time = "Date: " + current_date_and_time

                database.insert("Title: " + title_text.get(), owner_name, date_and_time,
                                "S.N: " + serial_number_text.get())
                list1.delete(0, END)
                list1.insert(END, ("Title: " + title_text.get(), owner_name, date_and_time,
                                   "S.N: " + serial_number_text.get()))
                signature1.after(1, signature1.destroy)
                signature1 = Label(window, text='Add entry - Successful !', font="Verdana 10 underline")
                signature1.grid(row=5, column=3, columnspan=3)
                view_command()
                signature1.after(10000, signature1.destroy)
            else:
                signature1.after(1, signature1.destroy)
                if 'Select an action' in title_text.get() and serial_number_text.get() == '':
                    signature1 = Label(window, text='Need to fill the fields:\n"Select an action" and "Serial number"'
                                                    '\nplease try again',
                                       font="Verdana 10 underline")
                elif 'Select an action' in title_text.get():
                    signature1 = Label(window, text='Need to fill the field:\n"Select an action" \nplease try again',
                                       font="Verdana 10 underline")
                elif serial_number_text.get() == '':
                    signature1 = Label(window, text='Need to fill the field:\n"Serial number" \nplease try again',
                                       font="Verdana 10 underline")
                else:
                    signature1 = Label(window, text="", font="Verdana 10")
                signature1.grid(row=5, column=3, columnspan=3)

        def update_command():
            current_date_and_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            # current_time = datetime.datetime.now().strftime("%H:%M:%S")
            try:
                if admin_mode == 1:
                    if owner_text.get():
                        owner_name = "Manual Owner: " + owner_text.get()
                    else:
                        owner_name = "Owner: " + user_domain
                    if date_text.get():
                        date_and_time = "Manual Date: " + date_text.get()
                    else:
                        date_and_time = "Date: " + current_date_and_time

                else:
                    owner_name = "Owner: " + user_domain
                    date_and_time = "Date: " + current_date_and_time

                database.update(selected_tuple[0], "Title: " + title_text.get(), owner_name, date_and_time,
                                "S.N: " + serial_number_text.get())
            except NameError:
                pass
            view_command()

        def delete_command():
            try:
                database.delete(selected_tuple[0])
            except NameError:
                pass
            view_command()

        def clear_fields():
            e1.delete(0, END)
            title_text.set(" Select an action")  # default value
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)

        try:
            window = Tk()

            global signature1

            window.wm_title("Phone DataBase Creator")

            l1 = Label(window, text="*Title")
            l1.grid(row=0, column=2)

            l2 = Label(window, text="Owner")
            l2.grid(row=0, column=4)

            l3 = Label(window, text="Date")
            l3.grid(row=1, column=2)

            l4 = Label(window, text="*Serial Number")
            l4.grid(row=1, column=4)

            # title_text = StringVar()
            # e1 = Entry(window, textvariable=title_text)
            # e1.grid(row=0, column=3)

            #
            title_text = StringVar()
            title_text.set(" Select an action")  # default value  # 18 "chars"
            e1 = Entry(window, textvariable=title_text)
            title_text2 = OptionMenu(window, title_text,
                                     " Taking a device ",  # "17" chars
                                     " Return device    ", )  # "18" chars
            title_text2.grid(row=0, column=3)
            #

            owner_text = StringVar()
            if admin_mode == 1:
                e2 = Entry(window, textvariable=owner_text)
            else:
                e2 = Entry(window, textvariable=owner_text, state='disable')
            e2.grid(row=0, column=5)

            date_text = StringVar()
            if admin_mode == 1:
                e3 = Entry(window, textvariable=date_text)
            else:
                e3 = Entry(window, textvariable=date_text, state='disable')
            e3.grid(row=1, column=3)

            serial_number_text = StringVar()
            e4 = Entry(window, textvariable=serial_number_text)
            e4.grid(row=1, column=5)

            # list1 = Listbox(window, selectmode=EXTENDED, height=20, width=80)  # for multi select
            list1 = Listbox(window, height=20, width=80)
            list1.grid(row=3, column=0, rowspan=6, columnspan=2)

            y_sb = Scrollbar(window, orient="vertical")
            y_sb.grid(row=3, column=2, rowspan=6, sticky='ns')

            x_sb = Scrollbar(window, orient="horizontal")
            x_sb.grid(row=9, column=0, columnspan=2, sticky=N + S + E + W)

            list1.configure(yscrollcommand=y_sb.set, xscrollcommand=x_sb.set)
            y_sb.configure(command=list1.yview)
            x_sb.configure(command=list1.xview)

            list1.bind('<<ListboxSelect>>', get_selected_row)

            label_space_1_2 = Label(window, text="  ")
            label_space_1_2.grid(row=2, column=1)

            b1 = Button(window, text="View all", width=12, command=view_command)
            b1.grid(row=1, column=0)

            b2 = Button(window, text="Search entry", width=12, command=search_command)
            b2.grid(row=1, column=1)

            label_space_3 = Label(window, text="  ")
            label_space_3.grid(row=0, column=6)

            b3 = Button(window, text="Add entry", width=12, command=add_command)
            b3.grid(row=3, column=3)

            label_space_4 = Label(window, text="  ")
            label_space_4.grid(row=1, column=6)

            if admin_mode == 1:
                b4 = Button(window, text="Update selected", width=12, command=update_command)
                b4.grid(row=3, column=4)
            else:
                b4 = Button(window, text="Update selected", width=12, state='disable', command=update_command)
                b4.grid(row=3, column=4)

            label_space_5 = Label(window, text="  ")
            label_space_5.grid(row=2, column=6)

            if admin_mode == 1:
                b5 = Button(window, text="Delete selected", width=12, command=delete_command)
                b5.grid(row=3, column=5)
            else:
                b5 = Button(window, text="Delete selected", width=12, state='disable', command=delete_command)
                b5.grid(row=3, column=5)

            #
            label_space_5 = Label(window, text="  ")
            label_space_5.grid(row=2, column=6)

            b5 = Button(window, text="clear fields", width=12, command=clear_fields)
            b5.grid(row=1, column=7)
            #

            label_space_6 = Label(window, text="  ")
            label_space_6.grid(row=3, column=6)

            b6 = Button(window, text="Close", width=12, command=window.destroy)
            b6.grid(row=8, column=7)

            label_space_6_1 = Label(window, text="  ")
            label_space_6_1.grid(row=8, column=8)

            signature1 = Label(window, text="                                                     ",
                               font="Verdana 10")
            signature1.grid(row=5, column=3, columnspan=3)

            window.mainloop()
        except Exception:
            self.logger.exception('')
