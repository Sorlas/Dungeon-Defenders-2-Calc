#!/usr/bin/python3

import tkinter
from tkinter import ttk
from random import randint
import time

class DungeonDefenders(tkinter.Frame):
    def __init__(self, master=None, debug=False):
        super().__init__(master)
        self.debug = debug
        self.regdmg = 0
        self.regdmg_fault = False
        self.critdmg = 0
        self.critdmg_fault = False
        self.atkrate = 0
        self.atkrate_fault = False
        self.crit = 0
        self.crit_fault = False
        self.runs = 100000

        self.setup_frame(master)
        self.setup_entry_boxes(master)
        self.setup_text_boxes(master)
        self.setup_buttons(master)
        self.grid()

    def textbox_update(self):
        self.textbox.delete(0.5, tkinter.END)
        if self.regdmg_fault or self.critdmg_fault or self.crit_fault or self.atkrate_fault:
            if self.regdmg_fault:
                self.textbox.insert(tkinter.CURRENT, "Regular DMG does not contain\na valid value\n")
            if self.critdmg_fault:
                self.textbox.insert(tkinter.CURRENT, "Crit DMG does not contain\na valid value\n")
            if self.atkrate_fault:
                self.textbox.insert(tkinter.CURRENT, "Atk Rate does not contain\na valid value\n")
            if self.crit_fault:
                self.textbox.insert(tkinter.CURRENT, "Crit Chance does not contain\na valid value")
        else:
            self.textbox.insert(tkinter.CURRENT, "Result will be here...\nClick Calc")

    def write_regdmg(self, event):
        try:
            self.regdmg = int(event.widget.get())
            self.regdmg_fault = False
        except ValueError:
            self.entry_regdmg.delete(0, tkinter.END)
            self.entry_regdmg.insert(0, "Regular DMG")
            self.regdmg_fault = True

        self.textbox_update()

        if self.debug:
            print("Regdmg =", self.regdmg)

    def write_critdmg(self, event):
        try:
            self.critdmg = int(event.widget.get())
            self.critdmg_fault = False
        except ValueError:
            self.entry_critdmg.delete(0, tkinter.END)
            self.entry_critdmg.insert(0, "Critical DMG")
            self.critdmg_fault = True

        self.textbox_update()

        if self.debug:
            print("Critdmg =", self.critdmg)

    def write_atkrate(self, event):
        try:
            self.atkrate = float(event.widget.get().replace(",", "."))
            self.atkrate_fault = False
        except ValueError:
            self.entry_atkrate.delete(0, tkinter.END)
            self.entry_atkrate.insert(0, "Attack Rate")
            self.atkrate_fault = True

        self.textbox_update()

        if self.debug:
            print("AtkRate =", self.atkrate)

    def write_crit(self, event):
        try:
            self.crit = int(event.widget.get())
            self.crit_fault = False
        except ValueError:
            self.entry_crit.delete(0, tkinter.END)
            self.entry_crit.insert(0, "Crit. Chance")
            self.crit_fault = True

        self.textbox_update()

        if self.debug:
            print("Crit =", self.crit)

    def setup_entry_boxes(self, master):
        self.entry_regdmg = self.add_entry(master, "Regular DMG", 0, 0, self.write_regdmg)
        self.entry_critdmg = self.add_entry(master, "Critical DMG", 1, 0, self.write_critdmg)
        self.entry_atkrate = self.add_entry(master, "Attack Rate", 2, 0, self.write_atkrate)
        self.entry_crit = self.add_entry(master, "Crit. Chance", 3, 0, self.write_crit)

    def setup_text_boxes(self, master):
        self.add_textbox(master, "Result will be here...\nClick Calc", 4, 0, 2)

    def setup_frame(self, master):
        frame = tkinter.Frame(master)
        frame.bind("<Button-1>", self.callback)

    def setup_buttons(self, master):
        self.add_button(master, "Calc", 4, 0, self.do_calc, tkinter.W )
        self.add_button(master, "Exit", 4, 1, lambda: self.exit_frame(master), tkinter.W)

    def exit_frame(self, master):
        master.destroy()

    def del_entry(self, event):
        event.widget.delete(0, tkinter.END)

    def add_textbox(self, master, text, rowspan, row, column):
        self.textbox = tkinter.Text(master)
        self.textbox.config(height=10, width=30)
        self.textbox.insert(tkinter.CURRENT, text)
        self.textbox.grid(rowspan=rowspan, column=column, row=row, sticky=tkinter.E)

    def add_entry(self, master, text, row, column, function):
        entry = tkinter.Entry(master)
        entry.config(width=15)
        entry.insert(0, text)
        entry.bind("<FocusIn>", self.del_entry)
        entry.bind("<FocusOut>", function)
        entry.bind("<Return>", function)
        entry.bind("<Tab>", function)
        entry.grid(row=row, column=column, sticky=tkinter.N)
        return entry

    def add_button(self, master, text, row, column, function, alignment):
        button = tkinter.Button(master, text=text, command=function)
        button.grid(row=row, column=column, sticky=alignment)

    def callback(self, event):
        print("Callback at: ", event.x, event.y)

    def get_value(self):
        return [ self.regdmg, self.critdmg, self.atkrate, self.crit ]

    def get_haderror(self):
        if self.regdmg_fault or self.critdmg_fault or self.atkrate_fault or self.crit_fault:
            return True
        else:
            return False

    def do_calc(self):
        self.CreateProgressBarWindow()
        total_dmg = 0
        dps = 0

        if self.debug:
            now = time.time()

            self.progressbar.start()
        for i in range(0, self.runs):
            rand = randint(0, 100)
            self.progressbar.update()
            if(rand <= self.crit):
                total_dmg += self.regdmg
                total_dmg += self.critdmg
            else:
                total_dmg += self.regdmg

        if self.debug:
            end = time.time()
            print("Took %s seconds to complete the main loop" % (end - now))

        total_dmg = total_dmg / self.atkrate
        dps = total_dmg / self.runs
        self.progresswindow.destroy()
        self.textbox.delete(0.5, tkinter.END)
        self.textbox.insert(tkinter.INSERT, "Total DMG: %s\nThat is %s DPS" % (int(total_dmg), int(dps)))

    def CreateProgressBarWindow(self):
        self.progresswindow = tkinter.Toplevel(self)
        #self.progresswindow.overrideredirect(True)
        self.progresswindow.wm_title("Simulating...")
        self.progressbar = ttk.Progressbar(self.progresswindow, length=200, mode="indeterminate")
        self.progressbar.pack()

if __name__ == '__main__':
    MainFrame = tkinter.Tk()
    MainFrame.wm_title("Dungeon Defenders 2 Calc")
    app = DungeonDefenders(MainFrame, True)
    app.grid()
    app.mainloop()
