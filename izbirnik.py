import os
import re
import tkinter
import shutil


class UI(tkinter.Frame):
    status_text = None

    def __init__(self, backend=None):
        self.master = tkinter.Tk()
        self.master.geometry('750x500+100+100')
        self.master.title('Izbirnik')
        self.backend = backend
        super().__init__(self.master, bg='white', borderwidth=10)
        self.pack(expand=True, fill=tkinter.BOTH)
        self.create_widgets()

        self.matched_files = []
        self.log('Vnesite ime datoteke, nato pritisnite ENTER.')

    def create_widgets(self):
        self.title = tkinter.Label(self, text='Izbirnik', background='white', borderwidth=0, font=("Courier", 44))
        self.title.pack(fill=tkinter.X)

        self.pattern = tkinter.Entry(self, borderwidth=2, insertborderwidth=10, justify=tkinter.CENTER, font=("Courier", 20))
        self.pattern.pack(fill=tkinter.X, pady=20)
        self.pattern.bind('<Return>', self.on_pattern_input)
        self.pattern.focus()

        self.files_found_container = tkinter.Frame(self, width=200, height=200, background='white')
        self.files_found_container.pack(fill=tkinter.X)

        self.status_text = tkinter.StringVar()
        self.status = tkinter.Label(self, textvariable=self.status_text, background='white', borderwidth=0, font=("Courier", 20))
        self.status.pack(side=tkinter.BOTTOM)

    def on_pattern_input(self, *args, **kwargs):
        pattern = self.pattern.get()
        self.matched_files = self.backend.match_pattern(pattern)
        self.show_buttons()

    def on_button_click(self, btn, file_found):
        self.backend.copy_file(file_found)
        btn.config(state=tkinter.DISABLED, )
        self.log('Skopirano.')

    def show_buttons(self):
        self.clear_buttons()

        if self.matched_files:
            tkinter.Label(self.files_found_container, text='Zadetki:', font=("Courier", 20), background='white', pady=10).pack()
            self.log('Kliknite puljubni zadetek da ga skopirate.')
        else:
            self.log('Ni zadetkov.')

        for f in self.matched_files:
            btn = tkinter.Button(
                self.files_found_container,
                text=f.path,
                font=("Courier", 10),
                pady=10,
                background='white',
            )
            btn.config(command=lambda: self.on_button_click(btn, f))
            btn.pack(fill=tkinter.X)

    def clear_buttons(self):
        for b in self.files_found_container.winfo_children():
            b.pack_forget()

    def log(self, txt):
        self.status.config(foreground='#cccccc')
        self.status_text.set(txt)


class Program:
    def __init__(self):
        self.ui = None
        self.input_dir = r'C:\Users\Miha\PycharmProjects\izbirnik\example\input'
        self.output_dir = r'C:\Users\Miha\PycharmProjects\izbirnik\example\output'

    def start_gui(self):
        self.ui = UI(backend=self)
        self.ui.mainloop()

    def match_pattern(self, pattern):
        r = re.compile('^{}(\..+)?$'.format(pattern))
        res = []
        for subdir, dirs, files in os.walk(self.input_dir):
            for filename in files:
                if r.match(filename):
                    res.append(MatchedFile(os.path.join(subdir, filename)))
        return res

    def copy_file(self, matched_file):
        print('Copying {} into {}'.format(matched_file.path, self.output_dir))
        shutil.copy(matched_file.path, self.output_dir)


class MatchedFile:
    def __init__(self, path):
        self.path = path


p = Program()
p.start_gui()
