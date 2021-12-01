import sqlite3
from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, Entry, END, StringVar
from tkinter import ttk, Scrollbar, Toplevel


class Contacts:
    db_file = 'contacts.db'

    def __init__(self, root):
        self.root = root
        self.gui()
        ttk.Style().configure("Treeview.Heading", font="bold")

    """Db connection and adding info to it"""

    def execute_db(self, query, parameters=()):
        with sqlite3.connect(self.db_file) as conn:
            print(conn)
            print("You've successfully connected to the Database.")
            cursor = conn.cursor()
            qry_result = cursor.execute(query, parameters)
            conn.commit()
        return qry_result

    def gui(self):
        self.create_LeftIcon()
        self.labelFrame()
        self.msgs()
        self.treeView()
        self.create_scrollbar()
        self.create_BottomButton()
        self.viewContacts()

    @staticmethod
    def create_LeftIcon():
        photo = PhotoImage(file='Icon/logo.gif')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=2)

    def labelFrame(self):
        labelframe = LabelFrame(self.root, text="Create new Contact", bg="sky blue")
        labelframe.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        labelframe.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        Label(labelframe, bg="sky blue", text="Name", fg="green").grid(sticky="W", row=1, column=1, padx=15, pady=2)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1, column=2, padx=5, pady=2, sticky="W")
        Label(labelframe, text="Email", bg="sky blue", fg="Brown").grid(row=2, sticky="W", column=1, padx=15, pady=2)
        self.email_field = Entry(labelframe)
        self.email_field.grid(row=2, column=2, padx=5, pady=2, sticky="W")
        Label(labelframe, bg="sky blue", text="Number").grid(row=3, column=1, padx=15, pady=2, sticky="W")
        self.numfield = Entry(labelframe)
        self.numfield.grid(row=3, column=2, padx=5, pady=2, sticky="W")
        Button(labelframe, text="Add Contact", command=self.add_contact_button, bg="white",
               fg="Blue").grid(row=4, column=2, padx=5, pady=5)

    def msgs(self):
        self.message = Label(text='', fg="red")
        self.message.grid(row=3, column=1, sticky="E")

    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient="vertical", command=self.tree.yview())
        self.scrollbar.grid(row=6, column=3, rowspan=10, sticky='sn')

    def create_BottomButton(self):
        Button().grid(row=8, column=0, padx=50)
        Button(text='Delete Selected', command=self.on_delete_button, bg='white',
               fg='red', ).grid(row=8, column=1, sticky=W, padx=10, pady=20)
        Button(text="Modify Selected", command=self.on_modify_button, bg='white',
               fg='purple').grid(row=8, column=2, sticky=W)

    def treeView(self):
        self.tree = ttk.Treeview(height=10, columns=("Email", "Phone Number"))
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading("#0", text="Name", anchor=W)
        self.tree.heading("Email", text="Email Address", anchor=W)
        self.tree.heading("Phone Number", text='Contact Number', anchor=W)

    def add_contact_button(self):
        self.addNewContact()

    def on_delete_button(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = "No Item Selected to Delete."
            return
        self.deleteContacts()

    def on_modify_button(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No Item Selected to modify.'
            return
        self.choice()

    def addNewContact(self):
        """ If namefields aren't empty this code will run"""
        if self.newContactValidate():
            qry = 'Insert into contacts_list VALUES(NULL, ?, ?, ?)'
            parameters = (self.namefield.get(), self.email_field.get(), self.numfield.get())
            self.execute_db(qry, parameters)
            self.message['text'] = 'New contact "' + self.namefield.get() + '" added.'
            self.namefield.delete(0, END)
            self.email_field.delete(0, END)
            self.numfield.delete(0, END)
            self.viewContacts()
        else:
            if len(self.namefield.get()) == 0:
                self.message['text'] = 'Name field cannot be blank.'
            elif len(self.email_field.get()) == 0:
                self.message['text'] = 'Email field cannot be blank.'
            elif len(self.numfield.get()) == 0:
                self.message['text'] = 'Phone Number cannot be blank.'
            self.viewContacts()

    def choice(self):
        self.transient = Toplevel()
        self.transient.title('Update Choice')
        self.transient.resizable(width=False, height=False)
        btn = Button(self.transient, text="Update Name", command=self.on_name_button, bg="white",
                     fg="Blue")

        btn2 = Button(self.transient, text="Update Phone Number", command=self.on_number_button, bg="white",
               fg="Blue")

        btn3 = Button(self.transient, text="Update Email ID", command=self.on_email_button, bg="white",
               fg="Blue")

        btn.pack()
        btn2.pack()
        btn3.pack()

    def on_name_button(self):
        name = self.tree.item(self.tree.selection())['text']
        number = self.tree.item(self.tree.selection())['values'][1]
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as e:
            self.message['text'] = 'No Item Selected to modify.'
            return
        self.openNameModifyWindow(name, number)


    def on_email_button(self):
        name = self.tree.item(self.tree.selection())['text']
        email = self.tree.item(self.tree.selection())['values'][0]
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No Item Selected to modify.'
            return
        self.openEmailModifyWindow(name, email)

    def on_number_button(self):
        name = self.tree.item(self.tree.selection())['text']
        number = self.tree.item(self.tree.selection())['values'][1]
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No Item Selected to modify.'
            return
        self.openContactModifyWindow(name, number)

    """Validates that the namefields aren't empty"""
    def newContactValidate(self):
        return len(self.namefield.get()) != 0 and len(self.email_field.get()) != 0 and len(self.numfield.get()) != 0

    def viewContacts(self):
        items = self.tree.get_children()  #Get_children is a method use to return item ids
        for item in items:
            self.tree.delete(item)
        query = 'Select * FROM contacts_list ORDER BY name desc'
        contact_entries = self.execute_db(query)
        for row in contact_entries:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3]))

    def deleteContacts(self):
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        qry = 'DELETE FROM contacts_list WHERE name = ?'
        self.execute_db(qry, (name,))
        self.message['text'] = 'Contact for "' + name + '" deleted.'
        self.viewContacts()


    def openNameModifyWindow(self, name, number):
        self.transient = Toplevel()  #will act for Poping up the window
        self.transient.title('Update Contact')
        Label(self.transient, text='Number:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=number), state='readonly').grid(row=0, column=2)
        Label(self.transient, text='Old Contact Name').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=1, column=2)

        Label(self.transient, text='New Contact Name').grid(row=2, column=1)
        newName_entryWidget = Entry(self.transient)
        newName_entryWidget.grid(row=2, column=2)

        Button(self.transient, text="Update Contact", command=lambda: self.updateName(
            newName_entryWidget.get(), name, number)).grid(row=3, column=2, sticky=E)

        self.transient.mainloop()

    def openContactModifyWindow(self, name, old_number):
        self.transient = Toplevel()  #will act for Poping up the window
        self.transient.title('Update Contact')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)
        Label(self.transient, text='Old Contact Number').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_number), state='readonly').grid(row=1, column=2)

        Label(self.transient, text='New Contact Number').grid(row=2, column=1)
        newPhoneNumber_entryWidget = Entry(self.transient)
        newPhoneNumber_entryWidget.grid(row=2, column=2)

        Button(self.transient, text="Update Contact", command=lambda: self.updateContacts(
            newPhoneNumber_entryWidget.get(), old_number, name)).grid(row=3, column=2, sticky=E)

        self.transient.mainloop()

    def openEmailModifyWindow(self, name, old_Email):
        self.transient = Toplevel()  # will act for Poping up the window
        self.transient.title('Update Contact Email')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)
        Label(self.transient, text='Old Contact Email').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_Email), state='readonly').grid(row=1, column=2)

        Label(self.transient, text='New Contact Email').grid(row=2, column=1)
        newEmail_entryWidget = Entry(self.transient)
        newEmail_entryWidget.grid(row=2, column=2)

        Button(self.transient, text="Update Contact", command=lambda: self.updateEmail(
            newEmail_entryWidget.get(), old_Email, name)).grid(row=3, column=2, sticky=E)

        self.transient.mainloop()

    def updateName(self, newName, oldName, number):
        qry = 'UPDATE contacts_list SET name=? WHERE name=? AND number=? '
        parameters = (newName, oldName, number)
        self.execute_db(qry, parameters)
        self.transient.destroy()
        self.message['text'] = 'Name has been updated.'
        self.viewContacts()

    def updateEmail(self, newEmail, oldEmail, name):
        qry = 'UPDATE contacts_list SET email=? WHERE email=? AND name=? '
        parameters = (newEmail, oldEmail, name)
        self.execute_db(qry, parameters)
        self.transient.destroy()
        self.message['text'] = 'Email Id of "' + name + '" has been modified.'
        self.viewContacts()

    def updateContacts(self, newPhone, oldPhone, name):
        qry = 'UPDATE contacts_list SET number=? WHERE number=? AND name=? '
        parameters = (newPhone, oldPhone, name)
        self.execute_db(qry, parameters)
        self.transient.destroy()
        self.message['text'] = 'Phone Number of "' + name + '" has been modified.'
        self.viewContacts()



# Beginning of GUI
if __name__ == "__main__":
    """Application Designed"""
    root = Tk()
    root.title("My Contact List")
    root.resizable(width=False, height=False)
    """Saying the compiler to run every code that is in class"""
    application = Contacts(root)
    root.mainloop()
