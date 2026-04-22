// 全局变量
let allItems = []; // 存储所有事项
let filteredItems = []; // 存储筛选后的事项
let currentAudio = null; // 当前播放的音频
let isAudioPlaying = false; // 音频播放状态

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
                    ${window.floor ? `<span class="window-floor">${window.floor}</span>` : ''}
                </div>
                <div class="window-desc">${window.desc}</div>
            </div>
        `).join('');
    }

    // 保存语音文本用于播报
    document.getElementById('voiceBtn').dataset.voiceText = data.voiceText || '';
    
    // 渲染事项
    if (data.items && data.items.length > 0) {
        allItems = data.items;
        filteredItems = data.items;
        renderUnitFilter(data.items);
        renderItems(filteredItems);
    } else {
        document.getElementById('itemsList').innerHTML = '<p style="text-align:center;color:#999;padding:40px 0;">暂无事项数据</p>';
    }
}

// 语音播报
let isPlaying = false;
let currentUtterance = null;

function playVoice(text) {
    if (!text) {
        alert('暂无语音介绍');
        return;
    }

    if (isPlaying) {
        // 停止播放
        speechSynthesis.cancel();
        isPlaying = false;
        currentUtterance = null;
        document.getElementById('voiceBtn').classList.remove('playing');
        return;
    }

    // 先清空队列，避免多次点击累积
    speechSynthesis.cancel();
    
    currentUtterance = new SpeechSynthesisUtterance(text);
    currentUtterance.lang = 'zh-CN';
    currentUtterance.rate = 1.0;

    currentUtterance.onend = () => {
        isPlaying = false;
        currentUtterance = null;
        document.getElementById('voiceBtn').classList.remove('playing');
    };

    currentUtterance.onerror = () => {
        isPlaying = false;
        currentUtterance = null;
        document.getElementById('voiceBtn').classList.remove('playing');
    };

    speechSynthesis.speak(currentUtterance);
    isPlaying = true;
    document.getElementById('voiceBtn').classList.add('playing');
}

// 渲染单位筛选下拉框
function renderUnitFilter(items) {
    const units = [...new Set(items.map(item => item.unit))];
    const select = document.getElementById('unitFilter');
    select.innerHTML = '<option value="">全部单位</option>' + 
        units.map(unit => `<option value="${unit}">${unit}</option>`).join('');
}

// 渲染事项列表
function renderItems(items) {
    const itemsList = document.getElementById('itemsList');
    
    if (items.length === 0) {
        itemsList.innerHTML = '<p style="text-align:center;color:#999;padding:40px 0;">没有找到匹配的事项</p>';
        return;
    }
    
    itemsList.innerHTML = items.map(item => `
        <div class="item-card" onclick="showItemDetail('${item.id}')">
            <div class="item-name">${item.name}</div>
            <span class="item-unit">${item.unit}</span>
            <div class="item-brief">${item.description || '点击查看详细信息'}</div>
        </div>
    `).join('');
}

// 搜索事项
function searchItems() {
    const keyword = document.getElementById('itemSearch').value.trim().toLowerCase();
    const unitFilter = document.getElementById('unitFilter').value;
    
    filteredItems = allItems.filter(item => {
        const matchKeyword = !keyword || 
            item.name.toLowerCase().includes(keyword) || 
            item.unit.toLowerCase().includes(keyword);
        const matchUnit = !unitFilter || item.unit === unitFilter;
        return matchKeyword && matchUnit;
    });
    
    renderItems(filteredItems);
}

// 筛选事项
function filterItems() {
    const keyword = document.getElementById('itemSearch').value.trim().toLowerCase();
    const unitFilter = document.getElementById('unitFilter').value;
    
    filteredItems = allItems.filter(item => {
        const matchKeyword = !keyword || 
            item.name.toLowerCase().includes(keyword) || 
            item.unit.toLowerCase().includes(keyword);
        const matchUnit = !unitFilter || item.unit === unitFilter;
        return matchKeyword && matchUnit;
    });
    
    renderItems(filteredItems);
}

// 显示事项详情
function showItemDetail(itemId) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;
    
    document.getElementById('modalTitle').textContent = item.name;
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <div class="detail-section">
            <div class="detail-label">🏢 所属单位</div>
            <div class="detail-value">${item.unit}</div>
        </div>
        
        <div class="detail-section">
            <div class="detail-label">📜 办理依据</div>
            <div class="detail-value">${item.basis || '-'}</div>
        </div>
        
        <div class="detail-section">
            <div class="detail-label">🪟 办理窗口</div>
            <div class="detail-value">${item.window || '-'}</div>
        </div>
        
        <div class="detail-section">
            <div class="detail-label">⏱️ 办理时限</div>
            <div class="detail-value">${item.timeLimit || '-'}</div>
        </div>
        
        <div class="detail-section">
            <div class="detail-label">💰 办理费用</div>
            <div class="detail-value">${item.fee || '-'}</div>
        </div>
        
        <div class="detail-section">
            <div class="detail-label">📝 办理流程</div>
            <div class="detail-value">${item.process || '-'}</div>
        </div>
        
        <div class="detail-section">
            <div class="detail-label">📄 所需材料</div>
            <div class="detail-value">
                <ul class="materials-list">
                    ${item.materials && item.materials.length > 0 ? 
                        item.materials.map(m => `<li>${m}</li>`).join('') : 
                        '<li>暂无材料要求</li>'}
                </ul>
            </div>
        </div>
        
        ${item.description ? `
        <div class="detail-section">
            <div class="detail-label">ℹ️ 事项说明</div>
            <div class="detail-value">${item.description}</div>
        </div>
        ` : ''}
        
        ${item.audio ? `
        <div class="audio-player">
            <button class="audio-btn" id="audioPlayBtn" onclick="toggleItemAudio('${item.audio}')">
                <span>⏸️</span> 暂停播放
            </button>
            <span class="audio-status" id="audioStatus">正在播放...</span>
        </div>
        ` : ''}
    `;
    
    document.getElementById('itemModal').style.display = 'block';
    
    // 如果有音频，自动播放
    if (item.audio) {
        playItemAudio(item.audio);
    }
}

