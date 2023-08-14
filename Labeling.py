"""
Used to label data on the yolo format.
The bunding boxes will be saved in the following format:

Name of label text file = image name, in text file:
[x0 y0 x1 y1], "class_name1"
[x0 y0 x1 y1], "class_name1"

How to do this:

Create one window, have text field to add classes. When adding a class it will show up with a check box next to it
A canvas will be drawn with an image in it. Select the class and draw bounding boxes on canvas. 

Hit the next image button label file will then be saved and a new image will appear. 
"""
import tkinter as tk
from PIL import ImageTk, Image
import os
class image_loader:
    def __init__(self,image_dir,label_dir):
        super().__init__()
        self.all_images = os.listdir(image_dir)
        for i in self.all_images:
            if os.listdir(label_dir):
                for r in os.listdir(label_dir):
                    if i.strip(".jpg") == r.strip(".txt"):
                        self.all_images.remove(i)

class CreateWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("450x300")
        
        self.drawing = False
        self.start_x = 0
        self.start_y = 0
        self.current_rectangle = None
        self.rectangles = []
        self.colors = ["red","blue","black","white","yellow"]

        self.frame = tk.Frame(self.window, width=300, height=300)
        self.frame.pack(side="left")

        self.canvas = tk.Canvas(self.frame, width=300, height=300)
        self.canvas.pack(side="top",padx=0, pady=0)
        self.canvas.configure(background="black")
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.image_index = 0
        
        
        self.image_path = "Data_Label_yolov1\\Images\\"
        self.label_path = "Data_Label_yolov1\\Labels\\"
        self.images = image_loader(self.image_path,self.label_path).all_images
        self.image = Image.open(self.image_path+self.images[self.image_index])
        self.image = self.image.resize((300, 300))
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        self.right_frame = tk.Frame(self.window, width=150, height=270)
        self.right_frame.pack(side="top", padx=0, pady=0)

        self.text_field = tk.Entry(self.right_frame)
        self.text_field.pack(pady=10)

        self.add_button = tk.Button(self.right_frame, text="Add class", command=self.add_checkbox)
        self.add_button.pack()

        self.checkbox_frame = tk.Frame(self.right_frame)
        self.checkbox_frame.pack(pady=10)

        self.checkboxes = []  # To store checkboxes

        self.next_button_frame = tk.Frame(self.window,width=150,height=30)
        self.next_button_frame.pack(side="bottom")

        self.next_image_button = tk.Button(self.next_button_frame,text="Next picture",command=self.next_figure)
        self.next_image_button.pack(pady=5)

        self.window.mainloop()

    def destroy_rectangles(self):
        for i in self.rectangles:
            self.canvas.delete(i[0])
        self.rectangles = []

    def save_labels(self):
        with open(self.label_path+self.images[self.image_index].replace(".jpg",".txt"), 'w') as f:
            for rectangle in self.rectangles:
                f.write(str(self.canvas.bbox(rectangle[0])))
                f.write(","+rectangle[1])
                f.write('\n')
            
    def next_figure(self):
        self.save_labels()
        self.image_index +=1
        self.image = Image.open(self.image_path+self.images[self.image_index])
        self.image = self.image.resize((300, 300))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_on_canvas,image=self.photo)
        self.destroy_rectangles()

    def pick_color(self, checkboxes):
        taken_colors = []
        for _,_,_,_,i,_ in checkboxes:
            taken_colors.append(i)
            print(f"taken_colors: {taken_colors}")
        available_colors = [i for i in self.colors if i not in taken_colors]
        return available_colors[0]

    def start_drawing(self, event):
        self.drawing = True
       
        self.start_x = event.x
        self.start_y = event.y
        self.current_rectangle = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline=self.checkboxes[self.current_index][4], width=2
        )

    def draw_rectangle(self, event):
        if self.drawing:
            self.canvas.coords(
                self.current_rectangle, self.start_x, self.start_y, event.x, event.y
            )

    def stop_drawing(self, event):
        if self.drawing:
            self.drawing = False
            self.rectangles.append((self.current_rectangle,self.checkboxes[self.current_index][5]))
        print(f'all rectangles = {self.rectangles}')

    def remove_checkbox(self, checkbox_touple):
        checkbox_touple[0].destroy()  # Remove the checkbox from the GUI
        checkbox_touple[2].destroy()  # Remove the corresponding "x" button
        checkbox_touple[3].destroy()
        for i in self.rectangles:
            if i[1] == checkbox_touple[5]:
                self.canvas.delete(i[0])
                self.rectangles.remove(i)
        self.checkboxes.remove(checkbox_touple)  # Remove the checkbox from the list

    def toggle_checkboxes(self, selected_checkbox):
        
        for checkbox in self.checkboxes:
            checkbox[0].deselect()
        selected_checkbox[0].select()
        self.current_index = self.checkboxes
        self.current_index = self.checkboxes.index(selected_checkbox)
        print(f'current {self.current_index}')
        
    def add_checkbox(self):
        text = self.text_field.get()
        if text:
            # Clear the text field
            self.text_field.delete(0, tk.END)

            checkbox_frame = tk.Frame(self.checkbox_frame)  # Create a new frame for each checkbox and button
            checkbox_frame.pack(anchor="w")

            # Create a separate IntVar for each checkbox
            checkbox_var = tk.IntVar(value=len(self.checkboxes))
            color = self.pick_color(self.checkboxes)
            checkbox = tk.Checkbutton(checkbox_frame, text=text, variable=checkbox_var,fg=color)
            checkbox.pack(side="left")
            
            # Add an "x" button to remove the checkbox
            remove_button = tk.Button(checkbox_frame, text="x", width=1, height=1)
            remove_button.pack(side="left")

            # Attach the checkbox, checkbox_var, and remove_button to a tuple for future management
            checkbox_tuple = (checkbox, checkbox_var, remove_button, checkbox_frame,color,text)
            self.checkboxes.append(checkbox_tuple)  # Store the checkbox and button in the list

            # Configure the checkbox command to toggle checkboxes
            checkbox.config(command=lambda c=checkbox_tuple: self.toggle_checkboxes(c))

             # Configure the "x" button command to call the remove_checkbox method
            remove_button.config(command=lambda c=checkbox_tuple: self.remove_checkbox(c))

window = CreateWindow()
window.window.mainloop()
