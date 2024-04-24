from tkinter import PhotoImage
from PIL import Image, ImageTk
import cv2
import numpy as np
import customtkinter as ctk
from customtkinter import filedialog
import os

class ImageToolbox:
    def __init__(self):
        pass

    def convert_color(self, image, color_space):
        return cv2.cvtColor(image, color_space)

    def apply_filter(self, image, kernel):
        return cv2.filter2D(image, -1, kernel)

    def detect_edges(self, image, min_val=100, max_val=200):
        return cv2.Canny(image, min_val, max_val)

    def binarize(self, image, threshold=128, max_val=255, type=cv2.THRESH_BINARY):
        _, binarized = cv2.threshold(image, threshold, max_val, type)
        return binarized

    def apply_morphology(self, image, operation=cv2.MORPH_OPEN, kernel_size=5):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(image, operation, kernel)

class OpenCV_Bimestre:

    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1020x500")
        self.root.title("Trabalho Bimestre")

        master_frame = ctk.CTkFrame(self.root)
        master_frame.pack(fill="both", expand=True)
        subframe = ctk.CTkFrame(master=master_frame)
        subframe.grid(row=1, column=1, padx=10, pady=10)    

        # Posicionamento dos widgets na grade
        self.bt_imgoriginal = ctk.CTkButton(master=master_frame, text="Load Image", command=self.imagemOriginal)
        self.bt_imgoriginal.grid(row=0, column=0, padx=5, pady=5, sticky="s")
        
        self.limpar = ctk.CTkButton(master=master_frame, text="Limpar", command='')
        self.limpar.grid(row=0, column=2, padx=5, pady=5, sticky="e")


        self.combobox = ctk.CTkOptionMenu(master=subframe,
                                           values=["Gray", "Filtered", "Edges", "Binarized", "Morphology"])
        self.combobox.pack(padx=2, pady=2)
        
        self.bt_iniciar = ctk.CTkButton(master=subframe, text="Aplicar", command=self.Optionmenu)
        self.bt_iniciar.pack(padx=5, pady=5)



        # Caixas para exibir as imagens
        self.canvas_original = ctk.CTkCanvas(master=master_frame, width=400, height=400, bd=50, highlightbackground="blue")
        self.canvas_original.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.canvas_modicado = ctk.CTkCanvas(master=master_frame, width=400, height=400, bd=50, highlightbackground="blue")
        self.canvas_modicado.grid(row=1, column=2, padx=10, pady=10, columnspan=2,  sticky="e")  # Estender por duas colunas

        # Variáveis de instância adicionadas
        self.image_toolbox = ImageToolbox()
        self.image = None
        self.gray_image = None
        self.filtered_image = None
        self.edges_image = None
        self.binarized_image = None
        self.morph_image = None
        self.kernel = np.ones((5, 5), np.float32) / 25
        self.image_tk = None

    def Optionmenu(self):
        option = self.combobox.get()

        if option == "Gray":
            self.Gray()
        elif option == "Filtered":
            self.Filtered()
        elif option == "Edges":
            self.Edges()
        elif option == "Binarized":
            self.Binarized()
        elif option == "Morphology":
            self.Morphology()

    def imagemOriginal(self):
        # Carregar a imagem
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is not None:
                self.show_image_on_canvas()

    def show_image_on_canvas(self):
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil_resized = self.resize_image_to_canvas(image_pil, (400, 400))  # Redimensionar imagem para o tamanho do canvas
        self.image_tk = ImageTk.PhotoImage(image_pil_resized)
        self.canvas_original.delete("all")
        self.canvas_original.create_image(0, 0, anchor="nw", image=self.image_tk)

    def show_image_on_canvas2(self, image):
        image_pil_resized = self.resize_image_to_canvas(image, (400, 400))  # Redimensionar imagem para o tamanho do canvas
        image_tk = ImageTk.PhotoImage(image_pil_resized)
        self.canvas_modicado.delete("all")
        self.canvas_modicado.create_image(0, 0, anchor="nw", image=image_tk)
        self.canvas_modicado.image = image_tk

    def resize_image_to_canvas(self, image, canvas_size):
        return image.resize(canvas_size, Image.LANCZOS)

    def Gray(self):
        if self.image is not None:
            self.gray_image = self.image_toolbox.convert_color(self.image, cv2.COLOR_BGR2GRAY)
            image_pil = Image.fromarray(self.gray_image)
            self.show_image_on_canvas2(image_pil)
        else:
            print("Nenhuma imagem carregada.")

    def Filtered(self):
        if self.gray_image is not None:
            self.filtered_image = self.image_toolbox.apply_filter(self.gray_image, self.kernel)
            image_pil = Image.fromarray(self.filtered_image)
            self.show_image_on_canvas2(image_pil)
        else:
            print("Nenhuma imagem em tons de cinza disponível.")

    def Edges(self):
        if self.filtered_image is not None:
            self.edges_image = self.image_toolbox.detect_edges(self.filtered_image)
            image_pil = Image.fromarray(self.edges_image)
            self.show_image_on_canvas2(image_pil)
        else:
            print("Nenhuma imagem filtrada disponível.")

    def Binarized(self):
        if self.edges_image is not None:
            self.binarized_image = self.image_toolbox.binarize(self.edges_image)
            image_pil = Image.fromarray(self.binarized_image)
            self.show_image_on_canvas2(image_pil)
        else:
            print("Nenhuma imagem com bordas disponível.")

    def Morphology(self):
        if self.binarized_image is not None:
            self.morph_image = self.image_toolbox.apply_morphology(self.binarized_image)
            image_pil = Image.fromarray(self.morph_image)
            self.show_image_on_canvas2(image_pil)
        else:
            print("Nenhuma imagem binarizada disponível.")

if __name__ == "__main__":
    app = OpenCV_Bimestre()
    app.root.mainloop()
