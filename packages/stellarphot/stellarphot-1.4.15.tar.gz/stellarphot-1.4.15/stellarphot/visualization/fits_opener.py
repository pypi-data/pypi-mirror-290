from pathlib import Path
import warnings

from astropy.io import fits
from astropy.nddata import CCDData

from ipyfilechooser import FileChooser


__all__ = ['FitsOpener']


class FitsOpener:
    """ A class to open FITS files and display them in an `astrowidgets.ImageWidget`.

    Attributes
    ----------

    ccd : `astropy.nddata.CCDData`
        The selected FITS file as a CCDData object.

    file_chooser : `ipyfilechooser.FileChooser`
        The actual FileChooser widget.

    header : dict
        The header of the selected FITS file.

    path : `pathlib.Path`
        The path to the selected FITS file.

    register_callback : function, optional
        A function that takes one argument. This function will be called when the
        selected file changes.
    """
    def __init__(self, title="Choose an image", filter_pattern=None, **kwargs):
        """
        Initializes an instance of the FitsOpener class, which is a wrapper around
        the `ipyfilechooser.FileChooser` widget that (if no `filter_pattern` is given)
        defaults to showing only FITS files.

        Parameters
        ----------

        title : str, optional
            The title of the FileChooser widget. The default is "Choose an image".

        filter_pattern : str, optional
            The filter pattern to use for the FileChooser widget. The default is None,
        """
        self._fc = FileChooser(title=title, **kwargs)
        if not filter_pattern:
            self._fc.filter_pattern = ['*.fit*', '*.fit*.[bg]z']
        else:
            self._fc.filter_pattern = filter_pattern

        self._header = {}
        self._selected_cache = self._fc.selected
        self.object = ""
        self.register_callback(lambda x: None)

    @property
    def file_chooser(self):
        """
        The actual FileChooser widget.
        """
        return self._fc

    @property
    def header(self):
        self._set_header()
        return self._header

    @property
    def ccd(self):
        """
        Return image as CCDData object
        """
        return CCDData.read(self.path)

    @property
    def path(self):
        return Path(self._fc.selected)

    def _set_header(self):
        if not self._header or self._fc.selected != self._selected_cache:
            self._selected_cache = self._fc.selected
            try:
                self._header = fits.getheader(self.path)
            except OSError:
                return

        try:
            self.object = self._header['object']
        except KeyError:
            pass

    def register_callback(self, callable):
        """
        Register a callback that is called when the value changes. This is
        the alternative to observing a value, which is not implemented for
        some reason. Only one callback function is allowed.

        This wraps the user-supplied callable to also update the header.

        Parameters
        ----------

        callable : function
            A function that takes one argument.
        """
        def wrap_call(change):
            self._set_header()
            callable(change)

        self._fc.register_callback(wrap_call)

    def load_in_image_widget(self, image_widget):
        """
        Load the selected image into an `astrowidgets.ImageWidget`, doing the best
        that can be done to suppress warnings.

        Parameters
        ----------

        image_widget : `astrowidgets.ImageWidget`
            The widget into which to load the image.
        """
        with warnings.catch_warnings():
            image_widget.load_fits(str(self.path))

    def set_file(self, file, directory=None):
        """
        Set the selected file of the `ipyfilechooser.FileChooser` to be the input file.

        Parameters
        ----------

        file : Path-like
            The file to be set as selected. Can be a string or a pathlib.Path.
            Cannot contain any directory information.

        directory : Path-like, optional
            Directory the file is in. The default value is the current directory of the
            `ipyfilechooser.FileChooser`.
        """
        if directory is None:
            directory = self._fc.selected_path

        self._fc.reset(directory, file)
        self._fc._apply_selection()
