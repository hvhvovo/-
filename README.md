# Booking API Tests

[![Offline tests](https://github.com/hvhvovo/-/actions/workflows/tests.yml/badge.svg)](https://github.com/hvhvovo/-/actions/workflows/tests.yml)

使用 Python、requests 与 pytest，针对 [Restful Booker](https://github.com/mwinteringham/restful-booker) 公开演示 API 开展接口自动化测试。重点是数据隔离、状态验证、鉴权拒绝及失败诊断。被测系统由原作者开发，本仓库提供测试工程。

## 测试范围

- **17项在线测试**：预订创建/读取、完整与部分更新、删除后查询、鉴权拒绝后数据不变、姓名筛选、合法边界值保存，以及列表与详情响应契约。
- **17项离线检查**：字段与日期校验、网络/响应异常诊断、清理前归属核验。
- 参数化展开共34项。离线检查不能算真实接口通过，跳过也不能算通过。

## 快速运行

只需要 Python 与两个依赖库，不需要 Docker、WSL、Java 或本地数据库。

Windows PowerShell，在项目目录运行：

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py offline
```

已有虚拟环境与依赖时，仅需最后一行。在线只读与完整流程需显式选择：

```powershell
.\.venv\Scripts\python.exe run.py read
.\.venv\Scripts\python.exe run.py full
```

也可双击 `run-full.cmd`，前提是 `.venv` 已存在。macOS/Linux 使用 `python3 -m venv .venv`，其余命令中的解释器替换为 `.venv/bin/python`。

| 模式 | 执行范围 |
|---|---|
| offline | 本地检查，在线用例跳过，不访问演示服务 |
| read | 本地检查加列表、详情、未知路径及错误凭据，不创建预订 |
| full | 全部用例，创建测试专属预订并在结束时尝试清理 |

## 数据与诊断

每个写入用例独立创建带随机姓名的记录，仅修改该次创建返回的编号。Fixture在结束时尝试清理，删除前核对姓名，归属发生变化时拒绝删除。检查与删除不是原子操作，仍有共享环境竞争窗口。

不自动重试写请求，避免响应丢失时重复创建；创建成功但响应丢失可能遗留数据，应记录。公共服务会重置或被他人修改，失败需排查网络、环境与脚本问题，不能直接判为产品缺陷。不进行压测。

运行后在 `reports/` 生成 HTML、JUnit 与 `*-cases.json`。报告分别统计在线和离线结果；请求元数据仅记录方法、路径、状态与耗时，不保存认证头、Cookie或请求正文。清理请求不在该轨迹内，失败通过teardown结果体现。报告默认不提交，可从CI的artifact获取离线运行报告。

## 验证记录与边界

2026-10-23，开发环境 Linux/Python 3.12 完整运行34项通过；使用者提供的 Windows/Python 3.14.7 完整运行输出也显示34项通过，17在线、17离线，无跳过。历史实跑仅代表当时环境，不证明生产正确率或容量。远程CI状态以本仓库Actions为准，CI默认只跑离线模式。

当前没有已确认的产品缺陷；没有数据库核验、负载/并发容量或完整异常输入覆盖。演示接口的零金额等行为属于当前接口特征，不是对真实酒店业务的建议。

## 项目结构

| 路径 | 用途 |
|---|---|
| `booking/client.py` | 请求封装、诊断与请求元数据 |
| `booking/checks.py` | 响应字段及日期检查 |
| `conftest.py` | 执行开关、Fixture与测试数据清理 |
| `tests/` | 在线及离线用例 |
| `run.py` | 执行入口与报告 |
| `docs/` | 预期依据、用例矩阵、复盘与问题模板 |

[测试依据](docs/CONTRACTS.md) · [用例矩阵](docs/TEST_MATRIX.md) · [验证记录](VALIDATION_V2.md) · [面试复盘](docs/INTERVIEW.md)

代码使用 ChatGPT 辅助生成与迭代，保留实际职责边界，不声称全部独立手写。使用者应理解预期、能修改测试并解释结果后，再用于求职项目陈述。
