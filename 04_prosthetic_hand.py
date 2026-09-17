import matplotlib.pyplot as plt


# ============================================================
# PROSTHETIC HAND STATE
# ============================================================

hand_state = "REST"


# ============================================================
# DRAW THE PROSTHETIC HAND
# ============================================================

def draw_hand(state):
    """
    Draw a simple virtual prosthetic hand based
    on the current command.
    """

    plt.clf()

    # --------------------------------------------------------
    # Hand position
    # --------------------------------------------------------

    palm_x = 0
    palm_y = 0

    # --------------------------------------------------------
    # Palm
    # --------------------------------------------------------

    palm = plt.Rectangle(
        (-0.8, -1.0),
        1.6,
        2.2,
        fill=False,
        linewidth=3,
    )

    plt.gca().add_patch(palm)

    # --------------------------------------------------------
    # Finger positions
    # --------------------------------------------------------

    if state == "CLOSE":

        # Closed fingers
        fingers = [
            (-0.65, 0.9, 1.0, 0.15),
            (-0.25, 0.9, 1.0, 0.15),
            (0.15, 0.9, 1.0, 0.15),
            (0.55, 0.8, 0.8, 0.15),
        ]

    else:

        # Open fingers
        fingers = [
            (-0.65, 1.1, 0.2, 1.2),
            (-0.25, 1.1, 0.2, 1.5),
            (0.15, 1.1, 0.2, 1.6),
            (0.55, 1.0, 0.2, 1.3),
        ]

    # --------------------------------------------------------
    # Draw fingers
    # --------------------------------------------------------

    for x, y, width, height in fingers:

        finger = plt.Rectangle(
            (x, y),
            width,
            height,
            fill=False,
            linewidth=3,
        )

        plt.gca().add_patch(finger)

    # --------------------------------------------------------
    # Thumb
    # --------------------------------------------------------

    if state == "CLOSE":

        thumb = plt.Line2D(
            [-0.8, -0.2],
            [0.3, 0.7],
            linewidth=5,
        )

    else:

        thumb = plt.Line2D(
            [-0.8, -1.3],
            [0.2, 0.8],
            linewidth=5,
        )

    plt.gca().add_line(thumb)

    # --------------------------------------------------------
    # Display state
    # --------------------------------------------------------

    if state == "OPEN":

        title = "PROSTHETIC HAND — OPEN"

    elif state == "CLOSE":

        title = "PROSTHETIC HAND — CLOSED"

    else:

        title = "PROSTHETIC HAND — REST"

    plt.title(
        title,
        fontsize=18,
        fontweight="bold",
    )

    plt.text(
        0,
        -1.7,
        f"Command: {state}",
        ha="center",
        fontsize=14,
    )

    plt.xlim(-2, 2)

    plt.ylim(-2, 3)

    plt.axis("off")

    plt.tight_layout()

    plt.draw()

    plt.pause(0.1)


# ============================================================
# PROSTHETIC HAND CONTROL TOOL
# ============================================================

def control_prosthetic_hand(command):
    """
    Control the virtual prosthetic hand.

    Commands:
        OPEN
        CLOSE
        REST
    """

    global hand_state

    command = command.upper().strip()

    if command not in ["OPEN", "CLOSE", "REST"]:

        return {
            "success": False,
            "command": command,
            "hand_state": hand_state,
            "message": (
                "Invalid command. "
                "Use OPEN, CLOSE, or REST."
            ),
        }

    hand_state = command

    draw_hand(hand_state)

    return {
        "success": True,
        "command": command,
        "hand_state": hand_state,
        "message": (
            f"Prosthetic hand command "
            f"{command} executed."
        ),
    }


# ============================================================
# SIMULATOR
# ============================================================

def main():

    print()
    print("======================================")
    print("     PROSTHETIC HAND SIMULATOR")
    print("======================================")

    print()
    print("Available commands:")
    print("  OPEN")
    print("  CLOSE")
    print("  REST")
    print("  EXIT")

    # Create simulator window
    plt.figure(
        figsize=(6, 7)
    )

    draw_hand("REST")

    while True:

        print()

        command = input(
            "Enter prosthetic hand command: "
        ).strip().upper()

        if command == "EXIT":

            break

        result = control_prosthetic_hand(
            command
        )

        print()

        print(
            "Simulator response:"
        )

        print(result)

    plt.close()

    print()
    print("Prosthetic hand simulator stopped.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()