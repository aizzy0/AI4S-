# OpenClaw 腾讯云一键部署教程

> 📺 参考视频：[B站 - 03-腾讯云一键部署OpenClaw](https://www.bilibili.com/video/BV1mrXBBWE2S/)
> 🎤 UP主：丨一丨丨二丨丨三丨
> ⏱ 时长：17分28秒
>
> 本教程涵盖：腾讯云轻量服务器选购、OpenClaw 一键部署、模型配置、消息渠道接入

---

## 目录

1. [前提条件](#1-前提条件)
2. [服务器选购](#2-服务器选购)
3. [一键部署（推荐）](#3-一键部署推荐)
4. [Docker 手动部署](#4-docker-手动部署)
5. [npm 安装部署](#5-npm-安装部署)
6. [防火墙配置](#6-防火墙配置)
7. [模型/Provider 配置](#7-模型provider-配置)
8. [消息渠道接入](#8-消息渠道接入)
9. [安全配置](#9-安全配置)
10. [验证与测试](#10-验证与测试)
11. [常见问题](#11-常见问题)

---

## 1. 前提条件

| 条件 | 说明 |
|------|------|
| ☁️ **腾讯云账号** | 已实名认证 |
| 🌐 **域名（可选）** | 用于配置 HTTPS/SSL |
| 🔑 **模型 API Key** | 至少一个（腾讯混元 / DeepSeek / 通义千问 / OpenAI 等） |
| 💻 **SSH 客户端** | 用于登录服务器（可选，一键部署可不需） |

---

## 2. 服务器选购

### 推荐配置：腾讯云轻量应用服务器 (Lighthouse)

| 档位 | 配置 | 参考价格 | 适用场景 |
|------|------|---------|---------|
| 🟢 **入门** | 2核2G / 40GB / 3M带宽 | ~¥288/年 | 单人轻量体验 |
| 🟡 **推荐** 🏆 | **2核4G / 60GB / 5M带宽** | ~¥500/年 | **2-5人使用，主力推荐** |
| 🔴 **进阶** | 4核8G / 100GB / 8M带宽 | ~¥1,000/年 | 高并发/复杂任务 |

**系统：** Ubuntu 22.04 / 24.04 LTS

> 💡 **经验之谈：** 4GB 内存是甜点配置。2GB 容易 OOM（内存不足），OpenClaw 官方推荐最低 8GB，但 2核4G 对个人/小团队完全够用。

---

## 3. 一键部署（推荐）

> 🎯 **这是视频中演示的方式，最简单快捷。**

### 3.1 通过 Lighthouse 模板创建

```bash
# 步骤：
1. 打开腾讯云官网 → 轻量应用服务器控制台
2. 点击 "新建实例"
3. 选择：应用模板 → AI智能体 → OpenClaw
4. 配置：2核4G / Ubuntu 24.04
5. 选择地域：广州/上海（国内低延迟）
6. 设置密码或 SSH 密钥
7. 确认购买，等待 1-2 分钟创建完成
```

创建完成后，OpenClaw 已**预装并自动启动**，只需配置模型和渠道即可使用。

### 3.2 初始化配置

1. 浏览器打开：`http://<服务器公网IP>:18789`
2. 使用默认管理员账号登录（从服务器应用管理获取初始密码）
3. 进入设置页面配置模型和渠道

---

## 4. Docker 手动部署

适用于已有服务器或想自己控制的用户：

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose git -y

# 2. 克隆部署包
git clone https://github.com/openclaw/deploy-kit.git
cd deploy-kit
cp .env.example .env

# 3. 编辑 .env 填写配置
#    SERVER_IP=你的服务器公网IP
#    ADMIN_PASSWORD=强密码

# 4. 一键部署
sudo bash deploy.sh
```

---

## 5. npm 安装部署

最灵活的方式，适合有 Node.js 经验的用户：

```bash
# 前置要求：Node.js 22.16+（推荐 Node 24）
curl -fsSL https://openclaw.ai/install.sh | bash

# 运行安装向导
openclaw onboard --install-daemon

# 验证
openclaw gateway status

# 打开控制面板
openclaw dashboard  # 打开 http://127.0.0.1:18789
```

---

## 6. 防火墙配置

> ⚠️ **最关键的一步！90% 的访问失败都是防火墙问题。**

| 端口 | 协议 | 用途 |
|------|------|------|
| **18789** | TCP | OpenClaw Web 控制面板 |
| 8080 | TCP | 管理后台（备用） |
| 443 | TCP | HTTPS（如配置 SSL） |
| 80 | TCP | HTTP（可选） |

**配置方法：**
1. 腾讯云控制台 → 服务器 → 防火墙 → 添加规则
2. 协议：TCP，端口：18789，来源：`0.0.0.0/0`
3. 如果服务器内开启了 `ufw`，也要放行相应端口

---

## 7. 模型/Provider 配置

### 通过 Web UI 配置（推荐小白）

1. 浏览器打开 `http://<服务器IP>:18789`
2. 进入 **模型设置**
3. 选择模型提供商：腾讯混元 / DeepSeek / 通义千问 / OpenAI 等
4. 输入 API Key → 保存 → 重启服务

### 国内推荐模型

| 提供商 | 特点 | 获取方式 |
|--------|------|---------|
| 🎯 **腾讯混元** | 腾讯云原生，延迟最低 | 腾讯云控制台申请 |
| 🚀 **DeepSeek** | 性价比极高 | deepseek.com |
| 🌟 **通义千问 (Qwen)** | 阿里云，免费额度多 | dashscope.aliyun.com |
| 💎 **GLM (智谱)** | 中文理解强 | open.bigmodel.cn |
| 📦 **Token Plan 套餐** | 集合主流模型 | 腾讯云大模型套餐，比按量便宜50-80% |

---

## 8. 消息渠道接入

### 支持的渠道

| 渠道 | 配置难度 | 说明 |
|------|---------|------|
| 💬 **微信** | ⭐⭐⭐ 中等 | 扫码接入，需公众号 |
| 💬 **QQ** | ⭐⭐ 中等 | 机器人 Token |
| 💼 **企业微信** | ⭐⭐ 中等 | App ID + Secret + 回调 |
| 📋 **飞书** | ⭐⭐ 中等 | 自建应用，App ID + Secret |
| 🔔 **钉钉** | ⭐⭐ 中等 | Bot Webhook |
| 🌍 **Discord** | ⭐ 简单 | Bot Token 即可 |
| ✈️ **Telegram** | ⭐ 简单 | Bot Token 即可 |

### 飞书配置示例

```
1. 飞书开放平台 → 创建企业自建应用
2. 获取 App ID + App Secret
3. 配置 .env 文件
4. 设置回调URL：http://<服务器IP>:8080/api/feishu/callback
5. 放行 TCP 8080 端口
6. 飞书后台 → 事件订阅 → 填入回调地址
```

### 微信配置

腾讯云最近为 OpenClaw Lighthouse 模板推出了**一键微信绑定**功能：
- 控制台 → 一键扫码接入微信

---

## 9. 安全配置

### Nginx 反向代理 + SSL（强烈推荐）

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 安全清单

- [ ] 使用 SSH 密钥登录（禁用密码登录）
- [ ] 设置强管理员密码（12位+含特殊字符）
- [ ] 启用自动生成的 Gateway Token
- [ ] 防火墙仅开放必要端口
- [ ] 配置自动快照备份
- [ ] 考虑使用 Tailscale 管理访问

---

## 10. 验证与测试

```bash
# 检查服务状态
openclaw gateway status

# 打开 Web 控制面板
openclaw dashboard  # 或 http://<IP>:18789

# CLI 测试对话
openclaw chat

# 查看 Docker 容器（如使用 Docker）
docker ps

# 查看日志
docker logs <容器ID>            # Docker 方式
journalctl -u openclaw-gateway  # systemd 方式
```

---

## 11. 常见问题

| 问题 | 解决方案 |
|------|---------|
| ❌ **Docker 拉取超时** | 配置腾讯云内网 Docker 镜像加速 |
| ❌ **无法访问 Web UI** | 90% 是防火墙问题，检查腾讯云防火墙 + ufw |
| ❌ **内存不足 (OOM)** | 2GB 不够用，升级到 4GB+ 或配置 Swap |
| ❌ **端口访问失败** | 重新检查防火墙规则是否生效 |
| ❌ **API Key 泄露风险** | 使用环境变量而非硬编码，定期更换 |
| ❌ **重启后服务停止** | 确保 daemon 已安装：`openclaw onboard --install-daemon` |

---

## 附录：三种部署方式对比

| 对比项 | 🏆 一键模板 | Docker 部署 | npm 安装 |
|--------|-----------|------------|---------|
| 难易度 | ⭐ 最简单 | ⭐⭐ 中等 | ⭐⭐⭐ 需经验 |
| 时间 | 1-2分钟 | 10-15分钟 | 5-10分钟 |
| 灵活性 | 低（固定模板） | 中 | 高 |
| Node.js | 不需（预装） | 不需 | Node 22.16+ |
| 适用场景 | 小白首选 | 已有服务器 | 进阶用户 |

---

## 参考资料

- 📖 OpenClaw 官方文档：https://docs.openclaw.ai
- 📺 B站视频教程：[BV1mrXBBWE2S](https://www.bilibili.com/video/BV1mrXBBWE2S/)
- 💻 GitHub：https://github.com/openclaw/openclaw
- ☁️ 腾讯云 OpenClaw 活动页：https://cloud.tencent.com/act/pro/openclaw
