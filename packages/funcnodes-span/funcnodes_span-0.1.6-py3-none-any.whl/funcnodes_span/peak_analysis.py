from funcnodes import NodeDecorator, Shelf
import numpy as np
from enum import Enum
from exposedfunctionality import controlled_wrapper
from typing import Optional, TypedDict, List
from scipy.signal import find_peaks
from scipy.stats import norm
from scipy import interpolate
import copy
import lmfit
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import re


class PeakProperties(TypedDict):
    id: str
    i_index: int
    index: int
    f_index: int
    x_at_i_index: int
    x_at_index: int
    x_at_f_index: int
    y_at_index: int
    y_at_f_index: int
    y_at_i_index: int
    area: float
    symmetricity: float
    tailing: float
    FWHM: float
    plate_nr: float
    width: float
    _is_fitted: bool = False
    _is_force_fitted: bool = False
    fitting_data: Optional[dict] = None
    fitting_info: Optional[dict] = None


def compute_peak_properties(
    x_array: np.ndarray,
    y_array: np.ndarray,
    peak_indices: List[int],
    peak_nr: int,
    is_fitted: bool = False,
    is_force_fitted: bool = False,
    fitting_data: Optional[dict] = None,
    fitting_info: Optional[dict] = None,
) -> PeakProperties:
    # """
    # Compute various properties of a given peak.

    # Parameters:
    # - x_array: np.ndarray - The array of x-values (e.g., time or wavelength).
    # - y_array: np.ndarray - The array of y-values (e.g., intensity).
    # - peak_indices: List[int] - A list containing the start index, peak index, and end index of the peak.
    # - peak_nr: int - The identifier number of the peak.
    # - is_fitted: bool = False - A flag indicating whether the peak is fitted or not.
    # - is_force_fitted: bool = False - A flag indicating whether the peak is forced fitted or not.
    # - fitting_data: Optional[dict] = None - A dictionary containing the fitting data if the peak is fitted.
    # - fitting_info: Optional[dict] = None - A dictionary containing the fitting information if the peak is fitted.

    # Returns:
    # - peak_properties: PeakProperties - A dictionary containing various properties of the peak.
    # """

    i_index, index, f_index = peak_indices

    # Extract the relevant portion of the arrays
    selected_signal = y_array[i_index:f_index]
    selected_time = x_array[i_index:f_index]

    # Create an interpolated time array with higher resolution
    selected_time_interpol = np.linspace(
        selected_time[0],
        selected_time[-1],
        num=len(selected_time) * 10,
        endpoint=True,
    )

    # Interpolate the selected signal to match the interpolated time array
    f_interpol = interpolate.interp1d(selected_time, selected_signal, kind="linear")
    selected_signal_interpol = f_interpol(selected_time_interpol)

    # Determine the amplitude and position of the peak in the interpolated signal
    amplitude = np.max(selected_signal_interpol)
    peak_position = np.where(selected_signal_interpol == amplitude)[0][0]

    # Split the interpolated signal into left and right spectra relative to the peak
    left_spectrum = selected_signal_interpol[:peak_position]
    right_spectrum = selected_signal_interpol[peak_position:]

    # Helper function to compute indices for a given percentage of amplitude
    def compute_indices(spectrum, percentage):
        try:
            left_index = (np.abs(spectrum - percentage * amplitude)).argmin()
        except ValueError:
            left_index = 0
        return left_index

    # Compute FWHM (Full Width at Half Maximum)
    FWHM_left_index = compute_indices(left_spectrum, 0.5)
    FWHM_right_index = compute_indices(right_spectrum, 0.5) + peak_position
    FWHM_a = abs(
        selected_time_interpol[FWHM_left_index] - selected_time_interpol[peak_position]
    )
    FWHM_b = abs(
        selected_time_interpol[FWHM_right_index] - selected_time_interpol[peak_position]
    )
    FWHM = np.around(FWHM_b / FWHM_a, 2) if FWHM_a != 0 else np.nan

    # Compute Symmetricity
    symmetricity_left_index = compute_indices(left_spectrum, 0.1)
    symmetricity_right_index = compute_indices(right_spectrum, 0.1) + peak_position
    symmetricity_a = abs(
        selected_time_interpol[symmetricity_left_index]
        - selected_time_interpol[peak_position]
    )
    symmetricity_b = abs(
        selected_time_interpol[symmetricity_right_index]
        - selected_time_interpol[peak_position]
    )
    symmetricity = (
        np.around(symmetricity_b / symmetricity_a, 2) if symmetricity_a != 0 else np.nan
    )

    # Compute Tailing
    tailing_left_index = compute_indices(left_spectrum, 0.05)
    tailing_right_index = compute_indices(right_spectrum, 0.05) + peak_position
    tailing_a = abs(
        selected_time_interpol[tailing_left_index]
        - selected_time_interpol[peak_position]
    )
    tailing_b = abs(
        selected_time_interpol[tailing_right_index]
        - selected_time_interpol[peak_position]
    )
    tailing = (
        np.around(((tailing_a + tailing_b) / 2 * tailing_a), 2)
        if tailing_a != 0
        else np.nan
    )

    # Compute Area under the peak
    area = abs(np.trapz(selected_signal_interpol, selected_time_interpol))

    # Compute Plate Number
    try:
        plate_nr = 2 * np.pi * ((x_array[i_index] * y_array[index]) / area) ** 2
    except ZeroDivisionError:
        plate_nr = np.nan

    # Compute Width of the peak
    width = x_array[f_index] - x_array[i_index]

    # Populate the PeakProperties dictionary
    peak_properties: PeakProperties = {
        "id": str(peak_nr + 1) + "_fitted" if is_fitted else str(peak_nr + 1),
        "i_index": i_index,
        "index": index,
        "f_index": f_index,
        "x_at_i_index": x_array[i_index],
        "x_at_index": x_array[index],
        "x_at_f_index": x_array[f_index],
        "y_at_i_index": y_array[i_index],
        "y_at_index": y_array[index],
        "y_at_f_index": y_array[f_index],
        "area": area,
        "symmetricity": symmetricity,
        "tailing": tailing,
        "FWHM": FWHM,
        "plate_nr": plate_nr,
        "width": width,
        "_is_fitted": is_fitted,
        "_is_force_fitted": is_force_fitted,
        "fitting_data": fitting_data,
        "fitting_info": fitting_info,
    }

    return peak_properties


