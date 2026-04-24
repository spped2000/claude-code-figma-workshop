# 🔧 Setup Guide

> ทำทุกขั้นตอนก่อนเข้า workshop ~20 นาที · ถ้าติดขั้นไหนดู [Troubleshooting](#troubleshooting) ด้านล่าง

---

## ✅ Checklist — ต้องมีทั้งหมดก่อนเริ่ม

- [ ] **Claude Code CLI** + login (ต้องมี Claude Pro account)
- [ ] **Python 3.10+** (สำหรับ preview server)
- [ ] **Git** (สำหรับ clone)
- [ ] **Browser** (Chrome / Edge / Firefox / Safari)
- [ ] **Terminal** ที่รองรับ UTF-8 (Thai text)

---

## Step 1 — ติดตั้ง Claude Code CLI (5 นาที)

### Windows / Mac / Linux
```bash
npm install -g @anthropic-ai/claude-code
```

### Verify
```bash
claude --version
```
ควรเห็น version เช่น `2.1.96 (Claude Code)`

### Login
```bash
claude login
```
→ จะเปิด browser ให้ login ด้วย Claude Pro account → กลับมาที่ terminal จะเห็น `✓ Authenticated`

**ถ้าไม่มี Claude Pro:** สมัครได้ที่ https://claude.ai/upgrade ($20/เดือน)

---

## Step 2 — ติดตั้ง Python (5 นาที)

### Windows
1. ไป https://www.python.org/downloads/
2. Download Python 3.10+ installer
3. Run installer — **ติ๊ก "Add Python to PATH"** (สำคัญ!)
4. Verify: เปิด new terminal → `python --version`

### Mac
```bash
brew install python@3.12
python3 --version
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install python3 python3-pip
python3 --version
```

### Verify
ควรเห็น `Python 3.10.x` หรือสูงกว่า

---

## Step 3 — Clone repo (2 นาที)

```bash
# เลือก folder ที่สะดวก
cd ~/Documents        # หรือที่ไหนก็ได้

# Clone
git clone https://github.com/spped2000/claude-code-figma-workshop.git

# เข้า folder
cd claude-code-figma-workshop
```

### Verify folder structure
```bash
ls
```
ควรเห็น: `README.md`, `.claude/`, `mock-data/`, `figma/`, `demos/`, `no-skill-demo/`

---

## Step 4 — Test preview server (3 นาที)

### รัน preview
```bash
python .claude/skills/mango-ui-builder/scripts/preview.py demos/src/rental_list.html 8090
```

**Windows ที่ใช้ `python3`:**
```bash
python3 .claude/skills/mango-ui-builder/scripts/preview.py demos/src/rental_list.html 8090
```

### ควรเห็น
```
🚀 Root:     /path/to/claude-code-figma-workshop
📍 URL:      http://localhost:8090/demos/src/rental_list.html
   (Ctrl+C to stop)
```

→ Browser เปิดอัตโนมัติที่ URL ดังกล่าว

### ตรวจหน้า rental_list.html
- ✅ Sidebar ซ้าย (สีเข้ม) + logo "MANGO ERP"
- ✅ Active item "สัญญาเช่า" (สีส้ม)
- ✅ ตาราง 5 rows (RC-2025-0001 ถึง 0005)
- ✅ KPI cards ด้านบน (สัญญาใช้งาน / ใกล้หมดอายุ / รายได้เดือนนี้)

ถ้าเห็น = ✅ **Setup สำเร็จ!** Ctrl+C เพื่อหยุด server

---

## Step 5 — Test Claude Code + skill (5 นาที)

### เปิด Claude Code ใน repo folder
```bash
cd claude-code-figma-workshop    # ต้องอยู่ใน root
claude
```

### ตรวจว่า skill auto-load
พิมพ์ใน Claude:
```
What skills do I have available?
```

Claude ควรตอบรายการที่มี `mango-ui-builder` อยู่ในนั้น

### ลอง XS task (Lean mode)
พิมพ์:
```
@skill mango-ui-builder
บอกผมว่า mango-ui-builder skill มี rules อะไรบ้าง สั้นๆ
```

Claude ควรอ่าน SKILL.md แล้วสรุป rules ให้

**ถ้า skill ไม่ trigger:** ดู [Troubleshooting](#skill-ไม่-auto-trigger) ด้านล่าง

---

## ✅ Ready to workshop!

ถ้า Step 1-5 ผ่านหมด → เปิด [README.md](README.md) → ข้ามไปหัวข้อ **🎬 Workshop 4 cases**

---

## Troubleshooting

### `claude: command not found`
- ตรวจว่า npm install สำเร็จ: `npm list -g @anthropic-ai/claude-code`
- Windows: restart terminal หลังติดตั้ง npm package
- Linux/Mac: เช็ค npm global bin ใน PATH: `echo $PATH | grep npm`

### `python: command not found` (Windows)
- ใช้ `python3` แทน
- หรือ reinstall Python + ติ๊ก "Add Python to PATH"

### `Port 8090 already in use`
```bash
bash .claude/skills/mango-ui-builder/scripts/stop.sh 8090
```
หรือใช้ port อื่น:
```bash
python .claude/skills/mango-ui-builder/scripts/preview.py demos/src/rental_list.html 8091
```

### CSV fetch 404 (table ว่าง browser console มี error)
- ตรวจว่ารัน preview **จาก root ของ repo** ไม่ใช่ subfolder
- Browser console → Network tab → ดูว่า request path ถูกไหม
- Hard refresh: `Ctrl+Shift+R`

### Thai text เพี้ยนใน terminal (Windows)
```bash
chcp 65001
```
รันก่อนเปิด `claude` — ตั้งให้ terminal ใช้ UTF-8

### Skill ไม่ auto-trigger
บังคับด้วย:
```
@skill mango-ui-builder
<your task here>
```
หรือตรวจว่า `.claude/skills/mango-ui-builder/SKILL.md` มีอยู่:
```bash
ls .claude/skills/mango-ui-builder/
```

### HTML เปิดด้วย `file://` ไม่โหลด CSV
Browser block CORS สำหรับ `file://` → **ต้องเปิดผ่าน `http://localhost`** (preview.py)
อย่า double-click HTML จาก Explorer

### `git clone` ล้มเหลว — proxy / firewall
ใช้ HTTPS clone URL (default) ถ้าที่ทำงาน block SSH
ถ้า proxy required: `git config --global http.proxy http://proxy:port`

### Claude Code login ปิด browser ไม่ทัน
```bash
claude logout
claude login
```
ลองอีกรอบ — บางครั้ง OAuth redirect ช้า

---

## 🆘 ยังติดอยู่?

1. เปิด issue ที่ repo: https://github.com/spped2000/claude-code-figma-workshop/issues
2. หรือถามใน workshop — instructor ช่วยได้
3. Backup plan: ถ้า local setup ไม่ได้ → ใช้ cloud shell (เช่น GitHub Codespaces) แทน

---

## 📎 Quick Reference

```bash
# All-in-one test (หลัง setup เสร็จ)
cd claude-code-figma-workshop
python .claude/skills/mango-ui-builder/scripts/preview.py demos/src/rental_list.html 8090 &
sleep 2
claude
# → พิมพ์ "@skill mango-ui-builder ลองใช้ skill ให้ดูหน่อย"

# Cleanup
bash .claude/skills/mango-ui-builder/scripts/stop.sh 8090
```
