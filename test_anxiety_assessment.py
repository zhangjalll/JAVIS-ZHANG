#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
焦虑自测量表程序测试脚本
"""

from anxiety_assessment import AnxietyAssessment

def test_assessment():
    """测试评估程序"""
    print("开始测试焦虑自测量表程序...\n")

    # 测试案例1：轻微焦虑 (总分 3)
    print("=" * 60)
    print("测试案例 1：轻微焦虑")
    print("=" * 60)
    assessment1 = AnxietyAssessment()
    assessment1.answers = [0, 0, 1, 1, 0, 1, 0]  # 总分 3
    assessment1.show_results()

    # 测试案例2：轻度焦虑 (总分 7)
    print("\n" + "=" * 60)
    print("测试案例 2：轻度焦虑")
    print("=" * 60)
    assessment2 = AnxietyAssessment()
    assessment2.answers = [1, 1, 1, 1, 1, 1, 1]  # 总分 7
    assessment2.show_results()

    # 测试案例3：中度焦虑 (总分 12)
    print("\n" + "=" * 60)
    print("测试案例 3：中度焦虑")
    print("=" * 60)
    assessment3 = AnxietyAssessment()
    assessment3.answers = [2, 2, 2, 1, 2, 2, 1]  # 总分 12
    assessment3.show_results()

    # 测试案例4：重度焦虑 (总分 18)
    print("\n" + "=" * 60)
    print("测试案例 4：重度焦虑")
    print("=" * 60)
    assessment4 = AnxietyAssessment()
    assessment4.answers = [3, 3, 3, 2, 3, 2, 2]  # 总分 18
    assessment4.show_results()

    print("\n所有测试完成！✓")

if __name__ == "__main__":
    test_assessment()
