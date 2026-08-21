import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import numpy as np
import math
import random
import copy
import threading
import time
import itertools
import gc
import shutil

LANGUAGES = {
    "zh_CN": {
        "title": "炼药锅颜色计算器",
        "current_status": "当前状态",
        "version": "版本:",
        "level": "填充层数:",
        "current_blend": "当前混合色:",
        "target_color": "目标色:",
        "delta_e": "ΔE:",
        "no_dye": "未添加染料",
        "sequence": "染料序列 (最多20个)",
        "clear": "清空序列",
        "dye_times": "染料有效使用次数",
        "dye_options": "可选染料",
        "export": "导出图片",
        "idle": "空闲。",
        "calculating": "序列计算中...",
        "done": "计算完成。",
        "migrating": "序列迁移中...",
        "migration_done": "迁移完成。",
        "export_success": "图片已保存在 {}",
        "error_no_image": "错误：没有图片可导出",
        "error_process": "错误：图片处理失败",
        "error": "错误：{}",
        "calc_sequence": "计算染料序列",
        "based_on": "(基于目标色)",
        "max_warning": "染料序列已达到最大容量 {} 个！",
        "gen_failed": "序列生成失败",
        "invalid_value": "无效值",
        "invalid_input": "请输入有效的数值",
        "invalid_number": "请输入有效的数字",
        "confirm": "确定",
        "cancel": "取消",
        "generating": "生成中...",
        "tip": "提示",
        "language": "语言:",
        "white": "白色",
        "orange": "橙色",
        "magenta": "品红",
        "light_blue": "淡蓝",
        "yellow": "黄色",
        "lime": "黄绿",
        "pink": "粉红",
        "gray": "灰色",
        "light_gray": "淡灰",
        "cyan": "青色",
        "purple": "紫色",
        "blue": "蓝色",
        "brown": "棕色",
        "green": "绿色",
        "red": "红色",
        "black": "黑色",
        "batch_render": "批量渲染",
        "batch_render_title": "批量渲染设置",
        "sequence_length": "序列长度:",
        "from_length": "从",
        "to_length": "到",
        "select_version": "选择版本:",
        "select_level": "选择层数:",
        "start_render": "开始渲染",
        "rendering": "渲染中...",
        "render_complete": "渲染完成！共生成 {} 张图片",
        "render_progress": "渲染进度: {}/{}",
        "select_all": "全选",
        "deselect_all": "取消全选",
        "exclude_duplicates": "忽略长度2序列的顺序颠倒",
        "render_settings": "渲染设置",
        "duplicate_hint": "仅对序列长度为2时有效（忽略颜色顺序颠倒）",
        "duplicate_disabled_hint": "当前长度范围不包含2，此选项无效",
        "invalid": "无效的操作：没有改变既有颜色。"
    },
    "zh_TW": {
        "title": "煉藥鍋顏色計算器",
        "current_status": "目前狀態",
        "version": "版本:",
        "level": "填充層數:",
        "current_blend": "目前混合色:",
        "target_color": "目標色:",
        "delta_e": "ΔE:",
        "no_dye": "未添加染料",
        "sequence": "染料序列 (最多20個)",
        "clear": "清空序列",
        "dye_times": "染料有效使用次數",
        "dye_options": "可選染料",
        "export": "匯出圖片",
        "idle": "空閒。",
        "calculating": "序列計算中...",
        "done": "計算完成。",
        "migrating": "序列遷移中...",
        "migration_done": "遷移完成。",
        "export_success": "圖片已保存在 {}",
        "error_no_image": "錯誤：沒有圖片可匯出",
        "error_process": "錯誤：圖片處理失敗",
        "error": "錯誤：{}",
        "calc_sequence": "計算染料序列",
        "based_on": "(基於目標色)",
        "max_warning": "染料序列已達到最大容量 {} 個！",
        "gen_failed": "序列生成失敗",
        "invalid_value": "無效值",
        "invalid_input": "請輸入有效的數值",
        "invalid_number": "請輸入有效的數字",
        "confirm": "確定",
        "cancel": "取消",
        "generating": "生成中...",
        "tip": "提示",
        "language": "語言:",
        "white": "白色",
        "orange": "橙色",
        "magenta": "品紅",
        "light_blue": "淡藍",
        "yellow": "黃色",
        "lime": "黃綠",
        "pink": "粉紅",
        "gray": "灰色",
        "light_gray": "淡灰",
        "cyan": "青色",
        "purple": "紫色",
        "blue": "藍色",
        "brown": "棕色",
        "green": "綠色",
        "red": "紅色",
        "black": "黑色",
        "batch_render": "批量渲染",
        "batch_render_title": "批量渲染設置",
        "sequence_length": "序列長度:",
        "from_length": "從",
        "to_length": "到",
        "select_version": "選擇版本:",
        "select_level": "選擇層數:",
        "start_render": "開始渲染",
        "rendering": "渲染中...",
        "render_complete": "渲染完成！共生成 {} 張圖片",
        "render_progress": "渲染進度: {}/{}",
        "select_all": "全選",
        "deselect_all": "取消全選",
        "exclude_duplicates": "忽略長度2序列的順序顛倒",
        "render_settings": "渲染設置",
        "duplicate_hint": "僅對序列長度為2時有效（忽略顏色順序顛倒）",
        "duplicate_disabled_hint": "目前長度範圍不包含2，此選項無效",
        "invalid": "無效的操作：沒有改變既有顏色。"
    },
    "ja_JP": {
        "title": "大釜色計算機",
        "current_status": "現在の状態",
        "version": "バージョン:",
        "level": "充填層数:",
        "current_blend": "現在の混合色:",
        "target_color": "目標色:",
        "delta_e": "ΔE:",
        "no_dye": "染料未追加",
        "sequence": "染料シーケンス (最大20個)",
        "clear": "シーケンスをクリア",
        "dye_times": "染料有効使用回数",
        "dye_options": "染料選択",
        "export": "画像をエクスポート",
        "idle": "アイドル。",
        "calculating": "シーケンス計算中...",
        "done": "計算完了。",
        "migrating": "シーケンス移行中...",
        "migration_done": "移行完了。",
        "export_success": "画像を保存しました: {}",
        "error_no_image": "エラー：画像がありません",
        "error_process": "エラー：画像処理失敗",
        "error": "エラー：{}",
        "calc_sequence": "染料シーケンスを計算",
        "based_on": "(目標色に基づく)",
        "max_warning": "染料シーケンスは最大容量 {} 個に達しました！",
        "gen_failed": "シーケンス生成失敗",
        "invalid_value": "無効な値",
        "invalid_input": "有効な数値を入力してください",
        "invalid_number": "有効な数値を入力してください",
        "confirm": "確定",
        "cancel": "キャンセル",
        "generating": "生成中...",
        "tip": "ヒント",
        "language": "言語:",
        "white": "白",
        "orange": "オレンジ",
        "magenta": "マゼンタ",
        "light_blue": "水色",
        "yellow": "黄色",
        "lime": "黄緑",
        "pink": "ピンク",
        "gray": "灰色",
        "light_gray": "薄灰色",
        "cyan": "シアン",
        "purple": "紫",
        "blue": "青",
        "brown": "茶",
        "green": "緑",
        "red": "赤",
        "black": "黒",
        "batch_render": "バッチレンダリング",
        "batch_render_title": "バッチレンダリング設定",
        "sequence_length": "シーケンス長:",
        "from_length": "から",
        "to_length": "まで",
        "select_version": "バージョン選択:",
        "select_level": "レベル選択:",
        "start_render": "レンダリング開始",
        "rendering": "レンダリング中...",
        "render_complete": "レンダリング完了！ {} 枚の画像を生成しました",
        "render_progress": "レンダリング進捗: {}/{}",
        "select_all": "すべて選択",
        "deselect_all": "すべて解除",
        "exclude_duplicates": "長さ2シーケンスの順序逆転を無視",
        "render_settings": "レンダリング設定",
        "duplicate_hint": "シーケンス長が2の場合のみ有効（色の順序逆転を無視）",
        "duplicate_disabled_hint": "現在の長さ範囲に2が含まれていません、このオプションは無効です",
        "invalid": "無効な操作：既存の色は変更されていません。"
    },
    "en_US": {
        "title": "Cauldron Color Calculator",
        "current_status": "Current Status",
        "version": "Version:",
        "level": "Fill Level:",
        "current_blend": "Current Blend:",
        "target_color": "Target Color:",
        "delta_e": "ΔE:",
        "no_dye": "No dye added",
        "sequence": "Dye Sequence (max 20)",
        "clear": "Clear Sequence",
        "dye_times": "Dye Usage Count",
        "dye_options": "Dye Options",
        "export": "Export Image",
        "idle": "Idle.",
        "calculating": "Calculating sequence...",
        "done": "Calculation complete.",
        "migrating": "Migrating sequence...",
        "migration_done": "Migration complete.",
        "export_success": "Image saved at {}",
        "error_no_image": "Error: No image to export",
        "error_process": "Error: Image processing failed",
        "error": "Error: {}",
        "calc_sequence": "Calculate Dye Sequence",
        "based_on": "(based on target color)",
        "max_warning": "Dye sequence has reached maximum capacity of {}!",
        "gen_failed": "Sequence generation failed",
        "invalid_value": "Invalid Value",
        "invalid_input": "Please enter a valid value",
        "invalid_number": "Please enter a valid number",
        "confirm": "Confirm",
        "cancel": "Cancel",
        "generating": "Generating...",
        "tip": "Tip",
        "language": "Language:",
        "white": "White",
        "orange": "Orange",
        "magenta": "Magenta",
        "light_blue": "Light Blue",
        "yellow": "Yellow",
        "lime": "Lime",
        "pink": "Pink",
        "gray": "Gray",
        "light_gray": "Light Gray",
        "cyan": "Cyan",
        "purple": "Purple",
        "blue": "Blue",
        "brown": "Brown",
        "green": "Green",
        "red": "Red",
        "black": "Black",
        "batch_render": "Batch Render",
        "batch_render_title": "Batch Render Settings",
        "sequence_length": "Sequence Length:",
        "from_length": "From",
        "to_length": "To",
        "select_version": "Select Version:",
        "select_level": "Select Level:",
        "start_render": "Start Render",
        "rendering": "Rendering...",
        "render_complete": "Render complete! Generated {} images",
        "render_progress": "Render progress: {}/{}",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "exclude_duplicates": "Ignore reversed order for length-2 sequences",
        "render_settings": "Render Settings",
        "duplicate_hint": "Only effective for sequences of length 2 (ignores color order reversal)",
        "duplicate_disabled_hint": "Current length range does not include 2, this option is disabled",
        "invalid": "Invalid operation: no existing colors were changed."
    }
}


class ImageBlendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("炼药锅颜色计算器")
        self.root.geometry("1450x1030")
        
        self.current_lang = "zh_CN"
        self.lang = LANGUAGES[self.current_lang]
        
        self.hex_color = tk.StringVar(value="#FFFFFF")
        self.current_image_index = 4
        self.image_size = (300, 300)
        
        self.color_sequence = []
        self.current_blend_color = (255, 255, 255)
        self.max_sequence_size = 20
        
        self.default_color = "#345159"
        self.current_version = 1
        
        self.target_color = (255, 255, 255)
        self.target_hex = "#FFFFFF"
        self.use_target = False
        
        self.is_generating = False
        self.is_migrating = False
        self.is_batch_rendering = False
        self.batch_cancelled = False
        self.status_timer = None
        
        self.color_data = [
            ("#F0F0F0", "白色", "white"),
            ("#9D9D97", "淡灰", "light_gray"),
            ("#474F52", "灰色", "gray"),
            ("#1D1D21", "黑色", "black"),
            ("#835432", "棕色", "brown"),
            ("#B02E26", "红色", "red"),
            ("#F9801D", "橙色", "orange"),
            ("#FED83D", "黄色", "yellow"),
            ("#80C71F", "黄绿", "lime"),
            ("#5E7C16", "绿色", "green"),
            ("#169C9C", "青色", "cyan"),
            ("#3AB3DA", "淡蓝", "light_blue"),
            ("#3C44AA", "蓝色", "blue"),
            ("#8932B8", "紫色", "purple"),
            ("#C74EBD", "品红", "magenta"),
            ("#F38BAA", "粉红", "pink")
        ]
        
        self.color_names = {
            "#F0F0F0": "white",
            "#9D9D97": "light_gray",
            "#474F52": "gray",
            "#1D1D21": "black",
            "#835432": "brown",
            "#B02E26": "red",
            "#F9801D": "orange",
            "#FED83D": "yellow",
            "#80C71F": "lime",
            "#5E7C16": "green",
            "#169C9C": "cyan",
            "#3AB3DA": "light_blue",
            "#3C44AA": "blue",
            "#8932B8": "purple",
            "#C74EBD": "magenta",
            "#F38BAA": "pink"
        }
        
        self.color_order = [
            "White", "Light_Gray", "Gray", "Black",
            "Brown", "Red", "Orange", "Yellow",
            "Lime", "Green", "Cyan", "Light_Blue",
            "Blue", "Purple", "Magenta", "Pink"
        ]
        
        self.color_abbr = {
            "white": "Wh",
            "light_gray": "Lgr",
            "gray": "Gr",
            "black": "Bk",
            "brown": "Br",
            "red": "Red",
            "orange": "Org",
            "yellow": "Yl",
            "lime": "Lm",
            "green": "Grn",
            "cyan": "Cy",
            "light_blue": "Lbl",
            "blue": "Bl",
            "purple": "Prp",
            "magenta": "Mag",
            "pink": "Pk"
        }
        
        self.color_times = {
            "white": 0,
            "light_gray": 0,
            "gray": 0,
            "black": 0,
            "brown": 0,
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "lime": 0,
            "green": 0,
            "cyan": 0,
            "light_blue": 0,
            "blue": 0,
            "purple": 0,
            "magenta": 0,
            "pink": 0
        }
        
        self.color_sort_order = {
            "white": 0,
            "light_gray": 1,
            "gray": 2,
            "black": 3,
            "brown": 4,
            "red": 5,
            "orange": 6,
            "yellow": 7,
            "lime": 8,
            "green": 9,
            "cyan": 10,
            "light_blue": 11,
            "blue": 12,
            "purple": 13,
            "magenta": 14,
            "pink": 15
        }
        
        self.image_names = [
            "Water_Level2.png", 
            "Water_Level3.png",
            "Water_Level4.png",
            "Water_Level5.png",
            "Water_Level6.png"
        ]
        
        self.version_image_paths = {
            1: os.path.join("textures", "water", "be1", "dye"),
            3: os.path.join("textures", "water", "be2-5,7"),
            4: os.path.join("textures", "water", "be2-5,7"),
            5: os.path.join("textures", "water", "be2-5,7"),
            6: os.path.join("textures", "water", "be6"),
            7: os.path.join("textures", "water", "be2-5,7")
        }
        
        self.version_image_paths_no_dye = {
            1: os.path.join("textures", "water", "be1", "nodye")
        }
        
        self.version_dye_paths = {
            1: os.path.join("textures", "dye", "be1"),
            3: os.path.join("textures", "dye", "be3-6"),
            4: os.path.join("textures", "dye", "be3-6"),
            5: os.path.join("textures", "dye", "be3-6"),
            6: os.path.join("textures", "dye", "be3-6"),
            7: os.path.join("textures", "dye", "be7")
        }
        
        self.version_backgrounds = {
            1: os.path.join("textures", "cauldron", "Cauldron_BE1.png"),
            3: os.path.join("textures", "cauldron", "Cauldron_BE1.png"),
            4: os.path.join("textures", "cauldron", "Cauldron_BE2.png"),
            5: os.path.join("textures", "cauldron", "Cauldron_BE3.png"),
            6: os.path.join("textures", "cauldron", "Cauldron_BE3.png"),
            7: os.path.join("textures", "cauldron", "Cauldron_BE3.png")
        }
        
        self.background_path = os.path.join("textures", "cauldron", "Cauldron_BE1.png")
        
        self.images = []
        self.background_image = None
        self.dye_images = {}
        self.dye_buttons = []
        self.dye_icon_labels = []
        self.all_buttons = []
        
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.load_images()
        self.load_background()
        self.load_dye_images()
        
        self.create_widgets()
        
        self.root.after(100, self.update_display)
        
    def set_status(self, text, auto_reset=False):
        if self.status_timer:
            self.root.after_cancel(self.status_timer)
            self.status_timer = None
        self.status_var.set(text)
        if auto_reset:
            self.status_timer = self.root.after(2000, lambda: self.set_status(self.lang["idle"]))
    
    def set_buttons_enabled(self, enabled):
        state = 'normal' if enabled else 'disabled'
        for btn in self.all_buttons:
            try:
                btn.config(state=state)
            except:
                pass
    
    def load_images(self):
        default_img = Image.new('RGBA', self.image_size, color=(128, 128, 128, 255))
        self.images = []
        
        if self.current_version == 1:
            if self.color_sequence:
                img_dir = self.version_image_paths.get(self.current_version, os.path.join("textures", "water", "be1", "dye"))
            else:
                img_dir = self.version_image_paths_no_dye.get(self.current_version, os.path.join("textures", "water", "be1", "nodye"))
        else:
            img_dir = self.version_image_paths.get(self.current_version, os.path.join("textures", "water", "be2-5,7"))
        
        for name in self.image_names:
            path = os.path.join(img_dir, name)
            try:
                if os.path.exists(path):
                    img = Image.open(path).convert('RGBA')
                    img = self.resize_image(img, self.image_size[0], self.image_size[1])
                else:
                    img = default_img.copy()
                    draw = ImageDraw.Draw(img)
                    draw.text((100, 130), f"请替换:\n{path}", fill=(255, 255, 255, 255))
                self.images.append(img)
            except Exception:
                img = default_img.copy()
                self.images.append(img)
    
    def reload_images(self):
        self.load_images()
        if self.current_image_index >= len(self.images):
            self.current_image_index = len(self.images) - 1
        self.update_display()
    
    def load_background(self):
        default_bg = Image.new('RGBA', self.image_size, color=(200, 200, 200, 255))
        try:
            bg_path = self.version_backgrounds.get(self.current_version, os.path.join("textures", "cauldron", "Cauldron_BE1.png"))
            if os.path.exists(bg_path):
                self.background_image = Image.open(bg_path).convert('RGBA')
                self.background_image = self.resize_image(self.background_image, 
                                                          self.image_size[0], 
                                                          self.image_size[1])
            else:
                self.background_image = default_bg.copy()
                draw = ImageDraw.Draw(self.background_image)
                draw.text((100, 130), f"请替换:\n{bg_path}", fill=(0, 0, 0, 255))
        except Exception:
            self.background_image = default_bg.copy()
    
    def get_dye_filename(self, english_name):
        if self.current_version == 1:
            return f"dye_powder_{english_name}.png"
        else:
            return f"{english_name}_dye.png"
    
    def get_english_name(self, hex_val):
        for h, _, en in self.color_data:
            if h == hex_val:
                return en
        return None
    
    def get_color_abbr(self, english_name):
        return self.color_abbr.get(english_name, english_name[:2])
    
    def get_color_full_name(self, english_name):
        full_names = {
            "white": "White",
            "light_gray": "Light_Gray",
            "gray": "Gray",
            "black": "Black",
            "brown": "Brown",
            "red": "Red",
            "orange": "Orange",
            "yellow": "Yellow",
            "lime": "Lime",
            "green": "Green",
            "cyan": "Cyan",
            "light_blue": "Light_Blue",
            "blue": "Blue",
            "purple": "Purple",
            "magenta": "Magenta",
            "pink": "Pink"
        }
        return full_names.get(english_name, english_name)
    
    def get_display_color_name(self, english_name):
        color_name_map = {
            "white": self.lang["white"],
            "light_gray": self.lang["light_gray"],
            "gray": self.lang["gray"],
            "black": self.lang["black"],
            "brown": self.lang["brown"],
            "red": self.lang["red"],
            "orange": self.lang["orange"],
            "yellow": self.lang["yellow"],
            "lime": self.lang["lime"],
            "green": self.lang["green"],
            "cyan": self.lang["cyan"],
            "light_blue": self.lang["light_blue"],
            "blue": self.lang["blue"],
            "purple": self.lang["purple"],
            "magenta": self.lang["magenta"],
            "pink": self.lang["pink"]
        }
        return color_name_map.get(english_name, english_name)
    
    def get_color_name_by_hex(self, hex_val):
        english_name = self.color_names.get(hex_val.upper(), hex_val)
        return self.get_display_color_name(english_name)
    
    def load_dye_images(self):
        self.dye_images = {}
        dye_dir = self.version_dye_paths.get(self.current_version, os.path.join("textures", "dye", "be1"))
        
        for hex_val, chinese_name, english_name in self.color_data:
            file_name = self.get_dye_filename(english_name)
            path = os.path.join(dye_dir, file_name)
            try:
                if os.path.exists(path):
                    img = Image.open(path).convert('RGBA')
                    img = img.resize((16, 16), Image.Resampling.LANCZOS)
                    self.dye_images[hex_val] = ImageTk.PhotoImage(img)
                else:
                    r, g, b = self.hex_to_rgb(hex_val)
                    img = Image.new('RGBA', (16, 16), (r, g, b, 255))
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([0, 0, 15, 15], outline=(100, 100, 100), width=1)
                    self.dye_images[hex_val] = ImageTk.PhotoImage(img)
            except Exception:
                r, g, b = self.hex_to_rgb(hex_val)
                img = Image.new('RGBA', (16, 16), (r, g, b, 255))
                draw = ImageDraw.Draw(img)
                draw.rectangle([0, 0, 15, 15], outline=(100, 100, 100), width=1)
                self.dye_images[hex_val] = ImageTk.PhotoImage(img)
    
    def resize_image(self, img, target_width, target_height):
        orig_width, orig_height = img.size
        ratio = min(target_width / orig_width, target_height / orig_height)
        new_width = int(orig_width * ratio)
        new_height = int(orig_height * ratio)
        
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        canvas.paste(resized, (x, y))
        return canvas
    
    def calculate_blend_color(self):
        if not self.color_sequence:
            return self.hex_to_rgb(self.default_color)
        
        if len(self.color_sequence) == 1:
            return self.hex_to_rgb(self.color_sequence[0])
        
        result_r, result_g, result_b = self.hex_to_rgb(self.color_sequence[0])
        
        for color in self.color_sequence[1:]:
            r, g, b = self.hex_to_rgb(color)
            result_r = (result_r + r) // 2
            result_g = (result_g + g) // 2
            result_b = (result_b + b) // 2
        
        return (result_r, result_g, result_b)
    
    def calculate_blend_color_for_sequence(self, seq):
        if not seq:
            return self.hex_to_rgb(self.default_color)
        
        if len(seq) == 1:
            return self.hex_to_rgb(seq[0])
        
        result_r, result_g, result_b = self.hex_to_rgb(seq[0])
        
        for color in seq[1:]:
            r, g, b = self.hex_to_rgb(color)
            result_r = (result_r + r) // 2
            result_g = (result_g + g) // 2
            result_b = (result_b + b) // 2
        
        return (result_r, result_g, result_b)
    
    def calculate_delta_e(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        def rgb_to_lab(r, g, b):
            r = r / 255.0
            g = g / 255.0
            b = b / 255.0
            
            r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
            
            x = r * 0.4124 + g * 0.3576 + b * 0.1805
            y = r * 0.2126 + g * 0.7152 + b * 0.0722
            z = r * 0.0193 + g * 0.1192 + b * 0.9505
            
            x_ref, y_ref, z_ref = 0.95047, 1.0, 1.08883
            
            x = x / x_ref if x / x_ref > 0.008856 else (x / x_ref * 903.3 + 16) / 116
            y = y / y_ref if y / y_ref > 0.008856 else (y / y_ref * 903.3 + 16) / 116
            z = z / z_ref if z / z_ref > 0.008856 else (z / z_ref * 903.3 + 16) / 116
            
            l = 116 * y - 16
            a = 500 * (x - y)
            b_lab = 200 * (y - z)
            
            return l, a, b_lab
        
        l1, a1, b1_lab = rgb_to_lab(r1, g1, b1)
        l2, a2, b2_lab = rgb_to_lab(r2, g2, b2)
        
        delta_l = l1 - l2
        delta_a = a1 - a2
        delta_b = b1_lab - b2_lab
        
        return math.sqrt(delta_l ** 2 + delta_a ** 2 + delta_b ** 2)
    
    def pick_target_color(self):
        color = colorchooser.askcolor(title=self.lang["target_color"], color=self.target_hex)
        if color and color[0] is not None:
            r, g, b = color[0]
            self.target_color = (int(r), int(g), int(b))
            self.target_hex = self.rgb_to_hex(int(r), int(g), int(b))
            self.use_target = True
            self.update_color_display()
    
    def crossover(self, parent1, parent2, available_colors):
        if not parent1 or not parent2:
            return [random.choice(available_colors)]
        
        length = max(len(parent1), len(parent2))
        child = []
        
        for i in range(length):
            if i < len(parent1) and i < len(parent2):
                child.append(parent1[i] if random.random() < 0.5 else parent2[i])
            elif i < len(parent1):
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        
        return child
    
    def mutate(self, seq, available_colors, max_length):
        if not seq:
            return [random.choice(available_colors)]
        
        new_seq = seq.copy()
        
        for i in range(len(new_seq)):
            if random.random() < 0.1:
                new_seq[i] = random.choice(available_colors)
        
        if random.random() < 0.2 and len(new_seq) < max_length:
            new_seq.append(random.choice(available_colors))
        
        if random.random() < 0.2 and len(new_seq) > 1:
            del new_seq[random.randint(0, len(new_seq)-1)]
        
        return new_seq
    
    def auto_generate_sequence(self):
        if self.is_generating:
            return
        
        target_rgb = self.target_color
        available_colors = [h for h, _, _ in self.color_data]
        max_length = 20
        
        self.is_generating = True
        self.set_buttons_enabled(False)
        self.auto_gen_btn.config(text=self.lang["generating"], state='disabled')
        self.set_status(self.lang["calculating"])
        
        def evaluate_sequence_full(seq):
            if not seq:
                return float('inf')
            blend = self.calculate_blend_color_for_sequence(seq)
            color_delta = self.calculate_delta_e(blend, target_rgb)
            return color_delta
        
        def generate():
            def evaluate_sequence(seq):
                if not seq:
                    return float('inf')
                return evaluate_sequence_full(seq)
            
            population_size = 100
            generations = 3000
            elite_size = 5
            tournament_size = 3
            
            def create_individual():
                length = random.randint(1, min(max_length, 8))
                return [random.choice(available_colors) for _ in range(length)]
            
            def crossover_improved(parent1, parent2):
                if len(parent1) < 2 or len(parent2) < 2:
                    return parent1.copy()
                
                pos1 = random.randint(1, len(parent1) - 1)
                pos2 = random.randint(1, len(parent2) - 1)
                
                child = parent1[:pos1] + parent2[pos2:]
                
                if len(child) > max_length:
                    child = child[:max_length]
                if not child:
                    child = [random.choice(available_colors)]
                
                return child
            
            def mutate_improved(seq):
                new_seq = seq.copy()
                
                for i in range(len(new_seq)):
                    if random.random() < 0.08:
                        new_seq[i] = random.choice(available_colors)
                
                if random.random() < 0.15 and len(new_seq) < max_length:
                    new_seq.insert(random.randint(0, len(new_seq)), random.choice(available_colors))
                
                if random.random() < 0.15 and len(new_seq) > 1:
                    del new_seq[random.randint(0, len(new_seq)-1)]
                
                if len(new_seq) > max_length:
                    new_seq = new_seq[:max_length]
                
                return new_seq
            
            def local_search(seq):
                best_seq = seq.copy()
                best_score = evaluate_sequence(best_seq)
                
                for i in range(len(best_seq)):
                    original_color = best_seq[i]
                    for color in random.sample(available_colors, min(5, len(available_colors))):
                        if color == original_color:
                            continue
                        test_seq = best_seq.copy()
                        test_seq[i] = color
                        score = evaluate_sequence(test_seq)
                        if score < best_score:
                            best_score = score
                            best_seq = test_seq
                
                if len(best_seq) < max_length:
                    for color in random.sample(available_colors, min(3, len(available_colors))):
                        test_seq = best_seq + [color]
                        score = evaluate_sequence(test_seq)
                        if score < best_score:
                            best_score = score
                            best_seq = test_seq
                
                if len(best_seq) > 1:
                    for i in range(len(best_seq)):
                        test_seq = best_seq[:i] + best_seq[i+1:]
                        score = evaluate_sequence(test_seq)
                        if score < best_score:
                            best_score = score
                            best_seq = test_seq
                
                return best_seq
            
            population = [create_individual() for _ in range(population_size)]
            best_overall = None
            best_overall_score = float('inf')
            
            no_improvement_count = 0
            
            for generation in range(generations):
                scores = [evaluate_sequence(ind) for ind in population]
                
                sorted_pairs = sorted(zip(scores, population), key=lambda x: x[0])
                current_best_score = sorted_pairs[0][0]
                current_best = sorted_pairs[0][1]
                
                if current_best_score < best_overall_score:
                    best_overall_score = current_best_score
                    best_overall = current_best.copy()
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1
                
                if generation % 100 == 0:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['calculating']} ({generation}/{generations})"))
                
                if best_overall_score < 0.5:
                    break
                
                elite = [ind for _, ind in sorted_pairs[:elite_size]]
                
                new_population = elite.copy()
                
                while len(new_population) < population_size:
                    tournament_indices = random.sample(range(len(population)), tournament_size)
                    tournament_winners = sorted([(scores[i], population[i]) for i in tournament_indices], key=lambda x: x[0])
                    parent1 = tournament_winners[0][1]
                    parent2 = tournament_winners[1][1]
                    
                    child = crossover_improved(parent1, parent2)
                    child = mutate_improved(child)
                    new_population.append(child)
                
                population = new_population
                
                if no_improvement_count > 200:
                    for i in range(population_size // 5):
                        idx = random.randint(0, population_size - 1)
                        population[idx] = create_individual()
                    no_improvement_count = 0
            
            final_scores = [evaluate_sequence(ind) for ind in population]
            final_best_idx = min(range(len(final_scores)), key=lambda i: final_scores[i])
            final_best = population[final_best_idx]
            
            if final_scores[final_best_idx] < best_overall_score:
                best_overall = final_best
                best_overall_score = final_scores[final_best_idx]
            
            if best_overall_score > 1.0:
                refined_seq = local_search(best_overall)
                if evaluate_sequence(refined_seq) < best_overall_score:
                    best_overall = refined_seq
            
            self.root.after(0, lambda: self.apply_generated_sequence(best_overall))
        
        thread = threading.Thread(target=generate)
        thread.daemon = True
        thread.start()
    
    def apply_generated_sequence(self, seq):
        self.is_generating = False
        self.auto_gen_btn.config(text=self.lang["calc_sequence"], state='normal')
        
        if not seq:
            self.set_buttons_enabled(True)
            self.set_status(self.lang["done"], auto_reset=True)
            messagebox.showinfo(self.lang["tip"], self.lang["gen_failed"])
            return
        
        self.color_sequence.clear()
        for key in self.color_times:
            self.color_times[key] = 0
        self.update_times_display()
        self.update_sequence_display()
        self.update_display()
        
        def add_colors_one_by_one():
            for color in seq:
                self.add_color_to_sequence(color)
                time.sleep(0.01)
            
            if self.current_version == 1 and self.color_sequence:
                self.root.after(0, self.reload_images)
            
            self.root.after(0, lambda: self.set_buttons_enabled(True))
            self.root.after(0, lambda: self.set_status(self.lang["done"], auto_reset=True))
        
        thread = threading.Thread(target=add_colors_one_by_one)
        thread.daemon = True
        thread.start()
    
    def get_color_code_for_sort(self, hex_val):
        english_name = self.get_english_name(hex_val)
        return self.color_sort_order.get(english_name, 999)
    
    def sort_two_color_sequence(self, seq):
        if len(seq) != 2:
            return seq
        code1 = self.get_color_code_for_sort(seq[0])
        code2 = self.get_color_code_for_sort(seq[1])
        if code1 <= code2:
            return seq
        else:
            return [seq[1], seq[0]]
    
    def get_valid_sequence(self):
        if not self.color_sequence:
            return []
        
        temp_color = self.hex_to_rgb(self.default_color)
        valid_sequence = []
        
        for color in self.color_sequence:
            r, g, b = self.hex_to_rgb(color)
            new_color = ((temp_color[0] + r) // 2, (temp_color[1] + g) // 2, (temp_color[2] + b) // 2)
            if new_color != temp_color:
                valid_sequence.append(color)
                temp_color = new_color
        
        return valid_sequence
    
    def remove_leading_duplicates(self, seq):
        if not seq or len(seq) <= 1:
            return seq
        
        first_color = seq[0]
        cut_pos = 1
        while cut_pos < len(seq) and seq[cut_pos] == first_color:
            cut_pos += 1
        
        if cut_pos == len(seq):
            return [first_color]
        
        return seq[cut_pos - 1:]
    
    def open_batch_render_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.lang["batch_render_title"])
        dialog.geometry("500x620")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=self.lang["render_settings"], font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        length_frame = ttk.LabelFrame(main_frame, text=self.lang["sequence_length"])
        length_frame.pack(fill=tk.X, pady=5)
        
        length_inner = ttk.Frame(length_frame)
        length_inner.pack(pady=10, padx=10)
        
        ttk.Label(length_inner, text=self.lang["from_length"] + ":").pack(side=tk.LEFT, padx=5)
        from_var = tk.StringVar(value="1")
        from_entry = ttk.Entry(length_inner, textvariable=from_var, width=5)
        from_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(length_inner, text=self.lang["to_length"] + ":").pack(side=tk.LEFT, padx=5)
        to_var = tk.StringVar(value="2")
        to_entry = ttk.Entry(length_inner, textvariable=to_var, width=5)
        to_entry.pack(side=tk.LEFT, padx=5)
        
        version_frame = ttk.LabelFrame(main_frame, text=self.lang["select_version"])
        version_frame.pack(fill=tk.X, pady=5)
        
        version_inner = ttk.Frame(version_frame)
        version_inner.pack(pady=10, padx=10)
        
        version_var = tk.StringVar(value="7")
        version_options = [1, 3, 4, 5, 6, 7]
        for v in version_options:
            rb = ttk.Radiobutton(version_inner, text=f"BE{v}", variable=version_var, value=str(v))
            rb.pack(side=tk.LEFT, padx=5)
        
        level_frame = ttk.LabelFrame(main_frame, text=self.lang["select_level"])
        level_frame.pack(fill=tk.X, pady=5)
        
        level_inner = ttk.Frame(level_frame)
        level_inner.pack(pady=10, padx=10)
        
        level_var = tk.StringVar(value="6")
        for i in range(2, 7):
            rb = ttk.Radiobutton(level_inner, text=f"Level {i}", variable=level_var, value=str(i))
            rb.pack(side=tk.LEFT, padx=5)
        
        options_frame = ttk.LabelFrame(main_frame, text=self.lang["render_settings"])
        options_frame.pack(fill=tk.X, pady=5)
        
        options_inner = ttk.Frame(options_frame)
        options_inner.pack(pady=10, padx=10)
        
        exclude_duplicates_var = tk.BooleanVar(value=True)
        cb_exclude = ttk.Checkbutton(options_inner, text=self.lang["exclude_duplicates"], variable=exclude_duplicates_var)
        cb_exclude.pack(anchor=tk.W)
        
        info_label = ttk.Label(options_inner, 
                               text=self.lang["duplicate_hint"], 
                               font=("Arial", 8), foreground="gray", wraplength=400)
        info_label.pack(anchor=tk.W, pady=(5, 0))
        
        def update_checkbox_state(*args):
            try:
                from_len = int(from_var.get())
                to_len = int(to_var.get())
                if from_len <= 2 <= to_len:
                    cb_exclude.config(state='normal')
                    info_label.config(text=self.lang["duplicate_hint"])
                else:
                    cb_exclude.config(state='disabled')
                    info_label.config(text=self.lang["duplicate_disabled_hint"])
            except ValueError:
                pass
        
        from_var.trace('w', update_checkbox_state)
        to_var.trace('w', update_checkbox_state)
        
        update_checkbox_state()
        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        progress_var = tk.StringVar(value=self.lang["idle"])
        progress_label = ttk.Label(progress_frame, textvariable=progress_var, font=("Arial", 9))
        progress_label.pack()
        
        progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        progress_bar.pack(fill=tk.X, pady=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        def start_batch_render():
            try:
                from_len = int(from_var.get())
                to_len = int(to_var.get())
                if from_len < 1 or to_len > 20 or from_len > to_len:
                    messagebox.showwarning(self.lang["invalid_value"])
                    return
                
                version = int(version_var.get())
                level = int(level_var.get())
                exclude_duplicates = exclude_duplicates_var.get()
                
                dialog.destroy()
                
                self.batch_render(from_len, to_len, version, level, exclude_duplicates)
            except ValueError:
                messagebox.showwarning(self.lang["invalid_value"], self.lang["invalid_number"])
        
        start_btn = ttk.Button(btn_frame, text=self.lang["start_render"], command=start_batch_render, width=15)
        start_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(btn_frame, text=self.lang["cancel"], command=dialog.destroy, width=15)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def generate_filename_for_sequence(self, seq):
        level_num = self.current_image_index + 2
        level_str = f"level_{level_num}"
        be_str = f"BE{self.current_version}"
        
        if not seq:
            if level_num == 6:
                return f"Water_Cauldron_{be_str}"
            else:
                return f"Water_Cauldron_({level_str})_{be_str}"
        
        temp_color = self.hex_to_rgb(self.default_color)
        valid_seq = []
        for color in seq:
            r, g, b = self.hex_to_rgb(color)
            new_color = ((temp_color[0] + r) // 2, (temp_color[1] + g) // 2, (temp_color[2] + b) // 2)
            if new_color != temp_color:
                valid_seq.append(color)
                temp_color = new_color
        
        if not valid_seq:
            if level_num == 6:
                return f"Water_Cauldron_{be_str}"
            else:
                return f"Water_Cauldron_({level_str})_{be_str}"
        
        if len(valid_seq) == 1:
            english_name = self.get_english_name(valid_seq[0])
            full_name = self.get_color_full_name(english_name)
            if level_num == 6:
                return f"{full_name}_Water_Cauldron_{be_str}"
            else:
                return f"{full_name}_Water_Cauldron_({level_str})_{be_str}"
        
        if len(valid_seq) == 2:
            code1 = self.get_color_code_for_sort(valid_seq[0])
            code2 = self.get_color_code_for_sort(valid_seq[1])
            if code1 > code2:
                valid_seq = [valid_seq[1], valid_seq[0]]
        
        abbr_parts = []
        for color in valid_seq:
            english_name = self.get_english_name(color)
            abbr = self.get_color_abbr(english_name)
            abbr_parts.append(abbr)
        
        abbr_string = "-".join(abbr_parts)
        
        if level_num == 6:
            return f"{abbr_string}_Water_Cauldron_{be_str}"
        else:
            return f"{abbr_string}_Water_Cauldron_({level_str})_{be_str}"
    
    def generate_filename(self):
        return self.generate_filename_for_sequence(self.color_sequence)
    
    def batch_render(self, from_len, to_len, version, level, exclude_duplicates):
        if self.is_batch_rendering:
            return
        
        self.is_batch_rendering = True
        self.batch_cancelled = False
        self.set_buttons_enabled(False)
        self.set_status(self.lang["rendering"])
        
        self.current_version = version
        self.version_display.config(text=f"BE{version}")
        self.current_image_index = level - 2
        level_num = self.current_image_index + 2
        self.level_display.config(text=f"Level {level_num}")
        
        self.load_background()
        self.load_dye_images()
        self.update_dye_buttons()
        self.load_images()
        self.update_display()
        
        if from_len == to_len:
            folder_name = f"BE{version}_Level{level}_Len{from_len}"
        else:
            folder_name = f"BE{version}_Level{level}_Len{from_len}-{to_len}"
        
        batch_output_dir = os.path.join(self.output_dir, folder_name)
        if not os.path.exists(batch_output_dir):
            os.makedirs(batch_output_dir)
        
        cache_dir = os.path.join(self.output_dir, ".cache", folder_name)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        
        progress_file = os.path.join(cache_dir, "progress.txt")
        enumerated_file = os.path.join(cache_dir, "enumerated.txt")
        enumerate_progress_file = os.path.join(cache_dir, "enumerate_progress.txt")
        render_progress_file = os.path.join(cache_dir, "render_progress.txt")
        deduped_file = os.path.join(cache_dir, "deduped.txt")
        
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title(self.lang["rendering"])
        progress_dialog.geometry("400x180")
        progress_dialog.transient(self.root)
        
        progress_frame = ttk.Frame(progress_dialog, padding=15)
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        progress_label = ttk.Label(progress_frame, text=self.lang["idle"], font=("Arial", 10))
        progress_label.pack(pady=5)
        
        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=350)
        progress_bar.pack(pady=10)
        
        status_label = ttk.Label(progress_frame, text="", font=("Arial", 8), foreground="gray")
        status_label.pack(pady=5)
        
        def cancel_batch():
            self.batch_cancelled = True
            self.set_status("正在取消...", auto_reset=True)
        
        cancel_btn = ttk.Button(progress_frame, text=self.lang["cancel"], command=cancel_batch, width=15)
        cancel_btn.pack(pady=5)
        
        def update_progress(current, total, seq_info=""):
            try:
                progress_label.config(text=self.lang["render_progress"].format(current, total))
                progress_bar.config(value=(current / total) * 100 if total > 0 else 0)
                status_label.config(text=seq_info)
                progress_dialog.update()
            except:
                pass
        
        def read_progress_state():
            if os.path.exists(progress_file):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        data = {}
                        for line in f:
                            if '=' in line:
                                key, val = line.strip().split('=', 1)
                                data[key] = val
                        state = data.get('state', '')
                        total = int(data.get('total', 0))
                        current_index = int(data.get('current_index', 0))
                        return state, total, current_index
                except:
                    pass
            return '', 0, 0
        
        def write_progress_state(state, total, current_index):
            try:
                with open(progress_file, 'w', encoding='utf-8') as f:
                    f.write(f"state={state}\n")
                    f.write(f"total={total}\n")
                    f.write(f"current_index={current_index}\n")
            except:
                pass
        
        def append_enumerated_sequence(seq):
            try:
                with open(enumerated_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass
        
        def load_enumerated_sequences():
            if os.path.exists(enumerated_file):
                try:
                    sequences = []
                    with open(enumerated_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []
        
        def save_deduped_sequences(sequences):
            try:
                with open(deduped_file, 'w', encoding='utf-8') as f:
                    for seq in sequences:
                        f.write(','.join(seq) + '\n')
            except:
                pass
        
        def load_deduped_sequences():
            if os.path.exists(deduped_file):
                try:
                    sequences = []
                    with open(deduped_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []
        
        def load_enumerate_progress():
            if os.path.exists(enumerate_progress_file):
                try:
                    with open(enumerate_progress_file, 'r', encoding='utf-8') as f:
                        line = f.read().strip()
                        if line:
                            return line.split(',')
                except:
                    pass
            return None
        
        def save_enumerate_progress(seq):
            try:
                with open(enumerate_progress_file, 'w', encoding='utf-8') as f:
                    if seq:
                        f.write(','.join(seq))
                    else:
                        f.write('')
            except:
                pass
        
        def load_render_progress():
            if os.path.exists(render_progress_file):
                try:
                    sequences = []
                    with open(render_progress_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []
        
        def save_render_progress(seq):
            try:
                with open(render_progress_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass
        
        def clear_cache():
            try:
                for f in [progress_file, enumerated_file, enumerate_progress_file, render_progress_file, deduped_file]:
                    if os.path.exists(f):
                        os.remove(f)
                if os.path.exists(cache_dir) and not os.listdir(cache_dir):
                    os.rmdir(cache_dir)
            except:
                pass
        
        def generate_sequences_with_progress(available_colors, from_len, to_len, start_length, start_seq):
            started = False if start_seq is not None else True
            
            for length in range(from_len, to_len + 1):
                if length < start_length:
                    continue
                elif length == start_length and start_seq is not None:
                    found_start = False
                    for seq in itertools.product(available_colors, repeat=length):
                        if not found_start:
                            if list(seq) == start_seq:
                                found_start = True
                                yield list(seq), length
                        else:
                            yield list(seq), length
                else:
                    for seq in itertools.product(available_colors, repeat=length):
                        yield list(seq), length
        
        def render_worker():
            try:
                available_colors = [h for h, _, _ in self.color_data]
                
                state, total, current_index = read_progress_state()
                
                deduped_sequences = load_deduped_sequences()
                
                if deduped_sequences:
                    state = 'rendering'
                    all_sequences = deduped_sequences
                else:
                    all_sequences = load_enumerated_sequences()
                
                enumerate_progress = load_enumerate_progress()
                rendered_sequences = load_render_progress()
                
                old_version = self.current_version
                old_level = self.current_image_index
                old_sequence = self.color_sequence.copy()
                old_times = self.color_times.copy()
                
                if state == 'rendering' and all_sequences:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))
                    
                    start_idx = 0
                    if rendered_sequences:
                        last_rendered = rendered_sequences[-1]
                        for idx, seq in enumerate(all_sequences):
                            if seq == last_rendered:
                                start_idx = idx
                                break
                        if start_idx > 0:
                            rendered_sequences = rendered_sequences[:-1]
                            with open(render_progress_file, 'w', encoding='utf-8') as f:
                                for seq in rendered_sequences:
                                    f.write(','.join(seq) + '\n')
                    
                    total = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({start_idx+1}/{total})"))
                    
                    for idx in range(start_idx, total):
                        if self.batch_cancelled:
                            break
                        
                        seq = all_sequences[idx]
                        seq_names = [self.get_english_name(c) for c in seq]
                        seq_display = ", ".join(seq_names[:3])
                        if len(seq_names) > 3:
                            seq_display += f"... (+{len(seq_names)-3})"
                        
                        if idx % 5 == 0 or idx == total - 1:
                            self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                            self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                            write_progress_state('rendering', total, idx)
                        
                        try:
                            self.color_sequence.clear()
                            for key in self.color_times:
                                self.color_times[key] = 0
                            
                            for color in seq:
                                self.add_color_to_sequence(color)
                            
                            self.update_sequence_display()
                            self.update_times_display()
                            self.update_display()
                            
                            final_img = self.render_single_image()
                            
                            filename = self.generate_filename_for_sequence(seq) + ".png"
                            file_path = os.path.join(batch_output_dir, filename)
                            final_img.save(file_path, 'PNG')
                            
                            del final_img
                            
                            save_render_progress(seq)
                            
                        except Exception as e:
                            print(f"渲染序列 {seq} 失败: {e}")
                        
                        if (idx + 1) % 5 == 0:
                            try:
                                progress_dialog.update()
                            except:
                                pass
                            gc.collect()
                            time.sleep(0.05)
                        
                        time.sleep(0.01)
                    
                    if not self.batch_cancelled:
                        clear_cache()
                        self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                        self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))
                    
                    self.current_version = old_version
                    self.current_image_index = old_level
                    self.color_sequence = old_sequence
                    self.color_times = old_times
                    
                    self.load_background()
                    self.load_dye_images()
                    self.load_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()
                    
                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))
                
                start_length = from_len
                start_seq = None
                
                if enumerate_progress:
                    start_seq = enumerate_progress
                    start_length = len(start_seq)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))
                
                enumerate_count = 0
                if all_sequences:
                    enumerate_count = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))
                
                seq_generator = generate_sequences_with_progress(
                    available_colors, from_len, to_len, start_length, start_seq
                )
                
                for seq, length in seq_generator:
                    if self.batch_cancelled:
                        break
                    
                    enumerate_count += 1
                    
                    if enumerate_count % 10 == 0:
                        save_enumerate_progress(seq)
                        if enumerate_count % 100 == 0:
                            self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))
                    
                    self.color_sequence.clear()
                    for key in self.color_times:
                        self.color_times[key] = 0
                    
                    all_valid = True
                    for color in seq:
                        if not self.add_color_to_sequence(color):
                            all_valid = False
                            break
                    
                    if all_valid and len(self.color_sequence) == len(seq):
                        final_seq = self.color_sequence.copy()
                        if len(final_seq) == 2:
                            final_seq = self.sort_two_color_sequence(final_seq)
                        append_enumerated_sequence(final_seq)
                
                if self.batch_cancelled:
                    self.current_version = old_version
                    self.current_image_index = old_level
                    self.color_sequence = old_sequence
                    self.color_times = old_times
                    
                    self.load_background()
                    self.load_dye_images()
                    self.load_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()
                    
                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return
                
                all_enumerated = load_enumerated_sequences()
                
                if not all_enumerated:
                    self.root.after(0, lambda: self.set_status(self.lang["error"], auto_reset=True))
                    messagebox.showinfo(self.lang["tip"])
                    
                    self.current_version = old_version
                    self.current_image_index = old_level
                    self.color_sequence = old_sequence
                    self.color_times = old_times
                    
                    self.load_background()
                    self.load_dye_images()
                    self.load_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()
                    
                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return
                
                if exclude_duplicates:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))
                    filtered_sequences = []
                    seen_signatures = set()
                    
                    for seq in all_enumerated:
                        if len(seq) == 2:
                            sig = tuple(sorted(seq))
                        else:
                            sig = tuple(seq)
                        
                        if sig not in seen_signatures:
                            seen_signatures.add(sig)
                            filtered_sequences.append(seq)
                    
                    all_sequences = filtered_sequences
                else:
                    all_sequences = all_enumerated
                
                save_deduped_sequences(all_sequences)
                write_progress_state('rendering', len(all_sequences), 0)
                
                if not all_sequences:
                    self.root.after(0, lambda: self.set_status(self.lang["error"], auto_reset=True))
                    messagebox.showinfo(self.lang["tip"])
                    
                    self.current_version = old_version
                    self.current_image_index = old_level
                    self.color_sequence = old_sequence
                    self.color_times = old_times
                    
                    self.load_background()
                    self.load_dye_images()
                    self.load_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()
                    
                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return
                
                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))
                
                total = len(all_sequences)
                for idx, seq in enumerate(all_sequences):
                    if self.batch_cancelled:
                        break
                    
                    seq_names = [self.get_english_name(c) for c in seq]
                    seq_display = ", ".join(seq_names[:3])
                    if len(seq_names) > 3:
                        seq_display += f"... (+{len(seq_names)-3})"
                    
                    if idx % 5 == 0 or idx == total - 1:
                        self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                        self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                        write_progress_state('rendering', total, idx)
                    
                    try:
                        self.color_sequence.clear()
                        for key in self.color_times:
                            self.color_times[key] = 0
                        
                        for color in seq:
                            self.add_color_to_sequence(color)
                        
                        self.update_sequence_display()
                        self.update_times_display()
                        self.update_display()
                        
                        final_img = self.render_single_image()
                        
                        filename = self.generate_filename_for_sequence(seq) + ".png"
                        file_path = os.path.join(batch_output_dir, filename)
                        final_img.save(file_path, 'PNG')
                        
                        del final_img
                        
                        save_render_progress(seq)
                        
                    except Exception as e:
                        print("")
                    
                    if (idx + 1) % 5 == 0:
                        try:
                            progress_dialog.update()
                        except:
                            pass
                        gc.collect()
                        time.sleep(0.05)
                    
                    time.sleep(0.01)
                
                if not self.batch_cancelled:
                    clear_cache()
                    self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                    self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))
                
                self.current_version = old_version
                self.current_image_index = old_level
                self.color_sequence = old_sequence
                self.color_times = old_times
                
                self.load_background()
                self.load_dye_images()
                self.load_images()
                self.update_sequence_display()
                self.update_times_display()
                self.update_display()
                
                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)
                
            except Exception as e:
                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)
                self.root.after(0, lambda: self.set_status(self.lang["error"].format(str(e)), auto_reset=True))
                messagebox.showerror(self.lang["error"], str(e))
        
        thread = threading.Thread(target=render_worker)
        thread.daemon = True
        thread.start()
    
    def calculate_times_for_sequence(self, seq):
        temp_color = self.hex_to_rgb(self.default_color)
        
        for color in seq:
            english_name = self.get_english_name(color)
            r, g, b = self.hex_to_rgb(color)
            
            old_color = temp_color
            temp_color = ((temp_color[0] + r) // 2, (temp_color[1] + g) // 2, (temp_color[2] + b) // 2)
            if old_color != temp_color:
                if english_name and english_name in self.color_times:
                    self.color_times[english_name] += 1
    
    def render_single_image(self):
        level_idx = self.current_image_index
        if level_idx >= len(self.images):
            level_idx = len(self.images) - 1
        
        original_img = self.images[level_idx]
        if original_img.size != self.image_size:
            original_img = self.resize_image(original_img, self.image_size[0], self.image_size[1])
        
        blend_color = self.calculate_blend_color()
        
        if self.current_version == 1 and not self.color_sequence:
            bg = self.background_image.copy()
            if bg.size != self.image_size:
                bg = self.resize_image(bg, self.image_size[0], self.image_size[1])
            return Image.alpha_composite(bg, original_img)
        else:
            fg_r, fg_g, fg_b, fg_a, original_a = self.blend_images_float(original_img, blend_color)
            if fg_r is None:
                return self.background_image.copy()
            return self.composite_with_background((fg_r, fg_g, fg_b), fg_a, original_a)
    
    def change_language(self, lang_code):
        if lang_code in LANGUAGES:
            self.current_lang = lang_code
            self.lang = LANGUAGES[lang_code]
            self.root.title(self.lang["title"])
            
            for code, frame in self.lang_tab_frames.items():
                if code == lang_code:
                    self.right_content = frame
                    break
            
            self.rebuild_content()
            self.update_all_texts()
            self.update_color_display()
            self.update_display()
            self.update_times_display()
            self.update_sequence_display()
    
    def rebuild_content(self):
        for widget in self.right_content.winfo_children():
            widget.destroy()
        
        self.status_label = ttk.LabelFrame(self.right_content, text=self.lang["current_status"])
        self.status_label.pack(pady=5, fill=tk.X)
        
        status_inner = ttk.Frame(self.status_label)
        status_inner.pack(pady=5, padx=10)
        
        self.version_label = ttk.Label(status_inner, text=self.lang["version"], font=("Arial", 10, "bold"))
        self.version_label.pack(side=tk.LEFT, padx=5)
        self.version_display = ttk.Label(status_inner, text=f"BE{self.current_version}", font=("Arial", 10), foreground="blue")
        self.version_display.pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(status_inner, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.level_label = ttk.Label(status_inner, text=self.lang["level"], font=("Arial", 10, "bold"))
        self.level_label.pack(side=tk.LEFT, padx=5)
        level_num = self.current_image_index + 2
        self.level_display = ttk.Label(status_inner, text=f"Level {level_num}", font=("Arial", 10), foreground="green")
        self.level_display.pack(side=tk.LEFT, padx=5)
        
        version_title_frame = ttk.Frame(self.right_content)
        version_title_frame.pack(pady=(0, 5))
        self.version_title_label = ttk.Label(version_title_frame, text=self.lang["version"], font=("Arial", 11, "bold"))
        self.version_title_label.pack()
        
        version_frame = ttk.Frame(self.right_content)
        version_frame.pack(pady=5)
        
        version_list = [1, 3, 4, 5, 6, 7]
        for v in version_list:
            btn = ttk.Button(
                version_frame, 
                text=f"BE{v}", 
                command=lambda val=v: self.select_version(val),
                width=5
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.all_buttons.append(btn)
        
        level_title_frame = ttk.Frame(self.right_content)
        level_title_frame.pack(pady=(0, 5))
        self.level_title_label = ttk.Label(level_title_frame, text=self.lang["level"], font=("Arial", 11, "bold"))
        self.level_title_label.pack()
        
        button_frame = ttk.Frame(self.right_content)
        button_frame.pack(pady=5)
        
        for i in range(5):
            level_num_btn = i + 2
            btn = ttk.Button(
                button_frame, 
                text=f"Level{level_num_btn}", 
                command=lambda idx=i: self.select_image(idx),
                width=6
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.all_buttons.append(btn)
        
        ttk.Separator(self.right_content, orient='horizontal').pack(fill=tk.X, pady=10)
        
        self.color_display_frame = ttk.Frame(self.right_content)
        self.color_display_frame.pack(pady=5, fill=tk.X)
        
        self.color_display_label = ttk.Label(self.color_display_frame, text=self.lang["current_blend"], font=("Arial", 9))
        self.current_color_preview = tk.Canvas(self.color_display_frame, width=25, height=18, 
                                               bg='white', relief='solid', borderwidth=1)
        self.current_color_label = ttk.Label(self.color_display_frame, text="#FFFFFF", font=("Arial", 8))
        
        self.target_prefix_label = ttk.Label(self.color_display_frame, text=self.lang["target_color"], font=("Arial", 9))
        self.target_color_preview = tk.Canvas(self.color_display_frame, width=25, height=18, 
                                              bg='white', relief='solid', borderwidth=1, cursor="hand2")
        self.target_color_preview.bind('<Button-1>', lambda e: self.pick_target_color())
        self.target_color_label = ttk.Label(self.color_display_frame, text="#FFFFFF", font=("Arial", 8))
        
        self.delta_prefix_label = ttk.Label(self.color_display_frame, text=self.lang["delta_e"], font=("Arial", 9, "bold"))
        self.delta_e_label = ttk.Label(self.color_display_frame, text="0.00", font=("Arial", 9, "bold"), foreground="green")
        
        self.placeholder_label = ttk.Label(self.color_display_frame, 
                                           text=self.lang["no_dye"], 
                                           font=("Arial", 10), foreground="gray")
        
        self.sequence_count_label = ttk.Label(self.color_display_frame, text="0/20", 
                                              font=("Arial", 10), foreground="gray")
        self.sequence_count_label.pack(side=tk.RIGHT, padx=5)
        
        self.color_display_label.pack_forget()
        self.current_color_preview.pack_forget()
        self.current_color_label.pack_forget()
        self.target_prefix_label.pack_forget()
        self.target_color_preview.pack_forget()
        self.target_color_label.pack_forget()
        self.delta_prefix_label.pack_forget()
        self.delta_e_label.pack_forget()
        self.placeholder_label.pack(side=tk.LEFT, padx=5)
        
        auto_frame = ttk.Frame(self.right_content)
        auto_frame.pack(pady=5, fill=tk.X)
        
        self.auto_gen_btn = ttk.Button(auto_frame, text=self.lang["calc_sequence"], 
                                       command=self.auto_generate_sequence, width=20)
        self.auto_gen_btn.pack(side=tk.LEFT, padx=5)
        self.all_buttons.append(self.auto_gen_btn)
        
        self.based_on_label = ttk.Label(auto_frame, text=self.lang["based_on"], font=("Arial", 8), foreground="gray")
        self.based_on_label.pack(side=tk.LEFT, padx=5)
        
        batch_btn = ttk.Button(auto_frame, text=self.lang["batch_render"], 
                               command=self.open_batch_render_dialog, width=15)
        batch_btn.pack(side=tk.RIGHT, padx=5)
        self.all_buttons.append(batch_btn)
        
        self.sequence_frame = ttk.LabelFrame(self.right_content, text=self.lang["sequence"])
        self.sequence_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        list_container = ttk.Frame(self.sequence_frame)
        list_container.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        self.list_canvas = tk.Canvas(list_container, height=80, bg='white', highlightthickness=1, highlightcolor='gray')
        self.list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.list_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.list_inner = tk.Frame(self.list_canvas, bg='white')
        self.list_canvas_window = self.list_canvas.create_window((0, 0), window=self.list_inner, anchor=tk.NW)
        
        self.list_items = []
        
        self.list_canvas.bind('<Configure>', self.on_canvas_configure)
        self.list_inner.bind('<Configure>', self.on_inner_configure)
        
        seq_control_frame = ttk.Frame(self.sequence_frame)
        seq_control_frame.pack(pady=5)
        
        self.clear_btn = ttk.Button(seq_control_frame, text=self.lang["clear"], command=self.clear_sequence, width=12)
        self.clear_btn.pack(side=tk.LEFT, padx=3)
        self.all_buttons.append(self.clear_btn)
        
        self.times_frame = ttk.LabelFrame(self.right_content, text=self.lang["dye_times"])
        self.times_frame.pack(pady=5, fill=tk.X)
        
        self.times_labels = {}
        times_inner = ttk.Frame(self.times_frame)
        times_inner.pack(pady=5, padx=5, fill=tk.X)
        
        for i, (hex_val, chinese_name, english_name) in enumerate(self.color_data):
            row = i // 8
            col = i % 8
            frame = ttk.Frame(times_inner)
            frame.grid(row=row, column=col, padx=2, pady=1, sticky='w')
            
            r, g, b = self.hex_to_rgb(hex_val)
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            square = tk.Canvas(frame, width=10, height=10, bg=color_hex, highlightthickness=0)
            square.pack(side=tk.LEFT)
            
            label = tk.Label(frame, text=f"{chinese_name}:0", font=("Arial", 8), bg='#f0f0f0')
            label.pack(side=tk.LEFT, padx=2)
            self.times_labels[english_name] = label
        
        for i in range(8):
            times_inner.grid_columnconfigure(i, weight=1)
        
        self.quick_frame = ttk.LabelFrame(self.right_content, text=self.lang["dye_options"])
        self.quick_frame.pack(pady=5, fill=tk.X)
        
        self.dye_buttons = []
        self.dye_icon_labels = []
        for i, (hex_val, chinese_name, english_name) in enumerate(self.color_data):
            row = i // 4
            col = i % 4
            
            btn_frame = tk.Frame(self.quick_frame, bg='#f0f0f0', relief='raised', bd=1)
            btn_frame.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            
            img = self.dye_images.get(hex_val)
            if img:
                icon_label = tk.Label(btn_frame, image=img, bg='#f0f0f0', width=16, height=16)
            else:
                icon_label = tk.Label(btn_frame, text='■', font=('Arial', 10), bg='#f0f0f0', width=2, height=1)
            icon_label.pack(pady=(2, 0))
            self.dye_icon_labels.append(icon_label)
            
            display_name = self.get_display_color_name(english_name)
            text_label = tk.Label(btn_frame, text=display_name, font=('Arial', 8), bg='#f0f0f0')
            text_label.pack(pady=(0, 2))
            
            def make_on_click(h):
                return lambda e: self.add_color_to_sequence(h)
            
            btn_frame.bind('<Button-1>', make_on_click(hex_val))
            icon_label.bind('<Button-1>', make_on_click(hex_val))
            text_label.bind('<Button-1>', make_on_click(hex_val))
            
            def on_enter(frame):
                return lambda e: frame.config(bg='#e0e8f0')
            def on_leave(frame):
                return lambda e: frame.config(bg='#f0f0f0')
            
            btn_frame.bind('<Enter>', on_enter(btn_frame))
            btn_frame.bind('<Leave>', on_leave(btn_frame))
            
            self.dye_buttons.append(btn_frame)
            self.all_buttons.append(btn_frame)
        
        for i in range(4):
            self.quick_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.quick_frame.grid_rowconfigure(i, weight=1)
        
        self.export_btn = ttk.Button(self.right_content, text=self.lang["export"], command=self.save_result, width=20)
        self.export_btn.pack(pady=5)
        self.all_buttons.append(self.export_btn)
        
        self.update_sequence_display()
        self.update_times_display()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.result_canvas = tk.Canvas(left_frame, bg='#f0f0f0', width=350, height=350)
        self.result_canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(main_frame, width=900)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.lang_notebook = ttk.Notebook(right_frame)
        self.lang_notebook.pack(fill=tk.BOTH, expand=True)
        
        lang_tabs = {
            "简体中文": "zh_CN",
            "繁體中文": "zh_TW",
            "日本語": "ja_JP",
            "English": "en_US"
        }
        
        self.lang_tab_frames = {}
        for display_name, code in lang_tabs.items():
            tab_frame = ttk.Frame(self.lang_notebook)
            self.lang_notebook.add(tab_frame, text=display_name)
            self.lang_tab_frames[code] = tab_frame
        
        def on_tab_changed(event):
            selected = self.lang_notebook.index(self.lang_notebook.select())
            lang_codes = list(lang_tabs.values())
            if selected < len(lang_codes):
                self.change_language(lang_codes[selected])
        
        self.lang_notebook.bind('<<NotebookTabChanged>>', on_tab_changed)
        
        current_tab_index = list(lang_tabs.values()).index(self.current_lang)
        self.lang_notebook.select(current_tab_index)
        
        self.right_content = self.lang_tab_frames[self.current_lang]
        self.rebuild_content()
        
        status_bar_frame = ttk.Frame(self.root)
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 10))
        
        ttk.Separator(status_bar_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value=self.lang["idle"])
        self.status_label2 = ttk.Label(status_bar_frame, textvariable=self.status_var, 
                                 font=("Arial", 9), foreground="gray")
        self.status_label2.pack(side=tk.LEFT, padx=5)
    
    def update_all_texts(self):
        current_status = self.status_var.get()
        if current_status in [LANGUAGES[code]["idle"] for code in LANGUAGES]:
            self.status_var.set(self.lang["idle"])
        elif "图片已保存在" in current_status or "Image saved at" in current_status:
            pass
        
        self.status_label.config(text=self.lang["current_status"])
        self.version_label.config(text=self.lang["version"])
        self.level_label.config(text=self.lang["level"])
        self.version_title_label.config(text=self.lang["version"])
        self.level_title_label.config(text=self.lang["level"])
        self.color_display_label.config(text=self.lang["current_blend"])
        self.target_prefix_label.config(text=self.lang["target_color"])
        self.delta_prefix_label.config(text=self.lang["delta_e"])
        self.placeholder_label.config(text=self.lang["no_dye"])
        self.sequence_frame.config(text=self.lang["sequence"])
        self.clear_btn.config(text=self.lang["clear"])
        self.times_frame.config(text=self.lang["dye_times"])
        self.quick_frame.config(text=self.lang["dye_options"])
        self.export_btn.config(text=self.lang["export"])
        self.auto_gen_btn.config(text=self.lang["calc_sequence"])
        self.based_on_label.config(text=self.lang["based_on"])
        
        self.update_dye_button_texts()
        self.update_times_display()
    
    def update_dye_button_texts(self):
        for i, btn_frame in enumerate(self.dye_buttons):
            if i < len(self.color_data):
                hex_val, chinese_name, english_name = self.color_data[i]
                display_name = self.get_display_color_name(english_name)
                children = btn_frame.winfo_children()
                if len(children) >= 2:
                    text_label = children[1]
                    if isinstance(text_label, tk.Label):
                        text_label.config(text=display_name)
    
    def update_times_display(self):
        for english_name, label in self.times_labels.items():
            count = self.color_times.get(english_name, 0)
            display_name = self.get_display_color_name(english_name)
            label.config(text=f"{display_name}:{count}")
        self.root.update_idletasks()
    
    def on_canvas_configure(self, event):
        self.list_canvas.itemconfig(self.list_canvas_window, width=event.width)
    
    def on_inner_configure(self, event):
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))
    
    def update_sequence_display(self):
        for item in self.list_items:
            item.destroy()
        self.list_items.clear()
        
        for i, color in enumerate(self.color_sequence):
            item_frame = tk.Frame(self.list_inner, bg='white', height=24)
            item_frame.pack(fill=tk.X, pady=1)
            
            def make_on_click(idx):
                return lambda e: self.select_list_item(idx)
            
            r, g, b = self.hex_to_rgb(color)
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            square = tk.Canvas(item_frame, width=14, height=14, bg=color_hex, highlightthickness=1, highlightcolor='gray')
            square.pack(side=tk.LEFT, padx=(5, 6))
            square.bind('<Button-1>', make_on_click(i))
            
            color_name = self.get_color_name_by_hex(color)
            label = tk.Label(item_frame, text=f"{i+1}. {color_name}", bg='white', font=("Arial", 9))
            label.pack(side=tk.LEFT)
            label.bind('<Button-1>', make_on_click(i))
            
            del_btn = tk.Label(item_frame, text="×", fg='red', bg='white', font=("Arial", 11, "bold"), cursor="hand2")
            del_btn.pack(side=tk.RIGHT, padx=8)
            del_btn.bind('<Button-1>', lambda e, idx=i: self.remove_item(idx))
            
            item_frame.bind('<Button-1>', make_on_click(i))
            
            self.list_items.append(item_frame)
        
        self.sequence_count_label.config(text=f"{len(self.color_sequence)}/{self.max_sequence_size}")
        self.update_color_display()
        
        self.list_canvas.update_idletasks()
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))
    
    def select_list_item(self, index):
        for i, item in enumerate(self.list_items):
            item.config(bg='white')
            for child in item.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg='white')
        
        if 0 <= index < len(self.list_items):
            self.list_items[index].config(bg='#e0e8f0')
            for child in self.list_items[index].winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg='#e0e8f0')
    
    def remove_item(self, index):
        if 0 <= index < len(self.color_sequence):
            removed_color = self.color_sequence[index]
            removed_english_name = self.get_english_name(removed_color)
            
            previous_color = self.calculate_blend_color()
            del self.color_sequence[index]
            new_color = self.calculate_blend_color()
            if previous_color != new_color:
                if removed_english_name and removed_english_name in self.color_times:
                    if self.color_times[removed_english_name] > 0:
                        self.color_times[removed_english_name] -= 1
                        self.update_times_display()
            
            self.update_sequence_display()
            self.update_display()
            
            if self.current_version == 1:
                self.reload_images()
    
    def migrate_sequence_to_new_version(self, old_version, new_version, seq_to_migrate):
        if not seq_to_migrate:
            return
        
        self.is_migrating = True
        self.set_buttons_enabled(False)
        self.set_status(self.lang["migrating"])
        
        def do_migration():
            self.color_sequence.clear()
            for key in self.color_times:
                self.color_times[key] = 0
            
            self.root.after(0, self.update_sequence_display)
            self.root.after(0, self.update_times_display)
            self.root.after(0, self.update_display)
            
            for color in seq_to_migrate:
                previous_color = self.calculate_blend_color()
                r, g, b = self.hex_to_rgb(color)
                new_color = ((previous_color[0] + r) // 2, (previous_color[1] + g) // 2, (previous_color[2] + b) // 2)
                if new_color != previous_color:
                    english_name = self.get_english_name(color)
                    self.color_sequence.append(color)
                    if english_name and english_name in self.color_times:
                        self.color_times[english_name] += 1
                
                self.root.after(0, self.update_sequence_display)
                self.root.after(0, self.update_times_display)
                self.root.after(0, self.update_display)
                
                time.sleep(0.01)
            
            if new_version == 1 and self.color_sequence:
                self.root.after(0, self.reload_images)
            
            self.root.after(0, lambda: self.set_buttons_enabled(True))
            self.root.after(0, lambda: self.set_status(self.lang["migration_done"], auto_reset=True))
            self.is_migrating = False
        
        thread = threading.Thread(target=do_migration)
        thread.daemon = True
        thread.start()
    
    def select_version(self, version):
        if self.is_generating or self.is_migrating:
            return
        
        if version == self.current_version:
            return
        
        old_seq = self.color_sequence.copy()
        old_version = self.current_version
        
        self.current_version = version
        self.version_display.config(text=f"BE{version}")
        
        self.load_background()
        self.load_dye_images()
        self.update_dye_buttons()
        
        self.current_image_index = 4
        level_num = self.current_image_index + 2
        self.level_display.config(text=f"Level {level_num}")
        
        self.color_sequence.clear()
        for key in self.color_times:
            self.color_times[key] = 0
        self.update_times_display()
        self.update_sequence_display()
        self.update_display()
        
        self.load_images()
        self.update_display()
        
        if old_seq:
            self.migrate_sequence_to_new_version(old_version, version, old_seq)
    
    def update_dye_buttons(self):
        for i, (hex_val, chinese_name, english_name) in enumerate(self.color_data):
            img = self.dye_images.get(hex_val)
            if i < len(self.dye_icon_labels):
                icon_label = self.dye_icon_labels[i]
                if img:
                    icon_label.config(image=img)
                    icon_label.config(text='')
                else:
                    icon_label.config(text='■', font=('Arial', 10))
    
    def select_image(self, index):
        self.current_image_index = index
        level_num = index + 2
        self.level_display.config(text=f"Level {level_num}")
        self.update_display()
    
    def update_color_display(self):
        for widget in self.color_display_frame.winfo_children():
            if widget not in [self.sequence_count_label]:
                widget.pack_forget()
        
        if not self.color_sequence:
            self.placeholder_label.pack(side=tk.LEFT, padx=5)
            return
        
        self.color_display_label.pack(side=tk.LEFT, padx=3)
        self.current_color_preview.pack(side=tk.LEFT, padx=3)
        self.current_color_label.pack(side=tk.LEFT, padx=3)
        
        self.target_prefix_label.pack(side=tk.LEFT, padx=(5, 3))
        self.target_color_preview.pack(side=tk.LEFT, padx=3)
        self.target_color_label.pack(side=tk.LEFT, padx=3)
        
        self.delta_prefix_label.pack(side=tk.LEFT, padx=(5, 3))
        self.delta_e_label.pack(side=tk.LEFT, padx=3)
        
        if self.use_target:
            target_rgb = self.target_color
            self.target_color_preview.config(bg=self.target_hex)
            self.target_color_label.config(text=self.target_hex)
        else:
            current_rgb = self.current_blend_color
            target_rgb = current_rgb
            self.target_color = current_rgb
            self.target_hex = self.rgb_to_hex(current_rgb[0], current_rgb[1], current_rgb[2])
            self.target_color_preview.config(bg=self.target_hex)
            self.target_color_label.config(text=self.target_hex)
        
        current_rgb = self.current_blend_color
        current_hex = self.rgb_to_hex(current_rgb[0], current_rgb[1], current_rgb[2])
        self.current_color_preview.config(bg=current_hex)
        self.current_color_label.config(text=current_hex)
        
        delta_e = self.calculate_delta_e(current_rgb, target_rgb)
        self.delta_e_label.config(text=f"{delta_e:.2f}")
        if delta_e < 1.0:
            self.delta_e_label.config(foreground="green")
        elif delta_e < 3.0:
            self.delta_e_label.config(foreground="orange")
        else:
            self.delta_e_label.config(foreground="red")
    
    def add_color_to_sequence(self, hex_val):
        if len(self.color_sequence) >= self.max_sequence_size:
            messagebox.showwarning(self.lang["tip"], self.lang["max_warning"].format(self.max_sequence_size))
            return False
        
        english_name = self.get_english_name(hex_val)
        changed = False
        
        previous_color = self.calculate_blend_color()
        r, g, b = self.hex_to_rgb(hex_val)
        new_color = ((previous_color[0] + r) // 2, (previous_color[1] + g) // 2, (previous_color[2] + b) // 2)
        
        if new_color != previous_color:
            self.color_sequence.append(hex_val)
            if english_name and english_name in self.color_times:
                self.color_times[english_name] += 1
                self.update_times_display()
            changed = True
            
            self.update_sequence_display()
            self.update_display()
            
            if self.current_version == 1:
                self.reload_images()
        else:
            display_name = self.get_display_color_name(english_name) if english_name else hex_val
            self.set_status(self.lang["invalid"], auto_reset=True)
        
        return changed
    
    def clear_sequence(self):
        self.color_sequence.clear()
        for key in self.color_times:
            self.color_times[key] = 0
        self.use_target = False
        self.target_color = (255, 255, 255)
        self.target_hex = "#FFFFFF"
        self.update_times_display()
        self.update_sequence_display()
        self.update_display()
        self.set_status(self.lang["idle"])
        
        if self.current_version == 1:
            self.reload_images()
    
    def hex_to_rgb(self, hex_str):
        hex_str = hex_str.strip()
        if not hex_str.startswith('#'):
            hex_str = '#' + hex_str
        try:
            if len(hex_str) == 7:
                r = int(hex_str[1:3], 16)
                g = int(hex_str[3:5], 16)
                b = int(hex_str[5:7], 16)
                return r, g, b
            elif len(hex_str) == 4:
                r = int(hex_str[1]*2, 16)
                g = int(hex_str[2]*2, 16)
                b = int(hex_str[3]*2, 16)
                return r, g, b
            else:
                return 255, 255, 255
        except:
            return 255, 255, 255
    
    def rgb_to_hex(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'.upper()
    
    def blend_images_float(self, original_img, blend_color):
        try:
            if original_img.size != self.image_size:
                original_img = self.resize_image(original_img, self.image_size[0], self.image_size[1])
            
            r_channel, g_channel, b_channel, a_channel = original_img.split()
            
            r_array = np.array(r_channel, dtype=np.float32)
            g_array = np.array(g_channel, dtype=np.float32)
            b_array = np.array(b_channel, dtype=np.float32)
            a_array_original = np.array(a_channel, dtype=np.float32)
            a_array = a_array_original
            
            r_normalized = r_array / 255.0
            g_normalized = g_array / 255.0
            b_normalized = b_array / 255.0
            
            blend_r, blend_g, blend_b = blend_color
            blend_normalized = np.array([blend_r/255.0, blend_g/255.0, blend_b/255.0])
            
            result_r = r_normalized * blend_normalized[0] * 255.0
            result_g = g_normalized * blend_normalized[1] * 255.0
            result_b = b_normalized * blend_normalized[2] * 255.0
            result_a = a_array
            
            return result_r, result_g, result_b, result_a, a_array_original
        except Exception:
            return None, None, None, None, None
    
    def composite_with_background(self, foreground_rgb, foreground_alpha, original_alpha_mask):
        try:
            bg = self.background_image.copy()
            if bg.size != self.image_size:
                bg = self.resize_image(bg, self.image_size[0], self.image_size[1])
            if bg.mode != 'RGBA':
                bg = bg.convert('RGBA')
            
            fg_r, fg_g, fg_b = foreground_rgb
            fg_a = foreground_alpha
            
            if len(fg_r.shape) != 2:
                fg_r = fg_r.reshape(self.image_size[1], self.image_size[0])
                fg_g = fg_g.reshape(self.image_size[1], self.image_size[0])
                fg_b = fg_b.reshape(self.image_size[1], self.image_size[0])
                fg_a = fg_a.reshape(self.image_size[1], self.image_size[0])
            
            original_mask = original_alpha_mask / 255.0
            
            if self.current_version != 1 and self.color_sequence:
                alpha_byte = 157
                new_alpha = fg_a.copy()
                water_positions = original_mask > 0
                new_alpha[water_positions] = alpha_byte
                new_alpha[~water_positions] = 0
                fg_a = new_alpha
            
            fg_r_clipped = np.clip(fg_r, 0, 255).astype(np.uint8)
            fg_g_clipped = np.clip(fg_g, 0, 255).astype(np.uint8)
            fg_b_clipped = np.clip(fg_b, 0, 255).astype(np.uint8)
            fg_a_clipped = fg_a.astype(np.uint8)
            
            fg_img = Image.merge('RGBA', (
                Image.fromarray(fg_r_clipped),
                Image.fromarray(fg_g_clipped),
                Image.fromarray(fg_b_clipped),
                Image.fromarray(fg_a_clipped)
            ))
            
            if fg_img.size != self.image_size:
                fg_img = self.resize_image(fg_img, self.image_size[0], self.image_size[1])
            
            result = Image.alpha_composite(bg, fg_img)
            return result
        except Exception as e:
            print("")
            return self.background_image.copy()
    
    def update_display(self):
        try:
            if not self.images or self.current_image_index >= len(self.images):
                return
            
            original_img = self.images[self.current_image_index]
            
            if original_img.size != self.image_size:
                original_img = self.resize_image(original_img, self.image_size[0], self.image_size[1])
                self.images[self.current_image_index] = original_img
            
            blend_color = self.calculate_blend_color()
            self.current_blend_color = blend_color
            
            self.update_color_display()
            
            if self.current_version == 1 and not self.color_sequence:
                bg = self.background_image.copy()
                if bg.size != self.image_size:
                    bg = self.resize_image(bg, self.image_size[0], self.image_size[1])
                preview_img = Image.alpha_composite(bg, original_img)
            else:
                fg_r, fg_g, fg_b, fg_a, original_a = self.blend_images_float(original_img, blend_color)
                if fg_r is None:
                    return
                preview_img = self.composite_with_background((fg_r, fg_g, fg_b), fg_a, original_a)
            
            canvas_width = self.result_canvas.winfo_width()
            canvas_height = self.result_canvas.winfo_height()
            
            if canvas_width <= 1:
                canvas_width = 350
                canvas_height = 350
            
            img_width, img_height = preview_img.size
            ratio = min(canvas_width/img_width, canvas_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            preview_resized = preview_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            result_tk = ImageTk.PhotoImage(preview_resized)
            self.result_canvas.delete("all")
            self.result_canvas.create_image(canvas_width//2, canvas_height//2, 
                                            image=result_tk, anchor=tk.CENTER)
            self.result_canvas.image = result_tk
            
        except Exception:
            pass
    
    def save_result(self):
        try:
            if not self.images or self.current_image_index >= len(self.images):
                self.set_status(self.lang["error_no_image"], auto_reset=True)
                return
            
            original_img = self.images[self.current_image_index]
            
            if original_img.size != self.image_size:
                original_img = self.resize_image(original_img, self.image_size[0], self.image_size[1])
            
            blend_color = self.current_blend_color
            
            if self.current_version == 1 and not self.color_sequence:
                bg = self.background_image.copy()
                if bg.size != self.image_size:
                    bg = self.resize_image(bg, self.image_size[0], self.image_size[1])
                final_img = Image.alpha_composite(bg, original_img)
            else:
                fg_r, fg_g, fg_b, fg_a, original_a = self.blend_images_float(original_img, blend_color)
                if fg_r is None:
                    self.set_status(self.lang["error_process"], auto_reset=True)
                    return
                final_img = self.composite_with_background((fg_r, fg_g, fg_b), fg_a, original_a)
            
            filename = self.generate_filename() + ".png"
            file_path = os.path.join(self.output_dir, filename)
            
            final_img.save(file_path, 'PNG')
            self.set_status(self.lang["export_success"].format(file_path), auto_reset=True)
            
        except Exception as e:
            self.set_status(self.lang["error"].format(str(e)), auto_reset=True)

def main():
    root = tk.Tk()
    app = ImageBlendApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
