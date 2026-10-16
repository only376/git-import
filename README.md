# git-import

代码导入与整理仓库。

## 用途

用于存放从各处收集、导入的代码与练习文件。

## 使用环境

- C / C++：MinGW-w64（`g++` / `gcc`）
- Python：3.x
- 编辑器：VS Code

## 日常提交

```bash
git add .
git commit -m "说明这次改了什么"
git push
```

## 说明

本仓库通过 `.gitignore` 排除了编译产物（`.exe`、`.o`、`__pycache__`、`venv` 等），
只提交源代码。
