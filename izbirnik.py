# -*- coding: utf-8 -*-

import yaml
import os
import re
import tkinter
import shutil
import sys


class UI(tkinter.Frame, object):
    status_text = None

    def __init__(self, backend=None):
        self.master = tkinter.Tk()
        self.master.geometry('750x500+100+100')
        self.master.title('Izbirnik')
        self.backend = backend
        super(UI, self).__init__(self.master, bg='white', borderwidth=10)
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
            def callback(button, matched_file):
                def f():
                    self.on_button_click(button, matched_file)
                return f

            btn = tkinter.Button(
                self.files_found_container,
                text=f.path,
                font=("Courier", 10),
                pady=10,
                background='white',
            )
            btn.config(command=callback(btn, f))
            btn.pack(fill=tkinter.X)

    def show_config(self, *args, **kwargs):
        self.clear_buttons()
        tkinter.Label(self.files_found_container, text='v0.3.0', font=("Courier", 20), background='white', pady=10).pack()

        tkinter.Label(self.files_found_container, text='Vhodne mape:', font=("Courier", 20), background='white', pady=10).pack()
        tkinter.Label(self.files_found_container, text='\n'.join(self.backend.input_dirs), font=("Courier", 12), background='white', pady=10).pack()

        tkinter.Label(self.files_found_container, text='Končnice:', font=("Courier", 20), background='white', pady=10).pack()
        tkinter.Label(self.files_found_container, text=', '.join(self.backend.suffices), font=("Courier", 12), background='white', pady=10).pack()

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
    def __init__(self, yaml_path=None):
        self.ui = None
        self.error = None
        self.error_trace = None
        self.yaml_path = yaml_path or './izbirnik.yaml'
        self.input_dirs = None
        self.suffices = None
        self.output_dir = None
        self.load_configuration()

    def start_gui(self):
        self.ui = UI(backend=self)
        self.ui.mainloop()

    def match_pattern(self, pattern):
        r = None
        try:
            r = re.compile('^{}{}$'.format(pattern, self.suffices_to_regex()))
        except Exception as e:
            self.error = 'Neveljavno ime datoteke.'
            self.error_trace = e
            return []

        res = []
        for input_dir in self.input_dirs:
            for subdir, dirs, files in os.walk(input_dir):
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
        if not os.path.isfile(self.yaml_path):
            self.error = 'Konfiguracijska datoteka ne obstaja.'
            return

        try:
            with open(self.yaml_path) as f:
                conf = yaml.load(f)
                self.input_dirs = conf.get('vhodne_mape')
                self.suffices = conf.get('koncnice')
                self.output_dir = conf.get('izhodna_mapa')
        except Exception as e:
            self.error = 'Napaka v konfiguraciji.'
            self.error_trace = e
            return

        # Validation.
        if self.input_dirs is None:
            self.error = 'Parameter "vhodne_mape" ni definiran.'
            return
        if self.suffices is None:
            self.error = 'Parameter "koncnice" ni definiran.'
            return
        if self.output_dir is None:
            self.error = 'Parameter "izhodna_mapa" ni definiran.'
            return
        for idx, input_dir in enumerate(self.input_dirs):
            if not os.path.isdir(input_dir):
                self.error = '{}. vhodna mapa ne obstaja. F1 za več info.'.format(idx+1)
                return
        if not os.path.isdir(self.output_dir):
            self.error = 'Izhodna mapa ne obstaja. F1 za več info.'
            return

    def suffices_to_regex(self):
        return ''.join(['({})?'.format(suffix) for suffix in self.suffices])


class MatchedFile:
    def __init__(self, path):
        self.path = path

yaml_path = None
if len(sys.argv) > 1:
    yaml_path = sys.argv[1]
p = Program(yaml_path)
p.start_gui()
