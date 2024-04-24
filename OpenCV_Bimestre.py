from tkinter import PhotoImage
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
import cv2
import numpy as np
import customtkinter as ctk
from customtkinter import filedialog
import os
from scipy.ndimage import gaussian_filter

class OpenCV_Bimestre:

    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1030x510")
        self.root.title("Trabalho Bimestre")

        master_frame = ctk.CTkFrame(self.root)
        master_frame.pack(fill="both", expand=True)
        subframe = ctk.CTkFrame(master=master_frame)
        subframe.grid(row=1, column=1, padx=10, pady=10)    

        # Posicionamento dos widgets na grade
        self.bt_imgoriginal = ctk.CTkButton(master=master_frame, text="Load Image", command=self.imagemOriginal)
        self.bt_imgoriginal.grid(row=0, column=0, padx=5, pady=5, sticky="s")
        
        self.limpar = ctk.CTkButton(master=master_frame, text="Limpar", command=self.limpar)
        self.limpar.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        self.combobox = ctk.CTkOptionMenu(master=subframe,
                                           values=["Gray", "Gaussian", "Edges", "Binarized", "Morphology"])
        self.combobox.pack(padx=2, pady=2)
        
        self.bt_iniciar = ctk.CTkButton(master=subframe, text="Aplicar", command=self.Optionmenu)
        self.bt_iniciar.pack(padx=5, pady=5)



        # Caixas para exibir as imagens
        self.canvas_original = ctk.CTkCanvas(master=master_frame, width=500, height=500, bd=5, highlightbackground="blue")
        self.canvas_original.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.canvas_modicado = ctk.CTkCanvas(master=master_frame, width=500, height=500, bd=5, highlightbackground="blue")
        self.canvas_modicado.grid(row=1, column=2, padx=10, pady=10, columnspan=2,  sticky="e")  # Estender por duas colunas
        
        self.salvar = ctk.CTkButton(master=master_frame, text="Salvar", command= self.save)
        self.salvar.grid(row=3, column=2, padx=5, pady=5, sticky="e")

        # Variáveis de instância adicionadas
        self.image = None
        self.gray_image = None
        self.filtered_image = None
        self.edges_image = None
        self.binarized_image = None
        self.morph_image = None
        self.kernel = np.ones((5, 5), np.float32) / 25
        self.image_tk = None
        
        self.save_path = None 
        self.files = None

    def Optionmenu(self):
        option = self.combobox.get()

        if option == "Gray":
            self.Gray()
        elif option == "Gaussian":
            self.Gaussian()
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
        image_pil_resized = self.resize_image_to_canvas(image_pil, (500, 500))  # Redimensionar imagem para o tamanho do canvas
        self.image_tk = ImageTk.PhotoImage(image_pil_resized)
        self.canvas_original.delete("all")
        self.canvas_original.create_image(0, 0, anchor="nw", image=self.image_tk)

    def show_image_on_canvas2(self, image):
        image_pil_resized = self.resize_image_to_canvas(image, (500, 500))  # Redimensionar imagem para o tamanho do canvas
        image_tk = ImageTk.PhotoImage(image_pil_resized)
        self.canvas_modicado.delete("all")
        self.canvas_modicado.create_image(0, 0, anchor="nw", image=image_tk)
        self.canvas_modicado.image = image_tk

    def resize_image_to_canvas(self, image, canvas_size):
        return image.resize(canvas_size, Image.LANCZOS)
    
    
    def limpar(self):
        self.canvas_modicado.delete("all") 
    
    
    def save(self):
        if self.files:
            file = filedialog.asksaveasfile(filetypes=(("PNG file", "*.png"),("All Files", "*.*")), defaultextension =".png")
            if file:
                # Convertendo a imagem PIL de volta para o formato de arquivo
                self.files.save(file.name)

        

    def Gray(self):
        if self.image is not None:
            self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image_pil = Image.fromarray(self.gray_image)
            self.show_image_on_canvas2(self.image_pil)
            self.files = self.image_pil
        else:
            print("Nenhuma imagem carregada.")
        
      
    def Gaussian(self):
        if self.image is not None:
            # Aplicando o filtro gaussiano com um desvio padrão de 1.5
            self.filtered_image = gaussian_filter(self.image, sigma=1.5)
            
            # Convertendo a imagem de volta para o formato PIL
            self.image_pil = Image.fromarray(np.uint8(self.filtered_image))
            
            # Exibindo a imagem no canvas
            self.show_image_on_canvas2(self.image_pil)
            
            # Salvando a imagem filtrada
            self.files = self.image_pil
        else:
            print("Nenhuma imagem em tons de cinza disponível.")

    def Edges(self):
        if self.image is not None:
            self.edges_image = cv2.Canny(self.image, 100, 200)
            self.image_pil = Image.fromarray(self.edges_image)
            self.show_image_on_canvas2(self.image_pil)
            self.files = self.image_pil
        else:
            print("Nenhuma imagem filtrada disponível.")

    def Binarized(self):
        if self.image is not None:
            _, self.binarized_image = cv2.threshold(self.image, 128, 255, cv2.THRESH_BINARY)
            self.image_pil = Image.fromarray(self.binarized_image)
            self.show_image_on_canvas2(self.image_pil)
            self.files = self.image_pil
        else:
            print("Nenhuma imagem com bordas disponível.")

    def Morphology(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.uint8)
            self.morph_image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
            self.image_pil = Image.fromarray(self.morph_image)
            self.show_image_on_canvas2(self.image_pil)
            self.files = self.image_pil
        else:
            print("Nenhuma imagem binarizada disponível.")

if __name__ == "__main__":
    app = OpenCV_Bimestre()
    app.root.mainloop()
