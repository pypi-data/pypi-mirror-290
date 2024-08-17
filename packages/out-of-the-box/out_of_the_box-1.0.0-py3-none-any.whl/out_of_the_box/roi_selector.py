import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from out_of_the_box.bounding_boxes import BoundingBox, VOCBox, YOLOBox, COCOBox


class ROISelector(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.state('zoomed')  # Start maximized

        self.image = None
        self.photo_image = None
        self.bounding_box = None
        self.image_position = (0, 0)
        self.scale_factor = 1.0

        # Frame for image
        self.image_frame = tk.Frame(self)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for entries and button
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Add a button for opening an image file
        open_button = tk.Button(self.entry_frame, text="Open Image", command=self.open_image)
        open_button.pack()

        # Create canvas
        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create input fields for each format
        self.voc_entries = self.create_format_entries("VOC", ["xmin", "ymin", "xmax", "ymax", "xmin_norm", "ymin_norm",
                                                              "xmax_norm", "ymax_norm"])
        self.coco_entries = self.create_format_entries("COCO",
                                                       ["x", "y", "width", "height", "x_norm", "y_norm", "width_norm",
                                                        "height_norm"])
        self.yolo_entries = self.create_format_entries("YOLO",
                                                       ["x_center", "y_center", "width", "height", "x_center_norm",
                                                        "y_center_norm", "width_norm", "height_norm"])

        # Mouse binding
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.start_x = None
        self.start_y = None

    def create_format_entries(self, format_name: str, field_names: list) -> dict:
        frame = tk.LabelFrame(self.entry_frame, text=format_name)
        frame.pack(fill=tk.X, padx=5, pady=5)
        entries = {}
        for i, name in enumerate(field_names):
            row = tk.Frame(frame)
            row.pack(fill=tk.X)
            tk.Label(row, text=f"{name}:").pack(side=tk.LEFT)
            entry = tk.Entry(row)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            entry.bind("<Return>", lambda event, f=format_name, n=name: self.on_entry_change(event, f, n))
            entries[name] = entry
            if i == 3:  # Add a separator between absolute and normalized values
                tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
        return entries

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.update_image()

    def update_image(self):
        if self.image is not None:
            # Get the size of the screen
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()

            # Get the size of the image
            img_height, img_width = self.image.shape[:2]

            # Calculate the scaling factor
            self.scale_factor = min(1.0, (screen_width * 0.8) / img_width, (screen_height * 0.8) / img_height)

            # Calculate new dimensions
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)

            # Resize the image
            resized_image = cv2.resize(self.image, (new_width, new_height), interpolation=cv2.INTER_AREA)

            self.photo_image = ImageTk.PhotoImage(image=Image.fromarray(resized_image))

            # Update window size
            window_width = new_width + self.entry_frame.winfo_reqwidth()
            window_height = max(new_height, self.entry_frame.winfo_reqheight())
            self.master.geometry(f"{window_width}x{window_height}")

            # Update canvas size
            self.canvas.config(width=new_width, height=new_height)

            # Calculate position to center the image
            self.image_position = ((new_width - self.photo_image.width()) // 2,
                                   (new_height - self.photo_image.height()) // 2)

            self.canvas.create_image(self.image_position[0], self.image_position[1], anchor=tk.NW,
                                     image=self.photo_image)

            # Reset the bounding box
            self.bounding_box = None
            self.canvas.delete("box")

    def start_draw(self, event):
        x, y = self.get_image_coordinates(event)
        if x is not None and y is not None:
            self.start_x, self.start_y = x, y

    def draw(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.canvas.delete("box")
            x, y = self.get_image_coordinates(event)
            if x is not None and y is not None:
                self.canvas.create_rectangle(
                    self.start_x * self.scale_factor + self.image_position[0],
                    self.start_y * self.scale_factor + self.image_position[1],
                    x * self.scale_factor + self.image_position[0],
                    y * self.scale_factor + self.image_position[1],
                    outline="red", tags="box"
                )

    def end_draw(self, event):
        x, y = self.get_image_coordinates(event)
        if x is not None and y is not None and self.start_x is not None and self.start_y is not None:
            x1, y1 = min(self.start_x, x), min(self.start_y, y)
            x2, y2 = max(self.start_x, x), max(self.start_y, y)

            self.update_bounding_box(x1, y1, x2, y2)

        self.start_x = None
        self.start_y = None

    def get_image_coordinates(self, event):
        x = (event.x - self.image_position[0]) / self.scale_factor
        y = (event.y - self.image_position[1]) / self.scale_factor

        img_height, img_width = self.image.shape[:2]

        if 0 <= x < img_width and 0 <= y < img_height:
            return int(x), int(y)
        return None, None

    def update_bounding_box(self, x1, y1, x2, y2):
        img_height, img_width = self.image.shape[:2]
        voc_box = VOCBox(x1, y1, x2, y2, normalized=False)
        self.bounding_box = BoundingBox(voc_box, (img_height, img_width))
        self.update_entries()
        self.draw_bounding_box()

    def draw_bounding_box(self):
        if self.bounding_box:
            self.canvas.delete("box")
            voc = self.bounding_box.to_voc()
            self.canvas.create_rectangle(
                voc.xmin * self.scale_factor + self.image_position[0],
                voc.ymin * self.scale_factor + self.image_position[1],
                voc.xmax * self.scale_factor + self.image_position[0],
                voc.ymax * self.scale_factor + self.image_position[1],
                outline="red", tags="box"
            )

    def update_entries(self):
        if self.bounding_box:
            voc = self.bounding_box.to_voc()
            voc_norm = self.bounding_box.to_voc(normalized=True)
            coco = self.bounding_box.to_coco()
            coco_norm = self.bounding_box.to_coco(normalized=True)
            yolo = self.bounding_box.to_yolo(normalized=False)
            yolo_norm = self.bounding_box.to_yolo()

            self.update_entry_values(self.voc_entries,
                                     [voc.xmin, voc.ymin, voc.xmax, voc.ymax,
                                      voc_norm.xmin, voc_norm.ymin, voc_norm.xmax, voc_norm.ymax])

            self.update_entry_values(self.coco_entries,
                                     [coco.x, coco.y, coco.width, coco.height,
                                      coco_norm.x, coco_norm.y, coco_norm.width, coco_norm.height])

            self.update_entry_values(self.yolo_entries,
                                     [yolo.x_center, yolo.y_center, yolo.width, yolo.height,
                                      yolo_norm.x_center, yolo_norm.y_center, yolo_norm.width, yolo_norm.height])

    def update_entry_values(self, entries, values):
        for entry, value in zip(entries.values(), values):
            entry.delete(0, tk.END)
            entry.insert(0, f"{value:.4f}")

    def on_entry_change(self, event, format_name, field_name):
        try:
            value = float(event.widget.get())
            if "norm" in field_name and (value < 0 or value > 1):
                raise ValueError("Normalized values must be between 0 and 1")

            img_height, img_width = self.image.shape[:2]

            if format_name == "VOC":
                current_box = self.bounding_box.to_voc(normalized="norm" in field_name)
                fields = ["xmin", "ymin", "xmax", "ymax"]
                index = fields.index(field_name.replace("_norm", ""))
                values = [current_box.xmin, current_box.ymin, current_box.xmax, current_box.ymax]
                values[index] = value
                new_box = VOCBox(*values, normalized="norm" in field_name)

            elif format_name == "COCO":
                current_box = self.bounding_box.to_coco(normalized="norm" in field_name)
                fields = ["x", "y", "width", "height"]
                index = fields.index(field_name.replace("_norm", ""))
                values = [current_box.x, current_box.y, current_box.width, current_box.height]
                values[index] = value
                new_box = COCOBox(*values, normalized="norm" in field_name)

            elif format_name == "YOLO":
                current_box = self.bounding_box.to_yolo(normalized="norm" in field_name)
                fields = ["x_center", "y_center", "width", "height"]
                index = fields.index(field_name.replace("_norm", ""))
                values = [current_box.x_center, current_box.y_center, current_box.width, current_box.height]
                values[index] = value
                new_box = YOLOBox(*values, normalized="norm" in field_name)

            else:
                raise ValueError(f"Unknown format: {format_name}")

            self.bounding_box = BoundingBox(new_box, (img_height, img_width))
            self.update_entries()
            self.draw_bounding_box()

        except ValueError as e:
            print(f"Invalid input: {e}")
