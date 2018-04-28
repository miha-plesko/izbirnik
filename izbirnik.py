import yaml
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
        self.check_backend_error()

    def create_widgets(self):
        self.title = tkinter.Label(self, text='Izbirnik', background='white', borderwidth=0, font=("Courier", 44))
        self.title.pack(fill=tkinter.X)

        self.pattern = tkinter.Entry(self, borderwidth=2, insertborderwidth=10, justify=tkinter.CENTER, font=("Courier", 20))
        self.pattern.pack(fill=tkinter.X, pady=20)
        self.pattern.bind('<Return>', self.on_pattern_input)
        self.pattern.bind('<F1>', self.show_config)
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
        self.check_backend_error()

    def on_button_click(self, btn, file_found):
        self.backend.copy_file(file_found)
        btn.config(state=tkinter.DISABLED, )
        self.log('Skopirano.')
        self.check_backend_error()

    def check_backend_error(self):
        if self.backend.error:
            self.log_error(self.backend.error)

        if self.backend.error_trace:
            self.clear_buttons()
            tkinter.Label(self.files_found_container, text=self.backend.error_trace).pack()

    def show_buttons(self):
        self.clear_buttons()

        if self.matched_files:
            tkinter.Label(self.files_found_container, text='Zadetki:', font=("Courier", 20), background='white', pady=10).pack()
            self.log('Kliknite puljubni zadetek da ga skopirate.')
        else:
            self.log('Ni zadetkov. Pritisnite F1 za več info.')

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

    def show_config(self, *args, **kwargs):
        self.clear_buttons()
        tkinter.Label(self.files_found_container, text='Vhodna mapa:', font=("Courier", 20), background='white', pady=10).pack()
        tkinter.Label(self.files_found_container, text=self.backend.input_dir, font=("Courier", 12), background='white', pady=10).pack()
        tkinter.Label(self.files_found_container, text='Izhodna mapa:', font=("Courier", 20), background='white', pady=10).pack()
        tkinter.Label(self.files_found_container, text=self.backend.output_dir, font=("Courier", 12), background='white', pady=10).pack()

    def clear_buttons(self):
        for b in self.files_found_container.winfo_children():
            b.pack_forget()

    def log(self, txt):
        self.status.config(foreground='#cccccc')
        self.status_text.set(txt)

    def log_error(self, txt):
        self.status.config(foreground='red')
        self.status_text.set(txt)


class Program:
    def __init__(self):
        self.ui = None
        self.error = None
        self.error_trace = None
        self.input_dir = None
        self.output_dir = None
        self.load_configuration()

    def start_gui(self):
        self.ui = UI(backend=self)
        self.ui.mainloop()

    def match_pattern(self, pattern):
        r = None
        try:
            r = re.compile('^{}(\..+)?$'.format(pattern))
        except Exception as e:
            self.error = 'Neveljavno ime datoteke.'
            self.error_trace = e
            return []

        res = []
        for subdir, dirs, files in os.walk(self.input_dir):
            for filename in files:
                if r.match(filename):
                    res.append(MatchedFile(os.path.join(subdir, filename)))
        return res

    def copy_file(self, matched_file):
        print('Copying {} into {}'.format(matched_file.path, self.output_dir))
        try:
            shutil.copy(matched_file.path, self.output_dir)
        except Exception as e:
            self.error = 'Napaka pri kopiranju.'
            self.error_trace = e

    def load_configuration(self):
        try:
            with open('./izbirnik.yaml') as f:
                conf = yaml.load(f)
                self.input_dir = conf.get('vhodna_mapa')
                self.output_dir = conf.get('izhodna_mapa')
        except Exception as e:
            self.error = 'Napaka v konfiguraciji.'
            self.error_trace = e
            return

        # Validation.
        if not os.path.isdir(self.input_dir):
            self.error = 'Vhodna mapa ne obstaja. F1 za več info.'
        elif not os.path.isdir(self.output_dir):
            self.error = 'Izhodna mapa ne obstaja. F1 za več info.'


class MatchedFile:
    def __init__(self, path):
        self.path = path


p = Program()
p.start_gui()
