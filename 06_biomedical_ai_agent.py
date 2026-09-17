import asyncio
import ast
import importlib.util
import json
import subprocess
from pathlib import Path

from autogen_core import CancellationToken
from autogen_core.models import ModelInfo, UserMessage
from autogen_core.tools import FunctionTool
from autogen_ext.models.ollama import OllamaChatCompletionClient


# ============================================================
# LOAD EXISTING MODULES
# ============================================================

def load_module(filename, module_name):

    file_path = Path(__file__).parent / filename

    spec = importlib.util.spec_from_file_location(
        module_name,
        file_path,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not load {filename}"
        )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


emg_module = load_module(
    "03_emg_tool.py",
    "emg_module",
)

gesture_module = load_module(
    "05_emg_gesture_tool.py",
    "gesture_module",
)

hand_module = load_module(
    "04_prosthetic_hand.py",
    "hand_module",
)


# ============================================================
# BIOMEDICAL AGENT TOOL
# ============================================================

def operate_prosthetic_hand() -> dict:
    """
    Complete biomedical control pipeline.

    1. Generate/analyze EMG
    2. Classify the muscle gesture
    3. Send the corresponding command
       to the prosthetic hand simulator

    This function is intentionally deterministic so
    the workshop demonstration is reliable.
    """

    # --------------------------------------------------------
    # STEP 1 — EMG ANALYSIS
    # --------------------------------------------------------

    time, emg = emg_module.generate_emg()

    rms = emg_module.calculate_rms(emg)

    mav = emg_module.calculate_mav(emg)

    (
        activation_start,
        activation_end,
        threshold,
        rms_time,
        rms_values,
    ) = emg_module.detect_muscle_activation(
        time,
        emg,
    )

    # --------------------------------------------------------
    # STEP 2 — DETERMINE GESTURE
    # --------------------------------------------------------

    if rms < 0.08:

        gesture = "REST"

    elif rms < 0.25:

        gesture = "OPEN"

    else:

        gesture = "CLOSE"

    # --------------------------------------------------------
    # STEP 3 — CONTROL PROSTHETIC HAND
    # --------------------------------------------------------

    hand_result = hand_module.control_prosthetic_hand(
        gesture
    )

    # --------------------------------------------------------
    # RETURN COMPLETE SYSTEM RESULT
    # --------------------------------------------------------

    return {

        "emg": {

            "rms": round(
                float(rms),
                4,
            ),

            "mav": round(
                float(mav),
                4,
            ),

            "activation_detected": (
                activation_start is not None
            ),

            "activation_start_seconds": (
                round(
                    float(activation_start),
                    3,
                )
                if activation_start is not None
                else None
            ),

            "activation_end_seconds": (
                round(
                    float(activation_end),
                    3,
                )
                if activation_end is not None
                else None
            ),
        },

        "gesture": gesture,

        "prosthetic_action": gesture,

        "hand_result": hand_result,
    }


# ============================================================
# GEMMA DECISION
# ============================================================

async def main():

    print()
    print("==============================================")
    print("     BIOMEDICAL ENGINEERING AI AGENT")
    print("==============================================")

    print()
    print("Architecture:")
    print()
    print("EMG → AI Agent → Biomedical Tool →")
    print("Gesture → Prosthetic Hand")
    print()

    # --------------------------------------------------------
    # GEMMA CLIENT
    # --------------------------------------------------------

    model_client = OllamaChatCompletionClient(

        model="gemma4:e4b",

        host="http://localhost:11434",

        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=True,
            family="unknown",
        ),
    )

    # --------------------------------------------------------
    # CREATE THE BIOMEDICAL TOOL
    # --------------------------------------------------------

    prosthetic_tool = FunctionTool(

        operate_prosthetic_hand,

        description=(
            "Operate a simulated EMG-controlled "
            "prosthetic hand. The tool analyzes the "
            "EMG signal, determines the muscle gesture "
            "and performs the corresponding prosthetic "
            "hand action. Use this tool when the user "
            "asks the system to operate the prosthetic "
            "hand from EMG activity."
        ),
    )

    # --------------------------------------------------------
    # STUDENT REQUEST
    # --------------------------------------------------------

    student_request = UserMessage(

        content=(
            "Operate the prosthetic hand using the "
            "simulated EMG signal. Analyze the signal, "
            "determine the appropriate gesture, and "
            "execute the corresponding hand action."
        ),

        source="user",
    )

    print("----------------------------------------------")
    print("STUDENT REQUEST")
    print("----------------------------------------------")

    print(student_request.content)

    # --------------------------------------------------------
    # AI AGENT DECISION
    # --------------------------------------------------------

    print()
    print("----------------------------------------------")
    print("AI AGENT")
    print("----------------------------------------------")

    print(
        "Gemma is deciding which biomedical "
        "tool to use..."
    )

    cancellation_token = CancellationToken()

    result = await model_client.create(

        messages=[
            student_request
        ],

        tools=[
            prosthetic_tool
        ],

        tool_choice=prosthetic_tool,

        extra_create_args={
            "think": False
        },

        cancellation_token=cancellation_token,
    )

    # --------------------------------------------------------
    # TOOL CALL
    # --------------------------------------------------------

    print()
    print("==============================================")
    print("          AGENT TOOL CALL")
    print("==============================================")

    tool_result = None

    for tool_call in result.content:

        print()
        print("Selected tool:")
        print(tool_call.name)

        print()
        print("Arguments:")
        print(tool_call.arguments)

        # ----------------------------------------------------
        # EXECUTE TOOL
        # ----------------------------------------------------

        print()
        print("----------------------------------------------")
        print("EXECUTING BIOMEDICAL PIPELINE")
        print("----------------------------------------------")

        arguments = json.loads(
            tool_call.arguments
        )

        execution_result = await prosthetic_tool.run_json(

            arguments,

            cancellation_token,
        )

        result_string = (
            prosthetic_tool.return_value_as_string(
                execution_result
            )
        )

        # Convert Python dictionary string safely.
        tool_result = ast.literal_eval(
            result_string
        )

        print()
        print("EMG RMS:")
        print(tool_result["emg"]["rms"])

        print()
        print("EMG MAV:")
        print(tool_result["emg"]["mav"])

        print()
        print("Muscle activation detected:")
        print(
            tool_result["emg"][
                "activation_detected"
            ]
        )

        print()
        print("Gesture:")
        print(tool_result["gesture"])

        print()
        print("Prosthetic action:")
        print(tool_result["prosthetic_action"])

        print()
        print("Hand response:")
        print(tool_result["hand_result"])

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print()
    print("==============================================")
    print("           AGENT EXECUTION COMPLETE")
    print("==============================================")

    print()
    print("EMG → Gesture → Prosthetic Hand")

    print()
    print(
        f"Final hand state: "
        f"{tool_result['hand_result']['hand_state']}"
    )

    print()
    print(
        "The AI agent successfully connected "
        "the biomedical signal-processing tool "
        "to the prosthetic-hand simulator."
    )

    await model_client.close()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())