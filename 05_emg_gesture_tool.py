import numpy as np


# ============================================================
# EMG GESTURE TOOL
# ============================================================

"""
Simulated EMG gesture classification for a
Biomedical Engineering AI Agent workshop.

Gestures:

REST  -> low muscle activity
OPEN  -> medium muscle activity
CLOSE -> high muscle activity

This file does NOT use an LLM.

It is a reliable biomedical engineering tool
that a future AI agent can call.
"""


# ============================================================
# GENERATE SIMULATED EMG
# ============================================================

def generate_gesture_emg(
    gesture,
    duration=2.0,
    sampling_rate=1000,
):
    """
    Generate a simulated EMG signal for a gesture.
    """

    gesture = gesture.upper().strip()

    valid_gestures = [
        "REST",
        "OPEN",
        "CLOSE",
    ]

    if gesture not in valid_gestures:

        raise ValueError(
            "Gesture must be REST, OPEN, or CLOSE."
        )

    number_of_samples = int(
        duration * sampling_rate
    )

    time = np.linspace(
        0,
        duration,
        number_of_samples,
        endpoint=False,
    )

    # --------------------------------------------------------
    # Use a fixed seed for reproducible workshop results
    # --------------------------------------------------------

    seeds = {
        "REST": 100,
        "OPEN": 200,
        "CLOSE": 300,
    }

    rng = np.random.default_rng(
        seeds[gesture]
    )

    # --------------------------------------------------------
    # Resting EMG noise
    # --------------------------------------------------------

    signal = rng.normal(
        0,
        0.05,
        number_of_samples,
    )

    # --------------------------------------------------------
    # Muscle activation window
    # --------------------------------------------------------

    activation = (
        (time >= 0.5)
        &
        (time < 1.5)
    )

    # --------------------------------------------------------
    # REST
    # --------------------------------------------------------

    if gesture == "REST":

        # Keep only low-level noise
        pass

    # --------------------------------------------------------
    # OPEN
    # --------------------------------------------------------

    elif gesture == "OPEN":

        signal[activation] = rng.normal(
            0,
            0.15,
            np.sum(activation),
        )

    # --------------------------------------------------------
    # CLOSE
    # --------------------------------------------------------

    elif gesture == "CLOSE":

        signal[activation] = rng.normal(
            0,
            0.35,
            np.sum(activation),
        )

    return time, signal


# ============================================================
# RMS
# ============================================================

def calculate_rms(signal):
    """
    Calculate Root Mean Square.
    """

    return float(
        np.sqrt(
            np.mean(
                signal ** 2
            )
        )
    )


# ============================================================
# MAV
# ============================================================

def calculate_mav(signal):
    """
    Calculate Mean Absolute Value.
    """

    return float(
        np.mean(
            np.abs(signal)
        )
    )


# ============================================================
# CLASSIFY EMG GESTURE
# ============================================================

def classify_gesture(gesture):
    """
    Analyze an EMG pattern and classify it.

    Returns structured information that can
    later be consumed by an AI agent.
    """

    gesture = gesture.upper().strip()

    # --------------------------------------------------------
    # Generate simulated EMG
    # --------------------------------------------------------

    time, signal = generate_gesture_emg(
        gesture
    )

    # --------------------------------------------------------
    # Analyze active muscle window
    # --------------------------------------------------------

    activation = (
        (time >= 0.5)
        &
        (time < 1.5)
    )

    active_signal = signal[
        activation
    ]

    # --------------------------------------------------------
    # Calculate biomedical features
    # --------------------------------------------------------

    rms = calculate_rms(
        active_signal
    )

    mav = calculate_mav(
        active_signal
    )

    # --------------------------------------------------------
    # Gesture classification
    #
    # These thresholds are intentionally simple
    # for the educational simulator.
    # --------------------------------------------------------

    if rms < 0.08:

        predicted_gesture = "REST"

    elif rms < 0.25:

        predicted_gesture = "OPEN"

    else:

        predicted_gesture = "CLOSE"

    # --------------------------------------------------------
    # Map gesture to prosthetic action
    # --------------------------------------------------------

    if predicted_gesture == "REST":

        prosthetic_action = "REST"

    elif predicted_gesture == "OPEN":

        prosthetic_action = "OPEN"

    else:

        prosthetic_action = "CLOSE"

    # --------------------------------------------------------
    # Return structured result
    # --------------------------------------------------------

    return {

        "input_gesture": gesture,

        "rms": round(
            rms,
            4,
        ),

        "mav": round(
            mav,
            4,
        ),

        "predicted_gesture": predicted_gesture,

        "prosthetic_action": prosthetic_action,

        "activation_start_seconds": 0.5,

        "activation_end_seconds": 1.5,

        "activation_duration_seconds": 1.0,
    }


# ============================================================
# WORKSHOP DEMONSTRATION
# ============================================================

def run_demo():

    print()
    print("======================================")
    print("       EMG GESTURE CLASSIFIER")
    print("======================================")

    print()
    print(
        "Testing three simulated EMG patterns..."
    )

    gestures = [
        "REST",
        "OPEN",
        "CLOSE",
    ]

    for gesture in gestures:

        result = classify_gesture(
            gesture
        )

        print()
        print("--------------------------------------")
        print(
            "Simulated EMG:",
            gesture
        )
        print("--------------------------------------")

        print(
            "RMS:",
            result["rms"]
        )

        print(
            "MAV:",
            result["mav"]
        )

        print(
            "Predicted gesture:",
            result["predicted_gesture"]
        )

        print(
            "Prosthetic action:",
            result["prosthetic_action"]
        )

    print()
    print("======================================")
    print("       CLASSIFICATION COMPLETE")
    print("======================================")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_demo()