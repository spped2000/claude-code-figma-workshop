# 🎨 Claude Code + Figma Workshop

> สาธิตการใช้ Claude Code แปลง Figma screenshot → HTML/CSS/JS
> พร้อม **Skill** เพื่อ enforce มาตรฐานทีม (design tokens, data discipline, runtime fetch)
>
> **เวลาทั้งหมด:** 30-45 นาที · **Level:** beginner-friendly

---

## 🎯 สิ่งที่จะได้เรียน

1. ใช้ Claude Code อ่าน Figma PNG → สร้าง HTML ใช้งานได้จริง
2. เขียน **Skill** (ไฟล์ markdown 80 บรรทัด) เพื่อให้ Claude ทำตาม style ทีม
3. เทียบ Before/After: ต่อให้มีไฟล์เดียวกัน ไม่มี skill ก็ไม่ได้ผลเหมือนกัน
4. ทำให้ UI กับ data แยกกัน — แก้ CSV → browser refresh → อัปเดตอัตโนมัติ

---

## 📦 Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/claude-code) ติดตั้งแล้ว (`claude --version`)
- Python 3.10+ (สำหรับ preview server)
- Browser ทั่วไป (Chrome/Edge/Safari)
- **ไม่ต้อง:** Figma paid plan (ใช้ screenshot เท่านั้น)

---

## 🚀 Quickstart (5 นาที)

### 1. Clone repo
```bash
git clone https://github.com/spped2000/claude-code-figma-workshop.git
cd claude-code-figma-workshop
```

### 2. เริ่ม preview server
```bash
python .claude/skills/mango-ui-builder/scripts/preview.py demos/src/rental_list.html 8090
```

เปิด browser ที่ http://localhost:8090/demos/src/rental_list.html
→ เห็นหน้า "สัญญาเช่าทั้งหมด" + ตาราง 5 rows = ✅ พร้อม

### 3. เปิด Claude Code
```bash
claude
```
Claude จะ auto-load `mango-ui-builder` skill จาก `.claude/skills/`

---

## 🎬 Workshop 4 cases (30 นาที)

### Case 1 — **Before vs After** skill (7 นาที)

เทียบว่ามี skill / ไม่มี skill ต่างกันยังไง

**Terminal A — ไม่มี skill:**
```bash
cd no-skill-demo
claude
```
พิมพ์:
```
สร้างหน้า dashboard สั้นๆ สำหรับระบบจัดการสัญญาเช่า มีตารางแสดง 5 สัญญา
```

**Terminal B — มี skill:**
```bash
cd .    # (กลับที่ root ของ repo)
claude
```
พิมพ์ prompt เดียวกัน

