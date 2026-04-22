# 音频文件存放说明

## 目录结构

```
audio/
├── ttsmaker-file-2026-4-22-16-25-46.mp3  # 大厅介绍音频
└── items/
    ├── item_001.mp3  # 事项音频
    ├── item_002.mp3
    └── ...
```

## 如何添加音频

### 1. 大厅介绍音频
将音频文件放在 `audio/` 目录下，然后在JSON中配置：
```json
{
  "voiceAudio": "/audio/ttsmaker-file-2026-4-22-16-25-46.mp3"
}
```

### 2. 事项音频
将音频文件放在 `audio/items/` 目录下，然后在事项的JSON中配置：
```json
{
  "items": [
    {
      "id": "item_001",
      "name": "事项名称",
      "audio": "/audio/items/item_001.mp3"
    }
  ]
}
```

## 注意事项

1. 音频路径必须是相对路径（以 `/` 开头）
2. 不要使用本地绝对路径（如 `C:\Users\...`）
3. 支持的音频格式：mp3, wav, ogg
4. 音频文件命名建议与事项ID对应
