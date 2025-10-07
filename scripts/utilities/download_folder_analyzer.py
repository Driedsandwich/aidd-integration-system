#!/usr/bin/env python3
"""
ダウンロードフォルダ分析・整理ツール
大量のファイルを自動的に分類・整理するためのスクリプト
"""

import os
import shutil
import json
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse

class DownloadFolderAnalyzer:
    def __init__(self, download_path=None):
        if download_path is None:
            # Windowsの一般的なダウンロードフォルダパス
            self.download_path = Path.home() / "Downloads"
        else:
            self.download_path = Path(download_path)
        
        self.analysis_result = {
            "total_files": 0,
            "total_dirs": 0,
            "total_size": 0,
            "file_types": defaultdict(int),
            "file_extensions": defaultdict(int),
            "size_categories": defaultdict(int),
            "date_categories": defaultdict(int),
            "duplicate_files": [],
            "large_files": [],
            "old_files": [],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # ファイル分類ルール
        self.file_categories = {
            "images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico'],
            "videos": ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            "audio": ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
            "documents": ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf'],
            "archives": ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            "executables": ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.app'],
            "code": ['.py', '.js', '.html', '.css', '.json', '.xml', '.sql', '.sh', '.bat'],
            "data": ['.csv', '.json', '.xml', '.sql', '.db', '.sqlite'],
            "fonts": ['.ttf', '.otf', '.woff', '.woff2'],
            "other": []
        }

    def analyze_folder(self):
        """ダウンロードフォルダを分析"""
        print(f"[INFO] ダウンロードフォルダを分析中: {self.download_path}")
        
        if not self.download_path.exists():
            print(f"[ERROR] ダウンロードフォルダが見つかりません: {self.download_path}")
            return False
        
        file_hashes = defaultdict(list)
        
        for item in self.download_path.iterdir():
            try:
                if item.is_file():
                    self._analyze_file(item, file_hashes)
                elif item.is_dir():
                    self._analyze_directory(item)
            except (PermissionError, OSError) as e:
                print(f"[WARNING] アクセスエラー: {item.name} - {e}")
        
        self._find_duplicates(file_hashes)
        return True

    def _analyze_file(self, file_path, file_hashes):
        """個別ファイルの分析"""
        try:
            stat = file_path.stat()
            size = stat.st_size
            ext = file_path.suffix.lower()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            self.analysis_result["total_files"] += 1
            self.analysis_result["total_size"] += size
            
            # ファイル拡張子の統計
            self.analysis_result["file_extensions"][ext] += 1
            
            # MIMEタイプの取得
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type:
                main_type = mime_type.split('/')[0]
                self.analysis_result["file_types"][main_type] += 1
            
            # サイズカテゴリ
            if size < 1024 * 1024:  # < 1MB
                self.analysis_result["size_categories"]["small"] += 1
            elif size < 10 * 1024 * 1024:  # < 10MB
                self.analysis_result["size_categories"]["medium"] += 1
            elif size < 100 * 1024 * 1024:  # < 100MB
                self.analysis_result["size_categories"]["large"] += 1
            else:
                self.analysis_result["size_categories"]["very_large"] += 1
                self.analysis_result["large_files"].append({
                    "name": file_path.name,
                    "size": size,
                    "size_mb": round(size / (1024 * 1024), 2),
                    "modified": mtime.isoformat()
                })
            
            # 日付カテゴリ
            days_old = (datetime.now() - mtime).days
            if days_old < 7:
                self.analysis_result["date_categories"]["recent"] += 1
            elif days_old < 30:
                self.analysis_result["date_categories"]["this_month"] += 1
            elif days_old < 365:
                self.analysis_result["date_categories"]["this_year"] += 1
            else:
                self.analysis_result["date_categories"]["old"] += 1
                self.analysis_result["old_files"].append({
                    "name": file_path.name,
                    "days_old": days_old,
                    "modified": mtime.isoformat(),
                    "size": size
                })
            
            # ハッシュ計算（重複検出用）
            try:
                file_hash = self._calculate_file_hash(file_path)
                file_hashes[file_hash].append({
                    "path": str(file_path),
                    "name": file_path.name,
                    "size": size
                })
            except Exception:
                pass  # ハッシュ計算に失敗した場合はスキップ
                
        except Exception as e:
            print(f"[WARNING] ファイル分析エラー: {file_path.name} - {e}")

    def _analyze_directory(self, dir_path):
        """ディレクトリの分析"""
        self.analysis_result["total_dirs"] += 1
        
        # フォルダの詳細情報を記録
        try:
            stat = dir_path.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            # フォルダサイズを計算（中のファイル数をカウント）
            file_count = 0
            total_size = 0
            try:
                for item in dir_path.iterdir():
                    if item.is_file():
                        file_count += 1
                        try:
                            total_size += item.stat().st_size
                        except (OSError, PermissionError):
                            pass
            except (OSError, PermissionError):
                pass
            
            # フォルダ情報を追加
            if "folders" not in self.analysis_result:
                self.analysis_result["folders"] = []
            
            self.analysis_result["folders"].append({
                "name": dir_path.name,
                "file_count": file_count,
                "total_size": total_size,
                "size_mb": round(total_size / (1024 * 1024), 2),
                "modified": mtime.isoformat()
            })
            
        except Exception as e:
            print(f"[WARNING] フォルダ分析エラー: {dir_path.name} - {e}")

    def _calculate_file_hash(self, file_path, chunk_size=8192):
        """ファイルのハッシュ値を計算（重複検出用）"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None

    def _find_duplicates(self, file_hashes):
        """重複ファイルを検出"""
        for file_hash, files in file_hashes.items():
            if len(files) > 1:
                self.analysis_result["duplicate_files"].append({
                    "hash": file_hash,
                    "count": len(files),
                    "files": files
                })

    def generate_report(self):
        """分析レポートを生成"""
        print("\n" + "="*60)
        print("[REPORT] ダウンロードフォルダ分析レポート")
        print("="*60)
        
        print(f"総ファイル数: {self.analysis_result['total_files']:,}")
        print(f"総ディレクトリ数: {self.analysis_result['total_dirs']:,}")
        print(f"総サイズ: {self._format_size(self.analysis_result['total_size'])}")
        
        print(f"\nファイル拡張子トップ10:")
        sorted_exts = sorted(self.analysis_result['file_extensions'].items(), 
                           key=lambda x: x[1], reverse=True)[:10]
        for ext, count in sorted_exts:
            print(f"  {ext or '(拡張子なし)'}: {count:,}個")
        
        print(f"\nファイルタイプ別:")
        for mime_type, count in sorted(self.analysis_result['file_types'].items()):
            print(f"  {mime_type}: {count:,}個")
        
        print(f"\nサイズ別:")
        for size_cat, count in self.analysis_result['size_categories'].items():
            print(f"  {size_cat}: {count:,}個")
        
        print(f"\n日付別:")
        for date_cat, count in self.analysis_result['date_categories'].items():
            print(f"  {date_cat}: {count:,}個")
        
        print(f"\n重複ファイル: {len(self.analysis_result['duplicate_files'])}グループ")
        print(f"大容量ファイル(>100MB): {len(self.analysis_result['large_files'])}個")
        print(f"古いファイル(>1年): {len(self.analysis_result['old_files'])}個")
        
        # フォルダ情報を表示
        if "folders" in self.analysis_result and self.analysis_result["folders"]:
            print(f"\nフォルダ詳細:")
            for folder in sorted(self.analysis_result["folders"], key=lambda x: x["size_mb"], reverse=True)[:5]:
                print(f"  {folder['name']}: {folder['file_count']}ファイル, {folder['size_mb']}MB")
        
        return self.analysis_result

    def _format_size(self, size_bytes):
        """バイト数を読みやすい形式に変換"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"

    def save_report(self, output_file="download_analysis_report.json"):
        """分析結果をJSONファイルに保存"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_result, f, ensure_ascii=False, indent=2)
        print(f"\n[INFO] 分析結果を保存しました: {output_file}")

    def suggest_cleanup_actions(self):
        """整理アクションの提案"""
        print("\n" + "="*60)
        print("[SUGGESTIONS] 整理アクション提案")
        print("="*60)
        
        suggestions = []
        
        # 重複ファイルの移動
        if self.analysis_result['duplicate_files']:
            total_duplicates = sum(len(group['files']) - 1 for group in self.analysis_result['duplicate_files'])
            suggestions.append(f"重複ファイル移動: {total_duplicates}個のファイルを専用フォルダに移動")
        
        # 古いファイルのアーカイブ
        old_count = len(self.analysis_result['old_files'])
        if old_count > 0:
            suggestions.append(f"古いファイル({old_count}個)をアーカイブフォルダに移動")
        
        # 大容量ファイルの確認
        large_count = len(self.analysis_result['large_files'])
        if large_count > 0:
            suggestions.append(f"大容量ファイル({large_count}個)の必要性を確認")
        
        # ファイルタイプ別整理
        for category, extensions in self.file_categories.items():
            if category != "other":
                count = sum(self.analysis_result['file_extensions'].get(ext, 0) for ext in extensions)
                if count > 0:
                    suggestions.append(f"{category}ファイル({count}個)を専用フォルダに分類")
        
        # フォルダの整理
        if "folders" in self.analysis_result and self.analysis_result["folders"]:
            folder_count = len(self.analysis_result["folders"])
            suggestions.append(f"フォルダ({folder_count}個)を専用フォルダに分類")
        
        for suggestion in suggestions:
            print(f"  - {suggestion}")
        
        return suggestions

def main():
    parser = argparse.ArgumentParser(description="ダウンロードフォルダ分析・整理ツール")
    parser.add_argument("--path", help="ダウンロードフォルダのパス（未指定時は標準パスを使用）")
    parser.add_argument("--report", default="download_analysis_report.json", help="レポート出力ファイル名")
    
    args = parser.parse_args()
    
    analyzer = DownloadFolderAnalyzer(args.path)
    
    if analyzer.analyze_folder():
        analyzer.generate_report()
        analyzer.save_report(args.report)
        analyzer.suggest_cleanup_actions()
    else:
            print("[ERROR] 分析に失敗しました")

if __name__ == "__main__":
    main()
