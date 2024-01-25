from type_checker.decorators import enforce_strict_types


@enforce_strict_types
def estimate_threshold_classification_from_pulse_and_resolution(ref_pulse_ns: int, ref_resolution_cm: int):
    three_times_pulse_width = 3 * (ref_pulse_ns / 10)
    forty_points_spacing_meters = 40 * (ref_resolution_cm / 100)
    if three_times_pulse_width < 10:
        treshold_classification_meters = 10.0
    elif three_times_pulse_width > 50:
        treshold_classification_meters = min(three_times_pulse_width, forty_points_spacing_meters)
    else:  # 3* pulse width between 10 and 50
        treshold_classification_meters = max(three_times_pulse_width, forty_points_spacing_meters)
    return treshold_classification_meters
