#!/usr/bin/env python3
"""
梁宁·增长思维30讲 - 增长计算器

提供以下计算功能：
1. 破局点评分计算
2. 商业模式健康度评估
3. 用户深度转化分析
4. 增长飞轮诊断
"""

import json
from typing import Dict, List, Optional, Tuple


def validate_score(value, name, min_val=1, max_val=5):
    """验证分数输入"""
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} 必须是数字")
    if value < min_val or value > max_val:
        raise ValueError(f"{name} 必须在 {min_val}-{max_val} 之间")


def validate_positive_int(value, name):
    """验证正整数输入"""
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} 必须是整数")
    if value < 0:
        raise ValueError(f"{name} 不能为负数")


def score_breakthrough(breadth: int, frequency: int, control: int) -> Dict:
    """
    破局点公式计算

    公式：破局点 = 相对广谱 × 高频 × 体验可控

    参数：
        breadth: 相对广谱性 (1-5分)
        frequency: 高频性 (1-5分)
        control: 体验可控性 (1-5分)

    返回：
        评分结果和建议
    """
    validate_score(breadth, "相对广谱性")
    validate_score(frequency, "高频性")
    validate_score(control, "体验可控性")

    score = breadth * frequency * control
    max_score = 125  # 5*5*5

    if score >= 80:
        verdict = "强破局点候选"
        suggestion = "具备成为破局点的条件，建议集中资源突破"
    elif score >= 50:
        verdict = "中等机会"
        suggestion = "需要强化某一维度，建议重点提升短板"
    elif score >= 25:
        verdict = "弱机会"
        suggestion = "三要素中有明显短板，需要系统性提升"
    else:
        verdict = "非破局点"
        suggestion = "不建议作为破局点，需重新寻找机会"

    return {
        "score": score,
        "max_score": max_score,
        "percentage": round(score / max_score * 100, 1),
        "breakdown": {
            "breadth": breadth,
            "frequency": frequency,
            "control": control
        },
        "verdict": verdict,
        "suggestion": suggestion
    }


def evaluate_business_model(goal_score: int, elements_score: int,
                             connection_score: int) -> Dict:
    """
    商业模式三要素健康度评估

    公式：商业模式健康度 = (目标 × 要素 × 连接) ^ (1/3)

    参数：
        goal_score: 目标清晰度 (1-5分)
        elements_score: 要素完整性 (1-5分)
        connection_score: 连接有效性 (1-5分)

    返回：
        健康度评估结果
    """
    validate_score(goal_score, "目标清晰度")
    validate_score(elements_score, "要素完整性")
    validate_score(connection_score, "连接有效性")

    health_score = (goal_score * elements_score * connection_score) ** (1/3)
    max_score = 5.0

    percentage = round(health_score / max_score * 100, 1)

    if health_score >= 4.0:
        verdict = "优秀"
        suggestions = ["保持当前模式优势", "持续优化各要素"]
    elif health_score >= 3.0:
        verdict = "良好"
        suggestions = ["某要素存在短板", "针对性地强化薄弱环节"]
    elif health_score >= 2.0:
        verdict = "一般"
        suggestions = ["需要系统性提升", "建议重新梳理商业模式"]
    else:
        verdict = "薄弱"
        suggestions = ["商业模式存在根本性问题", "建议重新思考定位"]

    # 找出最短板
    scores = {
        "目标": goal_score,
        "要素": elements_score,
        "连接": connection_score
    }
    weakest = min(scores, key=scores.get)

    return {
        "health_score": round(health_score, 2),
        "max_score": max_score,
        "percentage": percentage,
        "breakdown": scores,
        "weakest": weakest,
        "verdict": verdict,
        "suggestions": suggestions
    }


