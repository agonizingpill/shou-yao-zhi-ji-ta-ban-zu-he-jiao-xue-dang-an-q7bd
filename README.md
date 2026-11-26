# 手摇织机踏板组合教学档案

织野技师课堂以纸本录下踏板规律，复核容易混淆的纹样后在不同织架之间安全替换课程示范。

## 现场工作与联系人

模拟客户为织野工艺技师课堂。机型线位、动作样段、判别轴纠混、示范动作替换；不同机型脚位映射未签约禁止替换。

- 织架与踏板对照 `looms`，字段为 `machine`（机型）、`pedal_count`（踏板数）、`mapping_signed`（脚位映射已签）。模型约束位于 `backend/domain/looms_model.py`，规则位于 `looms_service.py`。
- 动作样段 `segments`，字段为 `loom`（织架）、`pattern`（物料纹样）、`right_rate`（右脚频次）、`left_rate`（左脚频次）、`pause`（踏间停顿 s）、`checked`（已对拍）、`revoked`（已撤销对拍）、`revoked_at`（撤销时间）。模型约束位于 `backend/domain/segments_model.py`，规则位于 `segments_service.py`。
- 判别纠混签注 `axes`，字段为 `segment`（待辨动作）、`suggestion`（判别纹样）、`confidence`（模型概率）、`holdout`（留出正确率）、`token`（计算号）、`state`（有效/已作废/待复核）。模型约束位于 `backend/domain/axes_model.py`，规则位于 `axes_service.py`。
- 签注样段来源 `axis_lineages`，逐条登记每个签注用过的样段与角色（target 待辨、train 训练、holdout 留出），撤销对拍时据此追溯，规则位于 `revocation_service.py`。
- 撤销对拍事件 `revocations`，保存每次撤销的影响快照（作废签注、待复核签注、被拦计算号、受牵连节次与回退结果），重放可查、重试不重复回退。
- 课堂示范册 `lesson_demos`，字段为 `axis`（判别依据）、`loom`（示范织架）、`lesson`（节次）、`state`（状态）、`replaced_from`（上一版本，构成替换链）。模型约束位于 `backend/domain/lesson_demos_model.py`，规则位于 `lesson_demos_service.py`。

团队为模拟的4 人工艺课堂，维护多架手摇织机的工艺教学例片。

技师用脚位图、动作片段和课堂讲义手工核对。不同织架的脚位号容易混用，平纹和斜纹节奏难肉眼判别，旧示范替换后难追到来源。

上游是机型脚位签记和对拍动作，授课技师拿到有版次关联的新示范。

### 一天的业务操作

1. 08:40 查看 LM-EAST 与 LM-WEST 的脚位对照。
2. 09:00 在 LM-EAST 上录制 SEG-A，右频 1.88。
3. 09:30 复核员对拍确认 SEG-A。
4. 10:30 用同织架分层留出八个样段，绘出判别轴。
5. 11:00 AXIS-02 签认斜纹。
6. 13:45 缺少目标织架签约，保留 LESSON-01。
7. 14:20 脚位图 A-219 双签后替换，保有可回退版本。
8. 15:10 复核员发现 SEG-09 对拍有误，撤销对拍：相关签注作废、排队计算拦下、在用示范沿替换链回退或停用，影响记入撤销影响台账。

## 撤销对拍规则

复核员可对已对拍样段执行 `/segments/revoke-segment`，规则集中在 `backend/domain/revocation_service.py`：

1. 样段置 `checked=false`、`revoked=true`；已撤销样段不能再次对拍，也不能作为待辨或参考样段进入计算。
2. 凡在 `axis_lineages` 中用过该样段的签注一律转 `已作废`——待辨（target）、训练（train）、留出（holdout）三种用法都算。
3. 排队中的计算若用过该样段（无论待辨还是参考），任务置 `rejected`，无法再签注；worker 落库前与签注提交时另有两道数据库兜底校验。
4. 受牵连的在用（`当前示范`）示范沿 `replaced_from` 替换链退到最近的有效版本：当前示范转 `已撤回`、旧版本恢复 `当前示范`；整条链找不到有效版本则当前示范转 `已停用`。
5. 没有来源台账、查不清用过哪些样段的旧签注转 `待复核`，不参与示范回退，也不能再用于替换或退回。
6. 撤销与示范替换同批提交时，撤销在同一事务内先把受影响签注作废，替换随后因签注非 `有效` 被拒绝。
7. 重试撤销直接重放已登记事件的影响快照，不重复回退；`GET /revocations` 工作台可查受影响节次、原签注、被拦计算号与回退/停用结果。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18309`。FastAPI OpenAPI 在 `http://127.0.0.1:19309/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
本机开发时，在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 织架与踏板对照 | `/looms` /looms/sign-mapping | `frontend/src/pages/looms.js` |
| 动作样段 | `/segments` /segments/record-segment，/segments/verify-segment，/segments/revoke-segment | `frontend/src/pages/segments.js` |
| 判别纠混签注 | `/axes` /axes/fit-axes，/axes/record-axis | `frontend/src/pages/axes.js` |
| 课堂示范册 | `/lesson_demos` /lesson_demos/replace-demo，/lesson_demos/restore-demo | `frontend/src/pages/lesson_demos.js` |
| 撤销对拍影响台账 | `/revocations` | `frontend/src/pages/revocations.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 LinearDiscriminantAnalysis。训练集上拟合 StandardScaler 与 LDA。按纹样分层留出 1/3，固定随机种子 24，返回二维坐标和模型分值。

动作数据为课堂模拟样段。当前版本采用结构化记录和判别坐标，课堂短片保留在线下。

[MIT](LICENSE)
