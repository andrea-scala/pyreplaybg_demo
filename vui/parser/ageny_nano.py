# nano_llm_wrapper.py
import os
from nanovllm import LLM, SamplingParams
from transformers import AutoTokenizer


class NanoLLMFallback:
    def __init__(self, model_path="~/Qwen3-0.6B/"):
        path = os.path.expanduser(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.llm = LLM(path, enforce_eager=True, tensor_parallel_size=1)
        self.sampling_params = SamplingParams(temperature=0.3, max_tokens=512)

    def ask(self, user_text):
        prompt = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": f"Estrai JSON con intent, paziente, data e terapia dal testo seguente:\n\"{user_text}\""}],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=True
        )
        outputs = self.llm.generate([prompt], self.sampling_params)
        return outputs[0]["text"]
