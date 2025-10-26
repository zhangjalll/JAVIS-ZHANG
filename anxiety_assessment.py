#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
焦虑自测量表程序
基于GAD-7（广泛性焦虑障碍量表）
"""

class AnxietyAssessment:
    """焦虑自测量表类"""

    def __init__(self):
        """初始化问题列表"""
        self.questions = [
            "感觉紧张、焦虑或急切",
            "不能够停止或控制担忧",
            "对各种各样的事情担忧过多",
            "很难放松下来",
            "由于不安而无法静坐",
            "变得容易烦恼或急躁",
            "感到似乎将有可怕的事情发生而害怕"
        ]

        self.options = {
            '0': {'text': '完全不会', 'score': 0},
            '1': {'text': '几天', 'score': 1},
            '2': {'text': '一半以上的天数', 'score': 2},
            '3': {'text': '几乎每天', 'score': 3}
        }

        self.score_levels = [
            {'range': (0, 4), 'level': '轻微焦虑', 'description': '您的焦虑程度较轻，属于正常范围'},
            {'range': (5, 9), 'level': '轻度焦虑', 'description': '您可能存在轻度焦虑，建议保持良好的生活习惯'},
            {'range': (10, 14), 'level': '中度焦虑', 'description': '您可能存在中度焦虑，建议寻求心理咨询'},
            {'range': (15, 21), 'level': '重度焦虑', 'description': '您可能存在重度焦虑，强烈建议寻求专业帮助'}
        ]

        self.answers = []

    def show_welcome(self):
        """显示欢迎信息"""
        print("\n" + "="*60)
        print("                   焦虑自测量表 (GAD-7)")
        print("="*60)
        print("\n说明：请回忆过去两周内，您被以下问题困扰的频率。")
        print("每个问题请选择最符合您情况的选项（输入对应数字）。\n")

    def show_options(self):
        """显示选项说明"""
        print("\n选项说明：")
        for key, value in self.options.items():
            print(f"  {key} - {value['text']}")
        print()

    def conduct_assessment(self):
        """进行测量"""
        self.show_welcome()
        self.show_options()

        print("-"*60)
        print("开始测评：\n")

        for i, question in enumerate(self.questions, 1):
            while True:
                print(f"问题 {i}/{len(self.questions)}：{question}")
                answer = input("请输入您的选择 (0-3): ").strip()

                if answer in self.options:
                    self.answers.append(int(answer))
                    print()
                    break
                else:
                    print("❌ 输入无效，请输入 0-3 之间的数字\n")

    def calculate_score(self):
        """计算总分"""
        return sum(self.answers)

    def get_assessment_result(self, total_score):
        """获取评估结果"""
        for level_info in self.score_levels:
            min_score, max_score = level_info['range']
            if min_score <= total_score <= max_score:
                return level_info
        return None

    def show_results(self):
        """展示评分结果"""
        print("="*60)
        print("                      测评结果")
        print("="*60)

        total_score = self.calculate_score()
        result = self.get_assessment_result(total_score)

        print(f"\n您的总分：{total_score} 分 (满分21分)")
        print(f"焦虑级别：{result['level']}")
        print(f"结果说明：{result['description']}")

        # 显示详细答案
        print("\n" + "-"*60)
        print("您的答案详情：")
        print("-"*60)
        for i, (question, answer) in enumerate(zip(self.questions, self.answers), 1):
            option_text = self.options[str(answer)]['text']
            print(f"{i}. {question}")
            print(f"   回答: {option_text} ({answer}分)\n")

        print("-"*60)
        print("\n温馨提示：")
        print("• 本测评仅供参考，不能替代专业医疗诊断")
        print("• 如果您感到严重不适，请及时寻求专业心理咨询或医疗帮助")
        print("• 保持规律作息、适度运动、与他人交流有助于缓解焦虑")
        print("="*60 + "\n")

    def run(self):
        """运行完整的测评流程"""
        try:
            self.conduct_assessment()
            self.show_results()
        except KeyboardInterrupt:
            print("\n\n测评已取消。")
        except Exception as e:
            print(f"\n发生错误：{e}")


def main():
    """主函数"""
    assessment = AnxietyAssessment()
    assessment.run()


if __name__ == "__main__":
    main()
