=======
# 医疗对话解决方案 (Medical Dialogue Solutions)

本项目提供了基于大语言模型的医疗对话解决方案，支持使用 LoRA 和 QLoRA 等高效微调技术进行模型训练和推理。

## 📁 模型下载

### LoRA 微调模型
| 模型版本 | 训练轮次 | 模型地址 |
|---------|----------|----------|
| MDL-lora1 | Epoch 1 | [ModelScope](https://modelscope.cn/models/magege/MDL-lora1/files) |
| MDL-lora2 | Epoch 2 | [ModelScope](https://modelscope.cn/models/magege/MDL-lora2/files) |

### QLoRA 微调模型
| 模型版本 | 训练轮次 | 模型地址 |
|---------|----------|----------|
| MDL-Qlora1 | Epoch 1 | [ModelScope](https://modelscope.cn/models/magege/MDL-Qlora1/files) |

## 🚀 快速推理

### 使用 SWIFT 进行模型部署

```bash
CUDA_VISIBLE_DEVICES=0 \
swift deploy \
    --adapters lora=./train_ada/v3-20250928-095853/checkpoint-2300 \  
    --infer_backend vllm \
    --temperature 0 \
    --max_new_tokens 2048 \
    --served_model_name Qwen2.5-7B-Instruct-lora1
```

### 参数说明
- `CUDA_VISIBLE_DEVICES=0`: 指定使用 GPU 0
- `--adapters lora=path/to/checkpoint`: 指定 LoRA 适配器路径（需自行替换）
- `--infer_backend vllm`: 使用 vLLM 推理后端以获得最佳性能
- `--temperature 0`: 设置温度为0，确保生成结果确定性
- `--max_new_tokens 2048`: 最大生成长度为2048个token
- `--served_model_name`: 部署的模型服务名称（可自行敲定）

### 不同模型的推理示例

**使用 LoRA Epoch 1 模型：**
```bash
CUDA_VISIBLE_DEVICES=0 \
swift deploy \
    --adapters lora=./MDL-lora1/checkpoint \
    --infer_backend vllm \
    --temperature 0.1 \
    --max_new_tokens 1024 \
    --served_model_name MDL-lora1
```

**使用 LoRA Epoch 2 模型：**
```bash
CUDA_VISIBLE_DEVICES=0,1 \
swift deploy \
    --adapters lora=./MDL-lora2/checkpoint \
    --infer_backend vllm \
    --temperature 0.1 \
    --max_new_tokens 2048 \
    --served_model_name MDL-lora2
```

**使用 QLoRA 模型：**
```bash
CUDA_VISIBLE_DEVICES=0 \
swift deploy \
    --adapters lora=./MDL-Qlora1/checkpoint \
    --infer_backend vllm \
    --temperature 0.2 \
    --max_new_tokens 1536 \
    --served_model_name MDL-Qlora1
```

## 💡 使用说明

1. **环境准备**: 确保在云上环境中运行所有训练和推理流程
   - LoRA Epoch: 微调版本
   - QLoRA: 内存效率更高的微调版本

2. **推理部署**: 
   - 下载对应的模型检查点
   - 根据需要调整推理参数（temperature、max_new_tokens等）
   - 使用上述脚本快速启动推理服务

3. **API 调用**: 部署成功后，可通过 REST API 进行医疗对话推理

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目。

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

*注意：所有训练和推理流程建议在云上环境中执行，以确保计算资源的充足和稳定性。*

