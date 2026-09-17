"""
07_true_biomedical_agent.py

Final workshop demonstration:

User selects intention
        ↓
Simulated EMG
        ↓
Analyze
        ↓
Classify
        ↓
Gemma AI Decision
        ↓
Prosthetic Hand

Educational simulation only.
No real biomedical device is being controlled.
"""

import asyncio
import importlib.util
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

from autogen_core.models import ModelInfo, UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient


# ============================================================
# LOAD WORKSHOP MODULES
# ============================================================

def load_module(filename, module_name):

    file_path = Path(__file__).parent / filename

    spec = importlib.util.spec_from_file_location(
        module_name,
        file_path
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not load {filename}"
        )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


emg_module = load_module(
    "05_emg_gesture_tool.py",
    "emg_gesture_module"
)

hand_module = load_module(
    "04_prosthetic_hand.py",
    "prosthetic_hand_module"
)


# ============================================================
# USER SELECTS THE MUSCLE INTENTION
# ============================================================

def get_user_gesture():

    print()
    print("==============================================")
    print("SELECT SIMULATED MUSCLE INTENTION")
    print("==============================================")
    print()
    print("1. REST")
    print("2. OPEN")
    print("3. CLOSE")
    print()

    while True:

        choice = input(
            "Enter your choice (1/2/3): "
        ).strip()

        if choice == "1":
            return "REST"

        if choice == "2":
            return "OPEN"

        if choice == "3":
            return "CLOSE"

        print()
        print("Please enter 1, 2 or 3.")


# ============================================================
# GENERATE AND ANALYZE EMG
# ============================================================

def analyze_emg(gesture):

    # Generate simulated EMG corresponding
    # to the selected muscle intention.

    time, signal = emg_module.generate_gesture_emg(
        gesture
    )

    # Calculate biomedical signal features.

    rms = emg_module.calculate_rms(
        signal
    )

    mav = emg_module.calculate_mav(
        signal
    )

    return {
        "gesture_input": gesture,

        "rms": round(
            float(rms),
            4
        ),

        "mav": round(
            float(mav),
            4
        )
    }


# ============================================================
# CLASSIFY GESTURE FROM EMG
# ============================================================

def classify_emg_gesture(emg_result):

    rms = emg_result["rms"]

    if rms < 0.08:

        gesture = "REST"

    elif rms < 0.25:

        gesture = "OPEN"

    else:

        gesture = "CLOSE"

    return {
        "predicted_gesture": gesture,
        "rms_used": rms
    }


# ============================================================
# ASK GEMMA FOR DECISION
# ============================================================

async def ask_agent_to_decide(
    emg_result,
    classifier_result
):

    model_client = OllamaChatCompletionClient(

        model="gemma4:e4b",

        host="http://localhost:11434",

        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=True,
            family="unknown"
        )
    )

    prompt = f"""
You are the AI decision-making component
of an educational biomedical engineering system.

The system analyzed a simulated EMG signal.

EMG analysis:
{json.dumps(emg_result, indent=2)}

Gesture classifier:
{json.dumps(classifier_result, indent=2)}

Choose the appropriate command for the
virtual prosthetic hand.

Allowed commands:

REST
OPEN
CLOSE

Return ONLY JSON.

Example:

{{"decision":"OPEN"}}

Do not provide explanations.
"""

    response = await model_client.create(

        messages=[
            UserMessage(
                content=prompt,
                source="student"
            )
        ],

        extra_create_args={
            "think": False
        }
    )

    await model_client.close()

    return response.content


# ============================================================
# EXTRACT GEMMA DECISION
# ============================================================

def extract_decision(response):

    try:

        data = json.loads(
            response
        )

        decision = data["decision"].upper().strip()

        if decision in [
            "REST",
            "OPEN",
            "CLOSE"
        ]:

            return decision

    except Exception:
        pass

    match = re.search(
        r"\b(REST|OPEN|CLOSE)\b",
        response.upper()
    )

    if match:

        return match.group(1)

    raise ValueError(
        "Gemma returned an invalid decision:\n"
        + str(response)
    )


# ============================================================
# CONTROL PROSTHETIC HAND
# ============================================================

def control_hand(command):

    return hand_module.control_prosthetic_hand(
        command
    )


# ============================================================
# FINAL HAND VISUALIZATION
# ============================================================

