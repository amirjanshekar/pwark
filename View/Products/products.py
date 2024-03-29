from tkinter import *
from tkinter import ttk, Entry
from tkinter import messagebox

from PIL import ImageTk, Image
from Controllers.products_controller import ProductsController
from Controllers.wastage_controller import WastageController
from Controllers.final_controller import FinalController
from Controllers.rework_controller import ReworkController


class Products(Tk):
    add_product_entry: Entry
    add_un_comforting_entry: Entry
    add_info_entry: Entry
    add_product_type: ttk.Combobox
    report_year_list: ttk.Combobox
    from_month_list: ttk.Combobox
    to_month_list: ttk.Combobox
    ppm_month_list: ttk.Combobox
    remove_product_combo: ttk.Combobox
    edit_data_type_combo: ttk.Combobox
    edit_product_combo: ttk.Combobox
    edit_data_list: Listbox
    edit_data_produce_entry: Entry
    edit_data_data_amount_entry: Entry

    def __init__(self, connection, data):
        super().__init__()

        self.show_work_data = []
        self.edit_show_work_data = []
        self.current_wastage = []
        self.current_reworks = []
        self.connection = connection
        self.data = data
        self.fetched_final_data = {}

        self.add_work_entries = []

        self.products = ProductsController.fetch_all_products(connection)
        self.edit_products = []

        self.geometry('1350x768')
        self.resizable(width=False, height=False)
        self.config(bg='black')

        self.icon = ImageTk.PhotoImage(Image.open("Images/123.png"))
        self.iconphoto(False, self.icon)

        self.img4 = ImageTk.PhotoImage(Image.open("Images/pwarklogo1.png"))
        self.top_image = Label(image=self.img4)
        self.top_image.config(bg='gray5')
        self.top_image.place(relx=0.001, rely=0.001)

        self.type_label = Label(self, text='Data type', fg='saddle brown', bg='gray5', font=("Arial", 12, 'bold'))
        self.type_label.place(relx=0.765, rely=0.23)

        self.type_list = ttk.Combobox(self, textvariable=StringVar(), values=['wastage', 'rework'],
                                      state="readonly", width=35)
        self.type_list.current(0)
        self.type_list.place(relx=0.71, rely=0.28)
        self.type_list.bind('<<ComboboxSelected>>', self.change_data_of_works)

        self.menubar = Menu(self)
        self.config(menu=self.menubar)

        self.main_menu = Menu(self.menubar, tearoff=0)
        self.report_menu = Menu(self.menubar, tearoff=0)
        self.edit_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.main_menu)
        self.menubar.add_cascade(label="Report", menu=self.report_menu)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

        self.edit_menu.add_command(label='ویرایش ', command=self.edit_data)

        self.product_sub_menu = Menu(self.main_menu, tearoff=0)
        self.product_sub_menu.add_command(label='Add', command=self.add_product)
        self.product_sub_menu.add_command(label='Remove', command=self.remove_product)
        self.main_menu.add_cascade(label="Product", menu=self.product_sub_menu)

        self.rework_sub_menu = Menu(self.report_menu, tearoff=0)
        self.rework_sub_menu.add_command(label='گزارش ',
                                         command=lambda: FinalController.export_data_by_type(self.connection, 'rework'))
        self.rework_sub_menu.add_command(label='لیست RPN و PPM',
                                         command=lambda: self.get_rpn_ppm_view('rework'))
        self.report_menu.add_cascade(label='دوباره کاری', menu=self.rework_sub_menu)

        self.un_comforting_sub_menu = Menu(self.report_menu, tearoff=0)
        self.un_comforting_sub_menu.add_command(label='گزارش ',
                                                command=lambda: FinalController.export_data_by_type(self.connection,
                                                                                                    'wastage'))
        self.un_comforting_sub_menu.add_command(label='لیست RPN و PPM',
                                                command=lambda: self.get_rpn_ppm_view('wastage'))
        self.report_menu.add_cascade(label='ضایعات', menu=self.un_comforting_sub_menu)

        self.product_label = Label(self, text='Chose product', fg='saddle brown', bg='gray5',
                                   font=("Arial", 12, 'bold'))
        self.product_label.place(relx=0.75, rely=0.33)

        self.product_list = ttk.Combobox(self, values=self.products, width=35)
        self.product_list.current(0)
        self.product_list.bind('<<ComboboxSelected>>', self.change_data_of_works)
        self.product_list.place(relx=0.71, rely=0.38)

        self.produce_label = Label(self, text='Produce', fg='saddle brown', bg='gray5',
                                   font=("Arial", 12, 'bold'))
        self.produce_label.place(relx=0.78, rely=0.43)

        self.produce_entry = Entry(self, width=39)
        self.produce_entry.place(relx=0.71, rely=0.48)

        self.label_ppm_rework = Label(self, text='Chose data', fg='saddle brown', bg='gray5',
                                      font=("Arial", 12, 'bold'))
        self.label_ppm_rework.place(relx=0.765, rely=0.57)

        self.label_ppm_rework_list = Listbox(self, width=50)
        self.label_ppm_rework_list.place(relx=0.69, rely=0.63)

        product_id = ProductsController.fetch_product_by_name(self.connection, self.product_list.get())[0]
        if self.type_list.get() == 'wastage':
            self.show_work_data = WastageController.fetch_all_wastage(self.connection, product_id)
        else:
            self.show_work_data = ReworkController.fetch_all_reworks(self.connection, product_id)
        for index in range(len(self.show_work_data)):
            self.label_ppm_rework_list.insert(index, self.show_work_data[index])

        self.number_spin = ttk.Spinbox(self, from_=0, to=10000, width=37, textvariable=StringVar(), wrap=True)
        self.number_spin.place(relx=0.20, rely=0.64)

        self.label_number = Label(self, text='Enter number', fg='saddle brown', bg='gray5',
                                  font=("Arial", 12,
                                        'bold'))
        self.label_number.place(relx=0.40, rely=0.635)

        self.label_explanation = Label(self, bg='grey3', width=109, height=16)
        self.label_explanation.place(relx=0.05, rely=0.26)

        ttk.Style().configure('TButton', background='blue', foreground='black')
        ttk.Style().map('TButton', background=[('active', 'darkorange')], foreground=[('active', 'darkorange')])
        self.save_button = ttk.Button(self, text='Add data', width=20, command=self.send_data)
        self.save_button.place(relx=0.40, rely=0.8)

    def add_product(self):
        add_product_window = Tk()
        add_product_window.geometry("600x400")
        add_product_window.configure(bg='white')
        add_product_window.resizable(False, False)
        add_product_window.title('Edit Products')

        add_product_entry_frame = Frame(add_product_window, bg='white')
        add_product_entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='')

        add_product_table_frame = Frame(add_product_window, bg='white')
        add_product_table_frame.grid(row=1, column=0, padx=10, pady=10, sticky='')

        add_product_button_frame = Frame(add_product_window, bg='white')
        add_product_button_frame.grid(row=2, column=0, pady=10, padx=10, sticky='')

        product_label = Label(add_product_entry_frame, text='Enter New Product', bg='white', fg='black')
        product_label.grid(row=0, column=0, sticky='')
        self.add_product_entry = Entry(add_product_entry_frame, width=30)
        self.add_product_entry.grid(row=1, column=0, sticky='')

        type_label = Label(add_product_entry_frame, text='Enter Type', bg='white', fg='black')
        type_label.grid(row=2, column=0, sticky='')
        self.add_product_type = ttk.Combobox(add_product_entry_frame, textvariable=StringVar(),
                                             values=['wastage', 'rework'],
                                             state="readonly", width=30)
        self.add_product_type.grid(row=3, column=0, sticky='')

        detection_label = Label(add_product_table_frame, text='Detection', bg='white', fg='black')
        detection_label.grid(row=0, column=0)

        severity_label = Label(add_product_table_frame, text='Severity', bg='white', fg='black')
        severity_label.grid(row=0, column=1)

        name_label = Label(add_product_table_frame, text='Name', bg='white', fg='black', width=20)
        name_label.grid(row=0, column=2)

        for col in range(3):
            if col == 2:
                self.add_work_entries.append(Entry(add_product_table_frame, width=20))
            else:
                self.add_work_entries.append(Entry(add_product_table_frame, width=10))
            self.add_work_entries[col].grid(row=1, column=col, padx=10)

        add_product_button = ttk.Button(add_product_button_frame, text='Add',
                                        command=lambda: self.insert_product_to_list(add_product_table_frame))
        add_product_button.grid(row=0, column=0, sticky='')

        close_button = ttk.Button(add_product_button_frame, text='Close',
                                  command=lambda: self.close_add_product_window(add_product_window))
        close_button.grid(row=0, column=1, sticky='')
        add_product_window.grid_columnconfigure(0, weight=1)

    def remove_product(self):
        remove_product_window = Tk()
        remove_product_window.geometry("400x200")
        remove_product_window.configure(bg='white')
        remove_product_window.resizable(False, False)
        remove_product_window.title('Edit Products')

        remove_product_entry_frame = Frame(remove_product_window, bg='white')
        remove_product_entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='')

        remove_product_button_frame = Frame(remove_product_window, bg='white')
        remove_product_button_frame.grid(row=2, column=0, pady=10, padx=10, sticky='')

        type_label = Label(remove_product_entry_frame, text='Enter Type', bg='white', fg='black')
        type_label.grid(row=2, column=0, sticky='')
        self.remove_product_combo = ttk.Combobox(remove_product_entry_frame, textvariable=StringVar(),
                                                 values=self.products,
                                                 state="readonly", width=30)
        self.remove_product_combo.grid(row=3, column=0, sticky='')

        remove_product_button = ttk.Button(remove_product_button_frame, text='Remove',
                                           command=lambda: self.remove_product_from_list(remove_product_window))
        remove_product_button.grid(row=0, column=0, sticky='')

        remove_product_window.grid_columnconfigure(0, weight=1)

    def edit_data(self):
        edit_data_window = Tk()
        edit_data_window.geometry("400x400")
        edit_data_window.configure(bg='white')
        edit_data_window.resizable(False, False)
        edit_data_window.title('Edit Products')

        edit_data_entry_frame = Frame(edit_data_window, bg='white')
        edit_data_entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='')

        edit_data_button_frame = Frame(edit_data_window, bg='white')
        edit_data_button_frame.grid(row=2, column=0, pady=10, padx=10, sticky='')

        data_type_label = Label(edit_data_entry_frame, text='Data Type', bg='white', fg='black')
        data_type_label.grid(row=2, column=0, sticky='')
        self.edit_data_type_combo = ttk.Combobox(edit_data_entry_frame, textvariable=StringVar(),
                                                 values=['wastage', 'rework'],
                                                 state="readonly", width=30)
        self.edit_data_type_combo.grid(row=3, column=0, sticky='')
        self.edit_data_type_combo.current(0)
        self.edit_data_type_combo.bind('<<ComboboxSelected>>', self.change_edit_data)

        self.edit_products = FinalController.fetch_data_by_type(self.connection, self.data['year'], self.data['month'],
                                                                self.data['day'], self.edit_data_type_combo.get())

        product_label = Label(edit_data_entry_frame, text='Data', bg='white', fg='black')
        product_label.grid(row=4, column=0, sticky='')
        self.fetched_final_data = FinalController.fetch_data_by_type(self.connection,
                                                                     self.data['year'],
                                                                     self.data['month'],
                                                                     self.data['day'],
                                                                     self.edit_data_type_combo.get())
        self.edit_product_combo = ttk.Combobox(edit_data_entry_frame, textvariable=StringVar(),
                                               values=self.fetched_final_data['item'],
                                               state="readonly", width=30)
        self.edit_product_combo.grid(row=5, column=0, sticky='')
        self.edit_product_combo.current(0)
        self.edit_product_combo.bind('<<ComboboxSelected>>', self.set_edit_data)

        produce_label = Label(edit_data_entry_frame, text='Produce', bg='white', fg='black')
        produce_label.grid(row=6, column=0, sticky='')
        self.edit_data_produce_entry = Entry(edit_data_entry_frame, width=50)
        self.edit_data_produce_entry.grid(row=7, column=0, sticky='')
        self.edit_data_produce_entry.insert(0, str(self.fetched_final_data['produce'][0]))

        data_amount_label = Label(edit_data_entry_frame, text='Data amount', bg='white', fg='black')
        data_amount_label.grid(row=8, column=0, sticky='')
        self.edit_data_data_amount_entry = Entry(edit_data_entry_frame, width=50)
        self.edit_data_data_amount_entry.grid(row=9, column=0, sticky='')
        self.edit_data_data_amount_entry.insert(0, str(self.fetched_final_data['amount'][0]))

        edit_data_button = ttk.Button(edit_data_button_frame, text='Edit',
                                      command=lambda: self.edit_data_from_list(edit_data_window))
        edit_data_button.grid(row=0, column=0, sticky='')

        edit_data_window.grid_columnconfigure(0, weight=1)

    def change_edit_data(self, args):
        self.fetched_final_data = FinalController.fetch_data_by_type(self.connection, self.data['year'],
                                                                     self.data['month'],
                                                                     self.data['day'],
                                                                     self.edit_data_type_combo.get())
        self.edit_product_combo['values'] = self.fetched_final_data['item']

    def set_edit_data(self, args):
        self.edit_data_produce_entry.delete(0, END)
        self.edit_data_produce_entry.insert(0, str(self.fetched_final_data['produce'][
                                                       self.fetched_final_data['item'].index(
                                                           self.edit_product_combo.get())]))
        self.edit_data_data_amount_entry.delete(0, END)
        self.edit_data_data_amount_entry.insert(0, str(self.fetched_final_data['amount'][
                                                           self.fetched_final_data['item'].index(
                                                               self.edit_product_combo.get())]))

    def send_data(self):
        self.data['type'] = self.type_list.get()
        self.data['data'] = self.number_spin.get()
        product_id = ProductsController.fetch_product_by_name(self.connection, self.product_list.get())[0]
        self.data['product'] = product_id

        for i in self.label_ppm_rework_list.curselection():
            if self.type_list.get() == 'wastage':
                wastage_id = WastageController.fetch_wastage_by_name(self.connection, product_id,
                                                                     self.label_ppm_rework_list.get(i))[0]
                self.data['work'] = self.label_ppm_rework_list.get(i)
                self.data['workId'] = wastage_id
            else:
                rework_id = ReworkController.fetch_rework_by_name(self.connection, product_id,
                                                                  self.label_ppm_rework_list.get(i))[0]
                self.data['work'] = self.label_ppm_rework_list.get(i)
                self.data['workId'] = rework_id
        self.data['produce'] = self.produce_entry.get()
        FinalController.add_final(self.connection, self.data)
        messagebox.showinfo(title="Successfully!...", message='Data has been added!...')

    def close_add_product_window(self, window):
        self.current_wastage = []
        self.current_reworks = []
        window.destroy()

    def change_data_of_works(self, args):
        product_id = ProductsController.fetch_product_by_name(self.connection, self.product_list.get())[0]
        if self.type_list.get() == 'wastage':
            self.show_work_data = WastageController.fetch_all_wastage(self.connection, product_id)
        else:
            self.show_work_data = ReworkController.fetch_all_reworks(self.connection, product_id)
        for index in range(len(self.show_work_data)):
            self.label_ppm_rework_list.insert(index, self.show_work_data[index])
        data = FinalController.fetch_data_by_type(self.connection, self.data['year'], self.data['month'],
                                                  self.data['day'], self.type_list.get())

    def remove_product_from_list(self, window):
        product_id = ProductsController.fetch_product_by_name(self.connection, self.remove_product_combo.get())[0]
        ProductsController.remove_product(self.connection, product_id)
        self.products = ProductsController.fetch_all_products(self.connection)
        self.remove_product_combo['values'] = self.products
        self.product_list['values'] = self.products
        window.destroy()

    def edit_data_from_list(self, window):
        final_id = self.fetched_final_data['id'][self.fetched_final_data['item'].index(self.edit_product_combo.get())]
        FinalController.update_data(self.connection, final_id, self.edit_data_produce_entry.get(),
                                    self.edit_data_data_amount_entry.get())
        window.destroy()

    def insert_product_to_list(self, frame):
        if (self.add_product_entry.get()) not in self.products:
            ProductsController.add_product(self.connection, self.add_product_entry.get())
            self.products = ProductsController.fetch_all_products(self.connection)
            self.product_list['values'] = self.products
        product_id = ProductsController.fetch_product_by_name(self.connection, self.add_product_entry.get())[0]
        if self.add_product_type.get() == 'wastage':
            if self.add_work_entries[2].get() not in self.current_wastage:
                self.current_wastage.append({'wastage': self.add_work_entries[2].get(),
                                             'severity': self.add_work_entries[1].get(),
                                             'detection': self.add_work_entries[0].get()})
                WastageController.add_wastage(self.connection, wastage=self.add_work_entries[2].get(),
                                              product_id=product_id, severity=self.add_work_entries[1].get(),
                                              detection=self.add_work_entries[0].get())
                for index in range(len(self.current_wastage)):
                    Label(frame, text=self.current_wastage[index]['detection'], bg='white',
                          fg='black').grid(
                        row=index + 2, column=0)

                    Label(frame, text=self.current_wastage[index]['severity'], bg='white',
                          fg='black').grid(
                        row=index + 2, column=1)
                    Label(frame, text=self.current_wastage[index]['wastage'], bg='white', fg='black',
                          width=20).grid(row=index + 2, column=2)
                    Label(frame, text='wastage', bg='white', fg='black',
                          width=20).grid(row=index + 2, column=3)
        else:
            if self.add_work_entries[2].get() not in self.current_reworks:
                self.current_reworks.append({'rework': self.add_work_entries[2].get(),
                                             'severity': self.add_work_entries[1].get(),
                                             'detection': self.add_work_entries[0].get()})
                ReworkController.add_rework(self.connection, rework=self.add_work_entries[2].get(),
                                            product_id=product_id, severity=self.add_work_entries[1].get(),
                                            detection=self.add_work_entries[0].get())
                for index in range(len(self.current_reworks)):
                    Label(frame, text=self.current_reworks[index]['detection'], bg='white',
                          fg='black').grid(
                        row=index + 2, column=0)

                    Label(frame, text=self.current_reworks[index]['severity'], bg='white',
                          fg='black').grid(
                        row=index + 2, column=1)

                    Label(frame, text=self.current_reworks[index]['rework'], bg='white', fg='black',
                          width=20).grid(row=index + 2, column=2)
                    Label(frame, text='rework', bg='white', fg='black',
                          width=20).grid(row=index + 2, column=3)

    def get_rpn_ppm_view(self, work_type):
        report_rpn_ppm_window = Tk()
        report_rpn_ppm_window.geometry("600x400")
        report_rpn_ppm_window.configure(bg='white')
        report_rpn_ppm_window.resizable(False, False)
        report_rpn_ppm_window.title('Report')

        report_rpn_ppm_frame = Frame(report_rpn_ppm_window, bg='white')
        report_rpn_ppm_frame.grid(row=0, column=0, padx=10, pady=10, sticky='')

        report_rpn_ppm_button_frame = Frame(report_rpn_ppm_window, bg='white')
        report_rpn_ppm_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky='')

        Label(report_rpn_ppm_frame, text='Month', bg='white', fg='black').grid(row=0, column=0)
        months = [
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
        self.ppm_month_list = ttk.Combobox(report_rpn_ppm_frame, textvariable=StringVar(),
                                           values=[month['value'] for month in months],
                                           state="readonly", width=15)
        self.ppm_month_list.current(0)
        self.ppm_month_list.grid(row=0, column=1)

        get_rpn_report_button = ttk.Button(report_rpn_ppm_button_frame, text='Save Report',
                                           command=lambda: self.get_ppm_report(work_type, months,
                                                                               report_rpn_ppm_window))
        get_rpn_report_button.grid(row=0, column=0, sticky='')
        report_rpn_ppm_window.grid_columnconfigure(0, weight=1)

    def get_ppm_report(self, work_type, months, modal):
        month = (month['id'] for month in months if month['value'] == self.ppm_month_list.get()).__next__()
        FinalController.export_formatted_data(self.connection, work_type, month)
        messagebox.showinfo(title="Successfully!...", message='Report saved!...')
        modal.destroy()
