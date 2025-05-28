import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import time

def modelInit() -> object:
    #При необходимости заменить модель
    model_id = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")
    print(torch.cuda.is_available())
    return model, tokenizer

def pipe(model, tokenizer, prompt) -> str | dict:
    prompt = prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=4)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    #Иначе необходимо вернуть данные в таком формате
    responseData = {
        "token_routing_map":None, #Карта маршрутизации токенов
        "expert_outputs":None, #Выводы экспертов
        "output":None, #Ответ нейросети
        "logic_summary":None, #Итоговая логика обработки
    }
    return response


if __name__ == "__main__":
    model, tokenizer = modelInit()
    st = time.time()
    print(pipe(model, tokenizer, "1+1="))
    print(round(time.time()-st,3))
    
    