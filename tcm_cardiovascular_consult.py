#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI中医心血管问诊对话系统
基于规则的辨证分析系统
"""

class TCMCardiovascularConsult:
    """中医心血管问诊类"""

    def __init__(self):
        """初始化问诊系统"""
        self.user_data = {
            'chief_complaint': [],      # 主诉症状
            'detailed_symptoms': {},    # 详细症状
            'tcm_signs': {},           # 中医四诊
            'lifestyle': {},           # 生活习惯
            'scores': {}               # 各证型得分
        }

        self._init_knowledge_base()
        self._init_questions()

    def _init_knowledge_base(self):
        """初始化中医证型知识库"""
        self.syndrome_types = {
            '心气虚证': {
                'description': '心气不足，鼓动无力',
                'main_symptoms': ['心悸', '气短', '乏力'],
                'secondary_symptoms': ['自汗', '活动后加重', '面色淡白'],
                'tongue': ['舌淡', '苔薄白'],
                'pulse': ['脉虚弱'],
                'weight': {
                    '心悸': 3, '气短': 3, '乏力': 2, '自汗': 2,
                    '活动后加重': 2, '面色淡白': 1,
                    '舌淡': 2, '脉虚弱': 2
                }
            },
            '心阳虚证': {
                'description': '心阳不足，温煦失职',
                'main_symptoms': ['心悸', '胸闷', '畏寒肢冷'],
                'secondary_symptoms': ['面色苍白', '气短', '自汗', '神疲乏力'],
                'tongue': ['舌淡胖', '苔白滑'],
                'pulse': ['脉沉迟', '脉微细'],
                'weight': {
                    '心悸': 2, '胸闷': 2, '畏寒肢冷': 3, '面色苍白': 2,
                    '气短': 2, '自汗': 2, '神疲乏力': 2,
                    '舌淡胖': 3, '苔白滑': 2, '脉沉迟': 3, '脉微细': 3
                }
            },
            '心血瘀阻证': {
                'description': '血行不畅，瘀阻心脉',
                'main_symptoms': ['胸痛', '胸闷', '心悸'],
                'secondary_symptoms': ['刺痛固定', '夜间加重', '面色晦暗', '唇舌紫暗'],
                'tongue': ['舌质紫暗', '有瘀斑'],
                'pulse': ['脉涩', '脉结代'],
                'weight': {
                    '胸痛': 3, '胸闷': 2, '心悸': 2, '刺痛固定': 3,
                    '夜间加重': 2, '面色晦暗': 2, '唇舌紫暗': 2,
                    '舌质紫暗': 3, '有瘀斑': 3, '脉涩': 2, '脉结代': 3
                }
            },
            '痰浊内阻证': {
                'description': '痰浊阻滞，胸阳不振',
                'main_symptoms': ['胸闷', '气短', '痰多'],
                'secondary_symptoms': ['体型肥胖', '身重困倦', '恶心', '纳呆'],
                'tongue': ['舌体胖大', '苔厚腻'],
                'pulse': ['脉滑'],
                'weight': {
                    '胸闷': 3, '气短': 2, '痰多': 3, '体型肥胖': 2,
                    '身重困倦': 2, '恶心': 1, '纳呆': 1,
                    '舌体胖大': 2, '苔厚腻': 3, '脉滑': 2
                }
            },
            '气阴两虚证': {
                'description': '气阴亏虚，心失所养',
                'main_symptoms': ['心悸', '气短', '口干'],
                'secondary_symptoms': ['五心烦热', '盗汗', '失眠', '腰膝酸软'],
                'tongue': ['舌红', '少苔'],
                'pulse': ['脉细数'],
                'weight': {
                    '心悸': 3, '气短': 2, '口干': 2, '五心烦热': 3,
                    '盗汗': 2, '失眠': 2, '腰膝酸软': 2,
                    '舌红': 3, '少苔': 2, '脉细数': 3
                }
            }
        }

        # 调理建议库
        self.treatment_advice = {
            '心气虚证': {
                'principle': '益气养心',
                'diet': ['党参', '黄芪', '大枣', '山药', '莲子', '桂圆'],
                'acupoints': ['内关', '心俞', '膻中', '足三里'],
                'lifestyle': ['避免过度劳累', '保证充足睡眠', '适度运动如太极拳', '保持心情舒畅']
            },
            '心阳虚证': {
                'principle': '温补心阳',
                'diet': ['桂枝', '干姜', '附子（需医师指导）', '羊肉', '核桃', '韭菜'],
                'acupoints': ['神阙', '关元', '心俞', '膻中'],
                'lifestyle': ['注意保暖', '避免寒冷刺激', '温补饮食', '艾灸相关穴位']
            },
            '心血瘀阻证': {
                'principle': '活血化瘀，通脉止痛',
                'diet': ['山楂', '丹参', '红花（少量）', '黑木耳', '洋葱', '西红柿'],
                'acupoints': ['内关', '郄门', '膻中', '血海'],
                'lifestyle': ['避免情绪激动', '戒烟限酒', '适度有氧运动', '定期监测血压']
            },
            '痰浊内阻证': {
                'principle': '化痰降浊，宽胸理气',
                'diet': ['陈皮', '半夏（需医师指导）', '白萝卜', '冬瓜', '薏米', '荷叶'],
                'acupoints': ['丰隆', '中脘', '足三里', '膻中'],
                'lifestyle': ['控制体重', '清淡饮食', '减少油腻甘厚', '增加运动量']
            },
            '气阴两虚证': {
                'principle': '益气养阴',
                'diet': ['西洋参', '麦冬', '五味子', '百合', '枸杞', '银耳'],
                'acupoints': ['内关', '三阴交', '太溪', '膻中'],
                'lifestyle': ['避免熬夜', '保持充足睡眠', '避免过度劳累', '多饮水']
            }
        }

    def _init_questions(self):
        """初始化问题库"""
        # 主诉症状选择
        self.chief_complaints = {
            '1': '胸痛或胸闷',
            '2': '心悸（心跳加快或不规律）',
            '3': '气短或呼吸困难',
            '4': '乏力或疲倦',
            '5': '头晕',
            '6': '其他'
        }

        # 胸痛详细询问
        self.chest_pain_questions = {
            'location': {
                'question': '胸痛的部位？',
                'options': {
                    '1': '心前区（左胸）',
                    '2': '胸骨后',
                    '3': '整个胸部',
                    '4': '不固定'
                }
            },
            'nature': {
                'question': '疼痛性质？',
                'options': {
                    '1': '刺痛（像针扎）',
                    '2': '闷痛（压迫感）',
                    '3': '隐痛',
                    '4': '绞痛'
                },
                'mapping': {
                    '1': '刺痛固定',  # 血瘀特征
                    '2': '胸闷',
                    '3': '胸闷',
                    '4': '胸痛'
                }
            },
            'duration': {
                'question': '持续时间？',
                'options': {
                    '1': '数秒',
                    '2': '数分钟',
                    '3': '数小时',
                    '4': '持续性'
                }
            },
            'trigger': {
                'question': '什么情况下加重？',
                'options': {
                    '1': '活动后',
                    '2': '夜间',
                    '3': '情绪激动',
                    '4': '无明显诱因'
                },
                'mapping': {
                    '1': '活动后加重',
                    '2': '夜间加重',  # 血瘀特征
                    '3': '胸痛',
                    '4': '胸痛'
                }
            }
        }

        # 伴随症状
        self.associated_symptoms = {
            '1': {'name': '畏寒怕冷', 'key': '畏寒肢冷'},
            '2': {'name': '手脚冰凉', 'key': '畏寒肢冷'},
            '3': {'name': '出汗（活动时）', 'key': '自汗'},
            '4': {'name': '盗汗（睡觉时）', 'key': '盗汗'},
            '5': {'name': '失眠多梦', 'key': '失眠'},
            '6': {'name': '口干口渴', 'key': '口干'},
            '7': {'name': '手心脚心发热', 'key': '五心烦热'},
            '8': {'name': '痰多', 'key': '痰多'},
            '9': {'name': '身体沉重', 'key': '身重困倦'},
            '10': {'name': '恶心', 'key': '恶心'},
            '11': {'name': '食欲不振', 'key': '纳呆'},
            '12': {'name': '腰膝酸软', 'key': '腰膝酸软'},
            '0': {'name': '没有了', 'key': None}
        }

        # 舌象选择
        self.tongue_options = {
            'color': {
                'question': '舌头颜色？',
                'options': {
                    '1': '淡红（正常）',
                    '2': '淡白',
                    '3': '红',
                    '4': '紫暗'
                },
                'mapping': {
                    '1': None,
                    '2': '舌淡',
                    '3': '舌红',
                    '4': '舌质紫暗'
                }
            },
            'shape': {
                'question': '舌体形状？',
                'options': {
                    '1': '正常',
                    '2': '胖大（有齿痕）',
                    '3': '瘦小'
                },
                'mapping': {
                    '1': None,
                    '2': '舌体胖大',
                    '3': None
                }
            },
            'coating': {
                'question': '舌苔情况？',
                'options': {
                    '1': '薄白（正常）',
                    '2': '厚腻',
                    '3': '少苔或无苔',
                    '4': '白滑'
                },
                'mapping': {
                    '1': '苔薄白',
                    '2': '苔厚腻',
                    '3': '少苔',
                    '4': '苔白滑'
                }
            },
            'spots': {
                'question': '舌头是否有瘀斑或瘀点？',
                'options': {
                    '1': '没有',
                    '2': '有'
                },
                'mapping': {
                    '1': None,
                    '2': '有瘀斑'
                }
            }
        }

        # 脉象（简化版）
        self.pulse_options = {
            'question': '您的脉搏感觉（可自测）？',
            'options': {
                '1': '跳动有力',
                '2': '跳动无力',
                '3': '跳动较快',
                '4': '跳动较慢',
                '5': '不规律（有停顿）'
            },
            'mapping': {
                '1': None,
                '2': '脉虚弱',
                '3': '脉细数',
                '4': '脉沉迟',
                '5': '脉结代'
            }
        }

        # 面色
        self.complexion_options = {
            'question': '面色如何？',
            'options': {
                '1': '正常红润',
                '2': '淡白',
                '3': '苍白',
                '4': '晦暗发青'
            },
            'mapping': {
                '1': None,
                '2': '面色淡白',
                '3': '面色苍白',
                '4': '面色晦暗'
            }
        }

        # 体型
        self.body_type_options = {
            'question': '您的体型？',
            'options': {
                '1': '正常',
                '2': '偏瘦',
                '3': '偏胖或肥胖'
            },
            'mapping': {
                '1': None,
                '2': None,
                '3': '体型肥胖'
            }
        }

    def show_welcome(self):
        """显示欢迎信息"""
        print("\n" + "="*70)
        print("                AI中医心血管问诊系统")
        print("="*70)
        print("\n欢迎使用AI中医心血管问诊系统！")
        print("\n本系统将通过一系列问题了解您的症状，并基于中医理论进行辨证分析。")
        print("请根据您最近的实际情况如实回答。\n")
        print("⚠️  重要提示：")
        print("   • 本系统仅供参考，不能替代专业医疗诊断")
        print("   • 如有严重不适，请立即就医")
        print("   • 心血管疾病需要专业医师诊治\n")

    def collect_chief_complaint(self):
        """收集主诉症状"""
        print("="*70)
        print("【第一步：主要症状】")
        print("="*70)
        print("\n请选择您当前的主要症状（可多选，输入数字，输入0结束）：\n")

        for key, value in sorted(self.chief_complaints.items()):
            if key != '0':
                print(f"  {key}. {value}")
        print(f"  0. 完成选择\n")

        selected = []
        while True:
            choice = input("请输入选项（0完成）: ").strip()

            if choice == '0':
                if selected:
                    break
                else:
                    print("❌ 请至少选择一个症状\n")
                    continue

            if choice in self.chief_complaints and choice not in selected:
                selected.append(choice)
                print(f"✓ 已选择：{self.chief_complaints[choice]}\n")
            elif choice in selected:
                print("❌ 该选项已选择\n")
            else:
                print("❌ 无效输入\n")

        self.user_data['chief_complaint'] = [self.chief_complaints[s] for s in selected]
        print(f"\n您的主要症状：{', '.join(self.user_data['chief_complaint'])}")

    def ask_chest_pain_details(self):
        """详细询问胸痛情况"""
        print("\n" + "-"*70)
        print("【详细询问：胸痛相关】")
        print("-"*70 + "\n")

        for key, item in self.chest_pain_questions.items():
            print(f"{item['question']}")
            for opt_key, opt_value in item['options'].items():
                print(f"  {opt_key}. {opt_value}")

            while True:
                answer = input("请选择: ").strip()
                if answer in item['options']:
                    # 存储原始答案
                    self.user_data['detailed_symptoms'][key] = item['options'][answer]

                    # 映射到症状关键词
                    if 'mapping' in item:
                        symptom_key = item['mapping'].get(answer)
                        if symptom_key:
                            if 'symptoms' not in self.user_data['detailed_symptoms']:
                                self.user_data['detailed_symptoms']['symptoms'] = []
                            self.user_data['detailed_symptoms']['symptoms'].append(symptom_key)

                    print(f"✓ {item['options'][answer]}\n")
                    break
                else:
                    print("❌ 无效输入，请重新选择\n")

    def collect_associated_symptoms(self):
        """收集伴随症状"""
        print("\n" + "="*70)
        print("【第二步：伴随症状】")
        print("="*70)
        print("\n除了主要症状，您还有以下症状吗？（可多选，输入0结束）：\n")

        for key, value in sorted(self.associated_symptoms.items(), key=lambda x: x[0]):
            print(f"  {key}. {value['name']}")

        print()
        selected_symptoms = []

        while True:
            choice = input("请输入选项（0结束）: ").strip()

            if choice == '0':
                break

            if choice in self.associated_symptoms and choice != '0':
                symptom = self.associated_symptoms[choice]
                if symptom['key'] and symptom['key'] not in selected_symptoms:
                    selected_symptoms.append(symptom['key'])
                    print(f"✓ 已记录：{symptom['name']}\n")
                elif symptom['key'] in selected_symptoms:
                    print("❌ 该症状已选择\n")
            else:
                print("❌ 无效输入\n")

        if 'symptoms' not in self.user_data['detailed_symptoms']:
            self.user_data['detailed_symptoms']['symptoms'] = []
        self.user_data['detailed_symptoms']['symptoms'].extend(selected_symptoms)

    def collect_tcm_signs(self):
        """收集中医四诊信息"""
        print("\n" + "="*70)
        print("【第三步：中医体征】")
        print("="*70)
        print("\n接下来了解一些中医特征，请仔细观察后回答：\n")

        tcm_symptoms = []

        # 舌象
        print("【舌象观察】")
        print("请对着镜子观察您的舌头\n")

        for key, item in self.tongue_options.items():
            print(f"{item['question']}")
            for opt_key, opt_value in item['options'].items():
                print(f"  {opt_key}. {opt_value}")

            while True:
                answer = input("请选择: ").strip()
                if answer in item['options']:
                    self.user_data['tcm_signs'][f'tongue_{key}'] = item['options'][answer]
                    symptom = item['mapping'].get(answer)
                    if symptom:
                        tcm_symptoms.append(symptom)
                    print(f"✓ {item['options'][answer]}\n")
                    break
                else:
                    print("❌ 无效输入\n")

        # 脉象
        print("\n【脉象自测】")
        print("请将食指、中指、无名指放在手腕桡动脉处（大拇指侧）\n")
        print(f"{self.pulse_options['question']}")
        for opt_key, opt_value in self.pulse_options['options'].items():
            print(f"  {opt_key}. {opt_value}")

        while True:
            answer = input("请选择: ").strip()
            if answer in self.pulse_options['options']:
                self.user_data['tcm_signs']['pulse'] = self.pulse_options['options'][answer]
                symptom = self.pulse_options['mapping'].get(answer)
                if symptom:
                    tcm_symptoms.append(symptom)
                print(f"✓ {self.pulse_options['options'][answer]}\n")
                break
            else:
                print("❌ 无效输入\n")

        # 面色
        print(f"{self.complexion_options['question']}")
        for opt_key, opt_value in self.complexion_options['options'].items():
            print(f"  {opt_key}. {opt_value}")

        while True:
            answer = input("请选择: ").strip()
            if answer in self.complexion_options['options']:
                self.user_data['tcm_signs']['complexion'] = self.complexion_options['options'][answer]
                symptom = self.complexion_options['mapping'].get(answer)
                if symptom:
                    tcm_symptoms.append(symptom)
                print(f"✓ {self.complexion_options['options'][answer]}\n")
                break
            else:
                print("❌ 无效输入\n")

        # 体型
        print(f"{self.body_type_options['question']}")
        for opt_key, opt_value in self.body_type_options['options'].items():
            print(f"  {opt_key}. {opt_value}")

        while True:
            answer = input("请选择: ").strip()
            if answer in self.body_type_options['options']:
                self.user_data['tcm_signs']['body_type'] = self.body_type_options['options'][answer]
                symptom = self.body_type_options['mapping'].get(answer)
                if symptom:
                    tcm_symptoms.append(symptom)
                print(f"✓ {self.body_type_options['options'][answer]}\n")
                break
            else:
                print("❌ 无效输入\n")

        # 将中医症状添加到总症状列表
        if 'symptoms' not in self.user_data['detailed_symptoms']:
            self.user_data['detailed_symptoms']['symptoms'] = []
        self.user_data['detailed_symptoms']['symptoms'].extend(tcm_symptoms)

    def analyze_syndrome(self):
        """辨证分析"""
        print("\n" + "="*70)
        print("【智能分析中...】")
        print("="*70 + "\n")

        all_symptoms = self.user_data['detailed_symptoms'].get('symptoms', [])

        # 从主诉中提取症状
        for complaint in self.user_data['chief_complaint']:
            if '心悸' in complaint:
                all_symptoms.append('心悸')
            if '胸痛' in complaint or '胸闷' in complaint:
                all_symptoms.append('胸闷')
            if '气短' in complaint or '呼吸困难' in complaint:
                all_symptoms.append('气短')
            if '乏力' in complaint or '疲倦' in complaint:
                all_symptoms.append('乏力')

        # 计算各证型得分
        for syndrome_name, syndrome_data in self.syndrome_types.items():
            score = 0
            matched_symptoms = []

            for symptom in all_symptoms:
                if symptom in syndrome_data['weight']:
                    weight = syndrome_data['weight'][symptom]
                    score += weight
                    matched_symptoms.append(f"{symptom}({weight}分)")

            self.user_data['scores'][syndrome_name] = {
                'score': score,
                'matched': matched_symptoms
            }

        # 排序找出最可能的证型
        sorted_syndromes = sorted(
            self.user_data['scores'].items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )

        return sorted_syndromes

    def show_results(self, sorted_syndromes):
        """展示辨证结果"""
        print("="*70)
        print("                    辨证分析结果")
        print("="*70 + "\n")

        # 显示主要证型（得分最高的）
        if sorted_syndromes[0][1]['score'] > 0:
            primary_syndrome = sorted_syndromes[0][0]
            primary_score = sorted_syndromes[0][1]['score']
            primary_matched = sorted_syndromes[0][1]['matched']

            print(f"【主要证型】{primary_syndrome}")
            print(f"匹配度：{primary_score} 分\n")

            syndrome_info = self.syndrome_types[primary_syndrome]
            print(f"证型说明：{syndrome_info['description']}\n")

            print(f"匹配的症状特征：")
            for symptom in primary_matched:
                print(f"  • {symptom}")

            # 检查是否有次要证型（得分>总分30%）
            print("\n" + "-"*70)
            secondary_syndromes = []
            for syndrome, data in sorted_syndromes[1:]:
                if data['score'] >= primary_score * 0.5:  # 得分达到主证型50%以上
                    secondary_syndromes.append((syndrome, data['score']))

            if secondary_syndromes:
                print("【可能的兼夹证】")
                for syndrome, score in secondary_syndromes:
                    print(f"  • {syndrome} (匹配度: {score}分)")

            # 显示调理建议
            print("\n" + "="*70)
            print("                    调理建议")
            print("="*70 + "\n")

            advice = self.treatment_advice[primary_syndrome]

            print(f"【治则】{advice['principle']}\n")

            print("【食疗建议】")
            print("可适当食用以下食材：")
            for item in advice['diet']:
                print(f"  • {item}")

            print("\n【穴位保健】")
            print("可按摩或艾灸以下穴位（每日1-2次，每次10-15分钟）：")
            for point in advice['acupoints']:
                print(f"  • {point}")

            print("\n【生活调理】")
            for tip in advice['lifestyle']:
                print(f"  • {tip}")

        else:
            print("未能明确辨证，建议就医进行专业诊断。")

        # 显示所有证型得分（调试用）
        print("\n" + "="*70)
        print("【详细分析】各证型匹配度")
        print("="*70 + "\n")
        for syndrome, data in sorted_syndromes:
            print(f"{syndrome}: {data['score']}分")
            if data['matched']:
                print(f"  匹配症状: {', '.join(data['matched'])}")
            print()

        # 重要提示
        print("="*70)
        print("⚠️  重要提示")
        print("="*70)
        print("""
