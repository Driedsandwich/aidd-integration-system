#!/usr/bin/env python3
"""
ダウンロードフォルダ整理ツール
分析結果に基づいてファイルを自動分類・整理するスクリプト
"""

import os
import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime
import argparse
from collections import defaultdict

class DownloadFolderOrganizer:
    def __init__(self, download_path=None, dry_run=False, create_backup=True):
        if download_path is None:
            self.download_path = Path.home() / "Downloads"
        else:
            self.download_path = Path(download_path)
        
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.organize_log = []
        self.backup_path = None
        
        # 整理先フォルダの設定
        self.organize_folders = {
            "images": "01_画像ファイル",
            "videos": "02_動画ファイル", 
            "audio": "03_音声ファイル",
            "documents": "04_文書ファイル",
            "archives": "05_アーカイブ",
            "executables": "06_実行ファイル",
            "code": "07_コードファイル",
            "data": "08_データファイル",
            "fonts": "09_フォントファイル",
            "folders": "10_フォルダ",
            "duplicates": "11_重複ファイル確認",
            "old_files": "12_アーカイブ",
            "large_files": "13_大容量ファイルレビュー",
            "other": "14_その他"
        }
        
        # ファイル分類ルール
        self.file_categories = {
            "images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico', '.heic', '.raw'],
            "videos": ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg'],
            "audio": ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.opus'],
            "documents": ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.odt', '.ods', '.odp'],
            "archives": ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.lz', '.lzh'],
            "executables": ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.app', '.run'],
            "code": ['.py', '.js', '.html', '.css', '.json', '.xml', '.sql', '.sh', '.bat', '.ps1', '.cpp', '.c', '.java'],
            "data": ['.csv', '.json', '.xml', '.sql', '.db', '.sqlite', '.xlsx', '.accdb'],
            "fonts": ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
            "other": []
        }

    def load_analysis_report(self, report_file="download_analysis_report.json"):
        """分析レポートを読み込み"""
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ 分析レポートが見つかりません: {report_file}")
            print("先に download_folder_analyzer.py を実行してください")
            return None

    def create_minimal_backup(self):
        """最小限のバックアップ（移動ログのみ）を作成"""
        if not self.create_backup or self.dry_run:
            return True
            
        print("[INFO] 最小限のバックアップ（移動ログ）を作成中...")
        
        try:
            # 移動ログファイルのみ作成（容量節約）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = self.download_path.parent / f"Downloads_organize_log_{timestamp}.txt"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"ダウンロードフォルダ整理ログ - {datetime.now().isoformat()}\n")
                f.write("="*60 + "\n")
                f.write("注意: このログは移動前の状態を記録しています\n")
                f.write("ファイルは移動のみで削除は行いません\n\n")
                
                # 現在のファイル一覧を記録
                f.write("整理前のファイル一覧:\n")
                f.write("-" * 40 + "\n")
                for item in self.download_path.iterdir():
                    if item.is_file():
                        f.write(f"{item.name}\n")
            
            print(f"  [SUCCESS] 移動ログを作成しました: {log_file.name}")
            print("  [INFO] 容量節約のため、ファイルのコピーは行いません")
            print("  [INFO] ファイルは移動のみで削除されません")
            return True
            
        except Exception as e:
            print(f"  [ERROR] ログ作成エラー: {e}")
            print("  [WARNING] ログなしで続行しますか？ (y/N)")
            response = input().strip().lower()
            return response in ['y', 'yes']

    def create_organize_folders(self):
        """整理用フォルダを作成"""
        print("[INFO] 整理用フォルダを作成中...")
        
        for folder_name, folder_display in self.organize_folders.items():
            folder_path = self.download_path / folder_display
            
            if not self.dry_run:
                folder_path.mkdir(exist_ok=True)
                print(f"  [SUCCESS] {folder_display}")
            else:
                print(f"  [DRY RUN] {folder_display} を作成予定")

    def organize_by_category(self, analysis_report):
        """ファイルをカテゴリ別に整理"""
        print("\n[INFO] ファイルをカテゴリ別に整理中...")
        
        moved_count = 0
        
        # 整理用フォルダ名のリストを作成（移動対象から除外）
        organize_folder_names = set(self.organize_folders.values())
        
        for item in self.download_path.iterdir():
            if (not item.name.startswith('.') and 
                item.name not in organize_folder_names):
                
                if item.is_file():
                    # ファイルの場合：カテゴリ別に分類
                    category = self._get_file_category(item)
                    target_folder = self.download_path / self.organize_folders[category]
                elif item.is_dir():
                    # フォルダの場合：フォルダ専用カテゴリに移動
                    category = "folders"
                    target_folder = self.download_path / self.organize_folders["folders"]
                else:
                    # その他の場合：その他フォルダに移動
                    category = "other"
                    target_folder = self.download_path / self.organize_folders["other"]
                
                try:
                    self._move_item(item, target_folder)
                    moved_count += 1
                    
                    if moved_count % 50 == 0:
                        print(f"  [INFO] {moved_count}個の項目を処理済み...")
                        
                except Exception as e:
                    self.organize_log.append(f"移動エラー: {item.name} - {e}")
        
        print(f"[SUCCESS] {moved_count}個の項目（ファイル・フォルダ）を整理しました")
        return moved_count

    def _get_file_category(self, file_path):
        """ファイルのカテゴリを判定"""
        ext = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if ext in extensions:
                return category
        
        return "other"

    def _move_item(self, source_path, target_folder):
        """ファイルまたはフォルダを移動（重複時は名前を変更）"""
        if self.dry_run:
            item_type = "フォルダ" if source_path.is_dir() else "ファイル"
            print(f"  [DRY RUN] {item_type}: {source_path.name} → {target_folder.name}/")
            return
        
        target_path = target_folder / source_path.name
        
        # 同名項目が存在する場合は番号を付ける
        counter = 1
        while target_path.exists():
            if source_path.is_dir():
                # フォルダの場合
                target_path = target_folder / f"{source_path.name}_{counter}"
            else:
                # ファイルの場合
                stem = source_path.stem
                suffix = source_path.suffix
                target_path = target_folder / f"{stem}_{counter}{suffix}"
            counter += 1
        
        shutil.move(str(source_path), str(target_path))
        
        item_type = "フォルダ" if source_path.is_dir() else "ファイル"
        self.organize_log.append(f"移動完了: {item_type} {source_path.name} → {target_folder.name}/")

    def organize_duplicates(self, analysis_report):
        """重複ファイルを専用フォルダに移動（削除は行わない）"""
        print("\n[INFO] 重複ファイルを専用フォルダに移動中...")
        
        duplicate_folder = self.download_path / "11_重複ファイル確認"
        if not self.dry_run:
            duplicate_folder.mkdir(exist_ok=True)
        
        moved_count = 0
        total_size = 0
        
        for duplicate_group in analysis_report.get('duplicate_files', []):
            if len(duplicate_group['files']) > 1:
                # 最初のファイルをそのまま残し、他を重複フォルダに移動
                keep_file = duplicate_group['files'][0]
                move_files = duplicate_group['files'][1:]
                
                print(f"  重複グループ: {keep_file['name']} (他{len(move_files)}個を移動)")
                
                # グループ用サブフォルダを作成
                group_folder = duplicate_folder / f"重複グループ_{len(move_files) + 1}個_{keep_file['name'][:20]}"
                if not self.dry_run:
                    group_folder.mkdir(exist_ok=True)
                
                for file_info in move_files:
                    file_path = Path(file_info['path'])
                    
                    if file_path.exists():
                        if not self.dry_run:
                            target_path = group_folder / file_info['name']
                            # 同名ファイルが存在する場合は番号を付ける
                            counter = 1
                            while target_path.exists():
                                stem = Path(file_info['name']).stem
                                suffix = Path(file_info['name']).suffix
                                target_path = group_folder / f"{stem}_重複{counter}{suffix}"
                                counter += 1
                            
                            shutil.move(str(file_path), str(target_path))
                            self.organize_log.append(f"重複ファイル移動: {file_info['name']} → 重複フォルダ")
                            moved_count += 1
                            total_size += file_info['size']
                        else:
                            print(f"    [DRY RUN] 移動予定: {file_info['name']} → 重複フォルダ")
        
        if moved_count > 0:
            print(f"[SUCCESS] {moved_count}個の重複ファイルを専用フォルダに移動しました")
            print(f"[INFO] 移動した容量: {self._format_size(total_size)}")
            print(f"[INFO] 確認フォルダ: {duplicate_folder.name}")
            print("   [WARNING] 重要: 不要な重複ファイルは手動で削除してください")
        
        return moved_count, total_size

    def archive_old_files(self, analysis_report, days_threshold=365):
        """古いファイルとフォルダをアーカイブ"""
        print(f"\n[INFO] {days_threshold}日以上古いファイル・フォルダをアーカイブ中...")
        
        archive_folder = self.download_path / "12_アーカイブ"
        if not self.dry_run:
            archive_folder.mkdir(exist_ok=True)
        
        archived_count = 0
        
        # 古いファイルをアーカイブ
        for old_file in analysis_report.get('old_files', []):
            if old_file['days_old'] >= days_threshold:
                file_path = self.download_path / old_file['name']
                
                if file_path.exists() and file_path.is_file():
                    if not self.dry_run:
                        shutil.move(str(file_path), str(archive_folder / old_file['name']))
                        self.organize_log.append(f"アーカイブ: {old_file['name']}")
                        archived_count += 1
                    else:
                        print(f"  [DRY RUN] アーカイブ予定: {old_file['name']}")
        
        # 古いフォルダもアーカイブ（フォルダ内のファイルが少ない場合）
        if "folders" in analysis_report:
            for folder in analysis_report["folders"]:
                folder_path = self.download_path / folder['name']
                
                if folder_path.exists() and folder_path.is_dir():
                    # フォルダの最終更新日を確認
                    try:
                        folder_mtime = datetime.fromtimestamp(folder_path.stat().st_mtime)
                        days_old = (datetime.now() - folder_mtime).days
                        
                        # 古くて小さなフォルダ（5MB未満、ファイル数10個以下）をアーカイブ
                        if (days_old >= days_threshold and 
                            folder['size_mb'] < 5 and 
                            folder['file_count'] <= 10):
                            
                            if not self.dry_run:
                                shutil.move(str(folder_path), str(archive_folder / folder['name']))
                                self.organize_log.append(f"アーカイブ: フォルダ {folder['name']}")
                                archived_count += 1
                            else:
                                print(f"  [DRY RUN] アーカイブ予定: フォルダ {folder['name']} ({folder['file_count']}ファイル)")
                    except Exception as e:
                        print(f"  [WARNING] フォルダ分析エラー: {folder['name']} - {e}")
        
        print(f"[SUCCESS] {archived_count}個の古いファイル・フォルダをアーカイブしました")
        return archived_count

    def review_large_files(self, analysis_report, size_threshold_mb=100):
        """大容量ファイルとフォルダをレビュー用フォルダに移動"""
        print(f"\n[INFO] {size_threshold_mb}MB以上の大容量ファイル・フォルダをレビュー用フォルダに移動...")
        
        review_folder = self.download_path / "13_大容量ファイルレビュー"
        if not self.dry_run:
            review_folder.mkdir(exist_ok=True)
        
        moved_count = 0
        
        # 大容量ファイルを移動
        for large_file in analysis_report.get('large_files', []):
            if large_file['size_mb'] >= size_threshold_mb:
                file_path = self.download_path / large_file['name']
                
                if file_path.exists() and file_path.is_file():
                    if not self.dry_run:
                        shutil.move(str(file_path), str(review_folder / large_file['name']))
                        self.organize_log.append(f"大容量ファイル移動: {large_file['name']}")
                        moved_count += 1
                    else:
                        print(f"  [DRY RUN] 移動予定: {large_file['name']} ({large_file['size_mb']}MB)")
        
        # 大容量フォルダも移動（50MB以上）
        if "folders" in analysis_report:
            for folder in analysis_report["folders"]:
                if folder['size_mb'] >= 50:  # フォルダは50MB以上で移動
                    folder_path = self.download_path / folder['name']
                    
                    if folder_path.exists() and folder_path.is_dir():
                        if not self.dry_run:
                            shutil.move(str(folder_path), str(review_folder / folder['name']))
                            self.organize_log.append(f"大容量フォルダ移動: {folder['name']}")
                            moved_count += 1
                        else:
                            print(f"  [DRY RUN] 移動予定: フォルダ {folder['name']} ({folder['size_mb']}MB, {folder['file_count']}ファイル)")
        
        print(f"[SUCCESS] {moved_count}個の大容量ファイル・フォルダをレビューフォルダに移動しました")
        return moved_count

    def generate_organize_report(self):
        """整理レポートを生成"""
        print("\n" + "="*60)
        print("[REPORT] 整理作業レポート")
        print("="*60)
        
        print(f"[INFO] 実行ログ ({len(self.organize_log)}件):")
        for log_entry in self.organize_log[-10:]:  # 最新10件を表示
            print(f"  - {log_entry}")
        
        if len(self.organize_log) > 10:
            print(f"  ... 他{len(self.organize_log) - 10}件")
        
        # ログをファイルに保存
        log_file = f"organize_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"ダウンロードフォルダ整理ログ - {datetime.now().isoformat()}\n")
            f.write("="*60 + "\n\n")
            for log_entry in self.organize_log:
                f.write(f"{log_entry}\n")
        
        print(f"\n[INFO] 詳細ログを保存しました: {log_file}")

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

    def run_full_organize(self, analysis_report_file="download_analysis_report.json"):
        """完全な整理プロセスを実行"""
        print("[INFO] ダウンロードフォルダ整理を開始します")
        print(f"対象フォルダ: {self.download_path}")
        print(f"DRY RUN モード: {'ON' if self.dry_run else 'OFF'}")
        
        # 分析レポートを読み込み
        analysis_report = self.load_analysis_report(analysis_report_file)
        if not analysis_report:
            return False
        
        # 実行前の確認
        if not self.dry_run:
            print("\n[WARNING] 実行前の確認:")
            print(f"  対象ファイル数: {analysis_report['total_files']:,}個")
            print(f"  総サイズ: {self._format_size(analysis_report['total_size'])}")
            print(f"  重複ファイル: {len(analysis_report['duplicate_files'])}グループ")
            print(f"  古いファイル: {len(analysis_report['old_files'])}個")
            print("\n[INFO] この処理では:")
            print("  - ファイルは移動のみで削除は行いません")
            print("  - 重複ファイルは専用フォルダに移動されます")
            print("  - 古いファイルはアーカイブフォルダに移動されます")
            print("  - 大容量ファイルはレビューフォルダに移動されます")
            print("\n続行しますか？ (y/N)")
            
            response = input().strip().lower()
            if response not in ['y', 'yes']:
                print("[INFO] 処理を中止しました")
                return False
        
        # 最小限のバックアップ（ログのみ）を作成
        if not self.create_minimal_backup():
            print("[ERROR] バックアップ作成に失敗しました。処理を中止します。")
            return False
        
        # 整理用フォルダを作成
        self.create_organize_folders()
        
        # 各整理作業を実行
        self.organize_by_category(analysis_report)
        self.organize_duplicates(analysis_report)
        self.archive_old_files(analysis_report)
        self.review_large_files(analysis_report)
        
        # レポートを生成
        self.generate_organize_report()
        
        print("\n[SUCCESS] 整理作業が完了しました！")
        if self.dry_run:
            print("[INFO] 実際に実行する場合は --dry-run フラグを外してください")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="ダウンロードフォルダ整理ツール")
    parser.add_argument("--path", help="ダウンロードフォルダのパス")
    parser.add_argument("--report", default="download_analysis_report.json", help="分析レポートファイル名")
    parser.add_argument("--dry-run", action="store_true", help="実際の移動は行わず、実行内容のみ表示")
    
    args = parser.parse_args()
    
    organizer = DownloadFolderOrganizer(args.path, args.dry_run)
    organizer.run_full_organize(args.report)

if __name__ == "__main__":
    main()
