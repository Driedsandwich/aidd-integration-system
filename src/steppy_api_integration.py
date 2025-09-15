"""
Steppy API統合・連携システム
- OpenAI API統合
- サーキットブレーカーパターン
- 非同期処理
- エラーハンドリング
- キャッシュ戦略
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging
from enum import Enum
import hashlib

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CircuitState(Enum):
    """サーキットブレーカー状態"""
    CLOSED = "closed"      # 正常動作
    OPEN = "open"          # 障害発生、API呼び出し停止
    HALF_OPEN = "half_open"  # 復旧テスト中

@dataclass
class APIConfig:
    """API設定"""
    base_url: str
    api_key: str
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60

@dataclass
class APIResponse:
    """API応答"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    response_time: float = 0.0
    cached: bool = False

class CircuitBreaker:
    """サーキットブレーカー"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def can_execute(self) -> bool:
        """実行可能かチェック"""
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        else:  # HALF_OPEN
            return True
    
    def on_success(self):
        """成功時の処理"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        """失敗時の処理"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

class SteppyAPIIntegration:
    """Steppy API統合システム"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=config.circuit_breaker_threshold,
            timeout=config.circuit_breaker_timeout
        )
        self.cache = {}
        self.cache_ttl = 300  # 5分
        self.logger = logging.getLogger(__name__)
    
    async def get_today_tasks(self, user_id: str, category_preferences: Dict[str, float] = None) -> APIResponse:
        """今日のタスク取得API"""
        cache_key = f"today_tasks_{user_id}_{hashlib.md5(str(category_preferences).encode()).hexdigest()}"
        
        # キャッシュチェック
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            return APIResponse(success=True, data=cached_response, cached=True)
        
        # サーキットブレーカーチェック
        if not self.circuit_breaker.can_execute():
            return APIResponse(success=False, error="Circuit breaker is open")
        
        try:
            start_time = time.time()
            
            # OpenAI API呼び出し
            response_data = await self._call_openai_api(
                endpoint="/v1/chat/completions",
                payload={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": self._get_system_prompt()
                        },
                        {
                            "role": "user",
                            "content": self._get_user_prompt(user_id, category_preferences)
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
            )
            
            response_time = time.time() - start_time
            
            # 成功処理
            self.circuit_breaker.on_success()
            
            # キャッシュに保存
            self._save_to_cache(cache_key, response_data)
            
            return APIResponse(
                success=True,
                data=response_data,
                response_time=response_time
            )
            
        except Exception as e:
            self.circuit_breaker.on_failure()
            self.logger.error(f"今日のタスク取得API エラー: {e}")
            
            return APIResponse(
                success=False,
                error=str(e)
            )
    
    async def submit_activity(self, user_id: str, task_id: str, duration_seconds: int, result_data: Dict[str, Any]) -> APIResponse:
        """活動提出API"""
        try:
            start_time = time.time()
            
            # 活動データの検証
            if not self._validate_activity_data(user_id, task_id, duration_seconds, result_data):
                return APIResponse(success=False, error="Invalid activity data")
            
            # データベースに保存（実装は後で追加）
            # await self._save_activity_to_db(user_id, task_id, duration_seconds, result_data)
            
            # 非認知能力分析
            analysis_result = await self._analyze_activity(user_id, result_data)
            
            response_time = time.time() - start_time
            
            return APIResponse(
                success=True,
                data={
                    "activity_id": f"act_{int(time.time())}",
                    "analysis_result": analysis_result,
                    "timestamp": datetime.now().isoformat()
                },
                response_time=response_time
            )
            
        except Exception as e:
            self.logger.error(f"活動提出API エラー: {e}")
            return APIResponse(success=False, error=str(e))
    
    async def get_dashboard_data(self, user_id: str) -> APIResponse:
        """ダッシュボードデータ取得API"""
        cache_key = f"dashboard_{user_id}"
        
        # キャッシュチェック
        cached_response = self._get_from_cache(cache_key)
        if cached_response:
            return APIResponse(success=True, data=cached_response, cached=True)
        
        try:
            start_time = time.time()
            
            # ダッシュボードデータ生成
            dashboard_data = await self._generate_dashboard_data(user_id)
            
            response_time = time.time() - start_time
            
            # キャッシュに保存
            self._save_to_cache(cache_key, dashboard_data)
            
            return APIResponse(
                success=True,
                data=dashboard_data,
                response_time=response_time
            )
            
        except Exception as e:
            self.logger.error(f"ダッシュボードデータ取得API エラー: {e}")
            return APIResponse(success=False, error=str(e))
    
    async def _call_openai_api(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """OpenAI API呼び出し"""
        url = f"{self.config.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for attempt in range(self.config.max_retries):
                try:
                    async with session.post(url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            data = await response.json()
                            return self._parse_openai_response(data)
                        else:
                            error_text = await response.text()
                            raise Exception(f"API error: {response.status} - {error_text}")
                
                except asyncio.TimeoutError:
                    if attempt < self.config.max_retries - 1:
                        await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
                        continue
                    raise Exception("API timeout after retries")
                
                except Exception as e:
                    if attempt < self.config.max_retries - 1:
                        await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
                        continue
                    raise e
    
    def _parse_openai_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """OpenAI API応答の解析"""
        try:
            content = response_data["choices"][0]["message"]["content"]
            # JSON形式の応答を想定
            return json.loads(content)
        except (KeyError, json.JSONDecodeError) as e:
            # フォールバック: テキスト形式の応答を処理
            return {
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
                    "balance_suggestion": "AI推薦が利用できません"
                }
            }
    
    def _get_system_prompt(self) -> str:
        """システムプロンプト取得"""
        return """
