import numpy as np
import matplotlib.pyplot as plt


def generate_emg(duration=2, sampling_rate=1000):
    """
    Generate a simulated EMG signal.

    0.0 - 0.5 sec : relaxed
    0.5 - 1.5 sec : muscle active
    1.5 - 2.0 sec : relaxed
    """

    number_of_samples = int(duration * sampling_rate)

    time = np.linspace(
        0,
        duration,
        number_of_samples,
        endpoint=False
    )

    # Low-level EMG when the muscle is relaxed
    emg_signal = np.random.normal(
        0,
        0.05,
        number_of_samples
    )

    # Muscle activation
    activation = (time >= 0.5) & (time < 1.5)

    emg_signal[activation] = np.random.normal(
        0,
        0.25,
        np.sum(activation)
    )

    return time, emg_signal


def calculate_rms(signal):
    """Calculate Root Mean Square."""

    return np.sqrt(np.mean(signal ** 2))


def calculate_mav(signal):
    """Calculate Mean Absolute Value."""

    return np.mean(np.abs(signal))


def calculate_windowed_rms(signal, sampling_rate, window_size=0.1):
    """
    Calculate RMS over short windows.

    window_size is in seconds.
    """

    samples_per_window = int(
        window_size * sampling_rate
    )

    number_of_windows = len(signal) // samples_per_window

    rms_values = []
    window_times = []

    for i in range(number_of_windows):

        start = i * samples_per_window
        end = start + samples_per_window

        window = signal[start:end]

        rms = calculate_rms(window)

        rms_values.append(rms)

        window_times.append(
            (start + end) / 2 / sampling_rate
        )

    return (
        np.array(window_times),
        np.array(rms_values)
    )


def detect_muscle_activation(
    time,
    signal,
    sampling_rate=1000,
    window_size=0.1
):
    """
    Detect muscle activation using windowed RMS.

    The baseline is estimated from the first
    0.5 seconds of the simulated signal.
    """

    rms_time, rms_values = calculate_windowed_rms(
        signal,
        sampling_rate,
        window_size
    )

    # Baseline = first 0.5 seconds
    baseline = rms_values[rms_time < 0.5]

    baseline_mean = np.mean(baseline)
    baseline_std = np.std(baseline)

    # Activation threshold
    threshold = baseline_mean + (3 * baseline_std)

    active_windows = rms_values > threshold

    active_times = rms_time[active_windows]

    if len(active_times) == 0:
        return None, None, threshold, rms_time, rms_values

    activation_start = (
        active_times[0] - window_size / 2
    )

    activation_end = (
        active_times[-1] + window_size / 2
    )

    return (
        activation_start,
        activation_end,
        threshold,
        rms_time,
        rms_values
    )


def main():

    # Generate EMG
    time, emg = generate_emg()

    # Overall features
    rms = calculate_rms(emg)
    mav = calculate_mav(emg)

    # Detect activation
    (
        activation_start,
        activation_end,
        threshold,
        rms_time,
        rms_values
    ) = detect_muscle_activation(
        time,
        emg
    )

    print("===================================")
    print("       EMG ANALYSIS TOOL")
    print("===================================")

    print("\n--- SIGNAL INFORMATION ---")

    print(
        "Number of samples:",
        len(emg)
    )

    print(
        "Sampling rate:",
        "1000 Hz"
    )

    print(
        "Signal duration:",
        time[-1],
        "seconds"
    )

    print("\n--- EMG FEATURES ---")

    print(
        "Overall RMS:",
        round(rms, 4)
    )

    print(
        "Overall MAV:",
        round(mav, 4)
    )

    print("\n--- MUSCLE ACTIVATION ---")

    print(
        "RMS activation threshold:",
        round(threshold, 4)
    )

    if activation_start is not None:

        print(
            "Muscle activation detected."
        )

        print(
            "Approximate activation start:",
            round(activation_start, 2),
            "seconds"
        )

        print(
            "Approximate activation end:",
            round(activation_end, 2),
            "seconds"
        )

        print(
            "Approximate activation duration:",
            round(
                activation_end - activation_start,
                2
            ),
            "seconds"
        )

    else:

        print(
            "No significant muscle activation detected."
        )

    # -----------------------------
    # Plot raw EMG
    # -----------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        time,
        emg,
        linewidth=0.8
    )

    if activation_start is not None:

        plt.axvline(
            activation_start,
            linestyle="--",
            label="Detected Start"
        )

        plt.axvline(
            activation_end,
            linestyle="--",
            label="Detected End"
        )

    plt.xlabel("Time (seconds)")
    plt.ylabel("EMG Amplitude")

    plt.title(
        "Simulated EMG Signal"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()

    # -----------------------------
    # Plot RMS
    # -----------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        rms_time,
        rms_values,
        linewidth=1.5
    )

    plt.axhline(
        threshold,
        linestyle="--",
        label="Activation Threshold"
    )

    plt.xlabel("Time (seconds)")
    plt.ylabel("Windowed RMS")

    plt.title(
        "EMG Windowed RMS and Activation Threshold"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()