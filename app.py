import tkinter as tk
import re
from cartesian_plan import CartesianPlan
from utils import generate_random_color


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vectors Race")

        # Input box for entering items
        self.input_frame = tk.Frame(self)
        self.input_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

        self.label = tk.Label(self.input_frame, text="Enter Item:")
        self.label.pack(pady=10)

        # Entry box for input (where the user enters the point or vector)
        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(pady=10)

        # Button to draw the item based on the input above
        self.draw_button = tk.Button(self.input_frame, text="Draw Item", command=self.draw_point_from_input)
        self.draw_button.pack(pady=10)

        # Bind the Enter key to trigger draw_point_from_input, which means pressing Enter will draw the item as if the button was clicked
        self.input_entry.bind("<Return>", lambda event: self.draw_point_from_input())

        # Listbox to display points
        self.point_list_label = tk.Label(self.input_frame, text="Items List:")
        self.point_list_label.pack(pady=10)

        # Where the items are being displayed
        self.point_listbox = tk.Listbox(self.input_frame)
        self.point_listbox.pack(pady=10)

        self.delete_button = tk.Button(self.input_frame, text="Delete Selected Item", command=self.delete_item)
        self.delete_button.pack(pady=10)

        # Create the canvas for the Cartesian plane
        self.cartesian_plane = CartesianPlan(self, self.point_listbox)
        self.cartesian_plane.place(relx=0, rely=0, relwidth=0.8, relheight=1)

        # Label to display error messages
        self.error_label = tk.Label(self.input_frame, text="", fg="red")
        self.error_label.pack(pady=10)

    def draw_point_from_input(self):
        """
        Handles drawing the point or vector based on the input from the entry box.
        The formats are:
            - Point: Letter in uppercase followed by '(' and the x and y coordinates separated by a comma and closed with ')'. Example: A(0,1)
            - Vector from origin: Letter in lowercase followed by the x and y coordinates separated by a comma. Example: u(1,3)
            - Vector between two points: Two uppercase letters representing the points. The vector will be from the first point to the second point. Example: AB
        """
        input_text = self.input_entry.get()

        # Check if the input is for two existing points (e.g., "AB")
        if re.match(r"^[A-Z]{2}$", input_text):
            start_label = input_text[0]
            end_label = input_text[1]

            # Ensure both points exist
            if start_label in self.cartesian_plane.items and end_label in self.cartesian_plane.items:
                # Get the coordinates of both points
                start_coords = self.cartesian_plane.items[start_label]["coords"]
                end_coords = self.cartesian_plane.items[end_label]["coords"]

                # Draw the vector from start to end
                self.cartesian_plane.draw_vector_between_points(start_coords, end_coords, start_label, end_label,
                                                                input_text)
                self.point_listbox.insert(tk.END, f"{input_text} vector from {start_label} to {end_label}")
                self.error_label.config(text="")  # Clear any previous error
            else:
                self.error_label.config(text=f"Error: Points {start_label} and/or {end_label} do not exist.")
            return

        # Check if the input is for a vector from the origin (e.g., "u(1,3)") or a point (e.g., "A(0,1)")
        match = re.match(r"([A-Za-z])\((-?\d+),\s*(-?\d+)\)", input_text)
        if match:
            label = match.group(1)
            x = int(match.group(2))
            y = int(match.group(3))

            # Check if the label already exists for both points and vectors
            if label in self.cartesian_plane.items:
                self.error_label.config(text=f"Error: Label {label} already exists.")
                return

            # Ensure that the coordinates are within the predefined range
            if -10 <= x <= 10 and -10 <= y <= 10:
                # Checks if it is a point or a vector to be drawn
                if label.isupper():
                    self.cartesian_plane.draw_point(x, y, label)
                    # Add point's notation to the listbox
                    self.point_listbox.insert(tk.END, f"{label}({x},{y})")
                else:
                    self.cartesian_plane.draw_vector(x, y, label)
                    # Add vector's notation to the listbox
                    self.point_listbox.insert(tk.END, f"{label} vector (0,0) to ({x},{y})")

                # Clear the input box after drawing the point or vector in case of any errors present
                self.error_label.config(text="")
            else:
                self.error_label.config(text="Coordinates out of range (-10 to 10).")
        else:
            self.error_label.config(text="Invalid input format. Please enter in the format A(0,1), u(1,3), or AB.")

    def delete_item(self):
        """
        Deletes the selected point or vector from the canvas and the list.
        The item deleted can be a point or a vector, and to delete just select the item from the listbox and click on the delete button.
        If the item is:
            - A vector (of any kind): only the item will be deleted
            - A point: if the point is deleted, all vectors that involve this point will also be deleted
        """
        selected_index = self.point_listbox.curselection()
        if selected_index:
            item_info = self.point_listbox.get(selected_index)

            # Extract the label from the item_info and check if it's a point or a vector
            if 'vector' in item_info:
                label = item_info.split(' ')[0]
                self.cartesian_plane.delete_vector(label)
            else:
                label = item_info.split('(')[0]

                # Create a list of vectors to delete that involve this point
                vectors_to_delete = [
                    vec_label for vec_label, vec_data in list(self.cartesian_plane.items.items())
                    if vec_data["type"] == "vector" and
                       (
                               "points" in vec_data and label in vec_data["points"]  # Vectors between points
                               or "points" not in vec_data and vec_data["coords"] == (0, 0)  # Vector from origin
                       )
                ]

                # Delete the vectors that involve this point
                for vec_label in vectors_to_delete:
                    self.cartesian_plane.delete_vector(vec_label)

                self.cartesian_plane.delete_point(label)

            # Update the listbox after deleting the item(s)
            self.update_listbox()

            self.error_label.config(text="")

    def update_listbox(self):
        """Updates the listbox to show the current points and vectors."""
        self.point_listbox.delete(0, tk.END)

        # Insert all points and vectors into the listbox again
        for label, item in self.cartesian_plane.items.items():
            if item["type"] == "point":
                x, y = item["coords"]
                self.point_listbox.insert(tk.END, f"{label}({x},{y})")
            elif item["type"] == "vector":
                if "points" in item:
                    # Vectors between two points
                    start_label, end_label = item["points"]
                    self.point_listbox.insert(tk.END, f"{label} vector from {start_label} to {end_label}")
                else:
                    # Vector from the origin (0,0)
                    x, y = item["coords"]
                    self.point_listbox.insert(tk.END, f"{label} vector (0,0) to ({x},{y})")


if __name__ == "__main__":
    app = App()
    app.geometry("1000x600")
    app.mainloop()
