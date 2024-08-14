"""
Module for Picta Image Processing's view layer.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk
import picta_common_layer
import picta_view_model

#Defining the tk Window must be done at beginning of script
#to stop double windows from opening
window = tk.Tk()
window.title("Apply Model to Image")
window.geometry("1400x750")

class PictaView():
    """
    View layer to handle all GUI operations for Picta Image Processing
    """
    original_image_display = tk.Label()
    segment_display = tk.Label()
    merged_image_display = tk.Label()
    not_merged = True
    progress_var = tk.DoubleVar()

    def __init__(self):
        self.picta_view_model = picta_view_model.PictaViewModelRoot(PictaTkCallback())

    def confirm(self):
        """Routine to check if MVVM layers are connected correctly."""
        print("View confirmed")
        self.picta_view_model.confirm()

    def file_load_model(self):
        """Functionality for File -> Load Model. 
        Enables functionality for the rest of the GUI 'File' options.
        """
        self.picta_view_model.get_keras_model_path()
        file_menu.entryconfig(0, state=tk.ACTIVE)
        file_menu.entryconfig(1, state=tk.ACTIVE)
        file_menu.entryconfig(2, state=tk.ACTIVE)
        file_menu.entryconfig(3, state=tk.ACTIVE)
        file_menu.entryconfig(4, state=tk.ACTIVE)
        file_menu.entryconfig(5, state=tk.ACTIVE)
        file_menu.entryconfig(6, state=tk.DISABLED)

    def pick_and_load_image_file(self, file_type):
        """Functionality for File -> Open .JPG File, and File -> Open .NEF File. 
        Displays image file to screen in a tk.Label.
        Inputs:
            file_type (string) : indicates whether the image file to open is a jpeg or nef file.
        """
        self.clear_screen()
        self.picta_view_model.set_image_file_path(file_type)
        self.picta_view_model.load_and_resize_image(
            window.winfo_width(), window.winfo_height(), file_type)
        label_selected_image_name.config(
            text='Selected: ' + self.picta_view_model.get_original_image_name())
        original_image_tk = ImageTk.PhotoImage(self.picta_view_model.get_resized_orginal_image())
        self.original_image_display = tk.Label(window, image=original_image_tk)
        self.original_image_display.image = original_image_tk
        self.original_image_display.grid(row=3, column=0, columnspan=1)
        button_apply_model['state'] = tk.ACTIVE
        button_next_image['state'] = tk.DISABLED
        button_previous_image['state'] = tk.DISABLED

    def display_segmentation(self):
        """Functionality for button_apply_model. 
        Displays the segmentation image in a tk.Label after it is generated."""
        self.segment_display.grid_forget()
        self.picta_view_model.create_and_load_segmentation(
            window.winfo_width(), window.winfo_height())
        segment_image_tk = ImageTk.PhotoImage(self.picta_view_model.get_resized_segmentation())
        self.segment_display = tk.Label(window, image=segment_image_tk)
        self.segment_display.image = segment_image_tk
        self.segment_display.grid(row=3, column=1)
        button_merge_images['state'] = tk.NORMAL
        button_save_segmented_area['state'] = tk.ACTIVE
        button_apply_model['state'] = tk.DISABLED
        button_pick_new_segmentation.grid(row=2, column= 1)
        button_pick_new_segmentation['state'] = tk.ACTIVE

    def load_files(self, file_type):
        """Functionality for File -> Process .NEF Files and File -> Procress .JPEG Files. 
        Let's the user pick which directories to load the NEF files 
        and subsequently where to save the segmentation images to.
        Inputs:
            file_type (string) : indicates whether loading jpegs or nefs
        """
        self.clear_screen()
        try:
            input_directory, output_directory = self.pick_input_and_output_directory(file_type)
            self.picta_view_model.set_input_directory(input_directory)
            self.picta_view_model.set_output_directory(output_directory)
            if file_type == 'nef':
                button_process_nef_directory['state'] = tk.ACTIVE
                label_selected_image_name.config(
                    text='Next click the \"Load NEF files\" button', font=('', '15'))
            else:
                button_process_jpeg_directory['state'] = tk.ACTIVE
                label_selected_image_name.config(
                    text='Next click the \"Load JPEG files\" button', font=('', '15'))
        except TypeError:
            print('Yeah it messed up')
            print(TypeError)
            label_selected_image_name.config(
                text='Error when picking directories, try again.', font=('', '15'))
            button_process_nef_directory['state'] = tk.DISABLED
            button_process_jpeg_directory['state'] = tk.DISABLED

    def pick_input_and_output_directory(self, file_type):
        """Routine for getting the directory of image files to process,
        and where to save the generated segmentation images.
        Inputs:
            file_type (String) : indicates whether jpegs or nefs are being dealt with
        Returns:
            input_directory (String) : the path to the directory with the image files.
            output_directory (String) : the path to the directory to save the segmentation images.
        """
        if file_type == 'nef':
            messagebox.showinfo('Instructions', 'Select the folder with your raw image .NEF files')
        else:
            messagebox.showinfo('Instructions', 'Select the folder with your .jpg image files')
        input_directory = filedialog.askdirectory()
        if input_directory:
            if file_type == 'nef':
                messagebox.showinfo(
                    'Instructions', 'Select which folder to output the generated JPEGs \
                    and segmentation images')
                output_directory = filedialog.askdirectory()
                if output_directory:
                    return input_directory, output_directory
            else:
                output_directory = input_directory
                return input_directory, output_directory

    def file_function_load_directory(self):
        """Functionality for File -> Load Directory.
        Takes a directory of images and segmentations
        and loads them into the program."""
        try:
            self.picta_view_model.set_output_directory(filedialog.askdirectory())
            self.picta_view_model.launch_load_directory(
                self.picta_view_model.get_output_directory())
            self.display_image_and_segmentation()
            button_next_image['state'] = tk.ACTIVE
            button_merge_images['state'] = tk.ACTIVE
        except TypeError as error:
            label_selected_image_name.config(
                text='Invalid directory selected, try again.', font=('', '15'))
            print('Error loading directory. Possibly no JPEGs or PNGs included \
                   in directory\n' + str(error))

    def display_image_and_segmentation(self):
        """Routine to launch model layer's method 'load_image_and_segmentation_in_conjunction'. 
        Then displays the loaded images and allows browsing through the images in the directory."""
        self.clear_screen()
        self.picta_view_model.launch_load_image_and_segmentation_in_conjunction(
            window.winfo_width(), window.winfo_height())
        label_selected_image_name.config(
            text='Viewing: ' + self.picta_view_model.get_original_image_name())
        original_image_tk = ImageTk.PhotoImage(self.picta_view_model.get_resized_orginal_image())
        self.original_image_display = tk.Label(window, image=original_image_tk)
        self.original_image_display.image = original_image_tk
        self.original_image_display.grid(row=3, column=0)
        segmentation_image_tk = ImageTk.PhotoImage(self.picta_view_model.get_resized_segmentation())
        self.segment_display = tk.Label(window, image=segmentation_image_tk)
        self.segment_display.image = segmentation_image_tk
        self.segment_display.grid(row=3, column=1)
        button_previous_image['state'] = tk.ACTIVE
        button_next_image['state'] = tk.ACTIVE
        button_pick_new_segmentation.grid(row=2, column= 1)
        button_pick_new_segmentation['state'] = tk.ACTIVE
        button_save_segmented_area['state'] = tk.ACTIVE
        button_merge_images['state'] = tk.ACTIVE

    def save_segmentation_image_file_function(self):
        """Functionality for File -> Save Segmentation. 
        Saves the currently displayed segmentation image to the chosen directory."""
        if self.picta_view_model.check_no_segment_loaded():
            messagebox.showerror('Error', 'No segmentation has been generated.')
        else:
            directory = filedialog.askdirectory()
            if directory:
                self.picta_view_model.launch_save_segmentation_image(directory)

    def display_previous_image(self):
        """Functionality for button_previous_image. Decrements the position of model layer's 
        index_of_image_lists if possible, then displays displays image and mask"""
        button_merge_images['state'] = tk.NORMAL
        button_next_image['state'] = tk.NORMAL
        if self.picta_view_model.get_index_of_image_lists() == 0:
            button_previous_image['state'] = tk.DISABLED
            return
        button_previous_image['state'] = tk.NORMAL
        self.picta_view_model.set_index_of_image_lists(
            self.picta_view_model.get_index_of_image_lists() - 1)
        self.display_image_and_segmentation()

    def display_next_image(self):
        """Functionality for button_next_image. Increments the position of model layer's 
        index_of_image_lists if possible, then displays displays image and mask"""
        button_merge_images['state'] = tk.NORMAL
        self.picta_view_model.set_index_of_image_lists(
            self.picta_view_model.get_index_of_image_lists() + 1)
        button_previous_image['state'] = tk.NORMAL
        if (
            self.picta_view_model.get_index_of_image_lists()
            >= self.picta_view_model.get_length_of_jpeg_list()
        ):
            button_next_image['state'] = tk.DISABLED
            self.picta_view_model.set_index_of_image_lists(
                self.picta_view_model.get_index_of_image_lists() - 1)
            return
        button_next_image['state'] = tk.NORMAL
        self.display_image_and_segmentation()

    def cancel_process_image(self):
        """Functionality for 'stop_button'. Signals to stop the thread applying
        the model to images in a directory by setting the model layer's member variable
        'cancel_apply_model_process_thread' to True"""
        self.picta_view_model.signal_cancel_apply_model_process_thread()

    def start_thread_for_process_image_files(self, file_type):
        """Functionality for button_process_jpeg_directory, and
        button_process_nef_directory. Calls the view model's launch thread function.
        Inputs:
            file_type (String) : indicates whether jpegs or nefs are being dealt with
        """
        self.picta_view_model.launch_thread_for_create_segmentations_from_image_directory(file_type)

    def process_image_files_in_directory(self, file_type):
        """Routine to display progress bar and cancel button, and then subsequently
        removes them when the routine finishes. Launches the model layer's routine
        'create_segmentations_from_image_directory', displays how many images had the
        keras model applied to them, and finally displays the images that were processed."""
        button_process_jpeg_directory['state'] = tk.DISABLED
        button_process_nef_directory['state'] = tk.DISABLED
        progress_bar = ttk.Progressbar(window, variable=self.progress_var, maximum=100, length=250)
        progress_bar.place(relx=0.40, rely=0.45)
        stop_button = tk.Button(window, text='Cancel', command=self.cancel_process_image)
        stop_button.place(relx=0.47, rely=0.49)
        files_used = (
            self.picta_view_model.launch_create_segmentations_from_image_directory(
                file_type, view_layer_common))
        progress_bar.place_forget()
        stop_button.place_forget()
        messagebox.showinfo('Info', 'Wrote ' + str(files_used) + ' files \
                             to ' + self.picta_view_model.get_output_directory())
        self.picta_view_model.launch_load_directory(
            self.picta_view_model.get_input_directory())
        self.display_image_and_segmentation()
        button_next_image['state'] = tk.ACTIVE
        button_merge_images['state'] = tk.ACTIVE
        button_merge_images['state'] = tk.ACTIVE

    def merge_images_display(self):
        """Functionality for button_merge_images. Overlays the 
        segmentation image over the original image through the use of PIL Image.blend()"""
        if self.not_merged:
            self.original_image_display.grid_forget()
            self.picta_view_model.launch_create_merged_image(
                window.winfo_width(), window.winfo_height())
            merged_image_tk = ImageTk.PhotoImage(self.picta_view_model.get_resized_merged_image())
            self.merged_image_display = tk.Label(window, image=merged_image_tk)
            self.merged_image_display.image = merged_image_tk
            self.merged_image_display.grid(row=3, column=0)
            self.not_merged = False
        else:
            self.merged_image_display.grid_forget()
            self.original_image_display.grid(row=3, column=0, columnspan=1)
            self.segment_display.grid(row=3, column=1)
            self.not_merged = True

    def save_segmented_area(self):
        """Functionality for button_save_segmented_area. Saves the area
        of the original image that is occupied by the segmentation, 
        then displays the next image in the directory"""
        self.picta_view_model.launch_get_segmented_area_on_original_image_and_save_segmentation()
        self.display_next_image()

    def clear_screen(self):
        """Removes the labels containing images and sets the screen back to a neutral state"""
        self.original_image_display.grid_forget()
        self.segment_display.grid_forget()
        self.merged_image_display.grid_forget()
        button_pick_new_segmentation.grid_forget()
        button_apply_model['state'] = tk.DISABLED
        button_pick_new_segmentation['state'] = tk.DISABLED
        button_next_image['state'] = tk.DISABLED
        button_previous_image['state'] = tk.DISABLED
        button_save_segmented_area['state'] = tk.DISABLED
        button_process_jpeg_directory['state'] = tk.DISABLED
        button_merge_images['state'] = tk.DISABLED

class PictaTkCallback(picta_view_model.PictaCallbacks):
    """Contains all routines specific to the Tkinter library
    that will be used in the View Model layer.
    """
    def request_user_file_selection(self, file_type):
        """Opens tkinter's file browser to search for specified file types.
        Inputs:
            file_type (string) : file extension to allow choosable by the file browser
        Returns:
            A string containing the path to the selected file
        """
        return filedialog.askopenfilename(filetypes=[(file_type + ' files', '*.' + file_type)])

    def get_window_dimensions(self):
        """Process to send window dimensions to the view model layer"""
        return window.winfo_width(), window.winfo_height()

    def launch_seperate_thread_for_gui_function(self, file_type):
        """Process to launch function process_image_files_in_directory
        in a seperate thread from the view model layer"""
        view.process_image_files_in_directory(file_type)

class CommonLayerControllerTk(picta_common_layer.CommonLayer):
    """A declaration of abstract class CommonLayer. Used to send """
    def __init__(self):
        self.tk_window = window
        self.progress_var = view.progress_var

    def update_gui_progress_bar(self, percent_progress, display_message):
        """Routine to update the progress of a tkinter ttk.ProgressBar
        Inputs:
            percent_progress (int) : Percentage of how many tasks have been completed 
                in accordance to total number of tasks to complete in the routine. 
        """
        self.progress_var.set(percent_progress)
        window.update_idletasks()

view = PictaView()
view.confirm()

view_layer_common = CommonLayerControllerTk()

label_selected_image_name = tk.Label(window, text='', padx=5, pady=5)
label_selected_image_name.grid(row=2)

#---All menu and interface buttons---#
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="Open .JPG File", command=lambda:view.pick_and_load_image_file('jpg'))
file_menu.add_command(label='Open .NEF File', command=lambda:view.pick_and_load_image_file('nef'))
file_menu.add_command(label='Process .NEF Files', command=lambda:view.load_files('nef'))
file_menu.add_command(label='Process .JPG Files', command=lambda:view.load_files('jpeg'))
file_menu.add_command(label='Load Directory', command=view.file_function_load_directory)
file_menu.add_command(label="Save Segmentation", command=view.save_segmentation_image_file_function)
file_menu.add_command(label='Load Model', command=view.file_load_model)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.entryconfig(0, state=tk.DISABLED)
file_menu.entryconfig(1, state=tk.DISABLED)
file_menu.entryconfig(2, state=tk.DISABLED)
file_menu.entryconfig(3, state=tk.DISABLED)
file_menu.entryconfig(4, state=tk.DISABLED)
file_menu.entryconfig(5, state=tk.DISABLED)

button_previous_image = tk.Button(
    window, text='<- Previous', command=view.display_previous_image, state=tk.DISABLED)
button_previous_image.place(relx=0.4, rely=0.75)

button_next_image = tk.Button(
    window, text='Next ->', command=view.display_next_image, state=tk.DISABLED)
button_next_image.place(relx=0.54, rely=0.75)

button_apply_model = tk.Button(
    window, text='Create Segmentation', command=view.display_segmentation, state=tk.DISABLED)
button_apply_model.place(relx=0.24, rely=0.83)

button_process_nef_directory = tk.Button(
    window, text='Load NEF files', command=lambda:view.start_thread_for_process_image_files('nef'),
    state=tk.DISABLED)
button_process_nef_directory.place(relx=0.4, rely=0.83)

button_process_jpeg_directory = tk.Button(
    window, text='Load JPEG files', command=lambda:view.start_thread_for_process_image_files('jpg'),
    state=tk.DISABLED)
button_process_jpeg_directory.place(relx=0.51, rely=0.83)

button_merge_images = tk.Button(
    window, text="Display Merged", command=view.merge_images_display, state=tk.DISABLED)
button_merge_images.place(relx=0.64, rely=0.83)

button_pick_new_segmentation = tk.Button(
    window, text='Try Different Segmentation', command='') #view.pick_new_segmentation

button_save_segmented_area =  tk.Button(
    window, text='Save Segmented Area', command=view.save_segmented_area, state=tk.DISABLED)
button_save_segmented_area.place(relx=0.64, rely=0.75)

window.config(menu=menu_bar)
window.mainloop()
