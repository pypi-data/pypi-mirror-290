"""
Module for Picta Image Processing's model layer.
"""
import os
import tempfile
from collections import deque
import rawpy
import tensorflow as tf
import cv2
import numpy as np
from PIL import Image, ImageFilter

class PictaImageModelRoot():
    """
    Model layer containing all data points for Picta Image Processing.

    """
    keras_model = ''
    jpeg_list = []
    png_list = []
    index_of_image_lists = 0
    no_segment_loaded = True
    image_file_path = ''
    image_file_name = ''
    output_directory = ''
    input_directory = ''
    original_image  = ''
    resized_original_image = ''
    segment_image = ''
    resized_segment_image = ''
    resized_merged_image = ''
    temp_dir = tempfile.TemporaryDirectory()
    cancel_apply_model_process_thread = False

    def confirm(self):
        """Routine to check if MVVM layers are connected correctly"""
        print('Image model root confirmed')

    def set_keras_model(self, keras_model_path):
        """Sets the member variable 'keras_model' by using the tensorflow load_model function
        Inputs:
            keras_model_path (string) : the file path to the .keras trained image model
        """
        self.keras_model = tf.keras.models.load_model(keras_model_path)

    def __resize_pil_image_for_picta_screen(self, image, window_width, window_height):
        """Resizes the image for the purpose of fitting it in on the GUI window screen. 
        Takes the window dimensions of the GUI and resizes 
        the image (with BICUBIC interpolation) based on if 
        the image is horizontal or vertical.
        Inputs:
            image (PIL.Image) : the image to be resized 
            window_width (int) : the width in pixels of the GUI window
            window_height (int) : the hieght in pixels of the GUI window
        """
        image_width, image_height = image.size
        aspect_ratio = image_width / image_height
        if aspect_ratio > 1:  # Image is wider
            width = int(window_width* 0.48)
            height = int(width / aspect_ratio)
        else:  # Image is taller
            height = int(window_height * 0.7)
            width = int(height * aspect_ratio)
        image = image.resize((width, height), Image.BICUBIC)
        return image

    def load_original_image(self, window_width, window_height, file_type):
        """Sets the 'original_image' member variable by using PIL.Image.open 
        function on the 'image_file_path' member variable. Then sets the
        'resized_original_image' member variable
        by calling resize_pil_image_for_picta_screen.
        Inputs:
            window_width(int) : width of the GUI screen
            window_height (int) : height of the GUI screen
            file_type (string) : indicates which image file type to work with.
                Currently can be 'jpg' or 'nef'
        """
        self.jpeg_list.clear()
        self.index_of_image_lists = 0
        self.no_segment_loaded = True
        self.output_directory = os.path.dirname(self.image_file_path)
        self.image_file_name = os.path.basename(self.image_file_path)
        self.jpeg_list.append(self.image_file_name)
        if file_type == 'jpg':
            self.original_image = Image.open(self.image_file_path)
            self.resized_original_image = self.__resize_pil_image_for_picta_screen(
                self.original_image, window_width, window_height)
        if file_type == 'nef':
            raw_file = rawpy.imread(self.image_file_path)
            raw_array = raw_file.postprocess(use_auto_wb=True)
            self.original_image = Image.fromarray(raw_array)
            base_name = os.path.splitext(self.image_file_name)[0]
            self.image_file_path = os.path.join(self.temp_dir.name, base_name+'.jpg')
            self.original_image.save(self.image_file_path, 'JPEG')
            self.resized_original_image = self.__resize_pil_image_for_picta_screen(
                self.original_image, window_width, window_height)

    def create_segmentation_image(self, window_width, window_height):
        """Applies the keras model to the image, then sets the member variables
        'segment_image' and 'resized_segment_image' with the generated segmentation image
        Inputs:
            window_width(int) : width of the GUI screen
            window_height (int) : height of the GUI screen
        """
        self.no_segment_loaded = False
        self.segment_image = self.__apply_model_to_image(self.keras_model, 128, self.image_file_path)
        self.resized_segment_image = self.__resize_pil_image_for_picta_screen(
            self.segment_image, window_width, window_height)

    def create_merged_image(self, window_width, window_height):
        """Creates an overlay image of the segmentation image over the original image
        through the PIL.Image.blend function. Sets member variables 'merged_image'
        and 'resized_merged_image' with the blended image"""
        merged_image = Image.blend(self.original_image, self.segment_image, 0.5)
        self.resized_merged_image = self.__resize_pil_image_for_picta_screen(
            merged_image, window_width, window_height)

    def get_segmented_area_on_original_image_and_save_segmentation(self):
        """Gets the area the segmented image occupies and applies that area to the
        original image. The original image and segmetation are first converted into arrays,
        with the segmentation array being a binary mask of False where the corresponding pixel
        is not equal to 255, and True where it is. This binary mask is applied to the
        original image array to copy only the corresponding parts into the segmented area array.
        The array is then converted back into an image and saved into
        the path asscociated with output directory.
        """
        original_image_array = np.array(self.original_image)
        binary_mask = np.array(self.segment_image) == 255
        segmented_area = np.zeros_like(original_image_array)
        segmented_area[binary_mask] = original_image_array[binary_mask]
        segmented_image = Image.fromarray(segmented_area)
        base_filename = os.path.splitext(self.jpeg_list[self.index_of_image_lists])[0]
        segmented_image.save(os.path.join(
            self.output_directory, base_filename+'_segmented.jpg'), 'JPEG')

    def load_directory(self, path):
        """Adds all images in the given directory to jpeg_list and png_list.
        Assumes the original image and its associated segmentation image are in the same directory.
        Inputs:
            path (String) : path to the directory containing the images to be displayed
        """
        self.index_of_image_lists = 0
        self.jpeg_list.clear()
        self.png_list.clear()
        files = os.listdir(path)
        for file in files:
            if '.jpg' in file:
                if not '_segmented' in file:
                    self.jpeg_list.append(file)
            if '.png' in file:
                self.png_list.append(file)
        self.jpeg_list.sort()
        self.png_list.sort()

    def load_image_and_segmentation_in_conjunction(self, window_width, window_height):
        """Loads the original image and segmentation image at the same time into
        the 'jpeg_list' and 'png_list' at position 'index_of_image_lists'. Assumes the
        image pair are at the same positions in the corresponding lists. Also stores
        a reszied version of each image
        Inputs:
            window_width(int) : width of the GUI screen
            window_height (int) : height of the GUI screen
        """
        self.image_file_name = self.jpeg_list[self.index_of_image_lists]
        self.original_image = Image.open(os.path.join(
            self.output_directory, self.jpeg_list[self.index_of_image_lists]))
        self.resized_original_image = self.__resize_pil_image_for_picta_screen(
            self.original_image, window_width, window_height)
        self.segment_image = Image.open(os.path.join(
            self.output_directory, self.png_list[self.index_of_image_lists]))
        self.resized_segment_image = self.__resize_pil_image_for_picta_screen(
            self.segment_image, window_width, window_height)
        self.no_segment_loaded = False

    def create_segmentations_from_image_directory(self, file_type, view_layer_common):
        """ Takes all jpegs or nefs from member variable 'input_directory' and
        applies the keras model to generate a segmentation image. If nef files are being 
        processed, they are first converted into jpegs before the model is applied. 
        The segmentation image is then saved as a png file using PIL.Image.save()
        Inputs:
            file_type (string) : indicates what file type to process,
                 currently works with jpg or nef
            view_layer_common (Common_Layer_Controller) : instance of
                picta_common_layer.Common_Layer.Common_Layer_Controller. Used to 
                signal updates for the gui progress bar
        Returns:
            files_used (int) : total number of segmentation images generated
        """
        self.cancel_apply_model_process_thread = False
        files_used = 0
        files_checked = 0
        files = os.listdir(self.input_directory)
        for file in files:
            if not self.cancel_apply_model_process_thread:
                if file_type == 'jpg':
                    try:
                        if '.jpg' in file.lower() and not '_segmented' in file:
                            base_filename = os.path.splitext(file)[0]
                            mask_png = self.__apply_model_to_image(
                                self.keras_model, 128, os.path.join(
                                    self.input_directory, base_filename+'.jpg'))
                            mask_png.save(os.path.join(
                                self.output_directory, base_filename+'_masked.png'), 'PNG')
                            progress_of_routine = (files_checked + 1) * 100 / len(files)
                            view_layer_common.update_gui_progress_bar(progress_of_routine, '')
                            files_used += 1
                    except IOError as error:
                        print('Invalid file found, skipping.\n' + str(error))
                if file_type == 'nef':
                    try:
                        if '.nef' in file.lower():
                            base_filename = os.path.splitext(file)[0]
                            raw_file = rawpy.imread(os.path.join(self.input_directory, file))
                            raw_array = raw_file.postprocess(use_auto_wb=True)
                            new_jpeg = Image.fromarray(raw_array)
                            new_jpeg.save(os.path.join(
                                self.output_directory, base_filename+'.jpg'), 'JPEG')
                            mask_png = self.__apply_model_to_image(
                                self.keras_model, 128, os.path.join(
                                    self.output_directory, base_filename+'.jpg'))
                            mask_png.save(os.path.join(
                                self.output_directory, base_filename+'_masked.png'), 'PNG')
                            progress_of_routine = (files_checked + 1) * 100 / len(files)
                            view_layer_common.update_gui_progress_bar(progress_of_routine, '')
                            files_used += 1
                    except IOError as error:
                        print('Invalid file found, skipping.\n' + str(error))
            else:
                break
            files_checked += 1
        return files_used

    def save_segmentation_image(self, directory):
        """Saves the member variable 'segment image' as a png using PIL.Image.save()"""
        base_name = os.path.basename(self.image_file_name)
        path_and_name = os.path.join(directory, 'segmented-'+base_name)
        self.segment_image.save(path_and_name)

    def __convert_image_into_tensor_and_apply_model_using_argmax(self, image, model):
        """Converts an image into a tensor and applies the trained model.
        Applies argmax to the model prediction on the last axis to identify the class
        
        Inputs:
            image (PIL.Image) : the image to convert into a tensor
            model (Keras model) : the model to apply 
        Returns:
            A tf tensor
        """
        image = tf.convert_to_tensor(image)
        image = tf.cast(image, tf.float32)/255.0
        modeled = tf.math.argmax(model.predict(image[tf.newaxis, ...]),axis=-1)
        modeled = modeled[...,tf.newaxis]
        modeled = modeled[0]
        modeled = modeled * 255
        return modeled

    def __crop_and_paste_into_sections(self, model_dimension, original_image, is_horizontal):
        """Routine to copy original image into two images spanning the entrie original image.
        Scales down the original image to size model_dimension x z, or 
        z x model_dimension where z = model_dimension * aspect_ratio (horizontal_orientation)
        or z = model_dimension / aspect ratio (vertical orientation). 
        Creates two images of size model_dimension x model_dimension, and copies their
        respective portion of the original image using the PIL.Image.paste() function.
        
        Inputs:
            model_dimension (int) : size of the two sections to be created,
                model_dimension x model_dimension
            og_image (PIL.Image) : the image to copy from
            is_horizontal(boolean) : indicates whether the image has a
                horizontal (true) or vertical (false) orientation
        Returns:
            left_half_or_top (PIL.Image) : first half of the copied portion of the scaled image.
                Will always copy the first model_dimension x model_dimension square
            right_half_or_bottom (PIL.Image) : second half of the copied image.
                Always starts copying at image width - model_dimension or
                image height - model_dimension depedning on horizontal or vertical
                orientation
            scaled_image.width (int) : width dimension of scaled og_image
            scaled_image.height (int) : height dimension of scaled og_image
            offset (int) : the x or y position where the second image
                began copying the original image (image height - model_dimension,
                or image width - model_dimension)
        """
        aspect_ratio = original_image.width / original_image.height
        left_half_or_top = Image.new("RGB", (model_dimension, model_dimension))
        right_half_or_bottom = Image.new("RGB", (model_dimension, model_dimension))
        if is_horizontal:
            scaled_image = original_image.resize(
                (int(model_dimension * aspect_ratio), model_dimension), resample=Image.BICUBIC)
            offset = scaled_image.width - model_dimension
            right_half_or_bottom.paste(
                scaled_image.crop((offset, 0, scaled_image.width, scaled_image.height)))
        else:
            scaled_image = original_image.resize(
                (model_dimension, int(model_dimension / aspect_ratio)), resample=Image.BICUBIC)
            offset = scaled_image.height - model_dimension
            right_half_or_bottom.paste(
                scaled_image.crop((0, offset, scaled_image.width, scaled_image.height)))
        left_half_or_top.paste(scaled_image.crop((0, 0, model_dimension, model_dimension)))
        print("Image size: " + str(original_image.width) + "x" + str(original_image.height) \
               + "\nRescaled to: " + str(scaled_image.width) + "x" + str(scaled_image.height))
        return left_half_or_top, right_half_or_bottom, \
              scaled_image.width, scaled_image.height, offset

    def __stitching_loops(
            self,
            x_range,
            y_range,
            x_range2,
            y_range2,
            preferred_segment,
            other_segment,
            x_offset,
            y_offset,
            canvas,
            prefer_segment_left_or_top):
        """Takes two segmentation images and copies portions of both images onto
        a 'canvas' image of size (x_ range + x_offset) x (y_range + y_offset) representng the 
        size of the scaled original image size. Uses PIL.Image.getpixel() to find white pixels
        in a range on each segmentation, then uses PIL.Image.putpixel() to 
        place a white pixel on canvas at the appropriate position using the offsets to match
        its placement on the original image.
        
        Inputs:
            x_range (int) : x range of where to copy from preferred_segement
            y range (int) : y range of where to copy from preferred_segement
            x_range2 (int) : x range of where to copy from other_segment
            y_range2 (int) : y range of where to copy from other_segment
            preferred_segment (PIL.Image) : the mask that will be favored for stitching
            other_segment (PIL.Image) : the secondary mask that will be less favored
                for stitching, range determined by offset
            x_offset (int) : used to determine where to put pixels from other_segment on x-axis
            y_offset (int) : used to determine where to put pixels from other_segment on y-axis
            canvas (PIL.Image) : stitched image where white pixels will be placed
            prefer_segment_left_or_top (boolean) : used to determine if the preferred_segment
                is segment_left_or_top (True) or segment_right_or_bottom (False)
        Returns:
            A PIL.Image containing the stitched pixels
        """
        if prefer_segment_left_or_top:
            for x in range(x_range):
                for y in range(y_range):
                    if preferred_segment.getpixel((x, y)) == 255:
                        canvas.putpixel((x, y), (255,255,255))
            for x_range2 in range(128):
                for y_range2 in range(128):
                    if other_segment.getpixel((x_range2, y_range2)) == 255:
                        canvas.putpixel((x_range2 + x_offset, y_range2 + y_offset), (255,255,255))
        else:
            for x in range(x_range):
                for y in range(y_range):
                    if preferred_segment.getpixel((x, y)) == 255:
                        canvas.putpixel((x, y), (255,255,255))
            for x in range(x_range2):
                for y in range(y_range2):
                    if other_segment.getpixel((x, y)) == 255:
                        canvas.putpixel((x + x_offset,  + y_offset), (255,255,255))
        return canvas

    def __perform_union_stitching(
            self,
            model_dimension,
            offset,
            canvas,
            segment_left_or_top,
            segment_right_or_bottom,
            prefer_segment_left_or_top,
            is_horizontal):
        """Passes the two segmentation images into the stitching loops in the appropriate
        order with the appropriate offsets. The segment with least amount of holes and blobs
        not part of the plastron is used as the preferred segment, meaning a majority 
        of that segment will be copied onto the canvas image. Offset is used both as 
        indication of the range in copying from segment_right_or_bottom and where to place
        the pixels on the canvas.
        
        Inputs:
            model_dimension (int) : the size of the segmentation images
            offset (int) : how far down the x or y-axis the copy of segment_right_or_bottom
                started copying from the orginial image.
            canvas (PIL.Image) : the Image object where the copied pixels will be placed
            segment_left_or_top (PIL.Image) : the first segmentation image to copy from
            segment_right_or_bottom (PIL.Image) : the second segmentation image to copy from
            prefer_segment_left_or_top (boolean) : indicates whether a majority of
                segment_left_or_top will be copied (True) or segment_right_or_bottom (False)
            is_horizontal (boolean) : indicates whether the stitching should be performed
                horizonatlly (True) or vertically (False)
        Returns:
            A single PIL.Image containing the stitched segments
        """
        if prefer_segment_left_or_top:
            if is_horizontal:
                canvas = self.__stitching_loops(
                    model_dimension, model_dimension, offset, model_dimension,
                      segment_left_or_top, segment_right_or_bottom, offset, 0, canvas, True)
            else:
                canvas = self.__stitching_loops(
                    model_dimension, model_dimension, model_dimension, offset,
                      segment_left_or_top, segment_right_or_bottom, 0, offset, canvas, True)
        else:
            if is_horizontal:
                canvas = self.__stitching_loops(
                    offset, model_dimension, model_dimension, model_dimension,
                     segment_left_or_top, segment_right_or_bottom, offset, 0, canvas, False) 
            else:
                canvas = self.__stitching_loops(
                    model_dimension, offset, model_dimension, model_dimension,
                    segment_left_or_top, segment_right_or_bottom, 0, offset, canvas, False)
        return canvas

    def __count_blobs_and_holes(self, segment, blob_or_hole):
        """ Performs depth first search on the pixels in a segement image to count either
        'blobs' not part of the plastron segment or 'holes' found inside the plastron segment.
        Inputs:
            segment (PIL.Image) : the image segment to run the check on
            blob_or_hole (int) : determines whether to check for blobs or holes based
                on pixel color to check for. 255 (white) for blobs, 0 (black) for holes
        Returns:
            An integer count of blobs or holes
        """
        num_of_blobs_or_holes = 0
        visited = set()
        def bfs(row, column):
            queue = deque()
            visited.add((x,y))
            queue.append((x,y))
            while queue:
                row, col = queue.popleft()
                directions =[[1,0], [-1,0], [0,1], [0,-1]]
                for dr, dc in directions:
                    row,column = row+dr, col+dc
                    if row in range(128) and column in range(128) and segment.getpixel((row,column)) == blob_or_hole and (row, column) not in visited:
                        queue.append((row, column))
                        visited.add((row,column))
        for x in range(128):
            for y in range(128):
                if segment.getpixel((x,y)) ==  blob_or_hole and (x,y) not in visited:
                    bfs(x,y)
                    num_of_blobs_or_holes += 1  
        return num_of_blobs_or_holes

    def __copy_single_segment_to_canvas(self, segment, x_offset, y_offset, canvas):
        """ Copies pixel by pixel a 128x128 segment image on to a black canvas of 
        the scaled image dimensions
        Inputs:
            segment (PIL.Image) : the segment to copy
            x_offset (int) : used to determine where to place pixels based on where
                the plastron resides in the original image
            y_offset (int) : same as x_offset, but for the y-axis
            canvas (PIL.Image) : 'blank' image containing only black pixels of
                size scaled_image.width by scaled_image.height
        Returns:
            The filled canvas
        """
        for x in range(128):
            for y in range(128):
                if segment.getpixel((x,y)) == 255:
                    canvas.putpixel((x + x_offset, y + y_offset), (255,255,255))
        return canvas

    def __is_plastron_too_large(self, segment_left_or_top, segment_right_or_bottom, is_horizontal):
        """Checks the borders of the segmentation images for white pixels to see if the full
        segmentation of the plastron from the original image is not fully contained in only
        segment_left_or_top or segment_right_or_bottom. Checks if segment_left_or_top has 
        a white pixel on the right or bottom edge, and if segment_right_or_bottom has a 
        white pixel on the left or top edge.
        Inputs:
            segment_left_or_top (PIL.Image): the first segment generated, no offsets
            segment_right_or_bottom (PIL.Image) : the second segment generated, with offsets
            is_horizontal (boolean) : True if checking the left and right most pixel,
                False if checking the top and bottom most pixel
        Returns:
            True if the plastron touches the boundaries in both segment images, False otherwise
        """
        possible_edge_left_or_top = False
        possible_edge_right_or_bottom = False
        if is_horizontal:
            for y in range(128):
                if segment_left_or_top.getpixel((127,y)) == 255:
                    possible_edge_left_or_top = True
                if segment_right_or_bottom.getpixel((0,y)) == 255:
                    possible_edge_right_or_bottom = True
        else:
            for x in range(128):
                if segment_left_or_top.getpixel((x,127)) == 255:
                    possible_edge_left_or_top = True
                if segment_right_or_bottom.getpixel((x, 0)) == 255:
                    possible_edge_right_or_bottom = True
        if possible_edge_right_or_bottom and possible_edge_left_or_top:
            return True
        else:
            return False

    def __find_more_centered_segmentation(self, segment_left_or_top, segment_right_or_bottom, is_horizontal, offset):
        """Used to determine the preferred segment to copy to the canvas (based on how far the plastron segment is from the center of the image).
        First checks if stitching the segmentation images is necessary due to the size of the plastron.
        For segment_left_or_top, checks which white pixel is greatest on the x or y axis. For segment_right_or_bottom, checks which white pixel is
        least on the x or y axis. Then compares the absolute difference between the x or y coordinate of the white pixels from half of the 
        model_dimension to determine which is closer to the center.
        Inputs:
            segment_left_or_top (PIL.Image): the first segment generated, no offsets
            segment_right_or_bottom (PIL.Image) : the second segment generated, with offsets
            is_horizontal (boolean) : indicates whether the original image's width > height (True) or width < height (False)
            offset (int) : the starting distance segment_right_or_bottom was copied from in the original image, i.e. not from position (0,0)
        Returns:
            preferred_segment (PIL.Image) : the segment with the plastron closest to the center, or none if sticthing is to be used
            use_stitching (boolean) : indicates whether the stitching loops are necessary or not
            offset (int) : remains the same, unless the preferred segment is segment_left_or_top, in which case the offset will be updated to 0
        """
        distance_left_or_top = 0
        distance_right_or_bottom = 0
        right_or_bottom_most_pixel = 0
        left_or_top_most_pixel = 127
        use_stitching = self.__is_plastron_too_large(segment_left_or_top, segment_right_or_bottom, is_horizontal)
        preferred_segment = None
        if not use_stitching:
            if is_horizontal:
                for x in range(127):
                    for y in range(127):
                        if segment_left_or_top.getpixel((x,y)) == 255 and x > right_or_bottom_most_pixel:
                            right_or_bottom_most_pixel = x
                        if segment_right_or_bottom.getpixel((x,y)) == 255 and x < left_or_top_most_pixel:
                            left_or_top_most_pixel = x
            else:
                for x in range(127):
                    for y in range(127):
                        if segment_left_or_top.getpixel((x,y)) == 255 and y > right_or_bottom_most_pixel:
                            right_or_bottom_most_pixel = y
                        if segment_right_or_bottom.getpixel((x,y)) == 255 and y < left_or_top_most_pixel:
                            left_or_top_most_pixel = y
            distance_left_or_top = abs(64 - right_or_bottom_most_pixel)
            distance_right_or_bottom = abs(64 - left_or_top_most_pixel)
            if distance_left_or_top < distance_right_or_bottom:
                preferred_segment = segment_left_or_top
                offset = 0
            elif distance_left_or_top > distance_right_or_bottom:
                preferred_segment = segment_right_or_bottom
            else:
                use_stitching = True
        return preferred_segment, use_stitching, offset

    def __apply_model_to_image(self, model, model_dimension, image_file):
        """Creates a segmentation image with the same size dimensions as the passed image_file. Scales the image file down to model_dimension x z or z x model_dimension.
        Creates two model_dimension x model_dimension images spanning the entirety of the original image, converts those images into tensors, applies the model, 
        and converts the tensors back into images. Then 'stitches' the two segmentation images into one, or copies the segmentation image with white 
        pixels closest to pixel coordinate (68,68). Both options are placed on a 'canvas' of size  model_dimension x z or z x model_dimension. Finally resizes the 
        canvas to the original image size and smoothes the outline of the segmentation pixels from blocky to ellipitical using morpholgical operations.
        Inputs:
            model (Keras model): trained neural net model
            model_dimension (int): dimension to use for specific model (128 for Picta, 512 for distress ID)
            image_file (string):  path to the JPG image file

        Returns:
            Resulting stitched PIL.Image
        """
        if model_dimension != 128 and model_dimension != 512:
            print('Invalid dimensions selected. Must be 128 or 512')
            return False
        is_jpeg = self.__is_jpeg_filename(image_file)
        if not is_jpeg:
            print('File is not a JPG')
            return False
        image = Image.open(image_file)
        width, height = image.size
        if width > height:      #Meaning horizontal orientation
            horizontal = True
            left_half_or_top, right_half_or_bottom, scaled_width, scaled_height, offset = self.__crop_and_paste_into_sections(model_dimension, image, horizontal)
        else:                   #Meaning vertical orientation
            horizontal = False
            left_half_or_top, right_half_or_bottom, scaled_width, scaled_height, offset = self.__crop_and_paste_into_sections(model_dimension, image, horizontal)
        left_or_top_tensor = self.__convert_image_into_tensor_and_apply_model_using_argmax(left_half_or_top, model)
        right_or_bottom_tensor = self.__convert_image_into_tensor_and_apply_model_using_argmax(right_half_or_bottom, model)
        segment_left_or_top = tf.keras.utils.array_to_img(left_or_top_tensor)
        segment_right_or_bottom = tf.keras.utils.array_to_img(right_or_bottom_tensor)
        segment_to_use, use_stitching, offset = self.__find_more_centered_segmentation(segment_left_or_top, segment_right_or_bottom, horizontal, offset)
        canvas = Image.new("RGB", (scaled_width, scaled_height))
        if use_stitching:
            #When using stitching, the segment with least amount of holes and blobs not part of the plastron is used as the preferred segment   
            blobs_segement_left_or_top = self.__count_blobs_and_holes(segment_left_or_top, 255)
            holes_in_segment_left_or_top = self.__count_blobs_and_holes(segment_left_or_top, 0)
            blobs_segement_right_or_bottom = self.__count_blobs_and_holes(segment_right_or_bottom, 255)
            holes_in_segment_right_or_bottom = self.__count_blobs_and_holes(segment_right_or_bottom, 0)
            if (blobs_segement_right_or_bottom < blobs_segement_left_or_top or holes_in_segment_right_or_bottom < holes_in_segment_left_or_top) and \
                (blobs_segement_right_or_bottom != 0):
                prefer_segment_left_or_top = False
            elif (blobs_segement_right_or_bottom > blobs_segement_left_or_top or holes_in_segment_right_or_bottom > holes_in_segment_left_or_top) and \
                (blobs_segement_left_or_top != 0):
                prefer_segment_left_or_top = True
            else:
                prefer_segment_left_or_top = True
            filled_canvas = self.__perform_union_stitching(model_dimension, offset, canvas, segment_left_or_top, segment_right_or_bottom, prefer_segment_left_or_top, horizontal)
        else:
            if horizontal:
                filled_canvas = self.__copy_single_segment_to_canvas(segment_to_use, offset, 0, canvas)
            else:
                filled_canvas = self.__copy_single_segment_to_canvas(segment_to_use, 0, offset, canvas)                               
        final_mask = filled_canvas.resize((width, height), resample=Image.BOX)
        final_mask_array = np.array(final_mask)
        print('Smoothing pixels...')
        #To 'smooth' the blocky pixels from upsacling the image, two morphological operations are performed, cv2.morpholgyEx() using MORPH_ELLIPSE and PIL.ImageFileter.ModeFilter(). The first changes the blocky pixels into ellipses, the second smoothes the valleys created by the ellipses. Decreasing the value of size in ModeFilter will speed up the runtime at the cost of 'smoothness' acheived
        smoothed_final_mask = Image.fromarray(cv2.morphologyEx(final_mask_array, cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))).filter(ImageFilter.ModeFilter(size=13))
        return smoothed_final_mask

    def __is_jpeg_filename(self, filename):
        """Determine if the filename has a jpg or jpeg extension

        Inputs:
            filename (string): full or partial or relative file name of the file
        Returns:
            (boolean) : True if the file extension is 'jpg' or 'jpeg'
                (case-insensitive), False otherwise
        """
        if len(filename) < 4:
            return False
        ext = filename[-4:].upper()
        return ext in ('.JPG', 'JPEG')
    