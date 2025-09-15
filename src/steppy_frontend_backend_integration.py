"""
Steppy フロントエンド・バックエンド連携システム
- 統合クライアント
- リアルタイム同期
- エラーハンドリング
- 状態管理
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
import logging
from enum import Enum

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyncStatus(Enum):
    """同期状態"""
    SYNCED = "synced"
    SYNCING = "syncing"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class IntegrationConfig:
    """統合設定"""
    api_base_url: str
    websocket_url: str
    sync_interval: int = 30  # 秒
    retry_attempts: int = 3
    timeout: int = 10

@dataclass
class UserState:
    """ユーザー状態"""
    user_id: str
    current_tasks: List[Dict[str, Any]]
    dashboard_data: Dict[str, Any]
    non_cognitive_scores: Dict[str, int]
    last_sync: datetime
    sync_status: SyncStatus

class SteppyFrontendBackendIntegration:
    """Steppy フロントエンド・バックエンド統合システム"""
    
    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.user_states: Dict[str, UserState] = {}
        self.sync_callbacks: List[Callable] = []
        self.error_callbacks: List[Callable] = []
        self.logger = logging.getLogger(__name__)
        self._sync_task = None
        self._running = False
    
    async def initialize(self):
        """初期化"""
        self.logger.info("フロントエンド・バックエンド統合システム初期化開始")
        self._running = True
        
        # 同期タスク開始
        self._sync_task = asyncio.create_task(self._sync_loop())
        
        self.logger.info("フロントエンド・バックエンド統合システム初期化完了")
    
    async def shutdown(self):
        """シャットダウン"""
        self.logger.info("フロントエンド・バックエンド統合システムシャットダウン開始")
        self._running = False
        
        if self._sync_task:
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("フロントエンド・バックエンド統合システムシャットダウン完了")
    
    async def get_today_tasks(self, user_id: str, category_preferences: Dict[str, float] = None) -> Dict[str, Any]:
        """今日のタスク取得（フロントエンド向け）"""
        try:
            # バックエンドAPI呼び出し
            response = await self._call_backend_api(
                "GET",
                f"{self.config.api_base_url}/api/today",
                params={"user_id": user_id, "preferences": json.dumps(category_preferences)}
            )
            
            if response["success"]:
                # ユーザー状態更新
                await self._update_user_tasks(user_id, response["data"]["cards"])
                
                return {
                    "success": True,
                    "data": response["data"],
                    "cached": False
                }
            else:
                # フォールバック: ローカルキャッシュ
                return await self._get_cached_tasks(user_id)
        
        except Exception as e:
            self.logger.error(f"今日のタスク取得エラー: {e}")
            return await self._get_cached_tasks(user_id)
    
    async def submit_activity(self, user_id: str, task_id: str, duration_seconds: int, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """活動提出（フロントエンド向け）"""
        try:
            # バックエンドAPI呼び出し
            response = await self._call_backend_api(
                "POST",
                f"{self.config.api_base_url}/api/submit",
                json={
                    "user_id": user_id,
                    "task_id": task_id,
                    "duration_seconds": duration_seconds,
                    "result_data": result_data
                }
            )
            
            if response["success"]:
                # ユーザー状態更新
                await self._update_user_activity(user_id, response["data"])
                
                # 同期コールバック実行
                await self._notify_sync_callbacks(user_id, "activity_submitted")
                
                return {
                    "success": True,
                    "data": response["data"]
                }
            else:
                return {
                    "success": False,
                    "error": response.get("error", "Unknown error")
                }
        
        except Exception as e:
            self.logger.error(f"活動提出エラー: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """ダッシュボードデータ取得（フロントエンド向け）"""
        try:
            # バックエンドAPI呼び出し
            response = await self._call_backend_api(
                "GET",
                f"{self.config.api_base_url}/api/dashboard",
                params={"user_id": user_id}
            )
            
            if response["success"]:
                # ユーザー状態更新
                await self._update_user_dashboard(user_id, response["data"])
                
                return {
                    "success": True,
                    "data": response["data"],
                    "cached": False
                }
            else:
                # フォールバック: ローカルキャッシュ
                return await self._get_cached_dashboard(user_id)
        
        except Exception as e:
            self.logger.error(f"ダッシュボードデータ取得エラー: {e}")
            return await self._get_cached_dashboard(user_id)
    
    async def _call_backend_api(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """バックエンドAPI呼び出し"""
        # 実装は後で追加（aiohttp使用）
        # 現在はモック応答
        if "today" in url:
            return {
                "success": True,
                "data": {
                    "user_id": kwargs.get("params", {}).get("user_id", "user_123"),
                    "cards": [
                        {
                            "id": "task_1",
                            "category": "学習",
                            "title": "英単語1個覚える",
                            "description": "今日覚える単語：Innovation",
                            "content": "Innovation = 革新",
                            "duration": 60,
                            "difficulty": "easy"
                        }
                    ],
                    "recommendations": {
                        "primary": "学習",
                        "balance_suggestion": "健康カテゴリが不足気味です"
                    }
                }
            }
        elif "submit" in url:
            return {
                "success": True,
                "data": {
                    "activity_id": f"act_{int(time.time())}",
                    "badges_earned": ["継続力★3"],
                    "non_cognitive_score": {
                        "continuity": 3,
                        "challenge": 2,
                        "balance": 4
                    }
                }
            }
        elif "dashboard" in url:
            return {
                "success": True,
                "data": {
                    "daily_summary": {
                        "total_minutes": 3,
                        "categories_active": ["学習", "健康"],
                        "streak_days": 5
                    },
                    "weekly_trend": [
                        {"date": "2025-09-05", "minutes": 2},
                        {"date": "2025-09-06", "minutes": 4}
                    ],
                    "badges": {
                        "continuity": 3,
                        "challenge": 2,
                        "balance": 4
                    }
                }
            }
        else:
            return {"success": False, "error": "Unknown endpoint"}
    
    async def _update_user_tasks(self, user_id: str, tasks: List[Dict[str, Any]]):
        """ユーザータスク更新"""
        if user_id not in self.user_states:
            self.user_states[user_id] = UserState(
                user_id=user_id,
                current_tasks=[],
                dashboard_data={},
                non_cognitive_scores={},
                last_sync=datetime.now(),
                sync_status=SyncStatus.SYNCED
            )
        
        self.user_states[user_id].current_tasks = tasks
        self.user_states[user_id].last_sync = datetime.now()
        self.user_states[user_id].sync_status = SyncStatus.SYNCED
    
    async def _update_user_activity(self, user_id: str, activity_data: Dict[str, Any]):
        """ユーザー活動更新"""
        if user_id not in self.user_states:
            return
        
        # 非認知スコア更新
        if "non_cognitive_score" in activity_data:
            self.user_states[user_id].non_cognitive_scores = activity_data["non_cognitive_score"]
        
        self.user_states[user_id].last_sync = datetime.now()
        self.user_states[user_id].sync_status = SyncStatus.SYNCED
    
    async def _update_user_dashboard(self, user_id: str, dashboard_data: Dict[str, Any]):
        """ユーザーダッシュボード更新"""
        if user_id not in self.user_states:
            return
        
        self.user_states[user_id].dashboard_data = dashboard_data
        self.user_states[user_id].last_sync = datetime.now()
        self.user_states[user_id].sync_status = SyncStatus.SYNCED
    
    async def _get_cached_tasks(self, user_id: str) -> Dict[str, Any]:
        """キャッシュされたタスク取得"""
        if user_id in self.user_states and self.user_states[user_id].current_tasks:
            return {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "cards": self.user_states[user_id].current_tasks,
                    "recommendations": {
                        "primary": "学習",
                        "balance_suggestion": "キャッシュデータを使用中"
                    }
                },
                "cached": True
            }
        else:
            # フォールバック: デフォルトタスク
            return {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "cards": [
                        {
                            "id": "fallback_1",
                            "category": "学習",
                            "title": "英単語1個覚える",
                            "description": "今日覚える単語：Innovation",
                            "content": "Innovation = 革新",
                            "duration": 60,
                            "difficulty": "easy"
                        }
                    ],
                    "recommendations": {
                        "primary": "学習",
                        "balance_suggestion": "オフライン状態です"
                    }
                },
                "cached": True
            }
    
    async def _get_cached_dashboard(self, user_id: str) -> Dict[str, Any]:
        """キャッシュされたダッシュボード取得"""
        if user_id in self.user_states and self.user_states[user_id].dashboard_data:
            return {
                "success": True,
                "data": self.user_states[user_id].dashboard_data,
                "cached": True
            }
        else:
            # フォールバック: デフォルトダッシュボード
            return {
                "success": True,
                "data": {
                    "daily_summary": {
                        "total_minutes": 0,
                        "categories_active": [],
                        "streak_days": 0
                    },
                    "weekly_trend": [],
                    "badges": {
                        "continuity": 0,
                        "challenge": 0,
                        "balance": 0
                    }
                },
                "cached": True
            }
    
    async def _sync_loop(self):
        """同期ループ"""
        while self._running:
            try:
                await asyncio.sleep(self.config.sync_interval)
                
                if not self._running:
                    break
                
                # 全ユーザーの同期
                for user_id in list(self.user_states.keys()):
                    await self._sync_user_data(user_id)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"同期ループエラー: {e}")
                await self._notify_error_callbacks("sync_error", str(e))
    
    async def _sync_user_data(self, user_id: str):
        """ユーザーデータ同期"""
        try:
            self.user_states[user_id].sync_status = SyncStatus.SYNCING
            
            # ダッシュボードデータ同期
            dashboard_response = await self.get_dashboard_data(user_id)
            if dashboard_response["success"]:
                await self._update_user_dashboard(user_id, dashboard_response["data"])
            
            # 同期コールバック実行
            await self._notify_sync_callbacks(user_id, "data_synced")
            
        except Exception as e:
            self.logger.error(f"ユーザー {user_id} データ同期エラー: {e}")
            self.user_states[user_id].sync_status = SyncStatus.ERROR
            await self._notify_error_callbacks("user_sync_error", str(e))
    
    async def _notify_sync_callbacks(self, user_id: str, event_type: str):
        """同期コールバック通知"""
        for callback in self.sync_callbacks:
            try:
                await callback(user_id, event_type)
            except Exception as e:
                self.logger.error(f"同期コールバックエラー: {e}")
    
    async def _notify_error_callbacks(self, error_type: str, error_message: str):
        """エラーコールバック通知"""
        for callback in self.error_callbacks:
            try:
                await callback(error_type, error_message)
            except Exception as e:
                self.logger.error(f"エラーコールバックエラー: {e}")
    
    def add_sync_callback(self, callback: Callable):
        """同期コールバック追加"""
        self.sync_callbacks.append(callback)
    
    def add_error_callback(self, callback: Callable):
        """エラーコールバック追加"""
        self.error_callbacks.append(callback)
    
    def get_user_state(self, user_id: str) -> Optional[UserState]:
        """ユーザー状態取得"""
        return self.user_states.get(user_id)
    
    def get_all_user_states(self) -> Dict[str, UserState]:
        """全ユーザー状態取得"""
        return self.user_states.copy()
    
    def clear_user_state(self, user_id: str):
        """ユーザー状態クリア"""
        if user_id in self.user_states:
            del self.user_states[user_id]

# 使用例
async def main():
    """使用例"""
    config = IntegrationConfig(
        api_base_url="http://localhost:3000",
        websocket_url="ws://localhost:3000/ws",
        sync_interval=30
    )
    
    integration = SteppyFrontendBackendIntegration(config)
    
    # 初期化
    await integration.initialize()
    
    # 同期コールバック追加
    async def on_sync(user_id: str, event_type: str):
        print(f"同期イベント: {user_id} - {event_type}")
    
    integration.add_sync_callback(on_sync)
    
    # 今日のタスク取得
    tasks = await integration.get_today_tasks("user_123")
    print("今日のタスク:", json.dumps(tasks, ensure_ascii=False, indent=2))
    
    # 活動提出
    activity = await integration.submit_activity(
        user_id="user_123",
        task_id="task_1",
        duration_seconds=45,
        result_data={"category": "学習", "difficulty": "easy", "confidence": "high"}
    )
    print("活動提出結果:", json.dumps(activity, ensure_ascii=False, indent=2))
    
    # ダッシュボードデータ取得
    dashboard = await integration.get_dashboard_data("user_123")
    print("ダッシュボードデータ:", json.dumps(dashboard, ensure_ascii=False, indent=2))
    
    # シャットダウン
    await integration.shutdown()

if __name__ == "__main__":
    asyncio.run(main())