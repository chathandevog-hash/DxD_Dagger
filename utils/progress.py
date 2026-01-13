import asyncio

BARS = [
    "⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪\n0%",
    "🔴🔴🔴⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪\n✅ 40%",
    "🟠🟠🟠🟠🟠🟠⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪\n✅ 50%",
    "🟡🟡🟡🟡🟡🟡🟡🟡🟡🟡⚪⚪⚪⚪⚪⚪\n✅ 80%",
    "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢\n✅ 100%",
]

async def show_progress(msg, title="Processing..."):
    for b in BARS:
        await msg.edit_text(f"⏳ {title}\n\n{b}")
        await asyncio.sleep(0.6)
