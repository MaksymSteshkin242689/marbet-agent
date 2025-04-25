# LLM Agent Q&A Chat Documentation

## Overview
This project implements an intelligent Q&A chat agent that can answer questions about various topics related to a company's services and information. The agent uses a LangChain-based architecture with Ollama as the underlying language model.

## Architecture

### Core Components

1. **Main Application (`main.py`)**
   - Entry point of the application
   - Initializes the Ollama model and AgentWorkflow
   - Provides an interactive command-line interface for Q&A

2. **Agent Workflow (`agent/agent_workflow.py`)**
   - Manages the main workflow of the Q&A system
   - Implements a state-based graph architecture using LangGraph
   - Handles context loading and topic-based routing

3. **Context Management**
   - Uses `ContextStore` to manage different knowledge domains
   - Loads context from text files in the `splitted` directory
   - Supports multiple topic-specific stores:
     - Activities
     - Company information
     - ESTA
     - ETA
     - Packlist
     - Scenic Eclipse A-Z
     - Spa
     - WiFi

### Workflow Process

```
+----------------+     +----------------+     +----------------+
|  User Question | --> | Topic Extraction| --> | Topic Routing  |
+----------------+     +----------------+     +----------------+
                                                      |
                                              +-------+-------+
                                              |               |
                                              v               v
                                      +-------------+ +----------------+
                                      |   "Other"   | | Specific Topic |
                                      +-------------+ +----------------+
                                              |               |
                                              v               v
                                      +-------------+ +----------------+
                                      | Generate    | | Extract Context|
                                      | General     | +----------------+
                                      | Answer      |         |
                                      +-------------+         v
                                                      +----------------+
                                                      | Generate       |
                                                      | Topic-specific |
                                                      | Answer         |
                                                      +----------------+
```

The workflow follows these steps:

1. **User Question Input**
   - User submits a question through the interface

2. **Topic Extraction**
   - System analyzes the question to identify the main topic
   - Uses the `extract_topic` tool to determine the context

3. **Topic Routing**
   - Based on the extracted topic, the system routes to one of two paths:
     - If topic is "Other": Proceeds to generate a general answer
     - If topic is specific: Extracts relevant context and generates a topic-specific answer

4. **Answer Generation**
   - For general questions: Uses `generate_general_answer` to provide a response
   - For topic-specific questions: 
     1. Extracts relevant context from the appropriate store
     2. Uses `generate_qa_answer` to create a response based on the context

5. **Response Delivery**
   - The generated answer is returned to the user

## Context Files Structure

The project uses a structured approach to manage context information:

1. **Source Files**
   - Original PDF files were converted to text format
   - Each text file contains information about a specific topic

2. **File Organization**
   - All context files are stored in the `splitted` directory
   - Each file is named according to its topic (e.g., `activities.txt`, `company.txt`, etc.)

3. **Context Loading**
   - Context files are loaded into separate `ContextStore` instances
   - Each store is associated with a specific topic
   - The stores are initialized when the agent starts

## Usage

1. **Setup**
   ```python
   from langchain_ollama import ChatOllama
   from agent.agent_workflow import AgentWorkflow

   # Initialize the model
   model = ChatOllama(
       base_url="http://194.171.191.226:3061",
       model="llama3.1:8b",
       format="json"
   )

   # Create the agent
   agent = AgentWorkflow(model=model)
   ```

2. **Asking Questions**
   ```python
   # Get an answer
   question = "What are the available activities?"
   answer = agent.start_flow(question)
   print(answer)
   ```

## Context File Creation Process

The context files were created through the following process:

1. **PDF to Text Conversion**
   - Original PDF documents were converted to text format
   - Each document was split into separate text files based on topics

2. **File Organization**
   - Created a `splitted` directory to store all context files
   - Named each file according to its content topic
   - Maintained a clear structure for easy reference

3. **Content Management**
   - Each text file contains relevant information for its specific topic
   - Files are organized to facilitate easy updates and maintenance
   - The content is structured to be easily processed by the LLM


## Dependencies

- langchain-ollama
- langgraph
- langchain-core

## Configuration

The system uses the following configuration:
- Ollama model: llama3.1:8b
- Base URL: http://194.171.191.226:3061
- Format: JSON

## Best Practices

1. **Context Management**
   - Keep context files up to date
   - Ensure proper formatting of text content
   - Maintain clear separation between different topics

2. **Question Handling**
   - Frame questions clearly and specifically
   - Use appropriate topic-related keywords
   - Avoid ambiguous or overly complex questions

3. **System Maintenance**
   - Regularly update context files
   - Monitor system performance
   - Keep dependencies up to date

## Proposed Improvements

### 1. SQL Storage Integration

#### Chat History Storage
- Implement SQL database to store chat history
- Add chat history to the agent workflow state
- Benefits:
  - Persistent storage of conversations
  - Ability to analyze past interactions
  - Improved context awareness for future responses
  - Better tracking of user interactions

### 2. Activity Data Management

#### SQL-based Activity Storage
- Move activity data from text files to SQL database
- Benefits:
  - Better handling of large datasets
  - Improved query performance
  - More flexible data structure
  - Easier data updates and maintenance

#### Agent Integration
- Modify agent workflow to query SQL database
- Add SQL query tools to agent toolkit
- Implement caching for frequently accessed data
- Add data validation and error handling