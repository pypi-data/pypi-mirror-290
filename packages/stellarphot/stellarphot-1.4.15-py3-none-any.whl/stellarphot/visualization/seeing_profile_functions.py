import warnings

import numpy as np
from photutils.centroids import centroid_com
import ipywidgets as ipw

from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.table import Table
from astropy.nddata import Cutout2D

try:
    from astrowidgets import ImageWidget
except ImportError:
    from astrowidgets.ginga import ImageWidget

import matplotlib.pyplot as plt

from stellarphot.io import TessSubmission
from stellarphot.visualization import seeing_plot
from stellarphot.visualization.fits_opener import FitsOpener

__all__ = ['set_keybindings', 'find_center', 'radial_profile',
            'find_hwhm', 'RadialProfile', 'box', 'SeeingProfileWidget']

desc_style = {"description_width": "initial"}


def set_keybindings(image_widget, scroll_zoom=False):
    """
    Set image widget keyboard bindings. The bindings are:

    + Pan by click-and-drag or with arrow keys.
    + Zoom by scrolling or using the ``+``/``-`` keys.
    + Adjust contrast by Ctrl-right click and drag
    + Reset contrast with shift-right-click.

    Any existing key bindings are removed.

    Parameters
    ----------

    image_widget : `astrowidgets.ImageWidget`
        Image widget on which to set the key bindings.

    scroll_zoom : bool, optional
        If True, zooming can be done by scrolling the mouse wheel.
        Default is False.

    Returns
    -------

    None
        Adds key bindings to the image widget.
    """
    bind_map = image_widget._viewer.get_bindmap()
    # Displays the event map...
    # bind_map.eventmap
    bind_map.clear_event_map()
    bind_map.map_event(None, (), 'ms_left', 'pan')
    if scroll_zoom:
        bind_map.map_event(None, (), 'pa_pan', 'zoom')

    # bind_map.map_event(None, (), 'ms_left', 'cursor')
    # contrast with right mouse
    bind_map.map_event(None, (), 'ms_right', 'contrast')

    # shift-right mouse to reset contrast
    bind_map.map_event(None, ('shift',), 'ms_right', 'contrast_restore')
    bind_map.map_event(None, ('ctrl',), 'ms_left', 'cursor')

    # Bind +/- to zoom in/out
    bind_map.map_event(None, (), 'kp_+', 'zoom_in')
    bind_map.map_event(None, (), 'kp_=', 'zoom_in')
    bind_map.map_event(None, (), 'kp_-', 'zoom_out')
    bind_map.map_event(None, (), 'kp__', 'zoom_out')

    # Bind arrow keys to panning
    # There is NOT a typo below. I want the keys to move the image in the
    # direction of the arrow
    bind_map.map_event(None, (), 'kp_left', 'pan_right')
    bind_map.map_event(None, (), 'kp_right', 'pan_left')
    bind_map.map_event(None, (), 'kp_up', 'pan_down')
    bind_map.map_event(None, (), 'kp_down', 'pan_up')


def find_center(image, center_guess, cutout_size=30, max_iters=10):
    """
    Find the centroid of a star from an initial guess of its position. Originally
    written to find star from a mouse click.

    Parameters
    ----------

    image : `astropy.nddata.CCDData` or numpy array
        Image containing the star.

    center_guess : array or tuple
        The position, in pixels, of the initial guess for the position of
        the star. The coordinates should be horizontal first, then vertical,
        i.e. opposite the usual Python convention for a numpy array.

    cutout_size : int, optional
        The default width of the cutout to use for finding the star.

    max_iters : int, optional
        Maximum number of iterations to go through in finding the center.

    Returns
    -------

    cen : array
        The position of the star, in pixels, as found by the centroiding
        algorithm.
    """
    pad = cutout_size // 2
    x, y = center_guess

    # Keep track of iterations
    cnt = 0

    # Grab the cutout...
    sub_data = image[y - pad:y + pad, x - pad:x + pad]  # - med

    # ...do stats on it...
    _, sub_med, _ = sigma_clipped_stats(sub_data)
    # sub_med = 0

    # ...and centroid.
    x_cm, y_cm = centroid_com(sub_data - sub_med)

    # Translate centroid back to original image (maybe use Cutout2D instead)
    cen = np.array([x_cm + x - pad, y_cm + y - pad])

    # ceno is the "original" center guess, set it to something nonsensical here
    ceno = np.array([-100, -100])

    while (cnt <= max_iters and
           (np.abs(np.array([x_cm, y_cm]) - pad).max() > 3
            or np.abs(cen - ceno).max() > 0.1)):

        # Update x, y positions for subsetting
        x = int(np.floor(x_cm)) + x - pad
        y = int(np.floor(y_cm)) + y - pad
        sub_data = image[y - pad:y + pad, x - pad:x + pad]  # - med
        _, sub_med, _ = sigma_clipped_stats(sub_data)
        # sub_med = 0
        mask = (sub_data - sub_med) < 0
        x_cm, y_cm = centroid_com(sub_data - sub_med, mask=mask)
        ceno = cen
        cen = np.array([x_cm + x - pad, y_cm + y - pad])
        if not np.all(~np.isnan(cen)):
            raise RuntimeError('Centroid finding failed, '
                               'previous was {}, current is {}'.format(ceno, cen))
        cnt += 1

    return cen


