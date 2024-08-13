import os
from datetime import datetime
from typing import Optional, Union
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
from tensorflow.python.data.experimental import unique

mpl.use('Qt5Agg')

sel_colormap = 'jet'  # matplotlib default is 'viridis'
default_fig_width = 8  # default figure width
plt_font_size = 20  # font size
plt_title = True  # plot figures titles
plot_db_range = 20  # default dynamic range of dB plots
default_save_type = ['png']  # default save image types
ddm_plt_default_delay_axis = 'x'

SMALL_SIZE = plt_font_size - 2
MEDIUM_SIZE = plt_font_size
BIGGER_SIZE = plt_font_size
plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

mpl.rcParams['font.size'] = plt_font_size
mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'medium'
mpl.rcParams["axes.unicode_minus"] = True

def lin2db(val): return 10.0 * np.log10(val)
def axis_formatter_no_frac(x, pos): return f'{x:-0.0f}'.replace('-', u'\u2212')

def format_range_val(start, finish, unit=''):
    return f'[{start}{unit},{finish}{unit}]'.replace('-', u'\u2212')

def pwr2db_threshold(power_linear, dynamic_range_db=None):
    """

    change power from linear two dB with a minimum threshold

    :param power_linear: power in linear scale
    :type power_linear: np.array
    :param dynamic_range_db: dynamic range in dB any value below the maximum by this is set to max - scale
    :type dynamic_range_db: float
    :return: power in dB scale
    :rtype: np.array
    """
    if dynamic_range_db is None:
        dynamic_range_db = plot_db_range

    threshold = np.max(power_linear) * 10 ** (-dynamic_range_db / 10)
    power_db = 10.0 * np.log10(np.where(power_linear < threshold, threshold, power_linear))
    return power_db


def plot_single_ddm(image, title, img_save_name, fig_out_folder, tf_save_fig=True, img_ext=None, fig_width=None, plt_delay_axis=None,
                    cbar_min_max=None, fig_save_types: Optional[list[str]] = None, cbar_title=None, delay_scale=None, dopp_scale=None):
    """

    plot a single DDM

    :param image: DDM [dim 0: delay, dim 1: Doppler]
    :type image: np.array
    :param title: plot title
    :type title: str
    :param img_save_name: image save name
    :type img_save_name: str
    :param fig_out_folder: image saving folder
    :type fig_out_folder: str
    :param tf_save_fig: save the figure?
    :type tf_save_fig: bool
    :param img_ext: extend of the image
    :type img_ext: tuple
    :param fig_width: figure width, if None default_fig_width is selected
    :type fig_width: int or float
    :param plt_delay_axis: where the delay axis? select 'x' or 'y'
    :type plt_delay_axis: str or None
    :return: figure handle
    :rtype: plt.figure
    """
    plt_bar_title = True
    if delay_scale is None:
        delay_scale = 1.0
    if dopp_scale is None:
        dopp_scale = 1.0
    if cbar_title is None:
        cbar_title = 'Reflectivity [dB]'
    if plt_delay_axis is None:
        plt_delay_axis = ddm_plt_default_delay_axis
    if fig_width is None:
        fig_width = default_fig_width
    if plt_delay_axis.lower() == 'x':
        image = np.transpose(image)

    delay_axis = 1 if (plt_delay_axis.lower() == 'x') else 0
    dopp_axis = 0 if (plt_delay_axis.lower() == 'x') else 1
    num_delay = int(image.shape[delay_axis] * delay_scale / 2)
    num_dopp = int(image.shape[dopp_axis] * dopp_scale / 2)
    if plt_delay_axis.lower() == 'x':
        fig_size = (fig_width, np.round(fig_width * num_dopp / num_delay, decimals=2))
        y_label = 'Doppler bin'
        x_label = 'Delay bin'
        if img_ext is None:  # image ext (left, right, bottom, top)
            img_ext = (-num_delay-0.5*delay_scale,
                       num_delay+0.5*delay_scale,
                       -num_dopp-0.5*dopp_scale,
                       num_dopp+0.5*dopp_scale)
    elif plt_delay_axis.lower() == 'y':
        fig_size = (np.round(fig_width * num_dopp / num_delay, decimals=2), fig_width * 0.9)
        x_label = 'Doppler bin'
        y_label = 'Delay bin'
        if img_ext is None:  # image ext (left, right, bottom, top)
            img_ext = (-num_dopp-0.5,
                       num_dopp+0.5,
                       -num_delay-0.5,
                       num_delay+0.5)
    else:
        raise RuntimeError(f'plt_delay_axis has only two options: x and y, you selected {plt_delay_axis}')

    fig = plt.figure(figsize=fig_size)
    ax = plt.subplot(111)
    im = ax.imshow(image, origin='lower', extent=img_ext, cmap=sel_colormap)
    if cbar_min_max is not None:
        im.set_clim(cbar_min_max[0], cbar_min_max[1])
    if title and plt_title:  # this in case we want to remove titles for papers
        plt.title(title, fontsize=plt_font_size-2)
    plt.xlabel(x_label, fontsize=plt_font_size)
    plt.ylabel(y_label, fontsize=plt_font_size)
    ax.tick_params(axis='both', which='major', labelsize=plt_font_size)
    if num_delay % 2 != 0:  # odd number
        num_delay += -1
    if num_dopp % 2 != 0:  # odd number
        num_dopp += -1
    delay_step = 2 if num_delay < 10 else 4
    delay_ticks = np.arange(-num_delay, stop=num_delay + delay_step, step=delay_step).astype(int)
    dopp_step = 2 if num_dopp < 10 else 4
    dopp_ticks = np.arange(-num_dopp, stop=num_dopp + dopp_step, step=dopp_step).astype(int)
    if plt_delay_axis.lower() == 'x':
        ax.set_xticks(delay_ticks)
        ax.set_yticks(dopp_ticks)
    else:
        ax.set_yticks(delay_ticks)
        ax.set_xticks(dopp_ticks)

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = plt.colorbar(im, cax=cax)
    # cbar = plt.colorbar(fraction=c_fraction, pad=0.02)
    cbar.ax.tick_params(labelsize=plt_font_size)
    cbar.ax.yaxis.set_major_formatter(axis_formatter_no_frac)
    if plt_bar_title:
        cbar.ax.set_ylabel(cbar_title, rotation=270, fontsize=plt_font_size, labelpad=plt_font_size)
    plt.tight_layout()
    plt.tight_layout()
    save_figure(fig, fig_out_folder, img_save_name, tf_save_fig, fig_save_types)
    return fig


