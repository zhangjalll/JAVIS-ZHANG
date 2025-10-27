#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI中医心血管问诊系统 - 测试脚本
测试不同证型的辨证分析
"""

from tcm_cardiovascular_consult import TCMCardiovascularConsult


class TestCase:
    """测试用例类"""

    def __init__(self, name, description, symptoms, expected_syndrome):
        self.name = name
        self.description = description
        self.symptoms = symptoms
        self.expected_syndrome = expected_syndrome


def create_test_cases():
    """创建测试用例"""
    test_cases = [
        TestCase(
            name="心气虚证",
            description="患者主要表现为心悸、气短、乏力，活动后加重",
            symptoms=['心悸', '气短', '乏力', '自汗', '活动后加重', '面色淡白', '舌淡', '脉虚弱'],
            expected_syndrome='心气虚证'
        ),
        TestCase(
            name="心阳虚证",
            description="患者畏寒肢冷明显，面色苍白，舌淡胖",
            symptoms=['心悸', '胸闷', '畏寒肢冷', '面色苍白', '气短', '神疲乏力', '舌淡胖', '苔白滑', '脉沉迟'],
            expected_syndrome='心阳虚证'
        ),
        TestCase(
            name="心血瘀阻证",
            description="患者胸痛明显，刺痛固定，夜间加重，舌质紫暗",
            symptoms=['胸痛', '胸闷', '心悸', '刺痛固定', '夜间加重', '面色晦暗', '舌质紫暗', '有瘀斑', '脉涩'],
            expected_syndrome='心血瘀阻证'
        ),
        TestCase(
            name="痰浊内阻证",
            description="患者体型肥胖，胸闷痰多，舌苔厚腻",
            symptoms=['胸闷', '气短', '痰多', '体型肥胖', '身重困倦', '恶心', '舌体胖大', '苔厚腻', '脉滑'],
            expected_syndrome='痰浊内阻证'
        ),
        TestCase(
            name="气阴两虚证",
            description="患者心悸气短，伴口干、五心烦热、盗汗",
            symptoms=['心悸', '气短', '口干', '五心烦热', '盗汗', '失眠', '腰膝酸软', '舌红', '少苔', '脉细数'],
            expected_syndrome='气阴两虚证'
        ),
        TestCase(
            name="混合证型1",
            description="气虚血瘀兼夹（心气虚+血瘀）",
            symptoms=['心悸', '气短', '乏力', '胸痛', '刺痛固定', '舌质紫暗', '脉虚弱'],
            expected_syndrome='心气虚证'  # 预期主证型
        ),
        TestCase(
            name="混合证型2",
            description="阳虚水停（心阳虚+痰浊）",
            symptoms=['心悸', '畏寒肢冷', '胸闷', '痰多', '体型肥胖', '舌淡胖', '苔白滑', '脉沉迟'],
            expected_syndrome='心阳虚证'  # 预期主证型
        )
    ]

    return test_cases


def run_test_case(test_case):
    """运行单个测试用例"""
    print("\n" + "="*80)
    print(f"测试用例：{test_case.name}")
    print("="*80)
    print(f"病例描述：{test_case.description}")
    print(f"症状列表：{', '.join(test_case.symptoms)}")
    print("\n" + "-"*80)

    # 创建问诊实例
    consult = TCMCardiovascularConsult()

    # 模拟症状数据
    consult.user_data['detailed_symptoms']['symptoms'] = test_case.symptoms.copy()

    # 进行辨证分析
    sorted_syndromes = consult.analyze_syndrome()

    # 显示分析结果
    print("【辨证分析结果】\n")

    # 显示所有证型得分
    print("各证型匹配度：")
    for syndrome, data in sorted_syndromes:
        score = data['score']
        matched = data['matched']
        marker = "★" if syndrome == sorted_syndromes[0][0] else " "
        print(f"{marker} {syndrome}: {score}分")
        if matched and score > 0:
            print(f"    匹配症状: {', '.join(matched)}")

    # 判断测试结果
    primary_syndrome = sorted_syndromes[0][0]
    primary_score = sorted_syndromes[0][1]['score']

    print("\n" + "-"*80)
    print(f"诊断结果：{primary_syndrome} (得分: {primary_score})")
    print(f"预期结果：{test_case.expected_syndrome}")

    if primary_syndrome == test_case.expected_syndrome:
        print("✓ 测试通过！")
        result = True
    else:
        print("✗ 测试未通过（主证型不匹配，可能存在兼夹证）")
        result = False

    # 显示次要证型
    secondary_syndromes = []
    for syndrome, data in sorted_syndromes[1:]:
        if data['score'] >= primary_score * 0.5:
            secondary_syndromes.append(f"{syndrome}({data['score']}分)")

    if secondary_syndromes:
        print(f"兼夹证型：{', '.join(secondary_syndromes)}")

    return result


def main():
    """主测试函数"""
    print("="*80)
    print("          AI中医心血管问诊系统 - 自动测试")
    print("="*80)
    print("\n本测试将验证不同证型的辨证准确性\n")

    test_cases = create_test_cases()

    passed = 0
    total = len(test_cases)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{total}] ", end="")
        if run_test_case(test_case):
            passed += 1

    # 显示总结
    print("\n" + "="*80)
    print("                        测试总结")
    print("="*80)
    print(f"\n总测试用例数: {total}")
    print(f"通过: {passed}")
    print(f"未通过: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%\n")

    if passed == total:
        print("✓ 所有测试用例通过！")
    else:
        print("⚠ 部分测试未通过，可能需要调整证型权重")

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
