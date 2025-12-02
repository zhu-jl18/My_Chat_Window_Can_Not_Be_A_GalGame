"""
测试裁剪功能的脚本
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.renderer import CharacterRenderer

def test_crop_feature():
    """测试裁剪功能"""
    print("=" * 60)
    print("测试裁剪功能")
    print("=" * 60)

    # 测试角色 ID（请根据实际情况修改）
    char_id = "yuraa"
    base_path = "assets"

    try:
        # 创建渲染器
        print(f"\n1. 加载角色: {char_id}")
        renderer = CharacterRenderer(char_id, base_path)

        # 测试不启用裁剪
        print("\n2. 测试不启用裁剪（默认行为）")
        renderer.layout["enable_crop"] = False
        img_full = renderer.render("这是一个测试文本，用于验证裁剪功能是否正常工作。")
        print(f"   完整图片尺寸: {img_full.size}")
        img_full.save("test_output_full.png")
        print("   ✅ 已保存: test_output_full.png")

        # 测试启用裁剪
        print("\n3. 测试启用裁剪")
        renderer.layout["enable_crop"] = True

        # 设置裁剪区域（例如：从画布中央裁剪 300x1200 的区域）
        canvas_w, canvas_h = renderer.canvas_size
        x1 = (canvas_w - 300) // 2
        y1 = 0
        x2 = x1 + 300
        y2 = canvas_h
        renderer.layout["crop_area"] = [x1, y1, x2, y2]

        print(f"   裁剪区域: ({x1}, {y1}) → ({x2}, {y2})")
        print(f"   预期输出尺寸: {x2 - x1} x {y2 - y1}")

        img_cropped = renderer.render("这是一个测试文本，用于验证裁剪功能是否正常工作。")
        print(f"   实际输出尺寸: {img_cropped.size}")
        img_cropped.save("test_output_cropped.png")
        print("   ✅ 已保存: test_output_cropped.png")

        # 验证裁剪是否生效
        expected_size = (x2 - x1, y2 - y1)
        if img_cropped.size == expected_size:
            print("\n✅ 裁剪功能测试通过！")
        else:
            print(f"\n❌ 裁剪功能测试失败！预期尺寸 {expected_size}，实际尺寸 {img_cropped.size}")

        # 测试不同的裁剪区域
        print("\n4. 测试不同的裁剪区域（左侧 1/3）")
        x1 = 0
        y1 = 0
        x2 = canvas_w // 3
        y2 = canvas_h
        renderer.layout["crop_area"] = [x1, y1, x2, y2]

        print(f"   裁剪区域: ({x1}, {y1}) → ({x2}, {y2})")
        img_left = renderer.render("左侧裁剪测试")
        print(f"   输出尺寸: {img_left.size}")
        img_left.save("test_output_left.png")
        print("   ✅ 已保存: test_output_left.png")

        print("\n" + "=" * 60)
        print("测试完成！请查看生成的图片文件：")
        print("  - test_output_full.png (完整图片)")
        print("  - test_output_cropped.png (中央裁剪)")
        print("  - test_output_left.png (左侧裁剪)")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = test_crop_feature()
    sys.exit(0 if success else 1)
