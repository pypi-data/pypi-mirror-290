"""
Module for Picta Image Processing's common layer.
Contains abstract class CommonLayer
"""
from abc import ABC, abstractmethod

class CommonLayer(ABC):
    """Abstract methods for sharing data across all layers of of Picta Image Processing"""

    @abstractmethod
    def update_gui_progress_bar(self, percent_progress, display_message):
        """Routine to update the progress of a progress bar
        Inputs:
            percent_progress (int) : Percentage of how many tasks have been completed 
                in accordance total number of tasks to complete in the routine.
            display_message (string) :
        """
