from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from Controllers.years_controller import YearsController
from View.Products.products import Products
from tkinter import messagebox


class MainMenu(Tk):
    add_year_entry: Entry
    remove_year_combo: ttk.Combobox

    def __init__(self, connection):
        super().__init__()

        self.connection = connection
        self.title('Pwark')
        self.geometry('800x480')
        self.resizable(width=False, height=False)
        self.config(bg='black')
        self.picon = ImageTk.PhotoImage(Image.open("Images/123.png"))
        self.iconphoto(False, self.picon)

        self.menubar = Menu(self)
        self.config(menu=self.menubar)

        self.main_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.main_menu)

        self.year_sub_menu = Menu(self.main_menu, tearoff=0)
        self.year_sub_menu.add_command(label='Add', command=self.add_year)
        self.year_sub_menu.add_command(label='Remove', command=self.remove_year)
        self.main_menu.add_cascade(label="Year", menu=self.year_sub_menu)

        self.title_img = ImageTk.PhotoImage(Image.open("Images/pwarklogo2.png"))
        self.title = Label(image=self.title_img)
        self.title.config(bg='black')
        self.title.place(relx=0.28, rely=0.075)

        self.right_logo_img = ImageTk.PhotoImage(Image.open("Images/1.jpg"))
        self.right_logo = Label(image=self.right_logo_img)
        self.right_logo.place(relx=0.43, rely=0.88)

        self.left_logo_img = ImageTk.PhotoImage(Image.open("Images/2.jpg"))
        self.left_logo = Label(image=self.left_logo_img)
        self.left_logo.place(relx=0.52, rely=0.88)

        self.divider_img = ImageTk.PhotoImage(Image.open("Images/line.png"))
        self.divider = Label(image=self.divider_img)
        self.divider.config(bg='black')
        self.divider.place(relx=0.25, rely=0.71)

        self.year_label = Label(self, text='Choose the year', bg='black', fg='white')
        self.year_label.place(relx=0.715, rely=0.4)

        self.year_data = YearsController.fetch_all_years(self.connection)
        self.years = [year_row['year'] for year_row in self.year_data]

        self.year_list = ttk.Combobox(self, textvariable=StringVar(), values=self.years, state="readonly", width=10)
        self.year_list.current(0)
        self.year_list.place(relx=0.72, rely=0.46)

        self.label_month = Label(self, text='Choose the month', bg='black', fg='white')
        self.label_month.place(relx=0.44, rely=0.4)

        self.months = [
            {'id': 1, 'value': 'فروردين'},
            {'id': 2, 'value': 'ارديبهشت'},
            {'id': 3, 'value': 'خرداد'},
            {'id': 4, 'value': 'تير'},
            {'id': 5, 'value': 'مرداد'},
            {'id': 6, 'value': 'شهريور'},
            {'id': 7, 'value': 'مهر'},
            {'id': 8, 'value': 'آبان'},
            {'id': 9, 'value': 'آذر'},
            {'id': 10, 'value': 'دي'},
            {'id': 11, 'value': 'بهمن'},
            {'id': 12, 'value': 'اسفند'},
        ]
        self.month_list = ttk.Combobox(self, textvariable=StringVar(), values=[month['value'] for month in self.months],
                                       state="readonly", width=15)
        self.month_list.current(0)
        self.month_list.place(relx=0.44, rely=0.46)

        self.day_label = Label(self, text='Chose the day', bg='black', fg='white')
        self.day_label.place(relx=0.15, rely=0.4)

        self.day_list = ttk.Combobox(self, textvariable=StringVar(),
                                     values=[f"{i}" for i in range(1, 32)], state="readonly", width=10)
        self.day_list.current(0)
        self.day_list.place(relx=0.15, rely=0.46)

        ttk.Style().configure('TButton', background='blue', foreground='black')
        ttk.Style().map('TButton', background=[('active', 'darkorange')], foreground=[('active', 'darkorange')])
        self.next_button = ttk.Button(self, text='Next Page', command=self.go_to_second_page)
        self.next_button.place(relx=0.46, rely=0.61)

    def go_to_second_page(self):
        month = (month['id'] for month in self.months if month['value'] == self.month_list.get()).__next__()
        data = {"year": self.year_list.get(), 'month': month, 'day': self.day_list.get()}
        self.destroy()
        products = Products(self.connection, data)
        products.mainloop()

    def add_year(self):
        add_year_window = Tk()
        add_year_window.geometry("400x200")
        add_year_window.configure(bg='white')
        add_year_window.resizable(False, False)
        add_year_window.title('Add years')

        add_year_entry_frame = Frame(add_year_window, bg='white')
        add_year_entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='')

        add_year_button_frame = Frame(add_year_window, bg='white')
        add_year_button_frame.grid(row=2, column=0, pady=10, padx=10, sticky='')

        year_label = Label(add_year_entry_frame, text='Enter New Year', bg='white', fg='black')
        year_label.grid(row=0, column=0, sticky='')
        self.add_year_entry = Entry(add_year_entry_frame, width=30)
        self.add_year_entry.grid(row=1, column=0, sticky='')

        add_year_button = ttk.Button(add_year_button_frame, text='Add year',
                                     command=lambda: self.add_year_function(add_year_window))
        add_year_button.grid(row=0, column=0, sticky='')

        add_year_window.grid_columnconfigure(0, weight=1)

    def add_year_function(self, window):
        if int(self.add_year_entry.get()) not in [item["year"] for item in
                                                  YearsController.fetch_all_years(self.connection)]:
            YearsController.add_year(self.connection, self.add_year_entry.get())
            self.year_data = YearsController.fetch_all_years(self.connection)
            self.years = [year_row['year'] for year_row in self.year_data]
            self.year_list['values'] = self.years
        else:
            messagebox.showerror(title="Login Error", message="Duplicate year")
        window.destroy()

    def remove_year(self):
        remove_year_window = Tk()
        remove_year_window.geometry("400x200")
        remove_year_window.configure(bg='white')
        remove_year_window.resizable(False, False)
        remove_year_window.title('Add years')

        remove_year_entry_frame = Frame(remove_year_window, bg='white')
        remove_year_entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='')

        remove_year_button_frame = Frame(remove_year_window, bg='white')
        remove_year_button_frame.grid(row=2, column=0, pady=10, padx=10, sticky='')

        remove_year_label = Label(remove_year_entry_frame, text='Enter Type', bg='white', fg='black')
        remove_year_label.grid(row=2, column=0, sticky='')
        self.remove_year_combo = ttk.Combobox(remove_year_entry_frame, textvariable=StringVar(),
                                              values=self.years,
                                              state="readonly", width=30)
        self.remove_year_combo.grid(row=3, column=0, sticky='')

        remove_year_button = ttk.Button(remove_year_button_frame, text='Remove year',
                                        command=lambda: self.remove_year_function(remove_year_window))
        remove_year_button.grid(row=0, column=0, sticky='')

        remove_year_window.grid_columnconfigure(0, weight=1)

    def remove_year_function(self, window):
        year_id = (year['id'] for year in self.year_data if
                   str(year['year']) == self.remove_year_combo.get()).__next__()
        YearsController.remove_year(self.connection, year_id)
        self.year_data = YearsController.fetch_all_years(self.connection)
        self.years = [year_row['year'] for year_row in self.year_data]
        self.year_list['values'] = self.years
        window.destroy()
