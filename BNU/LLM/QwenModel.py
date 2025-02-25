import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

# 函数1：加载模型
def load_model(model_path="/root/Qwen/Qwen2-VL-7B-Instruct"):
    """
    加载 Qwen2-VL 模型和处理器。
    :param model_path: 模型路径
    :return: 加载好的模型和处理器
    """
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_path, torch_dtype="auto", device_map="auto"
    )
    processor = AutoProcessor.from_pretrained(model_path)
    return model, processor


# 函数2：模型推理
def get_model_output(prompt, image_path, model, processor):
    """
    使用加载好的模型和处理器进行推理。
    :param prompt: 提示文本
    :param image_path: 图片路径
    :param model: 加载好的模型
    :param processor: 加载好的处理器
    :return: 模型生成的输出文本
    """
    # 准备输入消息
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {"type": "text", "text": prompt},
            ],
        }
    ]

    # 准备模型输入
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # 生成输出
    generated_ids = model.generate(**inputs, max_new_tokens=128)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )[0]

    return output_text