# Function to plot data for varying sp_inc_angle with fixed other parameters
def plot_varying_sp_inc_angle(grouped_data, folder_path, img_tag, fig_save_types):
    for smap_sm_group, sc_alt_groups in grouped_data.items():
        for sc_alt_group, sp_inc_angle_groups in sc_alt_groups.items():
            list_az_angles = []
            for sp_inc_angle_group, sc_az_angle_groups in sp_inc_angle_groups.items():
                for sc_az_angle_group, items in sc_az_angle_groups.items():
                    if sc_az_angle_group not in list_az_angles:
                        list_az_angles.append(sc_az_angle_group)
            list_az_angles.sort()
            for sc_az_angle_group in list_az_angles:
                fig = plt.figure()
                ax = plt.subplot(111)
                i_plt = 0
                for sp_inc_angle_group, sc_az_angle_items in sp_inc_angle_groups.items():
                    if sc_az_angle_group in sc_az_angle_items:
                        items = sc_az_angle_items[sc_az_angle_group]

                        timestamps = [datetime.fromisoformat(item['ddm_timestamp_utc_str'][:-3]) for item in items]
                        reflectivity_peaks = [item['reflectivity_peak'] for item in items]

                        if len(reflectivity_peaks) < 2:
                            continue
                        # Sort data by timestamps
                        sorted_data = sorted(zip(timestamps, reflectivity_peaks))
                        sorted_timestamps, sorted_reflectivity_peaks = zip(*sorted_data)
                        peak_refl = lin2db(np.array(sorted_reflectivity_peaks))
                        ax.plot(sorted_timestamps, peak_refl, marker='o', linestyle='', label=format_range_val(sp_inc_angle_group, sp_inc_angle_group+5, '$^o$'))
                        i_plt += 1

                if i_plt == 0:
                    plt.close(fig)
                    continue
                ax.set_xlabel('Timestamp (UTC)', fontsize=plt_font_size)
                ax.set_ylabel('DDM Peak Reflectivity [dB]', fontsize=plt_font_size)
                ax.grid()
                # plt.title(f'Reflectivity Peak over Time for smap_sm: {smap_sm_group}, sc_alt: {sc_alt_group}, sc_az_angle: {sc_az_angle_group}')
                legend_vbox = 1.5
                plt.legend(title='$\\theta_\mathrm{i}$', loc="upper center", bbox_to_anchor=(.5, legend_vbox), ncol=3,
                           fontsize=plt_font_size - (4 if plt_font_size > 16 else 0), handletextpad=0.3, borderpad=0.3, labelspacing=0.3, columnspacing=1.0, markerscale=1.5)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.tight_layout()
                sc_az_angle_group_str = str(sc_az_angle_group) if sc_az_angle_group > 0.0 else 'n' + str(abs(sc_az_angle_group))
                img_name = img_tag + f'_peak_refl_vary_inc_angle_sm_{int(smap_sm_group * 100):d}_alt_{sc_alt_group}_az_{sc_az_angle_group_str}'
                save_figure(fig, folder_path, img_name, fig_save_types=fig_save_types)
                plt.close(fig)


