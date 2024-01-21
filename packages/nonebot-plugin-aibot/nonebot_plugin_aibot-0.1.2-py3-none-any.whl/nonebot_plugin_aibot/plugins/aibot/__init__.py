from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from bigdl.llm.transformers import AutoModelForCausalLM
from transformers import LlamaTokenizer
import torch
import transformers
import os

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="aibot",
    description="use model Mistral-7B-v0.1 to chat with you",
    usage="a chatbot powered by ai",
    type="aplication",
    homepage="use model Mistral-7B-v0.1 to chat with you",
    config=Config,
)

tokenizer = LlamaTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

model_path = "mistralai/Mistral-7B-v0.1"
save_directory = "./nonebot_plugin_aibot/plugins/aibot/Mistral-7B-v0.1-bigdl-llm-INT4"

# Check if the model has been downloaded
if not os.path.exists(save_directory):
    # If the model has not been downloaded, download and convert it
    model = AutoModelForCausalLM.from_pretrained(model_path, load_in_4bit=True)
    model.save_low_bit(save_directory)
else:
    # If the model has been downloaded, load it from the local directory
    model = AutoModelForCausalLM.load_low_bit(save_directory)


transformers.logging.set_verbosity(50)

# Initialize an empty conversation history
conversation_history = ""


def generate(prompt, model=model, tokenizer=tokenizer):
    global conversation_history
    conversation_history += prompt
    # Generate a response using the entire conversation history
    with torch.inference_mode():
        # tokenize the input prompt from string to token ids
        input_ids = tokenizer.encode(conversation_history, return_tensors="pt")
        # predict the next tokens (maximum 64) based on the input token ids
        output = model.generate(input_ids, max_new_tokens=64)
        # decode the predicted token ids to output string
        output_str = tokenizer.decode(output[0], skip_special_tokens=True)

        # Only keep the answer part
        answer = output_str[len(conversation_history) :].strip()
        if "User:" in answer:
            answer = answer.split("User:")[0].strip()
        conversation_history += answer
    return answer


global_config = get_driver().config
config = Config.parse_obj(global_config)

aibot = on_command("chat", rule=to_me(), aliases={"聊天"}, priority=10, block=True)


@aibot.handle()
async def handle_function(args: Message = CommandArg()):
    # Extract the user's message
    user_message = args.extract_plain_text()

    if user_message:
        response = generate(f"User: {user_message}\nChatbot: ")

        await aibot.finish(response)
    else:
        await aibot.finish("请输入内容")