@NodeDecorator(id="span.basics.peaks", name="Peak finder node")
@controlled_wrapper(find_peaks, wrapper_attribute="__fnwrapped__")
def peak_finder(
    x_array: np.ndarray,
    y_array: np.ndarray,
    noise_level: Optional[int] = None,
    height: Optional[float] = None,
    threshold: Optional[float] = None,
    distance: Optional[float] = None,
    prominence: Optional[float] = None,
    width: Optional[float] = None,
    wlen: Optional[int] = None,
    rel_height: Optional[float] = None,
    plateau_size: Optional[int] = None,
) -> dict:
    peak_lst = []
    height = 0.05 * np.max(y_array) if height is None else height
    noise_level = 5000 if noise_level is None else noise_level

    # Make a copy of the input array
    y_array_copy = np.copy(y_array)

    # Find the peaks in the copy of the input array
    peaks, _ = find_peaks(
        y_array_copy,
        threshold=threshold,
        prominence=prominence,
        height=height,
        distance=distance,
        width=width,
        wlen=wlen,
        rel_height=rel_height,
        plateau_size=plateau_size,
    )

    # Calculate the standard deviation of peak prominences

    np.random.seed(seed=1)
    # Fit a normal distribution to the input array
    mu, std = norm.fit(y_array_copy)
    if peaks is not None:
        try:
            # Add noise to the input array
            noise = np.random.normal(
                mu / noise_level, std / noise_level, np.shape(y_array_copy)
            )
            y_array_copy = y_array_copy + noise

            # Find the minimums in the copy of the input array
            mins, _ = find_peaks(-1 * y_array_copy)

            # Iterate over the peaks
            for peak in peaks:
                # Calculate the prominences of the peak
                # Find the right minimum of the peak
                right_min = mins[np.argmax(mins > peak)]
                if right_min < peak:
                    right_min = len(y_array) - 1

                try:
                    # Find the left minimum of the peak
                    left_min = np.array(mins)[np.where(np.array(mins) < peak)][-1]
                except IndexError:
                    left_min = 0

                if height is None:
                    # If no height is specified, append the peak bounds to the peak list
                    peak_lst.append([left_min, peak, right_min])

                else:
                    # If a height is specified, append the peak bounds to the peak list
                    # if the peak's value is greater than the height
                    if y_array_copy[peak] > height:
                        peak_lst.append([left_min, peak, right_min])

        except ValueError:
            # If an error occurs when adding noise to the input array, add stronger noise and try again
            noise = np.random.normal(mu / 100, std / 100, np.shape(y_array_copy))
            y_array_copy = y_array_copy + noise
            mins, _ = find_peaks(-1 * y_array_copy)
            for peak in peaks:
                right_min = mins[np.argmax(mins > peak)]
                if right_min < peak:
                    right_min = len(y_array) - 1
                try:
                    left_min = np.array(mins)[np.where(np.array(mins) < peak)][-1]
                except IndexError:
                    left_min = 0
                if height is None:
                    # If no height is specified, append the peak bounds to the peak list
                    peak_lst.append([left_min, peak, right_min])
                else:
                    # If a height is specified, append the peak bounds to the peak list
                    # if the peak's value is greater than the height
                    if y_array_copy[peak] > height:
                        peak_lst.append([left_min, peak, right_min])

    peak_properties_list = []

    for peak_nr, peak in enumerate(peak_lst):
        peak_properties = compute_peak_properties(
            x_array=x_array, y_array=y_array, peak_indices=peak, peak_nr=peak_nr
        )
        peak_properties_list.append(peak_properties)

    return peak_properties_list


