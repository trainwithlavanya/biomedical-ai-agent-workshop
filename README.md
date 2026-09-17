AI AGENTS FOR BIOMEDICAL ENGINEERING From EMG Signals to Intelligent
Prosthetic Hand Control

This workshop demonstrates how AI Agents can be used in a biomedical
engineering application.

Instead of building a simple chatbot, we will build a system that can: -
Generate simulated EMG signals - Analyze muscle activity - Recognize
simple hand gestures - Make an AI-based decision - Control a simulated
prosthetic hand

WHAT ARE WE BUILDING?

The complete workflow is:

Human Muscle ↓ EMG Signal ↓ Signal Analysis ↓ Gesture Classification ↓
AI Agent Decision ↓ Simulated Prosthetic Hand

The AI Agent follows:

OBSERVE → ANALYZE → DECIDE → ACT

SOFTWARE REQUIREMENTS

The following environment was used and tested for this workshop.

Visual Studio Code: 1.132.0 
Python: 3.14.7 
pip: 26.2.1 
Ollama: 0.34.0
Gemma 4 E4B: Local model 
AutoGen AgentChat: 0.7.5 
NumPy: 2.5.3
Matplotlib: 3.11.2

Using the same versions can help students reproduce the workshop
environment.

STEP 1 — INSTALL VISUAL STUDIO CODE

Download Visual Studio Code from: https://code.visualstudio.com/download

Recommended version used for this workshop: Visual Studio Code 1.132.0

After installing VS Code: 1. Open Visual Studio Code. 2. Open the
Extensions panel. 3. Search for: Python 4. Install the Python extension
by Microsoft.

STEP 2 — INSTALL PYTHON

Download Python from: https://www.python.org/downloads/

Version used for this workshop: Python 3.14.7

During installation on Windows, make sure: Add Python to PATH is
selected.

Verify the installation:

python –version

Expected: Python 3.14.7

STEP 3 — INSTALL OLLAMA

Download Ollama from: https://ollama.com/download

Version used for this workshop: Ollama 0.34.0

After installation, verify:

ollama –version

Expected: ollama version 0.34.0

STEP 4 — DOWNLOAD GEMMA 4 E4B

This workshop uses Gemma 4 E4B as the local AI model.

Open the VS Code terminal and run:

ollama pull gemma4:e4b

Check the installed models:

ollama list

You should see: gemma4:e4b

Ollama runs the model locally on your computer.

STEP 5 — OPEN THE WORKSHOP PROJECT

Open this repository in VS Code.

Project structure:

biomedical-ai-agent-workshop/ │ ├── 03_emg_tool.py ├──
04_prosthetic_hand.py ├── 05_emg_gesture_tool.py ├──
06_biomedical_ai_agent.py ├── 07_true_biomedical_agent.py └── README.md

STEP 6 — CREATE A VIRTUAL ENVIRONMENT

Open the VS Code terminal.

Create the virtual environment:

python -m venv .venv

Activate it on Windows:

.venv

You should see: (.venv)

at the beginning of the terminal.

STEP 7 — INSTALL AUTOGEN

Install AutoGen AgentChat and the Ollama extension:

python -m pip install -U “autogen-agentchat” “autogen-ext[ollama]”

The tested AutoGen version is: 0.7.5

STEP 8 — INSTALL NUMPY

NumPy is used for numerical calculations and EMG signal processing.

Install:

python -m pip install numpy

Test:

python -c “import numpy; print(numpy.__version__)”

Tested version: 2.5.3

STEP 9 — INSTALL MATPLOTLIB

Matplotlib is used to visualize: - EMG signals - Muscle activity - The
simulated prosthetic hand

Install:

python -m pip install matplotlib

Test:

python -c “import matplotlib; print(matplotlib.__version__)”

Tested version: 3.11.2

STEP 10 — VERIFY THE ENVIRONMENT

Python:

python –version

Expected: Python 3.14.7

pip:

python -m pip –version

Expected pip version: 26.2.1

Ollama:

ollama –version

Expected: 0.34.0

NumPy:

python -c “import numpy; print(‘NumPy:’, numpy.__version__)”

Expected: NumPy: 2.5.3

Matplotlib:

python -c “import matplotlib; print(‘Matplotlib:’,
matplotlib.__version__)”

