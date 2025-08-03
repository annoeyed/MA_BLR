"""
모든 시나리오 일괄 실행 + 메트릭
"""
import asyncio, json, time
from src.utils.metrics import success_rate, stealth_score, impact_score
from experiments.scenarios.distributed_attack import main as dist_run
from experiments.scenarios.trust_exploitation import main as trust_run
from experiments.scenarios.spatiotemporal_trigger import main as st_run

async def bench(run, label):
    t0=time.time(); res=await run(); return {"case":label,"time":time.time()-t0,"alerts":res["total"]}

async def main():
    out=[]
    out.append(await bench(dist_run,"distributed"))
    out.append(await bench(trust_run,"trust"))
    out.append(await bench(st_run,"spatiotemporal"))
    print(json.dumps(out, indent=2))
if __name__=="__main__":
    asyncio.run(main())
