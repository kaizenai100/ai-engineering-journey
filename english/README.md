# AI Engineering 核心词汇表

## Week 1

| 单词 | 发音 | 中文 | 记忆方法 |
|------|------|------|---------|
| prompt | /prɒmpt/ | 提示词 | 给模型的"指令"，你每天都在写 |
| retrieve | /rɪˈtriːv/ | 检索/取回 | RAG 的 R，从知识库里"取回"文档 |
| embedding | /ɪmˈbedɪŋ/ | 向量嵌入 | 把文字"嵌入"数字空间，变成向量 |
| inference | /ˈɪnfərəns/ | 推理 | 每次调 API，模型生成回答就是一次 inference |
| fine-tune | /faɪn tjuːn/ | 微调 | 在预训练模型上"微微调整"参数 |
| token | /ˈtoʊkən/ | 词元 | LLM 处理文本的最小单位，"你好"≈1-2 个 token |
| context | /ˈkɒntekst/ | 上下文 | messages 列表就是 context，模型能"看到"的窗口 |
| chain | /tʃeɪn/ | 链 | Chain of Thought = 思维链，步骤串起来 |
| agent | /ˈeɪdʒənt/ | 智能体 | 你的 CLI 客服助手就是一个 agent |
| schema | /ˈskiːmə/ | 模式/结构定义 | Function Calling 里的 JSON Schema |

## Week 2

| 单词 | 发音 | 中文 | 记忆方法 |
|------|------|------|---------|
| pipeline | /ˈpaɪplaɪn/ | 管道/流水线 | LCEL 的 `prompt \| model \| parser` 就是 pipeline |
| parse | /pɑːrs/ | 解析 | OutputParser 的 parse，JSON.parse() |
| template | /ˈtemplɪt/ | 模板 | PromptTemplate，注意拼写不是 templet |
| output | /ˈaʊtpʊt/ | 输出 | OutputParser 的 output |
| wrapper | /ˈræpər/ | 包装器 | LangChain 就是 OpenAI SDK 的 wrapper |

