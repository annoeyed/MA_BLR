"""
분산 백도어 시나리오 – 3개 토큰 A/B/C
"""
import asyncio
from src.attacks.distributed_backdoor import DBAgent
async def main():
    toks=["A","B","C"]
    bots=[DBAgent(f"agent_{i:03}",t) for i,t in enumerate(toks)]
    for b in bots: await b.start()
    for a in bots:
        for b in bots:
            if a!=b: await a.connect(b.agent_id)
    await asyncio.gather(*(b.try_activate() for b in bots))
    await asyncio.sleep(2)
    # 탐지
    from src.detection.anomaly_detector import AnomalyDetector
    res=AnomalyDetector(bots).detect(); print(res)
    await asyncio.gather(*(b.stop() for b in bots))
if __name__=="__main__": asyncio.run(main())
