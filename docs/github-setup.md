# GitHub 同步配置说明

当前项目可以作为 Git 仓库同步到 GitHub。你需要先在 GitHub 上创建一个空仓库，然后把仓库地址填入下面命令。

## HTTPS 方式

```powershell
git remote add origin https://github.com/Zxyxuegao/rk1126b-assistant.git
git branch -M main
git push -u origin main
```

## SSH 方式

```powershell
git remote add origin git@github.com:Zxyxuegao/rk1126b-assistant.git
git branch -M main
git push -u origin main
```

## 常用检查命令

```powershell
git remote -v
git status
git log --oneline
```

## 初次提交建议

```powershell
git add README.md .gitignore docs/
git commit -m "docs: add initial project proposal"
```

如果后续需要提交模型权重、数据集或演示视频，建议使用 GitHub Release、网盘链接或 Git LFS，而不是直接提交到普通 Git 历史中。
