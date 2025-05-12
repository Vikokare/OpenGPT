from langchain_core.prompts import PromptTemplate
import prompts
prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template=prompts.system_prompt,
)

plan_prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template=prompts.system_prompt_2,
)

main_prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template=prompts.system_prompt_3,
)