def show_final_hand(command):

    # Close temporary figures created by File 04.

    plt.close("all")

    fig, ax = plt.subplots(
        figsize=(8, 8)
    )

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)

    ax.set_aspect("equal")

    ax.axis("off")

    # --------------------------------------------------------
    # PALM
    # --------------------------------------------------------

    palm = FancyBboxPatch(
        (3.2, 2.0),
        3.6,
        4.5,
        boxstyle=(
            "round,pad=0.08,"
            "rounding_size=0.35"
        ),
        linewidth=2
    )

    ax.add_patch(palm)

    # --------------------------------------------------------
    # OPEN HAND
    # --------------------------------------------------------

    if command == "OPEN":

        # Thumb
        ax.plot(
            [3.3, 1.6],
            [5.0, 7.0],
            linewidth=18,
            solid_capstyle="round"
        )

        # Index
        ax.plot(
            [4.0, 4.0],
            [6.0, 10.0],
            linewidth=18,
            solid_capstyle="round"
        )

        # Middle
        ax.plot(
            [5.0, 5.0],
            [6.0, 10.7],
            linewidth=18,
            solid_capstyle="round"
        )

        # Ring
        ax.plot(
            [6.0, 6.0],
            [6.0, 10.2],
            linewidth=18,
            solid_capstyle="round"
        )

        # Little
        ax.plot(
            [6.8, 6.8],
            [6.0, 9.0],
            linewidth=18,
            solid_capstyle="round"
        )

    # --------------------------------------------------------
    # CLOSED HAND
    # --------------------------------------------------------

    elif command == "CLOSE":

        for x in [
            4.0,
            4.8,
            5.6,
            6.4
        ]:

            ax.plot(
                [x, x + 0.6],
                [6.0, 6.5],
                linewidth=22,
                solid_capstyle="round"
            )

        # Thumb
        ax.plot(
            [3.5, 5.0],
            [5.0, 5.7],
            linewidth=22,
            solid_capstyle="round"
        )

    # --------------------------------------------------------
    # RESTING HAND
    # --------------------------------------------------------

    else:

        # Thumb
        ax.plot(
            [3.5, 2.0],
            [5.0, 6.0],
            linewidth=18,
            solid_capstyle="round"
        )

        for x in [
            4.0,
            4.8,
            5.6,
            6.4
        ]:

            ax.plot(
                [x, x + 0.3],
                [6.0, 7.0],
                linewidth=18,
                solid_capstyle="round"
            )

    # --------------------------------------------------------
    # WRIST
    # --------------------------------------------------------

    wrist = Rectangle(
        (4.1, 0.2),
        1.8,
        1.9,
        linewidth=2
    )

    ax.add_patch(wrist)

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    ax.text(
        5,
        11.5,
        "AI-CONTROLLED PROSTHETIC HAND",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold"
    )

    # --------------------------------------------------------
    # AI COMMAND
    # --------------------------------------------------------

    ax.text(
        5,
        10.9,
        f"AI COMMAND: {command}",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold"
    )

    # --------------------------------------------------------
    # FINAL STATE
    # --------------------------------------------------------

    ax.text(
        5,
        -0.4,
        f"FINAL HAND STATE: {command}",
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold"
    )

    plt.tight_layout()

    # Keep window open.

    plt.show(block=True)


# ============================================================
# MAIN
# ============================================================

async def main():

    print()
    print("==============================================")
    print("      AI AGENTS FOR BIOMEDICAL ENGINEERING")
    print("==============================================")
    print()
    print("EMG → AI AGENT → PROSTHETIC HAND")
    print()

    # --------------------------------------------------------
    # STEP 0 — USER INPUT
    # --------------------------------------------------------

    selected_gesture = get_user_gesture()

    print()
    print(
        f"Selected intention: {selected_gesture}"
    )

    # --------------------------------------------------------
    # STEP 1 — OBSERVE
    # --------------------------------------------------------

    print()
    print("----------------------------------------------")
    print("STEP 1 — OBSERVE")
    print("----------------------------------------------")

    print(
        "Generating simulated EMG..."
    )

    emg_result = analyze_emg(
        selected_gesture
    )

    print()
    print(
        f"Input intention: "
        f"{selected_gesture}"
    )

    # --------------------------------------------------------
    # STEP 2 — ANALYZE
    # --------------------------------------------------------

    print()
    print("----------------------------------------------")
    print("STEP 2 — ANALYZE")
    print("----------------------------------------------")

    print(
        f"EMG RMS: "
        f"{emg_result['rms']}"
    )

    print(
        f"EMG MAV: "
        f"{emg_result['mav']}"
    )

    # --------------------------------------------------------
    # STEP 3 — CLASSIFY
    # --------------------------------------------------------

    print()
    print("----------------------------------------------")
    print("STEP 3 — CLASSIFY")
    print("----------------------------------------------")

    classifier_result = classify_emg_gesture(
        emg_result
    )

    print()
    print(
        "Classifier result: "
        f"{classifier_result['predicted_gesture']}"
    )

    # --------------------------------------------------------
    # STEP 4 — GEMMA
    # --------------------------------------------------------

    print()
    print("----------------------------------------------")
    print("STEP 4 — AI AGENT DECISION")
    print("----------------------------------------------")

    print()
    print(
        "Gemma is making the decision..."
    )

    ai_response = await ask_agent_to_decide(
        emg_result,
        classifier_result
    )

    print()
    print("Gemma response:")

    print(ai_response)

    decision = extract_decision(
        ai_response
    )

    print()
    print(
        f"AI decision: {decision}"
    )

    # --------------------------------------------------------
    # STEP 5 — ACT
    # --------------------------------------------------------

    print()
    print("----------------------------------------------")
    print("STEP 5 — ACT")
    print("----------------------------------------------")

    print()
    print(
        f"Sending {decision} "
        "command to prosthetic hand..."
    )

    hand_result = control_hand(
        decision
    )

    print()
    print(
        "Prosthetic hand response:"
    )

    print(hand_result)

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("==============================================")
    print("          AGENT CYCLE COMPLETE")
    print("==============================================")

    print()
    print(
        f"Input intention : {selected_gesture}"
    )

    print(
        f"EMG RMS         : "
        f"{emg_result['rms']}"
    )

    print(
        f"Classifier      : "
        f"{classifier_result['predicted_gesture']}"
    )

    print(
        f"AI decision     : {decision}"
    )

    print(
        f"Hand state      : "
        f"{hand_result.get('hand_state', decision)}"
    )

    print()
    print(
        "OBSERVE → ANALYZE → DECIDE → ACT"
    )

    print()
    print(
        "Close the hand visualization window "
        "when finished."
    )

    # --------------------------------------------------------
    # FINAL VISUALIZATION
    # --------------------------------------------------------

    show_final_hand(
        decision
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())