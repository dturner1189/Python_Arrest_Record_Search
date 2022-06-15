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
        self.entry.pack(side=LEFT, fill=BOTH, ipady=1, padx=(0,spacing))

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

        self.button_label.pack(side=LEFT, fill=Y, ipadx=button_ipadx)

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

    import os

    try:
        from Tkinter import Tk
        from tkMessageBox import showinfo
    except ImportError:
        from tkinter import Tk
        from tkinter.messagebox import showinfo

    def ShowButton():
        # grabs selected (highlighted) text and saves as a single srring
        selected_names = "%s" %text_box.get(tk.SEL_FIRST, tk.SEL_LAST)

        # Clear the text screen of previous results
        #text_box.delete('1.0', END)

        # re-print just the eeslected nmes to the utput screen
        #printToTextbox(selected_names)

        # split the string into choped lines.
        # string.split(selected_names, '\n')

        v = IntVar()
        v.set(0)

        def ShowChoice():
            print(v.get())

        # iterate through and tokenize selected string by newlines
        for r in string.split(selected_names, '\n'):

            # test the split sptrings
            # print(r)

            DOA_temp = r.split(" ")
            DOA = DOA_temp[-1]
            PDF = DOA + ".pdf"
            print(PDF)
            open("./pdfs/" + PDF)
            #subprocess.Popen(["./pdfs/" + PDF],shell=True)
            #os.startfile("./pdfs/" + PDF)

            #Radiobutton(root,
                #text=r,
                #padx = 20,
                #variable=v,
                #command=ShowChoice,
                #value=r).pack(anchor=W)





    def HelpButton():
        # Clear the text screen of previous results
        text_box.delete('1.0', END)

        # insert results into the text frame
        text_box.insert(tk.END, 'Help feature')

        myhelp = open("help.d", "r")

        # iterate through the line entries of the master log
        for line in myhelp:
            # print the transaction log out to the user
            printToTextbox(line)

        # scroll feature in the case of many matches
        text_box.see(tk.END)

    def ClearButton():
        # Clear the text screen of previous results
        text_box.delete('1.0', END)



    def UpdateButton():
        # Clear the text screen of previous results
        text_box.delete('1.0', END)
        printToTextbox("Updating arrest records now...")

        #
        #
        #


    def LogButton():
        # Clear the text screen of previous results
        text_box.delete('1.0', END)
        printToTextbox("View Log...\n")

        mylog = open("LOG.d", "r")

        #iterate through the line entries of the master log
        for line in mylog:
            # print the transaction log out to the user
            printToTextbox(line)


    # takes the text-box object and the string of the line the
    # search result was found on. format: First, Last Middle D-O-A
    def printToTextbox(line):
        # insert results into the text frame
        text_box.insert(tk.END, line)

        # scroll feature in the case of many matches
        text_box.see(tk.END)



    # this command is when the user hits the search button.
    # "text" is the variable search string passed in from the user
    def SearchButton(text):
        # "myfile" = sorted.txt
        with open('sorted.txt') as myfile:

            # if a person matches the users search
            if text.upper() in myfile.read():

                # pop-up window showing results have been found
                # showinfo("Leon County Dirtbag Search", "Results Found for \"%s\"!"%text)

                # Clear the text screen of previous results
                text_box.delete('1.0', END)

                # opens the file with the sorted list of arrested persons
                myfile = open("sorted.txt", "r")

                # search every line in the sorted list
                for line in myfile:
                    # list is in uppercase, so convert and search
                    if re.search(text.upper(), line):
                        # print to console, the lines found from search result
                        #print(line)

                        # print the criminals line item to the text screen in main widget
                        if text:
                            printToTextbox(line)



            # if no suspect matches the users search string
            else:
                showinfo("Leon County Dirtbag Search", "Sorry, Nothing found for \"%s\"!"%text)


    ################################################################

    #set up the root gui object (window pane)
    root = Tk()
    root.title("Leon County Dirtbag Search")
    # set up a search box object in the frame
    SearchBox(root, command=SearchButton, placeholder="Who do you want to search for?", entry_highlightthickness=0).pack(pady=6, padx=3)


    # set up the buttons on the right (utilities and such)
    button_pane = Frame()
    button_pane.pack(side=LEFT)

    # set up a text box in the frame
    text_box = Text(master=root)
    text_box.pack(side=LEFT, fill=Y)

    # set up the scroll bar all the way on the far right side
    ScrollBar = Scrollbar(root)
    ScrollBar.config(command=text_box.yview)
    text_box.config(yscrollcommand=ScrollBar.set)
    ScrollBar.pack(side=RIGHT, fill=Y)




    #### buttons on the side of the frame (utility features) ###############

    # Show Selected button
    Button(button_pane, text='   Show  ', command=ShowButton).pack()

    # Update button
    Button(button_pane, text=' Update ', command=UpdateButton).pack()

    # view log button
    Button(button_pane, text='View log', command=LogButton).pack()

    # Help button
    Button(button_pane, text='   Help   ', command=HelpButton).pack()

    # clear button
    Button(button_pane, text='  Clear   ', command=ClearButton).pack()

    # exit button
    Button(button_pane, text='   Exit    ', command=root.destroy).pack()

    ### End of side buttons ###############################################

    # run the instance of our gui frame
    root.mainloop()

