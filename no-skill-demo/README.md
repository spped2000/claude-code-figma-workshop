# No-Skill Demo Folder

> **Workshop use:** comparison baseline สำหรับ Case 1 (Before vs After) ใน [SKILLS_SEGMENT.md](../section5/demos/demo-b/SKILLS_SEGMENT.md)

## Purpose
แสดงให้ผู้เรียนเห็นว่า **ต่อให้มีไฟล์ (CSV + design_tokens + PNG) พร้อมครบ**
หาก**ไม่มี skill** Claude ก็ทำงานตามใจตัวเอง ไม่ตามมาตรฐาน Mango

## Why outside `section5/`?
Claude Code จะ walk up หา `.claude/skills/` จาก cwd เสมอ
→ ถ้า folder นี้อยู่ใต้ `section5/` จะ **inherit** skill `mango-ui-builder` โดยอัตโนมัติ
→ ย้ายมาอยู่ sibling level ของ `section5/` เพื่อ**isolate** จริงๆ

## Folder contents (same resources as section5/)
```
no-skill-demo/
├── README.md                   ← ไฟล์นี้
├── mock-data/
│   ├── rental_contract_MOCK.csv
│   └── construction_project_MOCK.csv
├── figma/
│   ├── design_tokens.json
│   ├── construction_dashboard_v1.png
│   └── wireframe_fallback.txt
└── (NO .claude/ folder — this is the whole point)
```

## How to run Case 1 demo

### Step 1 — Open terminal in this folder
```bash
cd c:/Users/natdh/Documents/mango_claudecode/no-skill-demo
claude
```

### Step 2 — Verify no skills loaded
```
/context
```
ควร**ไม่**เห็น `mango-ui-builder` ในรายการ skills

### Step 3 — Prompt แบบเดียวกับใน skill demo
```
สร้างหน้า dashboard สั้นๆ สำหรับระบบจัดการสัญญาเช่า
มีตารางแสดง 5 สัญญา save ที่ dashboard.html
```

### Step 4 — ดูผลลัพธ์ + ปัญหาที่จะเกิด
Expected behavior (สิ่งที่ผู้เรียนจะเห็น):
- ❌ อาจใช้ Bootstrap/Tailwind (ไม่สน inline rule)
- ❌ อาจสมมุติชื่อผู้เช่าเป็น "John Doe" / "Jane Smith" (ไม่อ่าน CSV)
- ❌ อาจใช้สีสุ่ม ไม่ตรง design_tokens.json (#E67E22)
- ❌ อาจเป็นภาษาอังกฤษล้วน
- ❌ ไม่มี cross-check ว่าข้อมูลมาจากไหน
- ❌ ไม่ auto-preview

### Step 5 — Switch ไป folder มี skill
```bash
cd ../section5
claude
```

Run prompt เดียวกัน → เห็น Claude ทำงานต่าง:
- ✅ Inline CSS ใช้ Mango orange
- ✅ ผู้เช่าไทยจาก CSV (สมชาย ใจดี, สุดา รักเรียน, ...)
- ✅ Cross-check table
- ✅ Auto preview (M/L task)

---

## Teaching payoff

> "ต่อให้ dev copy **ไฟล์เดียวกันทั้งหมด** — CSV, design token, PNG ทุกอย่าง —
> **ไม่มี skill ก็ไม่ได้ของตรง**
>
> Skill คือสิ่งที่ทำให้ **resources เหล่านั้นถูกใช้ถูกต้อง**
> เหมือน manual วิธีใช้เครื่องมือ ไม่ใช่แค่เครื่องมือ"

---

## Cleanup after workshop

ลบ folder นี้ได้เมื่อ workshop จบ (ไม่ใช่ production code):
```bash
rm -rf c:/Users/natdh/Documents/mango_claudecode/no-skill-demo
```

หรือเก็บไว้ reference สำหรับ workshop ครั้งหน้า
