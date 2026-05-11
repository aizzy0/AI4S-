# Hermes Agent Windows 安装与配置完整教程

> 📺 参考视频：[B站 - 保姆级教程] Windows 上直接安装 Hermes Agent 及配置完整教程
> 🎤 UP主：Andy要上岸机器学习
> 📄 补充：Hermes Agent 官方文档
> 
> 本教程涵盖：Windows 原生安装、Token 获取、大模型配置、飞书/微信接入

---

## 目录

1. [环境准备与安装](#1-环境准备与安装)
2. [Token 科普与获取](#2-token-科普与获取)
3. [大模型配置](#3-大模型配置)
4. [飞书配置](#4-飞书配置)
5. [微信配置](#5-微信配置)
6. [验证安装](#6-验证安装)
7. [常见问题](#7-常见问题)

---

## 1. 环境准备与安装

### 1.1 Windows 原生安装（不用 WSL）

**前置要求：**
- Windows 10/11（64位）
- Python 3.10 或更高版本
- 网络环境能访问 GitHub（必要时准备代理）

**安装步骤：**

```bash
# 步骤1：安装 Python（如果没有）
# 从 https://www.python.org/downloads/ 下载安装包
# 安装时务必勾选 "Add Python to PATH"

# 步骤2：验证 Python 安装
python --version
pip --version

# 步骤3：安装 Hermes Agent
pip install hermes-agent

# 步骤4：验证安装
hermes --version
```

> ⚠️ **注意：** 如果 pip 安装慢，可以换国内源：
> ```bash
> pip install hermes-agent -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 1.2 初始化配置

```bash
# 运行安装向导
hermes setup

# 或者直接启动（会自动引导首次配置）
hermes
```

---

## 2. Token 科普与获取

> ⚠️ **重点提醒（视频特别强调）：**
> **TOKEN 不是会员！** 需要自己买套餐包！

### 2.1 什么是 Token？

Token 是大模型 API 的计费单位，可以理解为"字数/字符数"：
- 输入 Token：你发送的消息 + 历史记录
- 输出 Token：模型回复的内容
- 不同模型价格不同（一般几元到几十元/百万Token）

### 2.2 常见获取途径

#### 方案 A：OpenRouter（推荐，支持最多模型）

| 步骤 | 操作 |
|------|------|
| ① | 打开 [openrouter.ai](https://openrouter.ai) 注册账号 |
| ② | 充值（最低 $5 起） |
| ③ | 进入 Settings → API Keys → 创建 Key |
| ④ | 保存到 `OPENROUTER_API_KEY` |

#### 方案 B：MiniMax（国内可用，免翻墙）

| 步骤 | 操作 |
|------|------|
| ① | 打开 [minimax.com](https://minimax.com) 注册 |
| ② | 进入控制台 → API Keys → 创建 |
| ③ | 购买套餐包（视频强调：不是会员！） |
| ④ | 保存到 `MINIMAX_API_KEY` |

#### 方案 C：智谱 GLM（国内可用）

| 步骤 | 操作 |
|------|------|
| ① | 打开 [open.bigmodel.cn](https://open.bigmodel.cn) 注册 |
| ② | 实名认证 → 创建 API Key |
| ③ | 购买资源包 |
| ④ | 保存到 `GLM_API_KEY` |

#### 其他国内可用 Provider

| 提供商 | 配置变量 | 备注 |
|--------|---------|------|
| 阿里通义千问 | `DASHSCOPE_API_KEY` | 有免费额度 |
| 月之暗面 Kimi | `KIMI_API_KEY` | 需充值 |
| DeepSeek | `DEEPSEEK_API_KEY` | 性价比高 |
| 零一万物 Yi | 配置 base_url | 需充值 |

---

## 3. 大模型配置

### 3.1 创建环境变量文件

在用户目录下创建或编辑 `.hermes/.env`：

```bash
# Windows PowerShell
notepad $env:USERPROFILE\.hermes\.env
```

写入以下内容（根据你选择的提供商填写）：

```bash
# 方式一：OpenRouter（优先推荐）
OPENROUTER_API_KEY=sk-or-v1-你的key

# 方式二：MiniMax（国内直连）
MINIMAX_API_KEY=你的miniMaxKey

# 方式三：智谱 GLM（国内直连）
GLM_API_KEY=你的glmKey

# 方式四：DeepSeek（性价比高）
DEEPSEEK_API_KEY=sk-你的deepseekKey
```

### 3.2 配置默认模型

```bash
# 交互式选择模型
hermes model

# 或手动配置
hermes config set model.default "openrouter/anthropic/claude-sonnet-4"
hermes config set model.provider openrouter
```

**推荐模型组合：**

| 场景 | 推荐模型 | 提供商 |
|------|---------|--------|
| 日常使用 | Claude Sonnet 4 | OpenRouter |
| 编码任务 | Claude Sonnet 4 / GPT-4o | OpenRouter |
| 性价比 | DeepSeek V3 | DeepSeek |
| 国内直连 | MiniMax-01 / GLM-4 | MiniMax/智谱 |
| 本地运行 | Qwen2.5 / Llama 3 | Ollama 本地 |

### 3.3 配置示例（config.yaml）

配置文件路径：`~/.hermes/config.yaml`

```yaml
model:
  default: "openrouter/anthropic/claude-sonnet-4"
  provider: openrouter

agent:
  max_turns: 90
  tool_use_enforcement: true

terminal:
  backend: local
  timeout: 180

memory:
  memory_enabled: true
  user_profile_enabled: true

display:
  skin: default
  tool_progress: true
```

---

## 4. 飞书配置（强烈推荐！）

> 视频中特别推荐飞书作为消息平台接入方式。

### 4.1 创建飞书应用

| 步骤 | 操作 |
|------|------|
| ① | 打开 [飞书开发者后台](https://open.feishu.cn/app) |
| ② | 点击 **创建应用** → 填写应用名称 |
| ③ | 进入 **凭证与基础信息** → 获取 `App ID` 和 `App Secret` |
| ④ | 进入 **权限管理** → 添加机器人权限 |
| ⑤ | 进入 **事件订阅** → 添加回调地址 |

### 4.2 配置飞书网关

```bash
# 启动网关配置向导
hermes gateway setup

# 选择 Feishu/Lark，按提示填入：
# - App ID
# - App Secret
# - Bot Token（可选）
```

**手动配置方式（在 config.yaml 中）：**

```yaml
gateway:
  enabled: true
  platforms:
    feishu:
      enabled: true
      app_id: "cli_xxxxxxxxxxxx"
      app_secret: "xxxxxxxxxxxxxxxxxxxxxxxxxx"
      bot_name: "你的机器人名称"
```

### 4.3 发布应用

1. 在飞书开发者后台 → **版本管理与发布**
2. 创建新版本 → 填写版本说明
3. 提交审核（企业内部应用可免审核直接发布）
4. 在飞书中搜索机器人名称 → 添加好友 / 拉入群聊

### 4.4 飞书使用优势

- ✅ 国内直连，无需翻墙
- ✅ 支持丰富的消息类型（图片、文件、Markdown）
- ✅ 企业级稳定
- ✅ 可拉入群聊协作

---

## 5. 微信配置

> ⚠️ 微信配置相对复杂，视频中做了简单对比说明。

### 5.1 配置方式

Hermes Agent 通过 **Weixin（个人微信）** 通道接入：

```bash
# 启动网关配置向导
hermes gateway setup
# 选择 weixin 选项
```

**配置参数：**

```yaml
gateway:
  platforms:
    weixin:
      enabled: true
      # 需要配置微信相关的认证信息
```

### 5.2 微信 vs 飞书对比

| 对比项 | 微信 | 飞书 |
|--------|------|------|
| 配置难度 | ⭐⭐⭐ 较复杂 | ⭐⭐ 中等 |
| 稳定性 | 依赖第三方库 | 官方API，稳定 |
| 国内可用 | ✅ | ✅ |
| 消息类型 | 基础文本/图片 | 丰富格式 |
| 群聊支持 | ✅ | ✅ |
| **推荐度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

> 视频建议：**优先使用飞书**，微信作为辅助通道。

---

## 6. 验证安装

### 6.1 基本检查

```bash
# 检查版本
hermes --version

# 健康检查
hermes doctor

# 查看配置
hermes config
```

### 6.2 启动并测试

```bash
# CLI 模式（直接对话）
hermes

# 输入测试消息
# 你好，请介绍一下你自己

# 启动网关（连接消息平台）
hermes gateway run
```

### 6.3 常用命令速查

```bash
# 查看所有命令
hermes --help

# 更改模型
hermes model

# 启用/禁用工具
hermes tools

# 查看技能列表
hermes skills list

# 配置管理
hermes config set <section>.<key> <value>
hermes config edit
```

---

## 7. 常见问题

### Q1：安装时报错 `pip` 找不到

**解决：** 确保 Python 已添加到 PATH，或者使用：
```bash
python -m pip install hermes-agent
```

### Q2：启动后提示 API Key 错误

**解决：**
1. 检查 `.hermes/.env` 文件是否存在且格式正确
2. 确认 API Key 是否已充值/还有余额
3. 运行 `hermes doctor` 检查配置
4. 确认网络环境能否访问 API 服务

### Q3：飞书机器人无响应

**解决：**
1. 检查事件订阅地址是否正确配置
2. 确认应用已发布
3. 查看日志：`~/.hermes/logs/gateway.log`
4. 重启网关：`hermes gateway restart`

### Q4：Windows 上编码问题

**解决：**
- 配置文件务必保存为 **UTF-8 无 BOM** 格式
- 推荐使用 VSCode 或 Notepad++ 编辑配置文件
- 不要使用 Windows 自带的记事本（可能添加 BOM）

### Q5：网络环境不好，安装失败

**解决：**
```bash
# 使用国内镜像
pip install hermes-agent -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果 GitHub 下载脚本失败
# 手动下载安装包或使用代理
```

### Q6：如何更新 Hermes Agent

```bash
pip install --upgrade hermes-agent
```

---

## 参考资料

- 📖 Hermes Agent 官方文档：https://hermes-agent.nousresearch.com/docs/
- 📺 B站视频教程：[链接](https://www.bilibili.com/video/BV1vX5E6SEHt/)
- 💬 GitHub 仓库：https://github.com/NousResearch/hermes-agent
