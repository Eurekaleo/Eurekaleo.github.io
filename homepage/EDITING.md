# 主页内容编辑指南

[点击这里直接编辑 content.json](https://github.com/Eurekaleo/Eurekaleo.github.io/edit/main/homepage/content.json)。修改后点击 **Commit changes…**，提交到 `main`，GitHub 就会自动生成并发布主页。

不需要修改 Python、HTML、CSS，也不需要在电脑上运行命令。[查看自动发布进度](https://github.com/Eurekaleo/Eurekaleo.github.io/actions/workflows/publish-homepage.yml)。

## 修改现有文字

在编辑页搜索页面上的原文字，修改对应引号内的内容即可。现在已经移除了旧版中重复且不参与显示的记录。

| 内容 | content.json 中的位置 |
|---|---|
| 姓名、身份、学校、邮箱、头像、联系链接 | `profile` |
| 简介、教育背景 | `intro.paragraphs_html`，每一项是一段 |
| 研究方向 | `intro.research_prefix`、`intro.research_statement` |
| 邮件邀请句 | `intro.contact_prefix`、`intro.contact_suffix`；邮箱统一读取 `profile.email` |
| 导航、栏目标题 | `labels` |
| News | `news` |
| 论文 | `publications` |
| 实习和组织经历 | `professional_experience` |
| 审稿及其他学术服务 | `academic_service`，每一项是一条 |
| 荣誉和奖项 | `honors` |
| 页脚 | `footer` |
| 浏览器标题、搜索描述、分享信息 | `site` |

`intro.paragraphs_html` 和 `authors_html` 支持已有的 HTML 格式，例如 `<strong>加粗文字</strong>` 和链接。修改文字时保留周围的标签即可。其他标题、日期等字段直接写普通文字，不要加 HTML 标签。

侧栏的 Email 项没有单独的 URL，会自动使用 `profile.email`；修改这个邮箱会同时更新正文邮箱和侧栏邮箱入口。`profile.contacts` 的图标可使用 `mail`、`github`、`scholar` 或 `external`。

## 新增 News

在 `news` 数组最前面加入一条。新条目的 `id` 必须与已有条目不同；不需要修改旧条目的编号。

```json
{
  "id": "news-2026-10-example",
  "date": "2026.10",
  "headline": "这里填写动态标题",
  "title": "这里填写论文名称或补充说明",
  "url": null
}
```

有链接时，把 `null` 改成带引号的完整网址。条目之间需要英文逗号，最后一条后面不加逗号。网站按照数组顺序显示，不会自动排序。

`news_archive.before_year` 当前为 `2026`：2026 年及以后直接显示，较早新闻放在折叠区。`news_archive.label` 中的 `{count}` 自动替换成折叠条目数。

## 新增论文

复制 `publications` 中的一条记录，修改以下字段，并移到想显示的位置：

- `id`：唯一编号，例如 `paper-new-2026`。
- `title`：论文标题。
- `authors_html`：作者列表；用 `<strong>Meng Luo</strong>` 保留自己的强调样式。
- `venue`、`year`：会议或期刊名称、年份。
- `recognitions`：例如 `["Oral"]`、`["Best Paper Award"]`；没有则用 `[]`。
- `image`：图片路径，例如 `assets/images/new-paper.png`。
- `links`：实际要显示的入口，例如 `[{"label": "Paper", "url": "https://arxiv.org/abs/..."}]`；没有则用 `[]`。

图片先通过 GitHub 的 **Add file → Upload files** 上传到 `homepage/assets/images/`；PNG、JPG 和 WebP 都可以，不需要转换格式。`image` 的路径相对于 `homepage/`，不要再写一次 `homepage/` 前缀。

`image_dimensions` 可填写图片实际宽高，也可以整项删除，不要沿用其他图片的错误尺寸。`badge_venue` 用于图片上的短会议名；没有特殊需要可以删除，让它与 `venue` 相同。

News 与论文列表独立维护，新增其中一处不会自动生成另一处。

## 新增经历、服务或奖项

- 经历：复制 `professional_experience` 中的一项，修改 `id`、`organization`、`role`、`date_label`、`url`、`location` 等。机构标志放在 `homepage/assets/logos/`，`logo` 填 `assets/logos/文件名.png`。`program` 和 `description_html` 是可选项。
- 学术服务：在 `academic_service` 数组中添加一个带引号的文本项。
- 奖项：在 `honors.groups` 对应分组的 `items` 中添加 `{"year": 2026, "description": "奖项名称"}`。本科阶段的说明可修改 `honors.period`。

## 常见问题

- **引号与逗号**：使用英文双引号 `"` 和英文逗号 `,`。字符串内部的双引号需要写成 `\"`。JSON 不支持注释和尾随逗号。
- **修改后还没更新**：查看 **Actions → Publish Homepage**。显示绿色勾号后刷新主页；必要时强制刷新浏览器。
- **红色叉号**：打开失败的运行，查看 **Generate and validate the homepage**。JSON 语法错误会显示行号；重复 ID 或缺失图片也会提示。失败不会替换上一份已成功部署的页面。
- **不要编辑 `index.html`**：它由自动构建生成，手工修改会在发布时被覆盖。旧的 `_pages/about.md` 不再控制正式主页。

每次 GitHub 提交都会留下历史记录；可以从文件的 **History** 找到修改前的内容并恢复。
