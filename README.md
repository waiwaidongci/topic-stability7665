# 字岑展览语义主题册

字岑策展文本研究组的 15 位编辑需要把匿名、已分词的展签摘要整理成可审阅的主题册。上游提供 `zc-exhibition-tokens-2026.jsonl`，下游得到人工命名的主题与已确认编辑说明 CSV。项目处理关键词堆叠忽略混合内容、重复初始化改变主题顺序、重建误差被误读为语义质量这三个问题。

这是固定种子的合成场景，不含真实观众或作品身份。初始 360 篇文档约 50 词、四组混合内容，其中刻意包含空文本、全部非白名单词、低频词样本。默认 K=4、5 次初始化得到 357 篇有效文档、49 词。实际参考相对重建误差约 0.4959007151；其值不代表主题语义正确率。

## 启动

```sh
cp .env.example .env
docker compose up --build -d --wait
docker compose exec -T backend python -m scripts.seed_demo
```

前端 http://localhost:18225 ，API http://localhost:19225/docs ，MySQL 127.0.0.1:17725。Nginx `/api/` 与前端请求前缀一致。Compose 恰好 frontend、backend、worker、db、redis 五个服务，各有健康检查；worker 通过 Redis 接收真实 Celery 任务。首次启动也自动执行幂等 seed，手动再次执行不会覆盖已有编辑。

|账号|密码|职责|
|---|---|---|
|admin@zicen.demo|Zicen2026!|导入、运行、人工命名、审阅和审计|
|analyst@zicen.demo|Zicen2026!|核对、创建任务、人工命名及提交编辑说明|
|viewer@zicen.demo|Zicen2026!|阅读结果，下载已确认 CSV|

演示密码与 JWT secret 仅供本地，部署时通过 `.env` 设置。前端开发 `cd frontend && npm ci && npm run dev`；构建 `npm run build` 同时执行 vue-tsc。停止并清除本题演示数据使用 `docker compose down -v --remove-orphans`。

## 编辑的一天

1. 09:00，主题研究编辑周宁登录研究首页，读“稳定的词组，也需要人来读”。
2. 在“分词语料”核对 `秋季展签分词摘要 · 360篇` 的 reference、标题与空白分词文本；也可按页面 JSON 示例导入 5–1000 篇新文档。
3. 在“主题配置”预先决定 K=4、初始化重复 5、seed=221、min_df=2、max_iter=2000 和 tolerance=0.0001，再送入队列。K 是编辑研究选择，不自动按跨 K 的重建误差下降选优。
4. 在“词权与稳定”选择任务，查看冻结输入指纹、357 有效文档、3 个排除理由、词汇和 IDF。5 次真实拟合使用 seed 221–225，各自保存迭代数与重建误差。
5. 读主题词权与代表文档的相对激活，将“待命名主题01”改为自己的编辑名称，并留下命名依据。名称由人工输入，程序没有语义真值标签。
6. 对齐表展示每次独立拟合相对于第 0 次拟合的 Hungarian 匹配、每主题余弦相似度和原始匹配编号。第 0 次是预先固定参考，不是按误差挑选的赢家。
7. 在“编辑审阅”选择主题、写解释和后续核对行动，创建编辑说明。说明冻结所选主题的名称、词权、相似度快照。
8. 负责人 admin 阅读后确认或退回。viewer 只能下载已确认说明 CSV。后续修改实时主题名不会改写已经审阅的快照。
9. 在“成册留痕”核对导入、任务、命名、说明、审批与导出审计；每个请求携带 X-Request-ID。

## 数值口径

- 分词仅使用 `str.split()` 空白切分，严格匹配 `backend/src/constants/vocabulary.py` 的 50 词白名单。没有自动中文分词或词义扩展。词汇从所选语料按 min_df 筛选并排序；保存词汇、df、IDF 和全部参数。
- TF 是原始词频；`idf(t)=ln((1+n)/(1+df(t)))+1`；每篇 TF-IDF 向量 L2 归一。n 包含所选空文档。白名单或 min_df 后零行从 NMF 排除，理由单独保留，不悄悄删去 IDF 样本。
- NMF 使用 sklearn 的 random 初始化、coordinate descent、Frobenius 目标、无正则与固定 random_state。用户选择 K∈[2,6]，重复 5–10 次。每次都调用真实 `fit_transform`；任一次未收敛即任务失败，不拼成虚假稳定结果。
- H 每行 L1 归一时，W 同列乘以原 H 行和，所以 WH 不变。保存每次原顺序和对齐后的 W/H、seed、迭代、重建误差、余弦矩阵、置换与各主题相似度。
- 归一 H 通过 L2 余弦与 Hungarian 一对一最优匹配。平均稳定性只统计非参考重复，避免把参考自身的 1 加入均值。相似度量化初始化敏感性，不等于语义真值；相近或简并主题的匹配可能不唯一。
- 文档展示 W 与 `W_i/sum(W_i)` 的相对激活。这是归一后的模型强度，不是概率后验。H 词权也不是词义置信度。
- 有限非负矩阵、K 不超文档数/词数且不超数值秩（绝对容差 1e-10）。常量/低秩、空词汇、空主题与未收敛均明确失败。不同 K、词汇、min_df 的误差不直接比较语义质量。
- MySQL 使用 DOUBLE，SQLAlchemy 设置 `asdecimal=False`，避免默认 Decimal 结果的十位小数转换损失；API 测试将持久化主题均值与逐次余弦重新计算比较到 1e-12。

## 结构

75 个有职责的 Python/TypeScript/Vue/CSS 源文件（不含空包、依赖和编译产物）。六个业务页面为研究首页、分词语料、主题配置、词权与稳定、编辑审阅、成册留痕。五个业务实体 Corpus → TokenDocument → TopicRun → TopicProfile → EditorialNote，另有 User/AuditLog。路由、schema、服务、ORM、前端 API/store 和页面形成完整链路。

后端枚举位于 `src/constants/enums.py`，前端对应 `src/constants/enums.ts`。RequestID 与 Error 两个中间件统一请求追踪和错误边界。TopicTerms、RunSummary、RunTable、AlignmentGrid 和 common 组件复用真实接口数据。Celery 的结果持久化后由前端轮询刷新。审阅前冻结主题快照以保持批准结果的可复查性。

## 验证与边界

真实容器/API/独立数值 oracle、seed 保修改、角色 403、真实浏览器导入到导出与截图结果见 `TESTING.md`。测试产物独立存放在批次 `test-artifacts/gb-0021`，不混入源码。主 fixture 的 360 篇与浏览器另外导入的 8 篇块状语料是两次不同研究；后者可分解到近零误差，不能据此声称真实语料同样可完美重建。

当前面向已分词、固定领域白名单，未验证外部真实中文语料、跨领域泛化或生产并发。最多 1000 文档、10 次串行初始化，worker 并发 1；没有自动选 K、自动主题命名、在线增量词汇或外部发布。白名单会过滤未知词，编辑需核对原文。数值秩阈值及 NMF 容差会影响可拟合边界。元数据通过 SQLAlchemy create_all 创建，未提供生产迁移链。字体使用 Google Fonts，断网时退回本地衬线/无衬线字体。
