import streamlit as st

st.set_page_config(page_title="Good Morning", layout="centered")

# ---------- THEME / CSS ----------
st.markdown("""
<style>
.block-container { padding-top: 1.25rem; padding-bottom: 2rem; max-width: 900px; }
.card {
  background: #ffffff; border-radius: 16px; padding: 18px 18px;
  box-shadow: 0 10px 22px rgba(0,0,0,0.06); border: 1px solid #eee;
  margin-bottom: 14px;
}
h1, h2, h3 { line-height: 1.2; }
.stButton>button { border-radius: 12px; font-weight: 600; padding: .6rem 1.2rem; }
div.stMetric { background: #ffffff; border-radius: 14px; padding: 10px 12px; box-shadow: 0 6px 14px rgba(0,0,0,.06); }
.small-hint{ color:#6b7280; font-size:.9rem; margin-top:-6px; }
.hr{ height:1px; background:#eee; margin: 6px 0 14px; }
</style>
""", unsafe_allow_html=True)

# ---------- TEXT DICTS ----------
sleep_text = {
    'perfect': 'วันนี้จะเป็นที่สดชื่นของคุณ',
    'good': 'พลังงานเพียงพอสำหรับวันหนึ่ง',
    'fair': 'แต่ควรปรับเวลานอนให้เพิ่มในคืนถัดไป',
    'poor': 'พักผ่อนด่วน',
    'none': 'ควรพักได้แล้ว',
    'over': 'พลังงานเกินร้อยแล้ว'
}
meal_text = {
    3: 'ดีสำหรับคุณแล้ว',
    2: 'มันอาจจะเพียงพอสำหรับคุณในวันนั้น',
    1: 'วันต่อไปก็อย่าลืมหาอะไรทานเพิ่มให้เพียงพอด้วยละ',
    0: 'คุณควรได้รับประทานอาหารสักมื้อให้เพียงพอ ต่อร่างกาย'
}
day_text = {
    'le13': 'ถือว่าคุณได้ชีวิตเต็มที่แล้วในวันนี้ ไม่แปลกที่จะเหนื่อย อาจจะถึงเวลาพักผ่อน',
    'gt18': 'ถือว่าคุณได้ชีวิตได้มากแล้ว หาเวลาพักได้แล้ว',
    'zero_to_three': 'พรุ่งนี้ได้เวลาออกไปใช้ชีวิตแล้ว',
    'mid': 'คุณอย่าลืมหาเวลาพักด้วยละ (14-18 ชม.)'
}
ERROR_MSG = "Error: Unknown data. Please, you better go to sleep."

# ---------- HELPERS ----------
def parse_hhmm(s: str):
    """รับ '23:45' หรือ '2345' หรือ '23' แล้วคืนค่านาทีตั้งแต่ 00:00 (0..1439) หรือ None ถ้าผิดรูปแบบ"""
    try:
        s = s.strip()
        if ":" in s:
            h, m = s.split(":")
        elif s.isdigit() and len(s) in (3, 4):
            h, m = s[:-2], s[-2:]        # 930 -> 9:30 / 2345 -> 23:45
        else:
            h, m = s, "0"                # '23' -> 23:00
        h, m = int(h), int(m)
        if not (0 <= h < 24 and 0 <= m < 60):
            return None
        return h * 60 + m
    except:
        return None

def calc_sleep_minutes(bed_min, wake_min):
    """คำนวณนาทีที่นอน รองรับข้ามเที่ยงคืน + เคสเวลาตื่น=เวลานอน -> 0 ชม."""
    if wake_min == bed_min:
        return 0
    if wake_min <= bed_min:
        wake_min += 24 * 60
    return wake_min - bed_min

def parabolic_score(x, center, max_dev):
    s = 100 * (1 - ((x - center) / max_dev) ** 2)
    return max(0, min(100, s))

# ---------- UI ----------
st.title("Good Morning")

