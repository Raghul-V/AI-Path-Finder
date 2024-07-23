from tkinter import *
from tkinter import messagebox as msgbox


def message(msg_type, title="", message=""):
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    if msg_type == "showInfo":
        msgbox.showinfo(title, message)
    elif msg_type == "showError":
        msgbox.showerror(title, message)
    elif msg_type == "askokcancel":
        result = msgbox.askokcancel(title, message)
        root.destroy()
        return result
    root.destroy()


def get_inputs():
    def quit_prompt_box():
        if algorithm.get() != "Search Algorithm":
            prompt_box.destroy()
        else:
            msgbox.showerror("Invalid Search Algorithm", "Search algorithm cannot be empty.\nSelect any of the given algorithms in the options menu.")
        return True

    prompt_box = Tk()
    
    prompt_box.geometry("350x180")
    prompt_box.title("Required Inputs")

    size_title = Label(prompt_box, text="Maze Dimension: ", font=("Courier", 11))
    size_title.pack()
    size_title.place(relx=0.36, rely=0.125, anchor=CENTER)

    sizes = ["10 x 10", "25 x 25", "50 x 50"]

    size = StringVar()
    size.set("10 x 10")

    size_dropdown = OptionMenu(prompt_box, size, *sizes)
    size_dropdown.pack()
    size_dropdown.place(relx=0.7, rely=0.125, anchor=CENTER)

    search_algorithms = ["Depth First Search", "Breadth First Search", "Greedy Best-First Search", "A* Search"]

    algorithm = StringVar()
    algorithm.set("Search Algorithm")

    algorithm_dropdown = OptionMenu(prompt_box, algorithm, *search_algorithms)
    algorithm_dropdown.pack()
    algorithm_dropdown.place(relx=0.5, rely=0.31, anchor=CENTER)

    show_all_path = IntVar()
    checkbox1 = Checkbutton(prompt_box, text="Show all explored paths", variable=show_all_path,
                           onvalue=1, offvalue=0)
    checkbox1.pack()
    checkbox1.place(relx=0.5, rely=0.5, anchor=CENTER)

    allow_diagonal = IntVar()
    checkbox2 = Checkbutton(prompt_box, text="Allow Diagonal Moves", variable=allow_diagonal,
                           onvalue=1, offvalue=0)
    checkbox2.pack()
    checkbox2.place(relx=0.5, rely=0.63, anchor=CENTER)

    submit = Button(prompt_box, text="Submit", command=quit_prompt_box)
    submit.pack()
    submit.place(relx=0.5, rely=0.83, anchor=CENTER)

    def on_closing():
        if msgbox.askokcancel("Quit", "Do you want to close this window?\nNote: If you close this window, the program will quit automatically."):
            prompt_box.destroy()
            size.set("None")

    prompt_box.protocol("WM_DELETE_WINDOW", on_closing)

    prompt_box.mainloop()

    size = size.get().split("x")[0]
    return int(size.strip()), algorithm.get(), bool(show_all_path.get()), bool(allow_diagonal.get())