あなたはSteppyという学習・成長支援アプリのAI推薦エンジンです。
ユーザーに最適な1分間のタスクを推薦してください。

カテゴリ:
- 学習: 語学、資格、読書など
- 仕事: スキルアップ、効率化など
- 生活: 家事、整理、生活改善など
- 健康: 運動、食事、メンタルケアなど

応答形式:
{
    "cards": [
        {
            "id": "task_id",
            "category": "カテゴリ名",
            "title": "タスクタイトル",
            "description": "タスク説明",
            "content": "具体的な内容",
            "duration": 60,
            "difficulty": "easy/medium/hard"
        }
    ],
    "recommendations": {
        "primary": "メインカテゴリ",
        "balance_suggestion": "バランス提案"
    }
}
"""
    
    def _get_user_prompt(self, user_id: str, category_preferences: Dict[str, float] = None) -> str:
        """ユーザープロンプト取得"""
        preferences_text = ""
        if category_preferences:
            preferences_text = f"カテゴリ優先度: {category_preferences}"
        
        return f"""
ユーザーID: {user_id}
{preferences_text}

現在の時刻: {datetime.now().strftime('%H:%M')}
曜日: {datetime.now().strftime('%A')}

このユーザーに最適な1分間のタスクを3-5個推薦してください。
時間帯と曜日を考慮し、バランスの取れた推薦を心がけてください。
"""
    
    def _validate_activity_data(self, user_id: str, task_id: str, duration_seconds: int, result_data: Dict[str, Any]) -> bool:
        """活動データの検証"""
        if not user_id or not task_id:
            return False
        
        if duration_seconds < 0 or duration_seconds > 3600:  # 1時間以内
            return False
        
        required_fields = ['category', 'difficulty', 'confidence']
        for field in required_fields:
            if field not in result_data:
                return False
        
        return True
    
    async def _analyze_activity(self, user_id: str, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """活動分析"""
        # 実装は後で追加（非認知能力分析）
        return {
            "continuity_score": 3,
            "challenge_score": 2,
            "balance_score": 4,
            "badges_earned": ["継続力★3"]
        }
    
    async def _generate_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """ダッシュボードデータ生成"""
        # 実装は後で追加（ダッシュボードデータ生成）
        return {
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
    
    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """キャッシュから取得"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def _save_to_cache(self, key: str, data: Dict[str, Any]):
        """キャッシュに保存"""
        self.cache[key] = (data, time.time())
    
    def clear_cache(self):
        """キャッシュクリア"""
        self.cache.clear()
    
    def get_circuit_breaker_status(self) -> Dict[str, Any]:
        """サーキットブレーカー状態取得"""
        return {
            "state": self.circuit_breaker.state.value,
            "failure_count": self.circuit_breaker.failure_count,
            "last_failure_time": self.circuit_breaker.last_failure_time
        }

# 使用例
async def main():
    """使用例"""
    config = APIConfig(
        base_url="https://api.openai.com",
        api_key="your_openai_api_key",
        timeout=30,
        max_retries=3
    )
    
    api_integration = SteppyAPIIntegration(config)
    
    # 今日のタスク取得
    tasks_response = await api_integration.get_today_tasks("user_123")
    print("今日のタスク:", json.dumps(tasks_response.data, ensure_ascii=False, indent=2))
    
    # 活動提出
    activity_response = await api_integration.submit_activity(
        user_id="user_123",
        task_id="task_1",
        duration_seconds=45,
        result_data={"category": "学習", "difficulty": "easy", "confidence": "high"}
    )
    print("活動提出結果:", json.dumps(activity_response.data, ensure_ascii=False, indent=2))
    
    # ダッシュボードデータ取得
    dashboard_response = await api_integration.get_dashboard_data("user_123")
    print("ダッシュボードデータ:", json.dumps(dashboard_response.data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())