#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile
from datetime import datetime


class SDKPacker:
    def __init__(self, sdk_path=".", output_dir="./output"):
        """初始化打包器

        Args:
            sdk_path: SDK源码路径
            output_dir: 输出目录
        """
        self.sdk_path = os.path.abspath(sdk_path)
        self.output_dir = os.path.abspath(output_dir)
        self.temp_dir = os.path.join(self.output_dir, "temp")

        # 需要包含的文件和目录
        self.include_paths = [
            "lib/",
            "assets/",
            "pubspec.yaml",
            "LICENSE",
            "README.md",
            "CHANGELOG.md",
            "analysis_options.yaml",
        ]

        # 要排除的文件和目录
        self.exclude_patterns = [
            ".git/",
            ".dart_tool/",
            ".idea/",
            ".vscode/",
            "build/",
            "*.log",
            "*.lock",
            ".packages",
            ".flutter-plugins",
            ".flutter-plugins-dependencies",
            ".metadata",
            ".DS_Store",
            "Thumbs.db",
        ]

    def _should_exclude(self, path):
        """检查是否应该排除某个文件或目录

        Args:
            path: 文件或目录路径

        Returns:
            bool: 是否应该排除
        """
        from fnmatch import fnmatch

        # 转换为相对路径
        rel_path = os.path.relpath(path, self.sdk_path)

        # 检查是否匹配任何排除模式
        for pattern in self.exclude_patterns:
            if fnmatch(rel_path, pattern) or fnmatch(os.path.basename(path), pattern):
                return True
        return False

    def _copy_files(self):
        """复制必要的文件到临时目录"""
        print("正在复制文件...")

        # 创建临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

        # 复制文件和目录
        for include_path in self.include_paths:
            src_path = os.path.join(self.sdk_path, include_path)
            dst_path = os.path.join(self.temp_dir, include_path)

            if not os.path.exists(src_path):
                print(f"警告: {include_path} 不存在，已跳过")
                continue

            if os.path.isdir(src_path):
                shutil.copytree(
                    src_path,
                    dst_path,
                    ignore=lambda dir, files: {
                        f for f in files if self._should_exclude(os.path.join(dir, f))
                    },
                )
            else:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

    def _create_zip(self):
        """创建ZIP压缩包"""
        print("正在创建ZIP压缩包...")

        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"wukongimfluttersdk_{timestamp}.zip"
        zip_path = os.path.join(self.output_dir, zip_name)

        # 创建ZIP文件
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, self.temp_dir)
                    zf.write(file_path, arc_name)

        return zip_path

    def _cleanup(self):
        """清理临时文件"""
        print("正在清理临时文件...")
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def pack(self):
        """执行打包流程"""
        try:
            # 创建输出目录
            os.makedirs(self.output_dir, exist_ok=True)

            # 复制文件
            self._copy_files()

            # 创建ZIP
            zip_path = self._create_zip()

            print(f"\n打包完成！")
            print(f"SDK包已保存到: {zip_path}")

            return zip_path

        except Exception as e:
            print(f"打包过程中出错: {str(e)}")
            raise
        finally:
            # 清理临时文件
            self._cleanup()


def main():
    """主函数"""
    # 获取当前目录作为SDK路径
    sdk_path = os.path.dirname(os.path.abspath(__file__))

    # 创建打包器并执行打包
    packer = SDKPacker(sdk_path=sdk_path)
    packer.pack()


if __name__ == "__main__":
    main()
