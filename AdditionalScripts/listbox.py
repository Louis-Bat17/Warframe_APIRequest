import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext
import tkinter.ttk as ttk
import tkinter.constants as const
import tkinter.font as font
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import tkinter.colorchooser as colorchooser
import tkinter.tix as tix
import tkinter.dnd as dnd
import tkinter.simpledialog as simpledialog
import tkinter.font as font
import tkinter.colorchooser as colorchooser

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Create a list of items
        self.items = ["Item 1", "Item 2", "Item 3"]

        # Create a Listbox widget
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Add the items to the Listbox
        for item in self.items:
            self.listbox.insert(tk.END, item)

        # Bind the Listbox to the copy function
        self.listbox.bind('<Double-Button-1>', self.copy)

    def copy(self, event):
        # Get the selected item
        selection = self.listbox.curselection()
        if len(selection) == 0:
            return
        selected_item = self.items[selection[0]]

        # Copy the selected item to the clipboard
        self.clipboard_clear()
        self.clipboard_append(selected_item)

        # Show a message box indicating that the item has been copied
        messagebox.showinfo("Copied", "Item has been copied to the clipboard.")

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
