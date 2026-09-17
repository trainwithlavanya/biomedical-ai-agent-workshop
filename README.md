# AI Agents for Biomedical Engineering

## From EMG Signals to Intelligent Prosthetic Hand Control

This workshop demonstrates how AI Agents can be used in a biomedical
engineering application.

Instead of building a simple chatbot, we will build a system that can:

-   Generate simulated EMG signals
-   Analyze muscle activity
-   Recognize simple hand gestures
-   Make an AI-based decision
-   Control a simulated prosthetic hand

------------------------------------------------------------------------

## What Are We Building?

The complete workflow is:

``` text
Human Muscle
     ↓
EMG Signal
     ↓
Signal Analysis
     ↓
Gesture Classification
     ↓
AI Agent Decision
     ↓
Simulated Prosthetic Hand
```

The AI Agent follows:

**OBSERVE → ANALYZE → DECIDE → ACT**

------------------------------------------------------------------------

## Software Requirements

The following environment was used and tested for this workshop.

  Software             Tested Version
  -------------------- ----------------
  Visual Studio Code   1.132.0
  Python               3.14.7
  pip                  26.2.1
  Ollama               0.34.0
  Gemma 4 E4B          Local model
  AutoGen AgentChat    0.7.5
  NumPy                2.5.3
  Matplotlib           3.11.2

Using the same versions can help students reproduce the workshop
environment.

------------------------------------------------------------------------

## Step 1 --- Install Visual Studio Code

Download Visual Studio Code from:

https://code.visualstudio.com/download

Recommended version used for this workshop:

**Visual Studio Code 1.132.0**

After installing VS Code:

1.  Open Visual Studio Code.
2.  Open the Extensions panel.
3.  Search for `Python`.
4.  Install the **Python extension by Microsoft**.

------------------------------------------------------------------------

## Step 2 --- Install Python

Download Python from:

https://www.python.org/downloads/

Version used for this workshop:

**Python 3.14.7**

During installation on Windows, make sure:

**Add Python to PATH**

is selected.

Verify the installation:

``` bash
python --version
```

Expected:

``` text
Python 3.14.7
```

------------------------------------------------------------------------

## Step 3 --- Install Ollama

Download Ollama from:

https://ollama.com/download

Version used for this workshop:

**Ollama 0.34.0**

After installation, verify:

``` bash
ollama --version
```

Expected:

``` text
ollama version 0.34.0
```

------------------------------------------------------------------------

## Step 4 --- Download Gemma 4 E4B

This workshop uses **Gemma 4 E4B** as the local AI model.

Open the VS Code terminal and run:

``` bash
ollama pull gemma4:e4b
```

Check the installed models:

``` bash
ollama list
```

You should see:

``` text
gemma4:e4b
```

Ollama runs the model locally on your computer.

------------------------------------------------------------------------

## Step 5 --- Open the Workshop Project

Open this repository in VS Code.

Project structure:

``` text
biomedical-ai-agent-workshop/
│
├── 03_emg_tool.py
├── 04_prosthetic_hand.py
├── 05_emg_gesture_tool.py
├── 06_biomedical_ai_agent.py
├── 07_true_biomedical_agent.py
└── README.md
```

------------------------------------------------------------------------

## Step 6 --- Create a Virtual Environment

Open the VS Code terminal.

Create the virtual environment:

``` bash
python -m venv .venv
```

Activate it on Windows:

``` bash
.venv\Scripts\activate
```

You should see:

``` text
(.venv)
```

at the beginning of the terminal.

------------------------------------------------------------------------

## Step 7 --- Install AutoGen

Install AutoGen AgentChat and the Ollama extension:

``` bash
python -m pip install -U "autogen-agentchat" "autogen-ext[ollama]"
```

The tested AutoGen version is:

``` text
0.7.5
```

------------------------------------------------------------------------

## Step 8 --- Install NumPy

NumPy is used for numerical calculations and EMG signal processing.

Install:

``` bash
python -m pip install numpy
```

Test:

``` bash
python -c "import numpy; print(numpy.__version__)"
```

Tested version:

``` text
2.5.3
```

------------------------------------------------------------------------

## Step 9 --- Install Matplotlib

Matplotlib is used to visualize:

-   EMG signals
-   Muscle activity
-   The simulated prosthetic hand

Install:

``` bash
python -m pip install matplotlib
```

Test:

``` bash
python -c "import matplotlib; print(matplotlib.__version__)"
```

Tested version:

``` text
3.11.2
```

------------------------------------------------------------------------

## Step 10 --- Verify the Environment

### Python

``` bash
python --version
```

Expected:

``` text
Python 3.14.7
```

### pip

``` bash
python -m pip --version
```

Expected pip version:

``` text
26.2.1
```

### Ollama

``` bash
ollama --version
```

Expected:

``` text
ollama version 0.34.0
```

### NumPy

``` bash
python -c "import numpy; print('NumPy:', numpy.__version__)"
```

Expected:

``` text
NumPy: 2.5.3
```

### Matplotlib

``` bash
python -c "import matplotlib; print('Matplotlib:', matplotlib.__version__)"
```

Expected:

