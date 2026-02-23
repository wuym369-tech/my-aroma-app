import streamlit as st
import streamlit.components.v1 as components
from datetime import date
from collections import Counter
import time
import random
import math

# ── 開發者模式後門 ─────────────────────────────────
# 改成 True → Step 3 顯示「快速測試」按鈕（自動選第一個選項）
# 上線前改回 False 即可隱藏
DEV_MODE = False
# ──────────────────────────────────────────────────

# 1. 页面配置 (必须放在最顶端)
st.set_page_config(page_title="Aroma's Secret Lab", layout="centered")

# 自定义 CSS 样式 - 高级奢华风
st.markdown("""
<style>
/* ===== 高级奢华背景 ===== */
body, .stApp {
    background: linear-gradient(135deg, #faf8ff 0%, #f3f0ff 25%, #ede7f6 50%, #f5f0ff 75%, #ffffff 100%) !important;
    background-color: #ffffff !important;
    font-family: 'Noto Serif TC', 'Songti TC', serif !important;
}

/* ===== 高级标题 ===== */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Noto Serif TC', 'Songti TC', serif !important;
    font-weight: 600 !important;
    color: #1a1a2e !important;
    letter-spacing: 1px !important;
}

h1 { font-size: 2rem !important; }
h2 { font-size: 1.6rem !important; }
h3 { font-size: 1.3rem !important; }

/* ===== 奢华按钮 ===== */
div.stButton > button, .stButton > button {
    background: linear-gradient(135deg, #ffffff 0%, #faf8ff 50%, #ffffff 100%) !important;
    color: #1a1a2e !important;
    border: 1px solid rgba(196, 164, 132, 0.4) !important;
    border-radius: 20px !important;
    padding: 18px 36px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    box-shadow: 
        0 4px 30px rgba(196, 164, 132, 0.15) !important,
        0 1px 0 1px rgba(255,255,255,0.8) inset !important,
        0 -1px 0 1px rgba(0,0,0,0.05) inset !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    position: relative;
    overflow: hidden;
}

div.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
    transition: left 0.5s ease !important;
}

div.stButton > button:hover::before {
    left: 100%;
}

div.stButton > button:hover, .stButton > button:hover {
    background: linear-gradient(135deg, #faf8ff 0%, #fff 50%, #f5f0ff 100%) !important;
    transform: translateY(-4px) !important;
    box-shadow: 
        0 15px 50px rgba(196, 164, 132, 0.25) !important,
        0 1px 0 1px rgba(255,255,255,0.9) inset !important,
        0 -1px 0 1px rgba(0,0,0,0.03) inset !important;
    border-color: rgba(196, 164, 132, 0.6) !important;
}

div.stButton > button:active {
    transform: translateY(-1px) !important;
    box-shadow: 
        0 6px 25px rgba(196, 164, 132, 0.2) !important;
}

/* ===== 奢华卡片 ===== */
div[data-testid="stMetric"], div[data-testid="stInfo"], div[data-testid="stSuccess"], div[data-testid="stWarning"], 
div[data-testid="stError"], div.stMetric, .stAlert {
    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(250,248,245,0.85) 100%) !important;
    backdrop-filter: blur(25px) !important;
    -webkit-backdrop-filter: blur(25px) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(196, 164, 132, 0.2) !important;
    box-shadow: 
        0 10px 40px rgba(0,0,0,0.06) !important,
        0 1px 0 1px rgba(255,255,255,0.8) inset !important,
        0 -1px 0 1px rgba(0,0,0,0.02) inset !important;
}

/* ===== 高级单选按钮 ===== */
div[role="radiogroup"] > div {
    gap: 14px !important;
}

div[role="radiogroup"] label {
    border-radius: 18px !important;
    padding: 20px 28px !important;
    background: linear-gradient(135deg, rgba(255,255,255,0.85) 0%, rgba(250,248,245,0.8) 100%) !important;
    backdrop-filter: blur(30px) !important;
    -webkit-backdrop-filter: blur(30px) !important;
    margin: 10px 0 !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    border: 1px solid rgba(196, 164, 132, 0.25) !important;
    box-shadow: 
        0 4px 20px rgba(0,0,0,0.04) !important,
        0 1px 0 1px rgba(255,255,255,0.9) inset !important;
}

div[role="radiogroup"] label:hover {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 100%) !important;
    border-color: rgba(196, 164, 132, 0.5) !important;
    box-shadow: 
        0 12px 40px rgba(196, 164, 132, 0.18) !important,
        0 1px 0 1px rgba(255,255,255,0.95) inset !important;
    transform: translateY(-3px) !important;
}

div[role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(135deg, rgba(196, 164, 132, 0.15) 0%, rgba(212, 170, 125, 0.1) 100%) !important;
    border-color: rgba(196, 164, 132, 0.6) !important;
    box-shadow: 
        0 15px 50px rgba(196, 164, 132, 0.22) !important,
        inset 0 0 0 1px rgba(196, 164, 132, 0.1) !important;
}

/* ===== 高级输入框 ===== */
input[type="text"], .stTextInput input, input[type="number"], input[type="email"], input[type="password"] {
    border-radius: 16px !important;
    border: 1px solid rgba(196, 164, 132, 0.3) !important;
    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(250,248,245,0.85) 100%) !important;
    backdrop-filter: blur(15px) !important;
    padding: 16px 20px !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}

input[type="text"]:focus, .stTextInput input:focus, input[type="number"]:focus {
    border-color: rgba(196, 164, 132, 0.6) !important;
    box-shadow: 
        0 0 0 4px rgba(196, 164, 132, 0.12) !important,
        0 8px 30px rgba(196, 164, 132, 0.1) !important;
    background: rgba(255,255,255,0.98) !important;
}

/* ===== 高级选择框 ===== */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 16px !important;
    background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(250,248,245,0.85) 100%) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(196, 164, 132, 0.3) !important;
}

/* ===== 奢华进度条 ===== */
div[role="progressbar"] div {
    background: linear-gradient(90deg, #c4a484 0%, #d4aa7d 25%, #e8d5b7 50%, #d4aa7d 75%, #c4a484 100%) !important;
    border-radius: 12px !important;
    box-shadow: 
        0 2px 10px rgba(196, 164, 132, 0.4) !important,
        inset 0 1px 0 rgba(255,255,255,0.3) !important;
}

/* ===== 分隔线 ===== */
hr, .stDivider {
    border-color: rgba(196, 164, 132, 0.2) !important;
}

/* ===== 表格美化 ===== */
.stDataFrame {
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* ===== 滑块美化 ===== */
div.stSlider [data-baseweb="slider"] {
    background: rgba(196, 164, 132, 0.2) !important;
    border-radius: 6px !important;
}

div.stSlider [data-baseweb="slider"] > div {
    background: linear-gradient(90deg, #c4a484 0%, #d4aa7d 100%) !important;
    border-radius: 6px !important;
}

/* ===== 折叠面板 ===== */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(250,248,245,0.75) 100%) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(196, 164, 132, 0.2) !important;
}

/* ===== 徽章美化 ===== */
span[data-testid="stBadge"] {
    border-radius: 12px !important;
    padding: 6px 14px !important;
}

/* ===== 滚动条美化 ===== */
::-webkit-scrollbar {
    width: 8px !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-track {
    background: rgba(196, 164, 132, 0.1) !important;
    border-radius: 4px !important;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #c4a484 0%, #d4aa7d 100%) !important;
    border-radius: 4px !important;
}

/* ===== 文字选择 ===== */
::selection {
    background: rgba(196, 164, 132, 0.3) !important;
    color: #1a1a2e !important;
}

/* ===== 载入动画 ===== */
.stLoadingSpinner {
    color: #c4a484 !important;
}

/* ===== 分步骤淡入动画 ===== */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.main .block-container {
    animation: fadeInUp 0.55s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* ===== 成功/信息/警告/错误消息 ===== */
.stSuccess {
    background: linear-gradient(135deg, rgba(212, 170, 125, 0.15) 0%, rgba(196, 164, 132, 0.1) 100%) !important;
    border-left: 4px solid #c4a484 !important;
}

.stInfo {
    background: linear-gradient(135deg, rgba(196, 164, 132, 0.1) 0%, rgba(196, 164, 132, 0.05) 100%) !important;
    border-left: 4px solid #c4a484 !important;
}

.stWarning {
    background: linear-gradient(135deg, rgba(240, 200, 150, 0.15) 0%, rgba(230, 180, 130, 0.1) 100%) !important;
    border-left: 4px solid #e8c48a !important;
}

.stError {
    background: linear-gradient(135deg, rgba(220, 160, 150, 0.15) 0%, rgba(200, 140, 130, 0.1) 100%) !important;
    border-left: 4px solid #d4a494 !important;
}
</style>

<!-- Google Fonts: 高级字体 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ==========================================
# 数据库 A：78 种香味与感性描述
# ==========================================
scent_map = {
    # --- 前调 (Top Notes) - 共 20 种 ---
    "前调 芳香 01": "富家千金 (小豆蔻/乌龙茶)",
    "前调 芳香 02": "夏天的风 (罗勒/百里香)",
    "前调 芳香 03": "野花 (小豆蔻/含羞草)",
    "前调 芳香 04": "肆意奔放 (小豆蔻/马郁兰)",
    "前调 芳香 05": "乡愁 (栀子花/绿叶/甘草)",
    "前调 芳香 06": "茶树 (茶树)",
    "前调 芳香 07": "薄荷 (薄荷)",
    "前调 芳香 08": "马鞭草 (马鞭草)",
    "前调 芳香 09": "绿茶 (绿茶)",
    "前调 柑橘 01": "花园 (橘子/柠檬/开心果)",
    "前调 柑橘 02": "记忆蜜糖 (橘子/桃子)",
    "前调 柑橘 03": "寂静秋夜 (胡萝卜/番茄/橙子)",
    "前调 柑橘 04": "气泡水 (葡萄柚/橘子)",
    "前调 柑橘 05": "海边漫步 (橙子/柠檬)",
    "前调 柑橘 06": "海滩 (佛手柑/柠檬/香橙)",
    "前调 柑橘 07": "纯真 (橙子/茉莉/琥珀)",
    "前调 柑苔 01": "晨间森林 (无花果木/香根草)",
    "前调 柑苔 02": "信仰 (橘子/麝香/苦橙叶)",
    "前调 柑苔 03": "清新 (葡萄柚/橡木苔)",
    "前调 柑苔 04": "苔藓 (苔藓)",

    # --- 中调 (Middle Notes) - 共 34 种 ---
    "中调 果香 01": "夏日庄园 (柑橘/无花果)",
    "中调 果香 02": "纯粹 (香瓜/橘子/黄瓜)",
    "中调 果香 03": "甜美 (草莓/梨/蜜橘)",
    "中调 果香 04": "情窦初开 (红浆果/糖)",
    "中调 果香 05": "撒丁岛 (橙花油/柠檬)",
    "中调 果香 06": "仲夏花园 (红苹果/玫瑰)",
    "中调 果香 07": "酸甜软妹 (黑加仑/菠萝/焦糖)",
    "中调 果香 08": "地中海 (香豌豆/柠檬/焦糖)",
    "中调 果香 09": "海边微风 (黄葵/盐)",
    "中调 果香 10": "咖啡厅 (甜苹果/香橙花/香草)",
    "中调 果香 11": "柑橘 (柑橘)",
    "中调 果香 12": "柠檬 (柠檬)",
    "中调 果香 13": "百香果 (百香果)",
    "中调 果香 14": "青瓜 (青瓜)",
    "中调 果香 15": "青苹果 (青苹果)",
    "中调 花香 01": "白衬衫 (薰衣草/橙花)",
    "中调 花香 02": "优雅女人 (晚香玉/茉莉花)",
    "中调 花香 03": "雨后花园 (玫瑰/依兰)",
    "中调 花香 04": "静谧花园 (玫瑰/茉莉)",
    "中调 花香 05": "初春 (玫瑰/蜂蜜)",
    "中调 花香 06": "春意盎然 (茉莉/绿叶)",
    "中调 花香 07": "梨子酒 (梨/小苍兰)",
    "中调 花香 08": "森林小屋 (薰衣草/肉豆蔻)",
    "中调 花香 09": "稻香 (橙花/香草)",
    "中调 花香 10": "异域风情 (晚香玉/依兰)",
    "中调 花香 11": "优雅 (茉莉/兰花/李子)",
    "中调 花香 12": "薰衣草 (薰衣草)",
    "中调 花香 13": "夜来香 (夜来香)",
    "中调 花香 14": "栀子花 (栀子花)",
    "中调 花香 15": "依兰 (依兰)",
    "中调 花香 16": "玫瑰 (玫瑰)",
    "中调 花香 17": "风铃草 (风铃草)",
    "中调 花香 18": "茉莉 (茉莉)",
    "中调 花香 19": "桂花 (桂花)",

    # --- 后调 (Base Notes) - 共 24 种 ---
    "后调 东方 01": "雨落幽然 (苦橙/琥珀)",
    "后调 东方 02": "乌龙茶 (茶叶/香根草)",
    "后调 东方 03": "新伦敦男 (肉桂/烟草/橡木苔)",
    "后调 东方 04": "古老书店 (冬加豆)",
    "后调 东方 05": "西西里岛 (杏仁/香草/麝香)",
    "后调 东方 06": "阳光 (紫罗兰/香草/麝香)",
    "后调 东方 07": "高山微风 (迷迭香/广藿香)",
    "后调 东方 08": "冬日壁炉 (琥珀/麝香)",
    "后调 东方 09": "荷尔蒙 (花椒/广藿香)",
    "后调 东方 10": "法国绅士 (橘子/檀香木)",
    "后调 东方 11": "梅糖 (梨/杏仁/香草)",
    "后调 木质 01": "冬日松林 (雪松/麝香)",
    "后调 木质 02": "沉静森林 (白松香/檀香)",
    "后调 木质 03": "沉稳 (莞荽/香根草/雪松木)",
    "后调 木质 04": "龙涎 (龙涎/琥珀/木质)",
    "后调 木质 05": "雪松 (雪松)",
    "后调 木质 06": "空灵 (麝香/沉香)",
    "后调 木质 07": "晨间山风 (香草/沉香)",
    "后调 木质 08": "寺庙 (黑胡椒/檀木)",
    "后调 木质 09": "云雾 (迷迭香/樟木)",
    "后调 木质 10": "故乡 (沉香/广藿香)",
    "后调 木质 11": "焚香 (沉香/巴西红木)",
    "后调 木质 12": "月光柏木 (苦橙/柏树)",
    "后调 木质 13": "檀香 (檀香)"
}
scent_descriptions = {
    # --- 前调 (Top Notes) ---
    "前调 芳香 01": "清冷乌龙与辛香小豆蔻碰撞，仿佛在雾气缭绕的清晨茶山中独坐。",
    "前调 芳香 02": "清新的罗勒与百里香交织，如同漫步在洒满午后阳光的欧式香草园。",
    "前调 芳香 03": "含羞草的粉感与小豆蔻的暖意，像是踏入一片开满无名野花的静谧荒野。",
    "前调 芳香 04": "马郁兰的药草气息带动感性，散发出一种无拘无束、肆意奔放的自由感。",
    "前调 芳香 05": "栀子花的洁白与绿叶的清苦，勾起记忆中那抹淡淡的、带有草木香的乡愁。",
    "前调 芳香 06": "强劲的茶树气息，像是雨后森林般清冽，带给灵魂最彻底的净化与苏醒。",
    "前调 芳香 07": "极致清凉的薄荷，瞬间点燃感官，仿佛在炎热夏日喝下一口冰镇泉水。",
    "前调 芳香 08": "马鞭草的柠檬清香，带来轻盈跳跃的活力，让心情随之飞扬。",
    "前调 芳香 09": "优雅的绿茶清芬，如同细雨过后的竹林，安静、内敛且充满禅意。",
    "前调 柑橘 01": "橘子与柠檬的酸甜，伴随开心果的微香，像是一场色彩缤纷的花园派对。",
    "前调 柑橘 02": "多汁的桃子融入柑橘，营造出被蜜糖包裹的童年记忆，甜而不腻。",
    "前调 柑橘 03": "胡萝卜与橙子的奇妙结合，如同在秋日的寂静黄昏，看落叶铺满大地。",
    "前调 柑橘 04": "清爽喷涌的葡萄柚气泡，充满爆发力的酸甜，瞬间提振精神。",
    "前调 柑橘 05": "沁人心脾的清爽柑橘，仿佛光著脚在海边漫步，感受浪花轻拍脚踝。",
    "前调 柑橘 06": "佛手柑的轻盈与柠檬的海风感，让思绪飘向遥远的地中海沙滩。",
    "前调 柑橘 07": "橘子与纯真茉莉的邂逅，像是微风中摇曳的白色裙摆，纯净且动人。",
    "前调 柑苔 01": "无花果木与香根草的结合，如同清晨走进原始森林，脚下是潮湿的泥土。",
    "前调 柑苔 02": "苦橙叶与麝香的深层共鸣，代表一种内在的坚定，如同朝圣者的信仰。",
    "前调 柑苔 03": "橡木苔与葡萄柚的冷静感，像是一阵穿透迷雾的清香，带来极致的清醒。",
    "前调 柑苔 04": "潮湿的苔藓气息，带有一丝泥土的芬芳，让人不自觉地向大自然深处探索。",

    # --- 中调 (Middle Notes) ---
    "中调 果香 01": "柑橘与无花果的暖甜，仿佛置身于南法庄园，享受悠闲的午后时光。",
    "中调 果香 02": "甜美的香瓜与清凉黄瓜，纯粹得不带一丝杂质，让感官瞬间降温。",
    "中调 果香 03": "草莓与蜜橘的香甜，像是初恋时咬下的第一口水果糖，满口芳甜。",
    "中调 果香 04": "红浆果的酸甜与糖分的结合，谱写出一曲关于情窦初开的甜蜜乐章。",
    "中调 果香 05": "橙花油与柠檬的清冽，带您飞向撒丁岛，感受海风中的清爽果味。",
    "中调 果香 06": "红苹果与玫瑰的交融，如同在仲夏的花园中，邂逅最灿烂的盛放。",
    "中调 果香 07": "黑加仑与菠萝的奔放，带有一点焦糖的甜润，展现出酸甜软妹的俏皮感。",
    "中调 果香 08": "香豌豆与焦糖的层次感，像是地中海阳光下的午后茶点，慵懒而满足。",
    "中调 果香 09": "黄葵与盐的结合，如同海边拂过的微风，带有一丝不露痕迹的迷人魅力。",
    "中调 果香 10": "香橙花与香草交织出的温暖甜香，仿佛冬日午后，坐在弥漫香气的咖啡厅。",
    "中调 花香 01": "薰衣草与橙花的洁净，像是一件刚在阳光下晾干的白衬衫，让人倍感舒心。",
    "中调 花香 02": "晚香玉与茉莉的浓郁花香，自信而优雅，绽放出成熟女性的迷人光彩。",
    "中调 花香 03": "玫瑰与依兰在雨后湿润的气息中绽放，如同走入一座神秘且幽静的庭园。",
    "中调 花香 04": "玫瑰与茉莉的经典结合，安静地盛开在心田，营造出一份内心的静谧。",
    "中调 花香 05": "蜂蜜包裹著初春的玫瑰，柔情似水，缓缓释放出春天最温柔的讯息。",
    "中调 花香 06": "茉莉与翠绿叶片的气息，生机盎然，仿佛看见春芽在枝头轻轻颤动。",
    "中调 花香 07": "梨与小苍兰交织出的微醺气息，像是倒出一杯清透的梨子酒，晶莹动人。",
    "中调 花香 08": "薰衣草与肉豆蔻的温暖辛香，如同躲进大雪中的森林小屋，炉火正旺。",
    "中调 花香 09": "橙花与香草的清甜，带有一丝稻米的温润感，是丰收季节最安心的问候。",
    "中调 花香 10": "依兰与晚香玉的异国风情，神秘且大胆，领您踏上一场华丽的冒险之旅。",
    "中调 花香 11": "兰花与李子的交织，优雅而不失灵动，在举手投足间流露出高级质感。",
    "中调 花香 19": "清甜入骨的桂花香，仿佛在某个秋夜的街角，偶遇了一场关于月光的梦。",

    # --- 后调 (Base Notes) ---
    "后调 东方 01": "苦橙与琥珀的碰撞，如同细雨落下后的幽然森林，带著神秘的暖意。",
    "后调 东方 02": "茶叶与香根草的交融，带有一种沉淀过后的文雅，是灵魂深处的冷静。",
    "后调 东方 03": "肉桂与烟草的成熟韵味，如同在伦敦街头漫步的高雅男士，从容且自信。",
    "后调 东方 04": "冬加豆的醇厚气息，像是走进一间塞满旧书的老书店，时间在此凝固。",
    "后调 东方 05": "杏仁、香草与麝香的包裹，如同西西里岛的暖阳，温润而令人陶醉。",
    "后调 东方 06": "紫罗兰与香草的轻柔呼吸，像是在阳光下舒展身体，感受生命最柔软的时刻。",
    "后调 东方 07": "迷迭香与广藿香的交缠，如高山顶峰掠过的疾风，清澈且具有穿透力。",
    "后调 东方 08": "琥珀与麝香营造出炉火般的温度，如同在寒冬中，靠近最温暖的壁炉。",
    "后调 东方 09": "花椒的微辛与广藿香的深沉，释放出强烈的荷尔蒙感，危险且诱人。",
    "后调 东方 10": "橘子与檀香木的优雅结合，是一位风度翩翩的法国绅士，低调且尊贵。",
    "后调 东方 11": "梨与香草的甜糯感，像是童年最爱的那颗梅糖，在舌尖缓缓化开。",
    "后调 木质 01": "雪松与麝香的冷暖对比，如同银装素裹的松林，清冷而又透著生机。",
    "后调 木质 02": "白松香与檀香的沈静，如同进入一片无人打扰的森林深处，呼吸著自由。",
    "后调 木质 03": "香根草与雪松的扎实感，赋予心灵一种无与伦比的沉稳与定力。",
    "后调 木质 04": "龙涎与琥珀的交织，如同时间雕琢而成的树脂，闪烁著大地的光辉。",
    "后调 木质 05": "纯粹的雪松香气，洁净且笔直，是灵魂最不容妥协的底色。",
    "后调 木质 06": "麝香与沉香的空灵结合，仿佛跨越时空的呼吸，缥缈且神圣。",
    "后调 木质 07": "香草与沉香的甜苦交织，如同晨间穿透山风的第一缕阳光，充满希望。",
    "后调 木质 08": "檀木与黑胡椒的庄严感，像是踏入静谧的寺庙，浮躁瞬间消散无踪。",
    "后调 木质 09": "迷迭香与樟木的清冽，如云雾缭绕的山巅，清冷且让人心旷神怡。",
    "后调 木质 10": "沉香与广藿香的厚重感，是记忆中无法抹去的故乡记忆，深情且踏实。",
    "后调 木质 11": "沉香与巴西红木的激荡，在焚香的萦绕中，展现出一种超脱尘世的静谧。",
    "后调 木质 12": "柏树与苦橙的坚韧，如同在月光下挺拔的柏树，守护著夜晚的安宁。",
    "后调 木质 13": "纯净的檀香，温润如玉，是时间沉淀下来的最温柔的底气。"
}

# ==========================================
# 数据库 B：命理、人格与比例逻辑
# ==========================================
zodiac_db = {
    "白羊座": "勇气与活力的开拓者。拥有一往无前的能量，性格纯粹、直率。",
    "金牛座": "质感生活的守护者。感官敏锐，追求稳定与极致的美感。",
    "双子座": "好奇灵动的思想传播者。思维跳跃、热爱沟通，灵魂中藏著风的自由。",
    "巨蟹座": "细腻疗愈的情感温室。守护内在的安全感，感性且具备极强共情力。",
    "狮子座": "自信领导的创造力中心。拥有强大的意志与温暖的慷慨，如太阳般耀眼。",
    "处女座": "追求完美的秩序工匠。心思缜密，具备冷静的观察力与纯净灵魂底色。",
    "天秤座": "优雅平衡的协调艺术家。追求和谐与美感，处事从容不迫。",
    "天蝎座": "神秘洞察的灵魂探测器。情感深邃、意志坚定，气质高冷且极具磁性。",
    "射手座": "冒险自由的真理追寻者。热爱远方与探索，拥有一种不被世俗拘束的气场。",
    "摩羯座": "踏实责任的攀登先锋。拥有惊人的耐力与野心，气质沉著冷静。",
    "水瓶座": "独立革新的未来思想家。思维超前、特立独行，散发著智慧的独特电波。",
    "双鱼座": "灵性艺术的梦想编织者。灵魂充满诗意，感性且慈悲。"
}

element_traits = {
    "水": "【水能量：灵性智慧】具备极强的适应力与穿透力，性格细腻包容。",
    "木": "【木能量：成长生机】代表生命力，性格仁慈正直，拥有自我突破的渴望。",
    "火": "【火能量：热情热烈】散发温暖，性格开朗重视礼仪，具强大感染力。",
    "金": "【金能量：刚毅精准】拥有决断力，性格冷静正直，追求效率与核心价值。",
    "土": "【土能量：厚重稳定】象征大地的包容，性格沉稳踏实，是值得信赖的依靠。"
}

zodiac_animal_db = {
    "鼠": "机敏俐落，观察细微。", "牛": "勤奋稳重，意志力强。", "虎": "威猛果敢，具开创精神。",
    "兔": "文雅温柔，心思缜密。", "龙": "宏伟不凡，领袖魅力。", "蛇": "冷静沉著，直觉灵敏。",
    "马": "奔放热情，热爱自由。", "羊": "体贴仁慈，具艺术感。", "猴": "聪明变通，充满创意。",
    "鸡": "负责果断，讲求纪律。", "狗": "忠诚正义，值得信赖。", "猪": "真诚厚道，性情豁达。"
}

zodiac_elements = {"鼠": "水", "猪": "水", "虎": "木", "兔": "木", "蛇": "火", "马": "火", "猴": "金", "鸡": "金", "牛": "土", "龙": "土", "羊": "土", "狗": "土"}

# ==========================================
# 数据库 D：生命灵数个性与建议
# ==========================================
life_number_db = {
    "1": {
        "trait": "天生的领导者与开创者",
        "desc": "你拥有强烈的独立意识与开创精神，不喜欢被约束，总是走在前端。你的内在燃烧著一股不服输的火焰，渴望证明自己的价值。",
        "advice": "今年宜把握机会展现领导力，但切记刚柔并济。过度强势可能让贵人远离，学会倾听他人意见，成功将水到渠成。感情上主动出击会有好结果。"
    },
    "2": {
        "trait": "温柔的协调者与疗愈师",
        "desc": "你天生敏感细腻，擅长察觉他人情绪，是团体中的润滑剂。你追求和谐与平衡，不喜欢冲突，总是默默付出。",
        "advice": "今年是建立深度关系的好时机，但要注意不要过度委屈自己。学会设立界限，你的温柔才不会成为负担。财运平稳，合作投资优於单打独斗。"
    },
    "3": {
        "trait": "创意的表达者与乐观主义者",
        "desc": "你充满创造力与想像力，拥有感染他人的魅力。你热爱表达，无论是艺术、写作或口才都有天赋，是天生的表演者。",
        "advice": "今年创意能量爆发，适合展开艺术相关计划或副业。但要小心三分钟热度，专注完成一件事比开始十件事更重要。桃花运旺，但需分辨真心。"
    },
    "4": {
        "trait": "稳健的建筑师与守护者",
        "desc": "你务实可靠，是值得信赖的伙伴。你相信脚踏实地的力量，愿意付出努力建构稳固的基础，是团队中的定海神针。",
        "advice": "今年适合打稳根基，无论是事业、健康或财务都宜稳扎稳打。不要急于求成，你的坚持终将开花结果。注意身体保养，尤其是肩颈与肠胃。"
    },
    "5": {
        "trait": "自由的冒险家与变革者",
        "desc": "你渴望自由与变化，讨厌一成不变的生活。你拥有强烈的好奇心，喜欢探索未知，是勇于突破框架的先锋。",
        "advice": "今年变动能量强，可能有旅行、搬迁或转换跑道的机会。拥抱变化但不要冲动行事，做好规划再出发。感情上可能遇到异地或异国缘分。"
    },
    "6": {
        "trait": "爱的给予者与美的追求者",
        "desc": "你重视家庭与责任，拥有强烈的爱与奉献精神。你追求美好事物，对生活品质有要求，是天生的照顾者与美学家。",
        "advice": "今年家庭运势重要，可能有婚嫁、添丁或购屋等喜事。但要注意不要过度干涉他人，爱是给予自由而非控制。财运与美相关的投资有利。"
    },
    "7": {
        "trait": "深邃的思想家与灵性探索者",
        "desc": "你拥有深刻的洞察力与分析能力，喜欢独处思考人生大哉问。你追求真理与智慧，内在世界丰富而神秘。",
        "advice": "今年适合进修、研究或灵性成长，你的直觉特别准确。但要避免过度封闭自己，适时与人交流能带来意想不到的启发。健康上注意睡眠品质。"
    },
    "8": {
        "trait": "权力的掌控者与物质的创造者",
        "desc": "你拥有强大的执行力与商业头脑，对成功有强烈渴望。你懂得运用资源，是天生的企业家与领袖，注定与财富有缘。",
        "advice": "今年事业运强劲，有升迁加薪或创业良机。但权力越大责任越大，注意不要忽略家人感受。财运亨通但切忌贪婪，见好就收是智慧。"
    },
    "9": {
        "trait": "博爱的理想主义者与疗愈者",
        "desc": "你拥有宽广的胸怀与悲天悯人的情怀，渴望让世界变得更好。你是天生的助人者，经常吸引需要帮助的人靠近。",
        "advice": "今年是完成与放下的一年，旧的篇章即将结束，新的即将开始。学会释怀过去的遗憾，你的善良终将得到宇宙的回报。公益活动会带来好运。"
    }
}

# ==========================================
# 数据库 E：2026 马年幸运色
# ==========================================
horse_year_lucky_colors = {
    # 生肖幸运色 (2026 马年)
    "zodiac": {
        "鼠": {"colors": ["宝蓝色", "银白色"], "avoid": "红色", "reason": "鼠马相冲，宜用水色化解，蓝色带来冷静与智慧。"},
        "牛": {"colors": ["咖啡色", "米白色"], "avoid": "绿色", "reason": "牛与马无刑冲，土色系稳固根基，带来踏实能量。"},
        "虎": {"colors": ["翠绿色", "橙红色"], "avoid": "白色", "reason": "虎马三合，火木相生，绿色与橙色助旺贵人运。"},
        "兔": {"colors": ["浅粉色", "淡紫色"], "avoid": "深蓝色", "reason": "兔与马无大碍，柔和色调提升人缘与桃花运。"},
        "龙": {"colors": ["金黄色", "酒红色"], "avoid": "黑色", "reason": "龙马精神相助，金色招财，酒红增添尊贵气场。"},
        "蛇": {"colors": ["枣红色", "紫红色"], "avoid": "白色", "reason": "蛇马六合大吉，红紫色系强化这份贵人缘分。"},
        "马": {"colors": ["草绿色", "粉红色"], "avoid": "蓝色", "reason": "本命年宜低调，绿色带来生机，粉色化解煞气。"},
        "羊": {"colors": ["橘橙色", "鹅黄色"], "avoid": "灰色", "reason": "羊马三合，暖色调催旺这份好运，带来喜悦能量。"},
        "猴": {"colors": ["白色", "银灰色"], "avoid": "红色", "reason": "猴与马相刑，金色系化解冲突，带来冷静思考。"},
        "鸡": {"colors": ["金色", "米黄色"], "avoid": "红色", "reason": "鸡马无碍，金色招财纳福，米黄增添稳重气质。"},
        "狗": {"colors": ["墨绿色", "橙色"], "avoid": "蓝色", "reason": "狗马三合，绿橙色系强化合作运与事业运。"},
        "猪": {"colors": ["深蓝色", "黑色"], "avoid": "黄色", "reason": "猪与马无大冲，水色系带来智慧，黑色稳定情绪。"}
    },
    # 灵数幸运色 (2026 马年)
    "life_number": {
        "1": {"colors": ["正红色", "金色"], "reason": "领导者能量需要正红色的热情与金色的权威加持。"},
        "2": {"colors": ["粉红色", "银白色"], "reason": "协调者需要柔和色调，粉银带来和谐与温柔力量。"},
        "3": {"colors": ["橙色", "黄色"], "reason": "创意能量与暖色调共振，橙黄色激发灵感与表达力。"},
        "4": {"colors": ["棕色", "深绿色"], "reason": "稳健能量需要大地色系，带来扎根与安全感。"},
        "5": {"colors": ["天蓝色", "亮绿色"], "reason": "自由能量喜爱清新色调，蓝绿色带来冒险与突破。"},
        "6": {"colors": ["粉紫色", "玫瑰金"], "reason": "爱的能量与浪漫色系共振，增添美感与家庭和谐。"},
        "7": {"colors": ["靛蓝色", "紫色"], "reason": "灵性能量需要深邃色调，紫蓝色提升直觉与智慧。"},
        "8": {"colors": ["黑色", "金色"], "reason": "权力能量与尊贵色系共振，黑金组合招财又稳重。"},
        "9": {"colors": ["白色", "浅紫色"], "reason": "博爱能量需要纯净色调，白紫带来疗愈与慈悲力量。"}
    }
}

# ==========================================
# 数据库 F：八字五行计算
# ==========================================
# 天干
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# 天干五行
STEM_ELEMENTS = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
# 地支五行
BRANCH_ELEMENTS = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
# 时辰对应
HOUR_BRANCHES = {
    "子时 (23:00-01:00)": "子", "丑时 (01:00-03:00)": "丑", "寅时 (03:00-05:00)": "寅",
    "卯时 (05:00-07:00)": "卯", "辰时 (07:00-09:00)": "辰", "巳时 (09:00-11:00)": "巳",
    "午时 (11:00-13:00)": "午", "未时 (13:00-15:00)": "未", "申时 (15:00-17:00)": "申",
    "酉时 (17:00-19:00)": "酉", "戌时 (19:00-21:00)": "戌", "亥时 (21:00-23:00)": "亥"
}

# 五行补充建议
ELEMENT_ADVICE = {
    "金": {"desc": "金主义，代表决断与正义感", "补": "多穿白色、金色衣物，配戴金属饰品，多往西方发展。", "水晶": "白水晶、钛晶、金发晶"},
    "木": {"desc": "木主仁，代表成长与慈悲心", "补": "多穿绿色衣物，多接触植物与大自然，多往东方发展。", "水晶": "绿幽灵、绿发晶、东菱玉"},
    "水": {"desc": "水主智，代表智慧与灵活性", "补": "多穿黑色、蓝色衣物，多亲近水边，多往北方发展。", "水晶": "海蓝宝、黑曜石、蓝纹玛瑙"},
    "火": {"desc": "火主礼，代表热情与感染力", "补": "多穿红色、紫色衣物，多晒太阳，多往南方发展。", "水晶": "红玛瑙、紫水晶、石榴石"},
    "土": {"desc": "土主信，代表稳重与包容力", "补": "多穿黄色、棕色衣物，多接触大地，居中发展最佳。", "水晶": "黄水晶、虎眼石、茶晶"}
}

def get_year_pillar(year):
    """计算年柱"""
    stem_index = (year - 4) % 10
    branch_index = (year - 4) % 12
    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]

def get_month_pillar(year, month):
    """计算月柱（简化版）"""
    # 月柱的天干需要根据年干来推算
    year_stem_index = (year - 4) % 10
    # 月支固定：寅月=1月, 卯月=2月...
    month_branch_index = (month + 1) % 12
    # 月干计算公式
    month_stem_index = (year_stem_index * 2 + month) % 10
    return HEAVENLY_STEMS[month_stem_index], EARTHLY_BRANCHES[month_branch_index]

def get_day_pillar(year, month, day):
    """计算日柱（使用简化公式）"""
    # 简化的日柱计算
    base = date(1900, 1, 1)
    target = date(year, month, day)
    days = (target - base).days
    stem_index = (days + 10) % 10
    branch_index = days % 12
    return HEAVENLY_STEMS[stem_index], EARTHLY_BRANCHES[branch_index]

def get_hour_pillar(day_stem, hour_branch):
    """计算时柱"""
    day_stem_index = HEAVENLY_STEMS.index(day_stem)
    hour_branch_index = EARTHLY_BRANCHES.index(hour_branch)
    # 时干计算公式
    hour_stem_index = (day_stem_index * 2 + hour_branch_index) % 10
    return HEAVENLY_STEMS[hour_stem_index], hour_branch

def calculate_five_elements(birthday, birth_hour=None):
    """计算八字五行"""
    year, month, day = birthday.year, birthday.month, birthday.day

    # 计算四柱
    year_stem, year_branch = get_year_pillar(year)
    month_stem, month_branch = get_month_pillar(year, month)
    day_stem, day_branch = get_day_pillar(year, month, day)

    pillars = [
        (year_stem, year_branch, "年柱"),
        (month_stem, month_branch, "月柱"),
        (day_stem, day_branch, "日柱")
    ]

    if birth_hour:
        hour_stem, hour_branch = get_hour_pillar(day_stem, birth_hour)
        pillars.append((hour_stem, hour_branch, "时柱"))

    # 统计五行
    element_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    for stem, branch, _ in pillars:
        element_count[STEM_ELEMENTS[stem]] += 1
        element_count[BRANCH_ELEMENTS[branch]] += 1

    # 找出缺少的五行
    missing = [e for e, c in element_count.items() if c == 0]
    weak = [e for e, c in element_count.items() if c == 1]
    strong = [e for e, c in element_count.items() if c >= 3]

    return {
        "pillars": pillars,
        "counts": element_count,
        "missing": missing,
        "weak": weak,
        "strong": strong,
        "day_master": STEM_ELEMENTS[day_stem]  # 日主五行
    }

mbti_db = {
    "INTJ (建筑师)": {
        "top": ["前调 芳香 01", "前调 柑苔 01", "前调 芳香 05"],
        "mid": ["中调 花香 01", "中调 花香 02", "中调 花香 19"],
        "base": ["后调 木质 01", "后调 木质 08", "后调 木质 05"]
    },
    "INFP (调解者)": {
        "top": ["前调 芳香 03", "前调 芳香 02", "前调 柑橘 01"],
        "mid": ["中调 花香 19", "中调 花香 03", "中调 果香 01"],
        "base": ["后调 木质 13", "后调 木质 02", "后调 东方 02"]
    },
    "INFJ (提倡者)": {
        "top": ["前调 芳香 09", "前调 柑苔 04", "前调 芳香 05"],
        "mid": ["中调 花香 04", "中调 花香 06", "中调 花香 14"],
        "base": ["后调 木质 11", "后调 木质 06", "后调 东方 02"]
    },
    "ENFP (竞选者)": {
        "top": ["前调 柑橘 04", "前调 柑橘 02", "前调 芳香 08"],
        "mid": ["中调 果香 03", "中调 果香 04", "中调 花香 07"],
        "base": ["后调 东方 06", "后调 东方 11", "后调 木质 13"]
    },
    "ENTJ (指挥官)": {
        "top": ["前调 芳香 04", "前调 柑苔 01", "前调 柑橘 03"],
        "mid": ["中调 花香 11", "中调 果香 05", "中调 果香 01"],
        "base": ["后调 东方 09", "后调 木质 08", "后调 东方 03"]
    },
    "ENTP (辩论家)": {
        "top": ["前调 柑橘 04", "前调 芳香 07", "前调 柑苔 03"],
        "mid": ["中调 果香 07", "中调 果香 08", "中调 花香 17"],
        "base": ["后调 东方 03", "后调 东方 09", "后调 木质 11"]
    },
    "ENFJ (主人公)": {
        "top": ["前调 柑橘 07", "前调 芳香 09", "前调 柑橘 05"],
        "mid": ["中调 花香 05", "中调 花香 09", "中调 果香 06"],
        "base": ["后调 木质 13", "后调 东方 08", "后调 木质 12"]
    },
    "ISTJ (物流师)": {
        "top": ["前调 芳香 06", "前调 柑苔 02", "前调 芳香 08"],
        "mid": ["中调 花香 01", "中调 花香 08", "中调 果香 12"],
        "base": ["后调 木质 05", "后调 木质 03", "后调 木质 10"]
    },
    "ISFJ (守卫者)": {
        "top": ["前调 柑橘 07", "前调 芳香 02", "前调 柑橘 01"],
        "mid": ["中调 花香 09", "中调 花香 12", "中调 花香 18"],
        "base": ["后调 木质 02", "后调 东方 08", "后调 木质 01"]
    },
    "ESTJ (总经理)": {
        "top": ["前调 芳香 02", "前调 柑橘 05", "前调 芳香 08"],
        "mid": ["中调 花香 01", "中调 果香 11", "中调 果香 12"],
        "base": ["后调 木质 03", "后调 木质 08", "后调 木质 10"]
    },
    "ESFJ (执政官)": {
        "top": ["前调 果香 03", "前调 柑橘 02", "前调 柑橘 01"],
        "mid": ["中调 花香 14", "中调 花香 16", "中调 果香 10"],
        "base": ["后调 东方 06", "后调 木质 13", "后调 东方 11"]
    },
    "ISTP (鉴赏家)": {
        "top": ["前调 芳香 07", "前调 柑苔 03", "前调 芳香 06"],
        "mid": ["中调 果香 09", "中调 花香 08", "中调 果香 14"],
        "base": ["后调 木质 06", "后调 木质 12", "后调 东方 02"]
    },
    "ISFP (探险家)": {
        "top": ["前调 柑橘 03", "前调 芳香 03", "前调 柑橘 06"],
        "mid": ["中调 花香 07", "中调 果香 02", "中调 花香 03"],
        "base": ["后调 木质 07", "后调 东方 05", "后调 木质 04"]
    },
    "ESTP (企业家)": {
        "top": ["前调 柑橘 04", "前调 柑苔 01", "前调 芳香 04"],
        "mid": ["中调 果香 07", "中调 果香 08", "中调 果香 13"],
        "base": ["后调 东方 07", "后调 东方 09", "后调 木质 12"]
    },
    "ESFP (表演者)": {
        "top": ["前调 柑橘 02", "前调 柑橘 04", "前调 果香 04"],
        "mid": ["中调 花香 10", "中调 花香 13", "中调 果香 15"],
        "base": ["后调 东方 11", "后调 东方 06", "后调 东方 01"]
    },
    "INTP (逻辑学家)": {
        "top": ["前调 芳香 01", "前调 芳香 09", "前调 柑苔 04"],
        "mid": ["中调 果香 14", "中调 花香 06", "中调 果香 09"],
        "base": ["后调 木质 06", "后调 木质 11", "后调 东方 02"]
    }
}

# MBTI 个性关键词（用于香味匹配说明）
mbti_personality = {
    "INTJ (建筑师)": "深思熟虑、追求卓越",
    "INFP (调解者)": "浪漫理想、温柔敏感",
    "INFJ (提倡者)": "直觉敏锐、深情内敛",
    "ENFP (竞选者)": "热情开朗、充满活力",
    "ENTJ (指挥官)": "自信果断、领导魅力",
    "ENTP (辩论家)": "机智灵活、大胆创新",
    "ENFJ (主人公)": "温暖热心、感染力强",
    "ISTJ (物流师)": "稳重务实、严谨可靠",
    "ISFJ (守卫者)": "温柔体贴、细心呵护",
    "ESTJ (总经理)": "高效果断、务实负责",
    "ESFJ (执政官)": "热心友善、乐于助人",
    "ISTP (鉴赏家)": "冷静理性、独立沉著",
    "ISFP (探险家)": "艺术感性、自由真实",
    "ESTP (企业家)": "大胆果敢、勇于冒险",
    "ESFP (表演者)": "活泼开朗、热爱生活",
    "INTP (逻辑学家)": "理性深邃、好奇探索"
}

zodiac_scents = {
    "白羊座": {"top": "前调 柑橘 04", "reason": "葡萄柚的爆发力对应开拓者不熄的勇气能量。"},
    "金牛座": {"top": "前调 芳香 05", "reason": "栀子花的细腻纯净，呼应您对感官品质与质感的追求。"},
    "双子座": {"top": "前调 芳香 02", "reason": "罗勒与百里香的灵动，诠释您跳跃的好奇心与思考速度。"},
    "巨蟹座": {"top": "前调 芳香 01", "reason": "清冷乌龙后的温润余韵，营造出如家一般的归属与安全感。"},
    "狮子座": {"top": "前调 芳香 04", "reason": "马郁兰的肆意奔放，展现您天生的领导者魅力与创造力气场。"},
    "处女座": {"top": "前调 芳香 06", "reason": "茶树的清冽与纯净，呼应您对事物细节与完美的极致坚持。"},
    "天秤座": {"top": "前调 芳香 09", "reason": "绿茶的优雅清芬，助您达成内在灵魂与外在环境的极致平衡。"},
    "天蝎座": {"top": "前调 柑苔 01", "reason": "无花果木的深邃感，对应您神秘的直觉与强大的灵魂转化力。"},
    "射手座": {"top": "前调 芳香 08", "reason": "马鞭草的清爽跳跃，带领灵魂追寻远方不被束缚的绝对自由。"},
    "摩羯座": {"top": "前调 芳香 01", "reason": "沈稳结构的小豆蔻茶香，展现您踏实前行、值得信赖的责任感。"},
    "水瓶座": {"top": "前调 芳香 07", "reason": "极致清凉的薄荷，致敬您特立独行、革新未来的人道主义灵魂。"},
    "双鱼座": {"top": "前调 芳香 03", "reason": "含羞草的梦幻粉感，让您的艺术灵魂在梦境与现实间浪漫呼吸。"}
}

element_scents = {
    "水": {"base": "后调 东方 02"}, "木": {"base": "后调 木质 02"},
    "火": {"base": "后调 东方 06"}, "金": {"base": "后调 木质 05"}, "土": {"base": "后调 木质 08"}
}

model_logic = {
    "黄金平衡型 (20:35:45)": {"ratios": [0.20, 0.35, 0.45], "desc": "最稳定的结构，香气衔接平滑。"},
    "清新爆发型 (40:35:25)": {"ratios": [0.40, 0.35, 0.25], "desc": "强化前调爆发力，适合清爽提神。"},
    "深邃留香型 (15:30:55)": {"ratios": [0.15, 0.30, 0.55], "desc": "加重后调比重，展现持久魅力。"}
}

perfume_logic = {
    "日常通勤": {"type": "EDT", "total_oil": 1.0}, "约会派对": {"type": "EDP", "total_oil": 1.5},
    "商务正式": {"type": "EDP", "total_oil": 1.2}, "运动休闲": {"type": "Cologne", "total_oil": 0.8},
    "冥想睡眠": {"type": "Mist", "total_oil": 0.6}
}

# ==========================================
# 数据库 G：场景偏好题目
# ==========================================
scene_questions = [
    {
        "question": "闭上眼睛，想像一个让你最放松的自然环境：",
        "options": [
            {"text": "🌲 阳光穿透树叶的静谧森林", "scents": ["前调 柑苔 01", "前调 柑苔 04", "后调 木质 02"], "tag": "woody"},
            {"text": "🌊 海风轻拂的沙滩海岸", "scents": ["前调 柑橘 05", "前调 柑橘 06", "中调 果香 09"], "tag": "fresh"},
            {"text": "🌸 繁花盛开的浪漫花园", "scents": ["中调 花香 03", "中调 花香 04", "中调 花香 16"], "tag": "floral"},
            {"text": "⛰️ 云雾缭绕的高山之巅", "scents": ["前调 芳香 06", "后调 木质 09", "后调 东方 07"], "tag": "fresh"}
        ]
    },
    {
        "question": "什么时刻的氛围最能触动你的心？",
        "options": [
            {"text": "🌅 薄雾中的清晨，露珠还挂在叶尖", "scents": ["前调 芳香 09", "前调 芳香 02", "中调 花香 06"], "tag": "fresh"},
            {"text": "☀️ 阳光灿烂的午后，暖洋洋的惬意", "scents": ["前调 柑橘 01", "前调 柑橘 04", "中调 果香 01"], "tag": "citrus"},
            {"text": "🌆 华灯初上的傍晚，浪漫的微醺时分", "scents": ["中调 花香 02", "中调 花香 10", "后调 东方 01"], "tag": "oriental"},
            {"text": "🌙 万籁俱寂的深夜，独享静谧时光", "scents": ["后调 木质 06", "后调 木质 08", "后调 东方 04"], "tag": "woody"}
        ]
    },
    {
        "question": "以下哪个空间的气味让你最感到舒适？",
        "options": [
            {"text": "☕ 飘著咖啡香的温暖咖啡馆", "scents": ["中调 果香 10", "后调 东方 04", "后调 东方 08"], "tag": "oriental"},
            {"text": "🍵 清幽雅致的东方茶室", "scents": ["前调 芳香 01", "前调 芳香 09", "后调 东方 02"], "tag": "fresh"},
            {"text": "🍋 新鲜水果堆叠的夏日市集", "scents": ["前调 柑橘 02", "中调 果香 03", "中调 果香 07"], "tag": "citrus"},
            {"text": "🥐 刚出炉面包香的烘焙坊", "scents": ["后调 东方 05", "后调 东方 11", "中调 花香 09"], "tag": "oriental"}
        ]
    },
    {
        "question": "哪种活动状态最能代表你理想中的自己？",
        "options": [
            {"text": "🧘 静心冥想，与内在对话", "scents": ["后调 木质 08", "后调 木质 13", "前调 柑苔 04"], "tag": "woody"},
            {"text": "💃 派对狂欢，释放热情能量", "scents": ["前调 柑橘 04", "中调 果香 04", "中调 果香 07"], "tag": "citrus"},
            {"text": "📚 沉浸书海，享受知识洗礼", "scents": ["后调 东方 04", "后调 木质 02", "前调 芳香 05"], "tag": "woody"},
            {"text": "🎒 探索冒险，追寻未知刺激", "scents": ["前调 芳香 08", "前调 柑橘 06", "后调 东方 07"], "tag": "fresh"}
        ]
    },
    {
        "question": "哪个场景的气味会唤起你最美好的回忆？",
        "options": [
            {"text": "🏡 外婆家的老木柜与陈年香气", "scents": ["后调 木质 10", "后调 木质 11", "后调 东方 08"], "tag": "woody"},
            {"text": "🏨 高级饭店的优雅大厅香氛", "scents": ["中调 花香 02", "中调 花香 11", "后调 木质 13"], "tag": "floral"},
            {"text": "🌾 乡间田野的青草与泥土气息", "scents": ["前调 芳香 02", "前调 柑苔 04", "中调 花香 06"], "tag": "fresh"},
            {"text": "🌃 都市夜晚的时尚与神秘", "scents": ["后调 东方 03", "后调 东方 09", "后调 木质 06"], "tag": "oriental"}
        ]
    }
]

# ==========================================
# 数据库 H：季节偏好与香味对应
# ==========================================
season_scents = {
    "🌸 春天 - 万物复苏，生机盎然": {
        "top": ["前调 芳香 02", "前调 芳香 03", "前调 柑橘 01"],
        "mid": ["中调 花香 05", "中调 花香 06", "中调 花香 07"],
        "base": ["后调 木质 02", "后调 木质 07"],
        "desc": "春季香氛以清新花香为主调，带来新生的希望与活力。"
    },
    "☀️ 夏天 - 阳光灿烂，热情奔放": {
        "top": ["前调 柑橘 04", "前调 柑橘 05", "前调 柑橘 06"],
        "mid": ["中调 果香 02", "中调 果香 05", "中调 果香 09"],
        "base": ["后调 东方 06", "后调 木质 12"],
        "desc": "夏季香氛以柑橘果香为主调，清爽提神，充满活力。"
    },
    "🍂 秋天 - 金风送爽，沉稳内敛": {
        "top": ["前调 芳香 01", "前调 芳香 05", "前调 柑苔 01"],
        "mid": ["中调 花香 19", "中调 花香 08", "中调 果香 01"],
        "base": ["后调 木质 03", "后调 木质 10", "后调 东方 02"],
        "desc": "秋季香氛以木质温暖为主调，沉稳大气，韵味悠长。"
    },
    "❄️ 冬天 - 静谧深邃，温暖疗愈": {
        "top": ["前调 芳香 01", "前调 柑苔 02", "前调 芳香 07"],
        "mid": ["中调 花香 08", "中调 花香 09", "中调 果香 10"],
        "base": ["后调 东方 08", "后调 木质 08", "后调 东方 05"],
        "desc": "冬季香氛以东方暖香为主调，如壁炉般温暖，抚慰心灵。"
    }
}

# ==========================================
# 数据库 C：MBTI 简易测试题目
# ==========================================
mbti_questions = [
    # E/I 维度
    {"dimension": "EI", "question": "在社交场合中，你通常会：",
     "options": [("主动认识新朋友，享受交流", "E"), ("待在熟悉的人旁边，或找安静角落", "I")]},
    {"dimension": "EI", "question": "经过忙碌的一天后，你倾向用什么方式充电？",
     "options": [("和朋友聚会聊天", "E"), ("独处或安静地休息", "I")]},
    # S/N 维度
    {"dimension": "SN", "question": "你在思考事情时，更注重：",
     "options": [("具体的事实和细节", "S"), ("整体概念和未来可能性", "N")]},
    {"dimension": "SN", "question": "你更相信：",
     "options": [("实际经验和眼见为凭", "S"), ("直觉和第六感", "N")]},
    # T/F 维度
    {"dimension": "TF", "question": "做重要决定时，你更依赖：",
     "options": [("客观的逻辑分析", "T"), ("个人价值观和对他人的影响", "F")]},
    {"dimension": "TF", "question": "当朋友遇到困难向你倾诉时，你会先：",
     "options": [("帮忙分析问题并提供解决方案", "T"), ("倾听并给予情感支持", "F")]},
    # J/P 维度
    {"dimension": "JP", "question": "对于生活和工作，你更喜欢：",
     "options": [("事先计划好，按部就班", "J"), ("保持弹性，随机应变", "P")]},
    {"dimension": "JP", "question": "面对截止日期，你通常会：",
     "options": [("提前完成，避免压力", "J"), ("在最后期限前才完成，享受压力带来的动力", "P")]},
]

def calculate_mbti(answers):
    """根据测试答案计算 MBTI 类型"""
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for ans in answers:
        if ans:
            scores[ans] += 1

    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"

    # 对应到完整的 MBTI 名称
    mbti_names = {
        "INTJ": "INTJ (建筑师)", "INFP": "INFP (调解者)", "INFJ": "INFJ (提倡者)",
        "ENFP": "ENFP (竞选者)", "ENTJ": "ENTJ (指挥官)", "ENTP": "ENTP (辩论家)",
        "ENFJ": "ENFJ (主人公)", "ISTJ": "ISTJ (物流师)", "ISFJ": "ISFJ (守卫者)",
        "ESTJ": "ESTJ (总经理)", "ESFJ": "ESFJ (执政官)", "ISTP": "ISTP (鉴赏家)",
        "ISFP": "ISFP (探险家)", "ESTP": "ESTP (企业家)", "ESFP": "ESFP (表演者)",
        "INTP": "INTP (逻辑学家)"
    }
    return mbti_names.get(mbti, f"{mbti}")

# ==========================================
# 核心函数
# ==========================================
def generate_all_reasons(all_codes, personality_info):
    """
    为所有香味一次性生成不重复的个性匹配说明
    all_codes: 所有香味代码列表 (前调+中调+后调)
    personality_info: 个性资讯字典
    返回: {code: reason_text} 字典
    """
    if not personality_info:
        return {}

    # 为每个来源创建多个不同的模板，使用丰富多样的词汇
    all_templates = []

    # 星座模板 (10个，多样化词汇)
    if personality_info.get("zodiac_trait"):
        zodiac = personality_info.get("zodiac", "")
        trait = personality_info.get("zodiac_trait")
        all_templates.extend([
            ("zodiac", "{ing}的香味呼应你身为" + zodiac + trait + "的特质"),
            ("zodiac", "作为" + zodiac + "的你，{ing}的气息能衬托你" + trait + "的灵魂"),
            ("zodiac", zodiac + "天生" + trait + "，{ing}的香气正好能放大这份魅力"),
            ("zodiac", "{ing}与" + zodiac + trait + "的星象能量完美契合"),
            ("zodiac", "你的" + zodiac + "本命" + trait + "，{ing}能为你增添独特光彩"),
            ("zodiac", "{ing}的气息能唤醒" + zodiac + "内在" + trait + "的力量"),
            ("zodiac", zodiac + "守护星赋予你" + trait + "的气场，{ing}是最佳搭配"),
            ("zodiac", "{ing}的调性恰好映照" + zodiac + trait + "的星盘特质"),
            ("zodiac", "你" + zodiac + "的" + trait + "光环，因{ing}而更加闪耀"),
            ("zodiac", "{ing}能引导" + zodiac + trait + "的宇宙能量流动"),
        ])

    # MBTI 模板 (10个，多样化词汇)
    if personality_info.get("mbti_trait"):
        mbti = personality_info.get("mbti", "").split(" ")[0]
        trait = personality_info.get("mbti_trait")
        all_templates.extend([
            ("mbti", "{ing}的香味符合你" + trait + "的性格底蕴"),
            ("mbti", "你的 " + mbti + " 人格" + trait + "，与{ing}的气质完美共鸣"),
            ("mbti", "作为 " + mbti + " 型人格，{ing}能展现你" + trait + "的一面"),
            ("mbti", "{ing}的调性与 " + mbti + " " + trait + "的心理特质相辅相成"),
            ("mbti", "你" + trait + "的 " + mbti + " 性格，与{ing}产生美妙的化学反应"),
            ("mbti", "{ing}能强化你 " + mbti + " 人格中" + trait + "的魅力"),
            ("mbti", mbti + " 的认知功能" + trait + "，{ing}能将其具象化"),
            ("mbti", "{ing}为你 " + mbti + " 人格" + trait + "的内心世界增色"),
            ("mbti", "你" + trait + "的思维模式，与{ing}的香调异曲同工"),
            ("mbti", "{ing}呼应 " + mbti + " 型人" + trait + "的精神追求"),
        ])

    # 五行模板 (10个，多样化词汇) - 含水晶推荐
    if personality_info.get("element_trait"):
        element = personality_info.get("element", "")
        trait = personality_info.get("element_trait")

        # 五行对应水晶颜色与补充元素
        crystal_info = {
            "金": {"crystals": "白水晶、钛晶、金发晶", "color": "白色、金色", "enhance": "土", "enhance_crystal": "黄水晶、虎眼石"},
            "木": {"crystals": "绿幽灵、绿发晶、东菱玉", "color": "绿色", "enhance": "水", "enhance_crystal": "海蓝宝、黑曜石"},
            "水": {"crystals": "海蓝宝、黑曜石、蓝纹玛瑙", "color": "蓝色、黑色", "enhance": "金", "enhance_crystal": "白水晶、钛晶"},
            "火": {"crystals": "红玛瑙、紫水晶、石榴石", "color": "红色、紫色", "enhance": "木", "enhance_crystal": "绿幽灵、绿发晶"},
            "土": {"crystals": "黄水晶、虎眼石、茶晶", "color": "黄色、棕色", "enhance": "火", "enhance_crystal": "红玛瑙、紫水晶"}
        }

        info = crystal_info.get(element, {"crystals": "白水晶", "color": "透明", "enhance": "土", "enhance_crystal": "黄水晶"})
        crystal_tip = f"💎 推荐搭配{info['color']}系水晶如{info['crystals']}，或补{info['enhance']}行可选{info['enhance_crystal']}"

        all_templates.extend([
            ("element", "{ing}的香味能平衡你" + element + "属性" + trait + "的能量。" + crystal_tip),
            ("element", "你的五行属" + element + "，{ing}能滋养你" + trait + "的内在。" + crystal_tip),
            ("element", element + "行之人" + trait + "，{ing}能为你带来和谐。" + crystal_tip),
            ("element", "{ing}与你的" + element + "行能量" + trait + "相互呼应。" + crystal_tip),
            ("element", "五行" + element + "赋予你" + trait + "的本质，{ing}能将其升华。" + crystal_tip),
            ("element", "{ing}的气息能调和你" + element + "属性中" + trait + "的特质。" + crystal_tip),
            ("element", element + "命格" + trait + "，{ing}为你补足天地灵气。" + crystal_tip),
            ("element", "{ing}与" + element + "行" + trait + "的磁场形成共振。" + crystal_tip),
            ("element", "你" + element + "属性" + trait + "的根基，因{ing}而更稳固。" + crystal_tip),
            ("element", "{ing}能疏通" + element + "行" + trait + "的气脉运行。" + crystal_tip),
        ])

    # 生命灵数模板 (10个，多样化词汇)
    if personality_info.get("life_num_trait"):
        life_num = personality_info.get("life_num", "")
        trait = personality_info.get("life_num_trait")
        all_templates.extend([
            ("life_num", "作为 " + life_num + " 号人，{ing}的香气呼应你" + trait + "的天赋"),
            ("life_num", "{ing}的气息与你 " + life_num + " 号人" + trait + "的特质相得益彰"),
            ("life_num", "生命灵数 " + life_num + " 赋予你" + trait + "的能量，{ing}正好能放大它"),
            ("life_num", "{ing}能激发 " + life_num + " 号人内在" + trait + "的潜能"),
            ("life_num", "你 " + life_num + " 号人" + trait + "的特质，与{ing}的香调不谋而合"),
            ("life_num", "{ing}为 " + life_num + " 号人" + trait + "的灵魂注入活力"),
            ("life_num", "数字 " + life_num + " 的振动频率" + trait + "，与{ing}同频共振"),
            ("life_num", "{ing}能点亮 " + life_num + " 号人" + trait + "的生命蓝图"),
            ("life_num", "你与生俱来 " + life_num + " 号人" + trait + "的使命，{ing}助你绽放"),
            ("life_num", "{ing}的能量波与 " + life_num + " 号人" + trait + "的频率完美调谐"),
        ])

    # 生肖模板 (10个，多样化词汇)
    if personality_info.get("chinese_zodiac_trait"):
        c_zodiac = personality_info.get("chinese_zodiac", "")
        trait = personality_info.get("chinese_zodiac_trait")
        all_templates.extend([
            ("chinese_zodiac", "属" + c_zodiac + "的你" + trait + "，{ing}的香味能强化这份能量"),
            ("chinese_zodiac", "{ing}与生肖" + c_zodiac + trait + "的气质相互辉映"),
            ("chinese_zodiac", "生肖" + c_zodiac + "天生" + trait + "，{ing}能为你锦上添花"),
            ("chinese_zodiac", "{ing}的香气能提升属" + c_zodiac + "者" + trait + "的魅力"),
            ("chinese_zodiac", "你属" + c_zodiac + "的" + trait + "本性，与{ing}的调性完美融合"),
            ("chinese_zodiac", "{ing}能唤醒生肖" + c_zodiac + trait + "的内在能量"),
            ("chinese_zodiac", c_zodiac + "年生人" + trait + "的福运，{ing}为你加持"),
            ("chinese_zodiac", "{ing}与属" + c_zodiac + "者" + trait + "的命格相辅相成"),
            ("chinese_zodiac", "你" + c_zodiac + "生肖" + trait + "的灵动，因{ing}而更鲜明"),
            ("chinese_zodiac", "{ing}能催旺属" + c_zodiac + "之人" + trait + "的好运气场"),
        ])

    # 打乱模板顺序，确保随机性
    random.shuffle(all_templates)

    # 为每个香味分配不同的说明
    reasons = {}
    used_templates = set()

    for code in all_codes:
        full_info = scent_map.get(code, f"{code} (专属配方)")
        ing_raw = full_info.split(" (")[1].rstrip(")") if " (" in full_info else ""

        if not ing_raw:
            continue

        # 找一个还没用过的模板
        chosen_text = None
        for idx, (source, template) in enumerate(all_templates):
            if idx not in used_templates:
                chosen_text = template.replace("{ing}", ing_raw)
                used_templates.add(idx)
                break

        # 如果所有模板都用完了，从头开始但确保不连续重复
        if not chosen_text and all_templates:
            idx = len(used_templates) % len(all_templates)
            source, template = all_templates[idx]
            chosen_text = template.replace("{ing}", ing_raw)

        if chosen_text:
            reasons[code] = chosen_text

    return reasons


def translate_scents(code_list, personality_info=None, pre_generated_reasons=None):
    """
    显示香味建议，支援显示个性匹配说明
    pre_generated_reasons: 预先生成的说明字典 {code: reason_text}
    """
    html_snippets = ""

    for code in code_list:
        full_info = scent_map.get(code, f"{code} (专属配方)")
        name = full_info.split(" (")[0] if " (" in full_info else full_info
        ing = "(" + full_info.split(" (")[1] if " (" in full_info else ""
        desc = scent_descriptions.get(code, "这款香气能优雅平衡你的内在能量。")

        # 使用预先生成的说明
        match_reason = ""
        if pre_generated_reasons and code in pre_generated_reasons:
            reason_text = pre_generated_reasons[code]
            match_reason = f"<div style='font-size: 14px; color: #6B4E3D; margin-top:8px; padding:10px; background:rgba(139,69,19,0.08); border-radius:8px;'>💫 <b>为何适合你：</b>{reason_text}</div>"

        html_snippets += f"<div style='margin-bottom:12px; padding:14px; border-radius:12px; background:rgba(255,255,255,0.6); border:1px solid #e0d5c7;'><div style='color: #8B4513; font-weight: bold; font-size: 18px;'>建议：{name}</div><div style='font-size: 14px; color: #666; margin-top:4px;'>{ing}</div><div style='font-size: 14px; color: #9E7E6B; margin-top:8px; line-height:1.6;'><i>{desc}</i></div>{match_reason}</div>"
    return html_snippets

def get_zodiac(m, d):
    signs = [(1,20,"摩羯座"),(2,19,"水瓶座"),(3,21,"双鱼座"),(4,20,"白羊座"),(5,21,"金牛座"),(6,22,"双子座"),(7,23,"巨蟹座"),(8,23,"狮子座"),(9,23,"处女座"),(10,24,"天秤座"),(11,23,"天蝎座"),(12,22,"射手座"),(12,31,"摩羯座")]
    for mm, dd, s in signs:
        if m < mm or (m == mm and d <= dd): return s
    return "摩羯座"

def get_life_num(bday):
    d = "".join(filter(str.isdigit, str(bday)))
    while len(d) > 1: d = str(sum(int(x) for x in d))
    return d

def get_chinese_zodiac(year):
    animals = ["猴", "鸡", "狗", "猪", "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊"]
    return animals[year % 12]

# ==========================================
# 分页控制逻辑 (Step-by-Step)
# ==========================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<div style="text-align: center; padding: 2.8rem 1rem 1.2rem 1rem;">
    <p style="font-family: 'Noto Serif TC', serif; font-size: 0.65rem; letter-spacing: 8px; color: #c4a484; text-transform: uppercase; margin: 0 0 0.8rem 0; opacity: 0.9;">香 香 花 園 &nbsp;·&nbsp; 香 的 秘 密</p>
    <h1 style="font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 700; color: #1a1a2e; margin: 0; line-height: 1.15; letter-spacing: 1px;">Aroma's Secret Lab</h1>
    <div style="width: 90px; height: 1px; background: linear-gradient(90deg, transparent, #c4a484, transparent); margin: 1.1rem auto;"></div>
    <p style="font-family: 'Noto Serif TC', serif; font-size: 0.75rem; letter-spacing: 4px; color: #9a8a7a; margin: 0;">專屬香氛 · 命理調配 · 感性科學</p>
</div>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1

# 进度条 (现在有 5 个步骤)
progress_map = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}
current_progress = progress_map.get(st.session_state.step, 1.0)
if st.session_state.get("taking_mbti_test", False):
    current_progress = 0.4  # 测试中也显示 40%
st.progress(current_progress)

# --- Step 1: 命运基盘 ---
if st.session_state.step == 1:
    st.subheader("Step 1: 🌌 命运基盘能量")
    st.info("AI 将根据您的出生时刻，定位星盘坐标、生肖五行与八字能量。")

    st.session_state.birthday = st.date_input(
        "📅 您的出生年月日",
        value=date(2000, 1, 1),
        min_value=date(1926, 1, 1),
        max_value=date(2026, 12, 31),
        key="step1_birthday"
    )

    # 时辰选择
    st.markdown("**🕐 您的出生时辰**")
    know_birth_hour = st.radio(
        "您知道出生时辰吗？",
        ["知道", "不知道/不确定"],
        horizontal=True,
        key="know_birth_hour"
    )

    if know_birth_hour == "知道":
        st.session_state.birth_hour = st.selectbox(
            "请选择出生时辰",
            list(HOUR_BRANCHES.keys()),
            key="step1_hour"
        )
        st.session_state.know_hour = True
    else:
        st.session_state.birth_hour = None
        st.session_state.know_hour = False
        st.caption("💡 不知道时辰也没关系，我们会用简化版计算为您分析")

    if st.button("下一步：探索性格基因 ➔"):
        st.session_state.step = 2
        st.rerun()

# --- Step 2: 性格基因 ---
elif st.session_state.step == 2:
    st.subheader("Step 2: 🧠 内在性格基因")
    st.info("性格影响香味的中调选择，这是香水的灵魂核心。")

    # 检查是否正在进行 MBTI 测试
    if st.session_state.get("taking_mbti_test", False):
        st.markdown("### 📝 MBTI 简易测试")
        st.caption("请根据直觉选择最符合你的选项（共 8 题）")

        # 初始化答案列表
        if "mbti_answers" not in st.session_state:
            st.session_state.mbti_answers = [None] * 8

        # 显示所有题目
        for i, q in enumerate(mbti_questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            options = [opt[0] for opt in q["options"]]

            # 使用 radio 让用户选择
            choice = st.radio(
                f"选择 Q{i+1}",
                options=options,
                index=None,
                key=f"mbti_q_{i}",
                label_visibility="collapsed"
            )

            # 记录答案
            if choice:
                for opt_text, opt_value in q["options"]:
                    if choice == opt_text:
                        st.session_state.mbti_answers[i] = opt_value
                        break
            st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ 返回选择 MBTI"):
                st.session_state.taking_mbti_test = False
                st.session_state.mbti_answers = [None] * 8
                st.rerun()
        with col2:
            # 检查是否所有题目都已作答
            all_answered = all(ans is not None for ans in st.session_state.mbti_answers)
            if st.button("完成测试 ✓", disabled=not all_answered):
                # 计算 MBTI 结果
                result = calculate_mbti(st.session_state.mbti_answers)
                st.session_state.mbti_choice = result
                st.session_state.taking_mbti_test = False
                st.session_state.mbti_answers = [None] * 8
                st.session_state.show_mbti_result = True  # 显示结果页面
                st.rerun()

        if not all_answered:
            st.warning("请完成所有题目后再继续")

    # 显示 MBTI 测试结果
    elif st.session_state.get("show_mbti_result", False):
        mbti_result = st.session_state.mbti_choice
        personality = mbti_personality.get(mbti_result, "独特个性")

        # MBTI 香氣類型對應
        _mbti_scent_type = {
            "INTJ": ("深邃木質系", "神秘沉穩，帶著知性的曠野氣息"),
            "INTP": ("深邃木質系", "獨立清醒，如古木靜默中的智慧"),
            "ENTJ": ("深邃木質系", "強勢自信，如大地與雪松的霸氣"),
            "ENTP": ("清新柑橘系", "思維跳躍，如柑橘迸發的靈動火花"),
            "INFJ": ("清雅花香系", "洞察深邃，如夜間綻放的白色花朵"),
            "INFP": ("清雅花香系", "浪漫詩意，如雨後庭院的輕柔花香"),
            "ENFJ": ("清雅花香系", "溫暖感染力，如牡丹盛開的華麗芬芳"),
            "ENFP": ("清新柑橘系", "充滿熱情，如陽光下的橙花與檸檬"),
            "ISTJ": ("溫暖東方系", "踏實可靠，如沉香與檀木的經典底蘊"),
            "ISFJ": ("溫暖東方系", "溫柔守護，如茉莉與玫瑰的療愈暖香"),
            "ESTJ": ("溫暖東方系", "穩重果斷，如東方香料的厚重存在感"),
            "ESFJ": ("溫暖東方系", "親切溫馨，如家中常燃的溫柔香氛"),
            "ISTP": ("清新柑橘系", "沉著冷靜，如薄荷與木質的乾淨俐落"),
            "ISFP": ("清雅花香系", "感性藝術，如野花與青草的自然之美"),
            "ESTP": ("清新柑橘系", "活力奔放，如海風帶來的清爽柑橘"),
            "ESFP": ("清新柑橘系", "開朗活潑，如熱帶水果的甜美歡快"),
        }
        _mbti_key = mbti_result.split(" ")[0]
        _scent_type, _scent_desc = _mbti_scent_type.get(_mbti_key, ("獨特混調系", "你的靈魂香氣超越分類，獨一無二"))

        st.markdown("### ✨ 測試完成！")
        st.success(f"**您的 MBTI 人格類型是：{mbti_result}**")
        st.info(f"💡 **個性特質**：{personality}")
        st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(196,164,132,0.15), rgba(212,170,125,0.1)); border: 1px solid rgba(196,164,132,0.35); border-radius: 18px; padding: 1.2rem 1.5rem; margin: 0.8rem 0; text-align: center;">
    <p style="font-size: 0.72rem; letter-spacing: 5px; color: #c4a484; margin: 0 0 0.4rem 0; font-family:'Noto Serif TC',serif;">你的靈魂香氣屬於</p>
    <p style="font-size: 1.4rem; font-weight: 700; color: #1a1a2e; margin: 0 0 0.5rem 0; font-family:'Playfair Display','Noto Serif TC',serif;">🌿 {_scent_type}</p>
    <p style="font-size: 0.82rem; color: #7a6a5a; margin: 0; line-height: 1.6;">{_scent_desc}</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("继续下一步 ➔", use_container_width=True):
            st.session_state.show_mbti_result = False
            st.session_state.step = 3
            st.rerun()

    else:
        # 正常的 MBTI 选择介面
        st.session_state.mbti_choice = st.selectbox(
            "🧠 您的 MBTI 人格",
            list(mbti_db.keys()),
            key="step2_mbti"
        )

        # 显示选择的 MBTI 个性描述
        if st.session_state.mbti_choice:
            personality = mbti_personality.get(st.session_state.mbti_choice, "独特个性")
            st.info(f"💡 **个性特质**：{personality}")

        # 新增：不知道 MBTI 的按钮
        if st.button("🤔 我不知道我的 MBTI，进行测试"):
            st.session_state.taking_mbti_test = True
            st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ 返回上一步"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("下一步：探索感官偏好 ➔"):
                st.session_state.step = 3
                st.rerun()

# --- Step 3: 感官偏好 (场景 + 季节) ---
elif st.session_state.step == 3:
    st.subheader("Step 3: 🎭 感官记忆探索")
    st.info("透过场景联想，找出最能触动你内心的香气类型。")

    # 初始化场景答案
    if "scene_answers" not in st.session_state:
        st.session_state.scene_answers = [None] * 5

    # ── 開發者快速測試按鈕（DEV_MODE = False 即隱藏）──
    if DEV_MODE:
        if st.button("⚡ [DEV] 快速測試 - 全選第一個選項", type="secondary"):
            st.session_state.scene_answers = [q["options"][0]["text"] for q in scene_questions]
            st.session_state.season_choice = list(season_scents.keys())[0]
            for i, q in enumerate(scene_questions):
                st.session_state[f"scene_q_{i}"] = q["options"][0]["text"]
            st.session_state["season_select"] = list(season_scents.keys())[0]
            st.rerun()
    # ──────────────────────────────────────────────────

    # 场景题目
    st.markdown("### 🖼️ 场景联想测试")
    st.caption("请选择最能引起你共鸣的选项")

    for i, q in enumerate(scene_questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        options = [opt["text"] for opt in q["options"]]

        choice = st.radio(
            f"场景 Q{i+1}",
            options=options,
            index=None,
            key=f"scene_q_{i}",
            label_visibility="collapsed"
        )

        if choice:
            st.session_state.scene_answers[i] = choice
        st.markdown("---")

    # 季节选择
    st.markdown("### 🌿 季节偏好")
    st.session_state.season_choice = st.radio(
        "哪个季节的氛围最让你感到舒适？",
        list(season_scents.keys()),
        index=None,
        key="season_select"
    )

    # 检查是否完成
    all_scenes_answered = all(ans is not None for ans in st.session_state.scene_answers)
    season_selected = st.session_state.season_choice is not None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ 返回上一步"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("下一步：气味场景建模 ➔", disabled=not (all_scenes_answered and season_selected)):
            st.session_state.step = 4
            st.rerun()

    if not (all_scenes_answered and season_selected):
        st.warning("请完成所有场景题目并选择喜欢的季节")

# --- Step 4: 气味建模 ---
elif st.session_state.step == 4:
    st.subheader("Step 4: 📐 气味场景建模")
    st.info("选择使用的场合与您偏好的香气结构。")
    st.session_state.occasion = st.selectbox("🏙️ 预计使用场合", list(perfume_logic.keys()), key="step4_occ")

    # 說明香氣結構模型是什麼
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(250,248,245,0.8)); border: 1px solid rgba(196,164,132,0.25); border-radius: 20px; padding: 1.4rem 1.6rem; margin: 1rem 0 0.5rem 0;">
    <p style="font-family: 'Noto Serif TC', serif; font-size: 0.95rem; font-weight: 600; color: #1a1a2e; margin: 0 0 0.8rem 0; letter-spacing: 1px;">💡 什麼是香氣結構模型？</p>
    <p style="font-size: 0.82rem; color: #6a5a4a; margin: 0 0 0.8rem 0; line-height: 1.7;">每支香水由三層香調組成，就像一場表演的序曲、主題與尾聲。選擇不同比例，會讓整體香氛給人截然不同的感受：</p>
    <div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 120px; background: linear-gradient(135deg, rgba(255,220,180,0.4), rgba(255,200,150,0.3)); border-radius: 12px; padding: 0.7rem 0.9rem; border: 1px solid rgba(255,180,100,0.3);">
            <p style="margin: 0 0 0.3rem 0; font-size: 0.78rem; font-weight: 700; color: #c4784a; letter-spacing: 1px;">🌸 前調</p>
            <p style="margin: 0; font-size: 0.75rem; color: #7a5a3a; line-height: 1.5;">噴上後最先聞到<br>持續約 15–30 分鐘</p>
        </div>
        <div style="flex: 1; min-width: 120px; background: linear-gradient(135deg, rgba(196,164,132,0.25), rgba(180,140,110,0.2)); border-radius: 12px; padding: 0.7rem 0.9rem; border: 1px solid rgba(196,164,132,0.3);">
            <p style="margin: 0 0 0.3rem 0; font-size: 0.78rem; font-weight: 700; color: #9a7a5a; letter-spacing: 1px;">🌺 中調</p>
            <p style="margin: 0; font-size: 0.75rem; color: #7a5a3a; line-height: 1.5;">香水的靈魂核心<br>持續約 2–4 小時</p>
        </div>
        <div style="flex: 1; min-width: 120px; background: linear-gradient(135deg, rgba(90,70,50,0.12), rgba(70,50,30,0.08)); border-radius: 12px; padding: 0.7rem 0.9rem; border: 1px solid rgba(90,70,50,0.2);">
            <p style="margin: 0 0 0.3rem 0; font-size: 0.78rem; font-weight: 700; color: #5a4a3a; letter-spacing: 1px;">🌿 後調</p>
            <p style="margin: 0; font-size: 0.75rem; color: #7a5a3a; line-height: 1.5;">最深沉的底韻餘香<br>可留香 6–8 小時</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.session_state.selected_model = st.selectbox("📐 選擇您的香氣結構模型", list(model_logic.keys()), key="step4_model")

    # 視覺化顯示目前選擇的比例
    _m = model_logic[st.session_state.selected_model]
    _r = _m["ratios"]
    _top, _mid, _base = int(_r[0]*100), int(_r[1]*100), int(_r[2]*100)
    st.markdown(f"""
<div style="margin: 0.3rem 0 1rem 0;">
    <div style="display: flex; border-radius: 14px; overflow: hidden; height: 44px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
        <div style="width:{_top}%; background: linear-gradient(135deg, #ffb877, #ffd4a8); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#7a4a1a;">前調 {_top}%</div>
        <div style="width:{_mid}%; background: linear-gradient(135deg, #c4a484, #b8956e); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#fff;">中調 {_mid}%</div>
        <div style="width:{_base}%; background: linear-gradient(135deg, #7a6a5a, #5a4a3a); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#e8d5b7;">後調 {_base}%</div>
    </div>
    <p style="text-align:center; font-size:0.8rem; color:#9a8a7a; margin: 0.6rem 0 0 0; font-family:'Noto Serif TC', serif;">{_m["desc"]}</p>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ 返回上一步"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🔮 启动 AI 深度分析"):
            st.session_state.step = 5
            st.rerun()

