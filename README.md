# Meet Kevin - The Open Source Next.js Developer Agent

  

## About

  

Kevin is an open-source project aimed at providing web developers with a cost-effective LLM agent architecture to expedite product development. This project is perpetually a work in progress, embodying the spirit of continuous improvement and adaptation.

  

## Prerequisites

`Node v20.9.0`
`Python 3.12.1`
`Supabase CLI  v1.50.8`

## How to Use This Repo

### Cloning the Repository

Open a terminal (Linux/macOS) or CMD/PowerShell (Windows) and run the following command to clone the repository into your current directory:

`git clone https://github.com/AquilaTechAus/kevin.git`

## Starting Supabase

### Navigate to the Supabase-DB Folder

#### Linux/macOS:

`cd supabase-db`

#### Windows:

`cd supabase-db`

### Start Supabase
**Ensure the Supabase CLI is installed and properly configured before running this command.**

`supabase start`

## Set up environment variables (read carefully)

Note: You will see some environment variables pop up when you run `supabase start` which you will have to put into your .env formatted correctly. For example:

    API_URL="http://localhost:54321"
    GraphQL_URL="http://localhost:54321/graphql/v1"
    DB_URL="postgresql://postgres:postgres@localhost:54322/postgres"
    Studio_URL="http://localhost:54323"
    Inbucket_URL="http://localhost:54324"
    JWT_secret="super-secret-jwt-token-with-at-least-32-characters-long"
    anon_key="generated"
    service_role_key="generated"
    OPENAI_API_KEY="use your own'
    OS = "Windows" (or "Linux" for linux users) 
    BASE_FILEPATH = "Example - C:\Users\Documents\AI\ai-developer-assistant\"

  
##  Setting Up the Next.js Codebase

### Linux/macOS

    cd ../nextjs-codebase
    npm install

### Windows:

    cd ..\nextjs-codebase
    npm install

## Start the Development Server:

    npm run dev

# Running the Developer Agent

### Navigate to the Developer-Agent Folder:

### Linux/macOS

    cd ../agent/developer-agent
    pip install -r requirements.txt
    python agent.py

### Windows

    cd ..\agent\developer-agent
    pip install -r requirements.txt
    python agent.py
