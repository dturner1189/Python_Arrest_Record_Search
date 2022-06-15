import Tkinter as tk
import re
try:
    from Tkinter import Entry, Frame, Label, StringVar
    from Tkconstants import *
except ImportError:
    from tkinter import Entry, Frame, Label, StringVar
    from tkinter.constants import *

def hex2rgb(str_rgb):
    try:
        rgb = str_rgb[1:]

        if len(rgb) == 6:
            r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
        elif len(rgb) == 3:
            r, g, b = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
        else:
            raise ValueError()
    except:
        raise ValueError("Invalid value %r provided for rgb color."% str_rgb)

    return tuple(int(v, 16) for v in (r, g, b))


class Placeholder_State(object):
     __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
    normal_color = entry.cget("fg")
    normal_font = entry.cget("font")

    if font is None:
        font = normal_font

    state = Placeholder_State()
    state.normal_color=normal_color
    state.normal_font=normal_font
    state.placeholder_color=color
    state.placeholder_font=font
    state.placeholder_text = placeholder
    state.contains_placeholder=True

    def on_focusin(event, entry=entry, state=state):
        if state.contains_placeholder:
            entry.delete(0, "end")
            entry.config(fg = state.normal_color, font=state.normal_font)

            state.contains_placeholder = False

    def on_focusout(event, entry=entry, state=state):
        if entry.get() == '':
            entry.insert(0, state.placeholder_text)
            entry.config(fg = state.placeholder_color, font=state.placeholder_font)

            state.contains_placeholder = True

    entry.insert(0, placeholder)
    entry.config(fg = color, font=font)

    entry.bind('<FocusIn>', on_focusin, add="+")
    entry.bind('<FocusOut>', on_focusout, add="+")

    entry.placeholder_state = state

    return state

class SearchBox(Frame):
    def __init__(self, master, entry_width=30, entry_font=None, entry_background="white", entry_highlightthickness=1, button_text="Search", button_ipadx=10, button_background="#009688", button_foreground="white", button_font=None, opacity=0.8, placeholder=None, placeholder_font=None, placeholder_color="grey", spacing=3, command=None):
        Frame.__init__(self, master)

        self._command = SearchButton

        self.entry = Entry(self, width=entry_width, background=entry_background, highlightcolor=button_background, highlightthickness=entry_highlightthickness)
        self.entry.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))

        if entry_font:
            self.entry.configure(font=entry_font)

        if placeholder:
            add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

        self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
        self.entry.bind("<Return>", self._on_execute_command)

        opacity = float(opacity)

        if button_background.startswith("#"):
            r,g,b = hex2rgb(button_background)
        else:
            # Color name
            r,g,b = master.winfo_rgb(button_background)

        r = int(opacity*r)
        g = int(opacity*g)
        b = int(opacity*b)

        if r <= 255 and g <= 255 and b <=255:
            self._button_activebackground = '#%02x%02x%02x' % (r,g,b)
        else:
            self._button_activebackground = '#%04x%04x%04x' % (r,g,b)

        self._button_background = button_background

        self.button_label = Label(self, text=button_text, background=button_background, foreground=button_foreground, font=button_font)
        if entry_font:
            self.button_label.configure(font=button_font)

        self.button_label.grid(column=1, row=0, padx=10, pady=5)

        self.button_label.bind("<Enter>", self._state_active)
        self.button_label.bind("<Leave>", self._state_normal)

        self.button_label.bind("<ButtonRelease-1>", self._on_execute_command)

    def get_text(self):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            if entry.placeholder_state.contains_placeholder:
                return ""
            else:
                return entry.get()
        else:
            return entry.get()

    def set_text(self, text):
        entry = self.entry
        if hasattr(entry, "placeholder_state"):
            entry.placeholder_state.contains_placeholder = False

        entry.delete(0, END)
        entry.insert(0, text)

    def clear(self):
        self.entry_var.set("")

    def focus(self):
        self.entry.focus()

    def _on_execute_command(self, event):
        text = self.get_text()
        self._command(text)

    def _state_normal(self, event):
        self.button_label.configure(background=self._button_background)

    def _state_active(self, event):
        self.button_label.configure(background=self._button_activebackground)