// 播放事项音频
function playItemAudio(audioUrl) {
    const btn = document.getElementById('audioPlayBtn');
    const status = document.getElementById('audioStatus');
    
    // 开始或继续播放
    if (!currentAudio) {
        currentAudio = new Audio(audioUrl);
        
        currentAudio.onended = () => {
            isAudioPlaying = false;
            btn.innerHTML = '<span>🔊</span> 重新播放';
            btn.classList.remove('playing');
            status.textContent = '播放完成';
            currentAudio = null;
        };
        
        currentAudio.onerror = () => {
            isAudioPlaying = false;
            btn.innerHTML = '<span>🔊</span> 播放语音介绍';
            btn.classList.remove('playing');
            status.textContent = '音频加载失败';
            currentAudio = null;
        };
    }
    
    currentAudio.play();
    isAudioPlaying = true;
    btn.innerHTML = '<span>⏸️</span> 暂停';
    btn.classList.add('playing');
    status.textContent = '正在播放...';
}

// 切换播放/暂停
function toggleItemAudio(audioUrl) {
    const btn = document.getElementById('audioPlayBtn');
    const status = document.getElementById('audioStatus');
    
    if (isAudioPlaying) {
        // 暂停播放
        if (currentAudio) {
            currentAudio.pause();
            isAudioPlaying = false;
            btn.innerHTML = '<span>▶️</span> 继续播放';
            btn.classList.remove('playing');
            status.textContent = '已暂停';
        }
    } else {
        // 继续播放
        if (currentAudio) {
            currentAudio.play();
            isAudioPlaying = true;
            btn.innerHTML = '<span>⏸️</span> 暂停';
            btn.classList.add('playing');
            status.textContent = '正在播放...';
        } else {
            // 重新播放
            playItemAudio(audioUrl);
        }
    }
}

// 关闭弹窗
function closeModal() {
    document.getElementById('itemModal').style.display = 'none';
    // 停止音频播放
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }
    isAudioPlaying = false;
}

// 点击弹窗外部关闭
document.addEventListener('click', (e) => {
    const modal = document.getElementById('itemModal');
    if (e.target === modal) {
        closeModal();
    }
});

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
    
    // 搜索框回车键支持
    const searchInput = document.getElementById('itemSearch');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchItems();
            }
        });
    }
});