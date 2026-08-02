# Multitasking Text Utility

> An AI-powered assistant that helps customer support agents answer common questions using a business-specific knowledge base.

## Overview

This project simulates an AI-powered customer support assistant for an online learning platform.

The application helps customer support agents answer customer questions more efficiently. It receives a question from the user, sends it to the OpenAI Chat Completions API together with a structured prompt and a business-specific knowledge base, and returns a concise response.

Each response also includes a confidence score and a list of suggested actions that the support agent can perform. The knowledge base can be easily customized to adapt the application to different businesses.

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

- Answer customer support questions using the OpenAI Chat Completions API.
- Generate structured JSON responses.
- Use a customizable business knowledge base.
- Measure API latency and token usage.
- Estimate the cost of each request.
- Save metrics to a CSV file for later analysis.
- Include unit tests for the core application logic.

## Project Structure

```
data/       Business knowledge base.
metrics/    CSV files containing execution metrics.
prompts/    Prompt templates used by the model.
reports/    Project documentation and implementation report.
src/        Application source code.
tests/      Unit tests.
```

## Technologies

- Python
- OpenAI Chat Completions API
- python-dotenv
- pytest

## Installation

1. Clone this repository.
2. Install the project dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root.
4. Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key
```

## Usage

Run the application from the project root:

```bash
python -m src.run_query
```

The application will prompt you to enter a customer support question.

The console displays:
- The AI-generated answer.
- The confidence score.
- The suggested support actions.

Execution metrics (latency, token usage, estimated cost, and timestamp) are automatically saved to `metrics/metrics.csv` after each request.

## Running the Tests

Run all tests using:

```bash
python -m pytest
```

## Example Output

```json
{
  "question": "Can I cancel my order?",
  "answer": "Customers have 14 days to cancel their purchase.",
  "confidence": 0.98,
  "actions": [
    "Provide the cancellation instructions."
  ],
  "metrics": {
    "timestamp": "2026-07-30T18:45:10",
    "model": "gpt-4o-mini",
    "prompt_tokens": 284,
    "completion_tokens": 42,
    "total_tokens": 326,
    "latency_ms": 1452.31,
    "estimated_cost_usd": 0.0000678
  }
}
```

## Author

Developed by Virginia as part of the AI Engineering Bootcamp.

