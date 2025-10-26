# FastAPI UV App

一个使用 uv 管理本地开发环境的 FastAPI 应用，配套轻量级 Docker 镜像与 GitHub Actions CI/CD 工作流。

## 本地开发（使用 uv）

前置条件：安装 uv（建议通过 pipx）

- 安装 uv：`pipx install uv` 或参考官方文档 https://github.com/astral-sh/uv

初始化与开发：

- 在项目根目录 `fastapi-uv-app/` 执行：
  - 创建虚拟环境：`uv venv`
  - 安装依赖（包含运行时与开发依赖）：`uv sync --all-extras`
  - 运行应用：`uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`

接口说明：

- `GET /health`：健康检查，返回 `{"status": "ok"}`，HTTP 200
- `GET /hello?name=Alice`：问候，默认 `World`；返回 `{"message": "Hello, Alice!"}`
- `GET /items/{item_id}`：按路径参数返回项目信息

运行测试：

- `uv run pytest -q`

## 依赖管理

- 提供两种清单（任选其一即可满足要求）：
  - `pyproject.toml`：适用于 uv 管理（主清单，包含可选 dev 依赖）
  - `requirements.txt`：适用于 Docker/CI（固定版本）

主要依赖（已固定版本）：

- `fastapi==0.115.0`
- `uvicorn[standard]==0.30.1`
- `httpx==0.27.0`（测试）
- `pytest==8.3.3`（测试）

## Docker 镜像

- 使用多阶段构建，基础镜像：`python:3.12-slim`
- 在构建阶段创建独立 venv 并安装依赖；最终镜像复制 venv 与应用代码
- 以非 root 用户运行（`appuser`）
- 配置健康检查：`curl -fsS http://localhost:8000/health`
- 启动命令：`uvicorn app.main:app --host 0.0.0.0 --port 8000`

本地构建与运行：

- 构建：`docker build -t yourhub/fastapi-uv-app:local .`
- 运行：`docker run -p 8000:8000 yourhub/fastapi-uv-app:local`

## CI/CD（GitHub Actions）

工作流文件：`.github/workflows/ci-cd.yml`

功能概览：

- 在 push 或 PR 时自动运行测试（pytest）
- 仅在 push 到 `main` 分支时执行构建与推送 Docker 镜像
- 使用 GitHub Secrets 管理 Docker Hub 凭据：`DOCKER_HUB_USERNAME`、`DOCKER_HUB_ACCESS_TOKEN`
- 镜像标签策略：`latest` 与 `commit SHA` 两种标签

使用说明：

1. 在 GitHub 仓库 Settings → Secrets and variables → Actions 中新增：
   - `DOCKER_HUB_USERNAME`: 你的 Docker Hub 用户名
   - `DOCKER_HUB_ACCESS_TOKEN`: 你的 Docker Hub Access Token（建议使用 Token 而非密码）
2. 如需自定义仓库名，修改工作流中的 `env.IMAGE_NAME`，例如：`my-fastapi`
3. 推送代码后：
   - 任意分支：会触发测试
   - `main` 分支：在测试通过后，构建并推送镜像到 `docker.io/<DOCKER_HUB_USERNAME>/<IMAGE_NAME>:latest` 和 `:<commit_sha>`

## 重现性与维护性

- 版本固定，确保构建稳定可重现
- uv 管理虚拟环境与依赖，快速、可控
- 轻量级 Docker 镜像、非 root 运行增强安全性
- CI/CD 自动化测试与构建，保障合并质量并自动发布