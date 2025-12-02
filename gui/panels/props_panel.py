# gui/panels/props_panel.py
"""右侧属性面板 - 使用标签页分类"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QScrollArea, QGroupBox, QLineEdit, QSpinBox,
    QCheckBox, QLabel, QPushButton, QComboBox, QPlainTextEdit,
    QSizePolicy, QTabWidget,
)

from ..widgets import ColorButton
from ..constants import COMMON_RESOLUTIONS


class PropsPanel(QWidget):
    """属性面板 - 使用标签页分类组织"""

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建标签页控件
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 创建各个标签页
        self._create_basic_tab()      # 基础设置
        self._create_style_tab()      # 样式设置
        self._create_layout_tab()     # 布局设置
        self._create_advanced_tab()   # 高级设置

    # =========================================================================
    # 标签页 1: 基础设置
    # =========================================================================
    def _create_basic_tab(self):
        """基础设置标签页"""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # --- 基本信息 ---
        group_meta = QGroupBox("基本信息")
        form_meta = QFormLayout()
        form_meta.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_meta.setHorizontalSpacing(8)
        form_meta.setVerticalSpacing(6)

        self.edit_name = QLineEdit()
        form_meta.addRow("显示名称:", self.edit_name)
        group_meta.setLayout(form_meta)
        layout.addWidget(group_meta)

        # --- 画布设置 ---
        group_canvas = QGroupBox("画布设置")
        form_canvas = QFormLayout()
        form_canvas.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_canvas.setHorizontalSpacing(8)
        form_canvas.setVerticalSpacing(6)

        self.combo_resolution = QComboBox()
        self._populate_resolution_combo()
        form_canvas.addRow("分辨率:", self.combo_resolution)
        group_canvas.setLayout(form_canvas)
        layout.addWidget(group_canvas)

        # --- 对话框 ---
        group_box = QGroupBox("对话框")
        vbox_box = QVBoxLayout()
        vbox_box.setContentsMargins(8, 8, 8, 8)
        vbox_box.setSpacing(6)

        self.btn_select_dialog_box = QPushButton("更换底图 (自动贴底)...")
        vbox_box.addWidget(self.btn_select_dialog_box)

        hint = QLabel("💡 对话框会自动拉伸到画布宽度并贴底")
        hint.setStyleSheet("color: #888; font-size: 10px;")
        hint.setWordWrap(True)
        vbox_box.addWidget(hint)

        group_box.setLayout(vbox_box)
        layout.addWidget(group_box)

        layout.addStretch()
        self.tab_widget.addTab(scroll, "📋 基础")

    # =========================================================================
    # 标签页 2: 样式设置
    # =========================================================================
    def _create_style_tab(self):
        """样式设置标签页"""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # --- 文字样式 ---
        group_text = QGroupBox("文字样式")
        form_text = QFormLayout()
        form_text.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_text.setHorizontalSpacing(8)
        form_text.setVerticalSpacing(6)

        # 正文样式
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(10, 200)
        self.btn_text_color = ColorButton([255, 255, 255])

        row_text = QHBoxLayout()
        row_text.setContentsMargins(0, 0, 0, 0)
        row_text.setSpacing(4)
        row_text.addWidget(self.spin_font_size)
        row_text.addWidget(self.btn_text_color)
        form_text.addRow("正文 (大小/色):", row_text)

        # 名字样式
        self.spin_name_size = QSpinBox()
        self.spin_name_size.setRange(10, 200)
        self.btn_name_color = ColorButton([255, 0, 255])

        row_name = QHBoxLayout()
        row_name.setContentsMargins(0, 0, 0, 0)
        row_name.setSpacing(4)
        row_name.addWidget(self.spin_name_size)
        row_name.addWidget(self.btn_name_color)
        form_text.addRow("名字 (大小/色):", row_name)

        group_text.setLayout(form_text)
        layout.addWidget(group_text)

        # --- 自定义字体 ---
        group_font = QGroupBox("自定义字体")
        vbox_font = QVBoxLayout()
        vbox_font.setContentsMargins(8, 8, 8, 8)
        vbox_font.setSpacing(6)

        self.lbl_font_file = QLabel("默认字体")
        self.lbl_font_file.setStyleSheet("color: gray; font-size: 10px;")
        vbox_font.addWidget(self.lbl_font_file)

        row_font = QHBoxLayout()
        row_font.setSpacing(4)
        self.btn_select_font = QPushButton("选择字体...")
        self.btn_clear_font = QPushButton("清除")
        self.btn_clear_font.setMaximumWidth(60)
        row_font.addWidget(self.btn_select_font)
        row_font.addWidget(self.btn_clear_font)
        vbox_font.addLayout(row_font)

        group_font.setLayout(vbox_font)
        layout.addWidget(group_font)

        # --- 台词前后缀 ---
        group_wrapper = QGroupBox("台词前后缀")
        form_wrapper = QFormLayout()
        form_wrapper.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_wrapper.setHorizontalSpacing(8)
        form_wrapper.setVerticalSpacing(6)

        self.combo_wrapper_mode = QComboBox()
        self.combo_wrapper_mode.addItem("无", {"type": "none"})
        self.combo_wrapper_mode.addItem("「」", {"type": "preset", "preset": "corner_single"})
        self.combo_wrapper_mode.addItem("『』", {"type": "preset", "preset": "corner_double"})
        self.combo_wrapper_mode.addItem("自定义", {"type": "custom"})
        form_wrapper.addRow("模式:", self.combo_wrapper_mode)

        self.edit_wrapper_prefix = QLineEdit()
        self.edit_wrapper_prefix.setPlaceholderText("前缀")
        form_wrapper.addRow("前缀:", self.edit_wrapper_prefix)

        self.edit_wrapper_suffix = QLineEdit()
        self.edit_wrapper_suffix.setPlaceholderText("后缀")
        form_wrapper.addRow("后缀:", self.edit_wrapper_suffix)

        group_wrapper.setLayout(form_wrapper)
        layout.addWidget(group_wrapper)
        self.set_wrapper_custom_enabled(False)

        layout.addStretch()
        self.tab_widget.addTab(scroll, "🎨 样式")

    # =========================================================================
    # 标签页 3: 布局设置
    # =========================================================================
    def _create_layout_tab(self):
        """布局设置标签页"""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # --- 布局微调 ---
        group_layout = QGroupBox("布局微调")
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_layout.setHorizontalSpacing(8)
        form_layout.setVerticalSpacing(6)

        self.check_on_top = QCheckBox("立绘覆盖对话框")
        form_layout.addRow(self.check_on_top)

        self.lbl_pos_info = QLabel("💡 拖动画面元素以更新坐标")
        self.lbl_pos_info.setStyleSheet("color: #888; font-size: 10px;")
        self.lbl_pos_info.setWordWrap(True)
        form_layout.addRow(self.lbl_pos_info)

        group_layout.setLayout(form_layout)
        layout.addWidget(group_layout)

        # --- 裁剪区域 ---
        group_crop = QGroupBox("裁剪区域")
        vbox_crop = QVBoxLayout()
        vbox_crop.setContentsMargins(8, 8, 8, 8)
        vbox_crop.setSpacing(6)

        self.check_enable_crop = QCheckBox("启用裁剪")
        vbox_crop.addWidget(self.check_enable_crop)

        self.btn_show_crop_area = QPushButton("显示/隐藏裁剪框")
        vbox_crop.addWidget(self.btn_show_crop_area)

        self.lbl_crop_info = QLabel("💡 拖动红色框调整裁剪区域\n可以裁剪出任意尺寸的图片")
        self.lbl_crop_info.setStyleSheet("color: #888; font-size: 10px;")
        self.lbl_crop_info.setWordWrap(True)
        vbox_crop.addWidget(self.lbl_crop_info)

        group_crop.setLayout(vbox_crop)
        layout.addWidget(group_crop)

        layout.addStretch()
        self.tab_widget.addTab(scroll, "📐 布局")

    # =========================================================================
    # 标签页 4: 高级设置
    # =========================================================================
    def _create_advanced_tab(self):
        """高级设置标签页"""
        tab = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # --- 多层名称效果 ---
        group_advanced = QGroupBox("多层名称效果")
        vbox_advanced = QVBoxLayout()
        vbox_advanced.setContentsMargins(8, 8, 8, 8)
        vbox_advanced.setSpacing(8)

        self.check_name_advanced = QCheckBox("启用多层名称效果")
        vbox_advanced.addWidget(self.check_name_advanced)

        # 高级名称配置容器
        self.name_advanced_container = QWidget()
        advanced_layout = QVBoxLayout(self.name_advanced_container)
        advanced_layout.setContentsMargins(0, 0, 0, 0)
        advanced_layout.setSpacing(8)

        # 说明文字
        desc_label = QLabel(
            "💡 多层名称效果可以实现复杂的文字叠加，例如：\n"
            "   • 不同大小的文字组合\n"
            "   • 渐变色文字效果\n"
            "   • 艺术字排版"
        )
        desc_label.setStyleSheet("color: #666; font-size: 10px; padding: 8px; background: #f9f9f9; border-radius: 4px;")
        desc_label.setWordWrap(True)
        advanced_layout.addWidget(desc_label)

        # YAML 编辑区域
        self.edit_name_yaml = QPlainTextEdit()
        self.edit_name_yaml.setPlaceholderText(
            "# 示例：为角色名 '典狱长' 创建艺术字效果\n"
            "典狱长:\n"
            "  - text: \"典\"\n"
            "    position: [0, 0]\n"
            "    font_color: [195, 209, 231]\n"
            "    font_size: 196\n"
            "  - text: \"狱\"\n"
            "    position: [200, 100]\n"
            "    font_color: [255, 255, 255]\n"
            "    font_size: 92\n"
            "  - text: \"长\"\n"
            "    position: [300, 50]\n"
            "    font_color: [255, 255, 255]\n"
            "    font_size: 147\n"
            "default:\n"
            "  - text: \"{name}\"\n"
            "    position: [0, 0]\n"
            "    font_color: [255, 85, 255]\n"
            "    font_size: 32"
        )
        self.edit_name_yaml.setMinimumHeight(200)
        self.edit_name_yaml.setMaximumHeight(300)
        advanced_layout.addWidget(self.edit_name_yaml)

        # 按钮行
        yaml_buttons = QHBoxLayout()
        yaml_buttons.setSpacing(4)
        self.btn_apply_name_yaml = QPushButton("✓ 应用配置")
        self.btn_reset_name_yaml = QPushButton("↺ 恢复默认")
        yaml_buttons.addWidget(self.btn_apply_name_yaml)
        yaml_buttons.addWidget(self.btn_reset_name_yaml)
        advanced_layout.addLayout(yaml_buttons)

        # 提示信息
        hint_label = QLabel("📌 提示：在画布上拖动名字框可调整整体基准点位置")
        hint_label.setStyleSheet("color: #888; font-size: 10px; padding: 4px;")
        hint_label.setWordWrap(True)
        advanced_layout.addWidget(hint_label)

        vbox_advanced.addWidget(self.name_advanced_container)
        self.set_advanced_yaml_visible(False)

        group_advanced.setLayout(vbox_advanced)
        layout.addWidget(group_advanced)

        layout.addStretch()
        self.tab_widget.addTab(scroll, "⚙️ 高级")

    # =========================================================================
    # 辅助方法
    # =========================================================================
    def _populate_resolution_combo(self):
        self.combo_resolution.clear()
        for w, h in COMMON_RESOLUTIONS:
            label = f"{w} x {h}"
            self.combo_resolution.addItem(label, (w, h))

    def set_wrapper_custom_enabled(self, enabled: bool) -> None:
        self.edit_wrapper_prefix.setEnabled(enabled)
        self.edit_wrapper_suffix.setEnabled(enabled)

    def set_advanced_yaml_visible(self, visible: bool) -> None:
        """设置多层名称效果配置区域的可见性"""
        self.name_advanced_container.setVisible(visible)
