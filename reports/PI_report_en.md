# AI-Powered Customer Support Assistant

## Introduction

This project implements an AI-powered customer support assistant capable of answering frequently asked questions using a business-specific knowledge base. The application returns a structured JSON response containing an answer, a confidence score, and suggested actions. In addition, it records execution metrics such as token usage, estimated cost, and latency to monitor the application's performance.

## Architecture

The project follows a modular architecture that separates business knowledge, prompts, application logic, metrics, and tests into independent components. This organization improves maintainability, simplifies future modifications, and makes the application easier to extend.

| Module                | Responsibility                                |
| --------------------- | --------------------------------------------- |
| **run_query.py**      | Coordinates the application workflow.         |
| **openai_client.py**  | Handles communication with the OpenAI API.    |
| **prompt_builder.py** | Builds the prompt sent to the language model. |
| **metrics.py**        | Calculates and stores execution metrics.      |

## Prompt Engineering

The prompt is stored as a separate Markdown file, making it easier to maintain, version, and improve without modifying the application code.

It combines several complementary components, including role definition, context, task description, output format, business knowledge, behavioral rules, and few-shot examples. The business knowledge helps reduce hallucinations by providing company-specific information, while the few-shot examples reinforce the expected response structure.

A low temperature was intentionally selected because customer support requires consistent and reliable answers rather than creative ones. Finally, JSON responses are enforced both through prompt instructions and the OpenAI API, allowing the application to parse responses programmatically.

## Metrics Collection

The application records token usage, estimated cost, and latency for every request. Since language model APIs are billed according to token consumption, these metrics make it possible to estimate operational costs and compare different prompts or models.

Latency is also measured because response time directly impacts the user experience and the overall efficiency of the system. All metrics are stored in a CSV file, enabling future analysis and supporting data-driven decisions.

### Sample Results

| Metric            | Sample Value |
| ----------------- | -----------: |
| Model             |  gpt-4o-mini |
| Prompt Tokens     |          186 |
| Completion Tokens |           74 |
| Total Tokens      |          260 |
| Estimated Cost    |     $0.00007 |
| Latency           |       1.84 s |

## Challenges

One of the main challenges was designing a prompt capable of consistently generating structured JSON responses while remaining flexible enough to answer different customer support questions. Another challenge was organizing the application into independent modules so that future changes could be implemented with minimal impact on the rest of the code.

## Future Improvements

Two improvements could significantly increase the scalability of the application:

* **Implement Retrieval-Augmented Generation (RAG):** Replacing the static knowledge base with semantic retrieval would allow the assistant to work with a much larger collection of business documents while reducing token usage and API costs.

* **Support Multiple AI Providers:** The current implementation depends on a single provider. Supporting multiple providers would eliminate this single point of failure, improve system availability through failover mechanisms, and make it easier to compare cost, performance, and capabilities across different models.