def analyze_user_depth(dau: int, mau: int, paying_users: int,
                       total_users: int, ugc_count: int,
                       nps_score: int) -> Dict:
    """
    用户深度四层分析

    公式：用户深化 = 流量 → 用户 → 会员 → 共同体

    参数：
        dau: 日活跃用户数
        mau: 月活跃用户数
        paying_users: 付费用户数
        total_users: 总用户数
        ugc_count: UGC内容数量
        nps_score: NPS净推荐值

    返回：
        用户深度诊断结果
    """
    validate_positive_int(dau, "日活跃用户数")
    validate_positive_int(mau, "月活跃用户数")
    validate_positive_int(paying_users, "付费用户数")
    validate_positive_int(total_users, "总用户数")
    validate_positive_int(ugc_count, "UGC内容数量")
    if not isinstance(nps_score, int) or nps_score < -100 or nps_score > 100:
        raise ValueError("NPS净推荐值必须在 -100 到 100 之间")

    # 计算关键比率
    stickiness = dau / mau if mau > 0 else 0  # 留存率
    pay_rate = paying_users / total_users if total_users > 0 else 0  # 付费率

    # 判断当前层级 - 使用更合理的分层逻辑
    if nps_score > 60:
        current_level = "共同体"
        level_desc = "用户极度认同，主动传播"
        next_level = None
    elif nps_score > 50 and ugc_count > 500:
        current_level = "共同体"
        level_desc = "用户高度认同，开始主动传播"
        next_level = None
    elif pay_rate > 0.2:
        current_level = "会员"
        level_desc = "用户建立了付费关系"
        next_level = "共同体"
    elif stickiness > 0.2:
        current_level = "用户"
        level_desc = "用户有持续使用习惯"
        next_level = "会员"
    else:
        current_level = "流量"
        level_desc = "用户关系浅，多为一次性访问"
        next_level = "用户"

    # 计算各层级转化建议
    level_data = {
        "共同体": {
            "indicator": f"NPS={nps_score}>50, UGC={ugc_count}>1000",
            "key_metric": "NPS净推荐值、UGC数量"
        },
        "会员": {
            "indicator": f"付费率={round(pay_rate*100,1)}%>20%",
            "key_metric": "付费率、复购率"
        },
        "用户": {
            "indicator": f"DAU/MAU={round(stickiness*100,1)}%>20%",
            "key_metric": "DAU/MAU留存率"
        },
        "流量": {
            "indicator": "以一次性访问为主",
            "key_metric": "曝光量、点击率"
        }
    }

    return {
        "current_level": current_level,
        "level_desc": level_desc,
        "next_level": next_level,
        "metrics": {
            "stickiness": round(stickiness * 100, 1),
            "pay_rate": round(pay_rate * 100, 1),
            "ugc_count": ugc_count,
            "nps_score": nps_score
        },
        "level_data": level_data.get(current_level),
        "suggestions": _get_depth_suggestions(current_level, stickiness,
                                              pay_rate, nps_score, ugc_count)
    }


def _get_depth_suggestions(current_level: str, stickiness: float,
                           pay_rate: float, nps_score: int,
                           ugc_count: int) -> List[str]:
    """根据当前层级生成建议"""
    suggestions = []

    if current_level == "流量":
        suggestions.append("建立用户账户体系，沉淀用户")
        suggestions.append("优化首购体验，提高转化")
        if stickiness < 0.1:
            suggestions.append("提升产品核心价值，增加用户粘性")
    elif current_level == "用户":
        suggestions.append("设计会员权益体系")
        suggestions.append("优化留存，增强使用习惯")
        if pay_rate < 0.1:
            suggestions.append("评估付费点设置是否合理")
    elif current_level == "会员":
        suggestions.append("提升复购率，增加LTV")
        suggestions.append("建立用户社群，培养归属感")
        if nps_score < 50:
            suggestions.append("提升产品体验，提高用户推荐意愿")
        if ugc_count < 100:
            suggestions.append("建立UGC激励机制")
    elif current_level == "共同体":
        suggestions.append("维护共同体氛围，防止流失")
        suggestions.append("培养KOL，放大传播效应")

    return suggestions


def diagnose_flywheel(core_delivery: int, reinforcement: int,
                      network_effect: int) -> Dict:
    """
    用户增长飞轮诊断

    公式：飞轮 = 核心交付 × 增强回路 × 网络效应

    参数：
        core_delivery: 核心交付清晰度 (1-5分)
        reinforcement: 增强回路强度 (1-5分)
        network_effect: 网络效应程度 (1-5分)

    返回：
        飞轮诊断结果
    """
    validate_score(core_delivery, "核心交付清晰度")
    validate_score(reinforcement, "增强回路强度")
    validate_score(network_effect, "网络效应程度")

    flywheel_score = core_delivery * reinforcement * network_effect
    max_score = 125

    # 评估各要素状态
    elements = {
        "核心交付": {
            "score": core_delivery,
            "status": "[OK]" if core_delivery >= 4 else "[WARN]" if core_delivery >= 3 else "[FAIL]",
            "desc": "清晰" if core_delivery >= 4 else "模糊" if core_delivery < 3 else "一般"
        },
        "增强回路": {
            "score": reinforcement,
            "status": "[OK]" if reinforcement >= 4 else "[WARN]" if reinforcement >= 3 else "[FAIL]",
            "desc": "强" if reinforcement >= 4 else "弱" if reinforcement < 3 else "一般"
        },
        "网络效应": {
            "score": network_effect,
            "status": "[OK]" if network_effect >= 4 else "[WARN]" if network_effect >= 3 else "[FAIL]",
            "desc": "明显" if network_effect >= 4 else "不明显" if network_effect < 3 else "初步形成"
        }
    }

    # 生成诊断结论
    if flywheel_score >= 80:
        verdict = "飞轮已成型"
        conclusion = "三个要素形成正向循环，增长具有可持续性"
    elif flywheel_score >= 50:
        verdict = "飞轮雏形"
        weakest = min(elements.items(), key=lambda x: x[1]["score"])
        conclusion = f"{weakest[0]}是当前瓶颈，需要重点强化"
    elif flywheel_score >= 25:
        verdict = "飞轮薄弱"
        conclusion = "需要系统性建设，建议从核心交付开始"
    else:
        verdict = "飞轮缺失"
        conclusion = "需要重新思考增长模式，建议先找到核心交付"

    return {
        "flywheel_score": flywheel_score,
        "max_score": max_score,
        "percentage": round(flywheel_score / max_score * 100, 1),
        "elements": elements,
        "verdict": verdict,
        "conclusion": conclusion,
        "suggestions": _get_flywheel_suggestions(elements, flywheel_score)
    }


