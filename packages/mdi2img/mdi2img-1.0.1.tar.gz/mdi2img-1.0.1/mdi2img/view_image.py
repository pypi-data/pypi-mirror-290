"""
File in charge of displaying a converted image
"""

import os
import tkinter as tk
from platform import system
from window_asset_tkinter.window_tools import WindowTools as WT
from window_asset_tkinter.calculate_window_position import CalculateWindowPosition as CWP


class ViewImage(WT):
    """
    The class in charge of displaying the image
    """

    def __init__(self, parent_window: tk.Tk = None, width: int = 500, height: int = 400, success: int = 0, error: int = 1) -> None:
        # Status codes
        self.success = success
        self.error = error
        self.error_message = "Error: Path does not exist"
        # Saving width and height of the window
        self.width = width
        self.height = height
        # Creating parent window if it does not exist
        if parent_window is None:
            self.parent_window = self._create_parent_window()
        else:
            self.parent_window = parent_window
        self.host_dimensions = self.get_current_host_screen_dimensions(
            self.parent_window
        )
        # Initialising the window position calculator
        self.cwp = CWP(
            self.host_dimensions["width"],
            self.host_dimensions["height"],
            width,
            height
        )
        # Image tracking
        self._images_buffer = list()
        self.image_data = list()
        self.max_images = 0
        self.current_image = 0
        # Window position
        self.x_offset = 0
        self.y_offset = 0
        # GUI config
        self.bg = "white"
        self.fg = "black"
        # Title section
        self.title_label = tk.Label
        # image_viewer section
        self.image_viewer = tk.Label
        self.image_viewer_error = tk.Label
        self.has_been_forgotten = False
        # button_prev section
        self.button_prev = tk.Button
        # button_next section
        self.button_next = tk.Button
        # button_open_in_viewer section
        self.button_open_in_viewer = tk.Button
        # The image counter
        self.image_count = tk.Label

    def _create_parent_window(self) -> tk.Tk:
        """
        Create the parent window
        :return: The parent window
        """
        window = tk.Tk()
        window.withdraw()
        return window

    def _load_image(self, image_path: str, width: int, height: int) -> dict:
        """
        Load the image into memory
        :param image_path: The path to the image to load
        :return: The image node

        raw_content:
            * "img": <image_instance:obj>
            * "width": <width:int>
            * "height": <height:int>
            * "path": <image_path:str>
            * "name": <image_name:str>
        when error:
            * "name": <the_name:str>
            * "error": <the_error:str>  
        """
        if os.path.exists(image_path) is False:
            path_message = {
                "name": image_path,
                "error": self.error_message
            }
            self._images_buffer.append(self.error_message)
            self.image_data.append(path_message)
            return path_message
        data = self.load_image(
            image_path=image_path,
            width=width,
            height=height
        )
        if "img" in data:
            current_name = image_path.replace("\\", "/")
            current_name = current_name.split("/")[-1]
            self._images_buffer.append(data["img"])
            node = {
                "img": data["img"],
                "width": width,
                "height": height,
                "path": image_path,
                "name": current_name
            }
            self.image_data.append(node)
            return node
        else:
            node = {
                "name": image_path,
                "error": data["err_message"]
            }
            self._images_buffer.append(data["err_message"])
            self.image_data.append(node)
            return node

    def _load_images(self, image_paths: list[str], width: int, height: int) -> None:
        """
        Load multiple images into memory
        :param image_paths: The paths to the images to load
        :return: None
        """
        for index, item in enumerate(image_paths):
            self._load_image(item, width, height)
            self.max_images = index

    def _update_current_image_displayed(self) -> None:
        """
        Update the image displayed
        """
        if len(self.image_data) > 0 and self.current_image >= len(self.image_data):
            self.current_image = 0
        if isinstance(self._images_buffer[self.current_image], str) is True:
            self.image_viewer.pack_forget()
            self.button_open_in_viewer.config(state=tk.DISABLED)
            self.image_viewer_error.config(
                text=self._images_buffer[self.current_image]
            )
            self.image_viewer_error.pack()
            self.has_been_forgotten = True
        else:
            if self.has_been_forgotten is True:
                self.image_viewer_error.pack_forget()
                self.image_viewer.pack()
                self.has_been_forgotten = False
            self.image_viewer.configure(
                image=self._images_buffer[self.current_image]
            )
            self.button_open_in_viewer.config(state=tk.NORMAL)

    def _update_current_image_index(self) -> None:
        """
        Update the index displayed of the current image 
        """
        self.image_count.config(
            text=f"Image {self.current_image + 1}/{self.max_images + 1}"
        )

    def _update_current_image_title(self) -> None:
        """
        Update the title of the current image
        """
        self.title_label.config(
            text=self.image_data[self.current_image]["name"]
        )

    def _previous_image(self, *args) -> None:
        """
        Display the previous image and it's name
        :return: None
        """
        if self.max_images == 0:
            self.image_viewer.config(text="No images to display !")
            return
        if self.current_image > 0:
            self.current_image -= 1
        else:
            self.current_image = self.max_images
        self._update_current_image_displayed()
        self._update_current_image_title()
        self._update_current_image_index()

    def _next_image(self, *args) -> None:
        """
        Display the next image and it's name
        :return: None
        """
        if self.max_images == 0:
            self.image_viewer.config(text="No images to display !")
            return
        if self.current_image < self.max_images:
            self.current_image += 1
        else:
            self.current_image = 0
        self._update_current_image_displayed()
        self._update_current_image_title()
        self._update_current_image_index()

    def hl_swap(self, item1: any, item2: any) -> list[any, any]:
        """
        Swap the values of two items
        :param item1: The first item
        :param item2: The second item
        :return: The items with their values swapped
        """
        return [item2, item1]

    def _open_in_system_viewer(self, *args) -> None:
        """
        Open the current image in the system viewer
        :return: None
        """
        current_image = self.current_image
        if self.current_image > self.max_images:
            current_image = 0
        if system() == "Windows":
            os.system(
                f"start {self.image_data[current_image]['path']}"
            )
        elif system() == "Linux":
            os.system(
                f"xdg-open {self.image_data[current_image]['path']}"
            )
        elif system() == "Darwin":
            os.system(
                f"open {self.image_data[current_image]['path']}"
            )

    def view(self, image_paths: list[str] | str, width: int = 0, height: int = 0) -> int:
        """
        Display an image
        :param image_path: The path to the image to display
        :return: The status of the display (success:int  or error:int)
        """
        debug = False
        button_width = 10
        object_height = 135
        if width < 1:
            width = self.width - (button_width*2)
        else:
            width -= button_width*2
        if height < 1:
            height = self.height

        if width >= self.width:
            width = self.hl_swap(width, self.width)
            self.width = width[-1]+1
            width = width[0]
        if height >= self.height:
            height = self.hl_swap(height, self.height)
            self.height = height[-1]+1
            height = height[0]

        if isinstance(image_paths, str) is True:
            self._load_image(image_paths, width, height)
        elif isinstance(image_paths, list) is True:
            self._load_images(image_paths, width, height)
        else:
            return self.error
        window_coord = self.cwp.calculate_center()
        child_window = self.init_plain_window(self.parent_window)
        self.init_window(
            child_window,
            title="MDI viewer",
            bkg="white",
            width=self.width + self.x_offset,
            height=self.height + self.y_offset+object_height,
            position_x=window_coord[0],
            position_y=window_coord[1],
            fullscreen=False,
            resizable=True
        )
        title_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="blue" if debug else self.bg,
            width=self.width,
            height=2,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )
        image_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="orange" if debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )
        footer_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="cyan" if debug else self.bg,
            width=self.width,
            height=2,
            position_x=0,
            position_y=0,
            side=tk.BOTTOM,
            fill=tk.X,
            anchor=tk.CENTER
        )
        button_frame = self.add_frame(
            child_window,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="purple" if debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.BOTTOM,
            fill=tk.NONE,
            anchor=tk.CENTER
        )

        button_prev_frame = self.add_frame(
            button_frame,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="green" if debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.LEFT,
            fill=tk.NONE,
            anchor=tk.CENTER
        )
        image_viewer_frame = self.add_frame(
            image_frame,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="yellow" if debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.LEFT,
            fill=tk.NONE,
            anchor=tk.CENTER
        )
        button_next_frame = self.add_frame(
            button_frame,
            borderwidth=0,
            relief=tk.FLAT,
            bkg="red" if debug else self.bg,
            width=self.width,
            height=self.height - self.y_offset,
            position_x=0,
            position_y=0,
            side=tk.LEFT,
            fill=tk.NONE,
            anchor=tk.CENTER
        )
        self.title_label = self.add_label(
            title_frame,
            text="MDI Viewer",
            bkg=self.bg,
            fg=self.fg,
            width=self.width,
            height=2,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )
        self.image_viewer = self.add_label(
            image_viewer_frame,
            text="",
            bkg=self.bg,
            fg=self.fg,
            width=width,
            height=height - self.y_offset,
            position_x=20,
            position_y=0,
            side=tk.TOP,
            fill=tk.NONE,
            anchor=tk.CENTER
        )
        self.image_viewer_error = self.add_label(
            image_viewer_frame,
            text="",
            bkg=self.bg,
            fg=self.fg,
            width=width,
            height=2,
            position_x=20,
            position_y=0,
            side=tk.TOP,
            fill=tk.NONE,
            anchor=tk.CENTER
        )
        self.button_prev = self.add_button(
            button_prev_frame,
            text="Previous",
            fg=self.fg,
            bkg=self.bg,
            side=tk.TOP,
            command=self._previous_image,
            width=button_width,
            height=1,
            position_x=0,
            position_y=0,
            anchor=tk.CENTER,
            fill=tk.NONE
        )
        self.button_next = self.add_button(
            button_next_frame,
            text="Next",
            fg=self.fg,
            bkg=self.bg,
            side=tk.LEFT,
            command=self._next_image,
            width=button_width,
            height=1,
            position_x=0,
            position_y=0,
            anchor=tk.CENTER,
            fill=tk.NONE
        )
        self.button_open_in_viewer = self.add_button(
            button_next_frame,
            text="Open in system viewer",
            fg=self.fg,
            bkg=self.bg,
            side=tk.LEFT,
            command=self._open_in_system_viewer,
            width=button_width*2,
            height=1,
            position_x=0,
            position_y=0,
            anchor=tk.CENTER,
            fill=tk.NONE
        )
        self.image_count = self.add_label(
            footer_frame,
            text=f"Image {self.current_image + 1}/{self.max_images + 1}",
            bkg=self.bg,
            fg=self.fg,
            width=self.width - (button_width*2),
            height=2,
            position_x=0,
            position_y=0,
            side=tk.TOP,
            fill=tk.X,
            anchor=tk.CENTER
        )
        self.add_watermark(
            window=footer_frame,
            side=tk.RIGHT,
            anchor=tk.E,
            bkg=self.bg,
            fg=self.fg
        )
        self._previous_image()
        self._next_image()
        child_window.wait_window()
        return True


if __name__ == "__main__":
    window_width = 500
    window_height = 400
    VII = ViewImage(
        None,
        width=window_width,
        height=window_height,
        success=0,
        error=1
    )
    ressources = list()
    image_path = "../sample_images"
    if os.path.exists(image_path) is True:
        images = os.listdir(image_path)
        for index, item in enumerate(images):
            ressources.append(os.path.join(image_path, item))
        ressources.append("Not a path")
    VII.view(
        ressources,
        window_width,
        window_height
    )
