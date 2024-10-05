import tkinter as tk
from utils import generate_random_color

class CartesianPlan(tk.Canvas):
    def __init__(self, master, listbox, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="white", highlightthickness=0)
        self.bind("<Configure>", self._on_resize)

        self.origin = None
        # Dictionary to store items (points and vectors) with their labels as keys
        self.items = {}

        # Store reference to the listbox
        self.listbox = listbox

    def _on_resize(self, event):
        self.update()
        self.origin = (self.winfo_width() / 2, self.winfo_height() / 2)
        self.draw_axes()
        self.redraw_items()

    def draw_axes(self):
        """Draws the x and y axes on the canvas."""
        self.delete("axes")
        width = self.winfo_width()
        height = self.winfo_height()

        # Draw x and y axes, respectively
        self.create_line(0, self.origin[1], width, self.origin[1], fill="black", tags="axes")
        self.create_line(self.origin[0], 0, self.origin[0], height, fill="black", tags="axes")

        # Draw grid points, lines, and labels with values ranging from -10 to 10 - It means 21 parts, because 0 is also included
        self.draw_grid_points(21)

    def draw_grid_points(self, divisions):
        """Draw points, lines, and coordinate values from -10 to 10 on the Cartesian plane."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Calculate the step size for x and y axes based on 21 parts - which means "how many pixels each coordinate will take"
        x_step = width // (divisions - 1)
        y_step = height // (divisions - 1)

        # Draw points, lines, and labels on the x-axis (-10 to 10)
        for i in range(-10, 11):  # Range from -10 to 10
            x = self.origin[0] + i * x_step
            # Draw vertical grid line
            self.create_line(x, 0, x, height, fill="lightgray", dash=(2, 2), tags="axes")
            # Draw a small point at the intersection with the x-axis
            self.create_oval(x - 2, self.origin[1] - 2, x + 2, self.origin[1] + 2, fill="black", tags="axes")
            # Add the label for the x coordinate, besides the (0, 0) coordinate
            if i != 0:
                self.create_text(x, self.origin[1] + 15, text=f"{i}", tags="axes")

        # Draw points, lines, and labels on the y-axis (-10 to 10)
        for i in range(-10, 11):  # Range from -10 to 10
            y = self.origin[1] - i * y_step
            # Draw horizontal grid line
            self.create_line(0, y, width, y, fill="lightgray", dash=(2, 2), tags="axes")
            # Draw a small point at the intersection with the y-axis
            self.create_oval(self.origin[0] - 2, y - 2, self.origin[0] + 2, y + 2, fill="black", tags="axes")
            # Add the label for the y coordinate, besides the (0, 0) coordinate
            if i != 0:
                self.create_text(self.origin[0] + 15, y, text=f"{i}", tags="axes")

    def draw_point(self, x, y, label):
        """Draws a point on the Cartesian plane given the Cartesian coordinates and a label."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Calculate the pixel coordinates based on the canvas size and origin (20 steps are considered for the range -10 to 10)
        x_pixel = self.origin[0] + (x * (width // 20))
        y_pixel = self.origin[1] - (y * (height // 20))  # Invert y-axis for Cartesian plane

        color = generate_random_color()

        # Store the point in a dictionary with logical coordinates and color
        # The -5 and +5 are to ensure the point is centered on the pixel coordinates (there's a circle with a radius of 5)
        point_id = self.create_oval(x_pixel - 5, y_pixel - 5, x_pixel + 5, y_pixel + 5, fill=color, tags="items")
        text_id = self.create_text(x_pixel + 10, y_pixel - 10, text=label, tags="items")
        self.items[label] = {"type": "point", "coords": (x, y), "graphic": (point_id, text_id), "color": color}

    def draw_vector(self, x, y, label):
        """Draws a vector from the origin (0,0) to the specified coordinates with an arrow and a label."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Pixel coordinates for (0,0) and (x,y) - 20 steps are considered for the range -10 to 10
        x_pixel = self.origin[0] + (x * (width // 20))
        y_pixel = self.origin[1] - (y * (height // 20))  # Invert y-axis for Cartesian plane

        color = generate_random_color()

        line_id = self.create_line(self.origin[0], self.origin[1], x_pixel, y_pixel, fill=color, arrow=tk.LAST, width=2,
                                   tags="vector")

        # Add the label at the end of the vector
        text_id = self.create_text(x_pixel + 10, y_pixel - 10, text=label, fill=color, font=("Arial", 12, "bold"),
                                   tags="vector")

        # Store the vector (line and label) in the items dictionary with logical coordinates and color
        self.items[label] = {"type": "vector", "coords": (x, y), "graphic": (line_id, text_id), "color": color}

    def draw_vector_between_points(self, start_coords, end_coords, start_label, end_label, label):
        """Draws a vector from one point to another based on their coordinates, with the label dislocated based on orientation."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Get pixel coordinates for the start and end points
        start_x_pixel = self.origin[0] + (start_coords[0] * (width // 20))
        start_y_pixel = self.origin[1] - (start_coords[1] * (height // 20))
        end_x_pixel = self.origin[0] + (end_coords[0] * (width // 20))
        end_y_pixel = self.origin[1] - (end_coords[1] * (height // 20))

        # Calculate the midpoint for the label - the label is placed slightly dislocated from the middle of the vector, so it does not mix with the vector
        mid_x_pixel = (start_x_pixel + end_x_pixel) / 2
        mid_y_pixel = (start_y_pixel + end_y_pixel) / 2

        color = generate_random_color()

        # Draw the vector (line from start to end)
        line_id = self.create_line(start_x_pixel, start_y_pixel, end_x_pixel, end_y_pixel, fill=color, arrow=tk.LAST,
                                   width=2,
                                   tags="vector")

        # Determine the dislocation based on the orientation of the vector
        if abs(start_x_pixel - end_x_pixel) > abs(start_y_pixel - end_y_pixel):
            text_id = self.create_text(mid_x_pixel, mid_y_pixel - 10, text=label, fill=color,
                                       font=("Arial", 12, "bold"),
                                       tags="vector")
        elif abs(start_y_pixel - end_y_pixel) > abs(start_x_pixel - end_x_pixel):
            text_id = self.create_text(mid_x_pixel + 10, mid_y_pixel, text=label, fill=color,
                                       font=("Arial", 12, "bold"),
                                       tags="vector")
        else:
            text_id = self.create_text(mid_x_pixel + 10, mid_y_pixel - 10, text=label, fill=color,
                                       font=("Arial", 12, "bold"),
                                       tags="vector")

        # Store the vector (line and label) in the items dictionary, along with its start and end points
        self.items[label] = {
            "type": "vector",
            "coords": (start_coords, end_coords),
            "points": (start_label, end_label),  # Used to identify the points involved in the vector
            "graphic": (line_id, text_id),
            "color": color
        }

    def redraw_items(self):
        """Redraw all items (points and vectors) based on the new canvas size."""
        self.delete("items")  # Clear all existing items (points, vectors) from the canvas

        for label, item in self.items.items():
            x, y = item["coords"]
            color = item["color"]

            # Check if it's a point or a vector and redraw accordingly
            if item["type"] == "point":
                self.redraw_point(x, y, label, color)
            elif item["type"] == "vector":
                if "points" in item:
                    start_coords, end_coords = item["coords"]
                    start_label, end_label = item["points"]
                    self.redraw_vector_between_points(start_coords, end_coords, label, color)
                else:
                    self.redraw_vector(x, y, label, color)

    def redraw_point(self, x, y, label, color):
        """Redraws a point at the given coordinates using the stored color."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Calculate the pixel coordinates based on the canvas size and origin
        x_pixel = self.origin[0] + (x * (width // 20))
        y_pixel = self.origin[1] - (y * (height // 20))

        # Redraw the point and label using the stored color
        point_id = self.create_oval(x_pixel - 5, y_pixel - 5, x_pixel + 5, y_pixel + 5, fill=color, tags="items")
        text_id = self.create_text(x_pixel + 10, y_pixel - 10, text=label, tags="items")
        self.items[label]["graphic"] = (point_id, text_id)

    def redraw_vector(self, x, y, label, color):
        """Redraws a vector from the origin (0,0) to the specified coordinates using the stored color."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Pixel coordinates for (0,0) and (x,y)
        x_pixel = self.origin[0] + (x * (width // 20))
        y_pixel = self.origin[1] - (y * (height // 20))  # Invert y-axis for Cartesian plane

        # Delete the old vector if it exists
        if label in self.items:
            line_id, text_id = self.items[label]["graphic"]
            self.delete(line_id)
            self.delete(text_id)

        # Draw the vector (line from origin to (x, y))
        line_id = self.create_line(self.origin[0], self.origin[1], x_pixel, y_pixel, fill=color, arrow=tk.LAST, width=2,
                                   tags="items")

        # Add the label at the end of the vector
        text_id = self.create_text(x_pixel + 10, y_pixel - 10, text=label, fill=color, font=("Arial", 12, "bold"),
                                   tags="items")

        # Store the vector (line and label) in the items dictionary with logical coordinates and color
        self.items[label] = {"type": "vector", "coords": (x, y), "graphic": (line_id, text_id), "color": color}

    def redraw_vector_between_points(self, start_coords, end_coords, label, color):
        """Redraws a vector from one point to another based on their coordinates."""
        width = self.winfo_width()
        height = self.winfo_height()

        # Get pixel coordinates for the start and end points
        start_x_pixel = self.origin[0] + (start_coords[0] * (width // 20))
        start_y_pixel = self.origin[1] - (start_coords[1] * (height // 20))
        end_x_pixel = self.origin[0] + (end_coords[0] * (width // 20))
        end_y_pixel = self.origin[1] - (end_coords[1] * (height // 20))

        # Delete the old vector if it exists
        if label in self.items:
            line_id, text_id = self.items[label]["graphic"]
            self.delete(line_id)
            self.delete(text_id)

        # Calculate the midpoint for the label
        mid_x_pixel = (start_x_pixel + end_x_pixel) / 2
        mid_y_pixel = (start_y_pixel + end_y_pixel) / 2

        # Draw the vector (line from start to end)
        line_id = self.create_line(start_x_pixel, start_y_pixel, end_x_pixel, end_y_pixel, fill=color, arrow=tk.LAST,
                                   width=2, tags="items")

        # Determine the dislocation based on the orientation of the vector
        if abs(start_x_pixel - end_x_pixel) > abs(start_y_pixel - end_y_pixel):
            text_id = self.create_text(mid_x_pixel, mid_y_pixel - 10, text=label, fill=color,
                                       font=("Arial", 12, "bold"), tags="items")
        elif abs(start_y_pixel - end_y_pixel) > abs(start_x_pixel - end_x_pixel):
            text_id = self.create_text(mid_x_pixel + 10, mid_y_pixel, text=label, fill=color,
                                       font=("Arial", 12, "bold"), tags="items")
        else:
            text_id = self.create_text(mid_x_pixel + 10, mid_y_pixel - 10, text=label, fill=color,
                                       font=("Arial", 12, "bold"), tags="items")

        # Store the vector (line and label) in the items dictionary, along with its start and end points
        self.items[label]["graphic"] = (line_id, text_id)

    def delete_point(self, label):
        """Deletes a point from the canvas and also deletes any vectors that are using this point."""
        if label in self.items:
            # First, delete the point itself
            point_id, text_id = self.items[label]["graphic"]
            self.delete(point_id)
            self.delete(text_id)
            del self.items[label]

            # Now check for any vectors that involve this point
            vectors_to_delete = [
                vec_label for vec_label, vec_data in self.items.items()
                if vec_data["type"] == "vector" and (
                        ("points" in vec_data and (label == vec_data["points"][0] or label == vec_data["points"][
                            1]))  # Vectors between points
                        or ("points" not in vec_data and vec_data["coords"] == (0, 0))  # Vector from origin
                )
            ]

            # Delete all vectors associated with this point
            for vec_label in vectors_to_delete:
                self.delete_vector(vec_label)

            # Collect indices of items to delete in the listbox related to the point (exact match only)
            items_to_delete = []
            for i in range(self.listbox.size()):
                item_info = self.listbox.get(i)
                # Match the point and ensure it's not a vector
                if f"{label}(" in item_info and 'vector' not in item_info:
                    items_to_delete.append(i)

            # Perform deletion in reverse order to avoid shifting issues
            for index in sorted(items_to_delete, reverse=True):
                self.listbox.delete(index)

    def delete_vector(self, label):
        """Deletes a vector from the canvas and removes it from the listbox."""
        if label in self.items:
            vector_id, text_id = self.items[label]["graphic"]
            self.delete(vector_id)
            self.delete(text_id)
            del self.items[label]

            # Now delete the vector from the listbox
            items_to_delete = []
            for i in range(self.listbox.size()):
                item_info = self.listbox.get(i)
                if label in item_info and 'vector' in item_info:
                    items_to_delete.append(i)

            # Perform deletion after iteration
            for index in reversed(items_to_delete):
                self.listbox.delete(index)