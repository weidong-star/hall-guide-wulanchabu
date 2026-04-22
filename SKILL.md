---
name: hall-guide-generator
description: 自动生成政务服务大厅导览系统的静态H5页面和数据配置文件；当用户需要搭建大厅信息展示、窗口导览、二维码扫码导览系统时使用
---

# 政务服务大厅导览系统生成器

## 任务目标
- 本 Skill 用于：生成完整的政务服务大厅导览系统，包括H5页面、数据配置文件和部署方案
- 能力包含：生成页面模板、数据结构模板、二维码URL列表、部署指导
- 触发条件：用户需要搭建基于二维码的政务服务大厅信息展示系统

## 前置准备
- 无需安装依赖（使用纯Python标准库）
- 准备各大厅的实际信息：大厅名称、地址、入驻单位数、窗口信息、事项清单、语音介绍文本
- 准备部署平台账号（GitHub/Vercel/Netlify任选其一）

## 操作步骤

### 标准流程

#### 1. 生成数据结构模板
生成标准化的JSON数据配置文件模板，用于填写各大厅的实际信息。

**脚本调用示例：**
```bash
python scripts/generate-data-structure.py --hall-count 12
```

**参数说明：**
- `--hall-count`: 大厅数量（默认12）

**输出：**
- `hall-data-template.json` - 数据结构模板文件

#### 2. 生成H5页面模板
生成响应式的H5导览页面模板，支持数据加载、语音播报、事项展示等功能。

**脚本调用示例：**
```bash
python scripts/generate-hall-html.py --domain https://your-domain.com
```

**参数说明：**
- `--domain`: 部署域名（用于生成二维码URL，默认 https://example.com）

**输出：**
- `hall.html` - H5页面文件
- `style.css` - 样式文件
- `app.js` - 交互脚本文件

#### 3. 生成二维码URL列表
生成所有大厅对应的二维码内容列表，用于生成二维码贴纸。

**脚本调用示例：**
```bash
python scripts/generate-qr-urls.py --domain https://your-domain.com --hall-count 12
```

**参数说明：**
- `--domain`: 部署域名
- `--hall-count`: 大厅数量

**输出：**
- `qr-urls.txt` - 二维码URL列表文件

#### 4. 填写实际数据
根据生成的数据模板，填写各大厅的实际信息。

**操作步骤：**
1. 打开 `hall-data-template.json`
2. 按照 [数据格式说明](references/data-format.md) 填写各字段
3. 将填写后的JSON文件重命名为 `data/hall_{id}.json`（如 `data/hall_001.json`）
4. 为每个大厅创建独立的JSON文件

**注意事项：**
- `hallId` 必须与二维码URL中的ID保持一致
- `voiceText` 字段建议控制在100-200字，播报效果更佳
- 图片路径使用相对路径，如 `images/hall_001.jpg`

#### 5. 部署上线
选择静态托管平台进行部署，零成本、零维护。

**GitHub Pages 部署：**
1. 创建GitHub仓库
2. 上传所有生成的文件（HTML、CSS、JS、data/）
3. 进入仓库 Settings → Pages → Source 选择 main 分支
4. 访问 `https://username.github.io/repo-name/hall.html?id=001`

**Vercel 部署（推荐）：**
1. 登录 [vercel.com](https://vercel.com)
2. 点击 "New Project" → 连接GitHub仓库或上传文件
3. 自动部署完成，获得访问域名
4. 使用生成的域名替换脚本中的 `--domain` 参数

### 可选分支

#### 当需要多语言支持时
1. 在数据模板中添加 `lang` 字段（zh-CN / mn）
2. 在页面顶部添加语言切换按钮
3. 根据语言切换加载不同的JSON文件

#### 当需要地图导航时
1. 在数据模板中添加 `latitude` 和 `longitude` 字段
2. 集成高德地图API或百度地图API
3. 在页面中嵌入地图组件

## 使用示例

### 示例1：快速搭建12个大厅的导览系统
- **场景/输入**：用户有12个政务服务大厅需要导览系统
- **预期产出**：完整的H5页面、12个数据JSON文件、二维码URL列表
- **关键要点**：
  - 先生成模板，再批量填写数据
  - 每个大厅使用独立的hallId（001-012）
  - 二维码URL格式为 `域名/hall.html?id=001`

### 示例2：更新大厅信息
- **场景/输入**：某个大厅的窗口信息发生变化
- **预期产出**：只需修改对应的JSON文件并重新部署
- **关键要点**：
  - 直接编辑 `data/hall_005.json` 文件
  - 提交到Git仓库自动触发重新部署
  - 无需修改H5页面代码

## 资源索引

### 脚本
- [scripts/generate-data-structure.py](scripts/generate-data-structure.py) - 生成JSON数据结构模板，接受大厅数量参数
- [scripts/generate-hall-html.py](scripts/generate-hall-html.py) - 生成H5页面模板及相关资源文件（HTML/CSS/JS），接受域名参数
- [scripts/generate-qr-urls.py](scripts/generate-qr-urls.py) - 生成二维码URL列表，用于生成二维码贴纸

### 参考
- [references/data-format.md](references/data-format.md) - 数据格式详细说明，包含字段定义、示例和验证规则

### 资产
- [assets/hall-template.html](assets/hall-template.html) - H5页面基础模板（供脚本参考）
- [assets/hall-data-template.json](assets/hall-data-template.json) - JSON数据示例（供脚本参考）

## 注意事项

- 所有数据通过JSON静态文件存储，无需数据库
- 语音播报使用浏览器原生 Web Speech API，无需第三方服务
- 修改数据后需重新部署静态文件才能生效
- 建议为每个大厅准备一张实景照片，提升用户体验
- 二维码建议使用草料二维码或联图二维码等在线工具生成
- 确保大厅ID在所有文件中保持一致
