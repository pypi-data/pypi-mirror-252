import matplotlib.pyplot as plt
from .styles import EventStyle

def plot_events(ax, profile_events, plot_type='normal', event_alpha=0.6):
    """
    Plots the hline or vline for each event on a plot
    Args:
        ax: matplotlib.Axes to add horizontal or vertical lines to
        start: Array index to represent start of motion
        surface: Array index to represent snow surface
        stop: Array index to represent stop of motion
        nir_stop: Array index to represent stop estimated by nir
        plot_type: string indicating whether the index is on the y (vertical) or the x (normal)
    """
    # PLotting sensor data on the x axis and time/or depth on y axis
    if plot_type == 'vertical':
        line_fn = ax.axhline

    # Normal time series data with y = values, x = time
    elif plot_type == 'normal':
        line_fn = ax.axvline

    else:
        raise ValueError(f'Unrecognized plot type {plot_type}, options are vertical or normal!')

    for event in profile_events:
        if event.time is not None:
            style = EventStyle.from_name(event.name)
            line_fn(event.time, linestyle=style.linestyle, color=style.color,
                    label=style.label, alpha=event_alpha,  linewidth=style.linewidth)


def plot_ts(data, data_label=None, time_data=None, events=None, thresholds=None, features=None, show=True, ax=None, alpha=1.0, color=None):
    if ax is None:
        fig, ax = plt.subplots(1)
        ax.grid(True)
    n_samples = len(data)
    if n_samples < 100:
        mark = 'o--'
    else:
        mark = '-'

    if time_data is not None:
        ax.plot(time_data, data, mark, alpha=alpha, label=data_label, color=color)
    else:
        ax.plot(data, mark, alpha=alpha, label=data_label, color=color)

    if data_label is not None:
        ax.legend()

    if events is not None:
        for name, event_idx in events:
            s = EventStyle.from_name(name)
            if time_data is not None:
                v = time_data[event_idx]
            else:
                v = event_idx
            ax.axvline(v, color=s.color, linestyle=s.linestyle, label=name)
    if thresholds is not None:
        for name, tr in thresholds:
            ax.axhline(tr, label=name, alpha=0.8, linestyle='--')

    if features is not None:
        ydata = [data[f] for f in features]
        if time_data is not None:
            ax.plot([time_data[f] for f in features], ydata, '.')
        else:
            ax.plot(features, ydata, '.')

    if show:
        plt.show()

    return ax


def plot_constrained_baro(orig, partial, full, acc_pos, top, bottom, start, stop,
                          baro='filtereddepth', acc_axis='Y-Axis'):

    # zero it out
    partial[baro] = partial[baro] - partial[baro].iloc[0]
    # partial = partial.reset_index('time')
    # orig = orig.set_index('time')

    mid = int((start+stop)/2)

    orig[baro] = orig[baro] - orig[baro].iloc[0]
    ax = plot_ts(orig[baro], time_data=orig['time'], color='steelblue', alpha=0.2,
                 data_label='Orig.', show=False, features=[top, bottom])
    ax = plot_ts(acc_pos[acc_axis], time_data=acc_pos['time'], color='black', alpha=0.5,
                 ax=ax, data_label='Acc.', show=False,
                 events=[('start', start), ('stop', stop), ('mid', mid)])
    ax = plot_ts(partial[baro], time_data=partial['time'], color='blue',
                 ax=ax, show=False, data_label='Part. Const.', alpha=0.3)
    ax = plot_ts(full, time_data=partial['time'], color='magenta', alpha=1,
                 ax=ax, show=True, data_label='Constr.')

def plot_fused_depth(acc_depth, baro_depth, avg, scaled_baro=None, error=None):
    """
    Diagnostic plot to show the inner workings of the fusing technique
    """
    events = None
    if error is not None:
        events=[('error',error)]
    ax = plot_ts(avg, events=events, show=False)
    ax = plot_ts(acc_depth, ax=ax, data_label='Acc', show=False)
    ax = plot_ts(baro_depth, ax=ax, data_label='Baro', show=False)
    if scaled_baro is not None:
        ax = plot_ts(scaled_baro, ax=ax, data_label='Scaled Baro', show=False)

    ax.legend()
    plt.show()



def plot_ground_strike(signal, search_start, stop_idx, impact, long_press, ground):
    events = [('stop', stop_idx)]
    if long_press is not None:
        events.append(('long_press', long_press + search_start))
    if impact is not None:
        events.append(('impact', impact + search_start))
    if ground is not None:
        events.append(('ground', ground))
    ax = plot_ts(signal, events=events,show=False)
    ax.legend()
    plt.show()

