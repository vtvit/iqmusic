import asyncio
from pytgcalls import idle
from config import call_py
from Musicjepthon.کارپێکردن import arq

        
async def main():
    await call_py.start()
    print(
        """
    ------------------
   | میوزیکی بۆتی زیرەك کاردەکات |
    ------------------
"""
    )
    await idle()
    await arq.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
