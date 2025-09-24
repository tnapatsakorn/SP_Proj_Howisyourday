# Sprint 3
## Roles 
---
- **bie** - Coder & Planner
- **Twan** - Debugger & Planner

---

## Planning & Implementation
- เพิ่มระบบให้คะแนน มีตัวชี้วัด ได้แก่ Score และ Balance Score 0-100/100
  ```python
  
    score = 0
    if sleep_grade in ['สมบูรณ์', 'ดี']: score += 2
    elif sleep_grade in ['พอใช้']: score += 1
    if meal_grade == 'ดี': score += 2
    elif meal_grade == 'พอใช้': score += 1
    if day_grade in ['<=13 ชม.', '14-18 ชม.']: score += 2
    elif day_grade == '>18 ชม.': score += 1
    if score >= 3:
        overall = "โดยรวมสำหรับวันนี้ดีมาก "
    elif score >= 2:
        overall = "อยู่ในเกณฑ์พอใช้ "
    else:
        overall = "อยู่ในเกณฑ์ที่ค่อนข้างแย่ ต้องปรับเปลี่ยนพฤติกรรม"
  ```
---

- เพิ่มฟังก์ชัน Parabolic_score(x, center, max_dev)
  ``` python
    def parabolic_score(x, center, max_dev):
        s = 100 * (1 - ((x - center) / max_dev) ** 2)
        return max(0, min(100, s))
    sleep_score = parabolic_score(sleep_h, center=8,  max_dev=4)
    day_score   = parabolic_score(day_h,   center=12, max_dev=6)
  ```
---
- เพิ่มเงื่อนไข Penalty
``` python
penalty = 0
    if sleep_h < 4 or sleep_h > 11:   
        penalty += 15
    if cnt <= 1:    
        penalty += 15
    if day_h in (0, 1, 2, 3) or day_h > 18:  
        penalty += 15
```
---

## Debugged
แก้ score จาก 4 เป็น 3 เนื่องจากทดลองใช้ 4 แล้วค่าที่ได้ไม่ตรงตามสมดุลกับที่ตั้งไว้
