# Meng Luo · Academic Homepage

正式主页：[eurekaleo.github.io](https://eurekaleo.github.io/)

## 直接在 GitHub 网页更新内容

1. 打开 [homepage/content.json 的编辑页](https://github.com/Eurekaleo/Eurekaleo.github.io/edit/main/homepage/content.json)。
2. 修改文字，或复制一条同类记录来新增内容。
3. 点击 **Commit changes…**，提交到 **main**。
4. 在 [Actions → Publish Homepage](https://github.com/Eurekaleo/Eurekaleo.github.io/actions/workflows/publish-homepage.yml) 查看进度。出现绿色勾号后刷新主页。

不需要下载仓库、安装 Python、运行命令或手动生成 HTML。GitHub 自动运行生成脚本并部署页面。日常内容统一在 `homepage/content.json` 中维护，详细字段说明和新增示例见 [内容编辑指南](homepage/EDITING.md)。

如果填写的 JSON 格式有误、条目 ID 重复或图片不存在，构建会失败，线上保留上一次成功发布的版本；修正后重新提交即可。

不要直接编辑生成的根目录 `index.html`。GitHub 发布时会重新生成它，仓库中的这个文件仅保留为静态快照。原站的 `_pages/about.md`、`_config.yml` 和之前的设计预览目录不再是正式版的内容入口。

## 可选：本地开发

在仓库根目录使用 Python 3.12 或以上版本：

```sh
python3 homepage/build.py
python3 -m http.server 8765 --bind 127.0.0.1
```

打开 `http://127.0.0.1:8765/` 预览。

- 内容：`homepage/content.json`
- HTML 生成脚本：`homepage/build.py`
- 外观：`homepage/styles.css`
- 交互：`homepage/app.js`
- 图片、机构标志、字体：`homepage/assets/`
- 自动发布：`.github/workflows/publish-homepage.yml`

CSS 和 JavaScript 地址在构建时带有内容哈希，避免更新后的浏览器缓存问题。字体和图片由本站提供。

## 发布与版本管理

GitHub Pages 的发布来源是 **GitHub Actions**。`main` 的每次提交都会触发 **Publish Homepage**：先生成、校验，再上传和部署。也可以在该工作流页面点击 **Run workflow**，选择 `main` 手动重试。自动化只部署生成结果，不向仓库追加机器人提交。

主页地址保持 `https://eurekaleo.github.io/`；`/about/` 和 `/about.html` 跳转到主页。原站的新闻、论文、活动和荣誉锚点继续有效。

保留的版本：

- 原始主页：`homepage-before-v5.1-2026-09-29`
- 确认上线的 V5.1：`homepage-v5.1-2026-09-29`
- 增加网页编辑自动发布之前：`homepage-before-web-editing-2026-09-29`

普通内容修改可以恢复 `content.json` 的历史内容并重新提交，自动发布流程会照常运行。也可以 revert 对应的内容提交。

如果要完整恢复上述旧标签，需要一并恢复对应文件，并在仓库 **Settings → Pages → Build and deployment** 将 Source 改回 **Deploy from a branch**，选择 **main / (root)**。旧版本使用分支发布；仅恢复旧文件而不恢复 Pages 设置不足以完成回退。不需要强制推送或删除历史。

## Credits

The approved V5.1 visual design is unchanged. The publication presentation and heading typography follow [Jiwen Yu's homepage](https://yujiwen.github.io/). Research images and profile content come from this repository. Inter and Orbitron licenses are included in `homepage/assets/fonts/`; the GitHub icon license is included in `homepage/assets/logos/`.

The original site was based on [AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io). Its source and license remain in the repository.
