from openai import OpenAI
from os import getenv
import os
from datetime import datetime,timedelta
from concurrent.futures import ThreadPoolExecutor
import math
import pandas as pd
import re
import random
import threading
from dotenv import load_dotenv

load_dotenv()
# gets API Key from environment variable OPENAI_API_KEY
# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url=os.environ["OPENROUTER_API"],
  api_key=os.environ["OPENROUTER_KEY"],
)

# OPENROUTER MODEL
#MODEL='anthropic/claude-3.5-sonnet'
MODEL='meta-llama/llama-3.2-90b-vision-instruct'

def create_prompt():
    PROMPT = f"""
ZenUML is a code to diagram language with a DSL defined for creating sequence diagrams.

Rule and syntax with example below:

```zenuml
// Define participants, no spaces in the name
@Type1 "Name1"
@Type2 "Name2"

// Async Message from Name1 to Name2
"Name1" -> "Name2":messageText



// Sync Message from Name1 to Name2, no Spaces in messageText
"Name1" -> "Name2"."messageText"(){{
  // interactions between Sync Messages with activation bar
}}

// Return Message use @return keyword, from Name2 to Name1
@return "Name2"->"Name1": messageText

// If, use if("condition") with {{}}, optional use else {{}}
if("condition"){{
  // scope of a activation bar
  // any interactions between
}}

// Loop, for repeated tasks, use loop(condition) keyword with {{}}
loop("condition") {{
  // in scope interactions
}}
// optional
else {{
  // in scope else interactions
}}

// Optional use opt keyword with {{}}
opt{{
  // in scope interactions
}}

// parallel interactions, use par keyword with {{}}
par{{
  // in scope interactions
}}

// coloring, add (StandardCSSColorName) in comment line before any message
e.g:
// (red) some comment
"Name1" -> "Name2":messageText
```

Please you read the user input story, model the process and  create the sequence diagram in it with ZenUML language follow below rules:

- a solid line with a [solid arrowhead] means Sync Message
- a solid line with a [lined arrowhead] means Sync Message
- [a dashed line with a lined arrowhead] means Return Message, use @return
- read very carefully regarding the differences between types of messages, this is the key of diagraming
- if unknown scope keyword, always use opt
- replace all [-->] or [->>] or [<-] with [->]
- No spaces in any message names


Provide your output in json format:

```json
{{
  diagram_title: "",
  diagram_content: "ZenUML DSL" 
}}
```

User request:

Diagram for credit card payment process flow
"""
    return PROMPT



def generate_response():

    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "https://diagramly.ai", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "Diagramly POC", # Optional. Shows in rankings on openrouter.ai.
    },
    #model="qwen/qwen-2.5-72b-instruct",
    #model="anthropic/claude-3.5-sonnet",
    model=MODEL,
    response_format={ "type": "json_object" },
    messages=[
        {
        "role": "system",
        "content": create_prompt()
        }
    ]
    )
    #print(completion.choices[0].message.content)

    return completion.choices[0].message.content




if __name__ == "__main__":
    response = generate_response()
    print(response)