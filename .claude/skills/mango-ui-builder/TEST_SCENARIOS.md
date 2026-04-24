# Test Scenarios for mango-ui-builder v2.1

> ใช้ verify ว่า skill ทำงานตาม rule ครบถ้วน

## Scenario 1 — Lean Mode: เปลี่ยนสี (XS)

**Prompt:**
```
@skill mango-ui-builder
แค่เปลี่ยนสี primary ใน demos/demo-b/src/rental_list.html จากส้มเป็นฟ้า #4880FF
```

**✅ Pass criteria:**
- Claude ใช้ **Edit tool** (ไม่ Write ทั้งไฟล์)
- **ไม่มี** 5-bullet layout description
- **ไม่มี** full cross-check table
- **ไม่ auto-start** localhost
- Reply สั้น (< 5 บรรทัด): "แก้ `--primary: #4880FF` ที่ `:root` line 4 — refresh browser"

**❌ Fail signals:**
- Re-reads all CSVs, design_tokens, PNG
- Writes 500-line cross-check table
- Starts new localhost server

---

## Scenario 2 — Path Resolution (เจอปัญหาเดิม)

**Setup:** สมมุติ `rental_list.html` อยู่ที่ `demos/demo-b/src/` แล้ว

**Prompt:**
```
@skill mango-ui-builder
แก้ rental_list.html เพิ่ม column วันเริ่มสัญญา
```

**✅ Pass criteria:**
- Claude **ไม่ assume** path — ใช้ Glob/find หาไฟล์ก่อน
- ถ้าพบหลายไฟล์ที่ตรง → ถาม user
- ถ้าพบ 1 ไฟล์ → ใช้เลย (`demos/demo-b/src/rental_list.html`)

**❌ Fail signal:**
- สร้างใหม่ที่ `src/rental_list.html` (root) ทั้งที่มีที่อื่นอยู่แล้ว

---

## Scenario 3 — Data Freshness: แก้ CSV → auto-update (critical!)

**Setup:**
1. Start preview: `python scripts/preview.py demos/demo-b/src/rental_list.html 8090`
2. เปิด browser — ต้องเห็น 5 rows

**Steps:**
1. Edit `mock-data/rental_contract_MOCK.csv` — เพิ่ม row ใหม่:
   ```
   RC-2025-0008,ทดสอบ AI,1-8888-88888-88-8,UNIT-D-0001,คอนโด 1 ห้องนอน,2026-04-22,2027-04-21,20000,40000,ใช้งาน
   ```
2. **Hard refresh browser** (Ctrl+Shift+R)
3. ดู table

**✅ Pass criteria:**
- Table แสดง row ใหม่ "RC-2025-0008 / ทดสอบ AI" โดย**ไม่ต้องเรียก Claude**
- KPI "สัญญาใช้งาน" +1
- KPI "รายได้เดือนนี้" +20,000

**❌ Fail signal:**
- Table ยังแสดง 5 rows เหมือนเดิม → HTML hardcode data (ขัด Rule 2b)
- ถ้า fail → skill ต้อง flag + refactor ให้ fetch runtime

---

## Scenario 4 — Proportional Live Preview

**Prompt A (XS):**
```
@skill mango-ui-builder
แก้ font-size ของ h1 ใน rental_list.html จาก 28px เป็น 32px
```

**✅ Pass:** Claude reply "แก้แล้ว refresh browser" — **ไม่ launch server**

**Prompt B (L):**
```
@skill mango-ui-builder
สร้าง demos/demo-b/src/rental_detail.html หน้ารายละเอียดสัญญา
Reference: figma/rental_detail_mockup_SPEC.md
Data: mock-data/rental_contract_MOCK.csv (row ใดก็ได้)
```

**✅ Pass:** Claude **auto-launch** localhost + report URL

---

## Scenario 5 — Fabrication Detection

**Prompt:**
```
@skill mango-ui-builder
สร้าง demos/demo-b/src/user_profile.html — หน้าโปรไฟล์ของ user ที่ login อยู่
```

**ปัญหา:** ไม่มี "logged-in user" ใน CSV ไหน

**✅ Pass criteria:**
- Claude **ไม่** สมมุติชื่อ user
- Render เป็น `<span class="placeholder" data-todo="fetch-from-user-session">[ชื่อผู้ใช้]</span>`
- Cross-check table mark ทุก field = ⚠️ fabricated
- Suggest integration point: "add `fetchUser()` after backend ready"

**❌ Fail signal:** แต่งชื่อ "คุณสมชาย ใจดี" เองทั้งที่ไม่มี data source

---

## Scenario 6 — Port Collision Handling

**Setup:** มี process listening port 8080 อยู่แล้ว

**Prompt:**
```
@skill mango-ui-builder
Start preview of demos/demo-b/src/rental_list.html
```

**✅ Pass:** preview.py auto-fallback ไป 8081 + แจ้ง user + open browser

---

## Scenario 7 — Cleanup Protocol

**Prompt:**
```
หยุด server ทั้งหมด
```

**✅ Pass:** Claude รัน `scripts/stop.sh` ด้วย port ที่รันอยู่ + confirm

---

## Running the suite

เรียกใช้แต่ละ scenario ตามลำดับ → เทียบผลกับ Pass criteria
บันทึกผลใน `test_results_YYYYMMDD.md` ถ้ามี fail → update skill

## Workshop teaching use

Scenario 1, 3, 5 เหมาะสำหรับ live demo:
- Scenario 1: แสดง "AI ฉลาดพอที่จะไม่ทำเยอะเกินจำเป็น"
- Scenario 3: แสดง "data แยกจาก logic" (ERP principle)
- Scenario 5: แสดง "transparent AI — ไม่แต่ง, flag เสมอ"