with st.container():
    st.subheader("กรอกข้อมูล")

    cA, cB = st.columns(2)
    with cA:
        bed_str = st.text_input(
            "เวลาเข้านอน",
            value="23:00",
            help="พิมพ์ได้หลายแบบ: 23:45, 2345, 23 (=23:00)"
        )
        bf = st.checkbox("Breakfast", value=True)

    with cB:
        wake_str = st.text_input(
            "เวลาตื่น",
            value="07:00",
            help="พิมพ์ได้หลายแบบ: 07:10, 710, 7 (=07:00)"
        )
        lu = st.checkbox("Lunch", value=True)

    di = st.checkbox("Dinner", value=True)

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    day_h = st.slider("ใช้ชีวิตวันนี้กี่ชั่วโมง (0–24)", 0.0, 24.0, 12.0, 0.5)
    st.markdown(
        '<p class="small-hint">หมายเหตุ: ใช้ชีวิต = ชั่วโมงกิจกรรมรวมทั้งวัน (ไม่รวมเวลานอน)</p>',
        unsafe_allow_html=True
    )

    submitted = st.button("คำนวณผล")
    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    try:
        bed_min = parse_hhmm(bed_str)
        wake_min = parse_hhmm(wake_str)

        if bed_min is None or wake_min is None:
            st.error("รูปแบบเวลาผิด: ใส่แบบ 23:45 หรือ 2345 หรือ 23")
            st.stop()

        if not (0 <= day_h <= 24):
            st.error(ERROR_MSG)
            st.stop()

        # ---- คำนวณเวลานอน ----
        sleep_min = calc_sleep_minutes(bed_min, wake_min)
        sleep_h = round(sleep_min / 60, 2)

        # ---- จัดเกรดการนอน ----
        if sleep_min == 0:
            sleep_grade = 'ไม่ได้นอน'
            sleep_msg = sleep_text['none']
        elif 8 <= sleep_h <= 9:
            sleep_grade = 'สมบูรณ์'
            sleep_msg = sleep_text['perfect']
        elif 6 <= sleep_h < 8:
            sleep_grade = 'ดี'
            sleep_msg = sleep_text['good']
        elif 4 <= sleep_h < 6:
            sleep_grade = 'พอใช้'
            sleep_msg = sleep_text['fair']
        elif sleep_h > 9:
            sleep_grade = 'นอนเยอะเกินไป'
            sleep_msg = sleep_text['over']
        elif 0 < sleep_h < 4:
            sleep_grade = 'แย่'
            sleep_msg = sleep_text['poor']
        else:
            sleep_grade = 'กลางๆ'
            sleep_msg = '-'

        # ---- จำนวนมื้ออาหาร ----
        cnt = (1 if bf else 0) + (1 if lu else 0) + (1 if di else 0)

        if cnt == 3:
            meal_grade = 'ดี'
        elif cnt == 2:
            meal_grade = 'พอใช้'
        elif cnt == 1:
            meal_grade = 'ไม่เพียงพอ'
        else:
            meal_grade = 'ไม่ดี'

        meal_msg = meal_text[cnt]

        # ---- ชั่วโมงการใช้ชีวิต ----
        if day_h in (0, 1, 2, 3):
            day_grade = 'น้อยมาก'
            day_msg = day_text['zero_to_three']
        elif day_h <= 13:
            day_grade = '<=13 ชม.'
            day_msg = day_text['le13']
        elif day_h > 18:
            day_grade = '>18 ชม.'
            day_msg = day_text['gt18']
        else:
            day_grade = '14-18 ชม.'
            day_msg = day_text['mid']

        # ---- overall score ----
        score = 0
        if sleep_grade in ['สมบูรณ์', 'ดี']:
            score += 2
        elif sleep_grade in ['พอใช้']:
            score += 1

        if meal_grade == 'ดี':
            score += 2
        elif meal_grade == 'พอใช้':
            score += 1

        if day_grade in ['<=13 ชม.', '14-18 ชม.']:
            score += 2
        elif day_grade == '>18 ชม.':
            score += 1

        if score >= 3:
            overall = "โดยรวมสำหรับวันนี้ดีมาก "
        elif score >= 2:
            overall = "อยู่ในเกณฑ์พอใช้ "
        else:
            overall = "อยู่ในเกณฑ์ที่ค่อนข้างแย่ ต้องปรับเปลี่ยนพฤติกรรม"

        # ---- balance score ----
        sleep_score = parabolic_score(sleep_h, center=8,  max_dev=4)
        day_score   = parabolic_score(day_h,   center=12, max_dev=6)
        meal_score  = {3: 100, 2: 70, 1: 35, 0: 0}.get(cnt, 0)

        balance_raw = (sleep_score + meal_score + day_score) / 3
        penalty = 0
        if sleep_h < 4 or sleep_h > 11:
            penalty += 15
        if cnt <= 1:
            penalty += 15
        if day_h in (0, 1, 2, 3) or day_h > 18:
            penalty += 15

        balance_score = max(0, round(balance_raw - penalty, 1))

        if balance_score >= 80:
            balance_text = "สมดุลดีมาก รักษาแพทเทิร์นนี้ไว้!"
        elif balance_score >= 60:
            balance_text = "ค่อนข้างดี ปรับเล็กน้อยให้ดีขึ้นได้อีก"
        elif balance_score >= 40:
            balance_text = "พอใช้ ลองลดความสุดโต่งบางอย่างดู"
        else:
            balance_text = "ไม่ค่อยสมดุล หาเวลาพัก/กินให้พอ และจัดเวลาใหม่"

        # ---------- OUTPUT ----------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("ผลลัพธ์")
        st.write(f"**สรุปเวลานอน:** {sleep_h} ชั่วโมง")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Sleeping", f"{sleep_grade}")  # เอา help ออก
            st.caption(sleep_msg)                    # แสดงข้อความใต้ metric
        with m2:
            st.metric("Meals (มื้อ)", f"{cnt} ({meal_grade})")
            st.caption(meal_msg)
        with m3:
            st.metric("Daytime (ชม.)", f"{day_h:.2f} ({day_grade})")
            st.caption(day_msg)
        st.success(f"Summary: {overall}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Balance Summary")
        st.write(f"**Balance Score:** {balance_score} / 100")
        st.progress(min(100, int(balance_score)))
        st.info(balance_text)
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"{ERROR_MSG} -> {e}")
