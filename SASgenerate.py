import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from openpyxl import Workbook
import os

# 设置随机种子以保证可重复性
np.random.seed(42)

# 常量
NUM_PEOPLE_PER_SUBGROUP = 10  # 每个子组的人数
REVERSE_ITEMS = [5, 9, 13, 17, 19]  # 需要反向评分的题目

# 表1中的统计数据
SAS_STATS = {
    "第一组": {
        "正常高值血压组": {
            "前": {"mean": 49.3, "std_dev": 4.8, "bp_control_rate": 87.3},
            "后": {"mean": 47.3, "std_dev": 3.5, "bp_control_rate": 87.3}
        },
        "高血压组": {
            "前": {"mean": 58.6, "std_dev": 5.3, "bp_control_rate": 80.2},
            "后": {"mean": 51.6, "std_dev": 3.2, "bp_control_rate": 80.2}
        }
    },
    "第二组": {
        "正常高值血压组": {
            "前": {"mean": 49.8, "std_dev": 4.8, "bp_control_rate": 96.2},
            "后": {"mean": 39.2, "std_dev": 2.6, "bp_control_rate": 96.2}
        },
        "高血压组": {
            "前": {"mean": 58.2, "std_dev": 5.2, "bp_control_rate": 90.4},
            "后": {"mean": 43.1, "std_dev": 2.8, "bp_control_rate": 90.4}
        }
    }
}

# 生成姓名的函数
def generate_names(n):
    first_names = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴", 
                  "郑", "孙", "马", "朱", "胡", "林", "郭", "何", "高", "罗"]
    last_names = ["伟", "芳", "娜", "秀英", "敏", "静", "强", "磊", "军", "洋",
                 "勇", "艳", "杰", "涛", "明", "超", "霞", "平", "刚", "桂英"]
    
    names = []
    for i in range(n):
        name = random.choice(first_names) + random.choice(last_names)
        names.append(name)
    
    return names

# 生成问卷回答并计算SAS得分的函数
def generate_sas_data(mean_score, std_dev, n, group_name, bp_group, is_post=False):
    # 生成目标标准分数
    target_scores = np.random.normal(mean_score, std_dev, n)
    target_scores = np.clip(target_scores, 25, 100)  # 限制在合理范围内
    
    # 转换为原始分数，除以1.25
    raw_scores = target_scores / 1.25
    
    data = []
    for i in range(n):
        # 生成一组回答以达到目标原始分数
        responses = generate_responses_for_score(raw_scores[i])
        
        # 计算实际得分以验证
        score = calculate_sas_score(responses)
        
        # 将数字回答转换为字母（1->A, 2->B, 等）
        letter_responses = {f"题{j+1}选项": chr(64 + responses[j]) for j in range(20)}
        
        # 添加此人的数据
        person_data = {
            "编号": i+1,
            "姓名": generate_names(1)[0],
            "血压组": bp_group,
            **letter_responses,
            "SAS得分": int(round(score))
        }
        data.append(person_data)
    
    return pd.DataFrame(data)

# 生成回答以达到目标分数的函数
def generate_responses_for_score(target_raw_score):
    # 初始随机回答在1到4之间
    responses = np.random.randint(1, 5, 20)
    
    # 计算当前原始分数
    current_raw_score = sum([4 - responses[i-1] + 1 if i in REVERSE_ITEMS else responses[i-1] for i in range(1, 21)])
    
    # 调整回答以更接近目标分数
    attempts = 0
    while abs(current_raw_score - target_raw_score) > 1 and attempts < 100:
        # 随机选择一个问题
        q_idx = np.random.randint(0, 20)
        q_num = q_idx + 1
        
        # 当前回答的值
        old_val = responses[q_idx]
        new_val = np.random.randint(1, 5)
        
        # 如果新值与旧值相同则跳过
        if old_val == new_val:
            continue
            
        # 计算分数变化
        old_score = 4 - old_val + 1 if q_num in REVERSE_ITEMS else old_val
        new_score = 4 - new_val + 1 if q_num in REVERSE_ITEMS else new_val
        delta = new_score - old_score
        
        # 如果此变化使我们更接近目标，则接受它
        if abs((current_raw_score + delta) - target_raw_score) < abs(current_raw_score - target_raw_score):
            responses[q_idx] = new_val
            current_raw_score += delta
            
        attempts += 1
    
    return responses

# 从回答计算SAS得分
def calculate_sas_score(responses):
    # 计算原始分数
    raw_score = 0
    for i in range(20):
        if i+1 in REVERSE_ITEMS:
            # 反向评分：A(1)=4, B(2)=3, C(3)=2, D(4)=1
            raw_score += 5 - responses[i]
        else:
            # 正向评分：A(1)=1, B(2)=2, C(3)=3, D(4)=4
            raw_score += responses[i]
    
    # 转换为标准分数：原始分数 * 1.25，四舍五入到最接近的整数
    standard_score = round(raw_score * 1.25)
    
    return standard_score