Expected: Matplotlib: 3.11.2

AutoGen:

python -m pip show autogen-agentchat

Check that the version is: Version: 0.7.5

WORKSHOP FILES

03_emg_tool.py

This file introduces simulated EMG signals.

It: - Generates an EMG signal - Calculates RMS - Calculates MAV -
Detects muscle activation - Displays the EMG signal using Matplotlib

Run:

python 03_emg_tool.py

04_prosthetic_hand.py

This file introduces the virtual prosthetic hand.

The hand can perform:

OPEN CLOSE REST

Run:

python 04_prosthetic_hand.py

05_emg_gesture_tool.py

This file connects EMG activity with simple hand gestures.

The simulated gestures are:

REST OPEN CLOSE

The program analyzes the EMG signal and classifies the gesture.

Run:

python 05_emg_gesture_tool.py

06_biomedical_ai_agent.py

This file introduces the AI Agent into the biomedical workflow.

The system demonstrates:

OBSERVE ↓ ANALYZE ↓ DECIDE ↓ ACT

Run:

python 06_biomedical_ai_agent.py

07_true_biomedical_agent.py

This is the complete workshop demonstration.

The user can select:

1 - REST 2 - OPEN 3 - CLOSE

The system then: 1. Generates simulated EMG data 2. Calculates EMG
features 3. Classifies the gesture 4. Sends the analyzed evidence to the
local AI model 5. Gets the AI agent’s decision 6. Controls the simulated
prosthetic hand 7. Displays the final hand state

Run:

python 07_true_biomedical_agent.py

RECOMMENDED WORKSHOP ORDER

Run the files in this order:

03_emg_tool.py ↓ 04_prosthetic_hand.py ↓ 05_emg_gesture_tool.py ↓
06_biomedical_ai_agent.py ↓ 07_true_biomedical_agent.py

Each step adds another component to the system.

UNDERSTANDING THE AI AGENT

A normal chatbot works like:

User ↓ AI ↓ Response

Our biomedical AI workflow is different:

EMG Signal ↓ OBSERVE ↓ ANALYZE ↓ GESTURE ↓ AI DECISION ↓ ACT ↓
PROSTHETIC HAND

The key concept is:

AI Agent = AI Model + Tools + Decision + Action

TECHNOLOGY ARCHITECTURE

                GEMMA 4 E4B
                     │
                     ▼
              AI AGENT DECISION
                     │
                     ▼

EMG ──→ Python Analysis ──→ Gesture │ ▼ Prosthetic Hand

The Python tools perform the numerical and simulation work.

The AI model receives the analyzed information and makes the
demonstrated decision.

WHY IS THIS AN AI AGENT?

The important difference is that the system is connected to an action.

The workflow is:

OBSERVE ↓ ANALYZE ↓ DECIDE ↓ ACT

The AI is not simply answering a question.

It is participating in a workflow that leads to an action in a simulated
biomedical environment.

STUDENT CHALLENGE

After completing the workshop, try extending the system.

Challenge 1 — Add GRIP

Add a new gesture: GRIP

Challenge 2 — Add More Hand Movements

For example: OPEN CLOSE REST GRIP

Challenge 3 — Change the EMG Simulation

Experiment with: - Signal strength - Activation duration - Noise -
Different gesture patterns

Challenge 4 — Improve the Agent

Think about how the agent could: - Observe more signals - Use additional
tools - Make decisions using multiple inputs - Take different actions

IMPORTANT SAFETY NOTICE

This project is an educational simulation.

The EMG signals are simulated.

The prosthetic hand is a virtual demonstration.

This project is NOT intended for: - Clinical diagnosis - Medical
treatment - Patient care - Real prosthetic control - Real medical-device
operation

A real biomedical system would require appropriate engineering
validation, safety mechanisms, testing, human oversight, and applicable
regulatory approval.

LEARNING OUTCOME

By the end of this workshop, you will understand how:

Biomedical Signals + Python Tools + AI + Decision + Action

can be combined to create an AI Agent workflow for biomedical
engineering.

FINAL TAKEAWAY

The future of AI is not only about AI that can answer questions.

It is also about systems that can:

PERCEIVE → REASON → USE TOOLS → ACT

And in biomedical engineering, those actions must always be designed
with safety, validation and human oversight in mind.
