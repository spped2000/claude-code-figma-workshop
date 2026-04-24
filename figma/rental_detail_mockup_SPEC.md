# Figma Mockup Spec — Rental Detail Page (สำหรับ Exercise 2)

## Canvas
- 1440 × 900 (เล็กกว่า dashboard เพราะเป็นหน้ารายละเอียด)
- Background: #F8F9FA
- Watermark: "MOCK DATA"

## Layout

### Header + Sidebar
เหมือน dashboard (ใช้ design_tokens.json เดียวกัน)

### Main Content (padding 32px)

#### Title
H1 "รายละเอียดสัญญาเช่า — RC-2025-0001"
Sub: "สมชาย ใจดี · UNIT-A-0301 · สถานะ: ใช้งาน"

#### Action bar (right-aligned)
- Button "พิมพ์สัญญา" (secondary)
- Button "ต่ออายุ" (secondary)
- Button "ยกเลิกสัญญา" (danger)

#### Tab Navigation (margin-top 24px)
3 tabs (underline style, gap 32px):
1. **ข้อมูลสัญญา** (active, underline #E67E22)
2. ตารางชำระ
3. ประวัติ

#### Tab 1: ข้อมูลสัญญา (default active)
Form 2 columns, gap 24px. แต่ละ field มี label + input

**Column 1:**
- ชื่อผู้เช่า (required) — text input
- เลขบัตรประชาชน (required) — masked input 13 หลัก
- เบอร์โทร — tel input
- อีเมล — email input

**Column 2:**
- รหัสหน่วย (required) — dropdown
- ประเภทหน่วย — text (disabled, auto-fill)
- วันเริ่มสัญญา (required) — date picker
- วันสิ้นสุดสัญญา (required) — date picker

**Row 3 (full width):**
- ค่าเช่ารายเดือน (required, min 5000, max 500000) — number input with "บาท"
- เงินประกัน (required, ต้อง ≥ 2× ค่าเช่า) — number input with "บาท" + helper text "แนะนำ: 2 เท่า สำหรับที่อยู่อาศัย, 3 เท่า สำหรับพาณิชย์"

**Row 4:**
- หมายเหตุ — textarea (4 rows)

**Action row:**
- Button "บันทึก" (primary) — disabled จนกว่า required fields จะครบ
- Button "ยกเลิก" (ghost)

#### Tab 2: ตารางชำระ (empty in mockup — แค่แสดง placeholder "คลิกแท็บเพื่อดู")
#### Tab 3: ประวัติ (เหมือนกัน — placeholder)

## Export
- ไฟล์: `figma/rental_detail_mockup.png` (2x, max width 1600px)
- Designer ควรแสดง tab "ข้อมูลสัญญา" เป็น active ใน mockup
