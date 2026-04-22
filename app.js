// 获取大厅ID → 改成获取 regionid
function getHallId() {
    const params = new URLSearchParams(window.location.search);
    // 优先用 regionid，没有就用 001
    return params.get('regionid') || '001';
}

// 加载大厅数据
async function loadHallData(hallId) {
    try {
        const response = await fetch(`data/hall_${hallId}.json`);
        if (!response.ok) {
            throw new Error('数据加载失败');
        }
        const data = await response.json();
        renderHall(data);
        return data;
    } catch (error) {
        console.error('加载失败:', error);
        document.getElementById('hallName').textContent = '数据加载失败，请稍后重试';
        return null;
    }
}

// 渲染大厅信息
function renderHall(data) {
    // 基本信息
    document.getElementById('hallName').textContent = data.hallName;
    document.getElementById('address').textContent = data.address || '-';
    document.getElementById('phone').textContent = data.contact || '-'; // 改成 contact
    document.getElementById('workTime').textContent = data.workTime || '-';
    document.getElementById('units').textContent = data.units ? `${data.units}家` : '-';

    // 大厅图片
    if (data.image) {
        document.getElementById('hallImage').src = data.image;
    }

    // 温馨提示
    if (data.notice) {
        document.getElementById('notice').style.display = 'block';
        document.getElementById('noticeText').textContent = data.notice;
    }

    // 渲染窗口列表
    if (data.windows && data.windows.length > 0) {
        const windowsList = document.getElementById('windowsList');
        windowsList.innerHTML = data.windows.map(window => `
            <div class="window-card">
                <div class="window-header">
                    <span class="window-name">${window.no}</span>
                </div>
                <div class="window-desc">${window.desc}</div>
            </div>
        `).join('');
    }

    // 保存语音文本用于播报
    document.getElementById('voiceBtn').dataset.voiceText = data.voiceText || '';
}

// 语音播报
let isPlaying = false;
function playVoice(text) {
    if (!text) {
        alert('暂无语音介绍');
        return;
    }

    if (isPlaying) {
        speechSynthesis.cancel();
        isPlaying = false;
        document.getElementById('voiceBtn').classList.remove('playing');
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    utterance.rate = 1.0;

    utterance.onend = () => {
        isPlaying = false;
        document.getElementById('voiceBtn').classList.remove('playing');
    };

    utterance.onerror = () => {
        isPlaying = false;
        document.getElementById('voiceBtn').classList.remove('playing');
        alert('语音播放失败');
    };

    speechSynthesis.speak(utterance);
    isPlaying = true;
    document.getElementById('voiceBtn').classList.add('playing');
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    const hallId = getHallId();
    loadHallData(hallId).then(data => {
        if (data && data.voiceText) {
            document.getElementById('voiceBtn').addEventListener('click', () => {
                playVoice(data.voiceText);
            });
        } else {
            document.getElementById('voiceBtn').style.display = 'none';
        }
    });
});