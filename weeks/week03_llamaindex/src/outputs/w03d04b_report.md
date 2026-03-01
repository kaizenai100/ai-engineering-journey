Root cause（根因）
初始 nodes=2（coverage 不足）+ 中文 query 与英文 PDF 不匹配导致 keyword 抽取失败
Fix（改动）
降 chunk_size + 提 top_k
CN→EN query 翻译
Result（效果）
nodes 从 2 → 87（写数字）
平均分/有效命中显著提升
    测试用例：1.Scaled Dot-Product Attention 的公式是什么？为什么要除以 √d_k？评估：从0变成了2
            2.Position Encoding 是怎么做的？（sin/cos 的形式与直觉）评估：从0变成了2
Decision（决策）
默认：Vector（跨语言+语义召回稳定）
Fallback：Keyword由于是根据关键词匹配，所以只有当 query 同语言时效果才会好点
    示例：1.Scaled Dot-Product Attention 的公式是什么？为什么要除以 √d_k？评估：从0变成了2
Tree：结构性问题可用，但成本更高，召回数量不够，如果chunk_size太小，可能会说不清楚