# Main routine for gui component
if __name__ == "__main__":

    from Tkinter import *

    import sys

    import requests
    from requests import get
    from requests.exceptions import RequestException

    import tkFont

    import string

    import webbrowser

    from array import array

    try:
        from Tkinter import Tk
        from tkMessageBox import showinfo
    except ImportError:
        from tkinter import Tk
        from tkinter.messagebox import showinfo

    #set up the root gui object (window pane)
    root = Tk()

    # Words in title bar of gui pane
    root.title("Leon County Dirtbag Search")

    # hashed array of the dates people were arrested
    dates_of_arrested = []
    # dates correspond to names of arrested in hash
    names_of_arrested = []
    # string form of name
    noa = StringVar(value=names_of_arrested)

    # hash each person/date with the associated pdf file
    files_of_arrested = {}


    user_ops = {'Open':'Open', 'Save':'Save', 'New':'New'}

    uop = StringVar()
    done_msg = StringVar()
    status_msg = StringVar()

    # user functions or operations to be done with their desired person. three strings are passed in relating to the person who was arrested. they are that persons pdf, name and date of arrest.
    def OpenFunction(pdf, name, date):
        print("open func " + pdf)
        #os.startfile("./pdfs/" + pdf)
        file = "./pdfs/" + pdf
        webbrowser.open_new(file)
        #print(file)
        #subprocess.Popen([file],shell=True)

    def SaveFunction(pdf, name, date):
        print("save func " + pdf)

    def NewFunction(pdf, name, date):
        print("New func" + pdf)



    def ShowDetails(*args):
        itr = lbox.curselection()
        if len(itr)==1:
            itr = int(itr[0])

            date = dates_of_arrested[itr].replace ('\n', '')
            name = names_of_arrested[itr].replace ('\n', '')
            pdf = files_of_arrested[date].replace ('\n', '')

            status_msg.set("  \"%s\", was arrested on %s. To Downlad the mugshot pdf, Click Save then Go." % (name, date))
        done_msg.set('')

    def GoButton(*args):

        idxs = lbox.curselection()
        if len(idxs)==1:
            idx = int(idxs[0])
            lbox.see(idx)

            date = dates_of_arrested[idx].replace ('\n', '')
            name = names_of_arrested[idx].replace ('\n', '')
            pdf = files_of_arrested[date].replace ('\n', '')


            usrs_choice = user_ops[uop.get()]

            done_msg.set("Attempting to %s file for \"%s\"." % (usrs_choice, name))

            if usrs_choice == 'Save':
                done_msg.set("Saving mugshot for \"%s\"." % (name))
                SaveFunction(pdf, name, date)
            if usrs_choice == 'Open':
                done_msg.set("Opening mugshot for \"%s\"." % (name))
                OpenFunction(pdf, name, date)
            if usrs_choice == 'New':
                done_msg.set("Someing New Feature for \"%s\"." % (name))
                NewFunction(pdf, name, date)

    def UpdateListbox(name, date, pdf):
        #print("Print to listbox: " + name + " " + date + " " + pdf)

        tot = len(str(name))
        diff = 30 - tot
        for i in range(0, diff):
            ins = name + " "
        fin = ins + date

        lbox.insert(END,fin)

    # this command is when the user hits the search button.
    # "text" is the variable search string passed in from the user
    def SearchButton(text):

        # Clear the arrays/hash from any previous results
        del dates_of_arrested[:]
        del names_of_arrested[:]
        files_of_arrested.clear()

        status_msg.set("")
        # "myfile" = sorted.txt
        with open('sorted.txt') as myfile:

            # if a person matches the users search
            if text.upper() in myfile.read():

                # opens the file with the sorted list of arrested persons
                myfile = open("sorted.txt", "r")

                lbox.delete(0, END)

                # search every line in the sorted list
                for line in myfile:
                    # list is in uppercase, so convert and search
                    if re.search(text.upper(), line):

                        # print the criminals line item to the text screen in main widget
                        if text:

                            DOA_temp = line.split(" ")
                            DOA = DOA_temp[-1]
                            #print(DOA)

                            NOA = line.rsplit(' ', 1)[0]
                            #print(NOA)

                            PDFT = DOA.replace ('\n', '')
                            PDFA = PDFT + ".pdf"
                            #print(PDFA)

                            dates_of_arrested.append(DOA)
                            names_of_arrested.append(NOA)

                            files_of_arrested[PDFT] = PDFA
                            #print(files_of_arrested)

                            name = NOA.replace ('\n', '')
                            date = PDFT.replace ('\n', '')
                            pdf = files_of_arrested[PDFT].replace ('\n', '')

                            UpdateListbox(name, date, pdf)


            # if no suspect matches the users search string
            else:
                showinfo("Leon County Dirtbag Search", "Sorry, Nothing found for \"%s\"."%text)



          #####################################
          #            GUI objects            #
          #####################################

    c = Frame(root)
    c.grid(column=0, row=0, sticky=(N,W,E,S))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0,weight=1)

    # set up a search box object in the frame
    SearchBox(root, command=SearchButton, placeholder="Who do you want to search for?", entry_highlightthickness=0).grid(column=1, row=0, padx=10, pady=5)


    lbox = Listbox(master=root, listvariable=noa, height=20, width=50)



    lbl = Label(root, text="What would you like to do:")



    op1 = Radiobutton(root, text=user_ops['Open'], variable=uop, value='Open')

    op2 = Radiobutton(root, text=user_ops['Save'], variable=uop, value='Save')

    op3 = Radiobutton(root, text=user_ops['New'], variable=uop, value='New')

    go_button = Button(root, text='Go', command=GoButton, default='active')

    action_commencing_lbl = Label(root, textvariable=done_msg, anchor='center')

    status = Label(root, textvariable=status_msg, anchor=W)



    lbox.grid(column=0, row=0, rowspan=25, sticky=(N,S,E,W))
    lbl.grid(column=1, row=1, padx=10, pady=5)

    op1.grid(column=1, row=2, sticky=W, padx=20)
    op1.invoke() # makes sure that "open" radio button is selected by default
    op2.grid(column=1, row=3, sticky=W, padx=20)
    op3.grid(column=1, row=4, sticky=W, padx=20)

    go_button.grid(column=1, row=5, sticky=(W,E))

    action_commencing_lbl.grid(column=1, row=6, columnspan=2, sticky=N, pady=5, padx=5)

    status.grid(column=0, row=7, columnspan=2, sticky=(W,E))

    lbox.bind('<<ListboxSelect>>', ShowDetails)
    lbox.bind('<Double-1>', GoButton)
    root.bind('<Return>', ShowDetails)

    for i in range(0,len(names_of_arrested),2):
        lbox.itemconfigure(i, background='#f0f0ff')

    lbox.selection_set(0)


    # run the instance of our gui frame
    root.mainloop()
