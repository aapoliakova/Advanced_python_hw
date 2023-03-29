import asyncio
import os
import aiohttp


async def download_img(url, session, root):
    async with session.get(url) as r:
        out = await r.read()
        with open(root, "wb+") as savefile:
            savefile.write(out)


async def download(url, root, n=5):
    async with aiohttp.ClientSession() as ses:
        tasks = []
        for i in range(n):
            image_file_name = os.path.join(root, str(i) + ".png")
            tasks.append(asyncio.create_task(download_img(url, ses, image_file_name)))
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    os.makedirs("artifacts/easy", exist_ok=True)
    url = "https://picsum.photos/200/300"
    root = "artifacts/easy"
    asyncio.run(download(url, root))
