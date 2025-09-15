"""
Steppy AI/ML機能実装システム
- AI推薦エンジン（三段フォールバック戦略）
- 非認知能力分析システム
- 統合ダッシュボード機能
"""

import asyncio
import json
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Category(Enum):
    """カテゴリ定義"""
    LEARNING = "学習"
    WORK = "仕事"
    LIFE = "生活"
    HEALTH = "健康"

class Difficulty(Enum):
    """難易度定義"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

@dataclass
class Task:
    """タスクデータクラス"""
    id: str
    category: Category
    title: str
    description: str
    estimated_seconds: int
    difficulty: Difficulty
    content: Optional[str] = None

@dataclass
class UserActivity:
    """ユーザー活動データクラス"""
    user_id: str
    task_id: str
    category: Category
    completed_at: datetime
    duration_seconds: int
    result_data: Dict[str, Any]

@dataclass
class NonCognitiveScore:
    """非認知能力スコア"""
    continuity: int  # 継続力 (1-5)
    challenge: int   # 挑戦性 (1-5)
    balance: int     # バランス力 (1-5)

class AIRecommendationEngine:
    """AI推薦エンジン（三段フォールバック戦略）"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.fallback_enabled = True
        
    async def recommend_tasks(self, user_id: str, category_preferences: Dict[str, float] = None) -> List[Task]:
        """
        三段フォールバック戦略によるタスク推薦
        
        第1段階: AI推薦（OpenAI API）
        第2段階: ルールベース推薦
        第3段階: フォールバック（静的テンプレート）
        """
        try:
            # 第1段階: AI推薦（OpenAI API）
            if self.api_key and self._is_api_available():
                return await self._ai_recommend_tasks(user_id, category_preferences)
        except Exception as e:
            logger.warning(f"AI推薦失敗: {e}")
            
        try:
            # 第2段階: ルールベース推薦
            return self._rule_based_recommend_tasks(user_id, category_preferences)
        except Exception as e:
            logger.warning(f"ルールベース推薦失敗: {e}")
            
        # 第3段階: フォールバック（静的テンプレート）
        return self._fallback_tasks()
    
    async def _ai_recommend_tasks(self, user_id: str, category_preferences: Dict[str, float] = None) -> List[Task]:
        """AI推薦（OpenAI API使用）"""
        # 実装は後で追加（OpenAI API統合）
        # 現在はルールベースにフォールバック
        return self._rule_based_recommend_tasks(user_id, category_preferences)
    
    def _rule_based_recommend_tasks(self, user_id: str, category_preferences: Dict[str, float] = None) -> List[Task]:
        """ルールベース推薦"""
        tasks = []
        
        # カテゴリ別タスクテンプレート
        task_templates = {
            Category.LEARNING: [
                ("英単語1個覚える", "今日覚える単語を1つ選んで覚えましょう", 60, Difficulty.EASY),
                ("数学問題1問解く", "簡単な数学問題に挑戦しましょう", 60, Difficulty.MEDIUM),
                ("読書1ページ", "興味のある本を1ページ読みましょう", 60, Difficulty.EASY),
            ],
            Category.WORK: [
                ("資料整理1分", "デスク周りを1分間整理しましょう", 60, Difficulty.EASY),
                ("メール整理", "受信箱を1分間整理しましょう", 60, Difficulty.EASY),
                ("スキル学習", "新しいスキルを1分間学びましょう", 60, Difficulty.MEDIUM),
            ],
            Category.LIFE: [
                ("部屋掃除1分", "部屋の一角を1分間掃除しましょう", 60, Difficulty.EASY),
                ("料理準備", "今日の料理の準備を1分間しましょう", 60, Difficulty.MEDIUM),
                ("整理整頓", "身の回りを1分間整理しましょう", 60, Difficulty.EASY),
            ],
            Category.HEALTH: [
                ("ストレッチ1分", "全身を1分間ストレッチしましょう", 60, Difficulty.EASY),
                ("深呼吸", "深い呼吸を1分間行いましょう", 60, Difficulty.EASY),
                ("軽い運動", "その場で1分間軽い運動をしましょう", 60, Difficulty.MEDIUM),
            ]
        }
        
        # カテゴリ優先度に基づく推薦
        if category_preferences:
            sorted_categories = sorted(category_preferences.items(), key=lambda x: x[1], reverse=True)
        else:
            sorted_categories = [(cat.value, 1.0) for cat in Category]
        
        # 各カテゴリから1-2個のタスクを選択
        for category_name, priority in sorted_categories[:3]:  # 上位3カテゴリ
            try:
                category = Category(category_name)
                templates = task_templates[category]
                
                # 優先度に応じてタスク数を決定
                task_count = 2 if priority > 0.7 else 1
                
                for i in range(min(task_count, len(templates))):
                    title, desc, duration, difficulty = templates[i]
                    task = Task(
                        id=f"task_{category.value}_{i+1}_{int(time.time())}",
                        category=category,
                        title=title,
                        description=desc,
                        estimated_seconds=duration,
                        difficulty=difficulty,
                        content=f"{title}の詳細内容"
                    )
                    tasks.append(task)
            except ValueError:
                continue
                
        return tasks[:7]  # 最大7個のタスク
    
    def _fallback_tasks(self) -> List[Task]:
        """フォールバック（静的テンプレート）"""
        return [
            Task(
                id="fallback_1",
                category=Category.LEARNING,
                title="英単語1個覚える",
                description="今日覚える単語：Innovation",
                estimated_seconds=60,
                difficulty=Difficulty.EASY,
                content="Innovation = 革新"
            ),
            Task(
                id="fallback_2",
                category=Category.HEALTH,
                title="ストレッチ1分",
                description="全身を1分間ストレッチしましょう",
                estimated_seconds=60,
                difficulty=Difficulty.EASY,
                content="首、肩、腰を中心にストレッチ"
            ),
            Task(
                id="fallback_3",
                category=Category.WORK,
                title="資料整理1分",
                description="デスク周りを1分間整理しましょう",
                estimated_seconds=60,
                difficulty=Difficulty.EASY,
                content="書類を分類して整理"
            )
        ]
    
    def _is_api_available(self) -> bool:
        """API利用可能性チェック"""
        # 実装は後で追加（API状態確認）
        return False

