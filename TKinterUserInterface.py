from tkinter import Tk, Label, Entry, Button


GREY = "#808080"
FONT_NAME = "Helvetica"
TEXT_COLOR = "#FCFBF4"
TITLE_SIZE = 30
TEXT_SIZE = 15


class YellowpagesGUI:
    def __init__(self):
        self.lead_data = {}
        self.window = Tk()
        yp = "Yellowpages Leads Generator"
        input_width = 28
        self.window.title(yp)
        self.window.config(padx=20, pady=20, bg=GREY)
        self.window.minsize(width=575, height=200)

        # Labels
        self.title = Label(text=yp, bg=GREY, font=(FONT_NAME, TITLE_SIZE), fg=TEXT_COLOR)
        self.title.grid(column=0, row=0, columnspan=3)
        self.niche_label = Label(text="niche", bg=GREY, font=(FONT_NAME, TEXT_SIZE), fg=TEXT_COLOR)
        self.niche_label.config(pady=6)
        self.niche_label.grid(column=0, row=2, sticky="W")
        self.city_label = Label(text="city", bg=GREY, font=(FONT_NAME, TEXT_SIZE), fg=TEXT_COLOR)
        self.city_label.grid(column=1, row=2, sticky="W")
        self.state_label = Label(text="state", bg=GREY, font=(FONT_NAME, TEXT_SIZE), fg=TEXT_COLOR)
        self.state_label.grid(column=2, row=2, sticky="W")
        self.whitespace = Label(text=" ", bg=GREY)
        self.whitespace.grid(column=0, row=4)
        # Entry
        self.niche_input = Entry(width=input_width)
        self.niche_input.grid(column=0, row=3)
        self.city_input = Entry(width=input_width)
        self.city_input.grid(column=1, row=3)
        self.state_input = Entry(width=input_width)
        self.state_input.grid(column=2, row=3)
        # Button
        self.scrape_button = Button(text="scrape", command=self.scrapeWithInput, anchor="s")
        self.scrape_button.grid(column=1, row=5)

    def run(self):
        self.window.mainloop()
        return self.lead_data


    def scrapeWithInput(self):
        self.lead_data = {
            "city": self.city_input.get(),
            "niche": self.niche_input.get(),
            "state": self.state_input.get()
        }
        self.window.quit()
