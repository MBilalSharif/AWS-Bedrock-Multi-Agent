# Amazon Bedrock Customer Support Agents

## Overview

This project demonstrates how to build intelligent customer support solutions using **Amazon Bedrock Agents**. It includes both a **Single-Agent** implementation and a **Multi-Agent Supervisor Routing System**, showcasing how Amazon Bedrock can orchestrate specialized agents, invoke AWS Lambda functions, query Knowledge Bases, and enforce Guardrails for secure AI interactions.

The project is designed for learning and demonstration purposes and uses mock customer data without any external databases.

---

# Architecture

## Task 1 – Single Agent

A customer support agent capable of:

* Retrieving order status through an AWS Lambda action group.
* Answering product-related FAQs using an Amazon Bedrock Knowledge Base.
* Protecting sensitive information using Amazon Bedrock Guardrails.

### Components

* Amazon Bedrock Agent
* AWS Lambda

  * `get_order_status(order_id)`
* Amazon Bedrock Knowledge Base
* Amazon Bedrock Guardrails

---

## Task 2 – Multi-Agent Collaboration

A Supervisor Agent routes customer requests to specialized sub-agents.

### Supervisor Agent

Responsible for:

* Understanding customer intent.
* Selecting the appropriate specialized agent.
* Refusing to answer when the request cannot be confidently routed.

### Order Sub-Agent

Handles:

* Order status
* Shipping information

Uses:

* `get_order_status(order_id)` Lambda

### Returns Sub-Agent

Handles:

* Return eligibility
* Refund policy
* Return process

Uses:

* `get_return_policy(...)` Lambda

---

# Features

* Amazon Bedrock Agents
* Multi-Agent Collaboration
* Supervisor Agent Routing
* AWS Lambda Action Groups
* Amazon Bedrock Knowledge Base
* Amazon Bedrock Guardrails
* PII Redaction
* Denied Topics Configuration
* Mock Customer Support Dataset
* No external database required

---

# Project Structure

```text
.
├── lambdas/
│   ├── order-status/
│   └── return-policy/
│
└── README.md
```

---

# Lambda Functions

## 1. Order Status

Function:

```text
get_order_status(order_id)
```

Returns mock order information including:

* Order ID
* Product
* Order Status
* Estimated Delivery Date

---

## 2. Return Policy

Function:

```text
get_return_policy(product_name)
```

Returns mock information such as:

* Return eligibility
* Refund availability
* Return window
* Processing time

---

# Knowledge Base

The project includes a sample Product FAQ document indexed into an Amazon Bedrock Knowledge Base.

Example topics:

* Product specifications
* Warranty
* Shipping
* Setup instructions
* Common troubleshooting
* Compatibility

---

# Guardrails

The Bedrock Agent is configured with Guardrails to improve response safety.

### PII Redaction

Sensitive information is automatically redacted from prompts and responses.

Examples:

* Email addresses
* Phone numbers
* Physical addresses
* Credit card numbers

### Denied Topics

The agent refuses requests involving predefined restricted topics instead of generating responses.

---

# Multi-Agent Routing Logic

| Customer Request            | Routed To           |
| --------------------------- | ------------------- |
| Where is my order?          | Order Sub-Agent     |
| Has my package shipped?     | Order Sub-Agent     |
| Can I return my headphones? | Returns Sub-Agent   |
| When will my refund arrive? | Returns Sub-Agent   |
| My order arrived damaged    | Supervisor Decision |
| I need help                 | Supervisor Decision |

If the Supervisor Agent cannot confidently determine the correct destination, it responds that it cannot assist rather than making an incorrect routing decision.

---

# Test Scenarios

## Order Agent

* What is the status of order ORD-001?
* When will my order ORD-004 arrive?

## Returns Agent

* Can I return Product X?
* How long does a refund take?

## Ambiguous Requests

* I have an issue with my recent purchase.
* I need help with my order.

These scenarios are used to evaluate whether the Supervisor Agent routes requests appropriately or declines to route when confidence is insufficient.

---

# Technologies Used

* Amazon Bedrock Agents
* Amazon Bedrock Multi-Agent Collaboration
* Amazon Bedrock Knowledge Bases
* Amazon Bedrock Guardrails
* AWS Lambda
* Python
* AWS IAM

---

# Learning Objectives

This project demonstrates how to:

* Build Lambda-backed Bedrock Agents
* Integrate Amazon Bedrock Knowledge Bases
* Configure Guardrails for safer AI applications
* Design specialized AI agents
* Implement Supervisor-based agent routing
* Build scalable customer support workflows using Amazon Bedrock

---

# Disclaimer

This project is intended for educational and demonstration purposes only. All customer data, order information, return policies, and product FAQs are mock examples and do not represent real customer records.
