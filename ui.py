# ==============================
# IMPORTS
# ==============================
import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Personality AI",
    page_icon="🧠",
    layout="wide"
)

# ==============================
# BACKGROUND STYLE
# ==============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
}
h1, h2, h3 {
    color: #eafcff;
}
.stButton > button {
    background: linear-gradient(90deg, #00f5d4, #00bbf9);
    color: #003049;
    border-radius: 30px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("<h1 style='text-align:center;'>🧠 Personality AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Discover your personality • Trading-card style ✨</p>",
    unsafe_allow_html=True
)
st.divider()

# ==============================
# FASTAPI URL
# ==============================
API_URL = "https://personality-predictor-7xm4.onrender.com"

# ==============================
# SLIDER HELPER
# ==============================
def vibe_slider(label):
    return st.slider(label, 0, 10, 5, step=1)

# ==============================
# INPUTS (12 CLEAN SLIDERS)
# ==============================
c1, c2, c3 = st.columns(3)

with c1:
    social_energy = vibe_slider("⚡ Social Energy")
    creativity = vibe_slider("🎨 Creativity")
    empathy = vibe_slider("❤️ Empathy")
    emotional_stability = vibe_slider("🧘 Emotional Stability")

with c2:
    talkativeness = vibe_slider("🗣️ Talkativeness")
    curiosity = vibe_slider("🧠 Curiosity")
    leadership = vibe_slider("👑 Leadership")
    planning = vibe_slider("📋 Planning")

with c3:
    group_comfort = vibe_slider("👥 Group Comfort")
    deep_reflection = vibe_slider("🤔 Deep Reflection")
    adventurousness = vibe_slider("🏔️ Adventurousness")
    stress_handling = vibe_slider("🛡️ Stress Handling")

st.divider()

# ==============================
# PERSONALITY INSIGHTS
# ==============================
def one_liner(p):
    avg = (
        p["social_energy"] +
        p["creativity"] +
        p["leadership"] +
        p["empathy"] +
        p["adventurousness"] +
        p["stress_handling"]
    ) / 6

    if avg >= 7:
        return "Expressive, emotionally aware, and experience-driven — certified main-character energy ✨"
    elif avg >= 5:
        return "Balanced, thoughtful, and socially adaptive with calm confidence ⚖️"
    else:
        return "Low-key, introspective, and emotionally grounded — quiet depth 🌙"

def five_points(p):
    return [
        "People recharge your energy ⚡" if p["social_energy"] > 6 else "You value selective connections 🌙",
        "Creative ideas flow naturally 🎨" if p["creativity"] > 6 else "Logic and structure guide you 📐",
        "Emotionally perceptive and empathetic ❤️" if p["empathy"] > 6 else "Emotionally steady and controlled 🧊",
        "Leadership comes naturally 👑" if p["leadership"] > 6 else "You stabilize teams 🤝",
        "You seek experiences over comfort 🏔️" if p["adventurousness"] > 6 else "You prefer familiarity 🏡"
    ]

# ==============================
# RARITY LOGIC
# ==============================
def get_rarity(score):
    if score >= 80:
        return "LEGENDARY", (255, 215, 0)
    elif score >= 60:
        return "RARE", (0, 255, 200)
    else:
        return "COMMON", (180, 180, 180)

# ==============================
# PERSONALITY COLOR THEMES
# ==============================
def personality_theme(personality):
    themes = {
        "Extrovert": ((255, 90, 90), (255, 180, 150)),
        "Introvert": ((90, 130, 255), (170, 210, 255)),
        "Ambivert": ((0, 200, 170), (130, 255, 230)),
    }
    return themes.get(personality, ((120, 120, 120), (200, 200, 200)))

# ==============================
# TEXT WRAPPING
# ==============================
def draw_wrapped_text(draw, text, x, y, font, max_width, gap=6):
    words = text.split()
    line = ""
    for word in words:
        test = line + word + " "
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w <= max_width:
            line = test
        else:
            draw.text((x, y), line, fill=(235, 235, 235), font=font)
            y += font.size + gap
            line = word + " "
    if line:
        draw.text((x, y), line, fill=(235, 235, 235), font=font)
        y += font.size + gap
    return y

# ==============================
# ANIMATED GIF CARD
# ==============================
def generate_animated_gif_card(personality, score, summary, points):
    W, H = 900, 1300
    frames = []

    rarity, rarity_color = get_rarity(score)
    bg1, bg2 = personality_theme(personality)

    try:
        title_f = ImageFont.truetype("arialbd.ttf", 52)
        heading_f = ImageFont.truetype("arialbd.ttf", 36)
        text_f = ImageFont.truetype("arial.ttf", 28)
        small_f = ImageFont.truetype("arial.ttf", 22)
    except:
        title_f = heading_f = text_f = small_f = ImageFont.load_default()

    for glow in range(30, 110, 15):
        img = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(img)

        for y in range(H):
            mix = y / H
            r = int(bg1[0] * (1 - mix) + bg2[0] * mix)
            g = int(bg1[1] * (1 - mix) + bg2[1] * mix)
            b = int(bg1[2] * (1 - mix) + bg2[2] * mix)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        glow_layer = Image.new("RGBA", (W - 40, H - 40), (*rarity_color, glow))
        img.paste(glow_layer, (20, 20), glow_layer)

        card = Image.new("RGBA", (W - 80, H - 80), (18, 38, 48, 240))
        img.paste(card, (40, 40), card)

        draw = ImageDraw.Draw(img)

        x, y = 70, 60
        max_w = W - 160

        draw.text((x + 180, y), "PERSONALITY AI", fill=(235, 255, 255), font=title_f)
        y += 80

        badge = Image.new("RGBA", (320, 60), (*rarity_color, 210))
        img.paste(badge, (x, y), badge)
        draw.text((x + 20, y + 15), personality.upper(), fill=(15, 30, 40), font=heading_f)
        y += 90

        draw.text((x, y), "POWER", fill=(200, 255, 245), font=small_f)
        y += 26
        draw.text((x, y), f"{score}/100", fill=rarity_color, font=heading_f)
        y += 65

        draw.text((x, y), "DESCRIPTION", fill=(200, 255, 245), font=small_f)
        y += 30
        y = draw_wrapped_text(draw, summary, x, y, text_f, max_w)
        y += 25

        draw.text((x, y), "ABILITIES", fill=(200, 255, 245), font=heading_f)
        y += 45

        for p in points:
            y = draw_wrapped_text(draw, f"• {p}", x + 10, y, text_f, max_w)
            y += 6

        draw.text((x, H - 80), f"RARITY: {rarity}", fill=rarity_color, font=small_f)
        draw.text((W - 260, H - 80), "Made by Om", fill=(200, 255, 255), font=small_f)

        frames.append(img)

    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0
    )
    buffer.seek(0)
    return buffer

# ==============================
# BUTTON + PREDICTION
# ==============================
if st.button("✨ Reveal My Personality"):

    payload = {
        "social_energy": social_energy,
        "alone_time_preference": 10 - social_energy,
        "talkativeness": talkativeness,
        "deep_reflection": deep_reflection,
        "group_comfort": group_comfort,
        "party_liking": social_energy,
        "listening_skill": empathy,
        "empathy": empathy,
        "creativity": creativity,
        "organization": curiosity,
        "leadership": leadership,
        "risk_taking": adventurousness,
        "public_speaking_comfort": talkativeness,
        "curiosity": curiosity,
        "routine_preference": 10 - adventurousness,
        "excitement_seeking": adventurousness,
        "friendliness": empathy,
        "emotional_stability": emotional_stability,
        "planning": planning,
        "spontaneity": adventurousness,
        "adventurousness": adventurousness,
        "reading_habit": curiosity,
        "sports_interest": adventurousness,
        "online_social_usage": social_energy,
        "travel_desire": adventurousness,
        "gadget_usage": curiosity,
        "work_style_collaborative": group_comfort,
        "decision_speed": leadership,
        "stress_handling": stress_handling
    }

    response = requests.post(API_URL, json=payload)
    if response.status_code != 200:
    st.error("❌ Prediction API error")
    st.json(response.json())
    st.stop()

data = response.json()

if "predicted_personality" not in data:
    st.error("❌ Invalid API response")
    st.json(data)
    st.stop()

personality = data["predicted_personality"]


    score = round(
        (social_energy + creativity + leadership + adventurousness + talkativeness) / 5 * 10,
        1
    )

    summary = one_liner(payload)
    points = five_points(payload)

    st.success(f"🎯 Predicted Personality: {personality}")
    st.write(summary)

    gif_card = generate_animated_gif_card(personality, score, summary, points)

    st.download_button(
        "🎴 Download Animated Personality Card",
        gif_card,
        "personality_card.gif",
        "image/gif"
    )


