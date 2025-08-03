"""
멀티에이전트 공통 베이스 클래스
"""
import asyncio, time, logging, hashlib, uuid
from abc import ABC, abstractmethod
from typing import Dict, Any
from src.core.communication import AgentMessage, MessageType
from src.core.message_router import global_message_router

# ---------- 서명 및 인증 전용 통신 ----------
class SecureCommunicationProtocol:
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        self.key = hashlib.sha256(f"{agent_id}_key".encode()).hexdigest()
        self.authorized = set()
        self.log = logging.getLogger(f"Comm-{agent_id}")

    def _sign(self, msg: AgentMessage) -> str:
        # Simplified signature for example
        base = f"{msg.sender_id}{msg.receiver_id}{msg.timestamp}"
        return hashlib.sha256(base.encode()).hexdigest()

    def sign_message(self, msg: AgentMessage) -> None:
        msg.signature = self._sign(msg)

    def verify(self, msg: AgentMessage) -> bool:
        return self._sign(msg) == msg.signature

    def authenticate(self, peer_id: str) -> bool:
        ok = peer_id.startswith("agent_")
        if ok:
            self.authorized.add(peer_id)
        return ok

# ---------- 에이전트 베이스 ----------
class MultiAgentBase(ABC):
    def __init__(self, name: str, agent_type: str = "base") -> None:
        self.name = name
        self.agent_id = name
        self.agent_type = agent_type
        self.active = False
        self.peers: Dict[str, Dict[str, Any]] = {}
        self.msg_log, self.beh_log = [], []
        self.comm = SecureCommunicationProtocol(self.agent_id)
        self.queue = global_message_router.register_agent(self.agent_id)
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(self.agent_id)

    async def start(self) -> None:
        self.active = True
        asyncio.create_task(self._recv_loop())
        self.log.info("에이전트 기동")

    async def stop(self) -> None:
        self.active = False
        self.log.info("에이전트 중지")

    async def connect(self, peer_id: str) -> None:
        if self.comm.authenticate(peer_id):
            self.peers[peer_id] = {"since": time.time()}
            self.log.info(f"{peer_id} 연결 완료")

    async def send(self, target: str, mtype: MessageType, content: Dict[str,Any]) -> None:
        msg = AgentMessage(
            id=str(uuid.uuid4()), sender_id=self.agent_id, receiver_id=target,
            message_type=mtype, content=content, timestamp=time.time()
        )
        self.comm.sign_message(msg)
        await global_message_router.send_message(msg)
        self.msg_log.append(msg)

    async def broadcast(self, mtype: MessageType, content: Dict[str,Any]) -> None:
        for pid in self.peers:
            await self.send(pid, mtype, content)

    async def _recv_loop(self) -> None:
        while self.active:
            try:
                msg = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                if not self.comm.verify(msg):
                    self.log.warning("무결성 검증 실패")
                    continue
                await self._dispatch(msg)
            except asyncio.TimeoutError:
                continue # No message received, continue loop
            except Exception as e:
                self.log.error(f"수신 처리 오류: {e}")


    async def _dispatch(self, msg: AgentMessage) -> None:
        handler_map = {
            MessageType.HEARTBEAT: self.on_heartbeat,
            MessageType.QUERY    : self.on_query,
            MessageType.RESPONSE : self.on_response,
            MessageType.TRIGGER  : self.on_trigger,
            MessageType.BACKDOOR : self.on_backdoor,
            MessageType.BROADCAST: self.on_broadcast
        }
        handler = handler_map.get(msg.message_type)
        if handler:
            await handler(msg)
            self.beh_log.append({"t": time.time(), "evt": "recv", "type": msg.message_type.value})

    @abstractmethod
    async def on_heartbeat(self, msg: AgentMessage): ...
    @abstractmethod
    async def on_query(self, msg: AgentMessage): ...
    @abstractmethod
    async def on_response(self, msg: AgentMessage): ...
    @abstractmethod
    async def on_trigger(self, msg: AgentMessage): ...
    @abstractmethod
    async def on_backdoor(self, msg: AgentMessage): ...
    @abstractmethod
    async def on_broadcast(self, msg: AgentMessage): ...