def radial_profile(data, center, size=30, return_scaled=True):
    """
    Construct a radial profile of a chunk of width ``size`` centered
    at ``center`` from image ``data`.

    Parameters
    ----------

    data : `astropy.nddata.CCDData` or numpy array
        Image data

    center : list-like
        x, y position of the center in pixel coordinates, i.e. horizontal
        coordinate then vertical.

    size : int, optional
        Width of the rectangular cutout to use in constructing the profile.

    return_scaled : bool, optional
        If ``True``, return an average radius and profile, otherwise
        it is cumulative. Not at all clear what a "cumulative" radius
        means, tbh.

    Returns
    -------

    r_exact : numpy array
        Exact radius of center of each pixels from profile center.

    ravg : numpy array
        Average radius in pixels used in constructing profile.

    radialprofile : numpy array
        Radial profile.
    """
    yd, xd = np.indices((size, size))

    sub_image = Cutout2D(data, center, size, mode='strict')
    sub_center = sub_image.center_cutout

    r = np.sqrt((xd - sub_center[0])**2 + (yd - sub_center[1])**2)
    r_exact = r.copy()
    r = r.astype(int)

    sub_data = sub_image.data

    tbin = np.bincount(r.ravel(), sub_data.ravel())
    rbin = np.bincount(r.ravel(), r_exact.ravel())
    nr = np.bincount(r.ravel())
    if return_scaled:
        radialprofile = tbin / nr
        ravg = rbin / nr
    else:
        radialprofile = tbin
        ravg = rbin

    return r_exact, ravg, radialprofile


def find_hwhm(r, intensity):
    """
    Estimate the half-width half-max from normalized, angle-averaged intensity profile.

    Parameters
    ----------

    r : array
        Radius of each pixel from the center of the star.

    intensity : array
        Normalized intensity at each radius.

    Returns
    -------

    r_half : float
        Radius at which the intensity is 50% the maximum
    """

    # Make the bold assumption that intensity decreases monotonically
    # so that we just need to find the first place where intensity is
    # less than 0.5 to estimate the HWHM.
    less_than_half = intensity < 0.5
    half_index = np.arange(len(less_than_half))[less_than_half][0]
    before_half = half_index - 1

    # Do linear interpolation to find the radius at which the intensity
    # is 0.5.
    r_more = r[before_half]
    r_less = r[half_index]
    I_more = intensity[before_half]
    I_less = intensity[half_index]

    I_half = 0.5

    r_half = r_less - (I_less - I_half) / (I_less - I_more) * (r_less - r_more)

    return r_half


