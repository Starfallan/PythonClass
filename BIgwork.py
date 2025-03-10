import random
import numpy as np
import pandas as pd
import os

# 生成中文姓名的函数
def generate_chinese_name():
    surnames = ['李', '王', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', 
                '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
                '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧']
    
    names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军',
            '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞',
            '平', '刚', '桂英', '文', '辉', '建华', '玲', '红', '健', '玉兰',
            '欣', '俊', '楠', '阳', '红梅', '振', '建', '亮', '雪', '丹']
    
    return random.choice(surnames) + random.choice(names)

# 生成Excel文件的函数
def generate_excel_files():
    # 创建保存目录
    save_path = r"d:\Python\Class3"
    os.makedirs(save_path, exist_ok=True)
    
    # 第一组数据生成
    group1_data = []
    # 生成高血压组数据 (34人)
    # 1级高血压 (24人)
    for i in range(1, 25):
        group1_data.append({
            '编号': f'G1-H1-{i:02d}',
            '姓名': generate_chinese_name(),
            '性别': random.choice(['男', '女']),
            '年龄': int(np.random.normal(67.6, np.sqrt(4.28))),
            '血压级别': 1
        })
    
    # 2级高血压 (9人)
    for i in range(1, 10):
        group1_data.append({
            '编号': f'G1-H2-{i:02d}',
            '姓名': generate_chinese_name(),
            '性别': random.choice(['男', '女']),
            '年龄': int(np.random.normal(67.6, np.sqrt(4.28))),
            '血压级别': 2
        })
    
    # 3级高血压 (1人)
    group1_data.append({
        '编号': 'G1-H3-01',
        '姓名': generate_chinese_name(),
        '性别': random.choice(['男', '女']),
        '年龄': int(np.random.normal(67.6, np.sqrt(4.28))),
        '血压级别': 3
    })
    
    # 血压正常高值组 (15人)
    for i in range(1, 16):
        group1_data.append({
            '编号': f'G1-N-{i:02d}',
            '姓名': generate_chinese_name(),
            '性别': random.choice(['男', '女']),
            '年龄': int(np.random.normal(67.6, np.sqrt(4.28))),
            '血压级别': 4  # 4表示正常高值
        })
    
    # 第二组数据生成
    group2_data = []
    # 生成高血压组数据 (33人)
    # 1级高血压 (23人)
    for i in range(1, 24):
        group2_data.append({
            '编号': f'G2-H1-{i:02d}',
            '姓名': generate_chinese_name(),
            '性别': random.choice(['男', '女']),
            '年龄': int(np.random.normal(66.36, np.sqrt(3.03))),
            '血压级别': 1
        })
    
    # 2级高血压 (8人)
    for i in range(1, 9):
        group2_data.append({
            '编号': f'G2-H2-{i:02d}',
            '姓名': generate_chinese_name(),
            '性别': random.choice(['男', '女']),
            '年龄': int(np.random.normal(66.36, np.sqrt(3.03))),
            '血压级别': 2
        })
    
    # 3级高血压 (2人)
    for i in range(1, 3):
        group2_data.append({
            '编号': f'G2-H3-{i:02d}',
            '姓名': generate_chinese_name(),
            '性别': random.choice(['男', '女']),
            '年龄': int(np.random.normal(66.36, np.sqrt(3.03))),
            '血压级别': 3
        })
    
    # 血压正常高值组 (16人)
    for i in range(1, 17):
        group2_data.append({
            '编号': f'G2-N-{i:02d}',
            '姓名': generate_chinese_name(),
            '性别': random.choice(['男', '女']),
            '年龄': int(np.random.normal(66.36, np.sqrt(3.03))),
            '血压级别': 4  # 4表示正常高值
        })
    
    # 校正年龄范围为60~75
    for person in group1_data + group2_data:
        while person['年龄'] < 60 or person['年龄'] > 75:
            if person['编号'].startswith('G1'):
                person['年龄'] = int(np.random.normal(67.6, np.sqrt(4.28)))
            else:
                person['年龄'] = int(np.random.normal(66.36, np.sqrt(3.03)))
    
    # 转换为DataFrame并保存为Excel
    df1 = pd.DataFrame(group1_data)
    df2 = pd.DataFrame(group2_data)
    
    # 保存Excel文件
    df1.to_excel(os.path.join(save_path, "第一组.xlsx"), index=False)
    df2.to_excel(os.path.join(save_path, "第二组.xlsx"), index=False)
    
    print(f"Excel文件已成功生成，保存在: {save_path}")
    print(f"第一组: {len(group1_data)}人，第二组: {len(group2_data)}人")

# 执行数据生成函数
if __name__ == "__main__":
    generate_excel_files()

