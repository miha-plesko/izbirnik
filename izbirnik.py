import tkinter


class UI(tkinter.Frame):
    status_text = None

    def __init__(self):
        self.master = tkinter.Tk()
        self.master.geometry('750x500+100+100')
        self.master.title('Izbirnik')
        super().__init__(self.master, bg='white', borderwidth=10)
        self.pack(expand=True, fill=tkinter.BOTH)
        self.create_widgets()

        self.files_found = []

    def create_widgets(self):
        self.title = tkinter.Label(self, text='Izbirnik', background='white', borderwidth=0, font=("Courier", 44))
        self.title.pack(fill=tkinter.X)

        self.pattern = tkinter.Entry(self, borderwidth=2, insertborderwidth=10, justify=tkinter.CENTER, font=("Courier", 20))
        self.pattern.pack(fill=tkinter.X, pady=20)
        self.pattern.bind('<Return>', self.on_pattern_input)
        self.pattern.focus()

        self.files_found_container =

        # self.hi_there = tkinter.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack()

        # self.quit = tkinter.Button(self, text="Zapri", fg="red", command=self.master.destroy)
        # self.quit.pack()

        self.status_text = tkinter.StringVar()
        self.status = tkinter.Label(self, textvariable=self.status_text, background='white', borderwidth=0, font=("Courier", 20))
        self.status.pack(side=tkinter.BOTTOM)

    def on_pattern_input(self, *args, **kwargs):
        self.say_hi()

    def add_buttons(self):
        file_found = tkinter.Button(self, )
        self.files_found.append(file_found)


    def say_hi(self):
        print("hi there, everyone!")
        self.status_text.set('BUREK')


class Program:
    def __init__(self):
        self.ui = None

    def start_gui(self):
        self.ui = UI()
        self.ui.mainloop()


p = Program()
p.start_gui()
