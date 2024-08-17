import matplotlib.pyplot as plt

__all__ = ['seeing_plot', 'plot_predict_ingress_egress']


def seeing_plot(raw_radius, raw_counts, binned_radius, binned_counts, HWHM,
                plot_title='', file_name='', gap=6, annulus_width=13, radius=None,
                figsize=(20, 10)):
    """
    Show a seeing plot for data from an image with radius on the x axis and counts (ADU) on the y axis.

    Parameters
    ----------
    raw_radius : array
        the distance of each pixel from the object of interest

    raw_counts : array
        the counts of each pixel

    binned_radius : array
        pixels grouped by distance from object of interest

    binned_counts : array
        average counts of each group of pixels

    HWHM : number
        half width half max, 1/2 * FWHM

    plot_title : optional, string
        title of plot

    file_name : optional, string
        if entered, file will save as png with this name

    gap : number
        the distance between the aperture and the inner annulus

    annulus_width : number
        the distance between the inner and outer annulus

    figsize : tuple of int, optional
        Size of figure.

    Returns
    -------

    `matplotlib.pyplot.figure`
        The figure object containing the seeing plot.
    """
    if radius is None:
        radius = HWHM * 4

    fig = plt.figure(figsize=figsize)
    plt.grid(True)
    inner_annulus = radius + gap
    outer_annulus = inner_annulus + annulus_width

    # plot the raw radius and raw counts
    plt.plot(raw_radius, raw_counts, linestyle='none',
             marker="s", markerfacecolor='none', color='blue')

    # plot the binned radius and binned counts
    plt.plot(binned_radius, binned_counts, color='magenta', linewidth='1.0')

    # draw vertical line at HWHM and label it
    plt.vlines(HWHM, -0.2, 1.2, linestyle=(0, (5, 10)), color='#00cc00')
    plt.annotate(f"HWHM {HWHM:2.1f}", (HWHM, -0.25),
                 color='#00cc00', horizontalalignment='center')

    # label axis
    plt.xlabel('Radius (pixels)')
    plt.ylabel('ADU')

    # draw vertical line at the radius and label it
    plt.vlines(radius, -0.2, binned_counts[0], color='red')
    plt.annotate(f"Radius {radius:2.1f}", (radius, -0.25),
                 color='red', horizontalalignment='center')
    plt.hlines(binned_counts[0], binned_counts[0], radius, color='red')

    # label the source
    plt.annotate(
        'SOURCE', (radius, binned_counts[0] + 0.02),
        color='red', horizontalalignment='center')

    # draw vertical lines at the background and label it
    plt.vlines(inner_annulus, -0.2, binned_counts[0], color='red')
    plt.vlines(outer_annulus, -0.2, binned_counts[0], color='red')
    plt.hlines(binned_counts[0], inner_annulus, outer_annulus, color='red')
    plt.annotate('BACKGROUND', (inner_annulus,
                                binned_counts[0] + 0.02), color='red')
    plt.annotate(f"Back> {inner_annulus:2.1f}",
                 (inner_annulus, -0.25), color='red', horizontalalignment='center')
    plt.annotate(f"<Back {outer_annulus:2.1f}",
                 (outer_annulus, -0.25), color='red', horizontalalignment='center')

    # title the plot
    title_string = [f"{plot_title}", f"FWHM:{HWHM*2:.1f} pixels"]
    plt.title('\n'.join(title_string))

    # save plot as png
    if file_name:
        safe_name = file_name.replace(" ", "-")
        plt.savefig(f"{safe_name + '-seeing-profile'}.png")
    return fig


def plot_predict_ingress_egress(ingress_time, egress_time, end_line=1,
                                ingress_x_pos=1, egress_x_pos=1, labels_y_pos=1):
    """
    Parameters
    ----------
    ingress_time : float
        the beginning of an exoplanet transit

    egress_time : float
        the end of an exoplanet transit

    end_line : float
        offset to move the vertical lines

    ingress_x_pos : float
        offset to center ingress label

    egress_x_pos : float
        offset to center egress label

    labels_y_pos : float
        offset to move ingress and egress labels

    Returns
    -------

    None
        Directly adds lines and labels to the current plot.
    """
    ymin, ymax = plt.ylim()

    # create a vertical line at the ingress time and label it
    plt.vlines(ingress_time, ymin - end_line, ymax,
               linestyle=(0, (5, 10)), color='red')
    plt.annotate("Predicted Ingress", (ingress_time - ingress_x_pos,
                                       ymin - labels_y_pos), color='red')

    # create a vertical line at the egress time and label it
    plt.vlines(egress_time, ymin - end_line, ymax,
               linestyle=(0, (5, 10)), color='red')
    plt.annotate("Predicted Egress", (egress_time - egress_x_pos,
                                      ymin - labels_y_pos), fontsize=10, color='red')