# Function to plot data for varying sc_az_angle with fixed other parameters
def plot_varying_sc_az_angle(grouped_data, folder_path, img_tag, fig_save_types):
    for smap_sm_group, sc_alt_groups in grouped_data.items():
        for sc_alt_group, sp_inc_angle_groups in sc_alt_groups.items():
            for sp_inc_angle_group, sc_az_angle_groups in sp_inc_angle_groups.items():
                fig = plt.figure()
                ax = plt.subplot(111)
                i_plt = 0
                for sc_az_angle_group, items in sc_az_angle_groups.items():
                    timestamps = [datetime.fromisoformat(item['ddm_timestamp_utc_str'][:-3]) for item in items]
                    reflectivity_peaks = [item['reflectivity_peak'] for item in items]

                    # Sort data by timestamps
                    sorted_data = sorted(zip(timestamps, reflectivity_peaks))
                    sorted_timestamps, sorted_reflectivity_peaks = zip(*sorted_data)
                    peak_refl = lin2db(np.array(sorted_reflectivity_peaks))
                    ax.plot(sorted_timestamps, peak_refl, marker='o', linestyle='', label=format_range_val(sp_inc_angle_group, sc_az_angle_group+5, '$^o$'))
                    i_plt += 1
                if i_plt == 0:
                    plt.close(fig)
                    continue

                ax.set_xlabel('Timestamp (UTC)')
                ax.set_ylabel('DDM Peak Reflectivity [dB]')
                ax.grid()
                # plt.title(f'Reflectivity Peak over Time for smap_sm: {smap_sm_group}, sc_alt: {sc_alt_group}, sp_inc_angle: {sp_inc_angle_group}')
                legend_vbox = 1.5
                plt.legend(title='$\\theta_\mathrm{az}$', loc="upper center", bbox_to_anchor=(.5, legend_vbox), ncol=3,
                           fontsize=plt_font_size - (4 if plt_font_size > 16 else 0), handletextpad=0.3, borderpad=0.3, labelspacing=0.3, columnspacing=1.0, markerscale=1.5)


                plt.xticks(rotation=45)
                plt.tight_layout()
                img_name = img_tag + f'_peak_refl_vary_az_angle_sm_{int(smap_sm_group * 100):d}_alt_{sc_alt_group}_az_{sp_inc_angle_group}'
                save_figure(fig, folder_path, img_name, fig_save_types=fig_save_types)
                plt.close(fig)