1. 本分析结果仅供参考，基于中医辨证理论的规则推理
2. 中医诊断需要专业医师四诊合参，本系统不能替代医师诊断
3. 心血管疾病可能危及生命，如有以下情况请立即就医：
   • 剧烈胸痛持续不缓解
   • 胸痛伴大汗、恶心、呼吸困难
   • 晕厥或意识丧失
   • 心悸严重影响日常生活
4. 建议定期体检，监测血压、血脂、血糖等指标
5. 食疗和穴位保健需在专业指导下进行
6. 如需用药，必须在中医师指导下使用
        """)
        print("="*70 + "\n")

    def run(self):
        """运行完整的问诊流程"""
        try:
            self.show_welcome()

            # 收集主诉
            self.collect_chief_complaint()

            # 如果主诉包含胸痛，详细询问
            if any('胸痛' in c or '胸闷' in c for c in self.user_data['chief_complaint']):
                self.ask_chest_pain_details()

            # 收集伴随症状
            self.collect_associated_symptoms()

            # 收集中医四诊信息
            self.collect_tcm_signs()

            # 辨证分析
            sorted_syndromes = self.analyze_syndrome()

            # 展示结果
            self.show_results(sorted_syndromes)

        except KeyboardInterrupt:
            print("\n\n问诊已取消。")
        except Exception as e:
            print(f"\n发生错误：{e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    consult = TCMCardiovascularConsult()
    consult.run()


if __name__ == "__main__":
    main()
