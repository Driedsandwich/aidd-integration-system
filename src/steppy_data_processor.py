"""
Steppy データ処理・前処理システム
- データ正規化・検証
- 特徴量エンジニアリング
- パフォーマンス最適化
- データ品質管理
"""

import json
import sqlite3
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import logging
import statistics
from collections import defaultdict, Counter

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProcessedActivity:
    """処理済み活動データ"""
    user_id: str
    task_id: str
    category: str
    completed_at: datetime
    duration_seconds: int
    difficulty: str
    confidence: str
    normalized_duration: float
    time_of_day: int  # 0-23
    day_of_week: int  # 0-6 (月曜日=0)
    is_weekend: bool
    success_rate: float
    category_balance: float

@dataclass
class UserProfile:
    """ユーザープロファイル"""
    user_id: str
    total_activities: int
    avg_duration: float
    preferred_categories: List[str]
    preferred_time_slots: List[int]
    difficulty_preference: str
    activity_pattern: str  # "morning", "evening", "mixed"
    consistency_score: float
    last_activity: Optional[datetime]

class SteppyDataProcessor:
    """Steppy データ処理・前処理システム"""
    
    def __init__(self, db_path: str = "steppy_ai.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_database()
    
    def _init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 処理済み活動テーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                task_id TEXT NOT NULL,
                category TEXT NOT NULL,
                completed_at TIMESTAMP NOT NULL,
                duration_seconds INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                confidence TEXT NOT NULL,
                normalized_duration REAL NOT NULL,
                time_of_day INTEGER NOT NULL,
                day_of_week INTEGER NOT NULL,
                is_weekend BOOLEAN NOT NULL,
                success_rate REAL NOT NULL,
                category_balance REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ユーザープロファイルテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                total_activities INTEGER DEFAULT 0,
                avg_duration REAL DEFAULT 0.0,
                preferred_categories TEXT DEFAULT '[]',
                preferred_time_slots TEXT DEFAULT '[]',
                difficulty_preference TEXT DEFAULT 'easy',
                activity_pattern TEXT DEFAULT 'mixed',
                consistency_score REAL DEFAULT 0.0,
                last_activity TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def process_activity(self, raw_activity: Dict[str, Any]) -> ProcessedActivity:
        """活動データの処理・正規化"""
        try:
            # 基本データ抽出
            user_id = raw_activity.get('user_id', '')
            task_id = raw_activity.get('task_id', '')
            category = raw_activity.get('category', '学習')
            completed_at = datetime.fromisoformat(raw_activity.get('completed_at', datetime.now().isoformat()))
            duration_seconds = int(raw_activity.get('duration_seconds', 60))
            difficulty = raw_activity.get('difficulty', 'easy')
            confidence = raw_activity.get('confidence', 'medium')
            
            # データ正規化
            normalized_duration = self._normalize_duration(duration_seconds)
            time_of_day = completed_at.hour
            day_of_week = completed_at.weekday()
            is_weekend = day_of_week >= 5
            
            # 成功率計算
            success_rate = self._calculate_success_rate(user_id, category)
            
            # カテゴリバランス計算
            category_balance = self._calculate_category_balance(user_id)
            
            processed = ProcessedActivity(
                user_id=user_id,
                task_id=task_id,
                category=category,
                completed_at=completed_at,
                duration_seconds=duration_seconds,
                difficulty=difficulty,
                confidence=confidence,
                normalized_duration=normalized_duration,
                time_of_day=time_of_day,
                day_of_week=day_of_week,
                is_weekend=is_weekend,
                success_rate=success_rate,
                category_balance=category_balance
            )
            
            # データベースに保存
            self._save_processed_activity(processed)
            
            # ユーザープロファイル更新
            self._update_user_profile(user_id)
            
            return processed
            
        except Exception as e:
            self.logger.error(f"活動データ処理エラー: {e}")
            raise
    
    def _normalize_duration(self, duration_seconds: int) -> float:
        """実行時間の正規化（0-1スケール）"""
        # 1分=60秒を基準として正規化
        base_duration = 60
        normalized = min(duration_seconds / base_duration, 2.0)  # 最大2倍まで
        return max(0.0, min(1.0, normalized))
    
    def _calculate_success_rate(self, user_id: str, category: str) -> float:
        """成功率計算"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 過去7日間の同カテゴリ活動を取得
        cursor.execute("""
            SELECT result_data
            FROM user_activities
            WHERE user_id = ? AND category = ? AND completed_at >= datetime('now', '-7 days')
        """, (user_id, category))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return 0.5  # デフォルト値
        
        success_count = 0
        for result_data_str, in results:
            try:
                result_data = json.loads(result_data_str) if result_data_str else {}
                if result_data.get('completed', True):  # デフォルトは成功
                    success_count += 1
            except:
                success_count += 1  # エラー時は成功とみなす
        
        return success_count / len(results)
    
    def _calculate_category_balance(self, user_id: str) -> float:
        """カテゴリバランス計算（Shannon多様性指数）"""
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
        
        if not category_counts or len(category_counts) < 2:
            return 0.0
        
        # Shannon多様性指数計算
        total = sum(category_counts.values())
        shannon_diversity = 0
        
        for count in category_counts.values():
            if count > 0:
                p = count / total
                shannon_diversity -= p * (p.bit_length() - 1)  # log2近似
        
        # 正規化（0-1スケール）
        max_diversity = (len(category_counts) - 1).bit_length() - 1
        if max_diversity == 0:
            return 0.0
        
        return min(1.0, shannon_diversity / max_diversity)
    
    def _save_processed_activity(self, processed: ProcessedActivity):
        """処理済み活動データ保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO processed_activities
            (user_id, task_id, category, completed_at, duration_seconds, difficulty, confidence,
             normalized_duration, time_of_day, day_of_week, is_weekend, success_rate, category_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            processed.user_id,
            processed.task_id,
            processed.category,
            processed.completed_at.isoformat(),
            processed.duration_seconds,
            processed.difficulty,
            processed.confidence,
            processed.normalized_duration,
            processed.time_of_day,
            processed.day_of_week,
            processed.is_weekend,
            processed.success_rate,
            processed.category_balance
        ))
        
        conn.commit()
        conn.close()
    
    def _update_user_profile(self, user_id: str):
        """ユーザープロファイル更新"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 基本統計計算
        cursor.execute("""
            SELECT COUNT(*), AVG(duration_seconds), MAX(completed_at)
            FROM user_activities
            WHERE user_id = ?
        """, (user_id,))
        
        total_activities, avg_duration, last_activity = cursor.fetchone()
        avg_duration = avg_duration or 0.0
        
        # カテゴリ分布計算
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM user_activities
            WHERE user_id = ?
            GROUP BY category
            ORDER BY count DESC
        """, (user_id,))
        
        category_counts = dict(cursor.fetchall())
        preferred_categories = list(category_counts.keys())[:3]  # 上位3カテゴリ
        
        # 時間帯分布計算
        cursor.execute("""
            SELECT time_of_day, COUNT(*) as count
            FROM processed_activities
            WHERE user_id = ?
            GROUP BY time_of_day
            ORDER BY count DESC
        """, (user_id,))
        
        time_counts = dict(cursor.fetchall())
        preferred_time_slots = list(time_counts.keys())[:3]  # 上位3時間帯
        
        # 難易度分布計算
        cursor.execute("""
            SELECT difficulty, COUNT(*) as count
            FROM processed_activities
            WHERE user_id = ?
            GROUP BY difficulty
            ORDER BY count DESC
        """, (user_id,))
        
        difficulty_counts = dict(cursor.fetchall())
        difficulty_preference = max(difficulty_counts.keys(), key=difficulty_counts.get) if difficulty_counts else 'easy'
        
        # 活動パターン判定
        activity_pattern = self._determine_activity_pattern(preferred_time_slots)
        
        # 一貫性スコア計算
        consistency_score = self._calculate_consistency_score(user_id)
        
        # プロファイル保存
        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles
            (user_id, total_activities, avg_duration, preferred_categories, preferred_time_slots,
             difficulty_preference, activity_pattern, consistency_score, last_activity, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            user_id,
            total_activities,
            avg_duration,
            json.dumps(preferred_categories),
            json.dumps(preferred_time_slots),
            difficulty_preference,
            activity_pattern,
            consistency_score,
            last_activity
        ))
        
        conn.commit()
        conn.close()
    
    def _determine_activity_pattern(self, preferred_time_slots: List[int]) -> str:
        """活動パターン判定"""
        if not preferred_time_slots:
            return 'mixed'
        
        morning_slots = [6, 7, 8, 9, 10, 11]
        evening_slots = [18, 19, 20, 21, 22, 23]
        
        morning_count = sum(1 for slot in preferred_time_slots if slot in morning_slots)
        evening_count = sum(1 for slot in preferred_time_slots if slot in evening_slots)
        
        if morning_count > evening_count:
            return 'morning'
        elif evening_count > morning_count:
            return 'evening'
        else:
            return 'mixed'
    
    def _calculate_consistency_score(self, user_id: str) -> float:
        """一貫性スコア計算"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 過去30日間の日次活動数を取得
        cursor.execute("""
            SELECT DATE(completed_at) as activity_date, COUNT(*) as count
            FROM user_activities
            WHERE user_id = ? AND completed_at >= datetime('now', '-30 days')
            GROUP BY DATE(completed_at)
            ORDER BY activity_date
        """, (user_id,))
        
        daily_counts = dict(cursor.fetchall())
        conn.close()
        
        if not daily_counts:
            return 0.0
        
        # 一貫性スコア計算（標準偏差の逆数）
        counts = list(daily_counts.values())
        if len(counts) < 2:
            return 0.0
        
        mean_count = statistics.mean(counts)
        if mean_count == 0:
            return 0.0
        
        std_dev = statistics.stdev(counts)
        consistency_score = max(0.0, 1.0 - (std_dev / mean_count))
        
        return min(1.0, consistency_score)
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """ユーザープロファイル取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, total_activities, avg_duration, preferred_categories,
                   preferred_time_slots, difficulty_preference, activity_pattern,
                   consistency_score, last_activity
            FROM user_profiles
            WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return UserProfile(
            user_id=row[0],
            total_activities=row[1],
            avg_duration=row[2],
            preferred_categories=json.loads(row[3]),
            preferred_time_slots=json.loads(row[4]),
            difficulty_preference=row[5],
            activity_pattern=row[6],
            consistency_score=row[7],
            last_activity=datetime.fromisoformat(row[8]) if row[8] else None
        )
    
    def calculate_data_quality_metrics(self) -> Dict[str, Any]:
        """データ品質メトリクス計算"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        metrics = {}
        
        # データ完全性チェック
        cursor.execute("SELECT COUNT(*) FROM user_activities")
        total_activities = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM user_activities WHERE user_id IS NULL OR user_id = ''")
        incomplete_activities = cursor.fetchone()[0]
        
        completeness = (total_activities - incomplete_activities) / total_activities if total_activities > 0 else 0
        metrics['completeness'] = {
            'value': completeness,
            'threshold_min': 0.95,
            'threshold_max': 1.0,
            'status': 'good' if completeness >= 0.95 else 'warning'
        }
        
        # データ一貫性チェック
        cursor.execute("""
            SELECT COUNT(*) FROM user_activities
            WHERE duration_seconds < 0 OR duration_seconds > 3600
        """)
        inconsistent_durations = cursor.fetchone()[0]
        
        consistency = (total_activities - inconsistent_durations) / total_activities if total_activities > 0 else 0
        metrics['consistency'] = {
            'value': consistency,
            'threshold_min': 0.98,
            'threshold_max': 1.0,
            'status': 'good' if consistency >= 0.98 else 'warning'
        }
        
        conn.close()
        return metrics

# 使用例
def main():
    """使用例"""
    processor = SteppyDataProcessor()
    
    # 活動データ処理
    raw_activity = {
        'user_id': 'user_123',
        'task_id': 'task_1',
        'category': '学習',
        'completed_at': datetime.now().isoformat(),
        'duration_seconds': 45,
        'difficulty': 'easy',
        'confidence': 'high'
    }
    
    processed = processor.process_activity(raw_activity)
    print("処理済み活動データ:", asdict(processed))
    
    # データ品質メトリクス計算
    metrics = processor.calculate_data_quality_metrics()
    print("データ品質メトリクス:", json.dumps(metrics, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()