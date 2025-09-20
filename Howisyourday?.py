print("Good Morning")

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
    0: 'คุณควรได้รับประทานอาหารสักมื้อให้เพียงพอnnyต่อร่างกาย'
}

day_text = {
    'le13': 'ถือว่าคุณได้ชีวิตเต็มที่แล้วในวันนี้ ไม่แปลกที่จะเหนื่อย อาจจะถึงเวลาพักผ่อน',
    'gt18': 'ถือว่าคุณได้ชีวิตได้มากแล้ว หาเวลาพักได้แล้ว',
    'zero_to_three': 'พรุ่งนี้ได้เวลาออกไปใช้ชีวิตแล้ว',
    'mid': 'คุณอย่าลืมหาเวลาพักด้วยละ(14-18 ชม.)'
}

ERROR_MSG = "Error: Unknown data. Please, you better go to sleep."

def parse_hhmm(s):
    try:
        s = s.strip()
        if ':' not in s:  # เผื่อผู้ใช้พิมพ์เลขชั่วโมงอย่างเดียว
            h = int(s)
            m = 0
        else:
            h, m = s.split(':')
            h, m = int(h), int(m)
        if not(0 <= h < 24 and 0 <= m < 60):
            return None
        return h*60 + m
    except:
        return None

def calc_sleep_minutes(bed_min, wake_min):
    if wake_min == bed_min:
        return 0
    if wake_min <= bed_min:
        wake_min += 24*60
    return wake_min - bed_min

try:
    bed = input("(input) please tell your bedtime: ")
    wake = input("(input) what time did you wake up?: ")
    bf = input("(input) did you get breakfast? [y/n]: ")
    lunch = input("(input) did you get lunch? [y/n]: ")
    dinner = input("(input) did you get dinner? [y/n]: ")
    day = input("(input) how long did you spend your day? (hours): ")

    bed_min = parse_hhmm(bed)
    wake_min = parse_hhmm(wake)
    if bed_min is None or wake_min is None:
        print(ERROR_MSG)
        raise SystemExit

    # y/n อย่างง่าย
    bf = bf.strip().lower()
    lu = lunch.strip().lower()
    di = dinner.strip().lower()
    if bf not in ['y','n'] or lunch not in ['y','n'] or dinner not in ['y','n']:
        print(ERROR_MSG)
        raise SystemExit

    try:
        day_h = float(day)
        if day_h < 0 or day_h > 24:
            print(ERROR_MSG)
            raise SystemExit
    except:
        print(ERROR_MSG)
        raise SystemExit

    # ประเมินการนอน
    sleep_min = calc_sleep_minutes(bed_min, wake_min)
    sleep_h = round(sleep_min/60, 2)

    if sleep_min == 0:
        sleep_grade = 'ไม่ได้นอน'; sleep_msg = sleep_text['none']
    elif 8 <= sleep_h <= 9:
        sleep_grade = 'สมบูรณ์'; sleep_msg = sleep_text['perfect']
    elif 6 <= sleep_h < 8:
        sleep_grade = 'ดี'; sleep_msg = sleep_text['good']
    elif 4 <= sleep_h < 6:
        sleep_grade = 'พอใช้'; sleep_msg = sleep_text['fair']
    elif sleep_h > 9:
        sleep_grade = 'นอนเยอะเกินไป'; sleep_msg = sleep_text['over']
    elif 0 < sleep_h < 4:
        sleep_grade = 'แย่'; sleep_msg = sleep_text['poor']
    else:
        sleep_grade = 'กลางๆ'; sleep_msg = '-'

    # ประเมินมื้ออาหาร
    cnt = (1 if bf=='y' else 0) + (1 if lunch=='y' else 0) + (1 if dinner=='y' else 0)
    if cnt == 3:
        meal_grade = 'ดี'
    elif cnt == 2:
        meal_grade = 'พอใช้'
    elif cnt == 1:
        meal_grade = 'ไม่เพียงพอ'
    else:
        meal_grade = 'ไม่ดี'

    meal_msg = meal_text[cnt]

    if day_h in (0,1,2,3):
        day_grade = 'น้อยมาก'; day_msg = day_text['zero_to_three']
    elif day_h <= 13:
        day_grade = '<=13 ชม.'; day_msg = day_text['le13']
    elif day_h > 18:
        day_grade = '>18 ชม.'; day_msg = day_text['gt18']
    else:
        # 13 < day_h <= 18
        day_grade = '14-18 ชม.'; day_msg = day_text['mid']

    result = [
        {
            'category': 'sleeping',
            'value_hours': sleep_h,
            'grade': sleep_grade,
            'message': sleep_msg,
            'details': {'bedtime': bed, 'wake_time': wake}
        },
        {
            'category': 'meals',
            'value_meals': cnt,
            'grade': meal_grade,
            'message': meal_msg,
            'details': {'breakfast': bf=='y', 'lunch': lu=='y', 'dinner': di=='y'}
        },
        {
            'category': 'daytime',
            'value_hours': round(day_h, 2),
            'grade': day_grade,
            'message': day_msg
        }
    ]

    # แสดงผล
    print("\n--- Result ---")

    print(f"สรุปเวลานอน: {sleep_h} ชั่วโมง")
    print(f"[sleeping] -> grade: {sleep_grade} | message: {sleep_msg}")
    print(f"[meals]    -> grade: {meal_grade} | message: {meal_msg}")
    print(f"[daytime]  -> grade: {day_grade} | message: {day_msg}")
    print("[results] You are the best. You have done with your day and now you will sleep well :)")

except SystemExit:
    pass
except Exception as e:
    print(ERROR_MSG, "->",e)