class RadialProfile:
    """
    Class to hold radial profile information for a star.

    Parameters
    ----------

    data : numpy array
        Image data.

    x : int
        x position of the star.

    y : int
        y position of the star.

    Attributes
    ----------

    cen : tuple
        x, y position of the center of the star.

    data : numpy array
        Image data.

    FWHM : float
        Full-width half-max of the radial profile.

    profile_size : int
        Size of the cutout used to construct the radial profile.

    radius_values : numpy array
        Radius values for the radial profile.

    r_exact : numpy array
        Exact radius of center of each pixels from profile center.

    ravg : numpy array
        Average radius in pixels used in constructing profile.

    """
    def __init__(self, data, x, y):
        """
        Initialize the radial profile object instance.  Sets the center
        of the star and the image data.

        Parameters
        ----------

        data : numpy array
            Image data.

        x : int
            x position of the star.

        y : int
            y position of the star.


        """
        self.cen = find_center(data, (x, y), cutout_size=30)
        self.data = data

    def profile(self, profile_size):
        """
        Construct the radial profile of the star.  Sets
        ``r_exact``, ``ravg``, and ``radialprofile`` attributes.

        Parameters
        ----------

        profile_size : int
            Size of the cutout to use in constructing the profile.

        """
        self.profile_size = profile_size
        self.r_exact, self.ravg, self.radialprofile = (
            radial_profile(self.data,
                           self.cen,
                           size=profile_size)
        )

        self.sub_data = Cutout2D(self.data, self.cen, size=profile_size).data
        sub_med = np.median(self.sub_data)
        adjust_max = self.radialprofile.max() - sub_med
        self.scaled_profile = (self.radialprofile - sub_med) / adjust_max
        self.scaled_exact_counts = (self.sub_data - sub_med) / adjust_max
        self.HWHM = find_hwhm(self.ravg, self.scaled_profile)

    @property
    def FWHM(self):
        return int(np.round(2 * self.HWHM))

    @property
    def radius_values(self):
        return np.arange(len(self.radialprofile))


def box(imagewidget):
    """
    Compatibility layer for older versions of the photometry notebooks.

    Parameters
    ----------

    imagewidget : `astrowidgets.ImageWidget`
        ImageWidget instance to use for the seeing profile.

    Returns
    -------

    box : `ipywidgets.VBox`
        Box containing the seeing profile widget.
    """
    return SeeingProfileWidget(imagewidget=imagewidget).box


