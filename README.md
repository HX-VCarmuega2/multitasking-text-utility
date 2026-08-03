# Multitasking Text Utility

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white)
![Model](https://img.shields.io/badge/Model-gpt--4o--mini-orange)
![Pytest](https://img.shields.io/badge/Pytest-9.1.1-0A9EDC?logo=pytest&logoColor=white)

> An AI-powered assistant that helps customer support agents answer common questions using a business-specific knowledge base.

## Overview

This project simulates an AI-powered customer support assistant for an online learning platform.

The application helps customer support agents answer customer questions more efficiently. It receives a question from the user, sends it to the OpenAI Chat Completions API together with a structured prompt and a business-specific knowledge base, and returns a concise, structured response containing an answer, a confidence score, and suggested follow-up actions.

The knowledge base can be easily customized to adapt the application to different businesses.

## Business Context

This project simulates an AI-powered customer support assistant for an online learning platform. The assistant answers frequently asked questions using a business-specific knowledge base containing information about courses, enrollments, payments, certificates, refunds, and platform policies.

The assistant is designed to answer questions related to this knowledge base. Any information outside the provided documentation may result in a low-confidence response.

### Example Questions

* How do I enroll in a course?
* Can I request a refund after purchasing a course?
* How long do I have access to a course?
* When will I receive my certificate?
* What payment methods are accepted?
* Can I change my account email?
* What should I do if I can't access a course?

## Features

* Answer customer support questions using the OpenAI Chat Completions API.
* Generate structured AI responses in JSON format.
* Use a customizable business knowledge base.
* Measure API latency and token usage.
* Estimate the cost of each request.
* Save execution metrics to a CSV file.
* Include unit tests for the core application logic.

## Project Structure

```text
data/       Business knowledge base.
metrics/    CSV files containing execution metrics.
prompts/    Prompt templates used by the model.
reports/    Project documentation and implementation report.
src/        Application source code.
tests/      Unit tests.
```

## Technologies

* Python 3.13+
* OpenAI Chat Completions API
* python-dotenv
* pytest

## Prerequisites

Before running the project, make sure you have:

* Python 3.13 or later
* An OpenAI API key

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd multitasking-text-utility
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

**Windows (Git Bash)**

```bash
source .venv/Scripts/activate
```

**Windows (Command Prompt)**

```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

4. Install the project dependencies:

```bash
pip install -r requirements.txt
```

5. Copy the example environment file.

**Git Bash**

```bash
cp .env.example .env
```

**Windows (Command Prompt)**

```cmd
copy .env.example .env
```

6. Open the `.env` file and add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key
```

## Usage

Run the application from the project root:

```bash
python -m src.run_query
```

The application will prompt you to enter a customer support question.

### Example

```text
Enter your question:
How do I enroll in a course?
```

The console displays the following information:

* The AI-generated answer.
* The confidence score.
* The suggested support actions.

After each request, execution metrics (timestamp, token usage, latency, and estimated cost) are automatically appended to `metrics/metrics.csv`.

The application also allows multiple queries during the same session.

## Running the Tests

Run all tests using:

```bash
python -m pytest
```

## Example Console Output

```text
=======================================================
🤖 AI SUPPORT ASSISTANT
=======================================================

📝 Answer
-------------------------------------------------------
Customers have 14 days to request a refund after
purchasing a course.

📊 Confidence
-------------------------------------------------------
🟢 High (98%)

💡 Suggested Actions
-------------------------------------------------------
• Provide the refund instructions.
• Inform the customer about the refund period.

=======================================================
```

## Execution Metrics

Each request is automatically recorded in `metrics/metrics.csv`.

| Metric            |     Example |
| ----------------- | ----------: |
| Model             | gpt-4o-mini |
| Prompt Tokens     |         284 |
| Completion Tokens |          42 |
| Total Tokens      |         326 |
| Latency           |     1452 ms |
| Estimated Cost    |  $0.0000678 |

## Author

Developed by Virginia as part of the AI Engineering Bootcamp.
