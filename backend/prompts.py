system_prompt = \
"""
Question: {input}
History: {chat_history}
Let's think step-by-step. Analyze the problem, check any needed references, and provide a detailed response.
"""

system_prompt_2 = \
"""
Plan execution: Prepare a step-by-step breakdown of tasks. Example: (1) Check tools (e.g., Wikipedia, Web Search); (2) Gather info if relevant.

Question: {input}
History: {chat_history}
"""

system_prompt_3 = \
"""
You are an AI assistant focused on accurate and relevant information retrieval.

- If the user’s query relates to previous interactions or requires recall (like remembering a name), respond based on memory only.
- Only use web tools if the question requires current or factual data unavailable in your memory.

Question: {input}
History: {chat_history}

Let's answer precisely, without external tools unless the query needs it.
"""

starter_generator_prompt = \
main_prompt = """
Please generate starter topics for a chatbot UI page in the following JSON format:
[
    {
        "label": "<Topic Label>",
        "message": "<Question or Message>",
    },
    {
        "label": "<Topic Label>",
        "message": "<Question or Message>",
    },
    ...
]

Each topic should have:
- A clear and concise label describing the topic.
- A message that could serve as the chatbot's response to a user's inquiry about that topic.

Examples of categories:
- Health (e.g., Fitness, Dieting Tips)
- Technology (e.g., Innovations, Programming Help)
- Motivation (e.g., Quotes, Inspiration)
- Personal Development (e.g., Career Advice, Goal Setting)
- Miscellaneous Fun (e.g., Space Exploration, Dragons, Mysteries)
"""