**ชี้ให้ดู:**
| จุด | ไม่มี skill | มี skill |
|---|---|---|
| Framework | อาจใช้ Bootstrap/random | Inline CSS + Mango tokens |
| ชื่อผู้เช่า | สมมุติ John/Jane | สมชาย ใจดี (จาก CSV) |
| สี | สุ่ม | ส้ม Mango (#E67E22) |
| Cross-check | ไม่มี | ตารางบอกทุก field มาจากไหน |

### Case 2 — **Lean mode** (5 นาที)

งานเล็ก → skill ทำแค่ที่จำเป็น

พิมพ์:
```
@skill mango-ui-builder
แค่เปลี่ยน --primary ใน demos/src/rental_list.html เป็น #4880FF
```

Claude ตอบสั้น 2-3 บรรทัด, ไม่ launch server ใหม่, ไม่ re-read ไฟล์

### Case 3 — **Data discipline** (5 นาที)

Claude ไม่แต่งข้อมูลเมื่อไม่มี source

พิมพ์:
```
@skill mango-ui-builder
สร้าง demos/src/user_profile.html หน้าโปรไฟล์ของ user ที่ login อยู่
```

**ควรเห็น:** `<span class="placeholder">[ชื่อผู้ใช้]</span>` + `<!-- TODO -->` comments
→ skill flag ว่า**ไม่มี CSV ของ logged-in user** ไม่สมมุติ

### Case 4 — **Data freshness** (5 นาที)

แก้ CSV → browser refresh → ข้อมูลอัปเดตโดย**ไม่เรียก Claude**

1. เปิด `mock-data/rental_contract_MOCK.csv` ใน editor
2. เพิ่ม row:
   ```csv
   RC-2025-0099,ลิต LIVE,1-9999-99999-99-9,UNIT-X-0099,คอนโด,2026-04-22,2027-04-21,22000,44000,ใช้งาน
   ```
3. Save
4. Browser (rental_list.html) → **Ctrl+Shift+R** (hard refresh)
5. เห็น row "ลิต LIVE" โผล่ในตาราง

**สิ่งที่สำคัญ:** Data และ UI แยกกัน — แก้ CSV ไม่ต้องแก้ HTML

---

## 🛠️ Hands-on Challenge (10-15 นาที)

**Task:** สร้างหน้าใหม่ `demos/src/contract_detail.html` — รายละเอียดสัญญา 1 สัญญา

**Hints:**
- Reference: `figma/rental_detail_mockup_SPEC.md`
- Data: `mock-data/rental_contract_MOCK.csv` row แรก
- ใช้ design_tokens.json (สีตรง Figma)

**Prompt ตัวอย่าง:**
```
@skill mango-ui-builder
สร้าง demos/src/contract_detail.html หน้ารายละเอียดสัญญา RC-2025-0001
Reference: figma/rental_detail_mockup_SPEC.md
Data: mock-data/rental_contract_MOCK.csv (row 1)
```

**ผ่านเมื่อ:**
- ✅ เปิดใน browser ได้ไม่ error
- ✅ Cross-check table แสดงแหล่งข้อมูลทุก field
- ✅ สีตรง design tokens
- ✅ ไม่ hardcode data (ใช้ runtime fetch)

---

## 📂 โครงสร้าง repo

```
claude-code-figma-workshop/
├── README.md                         ← ไฟล์นี้
├── LICENSE
├── .claude/skills/mango-ui-builder/
│   ├── SKILL.md                      ← rules (84 lines)
│   ├── TEST_SCENARIOS.md             ← 7 test cases
│   └── scripts/
│       ├── preview.py                ← localhost launcher
│       ├── verify.py                 ← HTML smoke test
│       └── stop.sh                   ← kill server
├── mock-data/
│   └── rental_contract_MOCK.csv      ← data source
├── figma/
│   ├── design_tokens.json            ← colors/fonts/spacing
│   ├── construction_dashboard_v1.png ← screenshot #1
│   ├── dashboard_v2.png              ← screenshot #2
│   ├── wireframe_fallback.txt        ← ASCII backup
│   └── rental_detail_mockup_SPEC.md  ← สำหรับ challenge
├── demos/src/
│   └── rental_list.html              ← ตัวอย่าง runtime fetch CSV
└── no-skill-demo/                    ← Case 1 baseline (no .claude/)
    ├── README.md
    ├── mock-data/
    └── figma/
```

---

## 💡 Key takeaways

> **Skill = markdown file 1 ไฟล์ ~80 บรรทัด**
>
> - 🎯 **Consistency** — ทีม 15 คน ใช้ style เดียวกัน
> - 🔍 **Transparency** — Claude flag ว่าแต่งข้อมูลตรงไหน
> - 🏗️ **Architecture** — บังคับ data/UI separation
> - 🔄 **Reusability** — git checkin, share, review เหมือน code ปกติ

---

## 🔧 Useful commands

```bash
# Start preview
python .claude/skills/mango-ui-builder/scripts/preview.py <html-file> [port]

# Verify HTML
python .claude/skills/mango-ui-builder/scripts/verify.py <html-file>

# Stop server
bash .claude/skills/mango-ui-builder/scripts/stop.sh [port]

# Claude Code shortcuts ในระหว่าง session
/status       # ดูสถานะ
/cost         # ดูการใช้ token
/compact      # ย่อ context
/model sonnet # เปลี่ยนเป็น Sonnet (ประหยัดกว่า Opus)
```

---

## 🧯 Troubleshooting

| ปัญหา | แก้ทันที |
|---|---|
| `python: command not found` | ใช้ `python3` แทน หรือติดตั้ง Python 3.10+ |
| Port 8090 busy | `bash .claude/skills/mango-ui-builder/scripts/stop.sh 8090` |
| Thai ใน terminal เพี้ยน (Windows) | รัน `chcp 65001` ก่อน `claude` |
| Skill ไม่ auto-trigger | พิมพ์ `@skill mango-ui-builder` บังคับ |
| CSV fetch 404 | ตรวจว่ารัน preview.py จาก root ของ repo ไม่ใช่ subfolder |
| HTML open แบบ `file://` ไม่เห็น data | ต้องเปิดผ่าน `http://localhost` (CORS) |

---

## 📚 เรียนรู้ต่อ

- [Claude Code docs](https://docs.anthropic.com/claude-code)
- [Claude skills guide](https://docs.anthropic.com/claude/docs/skills) (concepts)
- [Figma + Claude Code blog](https://www.figma.com/blog/introducing-claude-code-to-figma/) — ถ้าอยากต่อยอดใช้ Figma MCP

---

## 🤝 Contributing / Feedback

- Issues/PRs welcome
- หรือ fork repo นี้ + ปรับ skill สำหรับ domain ของคุณเอง

## 📝 License

MIT — ดู [LICENSE](LICENSE)