class SeeingProfileWidget:
    """
    A class for storing an instance of a widget displaying the seeing profile of stars in an image.

    Parameters
    ----------
    imagewidget : `astrowidgets.ImageWidget`, optional
        ImageWidget instance to use for the seeing profile.

    width : int, optional
        Width of the seeing profile widget.
    """
    def __init__(self, imagewidget=None, width=500):
        if not imagewidget:
            imagewidget = ImageWidget(image_width=width,
                                      image_height=width,
                                      use_opencv=True)

        self.iw = imagewidget
        # Do some set up of the ImageWidget
        set_keybindings(self.iw, scroll_zoom=False)
        bind_map = self.iw._viewer.get_bindmap()
        bind_map.map_event(None, ('shift',), 'ms_left', 'cursor')
        gvc = self.iw._viewer.get_canvas()
        self._mse = self._make_show_event()
        gvc.add_callback('cursor-down', self._mse)

        # Outputs to hold the graphs
        self.out = ipw.Output()
        self.out2 = ipw.Output()
        self.out3 = ipw.Output()
        # Build the larger widget
        self.container = ipw.VBox()
        self.fits_file = FitsOpener(title="Choose an image")
        big_box = ipw.HBox()
        big_box = ipw.GridspecLayout(1, 2)
        layout = ipw.Layout(width='20ch')
        hb = ipw.HBox()
        self.ap_t = ipw.IntText(description='Aperture radius', value=5, layout=layout, style=desc_style)
        self.in_t = ipw.IntText(description='Inner annulus', value=10, layout=layout, style=desc_style)
        self.out_t = ipw.IntText(description='Outer annulus', value=20, layout=layout, style=desc_style)
        self.save_aps = ipw.Button(description="Save settings")
        hb.children = [self.ap_t, self.save_aps] #, self.in_t, self.out_t]

        lil_box = ipw.VBox()
        lil_tabs = ipw.Tab()
        lil_tabs.children = [self.out3, self.out, self.out2]
        lil_tabs.set_title(0, "SNR")
        lil_tabs.set_title(1, "Seeing profile")
        lil_tabs.set_title(2, "Integrated counts")
        self.tess_box = self._make_tess_box()
        lil_box.children = [lil_tabs, self.tess_box]

        imbox = ipw.VBox()
        imbox.children = [imagewidget, hb]
        big_box[0, 0] = imbox
        big_box[0, 1] = lil_box
        big_box.layout.width = '100%'

        # Line below puts space between the image and the plots so the plots
        # don't jump around as the image value changes.
        big_box.layout.justify_content = 'space-between'
        self.big_box = big_box
        self.container.children = [self.fits_file.file_chooser, self.big_box]
        self.box = self.container
        self._aperture_name = 'aperture'

        self._tess_sub = None

        # Fill this in later with name of object from FITS file
        self.object_name = ''
        self._set_observers()

    def load_fits(self, file):
        self.fits_file.load_in_image_widget(self.iw)

    def _update_file(self, change):
        self.load_fits(change.selected)

    def _construct_tess_sub(self):
        file = self.fits_file.path
        self._tess_sub = TessSubmission.from_header(
            fits.getheader(file),
            telescope_code=self.setting_box.telescope_code.value,
            planet=self.setting_box.planet_num.value
        )

    def _set_seeing_profile_name(self, change):
        self._construct_tess_sub()
        self.seeing_file_name.value = self._tess_sub.seeing_profile

    def _save_toggle_action(self, change):
        activated = change['new']

        if activated:
            self.setting_box.layout.visibility = "visible"
            self._set_seeing_profile_name("")
        else:
            self.setting_box.layout.visibility = "hidden"

    def _save_seeing_plot(self, button):
        self._seeing_plot_fig.savefig(self.seeing_file_name.value)

    def _set_observers(self):
        def aperture_obs(change):
            self._mse(self.iw, aperture=change['new'])

        self.ap_t.observe(aperture_obs, names='value')
        self.save_aps.on_click(self._save_ap_settings)
        self.fits_file.register_callback(self._update_file)
        self.save_toggle.observe(self._save_toggle_action, names='value')
        self.save_seeing.on_click(self._save_seeing_plot)
        self.setting_box.planet_num.observe(self._set_seeing_profile_name)
        self.setting_box.telescope_code.observe(self._set_seeing_profile_name)

    def _save_ap_settings(self, button):
        ap_rad = self.ap_t.value
        with open('aperture_settings.txt', 'w') as f:
            f.write(f'{ap_rad},{ap_rad + 10},{ap_rad + 15}')

    def _make_tess_box(self):
        box = ipw.VBox()
        setting_box = ipw.HBox()
        self.save_toggle = ipw.ToggleButton(description="TESS seeing profile...",
                                            disabled=True)
        scope_name = ipw.Text(description="Telescope code",
                              value="Paul-P-Feder-0.4m",
                              style=desc_style)
        planet_num = ipw.IntText(description="Planet", value=1)
        self.save_seeing = ipw.Button(description="Save")
        self.seeing_file_name = ipw.Label(value="Moo")
        setting_box.children = (scope_name, planet_num, self.seeing_file_name, self.save_seeing)
        # for kid in setting_box.children:
        #     kid.disabled = True
        box.children = (self.save_toggle, setting_box)
        setting_box.telescope_code = scope_name
        setting_box.planet_num = planet_num
        setting_box.layout.flex_flow = "row wrap"
        setting_box.layout.visibility = "hidden"
        self.setting_box = setting_box
        return box

    def _make_show_event(self):

        def show_event(viewer, event=None, datax=None, datay=None, aperture=None):
            profile_size = 60
            fig_size = (10, 5)

            self.save_toggle.disabled = False

            if event is not None:
                # User clicked on a star, so generate profile
                i = self.iw._viewer.get_image()
                data = i.get_data()

                # Rough location of click in original image
                x = int(np.floor(event.data_x))
                y = int(np.floor(event.data_y))

                rad_prof = RadialProfile(data, x, y)

                try:
                    try: # Remove previous marker
                        self.iw.remove_markers(marker_name=self._aperture_name)
                    except AttributeError:
                        self.iw.remove_markers_by_name(marker_name=self._aperture_name)
                except ValueError:
                    # No markers yet, keep going
                    pass

                # ADD MARKER WHERE CLICKED
                self.iw.add_markers(Table(data=[[rad_prof.cen[0]], [rad_prof.cen[1]]],
                                          names=['x', 'y']),
                                    marker_name=self._aperture_name)

                # ----> MOVE PROFILE CONSTRUCTION INTO FUNCTION <----

                # CONSTRUCT RADIAL PROFILE OF PATCH AROUND STAR
                # NOTE: THIS IS NOT BACKGROUND SUBTRACTED
                rad_prof.profile(profile_size)

                # Default is 1.5 times FWHM
                aperture_radius = np.round(1.5 * 2 * rad_prof.HWHM, 0)
                self.rad_prof = rad_prof

                # Set this AFTER the radial profile has been created to avoid an attribute
                # error.
                self.ap_t.value = aperture_radius
            else:
                # User changed aperture
                aperture_radius = aperture
                rad_prof = self.rad_prof

            # DISPLAY THE SCALED PROFILE
            self.out.clear_output(wait=True)
            with self.out:
                # sub_med += med
                self._seeing_plot_fig = seeing_plot(rad_prof.r_exact, rad_prof.scaled_exact_counts,
                            rad_prof.ravg,
                            rad_prof.scaled_profile, rad_prof.HWHM,
                            self.object_name, gap=10, annulus_width=15,
                            radius = aperture_radius,
                            figsize=fig_size)
                plt.show()

            # CALCULATE AND DISPLAY NET COUNTS INSIDE RADIUS
            self.out2.clear_output(wait=True)
            with self.out2:
                sub_blot = rad_prof.sub_data.copy().astype('float32')
                min_idx = profile_size // 2 - 2 * rad_prof.FWHM
                max_idx = profile_size // 2 + 2 * rad_prof.FWHM
                sub_blot[min_idx:max_idx, min_idx:max_idx] = np.nan
                sub_std = np.nanstd(sub_blot)
                new_sub_med = np.nanmedian(sub_blot)
                r_exact, ravg, tbin2 = radial_profile(rad_prof.data - new_sub_med, rad_prof.cen,
                                                      size=profile_size,
                                                      return_scaled=False)
                r_exact_s, ravg_s, tbin2_s = radial_profile(rad_prof.data - new_sub_med, rad_prof.cen,
                                                      size=profile_size,
                                                      return_scaled=True)
                #tbin2 = np.bincount(r.ravel(), (sub_data - sub_med).ravel())
                counts = np.cumsum(tbin2)
                plt.figure(figsize=fig_size)
                plt.plot(rad_prof.radius_values, counts)
                plt.xlim(0, 40)
                ylim = plt.ylim()
                plt.vlines(aperture_radius, *plt.ylim(), colors=['red'])
                plt.ylim(*ylim)
                plt.grid()

                plt.title('Net counts in aperture')
                e_sky = np.nanmax([np.sqrt(new_sub_med), sub_std])

                plt.xlabel('Aperture radius (pixels)')
                plt.ylabel('Net counts')
                plt.show()

            # CALCULATE And DISPLAY SNR AS A FUNCTION OF RADIUS
            self.out3.clear_output(wait=True)
            with self.out3:
                read_noise = 10  # electrons
                gain = 1.5  # electrons/count
                # Poisson error is square root of the net number of counts enclosed
                poisson = np.sqrt(np.cumsum(tbin2))

                # This is obscure, but correctly calculated the number of pixels at
                # each radius, since the smoothed is tbin2 divided by the number of
                # pixels.
                nr = tbin2 / tbin2_s

                # This ignores dark current
                error = np.sqrt(poisson ** 2 + np.cumsum(nr)
                                * (e_sky ** 2 + (read_noise / gain)** 2))

                snr = np.cumsum(tbin2) / error
                plt.figure(figsize=fig_size)
                plt.plot(rad_prof.radius_values + 1, snr)

                plt.title(f'Signal to noise ratio max {snr.max():.1f} '
                          f'at radius {snr.argmax() + 1}')
                plt.xlim(0, 40)
                ylim = plt.ylim()
                plt.vlines(aperture_radius, *plt.ylim(), colors=['red'])
                plt.ylim(*ylim)
                plt.xlabel('Aperture radius (pixels)')
                plt.ylabel('SNR')
                plt.grid()
                plt.show()
        return show_event

