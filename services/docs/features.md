# Features

This document provides an overview of the key features of the Pankh.AI platform.

## 1. AI-Powered Block Generation

Pankh.AI includes an intelligent block generation system that automatically creates workflow blocks from natural language descriptions using AI.

### 1.1. Overview

The AI Block Generation system uses Azure OpenAI (GPT-4) or Anthropic Claude to:

1.  **Analyze** natural language task descriptions
2.  **Generate** production-ready Python block code
3.  **Validate** syntax and structure
4.  **Test** blocks in a safe sandbox
5.  **Self-heal** failing tests automatically using LangGraph
6.  **Return** complete, tested block implementations

### 1.2. Architecture

The system is designed as a pipeline that takes a natural language task and outputs a production-ready workflow block.

```
API Endpoint (/api/v1/blocks/generate)
|
V
EnhancedAIBlockGenerator
|
V
[Similarity Check] -> [Requirement Analysis] -> [Code Generation] -> [Validation] -> [Test Generation] -> [Test Execution] -> [Self-Healing]
```

### 1.3. Features

-   **AI-Powered Code Generation:** Supports Azure OpenAI, OpenAI, and Anthropic Claude.
-   **Block Similarity Service:** Prevents duplicate blocks by checking for similar descriptions and functionality.
-   **Test Execution Service:** Provides a safe sandbox for testing generated blocks with restricted built-ins and timeout protection.
-   **Self-Healing Service (LangGraph):** Automatically fixes failing tests using a LangGraph state machine.

### 1.4. API Usage

To generate a block, send a POST request to `/api/v1/blocks/generate` with a JSON payload containing the task description and category.

```json
{
  "task": "Create a block that fetches weather data from OpenWeatherMap API",
  "category": "simple_api",
  "enable_self_healing": true
}
```

## 2. Agent Block

The agent block provides multi-provider LLM support, allowing you to use models from OpenAI, Azure OpenAI, Anthropic, Groq, and Google.

### 2.1. Supported Providers

-   **OpenAI:** GPT-3.5, GPT-4, GPT-4-turbo
-   **Azure OpenAI:** All OpenAI models via Azure
-   **Anthropic:** Claude 3 models (Opus, Sonnet, Haiku)
-   **Groq:** Fast inference (Llama 3, Mixtral)
-   **Google:** Gemini Pro

### 2.2. Usage

The provider is auto-detected based on the model name, but you can also specify it explicitly.

```json
{
    "type": "agent",
    "data": {
        "provider": "openai",
        "model": "gpt-4-turbo",
        "system_prompt": "You are a helpful AI assistant.",
        "user_prompt": "{{input.question}}",
        "temperature": 0.7,
        "max_tokens": 2000
    }
}
```

## 3. New Blocks Created

6 powerful new block types have been created to expand workflow capabilities:

-   **Transformer Block:** 30+ data manipulation operations (JSON, text, array, object, etc.).
-   **Database Block:** PostgreSQL & MongoDB support.
-   **Delay Block:** Pause/wait functionality.
-   **Webhook Block:** Outbound webhook calls with HMAC signing.
-   **Email Block:** Email sending via Resend API.
-   **Variables Block:** Dynamic variable management during execution.

## 4. Chatbot Feature

A working chatbot feature has been implemented in the new React + Vite frontend. The chatbot connects to the backend API and allows real-time conversation with the AI.

### 4.1. Features

-   Real-time message sending
-   Loading states and error handling
-   Conversation ID tracking
-   Keyboard shortcuts
-   Responsive design

### 4.2. API Endpoint

The chatbot uses the `POST /api/v1/chat` endpoint to send and receive messages.

## 5. Templates Feature

The Templates feature allows users to create, browse, discover, and use workflow templates.

### 5.1. Frontend

-   **Templates List Page:** Displays a list of templates with search and filtering capabilities.
-   **Template Detail Page:** Shows the details of a single template, including a preview of the workflow.
-   **Template Modal:** Allows users to create and edit templates from the workflow editor.

### 5.2. Backend

-   **API Endpoints:** 8 endpoints for CRUD operations, starring, and using templates.
-   **Database:** `WorkflowTemplate` and `TemplateStar` tables to store template data.

## 6. Workers & Realtime Services

Two critical services have been implemented for the backend:

### 6.1. Workers Service (Celery)

-   **Task Queue System:** Celery with Redis broker.
-   **4 Dedicated Queues:** `workflows`, `notifications`, `scheduled`, and `default`.
-   **10+ Background Tasks:** Asynchronous workflow execution, scheduled tasks, and notifications.
-   **REST API:** 7 endpoints for task management.

### 6.2. Realtime Service (Socket.IO)

-   **Socket.IO Server:** Async ASGI application.
-   **Room-based Broadcasting:** Workflow, execution, user, and organization rooms.
-   **JWT Authentication:** Secure WebSocket connections.
-   **15+ Event Types:** Execution updates, collaboration, and notifications.
-   **Real-time Execution Notifier:** Seamless integration with the workflow executor.

## Additional Features Content

### Blocks Created

Content from `BLOCKS_CREATED.md`.

### Chatbot Feature

Content from `CHATBOT_FEATURE.md`.