def _get_flywheel_suggestions(elements: Dict, score: int) -> List[str]:
    """根据飞轮诊断生成建议"""
    suggestions = []

    if elements["核心交付"]["score"] < 4:
        suggestions.append(f"核心交付({elements['核心交付']['score']}/5)：明确定位核心价值主张")
    if elements["增强回路"]["score"] < 4:
        suggestions.append(f"增强回路({elements['增强回路']['score']}/5)：设计用户自增长机制")
    if elements["网络效应"]["score"] < 4:
        suggestions.append(f"网络效应({elements['网络效应']['score']}/5)：增加用户间互动场景")

    if score < 50:
        suggestions.append("建议按顺序建设：先核心交付，再增强回路，最后网络效应")

    return suggestions


def print_header(title: str) -> None:
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_result(data: Dict, indent: int = 2) -> None:
    """打印结果"""
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{' '*indent}{key}:")
            print_result(value, indent + 2)
        elif isinstance(value, list):
            print(f"{' '*indent}{key}:")
            for item in value:
                print(f"{' '*(indent+2)}- {item}")
        else:
            print(f"{' '*indent}{key}: {value}")


def interactive_mode():
    """交互模式"""
    print("\n" + "="*60)
    print("  梁宁·增长思维30讲 - 增长计算器")
    print("="*60)
    print("\n选择一个计算功能：")
    print("1. 破局点评分计算")
    print("2. 商业模式健康度评估")
    print("3. 用户深度四层分析")
    print("4. 增长飞轮诊断")
    print("5. 全部运行（示例数据）")
    print("0. 退出")

    while True:
        choice = input("\n请选择 (0-5): ").strip()

        if choice == "0":
            print("再见！")
            break

        if choice == "1":
            print("\n--- 破局点公式计算 ---")
            try:
                breadth = int(input("相对广谱性 (1-5): "))
                frequency = int(input("高频性 (1-5): "))
                control = int(input("体验可控性 (1-5): "))
                result = score_breakthrough(breadth, frequency, control)
                print_header("破局点评分结果")
                print_result(result)
            except ValueError:
                print("请输入有效的数字！")

        elif choice == "2":
            print("\n--- 商业模式三要素评估 ---")
            try:
                goal = int(input("目标清晰度 (1-5): "))
                elements = int(input("要素完整性 (1-5): "))
                connection = int(input("连接有效性 (1-5): "))
                result = evaluate_business_model(goal, elements, connection)
                print_header("商业模式健康度评估")
                print_result(result)
            except ValueError:
                print("请输入有效的数字！")

        elif choice == "3":
            print("\n--- 用户深度四层分析 ---")
            try:
                dau = int(input("日活跃用户数 (DAU): "))
                mau = int(input("月活跃用户数 (MAU): "))
                paying = int(input("付费用户数: "))
                total = int(input("总用户数: "))
                ugc = int(input("UGC内容数量: "))
                nps = int(input("NPS净推荐值 (-100~100): "))
                result = analyze_user_depth(dau, mau, paying, total, ugc, nps)
                print_header("用户深度诊断结果")
                print_result(result)
            except ValueError:
                print("请输入有效的数字！")

        elif choice == "4":
            print("\n--- 增长飞轮诊断 ---")
            try:
                core = int(input("核心交付清晰度 (1-5): "))
                reinforcement = int(input("增强回路强度 (1-5): "))
                network = int(input("网络效应程度 (1-5): "))
                result = diagnose_flywheel(core, reinforcement, network)
                print_header("增长飞轮诊断结果")
                print_result(result)
            except ValueError:
                print("请输入有效的数字！")

        elif choice == "5":
            print("\n--- 使用示例数据运行全部计算 ---")

            print_header("1. 破局点评分")
            result1 = score_breakthrough(4, 5, 4)
            print_result(result1)

            print_header("2. 商业模式健康度")
            result2 = evaluate_business_model(4, 3, 4)
            print_result(result2)

            print_header("3. 用户深度分析")
            result3 = analyze_user_depth(10000, 50000, 25000, 100000, 500, 55)
            print_result(result3)

            print_header("4. 增长飞轮诊断")
            result4 = diagnose_flywheel(4, 4, 3)
            print_result(result4)

        else:
            print("无效选择，请输入 0-5")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        # 批处理模式，输出JSON
        sample_data = {
            "breakthrough": score_breakthrough(4, 5, 4),
            "business_model": evaluate_business_model(4, 3, 4),
            "user_depth": analyze_user_depth(10000, 50000, 25000, 100000, 500, 55),
            "flywheel": diagnose_flywheel(4, 4, 3)
        }
        print(json.dumps(sample_data, indent=2, ensure_ascii=False))
    else:
        interactive_mode()