# Function to plot data for varying sc_az_angle with fixed other parameters
def plot_reflectivity_x_az_lg_inc_angle(grouped_data, folder_path, img_tag, fig_save_types):
    # clr_list = mpl.rcParams['axes.prop_cycle']
    # clr_list = ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd', '#5e4fa2']
    clr_list = ["#E5E5E5","#D2D2D2","#BFBFBF","#ACACAC","#999999","#868686","#737373","#5F5F5F","#4C4C4C","#393939","#262626","#131313","#000000"]
    symb_list = ['o', 's', '^']
    save_lim = 3  # save image if number of incidence angles >= savelim
    for smap_sm_group, sc_alt_groups in grouped_data.items():
        if smap_sm_group < 0: # skip soil moisture below 0.
            continue
        for sc_alt_group, sp_inc_angle_groups in sc_alt_groups.items():
            # Sort sp_inc_angle groups before plotting
            sorted_sp_inc_angle_groups = sorted(sp_inc_angle_groups.items(), key=lambda x: x[0])
            num_plt = len([inc_ang for inc_ang, _ in sorted_sp_inc_angle_groups if inc_ang <= 60.0])
            if num_plt < save_lim:
                continue

            fig_height = 5
            if num_plt > 6:
                fig_height = 6
            if num_plt > 9:
                fig_height = 7
            if num_plt > 9:
                fig_height = 7.5

            fig = plt.figure(figsize=(6,fig_height))
            ax = plt.subplot(111)
            i_plt = 0
            for sp_inc_angle_group, sc_az_angle_groups in sorted_sp_inc_angle_groups:
                if sp_inc_angle_group > 60.0:  # only plot incidence angles below 60
                    continue
                clr_idx = int(sp_inc_angle_group / 5)
                sc_az_angles = []
                reflectivity_peaks = []

                for sc_az_angle_group, items in sc_az_angle_groups.items():
                    sc_az_angles.extend([item['sc_az_angle'] for item in items])
                    reflectivity_peaks.extend([item['reflectivity_peak'] for item in items])

                # Sort data by sc_az_angles
                sorted_data = sorted(zip(sc_az_angles, reflectivity_peaks))
                sorted_sc_az_angles, sorted_reflectivity_peaks = zip(*sorted_data)
                peak_refl = lin2db(np.array(sorted_reflectivity_peaks))
                plt.plot(sorted_sc_az_angles, peak_refl, marker=symb_list[clr_idx % len(symb_list)], linestyle='', color=clr_list[clr_idx % len(clr_list)],
                         label=format_range_val(sp_inc_angle_group, sp_inc_angle_group+5, '$^o$'))
                i_plt += 1
            ax.set_xlim([-180, 180])
            xticks = np.arange(-180, 180+90, 90)

            # Determine the tick range for y-axis
            y_min, y_max = plt.ylim()

            # Define ticks with a step of y-axis
            if (y_max - y_min) < 16.0:
                y_ticks = np.arange(np.floor(y_min/2) * 2, np.ceil(y_max/2) * 2 + 2, 2)
                ax.set_yticks(y_ticks)

            ax.set_xticks(xticks)
            plt.xlabel('Receiver azimuth angle [$^o$]')
            plt.ylabel('Peak Reflectivity [dB]')
            plt.grid()
            # plt.title(f'Reflectivity Peak over Time for smap_sm: {smap_sm_group}, sc_alt: {sc_alt_group}, sp_inc_angle: {sp_inc_angle_group}')
            legend_vbox = 1.35 if i_plt <= 3 else 1.6
            plt.legend(title='$\\theta_\mathrm{i}$', loc="upper center", bbox_to_anchor=(.5, legend_vbox), ncol=3,
                       fontsize=plt_font_size - (4 if plt_font_size > 16 else 0), handletextpad=0.0, borderpad=0.3, labelspacing=0.3, columnspacing=0.3, markerscale=1.0)

            # plt.xticks(rotation=45)
            plt.tight_layout()
            plt.tight_layout()
            plt.tight_layout()
            img_name = img_tag + f'_peak_refl_vs_az_angle_varying_inc_angle_sm_{int(smap_sm_group * 100):d}_alt_{sc_alt_group}'
            save_figure(fig, folder_path, img_name, fig_save_types=fig_save_types)
            plt.close(fig)


def save_figure(fig, fig_out_folder, img_save_name, tf_save_fig=True, fig_save_types: Optional[list[str]] = None):
    """
    save figure

    :param fig: figure object
    :param fig_out_folder: image saving folder
    :param img_save_name: image save name
    :param tf_save_fig: save the figure?
    :param fig_save_types: type of image? png, eps, pdf, svg ...
    :return: True if image is saved, else False
    """
    if not tf_save_fig:
        return False
    if fig_save_types is None:
        fig_save_types = default_save_type
    elif type(fig_save_types) is str:
        fig_save_types = [fig_save_types]
    for fig_type in fig_save_types:
        name = f"{img_save_name.split('.')[0]}.{fig_type}"
        fig.savefig(os.path.join(fig_out_folder, name), format=fig_type, bbox_inches='tight')
    return True