# --- Step 5: 结果展示 ---
elif st.session_state.step == 5:
    # 判断是否已经运行过载入动画
    if "done_loading" not in st.session_state:
        progress_bar = st.progress(0)
        status_text = st.empty()
        loading_steps = [
            {"text": "🌌 正在调取星盘坐标，对齐黄道十二宫脉络...", "t": 1.0},
            {"text": "🏮 读取生肖命理，计算五行能量流动...", "t": 0.8},
            {"text": "📜 推算八字命盘，分析五行盈缺...", "t": 1.0},
            {"text": "🎭 解析场景记忆，提取感官偏好...", "t": 1.2},
            {"text": "🌿 融合季节能量，调和香气频率...", "t": 0.8},
            {"text": "🧪 正在从气味库中筛选灵魂气味基因...", "t": 1.2},
            {"text": "🧠 匹配人格核心，排除分子排斥反应...", "t": 1.0},
            {"text": "🎨 计算 2026 马年专属幸运色...", "t": 0.6},
            {"text": "⚖️ 正在校准最佳 10ml 调配滴数...", "t": 0.6}
        ]
        for i, step in enumerate(loading_steps):
            status_text.markdown(f"**{step['text']}**")
            time.sleep(step['t'])
            progress_bar.progress((i + 1) / len(loading_steps))

        status_text.empty()
        progress_bar.empty()
        st.session_state.done_loading = True
        st.rerun()

    # 执行实际运算
    birthday = st.session_state.birthday
    mbti_choice = st.session_state.mbti_choice
    occasion = st.session_state.occasion
    selected_model = st.session_state.selected_model
    birth_hour = st.session_state.get("birth_hour")
    know_hour = st.session_state.get("know_hour", False)
    scene_answers = st.session_state.get("scene_answers", [])
    season_choice = st.session_state.get("season_choice", "🌸 春天 - 万物复苏，生机盎然")

    z_name = get_zodiac(birthday.month, birthday.day)
    c_zodiac = get_chinese_zodiac(birthday.year)
    c_element = zodiac_elements[c_zodiac]
    l_num = get_life_num(birthday)

    # 计算八字五行
    hour_branch = HOUR_BRANCHES.get(birth_hour) if birth_hour else None
    five_elements = calculate_five_elements(birthday, hour_branch)

    res = mbti_db[mbti_choice]
    occ_data = perfume_logic[occasion]
    model_data = model_logic[selected_model]
    z_scent = zodiac_scents.get(z_name, {"top": "前调 芳香 01", "reason": "能量引导"})
    e_data = element_scents.get(c_element, {"base": "后调 木质 08"})

    # 获取灵数资讯
    life_info = life_number_db.get(l_num, life_number_db["1"])

    # 获取幸运色
    zodiac_colors = horse_year_lucky_colors["zodiac"].get(c_zodiac, {"colors": ["金色"], "avoid": "无", "reason": ""})
    life_colors = horse_year_lucky_colors["life_number"].get(l_num, {"colors": ["白色"], "reason": ""})

    # 处理场景偏好推荐
    scene_scent_suggestions = {"top": [], "mid": [], "base": []}
    scene_tags = []
    for i, answer in enumerate(scene_answers):
        if answer:
            for opt in scene_questions[i]["options"]:
                if opt["text"] == answer:
                    scene_tags.append(opt["tag"])
                    for scent in opt["scents"]:
                        if scent.startswith("前调"):
                            scene_scent_suggestions["top"].append(scent)
                        elif scent.startswith("中调"):
                            scene_scent_suggestions["mid"].append(scent)
                        else:
                            scene_scent_suggestions["base"].append(scent)
                    break

    # 获取季节推荐
    season_data = season_scents.get(season_choice, season_scents["🌸 春天 - 万物复苏，生机盎然"])

    # 整合所有推荐：星座 + MBTI + 场景 + 季节
    # 优先顺序：场景偏好 > 季节 > 星座 > MBTI
    all_top = scene_scent_suggestions["top"] + season_data["top"] + [z_scent["top"]] + res['top']
    all_mid = scene_scent_suggestions["mid"] + season_data["mid"] + res['mid']
    all_base = scene_scent_suggestions["base"] + season_data["base"] + [e_data["base"]] + res['base']

    # 去重并限制 3 个
    final_top = list(dict.fromkeys(all_top))[:3]
    final_mid = list(dict.fromkeys(all_mid))[:3]
    final_base = list(dict.fromkeys(all_base))[:3]

    # 分析场景偏好标签
    from collections import Counter
    tag_counts = Counter(scene_tags)
    dominant_tag = tag_counts.most_common(1)[0][0] if tag_counts else "balanced"
    tag_descriptions = {
        "woody": "木质沉稳型 - 你偏好沉静内敛的氛围，适合带有木质、苔藓调的香气",
        "fresh": "清新自然型 - 你喜欢清爽通透的感觉，适合绿叶、草本调的香气",
        "floral": "花香浪漫型 - 你欣赏优雅细腻的美，适合花香、粉香调的香气",
        "citrus": "柑橘活力型 - 你喜欢明亮愉悦的能量，适合果香、柑橘调的香气",
        "oriental": "东方神秘型 - 你被温暖深邃的氛围吸引，适合东方、辛香调的香气",
        "balanced": "平衡和谐型 - 你的品味多元包容，适合层次丰富的复合香气"
    }

    # 星座个性简短描述（用于香味匹配说明）
    zodiac_personality = {
        "白羊座": "勇敢热情", "金牛座": "稳重质感", "双子座": "灵动好奇",
        "巨蟹座": "细腻温暖", "狮子座": "自信耀眼", "处女座": "细心完美",
        "天秤座": "优雅平衡", "天蝎座": "神秘深邃", "射手座": "自由冒险",
        "摩羯座": "沉稳踏实", "水瓶座": "独立创新", "双鱼座": "浪漫感性"
    }

    # 五行个性简短描述
    element_personality = {
        "水": "智慧灵性", "木": "成长生机", "火": "热情活力", "金": "刚毅精准", "土": "厚重稳定"
    }

    # 生命灵数个性简短描述
    life_num_personality = {
        "1": "领导独立", "2": "温和协调", "3": "创意表达",
        "4": "务实稳定", "5": "自由冒险", "6": "关怀责任",
        "7": "智慧探索", "8": "权威成就", "9": "博爱理想"
    }

    # 生肖个性简短描述
    chinese_zodiac_personality = {
        "鼠": "机敏聪慧", "牛": "勤奋踏实", "虎": "勇猛果敢",
        "兔": "温柔细腻", "龙": "气度非凡", "蛇": "冷静睿智",
        "马": "热情奔放", "羊": "温和善良", "猴": "灵活聪颖",
        "鸡": "勤勉自信", "狗": "忠诚正直", "猪": "真诚乐观"
    }

    # 建立个性资讯字典，传给 translate_scents
    personality_info = {
        "mbti": mbti_choice,
        "mbti_trait": mbti_personality.get(mbti_choice, "独特"),
        "zodiac": z_name,
        "zodiac_trait": zodiac_personality.get(z_name, "独特"),
        "element": c_element,
        "element_trait": element_personality.get(c_element, "平衡"),
        "life_num": l_num,
        "life_num_trait": life_num_personality.get(l_num, "独特"),
        "chinese_zodiac": c_zodiac,
        "chinese_zodiac_trait": chinese_zodiac_personality.get(c_zodiac, "独特")
    }

    # 一次性为所有香味生成不重复的说明
    all_scent_codes = final_top + final_mid + final_base
    pre_generated_reasons = generate_all_reasons(all_scent_codes, personality_info)

    # ── 驚艷揭幕動畫 ──
    st.markdown("""
<style>
@keyframes crownSpin {
    0%   { transform: rotate(-180deg) scale(0); opacity: 0; }
    60%  { transform: rotate(10deg) scale(1.12); opacity: 1; }
    80%  { transform: rotate(-4deg) scale(0.96); }
    100% { transform: rotate(0deg) scale(1); opacity: 1; }
}
@keyframes textGoldShimmer {
    0%   { background-position: -300% center; opacity: 0; }
    20%  { opacity: 1; }
    100% { background-position: 300% center; opacity: 1; }
}
@keyframes lineExpand {
    from { width: 0px; opacity: 0; }
    to   { width: 140px; opacity: 1; }
}
@keyframes subFadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.reveal-crown {
    display: inline-block;
    animation: crownSpin 1.4s cubic-bezier(0.34,1.56,0.64,1) forwards;
}
.reveal-title {
    background: linear-gradient(90deg, #8B6914, #D4AF37, #FFF0A0, #D4AF37, #8B6914);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: textGoldShimmer 3s ease forwards, textGoldShimmer 4s 3s linear infinite;
    font-family: 'Playfair Display', 'Noto Serif TC', serif;
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: 2px;
    display: block;
    margin: 0.6rem 0 0 0;
}
.reveal-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, #D4AF37, transparent);
    margin: 1rem auto;
    animation: lineExpand 1.2s 0.6s cubic-bezier(0.25,0.46,0.45,0.94) both;
}
.reveal-sub {
    font-family: 'Noto Serif TC', serif;
    font-size: 0.75rem;
    letter-spacing: 4px;
    color: #9a8a7a;
    animation: subFadeUp 0.8s 1s ease both;
}
</style>
<div style="text-align:center; padding: 2.5rem 1rem 2rem;">
    <span class="reveal-crown" style="font-size:2.8rem;">✦</span>
    <span class="reveal-title">您的專屬香氛已揭曉</span>
    <div class="reveal-line"></div>
    <span class="reveal-sub">以下配方，由命理 · 性格 · 感官共同調製</span>
</div>
""", unsafe_allow_html=True)

    # 渲染主卡片 - 放大标签字体
    st.markdown(f"""
    <div style="background: white; padding: 25px; border-radius: 20px; border: 2px solid #1a1a1a; box-shadow: 8px 8px 0px #F5F5F5; color: #333;">
        <h2 style="text-align:center; color:#8B4513;">🧬 AI 全维度专属配方</h2>
        <div style="display:flex; justify-content:center; gap:12px; margin:15px 0; flex-wrap:wrap;">
            <span style="background:#E3F2FD; padding:8px 16px; border-radius:12px; font-size:15px; font-weight:bold;">🌠 {z_name}</span>
            <span style="background:#F3E5F5; padding:8px 16px; border-radius:12px; font-size:15px; font-weight:bold;">🏮 {c_zodiac}年（{c_element}）</span>
            <span style="background:#FFF3E0; padding:8px 16px; border-radius:12px; font-size:15px; font-weight:bold;">🧠 {mbti_choice}</span>
            <span style="background:#E8F5E9; padding:8px 16px; border-radius:12px; font-size:15px; font-weight:bold;">🔢 {l_num} 号人</span>
        </div>
        <div style="font-size: 13px; color: #4A5568; line-height: 1.7; background: #FAFAFA; padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 0.5px solid #EDF2F7;">
            <p style="margin:0 0 10px 0;"><b>✨ 星座特质：</b>{zodiac_db.get(z_name, "能量引导者")}</p>
            <p style="margin:0 0 10px 0;"><b>🧠 MBTI 人格：</b>{mbti_personality.get(mbti_choice, "独特个性")}</p>
            <p style="margin:0;"><b>☯️ 五行能量：</b>{element_traits.get(c_element, "稳定底蕴")}</p>
        </div>
        <div style="background:#FFF9F0; padding:15px; border-radius:10px; border-left: 5px solid #D4AF37;">
            <p style="font-weight:bold; margin:0; font-size:16px;">【前调建议】</p>{translate_scents(final_top, personality_info, pre_generated_reasons)}
            <p style="font-weight:bold; margin:15px 0 0 0; font-size:16px;">【中调建议】</p>{translate_scents(final_mid, personality_info, pre_generated_reasons)}
            <p style="font-weight:bold; margin:15px 0 0 0; font-size:16px;">【后调建议】</p>{translate_scents(final_base, personality_info, pre_generated_reasons)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 感官偏好分析卡片
    st.write("---")
    st.subheader("🎭 感官偏好分析")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 26px 28px; border-radius: 18px;">
            <h4 style="margin:0 0 12px 0; color:#333;">🖼️ 你的香气人格</h4>
            <p style="font-size:14px; color:#444; line-height:1.9; margin:0;">{tag_descriptions.get(dominant_tag, tag_descriptions["balanced"])}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        season_emoji = season_choice.split(" ")[0]
        season_name = season_choice.split(" - ")[0].replace(season_emoji, "").strip()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 26px 28px; border-radius: 18px;">
            <h4 style="margin:0 0 12px 0; color:#333;">🌿 季節香氣偏好</h4>
            <p style="font-size:18px; font-weight:bold; color:#8B4513; margin:5px 0;">{season_emoji} {season_name}</p>
            <p style="font-size:13px; color:#666; margin:8px 0 0 0; line-height:1.7;">{season_data["desc"]}</p>
        </div>
        """, unsafe_allow_html=True)

    # 八字五行分析卡片
    st.write("---")
    st.subheader("📜 八字五行命盘分析")

    # 五行统计
    element_icons = {"金": "🪙", "木": "🌳", "水": "💧", "火": "🔥", "土": "�ite🏔️"}
    cols = st.columns(5)
    for i, (elem, count) in enumerate(five_elements["counts"].items()):
        with cols[i]:
            icon = {"金": "🪙", "木": "🌿", "水": "💧", "火": "🔥", "土": "🏔️"}[elem]
            st.metric(f"{icon} {elem}", f"{count} 个")

    # 五行分析结果
    missing_text = "、".join(five_elements["missing"]) if five_elements["missing"] else "无"
    weak_text = "、".join(five_elements["weak"]) if five_elements["weak"] else "无"
    strong_text = "、".join(five_elements["strong"]) if five_elements["strong"] else "无"

    analysis_note = "（含时辰完整分析）" if know_hour else "（简易分析，不含时辰）"

    st.markdown(f"""<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:32px 36px;border-radius:20px;color:white;margin:16px 0;line-height:2.0;">
<h4 style="margin:0 0 20px 0;font-size:1.05rem;letter-spacing:1px;">🔮 五行盈缺分析 {analysis_note}</h4>
<p style="margin:10px 0;"><b>⚠️ 缺少五行：</b>{missing_text}</p>
<p style="margin:10px 0;"><b>📉 偏弱五行：</b>{weak_text}</p>
<p style="margin:10px 0;"><b>📈 較旺五行：</b>{strong_text}</p>
<p style="margin:10px 0;"><b>🎯 日主五行：</b>{five_elements["day_master"]}</p>
</div>""", unsafe_allow_html=True)

    # 五行补充建议
    if five_elements["missing"] or five_elements["weak"]:
        need_elements = five_elements["missing"] + five_elements["weak"]
        st.markdown("#### 💡 五行补充建议")
        for elem in need_elements[:2]:  # 最多显示两个
            advice = ELEMENT_ADVICE.get(elem, {})
            st.info(f"**补{elem}**：{advice.get('补', '')}")
            st.info(f"💎 **推荐水晶**：{advice.get('水晶', '')}")

    # 生命灵数解析
    st.write("---")
    st.subheader(f"🔢 {l_num} 号人命格解析")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 15px; color: white;">
        <h4 style="margin:0 0 10px 0;">✨ {life_info['trait']}</h4>
        <p style="margin:10px 0; line-height:1.8;">{life_info['desc']}</p>
        <div style="background:rgba(255,255,255,0.2); padding:15px; border-radius:10px; margin-top:15px;">
            <p style="margin:0;"><b>🏮 2026 马年运势指引：</b></p>
            <p style="margin:10px 0 0 0; line-height:1.8;">{life_info['advice']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2026 马年幸运色
    st.write("---")
    st.subheader("🎨 2026 马年专属幸运色")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: #FFF5E6; padding: 20px; border-radius: 15px; border: 2px solid #FFB366;">
            <h4 style="margin:0 0 10px 0; color:#CC6600;">🏮 生肖「{c_zodiac}」幸运色</h4>
            <p style="font-size:20px; font-weight:bold; color:#8B4513;">{'、'.join(zodiac_colors['colors'])}</p>
            <p style="font-size:12px; color:#666; margin:10px 0 0 0;">🚫 避开：{zodiac_colors['avoid']}</p>
            <p style="font-size:11px; color:#888; margin:5px 0 0 0; line-height:1.5;"><i>{zodiac_colors['reason']}</i></p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: #F0F5FF; padding: 20px; border-radius: 15px; border: 2px solid #6699FF;">
            <h4 style="margin:0 0 10px 0; color:#3366CC;">🔢 灵数「{l_num}」幸运色</h4>
            <p style="font-size:20px; font-weight:bold; color:#333;">{'、'.join(life_colors['colors'])}</p>
            <p style="font-size:11px; color:#888; margin:10px 0 0 0; line-height:1.5;"><i>{life_colors['reason']}</i></p>
        </div>
        """, unsafe_allow_html=True)

    # 配比显示 + B: 結果頁模型切換器
    st.write("---")
    st.markdown("### 🧪 專業配比建議")
    _new_model = st.radio(
        "調整香氣結構模型，即時更新配比：",
        list(model_logic.keys()),
        index=list(model_logic.keys()).index(selected_model),
        horizontal=True,
        key="result_model_switcher"
    )
    if _new_model != selected_model:
        st.session_state.selected_model = _new_model
        selected_model = _new_model
        st.rerun()
    model_data = model_logic[selected_model]
    _r2 = model_data["ratios"]
    _t2, _m2, _b2 = int(_r2[0]*100), int(_r2[1]*100), int(_r2[2]*100)
    st.markdown(f"""
<div style="margin: 0.5rem 0 1rem 0;">
    <div style="display: flex; border-radius: 14px; overflow: hidden; height: 40px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);">
        <div style="width:{_t2}%; background: linear-gradient(135deg, #ffb877, #ffd4a8); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#7a4a1a;">前調 {_t2}%</div>
        <div style="width:{_m2}%; background: linear-gradient(135deg, #c4a484, #b8956e); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#fff;">中調 {_m2}%</div>
        <div style="width:{_b2}%; background: linear-gradient(135deg, #7a6a5a, #5a4a3a); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#e8d5b7;">後調 {_b2}%</div>
    </div>
    <p style="text-align:center; font-size:0.78rem; color:#9a8a7a; margin:0.5rem 0 0 0;">{model_data["desc"]}</p>
</div>
""", unsafe_allow_html=True)
    r, total, df = model_data["ratios"], occ_data["total_oil"], 25
    _t_ml  = round(total * r[0], 2);  _t_dr  = round(total * r[0] * df)
    _m_ml  = round(total * r[1], 2);  _m_dr  = round(total * r[1] * df)
    _b_ml  = round(total * r[2], 2);  _b_dr  = round(total * r[2] * df)
    st.markdown(f"""<div style="display:flex;gap:12px;margin:1.2rem 0;">
<div style="flex:1;text-align:center;background:linear-gradient(135deg,rgba(255,220,170,0.25),rgba(255,200,140,0.15));border:1px solid rgba(255,170,90,0.25);border-radius:18px;padding:1.4rem 0.5rem;">
  <p style="font-size:0.68rem;font-weight:700;color:#c4784a;letter-spacing:2px;margin:0 0 0.5rem;">🌸 前調</p>
  <p style="font-size:1.6rem;font-weight:700;color:#1a1a2e;margin:0;line-height:1.1;">{_t_ml}<span style="font-size:0.75rem;margin-left:3px;">ml</span></p>
  <p style="font-size:0.75rem;color:#9a8a7a;margin:0.35rem 0 0;">{_t_dr} 滴</p>
</div>
<div style="flex:1;text-align:center;background:linear-gradient(135deg,rgba(196,164,132,0.18),rgba(180,140,100,0.12));border:1px solid rgba(196,164,132,0.28);border-radius:18px;padding:1.4rem 0.5rem;">
  <p style="font-size:0.68rem;font-weight:700;color:#9a7a5a;letter-spacing:2px;margin:0 0 0.5rem;">🌺 中調</p>
  <p style="font-size:1.6rem;font-weight:700;color:#1a1a2e;margin:0;line-height:1.1;">{_m_ml}<span style="font-size:0.75rem;margin-left:3px;">ml</span></p>
  <p style="font-size:0.75rem;color:#9a8a7a;margin:0.35rem 0 0;">{_m_dr} 滴</p>
</div>
<div style="flex:1;text-align:center;background:linear-gradient(135deg,rgba(90,65,45,0.1),rgba(70,50,30,0.06));border:1px solid rgba(90,65,45,0.18);border-radius:18px;padding:1.4rem 0.5rem;">
  <p style="font-size:0.68rem;font-weight:700;color:#5a4a3a;letter-spacing:2px;margin:0 0 0.5rem;">🌿 後調</p>
  <p style="font-size:1.6rem;font-weight:700;color:#1a1a2e;margin:0;line-height:1.1;">{_b_ml}<span style="font-size:0.75rem;margin-left:3px;">ml</span></p>
  <p style="font-size:0.75rem;color:#9a8a7a;margin:0.35rem 0 0;">{_b_dr} 滴</p>
</div>
</div>""", unsafe_allow_html=True)

    # ── 一次性爆炸動畫（只在結果第一次出現時播放）──
    if "result_burst_done" not in st.session_state:
        st.session_state.result_burst_done = True
        _burst_html = """<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:linear-gradient(135deg,#faf8ff 0%,#f5f0e8 100%);overflow:hidden;height:260px;display:flex;align-items:center;justify-content:center;font-family:serif;}
#wrap{position:relative;width:1px;height:1px;}
.p{position:absolute;top:0;left:0;pointer-events:none;display:flex;align-items:center;justify-content:center;}
.tagline{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:1.05rem;color:#c4a484;letter-spacing:5px;white-space:nowrap;opacity:0;animation:tFade 2.2s 1.2s ease forwards;}
@keyframes tFade{0%{opacity:0;transform:translate(-50%,-55%);}60%{opacity:1;}100%{opacity:0.85;transform:translate(-50%,-50%);}}
</style></head><body>
<div id="wrap"><div class="tagline">✦ 您的配方已揭曉 ✦</div></div>
<script>
const syms=["✦","✧","✿","❋","❀","✾","✱","◈","⊹","✲","❃","❊","·","⁕"];
const cols=["#D4AF37","#C4A484","#E8D5A0","#FFE082","#F5CBA7","#FAD7A0","#FDEBD0","#FFF0A0","#E8C4A0","#f5d5b0"];
const wrap=document.getElementById("wrap");
const N=42;
for(let i=0;i<N;i++){
  const ang=(i/N)*2*Math.PI;
  const dist=70+Math.random()*140;
  const tx=Math.cos(ang)*dist, ty=Math.sin(ang)*dist;
  const rot=Math.random()*720-360;
  const sz=0.7+Math.random()*1.4;
  const dur=1.6+Math.random()*1.6;
  const dl=Math.random()*0.5;
  const col=cols[i%cols.length];
  const sym=syms[i%syms.length];
  const el=document.createElement("span");
  el.className="p";
  el.textContent=sym;
  el.style.cssText="color:"+col+";font-size:"+sz+"rem;animation:b"+i+" "+dur+"s "+dl+"s ease-out forwards;";
  const st=document.createElement("style");
  st.textContent="@keyframes b"+i+"{0%{transform:translate(-50%,-50%) scale(0) rotate(0deg);opacity:1;}15%{opacity:1;}100%{transform:translate(calc(-50% + "+tx+"px),calc(-50% + "+ty+"px)) scale(1.1) rotate("+rot+"deg);opacity:0;}}";
  document.head.appendChild(st);
  wrap.appendChild(el);
}
</script></body></html>"""
        components.html(_burst_html, height=260)
    # ── 選香互動：客人從推薦中各選一款 ─────────────
    st.write("---")
    st.markdown("""
<div style="text-align:center; padding:0.5rem 0 1.2rem;">
    <p style="font-size:0.68rem; letter-spacing:6px; color:#c4a484; margin:0 0 0.3rem 0;">PERSONALIZE YOUR FORMULA</p>
    <p style="font-family:'Playfair Display','Noto Serif TC',serif; font-size:1.3rem; font-weight:700; color:#1a1a2e; margin:0;">打造你的專屬配方</p>
    <p style="font-size:0.8rem; color:#9a8a7a; margin:0.5rem 0 0 0;">從以下推薦中，每個調性各挑一款，完成你的配方</p>
</div>
""", unsafe_allow_html=True)

    # ── 初始化選香索引 ──
    for _sk in ["sel_top", "sel_mid", "sel_base"]:
        if _sk not in st.session_state:
            st.session_state[_sk] = 0

    def _card_sel(codes, state_key, label_color, accent_bg):
        cols = st.columns(len(codes))
        cur = st.session_state.get(state_key, 0)
        for i, code in enumerate(codes):
            full = scent_map.get(code, code)
            nm = full.split(" (")[0] if " (" in full else full
            ig = full.split("(")[1].rstrip(")") if "(" in full else ""
            dc = scent_descriptions.get(code, "")
            dc_s = dc[:55] + "…" if len(dc) > 55 else dc
            is_sel = (i == cur)
            with cols[i]:
                if is_sel:
                    st.markdown(f"""
<div style="border:2px solid {label_color};background:{accent_bg};border-radius:18px;padding:1.15rem 0.9rem 0.8rem;text-align:center;box-shadow:0 10px 28px rgba(196,164,132,0.3);transform:translateY(-6px);min-height:175px;">
    <div style="font-size:1.05rem;color:{label_color};margin-bottom:0.35rem;font-weight:700;">✦</div>
    <div style="font-weight:700;color:#1a1a2e;font-size:0.9rem;line-height:1.3;margin-bottom:0.3rem;">{nm}</div>
    <div style="font-size:0.63rem;color:#9a8a7a;margin-bottom:0.45rem;">{ig}</div>
    <div style="font-size:0.69rem;color:#6a5a4a;font-style:italic;line-height:1.65;">{dc_s}</div>
</div>""", unsafe_allow_html=True)
                    st.button("✦ 已選", key=f"{state_key}_{i}", use_container_width=True, type="primary")
                else:
                    st.markdown(f"""
<div style="border:1px solid rgba(196,164,132,0.2);background:rgba(255,255,255,0.78);border-radius:18px;padding:1.15rem 0.9rem 0.8rem;text-align:center;box-shadow:0 3px 14px rgba(0,0,0,0.05);min-height:175px;">
    <div style="font-size:1.05rem;color:transparent;margin-bottom:0.35rem;">·</div>
    <div style="font-weight:700;color:#1a1a2e;font-size:0.9rem;line-height:1.3;margin-bottom:0.3rem;">{nm}</div>
    <div style="font-size:0.63rem;color:#9a8a7a;margin-bottom:0.45rem;">{ig}</div>
    <div style="font-size:0.69rem;color:#6a5a4a;font-style:italic;line-height:1.65;">{dc_s}</div>
</div>""", unsafe_allow_html=True)
                    if st.button("選擇", key=f"{state_key}_{i}", use_container_width=True):
                        st.session_state[state_key] = i
                        st.rerun()

    st.markdown('<p style="font-size:0.75rem;font-weight:700;color:#c4784a;letter-spacing:2px;margin:0 0 0.5rem;">🌸 前調　點選你喜歡的</p>', unsafe_allow_html=True)
    _card_sel(final_top, "sel_top", "#c4784a", "rgba(255,210,160,0.25)")
    st.write("")
    st.markdown('<p style="font-size:0.75rem;font-weight:700;color:#9a7a5a;letter-spacing:2px;margin:0 0 0.5rem;">🌺 中調　點選你喜歡的</p>', unsafe_allow_html=True)
    _card_sel(final_mid, "sel_mid", "#9a7a5a", "rgba(196,164,132,0.15)")
    st.write("")
    st.markdown('<p style="font-size:0.75rem;font-weight:700;color:#5a4a3a;letter-spacing:2px;margin:0 0 0.5rem;">🌿 後調　點選你喜歡的</p>', unsafe_allow_html=True)
    _card_sel(final_base, "sel_base", "#5a4a3a", "rgba(90,65,45,0.09)")

    _chosen_top  = final_top [st.session_state.get("sel_top",  0)]
    _chosen_mid  = final_mid [st.session_state.get("sel_mid",  0)]
    _chosen_base = final_base[st.session_state.get("sel_base", 0)]

    _cn_top  = scent_map.get(_chosen_top,  _chosen_top ).split(" (")[0]
    _cn_mid  = scent_map.get(_chosen_mid,  _chosen_mid ).split(" (")[0]
    _cn_base = scent_map.get(_chosen_base, _chosen_base).split(" (")[0]

    # ── G + A: 富內容報告卡（含描述）+ 下載圖片 + 列印 ──
    st.write("---")
    st.markdown("#### 🪄 你的專屬香氛報告卡")

    # 取得每個選擇香氣的完整資料
    def _gi(code):
        full = scent_map.get(code, code)
        nm   = full.split(" (")[0] if " (" in full else full
        ig   = full.split("(")[1].rstrip(")") if "(" in full else ""
        dc   = scent_descriptions.get(code, "這款香氣能優雅平衡你的內在能量。")
        wy   = pre_generated_reasons.get(code, "")
        # 簡單 HTML 轉義
        def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
        return esc(nm), esc(ig), esc(dc), esc(wy)

    _tnm,_tig,_tdc,_twy = _gi(_chosen_top)
    _mnm,_mig,_mdc,_mwy = _gi(_chosen_mid)
    _bnm,_big,_bdc,_bwy = _gi(_chosen_base)
    _rs  = model_data["ratios"]
    _r0,_r1,_r2 = int(_rs[0]*100), int(_rs[1]*100), int(_rs[2]*100)
    _mbti_s = mbti_choice.split(" ")[0]

    def _why_block(w, bg):
        if not w: return ""
        return f'<div style="font-size:0.71rem;color:#7a6a5a;line-height:1.65;margin-top:0.55rem;padding:0.55rem 0.75rem;background:{bg};border-radius:9px;">💫 {w}</div>'

    _card_comp = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Noto+Serif+TC:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:#f0ece4;padding:18px;font-family:'Noto Serif TC',serif;}}
#card{{background:linear-gradient(145deg,#faf7f2,#f5f0e8);border:1px solid rgba(196,164,132,0.45);border-radius:22px;padding:1.8rem 2rem;max-width:520px;margin:0 auto;box-shadow:0 10px 36px rgba(196,164,132,0.22);}}
.b-top{{text-align:center;font-size:0.58rem;letter-spacing:7px;color:#c4a484;margin-bottom:0.4rem;}}
.b-title{{text-align:center;font-family:'Playfair Display',serif;font-size:1.45rem;font-weight:700;color:#1a1a2e;}}
.divider{{width:60px;height:1px;background:linear-gradient(90deg,transparent,#c4a484,transparent);margin:0.75rem auto 1rem;}}
.info-t{{width:100%;font-size:0.77rem;border-collapse:collapse;margin-bottom:1.1rem;}}
.info-t td{{padding:3px 0;}}
.il{{color:#9a8a7a;width:28%;}}
.iv{{color:#1a1a2e;font-weight:600;}}
.sec{{font-size:0.65rem;letter-spacing:3px;color:#c4a484;margin:0.5rem 0 0.9rem;}}
.sb{{margin-bottom:1rem;padding:1rem 1.1rem;border-radius:14px;border:1px solid;}}
.st{{background:rgba(255,215,170,0.22);border-color:rgba(255,170,90,0.22);}}
.sm{{background:rgba(196,164,132,0.13);border-color:rgba(196,164,132,0.22);}}
.sb2{{background:rgba(80,60,40,0.06);border-color:rgba(80,60,40,0.13);}}
.nl{{font-size:0.68rem;font-weight:700;letter-spacing:1px;margin-bottom:0.3rem;}}
.sn{{font-size:0.98rem;font-weight:700;color:#1a1a2e;}}
.si{{font-size:0.7rem;color:#9a8a7a;margin:0.15rem 0 0.45rem;}}
.sd{{font-size:0.74rem;color:#5a4a3a;line-height:1.75;font-style:italic;}}
.rbar{{display:flex;border-radius:10px;overflow:hidden;height:26px;margin:1.1rem 0 0.35rem;}}
.rt{{background:linear-gradient(135deg,#ffb877,#ffd4a8);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#7a4a1a;}}
.rm{{background:linear-gradient(135deg,#c4a484,#b8956e);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;}}
.rb{{background:linear-gradient(135deg,#7a6a5a,#5a4a3a);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#e8d5b7;}}
.mname{{text-align:center;font-size:0.62rem;color:#9a8a7a;margin:0.3rem 0 0;}}
.footer{{text-align:center;font-size:0.6rem;color:#c4a484;letter-spacing:3px;margin-top:1.2rem;}}
.btns{{display:flex;gap:10px;max-width:520px;margin:14px auto 0;}}
.btn{{flex:1;padding:13px 0;border:1px solid rgba(196,164,132,0.5);border-radius:14px;background:linear-gradient(135deg,#faf8ff,#fff);font-family:'Noto Serif TC',serif;font-size:13px;font-weight:600;color:#1a1a2e;cursor:pointer;letter-spacing:1px;transition:all .3s;}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(196,164,132,0.2);}}
.btn-gold{{background:linear-gradient(135deg,#c4a484,#b8956e);color:#fff;border:none;}}
@media print{{.btns{{display:none!important;}}body{{background:white;padding:0;}}#card{{box-shadow:none;border:1px solid #ddd;}}}}
</style></head><body>
<div id="card">
  <p class="b-top">香 香 花 園 · 香 的 秘 密</p>
  <p class="b-title">Aroma's Secret Lab</p>
  <div class="divider"></div>
  <table class="info-t">
    <tr><td class="il">星座</td><td class="iv">{z_name}</td><td class="il">生肖</td><td class="iv">屬{c_zodiac}</td></tr>
    <tr><td class="il">MBTI</td><td class="iv">{_mbti_s}</td><td class="il">靈數</td><td class="iv">{l_num} 號</td></tr>
  </table>
  <p class="sec">✦ 專屬香氣配方</p>
  <div class="sb st">
    <p class="nl" style="color:#c4784a;">🌸 前調</p>
    <p class="sn">{_tnm}</p>
    <p class="si">（{_tig}）</p>
    <p class="sd">{_tdc}</p>
    {_why_block(_twy,"rgba(255,200,140,0.18)")}
  </div>
  <div class="sb sm">
    <p class="nl" style="color:#9a7a5a;">🌺 中調</p>
    <p class="sn">{_mnm}</p>
    <p class="si">（{_mig}）</p>
    <p class="sd">{_mdc}</p>
    {_why_block(_mwy,"rgba(196,164,132,0.14)")}
  </div>
  <div class="sb sb2">
    <p class="nl" style="color:#5a4a3a;">🌿 後調</p>
    <p class="sn">{_bnm}</p>
    <p class="si">（{_big}）</p>
    <p class="sd">{_bdc}</p>
    {_why_block(_bwy,"rgba(90,70,50,0.08)")}
  </div>
  <div class="rbar">
    <div class="rt" style="width:{_r0}%">前 {_r0}%</div>
    <div class="rm" style="width:{_r1}%">中 {_r1}%</div>
    <div class="rb" style="width:{_r2}%">後 {_r2}%</div>
  </div>
  <p class="mname">｛{selected_model}｝</p>
  <p class="footer">✦ &nbsp; 每一滴都是你的故事 &nbsp; ✦</p>
</div>
<div class="btns">
  <button class="btn btn-gold" onclick="dlCard()">📥 下載圖片</button>
  <button class="btn" onclick="window.print()">🖨️ 列印 / 儲存 PDF</button>
</div>
<script>
function dlCard(){{
  const btns=document.querySelector('.btns');
  btns.style.display='none';
  html2canvas(document.getElementById('card'),{{scale:2,backgroundColor:'#f0ece4',useCORS:true,logging:false}}).then(c=>{{
    btns.style.display='flex';
    const a=document.createElement('a');
    a.download='aroma_secret_lab.png';
    a.href=c.toDataURL('image/png');
    a.click();
  }}).catch(()=>{{btns.style.display='flex';}});
}}
</script>
</body></html>"""

    components.html(_card_comp, height=920, scrolling=True)
    st.caption("💡 點「下載圖片」儲存 PNG · 點「列印」可輸出 PDF 或實體列印")
    st.write("---")
    if st.button("🔄 重新开始分析"):
        st.session_state.clear()
        st.rerun()