# ['Constant', 'Complex Constant', 'Linear', 'Quadratic', 'Polynomial',
# 'Spline', 'Gaussian', 'Gaussian-2D', 'Lorentzian', 'Split-Lorentzian', 'Voigt',
# 'PseudoVoigt', 'Moffat', 'Pearson4', 'Pearson7', 'StudentsT', 'Breit-Wigner', 'Log-Normal',
# 'Damped Oscillator', 'Damped Harmonic Oscillator', 'Exponential Gaussian', 'Skewed Gaussian',
# 'Skewed Voigt', 'Thermal Distribution', 'Doniach', 'Power Law', 'Exponential', 'Step',
# 'Rectangle', 'Expression']


class FittingModel(Enum):
    ComplexConstant = "Complex Constant"
    Linear = "Linear"
    Quadratic = "Quadratic"
    Polynomial = "Polynomial"
    Spline = "Spline"
    Gaussian = "Gaussian"
    Gaussian2D = "Gaussian-2D"
    Lorentzian = "Lorentzian"
    SplitLorentzian = "Split-Lorentzian"
    Voigt = "Voigt"
    PseudoVoigt = "PseudoVoigt"
    Moffat = "Moffat"
    Pearson4 = "Pearson4"
    Pearson7 = "Pearson7"
    StudentsT = "StudentsT"
    BreitWigner = "Breit-Wigner"
    LogNormal = "Log-Normal"
    DampedOscillator = "Damped Oscillator"
    DampedHarmonicOscillator = "Damped Harmonic Oscillator"
    ExponentialGaussian = "Exponential Gaussian"
    SkewedGaussian = "Skewed Gaussian"
    SkewedVoigt = "Skewed Voigt"
    ThermalDistribution = "Thermal Distribution"
    Doniach = "Doniach"
    PowerLaw = "Power Law"
    Exponential = "Exponential"
    Step = "Step"
    Rectangle = "Rectangle"
    Expression = "Expression"
    Constant = "Constant"

    @classmethod
    def default(cls):
        return cls.Gaussian.value


