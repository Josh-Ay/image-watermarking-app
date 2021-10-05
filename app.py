import getpass
import os
from os import name
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog

import PIL
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
import pathlib

WHITE, RED, GREY, BLACK, GREEN = "#FFF", "#DE1F34", "#F0F0F0", "#000", "#0Eff00"
FONT = ("Roboto", 12)


class App:
    def __init__(self):
        self.img = ""
        self.filepath = ""
        self.watermark_img = ""

        self.window = TkinterDnD.Tk()
        self.window.title("Image Watermarking App")
        self.window.iconbitmap("./icon/favicon.ico")
        self.window.config(padx=0, pady=0, bg=WHITE)

        self.canvas = tk.Canvas(width=500, height=400, bg=WHITE, highlightthickness=0)
        self.canvas.grid(column=1, row=1, columnspan=2)

        # Drag and drop functionality
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind("<<Drop>>", self.drop_inside_canvas)

        self.intro_image = PhotoImage(file="./bg.png")
        self.background_image = self.canvas.create_image(250, 180, image=self.intro_image)
        self.info_text = self.canvas.create_text(250, 180, text="Drag and drop your image here or click 'add' button "
                                                                "above \n \t\t (JPG, PNG or GIF)", font=FONT)

        self.cancel_btn = Button(text="Cancel", font=FONT, borderwidth=0, relief="flat", bg=GREY, fg=BLACK,
                                 command=self.remove_loaded_image)
        self.cancel_btn.grid(column=0, row=0, padx=15, pady=15)

        self.add_btn = Button(text="Add", font=FONT, bg=GREEN, fg=WHITE, borderwidth=0, relief="flat",
                              command=self.open_image_from_system)
        self.add_btn.grid(column=3, row=0, padx=20, pady=15)

        self.watermark_btn = Button(text="Add Watermark", font=FONT, bg=GREY, fg=BLACK, borderwidth=0, relief="flat",
                                    command=self.watermark_image)
        self.watermark_btn.grid(column=1, row=2, pady=15)

        self.download_btn = Button(text="Download", font=FONT, bg=GREEN, fg=WHITE, borderwidth=0, relief="flat",
                                   command=self.download_image_to_system)
        self.download_btn.grid(column=2, row=2, pady=15)

        self.window.mainloop()

    def open_image_from_system(self):
        """ To select an image from the user's device """
        # windows
        if name == "nt":
            name_of_user = getpass.getuser()  # to get the name of the current user
            self.filepath = filedialog.askopenfilename(initialdir=f"C:/Users/{name_of_user}/", title="Select image",
                                                       filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png"),
                                                                  ("GIF files", "*.gif")))

            if self.filepath != "":
                self.img = ImageTk.PhotoImage(Image.open(self.filepath))
                self.load_image(self.img)

        # mac os
        else:
            self.filepath = filedialog.askopenfilename(initialdir="~/", title="Select image",
                                                       filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png"),
                                                                  ("GIF files", "*.gif")))
            if self.filepath != "":
                self.img = ImageTk.PhotoImage(Image.open(self.filepath))
                self.load_image(self.img)

    def load_image(self, image_to_load):
        """ To load an image into the canvas """
        self.canvas.itemconfig(self.info_text, text="")

        self.canvas.itemconfig(self.background_image, image=image_to_load)
        self.canvas.update()

    def watermark_image(self):
        """ To watermark the image """
        if self.img != "":
            image_new = Image.open(self.filepath)

            draw = ImageDraw.Draw(image_new)
            image_width, image_height = image_new.size
            watermark_text = simpledialog.askstring(title="Enter watermark text", prompt="Please enter the text you "
                                                                                         "would like to put on the "
                                                                                         "image")
            if watermark_text is not None:
                font_size = simpledialog.askinteger(title="Enter font size",
                                                    prompt="Please enter the font size (e.g 1,6,16) "
                                                           "you would like: ")
                image_file_extension = pathlib.Path(self.filepath).suffix
                if font_size is not None:
                    image_font = ImageFont.truetype("arial.ttf", font_size)
                    text_width, text_height = draw.textsize(watermark_text, image_font)
                    x, y = image_width - text_width, image_height - text_height
                    draw.text((x, y), watermark_text, font=image_font)

                    image_new.save(f"watermark{image_file_extension}")  # saving the new image
                    self.watermark_img = ImageTk.PhotoImage(Image.open("watermark.jpg"))
                    self.load_image(self.watermark_img)  # loading the watermarked image into the canvas

                else:
                    image_font = ImageFont.truetype("arial.ttf", 16)
                    text_width, text_height = draw.textsize(watermark_text, image_font)
                    x, y = image_width - text_width, image_height - text_height
                    draw.text((x, y), watermark_text, font=image_font)

                    image_new.save(f"watermark{image_file_extension}")  # saving the new image
                    self.watermark_img = ImageTk.PhotoImage(Image.open("watermark.jpg"))
                    self.load_image(self.watermark_img)

    def remove_loaded_image(self):
        """ To remove the loaded image from the canvas """
        if self.img != "":
            is_ok_to_delete = messagebox.askyesnocancel(title="Delete Image",
                                                        message="Are you sure you want to delete this"
                                                                " image? ")

            if is_ok_to_delete:
                self.canvas.itemconfig(self.info_text, text="Drag and drop your image here or click 'add' button above"
                                                            "\n \t\t (JPG, PNG or GIF)")
                self.canvas.itemconfig(self.background_image, image=self.intro_image)

        else:
            self.canvas.itemconfig(self.info_text, text="Drag and drop your image here or click 'add' button above"
                                                        "\n \t\t (JPG, PNG or GIF)")
            self.canvas.itemconfig(self.background_image, image=self.intro_image)

    def download_image_to_system(self):
        """ To download the watermarked image to the user's device """
        if self.watermark_img != "":
            file_extension = pathlib.Path(self.filepath).suffix
            image_to_save = Image.open(f"watermark{file_extension}")   # load the image to save

            new_file = filedialog.asksaveasfile(defaultextension=file_extension, filetypes=[("JPG", ".jpg"),
                                                                                            ("PNG", ".png")])

            image_to_save.save(new_file.name)   # saving the image to the file created above
            os.remove("watermark.jpg")  # remove the copy of the image that is saved to the current directory

    def drop_inside_canvas(self, event):
        """ Drag and drop image into the canvas """
        self.filepath = event.data

        try:
            self.img = ImageTk.PhotoImage(Image.open(self.filepath))
        except PIL.UnidentifiedImageError:
            messagebox.showerror(title="Select an image", message="Please select a file with an extension of either "
                                                                  "'.jpg', '.jpeg','.png' or '.gif'")
        else:
            self.load_image(self.img)