# 根据要求生成数据集
def generate_and_save_datasets():
    datasets = {}
    
    # 遍历每个组和血压类型
    for group_name, bp_groups in SAS_STATS.items():
        for bp_group, timepoints in bp_groups.items():
            # 生成前测数据
            pre_data = generate_sas_data(
                mean_score=timepoints["前"]["mean"],
                std_dev=timepoints["前"]["std_dev"],
                n=NUM_PEOPLE_PER_SUBGROUP,
                group_name=group_name,
                bp_group=bp_group
            )
            
            # 生成后测数据
            post_data = generate_sas_data(
                mean_score=timepoints["后"]["mean"],
                std_dev=timepoints["后"]["std_dev"],
                n=NUM_PEOPLE_PER_SUBGROUP,
                group_name=group_name,
                bp_group=bp_group,
                is_post=True
            )
            
            # 将前测数据添加到相应组的前测数据集中
            pre_key = f"{group_name}跟踪前"
            if pre_key not in datasets:
                datasets[pre_key] = pre_data
            else:
                datasets[pre_key] = pd.concat([datasets[pre_key], pre_data])
            
            # 将后测数据添加到相应组的后测数据集中
            post_key = f"{group_name}跟踪后"
            if post_key not in datasets:
                datasets[post_key] = post_data
            else:
                datasets[post_key] = pd.concat([datasets[post_key], post_data])
    
    # 保存数据集到Excel文件
    for name, df in datasets.items():
        # 重新编号
        df['编号'] = range(1, len(df) + 1)
        
        filename = f"{name}.xlsx"
        df.to_excel(filename, index=False)
        print(f"生成并保存：{filename}")
    
    return datasets

# 创建折线图比较第二组高血压组跟踪前后的得分
def create_comparison_chart(datasets):
    pre_data = datasets["第二组跟踪前"]
    post_data = datasets["第二组跟踪后"]
    
    # 只选择高血压组的数据
    pre_data_hp = pre_data[pre_data["血压组"] == "高血压组"]
    
    # 按跟踪前得分排序
    pre_data_hp = pre_data_hp.sort_values("SAS得分", ascending=False)
    
    # 通过匹配姓名找到对应的跟踪后数据
    sorted_names = pre_data_hp["姓名"].tolist()
    post_data_hp = post_data[post_data["血压组"] == "高血压组"]
    
    post_data_sorted = [post_data_hp[post_data_hp["姓名"] == name]["SAS得分"].values[0] 
                       if name in post_data_hp["姓名"].values else None for name in sorted_names]
    
    # 创建折线图
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(sorted_names)), pre_data_hp["SAS得分"].tolist(), 'o-', label='跟踪前', color='red')
    plt.plot(range(len(sorted_names)), post_data_sorted, 's-', label='跟踪后', color='green')
    plt.title('第二组高血压患者跟踪前后SAS得分对比')
    plt.xlabel('患者')
    plt.ylabel('SAS得分')
    plt.xticks(range(len(sorted_names)), sorted_names, rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig('第二组高血压患者得分对比图.png')
    plt.show()
    print("图表已创建并保存为：第二组高血压患者得分对比图.png")

# 生成统计摘要以验证结果符合要求
def generate_statistics_report(datasets):
    print("\n===== 生成数据统计摘要 =====")
    for group in ["第一组", "第二组"]:
        print(f"\n{group}统计数据:")
        for time in ["跟踪前", "跟踪后"]:
            data = datasets[f"{group}{time}"]
            print(f"\n{time}:")
            
            # 按血压组分组统计
            for bp_group in ["正常高值血压组", "高血压组"]:
                group_data = data[data["血压组"] == bp_group]
                mean_score = group_data["SAS得分"].mean()
                std_score = group_data["SAS得分"].std()
                
                # 查找目标值比较
                target_mean = SAS_STATS[group][bp_group]["前" if time=="跟踪前" else "后"]["mean"]
                target_std = SAS_STATS[group][bp_group]["前" if time=="跟踪前" else "后"]["std_dev"]
                
                print(f"{bp_group}: {mean_score:.1f}±{std_score:.1f} (目标: {target_mean}±{target_std})")
    
    # 创建表格形式的报告并保存
    report_data = []
    for group in ["第一组", "第二组"]:
        for bp_group in ["正常高值血压组", "高血压组"]:
            pre_data = datasets[f"{group}跟踪前"][datasets[f"{group}跟踪前"]["血压组"] == bp_group]
            post_data = datasets[f"{group}跟踪后"][datasets[f"{group}跟踪后"]["血压组"] == bp_group]
            
            pre_mean = pre_data["SAS得分"].mean()
            pre_std = pre_data["SAS得分"].std()
            post_mean = post_data["SAS得分"].mean()
            post_std = post_data["SAS得分"].std()
            bp_control = SAS_STATS[group][bp_group]["前"]["bp_control_rate"]
            
            report_data.append({
                "组别": group,
                "血压组": bp_group,
                "SAS得分（前）": f"{pre_mean:.1f}±{pre_std:.1f}",
                "SAS得分（后）": f"{post_mean:.1f}±{post_std:.1f}",
                "血压控制率/%": bp_control
            })
    
    # 创建统计报告DataFrame并保存
    report_df = pd.DataFrame(report_data)
    report_df.to_excel("SAS情绪统计表.xlsx", index=False)
    print("\n统计报告已保存到：SAS情绪统计表.xlsx")

def main():
    print("开始生成SAS问卷数据...")
    datasets = generate_and_save_datasets()
    print("数据生成完成！")
    
    print("生成统计报告...")
    generate_statistics_report(datasets)
    
    print("开始生成对比图表...")
    create_comparison_chart(datasets)
    print("图表生成完成！")

if __name__ == "__main__":
    main()