@NodeDecorator(id="span.basics.fit", name="Fit 1D")
def fit_1D(
    x_array: np.ndarray,
    y_array: np.ndarray,
    basic_peaks: List[PeakProperties],
    model_name: FittingModel = FittingModel.default(),
) -> List[PeakProperties]:
    # """
    # Fit a 1D model to the given data.

    # Parameters:
    #     peaks: dict
    #         Dictionary containing the data and information about the peaks.
    #     fitting_model: Optional[str]
    #         The model to use for fitting. Defaults to "Gaussian".
    #     preview: bool
    #         Whether to preview the fit with a plot. Defaults to True.
    #     color: Optional[Tuple[int, int, int] | str]
    #         Color for the plot.

    # Returns:
    #     Tuple[dict, Optional[Figure]]:
    #         A tuple containing a dictionary of evaluated components of the fit and additional information about the fit, and an optional figure for the plot.

    # """
    if isinstance(model_name, FittingModel):
        model_name = model_name.value
    peaks = copy.deepcopy(basic_peaks)
    y = y_array
    x = x_array
    # if is_sturated:
    #     if len(peaks['peaks']) == 2:
    #         peaks['peaks'] = [{
    #             "Peak #": 'peak1_',
    #             "Index": peaks['peaks'][0]['Ending index'] + int( (peaks['peaks'][1]['Initial index'] - peaks['peaks'][0]['Ending index'])/ 2),
    #             "Initial index": peaks['peaks'][0]['Ending index'],
    #             "Ending index": peaks['peaks'][1]['Initial index'],
    #             "Retention": np.NaN,
    #             "Area": np.NaN,
    #             "Height": y[peaks['peaks'][0]['Ending index'] + int( (peaks['peaks'][1]['Initial index'] - peaks['peaks'][0]['Ending index'])/ 2)],
    #             "Symmetricity": np.NaN,
    #             "Tailing": np.NaN,
    #             "FWHM": np.NaN,
    #             "Plate #": np.NaN,
    #             "Width":  x[peaks['peaks'][1]['Initial index']] - x[peaks['peaks'][0]['Ending index']],
    #             "is_fitted": False,
    #         }]
    #                     not_saturated_x = np.concatenate((x[:peaks['peaks'][0]['Ending index']-1], x[peaks['peaks'][1]['Initial index']+1:]))
    #         not_saturated_y = np.concatenate((y[:peaks['peaks'][0]['Ending index']-1], y[peaks['peaks'][1]['Initial index']+1:]))
    #     else:
    #         raise ValueError('invalid number of peak selection. Either the entire or two sides of the saturated peak should be selected')

    lowest_index = min(dictionary["i_index"] for dictionary in peaks)
    highest_index = max(dictionary["f_index"] for dictionary in peaks)

    # list of modelnames:
    # lmfit.models.__dict__['lmfit_models'].keys()
    # ['Constant', 'Complex Constant', 'Linear', 'Quadratic', 'Polynomial', 'Spline', 'Gaussian', 'Gaussian-2D', 'Lorentzian', 'Split-Lorentzian', 'Voigt', 'PseudoVoigt', 'Moffat', 'Pearson4', 'Pearson7', 'StudentsT', 'Breit-Wigner', 'Log-Normal', 'Damped Oscillator', 'Damped Harmonic Oscillator', 'Exponential Gaussian', 'Skewed Gaussian', 'Skewed Voigt', 'Thermal Distribution', 'Doniach', 'Power Law', 'Exponential', 'Step', 'Rectangle', 'Expression']
    # peak like models are:  GaussianModel, LorentzianModel, VoigtModel and their modified versions

    fitting_model = lmfit.models.__dict__["lmfit_models"][model_name]
    # bkg1 = lmfit.models.__dict__["lmfit_models"]["Spline"](prefix="baseline", xknots=np.concatenate((x[:lowest_index], x[highest_index:])))
    bkg2 = lmfit.models.__dict__["lmfit_models"]["Exponential"](prefix="baseline")

    f = bkg2

    pars = f.guess(y, x=x)
    for index, peak in enumerate(peaks):
        model = fitting_model(prefix=f"peak{index+1}_")
        pars.update(model.make_params())
        pars[f"peak{index+1}_center"].set(
            value=x[peak["index"]],
            min=x[peak["i_index"]],
            max=x[peak["f_index"]],
        )
        pars[f"peak{index+1}_sigma"].set(
            value=(x[peak["f_index"]] - x[peak["i_index"]]) / 2
        )
        pars[f"peak{index+1}_amplitude"].set(value=y[peak["index"]], min=0)

        if model_name == "Exponential Gaussian" or model_name == "Skewed Gaussian":
            pars[f"peak{index+1}_gamma"].set(value=1)

        f += model

    out = f.fit(y, pars, x=x)

    f = bkg2
    pars = f.guess(y, x=x)
    for index, peak in enumerate(peaks):
        model = fitting_model(prefix=f"peak{index+1}_")
        pars.update(model.make_params())
        pars[f"peak{index+1}_center"].set(
            value=out.__dict__["best_values"][f"peak{index+1}_center"],
            min=x[peak["i_index"]],
            max=x[peak["f_index"]],
        )
        pars[f"peak{index+1}_sigma"].set(
            value=(x[peak["f_index"]] - x[peak["i_index"]]) / 2
        )
        pars[f"peak{index+1}_amplitude"].set(
            value=out.__dict__["best_values"][f"peak{index+1}_amplitude"], min=0
        )

        if model_name == "Exponential Gaussian" or model_name == "Skewed Gaussian":
            pars[f"peak{index+1}_gamma"].set(
                value=out.__dict__["best_values"][f"peak{index+1}_gamma"]
            )

        f += model

    out = f.fit(y, pars, x=x)
    com = out.eval_components(x=x)
    info_dict = out.__dict__
    info_dict["model_name"] = model_name

    peak_properties_list = []

    for key in com.keys():
        if key != "baseline":
            y_array = com[key]
            peak_lst = [(0, np.argmax(y_array), len(y_array) - 1)]
            for peak_nr, peak in enumerate(peak_lst):
                peak_properties = compute_peak_properties(
                    x_array=x_array,
                    y_array=y_array,
                    peak_indices=peak,
                    peak_nr=peak_nr,
                    is_fitted=True,
                    fitting_data=com,
                    fitting_info=info_dict,
                )
                peak_properties_list.append(peak_properties)

    return peak_properties_list


