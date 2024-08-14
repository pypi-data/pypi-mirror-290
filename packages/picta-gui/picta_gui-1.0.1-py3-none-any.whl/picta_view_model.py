"""
Module for Picta Image Processing's view model layer.
"""
from abc import ABC, abstractmethod
import threading
import picta_image_model

class PictaCallbacks(ABC):
    """Abstract class for handling GUI functions."""
    @abstractmethod
    def request_user_file_selection(self, file_type):
        """Launches GUI's file selection operation
        Inputs:
            file_type (string) : file extension type to allow selectable
        """

    @abstractmethod
    def get_window_dimensions(self):
        """Obtains the dimensions (width x height) of the GUI's window screen."""

    @abstractmethod
    def launch_seperate_thread_for_gui_function(self, file_type):
        """Opens a new thread to allow launching concurrent GUI functions"""

class PictaViewModelRoot():
    """
    View Model layer class to handle operations between Picta View layer and Picta Model Layer.
    """
    def __init__(self, callbacks):
        self.callbacks = callbacks
        self.__image_model_root = picta_image_model.PictaImageModelRoot()

    def confirm(self):
        """Routine to check if MVVM layers are connected correctly"""
        print('View model root confirmed')
        if self.callbacks is not None:
            print('Callbacks set')
        self.__image_model_root.confirm()

    def get_keras_model_path(self):
        """Routine to find path to keras model and send path to model layer"""
        keras_model_path = self.callbacks.request_user_file_selection('keras')
        self.__image_model_root.set_keras_model(keras_model_path)

    def set_image_file_path(self, file_type):
        """Sets the model layer's member variable 'image_file_path'
        Inputs:
            file_type (string) : indicates the type of file to show in the file browser. 
                Currently can be jpg or nef.
        """
        self.__image_model_root.image_file_path = (
            self.callbacks.request_user_file_selection(file_type))

    def launch_thread_for_create_segmentations_from_image_directory(self, file_type):
        """
        Routine to launch the view layer's routine 
        'target_thread_for_process_image_files_in_directory'
        and subsequently the model layer's routine 
        'create_segmentations_from_image_directory' in a seperate thread.
        Makes the routines cancellable.
        """
        new_thread = threading.Thread(
            target=lambda:self.callbacks.launch_seperate_thread_for_gui_function(file_type))
        new_thread.start()

    def get_original_image_name(self):
        """Routine to send the model layer's original image file name
        to the view layer.

        Returns:
            __image_model_root.image_file_name (string) : the file name
                of the displayed image
        """
        return self.__image_model_root.image_file_name

    def get_resized_orginal_image(self):
        """Routine to send the model layer's resized_original_image
        back to the view layer.
        Returns:
            The resized version of the original image to fit the
            GUI screen, a PIL.Image object
        """
        return self.__image_model_root.resized_original_image

    def get_resized_segmentation(self):
        """Routine to send the model layer's resized_segment_image
        back to the view layer.
        Returns:
            The resized segmentation image to fit the GUI screen,
            a PIL.Image object
        """
        return self.__image_model_root.resized_segment_image

    def get_resized_merged_image(self):
        """Routine to send the model layer's resized_segment_image
        back to the view layer.
        Returns:
            The resized merged image to fit the GUI screen,
            a PIL.Image object
        """
        return self.__image_model_root.resized_merged_image

    def get_output_directory(self):
        """Routine to send the model layer's output_directory
        back to the view layer.
        Returns:
            __image_model_root.output_directory (string) : path
                to the directory conating the original images and their
                corresponding segmentation
        """
        return self.__image_model_root.output_directory

    def get_input_directory(self):
        """Routine to send the model layer's input_directory
        back to the view layer.
        Returns:
            __image_model_root.input_directory (string) : path
                to the directory containing the original images
        """
        return self.__image_model_root.input_directory

    def get_length_of_jpeg_list(self):
        """Sends the length of the model layer variable jpeg_list
        to the view layer"""
        return len(self.__image_model_root.jpeg_list)

    def get_index_of_image_lists(self):
        """Routine to send the model layer's index_of_image_lists variable
        to the view layer"""
        return self.__image_model_root.index_of_image_lists

    def set_index_of_image_lists(self, new_index):
        """Routine to change the index_of_image_lists variable
        Inputs:
            new_index(int) : the new value to set index_of_image_lists to.
                Will either increase or decrease by 1. 
        """
        self.__image_model_root.index_of_image_lists = new_index

    def check_no_segment_loaded(self):
        """Returns the model layer's variable 'no_segment_loaded' to see if a
        segmentation image has been generated"""
        return self.__image_model_root.no_segment_loaded

    def set_input_directory(self, input_directory):
        """Routine to set the model layer's input_directory member variable
        from the view layer
        Inputs:
            input_directory (string) : path to the directory containing
                image files
        """
        self.__image_model_root.input_directory = input_directory

    def set_output_directory(self, output_directory):
        """Routine to set the model layer's output_directory member variable
        from the view layer
        Inputs:
            input_directory (string) : path to which directory segmentation
                images will be saved to
        """
        self.__image_model_root.output_directory = output_directory

    def signal_cancel_apply_model_process_thread(self):
        """Sets the model layer's 'cancel_apply_model_process_thread' variable
        to true to end the thread applying the model to the image"""
        self.__image_model_root.cancel_apply_model_process_thread = True

    def load_and_resize_image(self, window_width, window_height, file_type):
        """Routine to pass the GUI screen's dimensions to the model layer for
        resizing the image to fit the GUI screen.
        Inputs:
            window_width (int) : the width of the GUI screen
            window_height (int) : the height of the GUI screen
        """
        self.__image_model_root.load_original_image(window_width, window_height, file_type)

    def create_and_load_segmentation(self, window_width, window_height):
        """Routine to pass the GUI screen's dimensions to the model layer for
        resizing the generated segmentation image
        Inputs:
            window_width (int) : the width of the GUI screen
            window_height (int) : the height of the GUI screen
        """
        self.__image_model_root.create_segmentation_image(window_width, window_height)

    def launch_load_directory(self, path):
        """Routine to start model layer routine 'load_directory' from the
        view model
        Inputs:
            path (string): path to the directory containing the images to be displayed
        """
        self.__image_model_root.load_directory(path)

    def launch_load_image_and_segmentation_in_conjunction(self, window_width, window_height):
        """Routine to start model layer routine 'load_directory' from the
        view model
        Inputs:
            window_width(int) : width of the GUI screen
            window_height (int) : height of the GUI screen
        """
        self.__image_model_root.load_image_and_segmentation_in_conjunction(
            window_width, window_height)

    def launch_save_segmentation_image(self, directory):
        """Routine to start model layer routine 'save_segmentation_image'
        Inputs:
            directory (string) : where to save displayed segmentation image
        """
        self.__image_model_root.save_segmentation_image(directory)

    def launch_create_segmentations_from_image_directory(self, file_type, view_layer_common):
        """Routine to start model layer routine 'create_segmentations_from_image_directory'
        Inputs:
            file_type (string) : indicates what file type to process,
                 currently works with jpg or nef
            view_layer_common (Common_Layer_Controller) : instance of
                picta_common_layer.Common_Layer.Common_Layer_Controller. Used to 
                signal updates for the gui progress bar
        Returns:
            files_used (int) : total number of segmentation images generated
        """
        files_used = self.__image_model_root.create_segmentations_from_image_directory(
            file_type, view_layer_common)
        return files_used

    def launch_create_merged_image(self, window_width, window_height):
        """Routine to start model layer routine 'create_merged_image'
        Inputs:
            window_width(int) : width of the GUI screen
            window_height (int) : height of the GUI screen
        """
        self.__image_model_root.create_merged_image(window_width, window_height)

    def launch_get_segmented_area_on_original_image_and_save_segmentation(self):
        """Routine to start model layer routine
        'get_segmented_area_on_original_image_and_save_segmentation'"""
        self.__image_model_root.get_segmented_area_on_original_image_and_save_segmentation()