``` text
Matplotlib: 3.11.2
```

### AutoGen

``` bash
python -m pip show autogen-agentchat
```

Check that the version is:

``` text
Version: 0.7.5
```

------------------------------------------------------------------------

# Workshop Files

## 03_emg_tool.py

This file introduces simulated EMG signals.

It:

-   Generates an EMG signal
-   Calculates RMS
-   Calculates MAV
-   Detects muscle activation
-   Displays the EMG signal using Matplotlib

Run:

``` bash
python 03_emg_tool.py
```

------------------------------------------------------------------------

## 04_prosthetic_hand.py

This file introduces the virtual prosthetic hand.

The hand can perform:

``` text
OPEN
CLOSE
REST
```

Run:

``` bash
python 04_prosthetic_hand.py
```

------------------------------------------------------------------------

## 05_emg_gesture_tool.py

This file connects EMG activity with simple hand gestures.

The simulated gestures are:

``` text
REST
OPEN
CLOSE
```

The program analyzes the EMG signal and classifies the gesture.

Run:

``` bash
python 05_emg_gesture_tool.py
```

------------------------------------------------------------------------

## 06_biomedical_ai_agent.py

This file introduces the AI Agent into the biomedical workflow.

The system demonstrates:

``` text
OBSERVE
   ↓
ANALYZE
   ↓
DECIDE
   ↓
ACT
```

Run:

``` bash
python 06_biomedical_ai_agent.py
```

------------------------------------------------------------------------

## 07_true_biomedical_agent.py

This is the complete workshop demonstration.

The user can select:

``` text
1 - REST
2 - OPEN
3 - CLOSE
```

The system then:

1.  Generates simulated EMG data
2.  Calculates EMG features
3.  Classifies the gesture
4.  Sends the analyzed evidence to the local AI model
5.  Gets the AI agent's decision
6.  Controls the simulated prosthetic hand
7.  Displays the final hand state

Run:

``` bash
python 07_true_biomedical_agent.py
```

------------------------------------------------------------------------

# Recommended Workshop Order

Run the files in this order:

``` text
03_emg_tool.py
       ↓
04_prosthetic_hand.py
       ↓
05_emg_gesture_tool.py
       ↓
06_biomedical_ai_agent.py
       ↓
07_true_biomedical_agent.py
```

Each step adds another component to the system.

------------------------------------------------------------------------

# Understanding the AI Agent

A normal chatbot works like:

``` text
User
 ↓
AI
 ↓
Response
```

Our biomedical AI workflow is different:

``` text
EMG Signal
     ↓
OBSERVE
     ↓
ANALYZE
     ↓
GESTURE
     ↓
AI DECISION
     ↓
ACT
     ↓
PROSTHETIC HAND
```

The key concept is:

**AI Agent = AI Model + Tools + Decision + Action**

------------------------------------------------------------------------

# Technology Architecture

``` text
                GEMMA 4 E4B
                     │
                     ▼
              AI AGENT DECISION
                     │
                     ▼
EMG ──→ Python Analysis ──→ Gesture
                     │
                     ▼
             Prosthetic Hand
```

The Python tools perform the numerical and simulation work.

The AI model receives the analyzed information and makes the
demonstrated decision.

------------------------------------------------------------------------

# Why Is This an AI Agent?

The important difference is that the system is connected to an action.

The workflow is:

``` text
OBSERVE
   ↓
ANALYZE
   ↓
DECIDE
   ↓
ACT
```

The AI is not simply answering a question.

It is participating in a workflow that leads to an action in a simulated
biomedical environment.

------------------------------------------------------------------------

# Student Challenge

After completing the workshop, try extending the system.

## Challenge 1 --- Add GRIP

Add a new gesture:

``` text
GRIP
```

## Challenge 2 --- Add More Hand Movements

For example:

``` text
OPEN
CLOSE
REST
GRIP
```

## Challenge 3 --- Change the EMG Simulation

Experiment with:

-   Signal strength
-   Activation duration
-   Noise
-   Different gesture patterns

## Challenge 4 --- Improve the Agent

Think about how the agent could:

-   Observe more signals
-   Use additional tools
-   Make decisions using multiple inputs
-   Take different actions

------------------------------------------------------------------------

# Important Safety Notice

This project is an **educational simulation**.

The EMG signals are simulated.

The prosthetic hand is a virtual demonstration.

This project is **NOT intended for**:

-   Clinical diagnosis
-   Medical treatment
-   Patient care
-   Real prosthetic control
-   Real medical-device operation

A real biomedical system would require appropriate engineering
validation, safety mechanisms, testing, human oversight, and applicable
regulatory approval.

------------------------------------------------------------------------

# Learning Outcome

By the end of this workshop, you will understand how:

**Biomedical Signals + Python Tools + AI + Decision + Action**

can be combined to create an AI Agent workflow for biomedical
engineering.

------------------------------------------------------------------------

# Final Takeaway

The future of AI is not only about AI that can answer questions.

It is also about systems that can:

**PERCEIVE → REASON → USE TOOLS → ACT**

And in biomedical engineering, those actions must always be designed
with **safety, validation and human oversight** in mind.
