# ==============================
# IMPORTS
# ==============================
import streamlit as st
import streamlit.components.v1 as components
import random
import base64
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Personality AI",
    page_icon="🧠",
    layout="centered"
)

# ==============================
# GLOBAL STYLE
# ==============================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f2027, #000);
    color: white;
}
.stButton>button {
    background: linear-gradient(90deg, #00ffd5, #00aaff);
    color: black;
    border-radius: 30px;
    font-weight: bold;
    padding: 10px 24px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("<h1 style='text-align:center;'>🧠 Personality AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Anime-style personality cards ✨</p>", unsafe_allow_html=True)
st.divider()

# ==============================
# USER NAME
# ==============================
name = st.text_input("Your Name", "Om")

# ==============================
# INPUTS (12 SLIDERS)
# ==============================
c1, c2, c3 = st.columns(3)

with c1:
    social_energy = st.slider("⚡ Social Energy", 0, 10, 5)
    empathy = st.slider("❤️ Empathy", 0, 10, 5)
    curiosity = st.slider("🧠 Curiosity", 0, 10, 5)
    stress_handling = st.slider("🛡️ Stress Handling", 0, 10, 5)

with c2:
    talkativeness = st.slider("🗣️ Talkativeness", 0, 10, 5)
    creativity = st.slider("🎨 Creativity", 0, 10, 5)
    planning = st.slider("📋 Planning", 0, 10, 5)
    emotional_stability = st.slider("🧘 Emotional Stability", 0, 10, 5)

with c3:
    group_comfort = st.slider("👥 Group Comfort", 0, 10, 5)
    leadership = st.slider("👑 Leadership", 0, 10, 5)
    adventurousness = st.slider("🏔️ Adventurousness", 0, 10, 5)
    deep_reflection = st.slider("🤔 Deep Reflection", 0, 10, 5)

# ==============================
# PERSONALITY LOGIC
# ==============================
def get_personality():
    avg = (
        social_energy + talkativeness + leadership +
        empathy + group_comfort + adventurousness
    ) / 6

    if avg >= 7:
        return "Extrovert"
    elif avg >= 5:
        return "Ambivert"
    else:
        return "Introvert"

def one_liner():
    return "Balanced, adaptive, and quietly confident — certified main-character energy ⚖️"

def five_points():
    return [
        "Selective but meaningful connections 🌙",
        "Creative yet grounded thinking 🎨",
        "Emotionally calm under pressure 🧊",
        "Reliable team presence 🤝",
        "Comfortable with calculated risks 🏔️"
    ]

# ==============================
# STATS (0–100)
# ==============================
def compute_stats():
    return {
        "Power": int((leadership + social_energy) / 2 * 10),
        "Creativity": int((creativity + curiosity) / 2 * 10),
        "Control": int((planning + emotional_stability) / 2 * 10),
        "Chaos": int(adventurousness * 10),
        "Empathy": int((empathy + group_comfort) / 2 * 10),
    }

# ==============================
# RARITY BORDER
# ==============================
def get_border_color(score):
    if score >= 85:
        return (255, 215, 0)   # Gold
    elif score >= 65:
        return (0, 200, 255)   # Cyan
    else:
        return (160, 160, 160) # Gray

# ==============================
# CHARACTER IMAGE
# ==============================
def get_character_image():
    path = Path("assets/characters")
    images = list(path.glob("*.png"))

    if not images:
        return None

    return random.choice(images)

def image_to_base64(img_path):
    encoded = base64.b64encode(img_path.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"

# ==============================
# HTML CARD (PREVIEW)
# ==============================
def get_card_html(name, personality, score, summary, points, stats, img_path):
    image_data = image_to_base64(img_path) if img_path else ""

    bars = ""
    for stat, value in stats.items():
        bars += f"""
        <div class="stat">
            <span>{stat}</span>
            <div class="bar-bg">
                <div class="bar-fill" style="width:{value}%"></div>
            </div>
            <span>{value}</span>
        </div>
        """

    abilities = "".join([f"<li>{p}</li>" for p in points])

    return f"""
<style>
.card {{
    width: 380px;
    height: 700px;
    padding: 18px;
    border-radius: 28px;
    background: #0b0b0b;
    color: white;
    border: 6px solid #666;
}}

.character img {{
    width: 100%;
    height: 240px;
    object-fit: cover;
    border-radius: 16px;
}}

.stat {{
    display: grid;
    grid-template-columns: 70px 1fr 30px;
    gap: 6px;
    font-size: 0.7rem;
}}

.bar-bg {{
    background: rgba(255,255,255,0.15);
    height: 8px;
    border-radius: 6px;
}}

.bar-fill {{
    height: 100%;
    background: white;
    border-radius: 6px;
}}
</style>

<div class="card">
    <h3>{name} · {personality} · HP {score}</h3>
    <div class="character"><img src="{image_data}"></div>
    {bars}
    <p>{summary}</p>
    <ul>{abilities}</ul>
    <small>PERSONALITY AI · Made by Om</small>
</div>
"""

# ==============================
# PNG CARD GENERATION
# ==============================
def generate_png_card(name, personality, score, summary, points, stats, img_path):
    W, H = 1200, 2000
    img = Image.new("RGB", (W, H), (10, 10, 10))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 60)
        text_font = ImageFont.truetype("arial.ttf", 40)
    except:
        title_font = text_font = ImageFont.load_default()

    border_color = get_border_color(score)
    draw.rectangle([0, 0, W, H], outline=border_color, width=24)

    draw.text((60, 40), f"{name} · {personality} · HP {score}", fill="white", font=title_font)

    if img_path:
        char = Image.open(img_path).convert("RGBA").resize((900, 900))
        img.paste(char, (150, 120), char)

    y = 1100
    for stat, value in stats.items():
        draw.text((120, y), stat, fill="white", font=text_font)
        draw.rectangle([320, y+15, 900, y+35], fill=(40,40,40))
        draw.rectangle([320, y+15, 320 + int(580 * value / 100), y+35], fill=border_color)
        draw.text((930, y), str(value), fill="white", font=text_font)
        y += 70

    draw.text((120, y+20), summary, fill="white", font=text_font)
    # ==============================
    # WATERMARK (BOTTOM RIGHT)
    # ==============================
    watermark_text = "PERSONALITY AI · Made by Om"

    try:
        watermark_font = ImageFont.truetype("arial.ttf", 28)
    except:
        watermark_font = ImageFont.load_default()

    text_w, text_h = draw.textbbox((0, 0), watermark_text, font=watermark_font)[2:]
    draw.text(
        (W - text_w - 40, H - text_h - 30),
        watermark_text,
        fill=(180, 180, 180),
        font=watermark_font
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# ==============================
# ACTION
# ==============================
if st.button("✨ Reveal My Personality"):
    personality = get_personality()
    score = int((social_energy + leadership + creativity + adventurousness) / 4 * 10)
    stats = compute_stats()
    img_path = get_character_image()

    components.html(
        get_card_html(
            name,
            personality,
            score,
            one_liner(),
            five_points(),
            stats,
            img_path
        ),
        height=760,
        scrolling=False
    )

    png = generate_png_card(
        name,
        personality,
        score,
        one_liner(),
        five_points(),
        stats,
        img_path
    )

    st.download_button(
        "⬇️ Download Personality Card (PNG)",
        png,
        file_name="personality_card.png",
        mime="image/png"
    )
