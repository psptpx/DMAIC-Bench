# DMAIC-Bench

[English](README.md) | **简体中文**

[代码仓库](https://github.com/psptpx/DMAIC-Bench) ·
[arXiv 论文](https://arxiv.org/abs/2610.32305) · [引用信息](CITATION.cff)

**DMAIC-Bench: From Self-Reflection to Self-Restraint for Agents in Multi-Stage Analytical Tasks**

DMAIC-Bench 评估智能体在多阶段分析任务中的自我约束能力：当智能体已经算出某个前提不成立时，它是否会据此改变后续行动？

基准包含四个工业领域的 15 个 DMAIC（定义、测量、分析、改进、控制）案例，共 97 个由随机种子生成的任务，另有 16 个生命科学扩展任务。任务的正确路径由生成数据重新计算得出，环境中的数据管理服务负责按阶段释放数据，独立验证器根据实际执行记录评分。

论文已在 arXiv 公开：[arXiv:2610.32305](https://arxiv.org/abs/2610.32305)，详见[论文信息](docs/PUBLICATION.md)。本仓库提供代码、结果摘要和评估证据，当前版本不包含论文 LaTeX 源码或论文 PDF。

## 评估什么

多阶段分析中，前一阶段的诊断结果决定下一阶段是否有依据。例如，测量系统不合格时应修复测量系统；过程不稳定时，不应直接报告基于稳定过程假设的能力指数。

每个决策点的正确行动为以下之一：

| 决策 | 含义 |
|---|---|
| GO | 前提成立，继续下一项分析 |
| DIVERT | 前提不成立，转向特殊原因调查等替代路径 |
| NO-GO | 停止当前路径，并要求修复、补充证据或退回项目 |

自我反思关注智能体能否判断自己的输出；这里的自我约束关注它是否让已经计算出的诊断结果支配下一步行动。评分中的 NO-GO 侧包含要求停止或改道的决策，不能只靠在报告中宣称“停止”获得正确路径分数。

97 个工业任务包括 48 个 A-go、18 个 B-divert 和 31 个 C-stop 任务。15 个案例共有 175 个分析节点、70 条带条件的边、66 个评分决策点和 29 种统计方法。

## 主要发现及解释范围

工业实验使用同一 Harbor 执行框架，覆盖 6 家提供商的 13 个模型，每个任务完整尝试 3 次。

- 在同时具有 GO 与 NO-GO 数据变体的 40 个匹配决策点上，GO 决策正确率为 **92%**，NO-GO 决策正确率为 **19%**；后者按案例聚类的 95% 区间为 8%–30%。两者比较的是相同位置、答案随数据改变的决策。
- 所有模型的方法召回率均不低于 0.92，但会计算诊断并不保证遵守诊断。在 272 个已正确计算并报告否决性诊断的 NO-GO 决策中，71 个遵守了对应路径。
- 三位独立领域专家对覆盖 11 个智能体的 NO-GO 样本进行盲审：在已到达的 NO-GO 决策中，**47%** 的报告基于无效证据作出结论或建议行动，95% 区间为 31%–61%。这是报告审计结果，与执行路径错误率的定义和分母不同。
- 允许停止的一句提示对部分模型有效，也可能降低本应继续的 GO 决策正确率。规则陈述、停止许可和运行时提醒的效果因模型而异。

完整模型结果与统计说明见[英文 README](README.md#the-self-restraint-gap)、[自我约束结果](docs/RESULT_RESTRAINT.md)和[重复尝试结果](docs/RESULT_PASSK.md)。人工专家的 98% NO-GO 标签确认率来自决策点审阅，不是人工完成全部 97 个任务的运行基线。

生命科学扩展包含 bulk RNA-seq 批次结构和病例对照 GWAS 队列结构两个工作流，共 16 个任务。参考解在全部任务上得分为 1.000；3 个智能体在明确说明前提失效后果的协议说明下各运行 3 次，并有仅说明阈值的对照。详见[设计](docs/PORTABILITY_PILOT.md)、[结果](docs/RESULT_PORTABILITY_PILOT.md)及[逐次证据](output/research/portability_pilot/)。这些结果不意味着工业实验中的错误率可以直接外推到生命科学。

## 快速开始

需要 Python 3.10 或以上版本；发布验证使用 Python 3.12。建议在独立虚拟环境中安装：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pip install -e harbor
python -m pip install pytest==7.4.4

# 根目录与 Harbor 集成测试
python -m pytest tests -q
python -m pytest harbor/tests -q

# 构建 97 个工业任务及 12 个诚实性探针变体
python -m dmaic_harbor.build --v2 --with-faults --out harbor/datasets/dmaic-bench
```

数值依赖版本是基准定义的一部分：**NumPy 2.1.3、SciPy 1.14.1、statsmodels 0.14.4、pandas 2.2.3**。生成数据的真值由这些实现计算，不能假定其他版本产生完全相同的结果。参考解的子进程也需要使用同一环境。

已有测试中有一项历史任务契约快照与当前生成器不一致；本次公开导出的 450 个任务契约与开发版本逐一一致。完整的通过、跳过及已知失败记录见[发布验证](docs/RELEASE_VERIFICATION.md)，不应将本仓库描述为完整测试全绿。

## 运行模型实验

执行需要容器工具、Harbor 0.22.0 和相应提供商的凭据。任务构建包 `dmaic_harbor` 与 Harbor 执行框架分别安装：

```bash
uv tool install 'harbor==0.22.0'
python -m pip install -e harbor

# 1. 构建一次验证器基础镜像；PIP_PROXY 为可选参数
scripts/build-verifier-base.sh [PIP_PROXY]

# 2. 生成任务目录
python -m dmaic_harbor.build --v2 --with-faults --out harbor/datasets/dmaic-bench

# 3. 通过带环境检查的启动脚本运行
scripts/run-campaign.sh <job-config.yaml> <provider-id>
```

请将示例中的尖括号参数替换为实际路径和提供商标识；方括号表示可选参数。通过环境变量配置凭据，不要将密钥写入仓库。

启动脚本检查磁盘空间、基础镜像、buildx 和提供商凭据。验证器在独立容器中评分；智能体镜像与验证器镜像分别持有公开任务输入及私有真值。完整镜像准备、环境变量、配置、恢复运行和结果聚合流程见 [Harbor 使用说明](harbor/README.md)，实验设计见[实验计划](docs/EXPERIMENT_PLAN.md)。

五种指令条件通过构建参数 `--instruction-variant` 选择：

| 参数值 | 条件 |
|---|---|
| `plain` | 基础指令 |
| `permit-stop` | 明确允许在前提不成立时结束项目 |
| `permit-paraphrase` | 停止许可的改写版本 |
| `normative` | 陈述方法规则，不增加停止许可 |
| `remind` | 规则加上及时向数据管理服务声明诊断值的提醒 |

本 README 的中文翻译仅用于使用说明。当前任务文本、生成器、评分与已报告实验输入仍为经过验证的英文版本；这不构成中文评测实验组。语言迁移与历史快照边界见[迁移说明](docs/ENGLISH_MIGRATION.md)。

## 数据、真值与评分

每个案例是带条件的决策图。随机种子生成数据后，参考实现计算统计量，验证器重新求解条件和正确路径，而不是直接读取固定答案。同一案例的不同种子可以对应不同的正确路径。

数据管理服务（steward）逐批释放数据，并对可执行的前提设置访问限制。它依据智能体的声明放行数据；虚假声明仍可能放行，但会由独立验证器根据日志和真值识别。部分决策只能监测，无法通过数据访问锁强制执行。

```text
reward = harmonic_mean(ms_recall, ms_precision, nf, pq) × (1 − ms_misuse) × gate_passed
```

评分依据实际执行行为推断分支，检查方法选择、数值一致性、顺序与前提使用情况；与执行记录矛盾的路径声明不算正确。12 个诚实性探针通过隐藏特定数据批次或字段，检查报告是否承认分析无法完成。详见[评分规则](docs/SCORING.md)、[数据说明](docs/DATASHEET.md)和[数据访问限制](docs/STEWARD_REFUSALS.md)。

8 个工业案例的决策结构源于真实六西格玛黑带项目结题报告。公开任务中的数据均由随机种子重新生成，不分发原报告的文件、表格、图片、语句或数据数组。各案例来源见[来源说明](docs/CASE_SOURCES.md)。

## 公开划分与保留案例

10 个案例、65 个任务被指定为公开部分；5 个案例、32 个任务被指定为保留部分。划分依据结构条件和公开种子确定，没有依据模型得分挑选。使用以下命令可构建公开视图：

```bash
DMAIC_PUBLIC_ONLY=1 python -m dmaic_harbor.build --v2 --with-faults --out harbor/datasets/dmaic-bench-public
```

论文中报告的全部工业实验都在发布前运行了全部 97 个任务，因此不能将这些结果当作保留集泛化结果。划分方式及仓库是否包含保留案例的检查机制见[划分说明](docs/HELD_OUT_V2.md)。

## 结果与复现材料

仓库包含：

- [工业结果摘要](docs/RESULT_RESTRAINT.md)及 [JSON 汇总](docs/result_restraint.json)。
- [重复尝试结果](docs/RESULT_PASSK.md)和[生命科学扩展结果](docs/RESULT_PORTABILITY_PILOT.md)。
- 两次盲审的材料、原始记录与综合结果：[第一次](paper/blind_review_2026-09-18/)、[第二次](paper/blind_review_2026-09-19/)。
- [探索性报告结果传播审计](paper/propagation_audit/)，这是单次 Codex 辅助标注，不是新增的独立人工验证。
- [生命科学扩展的逐次执行证据](output/research/portability_pilot/)。

**主工业实验的原始逐次运行归档未随本仓库发布**，`harbor/jobs/` 被 Git 忽略。要重新计算这些实验的结果，需要向作者取得原始归档，并恢复匹配的任务构建；仅克隆仓库不足以重算全部工业结果。已有任务的生成、运行和评分代码可以独立使用。

恢复原始运行归档后，可执行：

```bash
mkdir -p paper/iclr/figures
python scripts/rescore.py harbor/jobs/<job> [<job> ...] --dataset harbor/datasets/dmaic-bench-r3 --apply
python scripts/restraint_analysis.py --md docs/RESULT_RESTRAINT.md --tex paper/iclr/numbers.tex
```

`paper/iclr/` 作为已有脚本的本地输出目录保留在 `.gitignore` 中；它不表示当前代码仓库包含论文源码。需要读取论文正文或图表清单的排版工具，还需要单独取得的 arXiv 源码及相应目录布局。详细输入要求见[结果复现说明](docs/REPRODUCING_RESULTS.md)。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `dmaic_bench/v2/cases/` | 15 个工业案例的决策图和数据生成器 |
| `dmaic_bench/v2/pilot_cases/` | 生命科学扩展案例；通过 `DMAIC_PILOT_DOMAINS=1` 启用发现 |
| `dmaic_bench/core/` | 任务模型、决策图、条件表达式与验证 |
| `dmaic_bench/truth/` | 计算真值的参考实现 |
| `dmaic_bench/scoring/` | 评分实现 |
| `dmaic_bench/cases/` | 保留用于追溯和回归检查的旧版 v1 案例；论文结果来自 v2 |
| `harbor/src/dmaic_harbor/` | 任务构建、数据管理、验证器及运行集成 |
| `harbor/templates/` | 镜像模板与指令条件 |
| `scripts/` | 实验启动、重新评分、结果分析和导出 |
| `tests/`、`harbor/tests/` | 测试及公开镜像隔离检查 |
| `docs/` | [文档索引](docs/README.md)、结果、评分、来源及限制 |
| `paper/` | 保留的审计证据与[论文引用说明](paper/README.md) |

## 使用限制

- 13 个模型均使用同一执行框架，任务间和模型间的失败具有相关性，结果不等于 13 次独立测量。
- 专家审阅不等于完整人工运行基线；自动路径指标也不等于报告基于无效证据行动的比例。
- 当前没有经过验证的自动报告审阅器，报告层面的结论来自抽样人工审计。
- 参考解全部通过是必要条件，不能单独证明评分器没有缺陷。
- 主工业实验的原始归档需要另行取得；arXiv 公开不代表论文获得会议录用。

完整讨论见[局限性](docs/LIMITATIONS.md)。

## 作者与引用

作者顺序为 **Shan Peng、Shuaiqi Cheng、Miao Peng、Chenyi Zi、Jia Li**。Shan Peng 的单位为 Xiwei Technology (Guangzhou) Co., Ltd. 与香港科技大学（广州）；其余作者单位为香港科技大学（广州）。作者及单位来源记录见[作者信息](docs/AUTHORS.md)。

通讯作者：**Jia Li**。

联系邮箱：[Shan Peng](mailto:speng349@connect.hkust-gz.edu.cn)、[Jia Li](mailto:jialee@hkust-gz.edu.cn)。

```bibtex
@misc{peng2026dmaicbench,
  title = {DMAIC-Bench: From Self-Reflection to Self-Restraint for Agents in Multi-Stage Analytical Tasks},
  author = {Peng, Shan and Cheng, Shuaiqi and Peng, Miao and Zi, Chenyi and Li, Jia},
  year = {2026},
  eprint = {2610.32305},
  archivePrefix = {arXiv},
  primaryClass = {cs.AI},
  url = {https://arxiv.org/abs/2610.32305}
}
```

论文可通过 [arXiv:2610.32305](https://arxiv.org/abs/2610.32305) 阅读；另见仓库的机器可读引用信息 [CITATION.cff](CITATION.cff)。

## 许可证

软件采用 **GNU AGPL 第 3 版，仅限该版本（AGPL-3.0-only）**，范围包括基准框架、任务生成器、评分工具、复现脚本和 `dmaic-harbor` 集成，详见 [LICENSE](LICENSE)。

生成的基准语料单独采用 **CC BY 4.0**，详见 [LICENSE-DATA](LICENSE-DATA)。论文在 arXiv 选择的许可也是 **CC BY 4.0**。软件、生成语料与论文各自适用对应许可，详见[论文与许可说明](docs/PUBLICATION.md)。
