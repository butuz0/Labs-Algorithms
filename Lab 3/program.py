from b_tree import BTree
from random import randint
import customtkinter
from customtkinter import *
from tkinter import messagebox
from tkinter import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class BTreeProgram:
    def __init__(self, t):
        self.tree = BTree(t)
        self.elements_amount = 0

        self.window = CTk()
        self.window.title("B-Tree")
        self.window.geometry("1030x600")

        self.commands = CTkFrame(self.window)
        self.commands.grid(row=0, column=0, sticky=(N, W))

        self.visual_tree = []

        self.autofill_button = CTkButton(self.commands, text="Auto Fill", width=240, command=self.autofill)
        self.autofill_button.grid(row=0, column=0, padx=10, pady=5)

        self.elem_quantity = CTkEntry(self.commands, placeholder_text="Quantity", width=140)
        self.elem_quantity.grid(row=0, column=1)

        self.insert_button = CTkButton(self.commands, text="Insert Data", width=240, command=self.insert)
        self.insert_button.grid(row=1, column=0, padx=10, pady=5)

        self.insertion_key = CTkEntry(self.commands, placeholder_text="Key", width=140)
        self.insertion_key.grid(row=1, column=1)

        self.insertion_data = CTkEntry(self.commands, placeholder_text="Data", width=140)
        self.insertion_data.grid(row=1, column=2)

        self.search_button = CTkButton(self.commands, text="Search", width=240, command=self.search)
        self.search_button.grid(row=2, column=0, padx=10, pady=5)

        self.search_key = CTkEntry(self.commands, placeholder_text="Key", width=140)
        self.search_key.grid(row=2, column=1)

        self.edit_button = CTkButton(self.commands, text="Edit element", width=240, command=self.replace)
        self.edit_button.grid(row=3, column=0, padx=10, pady=5)

        self.edit_key = CTkEntry(self.commands, placeholder_text="Key", width=140)
        self.edit_key.grid(row=3, column=1, pady=5)

        self.edit_value = CTkEntry(self.commands, placeholder_text="Data", width=140)
        self.edit_value.grid(row=3, column=2, pady=5, padx=10)

        self.delete_button = CTkButton(self.commands, text="Delete element", width=240, command=self.delete)
        self.delete_button.grid(row=4, column=0, padx=10, pady=5)

        self.delete_value = CTkEntry(self.commands, placeholder_text="Key", width=140)
        self.delete_value.grid(row=4, column=1)

        self.print_button = CTkButton(self.commands, text="Print Tree", width=240, command=self.pprint)
        self.print_button.grid(row=6, column=0, padx=10, pady=5)

        self.window.mainloop()

    def autofill(self):
        try:
            amount = int(self.elem_quantity.get())
        except ValueError:
            messagebox.showerror(title="Error", message="Fill the fields correctly")
            return
        if amount != 0:
            for i in range(amount):
                self.tree.insert((self.elements_amount, randint(0, 1000)))
                self.elements_amount += 1
            self.pprint()

    def insert(self):
        key = int(self.insertion_key.get())
        data = self.insertion_data.get()
        if data != "":
            self.tree.insert((key, data))
            self.pprint()

    def search(self):
        try:
            key = int(self.search_key.get())
        except ValueError:
            messagebox.showerror(title="Error", message="Fill the fields correctly")
            return
        else:
            i, node, parent = self.tree.uniform_bin_search(key, self.tree.root)
            if node:
                print(f"node: {[elem[0] for elem in node.keys]}\n"
                      f"index: {i}\n"
                      f"key: {key}\n"
                      f"data: {node.keys[i][1]}\n")
            else:
                messagebox.showerror(title="Error", message="Key does not exist")

    def replace(self):
        try:
            key = int(self.edit_key.get())
            value = self.edit_value.get()
        except ValueError:
            messagebox.showerror(title="Error", message="Fill the fields correctly")
            return
        else:
            self.tree.replace(key, value)
            self.pprint()

    def delete(self):
        try:
            key = int(self.delete_value.get())
        except ValueError:
            messagebox.showerror(title="Error", message="Fill the fields correctly")
            return
        else:
            if not self.tree.delete_key(key):
                messagebox.showerror(title="Error", message="Key does not exist")
            else:
                self.elements_amount -= 1
            self.pprint()

    def pprint(self):
        if self.visual_tree:
            for row in self.visual_tree:
                row.configure(text="")

        text = self.tree.print_tree(self.tree.root)
        if self.elements_amount <= 130:
            for i, level in enumerate(text):
                x = CTkLabel(self.window, text=level, font=("Courier", 12, "normal"))
                x.grid(row=i+1, column=0)
                self.visual_tree.append(x)
        else:
            self.tree.console_print(self.tree.root)
            print("\n")

    def test(self):
        for _ in range(15):
            i, node, parent = self.tree.uniform_bin_search(randint(0, self.elements_amount), self.tree.root)
            if node:
                print(f"\nkey: {node.keys[i][0]}")
            print(self.tree.compares)
            self.tree.compares = 0