class NonCognitiveAnalyzer:
    """非認知能力分析システム"""
    
    def __init__(self, db_path: str = "steppy_ai.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # ユーザー活動テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                task_id TEXT NOT NULL,
                category TEXT NOT NULL,
                completed_at TIMESTAMP NOT NULL,
                duration_seconds INTEGER NOT NULL,
                result_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 非認知スコアテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS non_cognitive_scores (
                user_id TEXT PRIMARY KEY,
                continuity INTEGER DEFAULT 0,
                challenge INTEGER DEFAULT 0,
                balance INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def analyze_continuity(self, user_id: str) -> int:
        """継続力分析（連続実行日数ベース）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 過去30日間の活動データを取得
        cursor.execute("""
            SELECT DISTINCT DATE(completed_at) as activity_date
            FROM user_activities
            WHERE user_id = ? AND completed_at >= datetime('now', '-30 days')
            ORDER BY activity_date DESC
        """, (user_id,))
        
        dates = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not dates:
            return 0
        
        # 連続日数を計算
        consecutive_days = 1
        current_date = datetime.strptime(dates[0], '%Y-%m-%d').date()
        
        for date_str in dates[1:]:
            activity_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if (current_date - activity_date).days == 1:
                consecutive_days += 1
                current_date = activity_date
            else:
                break
        
        # スコア計算（1-5段階）
        if consecutive_days >= 30:
            return 5
        elif consecutive_days >= 14:
            return 4
        elif consecutive_days >= 7:
            return 3
        elif consecutive_days >= 3:
            return 2
        elif consecutive_days >= 1:
            return 1
        else:
            return 0
    
    def analyze_challenge(self, user_id: str) -> int:
        """挑戦性分析（難易度選択パターン）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 過去7日間の難易度分布を取得
        cursor.execute("""
            SELECT result_data
            FROM user_activities
            WHERE user_id = ? AND completed_at >= datetime('now', '-7 days')
        """, (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return 0
        
        # 難易度分析
        hard_count = 0
        medium_count = 0
        easy_count = 0
        
        for result_data_str, in results:
            try:
                result_data = json.loads(result_data_str) if result_data_str else {}
                difficulty = result_data.get('difficulty', 'easy')
                
                if difficulty == 'hard':
                    hard_count += 1
                elif difficulty == 'medium':
                    medium_count += 1
                else:
                    easy_count += 1
            except:
                easy_count += 1
        
        total = hard_count + medium_count + easy_count
        if total == 0:
            return 0
        
        # 挑戦性スコア計算
        hard_ratio = hard_count / total
        medium_ratio = medium_count / total
        
        if hard_ratio >= 0.3:
            return 5
        elif hard_ratio >= 0.2 or (hard_ratio + medium_ratio) >= 0.6:
            return 4
        elif hard_ratio >= 0.1 or (hard_ratio + medium_ratio) >= 0.4:
            return 3
        elif medium_ratio >= 0.3:
            return 2
        elif medium_ratio >= 0.1:
            return 1
        else:
            return 0
    
    def analyze_balance(self, user_id: str) -> int:
        """バランス力分析（Shannon多様性指数）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 過去7日間のカテゴリ分布を取得
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM user_activities
            WHERE user_id = ? AND completed_at >= datetime('now', '-7 days')
            GROUP BY category
        """, (user_id,))
        
        category_counts = dict(cursor.fetchall())
        conn.close()
        
        if not category_counts:
            return 0
        
        # Shannon多様性指数計算
        total = sum(category_counts.values())
        if total == 0:
            return 0
        
        shannon_diversity = 0
        for count in category_counts.values():
            if count > 0:
                p = count / total
                shannon_diversity -= p * (p.bit_length() - 1)  # log2近似
        
        # バランススコア計算（1-5段階）
        max_diversity = (len(category_counts) - 1).bit_length() - 1  # 最大多様性
        if max_diversity == 0:
            return 0
        
        normalized_diversity = shannon_diversity / max_diversity
        
        if normalized_diversity >= 0.8:
            return 5
        elif normalized_diversity >= 0.6:
            return 4
        elif normalized_diversity >= 0.4:
            return 3
        elif normalized_diversity >= 0.2:
            return 2
        elif normalized_diversity > 0:
            return 1
        else:
            return 0
    
    def get_non_cognitive_score(self, user_id: str) -> NonCognitiveScore:
        """非認知能力スコア取得"""
        continuity = self.analyze_continuity(user_id)
        challenge = self.analyze_challenge(user_id)
        balance = self.analyze_balance(user_id)
        
        # データベースに保存
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO non_cognitive_scores
            (user_id, continuity, challenge, balance, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, continuity, challenge, balance))
        
        conn.commit()
        conn.close()
        
        return NonCognitiveScore(continuity=continuity, challenge=challenge, balance=balance)
    
    def record_activity(self, activity: UserActivity):
        """活動記録"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_activities
            (user_id, task_id, category, completed_at, duration_seconds, result_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            activity.user_id,
            activity.task_id,
            activity.category.value,
            activity.completed_at.isoformat(),
            activity.duration_seconds,
            json.dumps(activity.result_data)
        ))
        
        conn.commit()
        conn.close()

class SteppyAIMLSystem:
    """Steppy AI/ML統合システム"""
    
    def __init__(self, api_key: Optional[str] = None, db_path: str = "steppy_ai.db"):
        self.recommendation_engine = AIRecommendationEngine(api_key)
        self.analyzer = NonCognitiveAnalyzer(db_path)
        self.logger = logging.getLogger(__name__)
    
    async def get_today_tasks(self, user_id: str, category_preferences: Dict[str, float] = None) -> Dict[str, Any]:
        """今日のタスク取得"""
        try:
            tasks = await self.recommendation_engine.recommend_tasks(user_id, category_preferences)
            
            return {
                "user_id": user_id,
                "cards": [
                    {
                        "id": task.id,
                        "category": task.category.value,
                        "title": task.title,
                        "description": task.description,
                        "content": task.content,
                        "duration": task.estimated_seconds,
                        "difficulty": task.difficulty.value
                    }
                    for task in tasks
                ],
                "recommendations": {
                    "primary": tasks[0].category.value if tasks else "学習",
                    "balance_suggestion": self._get_balance_suggestion(user_id)
                },
                "fallback_available": True
            }
        except Exception as e:
            self.logger.error(f"タスク取得エラー: {e}")
            return self._get_fallback_response(user_id)
    
    def submit_activity(self, user_id: str, task_id: str, duration_seconds: int, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """活動提出"""
        try:
            # 活動記録
            activity = UserActivity(
                user_id=user_id,
                task_id=task_id,
                category=Category(result_data.get('category', '学習')),
                completed_at=datetime.now(),
                duration_seconds=duration_seconds,
                result_data=result_data
            )
            
            self.analyzer.record_activity(activity)
            
            # 非認知スコア更新
            non_cognitive_score = self.analyzer.get_non_cognitive_score(user_id)
            
            # バッジ判定
            badges_earned = self._check_badges_earned(non_cognitive_score)
            
            return {
                "success": True,
                "badges_earned": badges_earned,
                "non_cognitive_score": {
                    "continuity": non_cognitive_score.continuity,
                    "challenge": non_cognitive_score.challenge,
                    "balance": non_cognitive_score.balance
                },
                "next_suggestion": self._get_next_suggestion(user_id)
            }
        except Exception as e:
            self.logger.error(f"活動提出エラー: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """ダッシュボードデータ取得"""
        try:
            # 非認知スコア取得
            non_cognitive_score = self.analyzer.get_non_cognitive_score(user_id)
            
            # 日次サマリー計算
            daily_summary = self._calculate_daily_summary(user_id)
            
            # 週間トレンド計算
            weekly_trend = self._calculate_weekly_trend(user_id)
            
            return {
                "daily_summary": daily_summary,
                "weekly_trend": weekly_trend,
                "badges": {
                    "continuity": non_cognitive_score.continuity,
                    "challenge": non_cognitive_score.challenge,
                    "balance": non_cognitive_score.balance
                }
            }
        except Exception as e:
            self.logger.error(f"ダッシュボードデータ取得エラー: {e}")
            return self._get_fallback_dashboard()
    
    def _get_balance_suggestion(self, user_id: str) -> str:
        """バランス提案"""
        # 実装は後で追加（カテゴリ分析）
        return "健康カテゴリが不足気味です"
    
    def _check_badges_earned(self, score: NonCognitiveScore) -> List[str]:
        """バッジ獲得判定"""
        badges = []
        
        if score.continuity >= 3:
            badges.append(f"継続力★{score.continuity}")
        if score.challenge >= 2:
            badges.append(f"挑戦性★{score.challenge}")
        if score.balance >= 3:
            badges.append(f"バランス力★{score.balance}")
        
        return badges
    
    def _get_next_suggestion(self, user_id: str) -> str:
        """次の提案"""
        return "今日の目標達成まで残り2分"
    
    def _calculate_daily_summary(self, user_id: str) -> Dict[str, Any]:
        """日次サマリー計算"""
        # 実装は後で追加
        return {
            "total_minutes": 3,
            "categories_active": ["学習", "健康"],
            "streak_days": 5
        }
    
    def _calculate_weekly_trend(self, user_id: str) -> List[Dict[str, Any]]:
        """週間トレンド計算"""
        # 実装は後で追加
        return [
            {"date": "2025-09-05", "minutes": 2},
            {"date": "2025-09-06", "minutes": 4}
        ]
    
    def _get_fallback_response(self, user_id: str) -> Dict[str, Any]:
        """フォールバック応答"""
        return {
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
                "balance_suggestion": "システムを再起動中です"
            },
            "fallback_available": True
        }
    
    def _get_fallback_dashboard(self) -> Dict[str, Any]:
        """フォールバックダッシュボード"""
        return {
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
        }

# 使用例
async def main():
    """使用例"""
    # AI/MLシステム初期化
    ai_system = SteppyAIMLSystem(api_key="your_openai_api_key")
    
    # 今日のタスク取得
    tasks = await ai_system.get_today_tasks("user_123")
    print("今日のタスク:", json.dumps(tasks, ensure_ascii=False, indent=2))
    
    # 活動提出
    result = ai_system.submit_activity(
        user_id="user_123",
        task_id="task_1",
        duration_seconds=45,
        result_data={"category": "学習", "difficulty": "easy", "confidence": "high"}
    )
    print("活動提出結果:", json.dumps(result, ensure_ascii=False, indent=2))
    
    # ダッシュボードデータ取得
    dashboard = ai_system.get_dashboard_data("user_123")
    print("ダッシュボードデータ:", json.dumps(dashboard, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())