# Define a mapping from "C0", "C1", etc., to CSS color names
color_map = {
    "C0": "blue",
    "C1": "orange",
    "C2": "green",
    "C3": "red",
    "C4": "purple",
    "C5": "brown",
    "C6": "pink",
    "C7": "gray",
    "C8": "olive",
    "C9": "cyan",
}


@NodeDecorator(id="span.basics.fit.plot", name="Plot fit 1D")
def plot_fitted_peaks(peaks: List[PeakProperties]) -> go.Figure:
    peak = peaks[0]
    x = peak["fitting_info"]["userkws"]["x"]
    # Extract data from peaks
    y = peak["fitting_info"]["data"]
    best_fit = peak["fitting_info"]["best_fit"]

    # Create a subplot with 1 row, 1 column, and a secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add the original data trace
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode="lines", name="original", line=dict(color=color_map["C0"])
        ),
        secondary_y=False,
    )

    # Add the best fit trace
    fig.add_trace(
        go.Scatter(
            x=x,
            y=best_fit,
            mode="lines",
            name="best_fit",
            line=dict(dash="dash", color=color_map["C1"]),
        ),
        secondary_y=False,
    )

    # Add the baseline and individual peak traces
    for key in peak["fitting_data"].keys():
        if key == "baseline":
            color = color_map["C2"]
        else:
            peak_number = int(re.search(r"\d+", key).group())
            color = color_map.get(
                f"C{peak_number + 2}", "black"
            )  # Default to black if not found

        trace = go.Scatter(
            x=x,
            y=peak["fitting_data"][key],
            mode="lines",
            name=key,
            line=dict(color=color),
        )
        fig.add_trace(trace, secondary_y=(key != "baseline"))

    # Update axes labels and legend
    fig.update_yaxes(title_text="Original", secondary_y=False)
    fig.update_yaxes(title_text="Baseline corrected", secondary_y=True)
    fig.update_layout(
        title={
            "text": f"{peak['fitting_info']['model_name']} model with fitting score = {np.round(peak['fitting_info']['rsquared'], 4)}",
            "x": 0.5,  # Center the title
            "xanchor": "center",
        },
    )

    return fig


PEAKS_NODE_SHELF = Shelf(
    nodes=[peak_finder, fit_1D, plot_fitted_peaks],
    subshelves=[],
    name="Peak analysis",
    description="Tools for the peak analysis of the spectra",
)
