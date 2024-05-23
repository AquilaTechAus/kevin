from langchain_community.utilities.sql_database import SQLDatabase
from typing import List, Tuple
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import subprocess
import psycopg2
from dotenv import load_dotenv
import os
import langchain_openai
from langchain.prompts import PromptTemplate


dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)

conn_string = os.environ.get('DB_URL')
openai_key = os.environ.get('OPENAI_API_KEY')
operating_system = os.environ.get('OS')
base_path = os.environ.get('BASE_APTH')


class FileWrite(BaseModel):
    file_path: str = Field(
        description="Should be a file path that is accessible from the current environment.")
    file_text: str = Field(
        description="The text to write to the file.")
   
class FileRead(BaseModel):
    file_path: str = Field(
        description="Should be a file path that is accessible from the current environment.")
   
class WindowsCommand(BaseModel):
    command: str = Field(
        description="The command to run on the Windows operating system.")
    
class SQLCommand(BaseModel):
    command: str = Field(
        description="The command to run on the SQL DB.")
    

custom_react_prompt = PromptTemplate.from_template("""AutoDev is a large language model that is a specialist asisstant in developing full stack web applications.

AutoDev is designed to be able to assist with the development of a full-stack web application using Next.js + Supabase + TypeScript.

AutoDev is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of code. Additionally, AutoDev is able to act as a database administrator, code writer and reviewer.

TOOLS:
------

AutoDev has access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}""")


struc_chat_agent = PromptTemplate.from_template("""You are a full stack developer's assistant. You have access to the following tools:

{tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Task: The input task to be completed.
Thought: Consider previous and subsequent steps before you take action.
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
                                                
Chat History:
{chat_history}

Human:
{input}
                                                
Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation
                                                
{agent_scratchpad}""")


@tool("execute_sql", args_schema=SQLCommand, return_direct=True)
def execute_sql(command: str):
    """Execute a SQL command on the PostgreSQL (Supabase) DB and return its output."""
    conn = None
    try:
        # Assume conn_string is defined elsewhere and contains your connection details
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute(command)
        
        # Try to fetch the results if it's a command that returns data
        if command.strip().upper().startswith("SELECT"):
            # Fetches all the rows of a query result, returning them as a list of tuples.
            results = cur.fetchall()
            message = 'Success', results
        else:
            # For non-SELECT queries that don't return data
            conn.commit()
            message = 'Success', None
    except Exception as e:
        message = "Error: " + str(e), None
    finally:
        if conn:
            cur.close()
            conn.close()
        return message


@tool("read_file", args_schema=FileRead, return_direct=True)
def read_file(file_path: FileRead) -> str:
    """Read a file from the file system. 
    # Project folder structure #
    The root of the Next.js Project is the following path:
    /nextjs-codebase

    Within the nextjs-codebase folder, here are some important subdirectories to keep in mind:
    Subdirectory: /app/home | Description: Home page lives here - the page.tsx file inside it is a Server side route.
    Subdirectory: /components/ui/ | Description: This is where you will be able to find the following pre-coded UI Path: /components that you can import elsewhere in the application.

    add ../../ to the file path as the nexts-codebase is 2 levels up from folder you are in."""
    with open(file_path, "r") as file:
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {e}"
   


@tool("write_file", args_schema=FileWrite, return_direct=True)
def write_file(file_path: str, file_text: str) -> str:
    """Write to a file in the file system.
       # Project folder structure #
        The root of the Next.js Project is the following path:
        nextjs-codebase

        Within the nextjs-codebase folder, here are some important subdirectories to keep in mind:
        Subdirectory: /app/home | Description: Home page lives here - the page.tsx file inside it is a Server side route.
        Subdirectory: /components/ui/ | Description: This is where you will be able to find the following pre-coded UI Path: /components that you can import elsewhere in the application."""
    with open(file_path, "w") as file:
        file.write(file_text)
    return "Successfully written to file."


@tool("run_windows_command", args_schema=WindowsCommand, return_direct=True)
def run_windows_command(command: str) -> str:
    """Run a command and get the result."""

    try:
        result = subprocess.run(command, shell=True, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout or "Command ran successfully."
    except subprocess.CalledProcessError as e:
        return f"Command failed with exit code {e.returncode}:\n{e.stderr}"
    except Exception as e:
        return f"Error running command: {e}"




tools = [run_windows_command, read_file, write_file, execute_sql]
llm = ChatOpenAI(temperature=0.5, model="gpt-4-turbo-preview", openai_api_key=openai_key)
agent = create_structured_chat_agent(llm, tools, struc_chat_agent)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, return_intermediate_steps=True
)


with open('./system_prompt.md', 'r') as file:
    content = file.read()

# Create an instance of SystemMessage with the file content
message_history = [SystemMessage(content=content)]

print ("Welcome to the Extensa AI Next.js - Supabase - Shadcn UI Bot! ")
print ("Type 'Exit' to exit ..")
print ("I'm ready to go - how should we start?")
user_input = input()
while user_input != 'Exit':
    result = agent_executor.invoke(
        {
            "input": user_input,
            "chat_history": message_history,
        }
    )
    outcome = str(result['output']) if result['output'] else str(result)
    ai_message = ""
    outcome += "\n"
    for step in result['intermediate_steps']:
        ai_message += step[0].log
    
    ai_message += f"\n This was the outcome: {outcome}."
    print ("AI: ")
    print (ai_message)
    message_history.append(AIMessage(content=ai_message))
    print ("Human: ")
    user_input = input()






