#для запуска worker
import asyncio, sys
sys.path.append("./")
from main import main

if __name__ == "__main__":
    asyncio.run(main())