import pandas as pd
import numpy as np

def verify_data():
    # 读取生成的Excel文件
    df1 = pd.read_excel(r"d:\Python\Class3\第一组.xlsx")
    df2 = pd.read_excel(r"d:\Python\Class3\第二组.xlsx")
    
    # 验证第一组
    print("第一组数据验证:")
    print(f"总人数: {len(df1)}")
    
    # 年龄分布
    age_mean = df1['年龄'].mean()
    age_std = df1['年龄'].std()
    print(f"年龄分布: {age_mean:.2f}±{age_std:.2f} (目标: 67.6±{np.sqrt(4.28):.2f})")
    
    # 血压级别分布
    high_bp = df1[df1['血压级别'].isin([1, 2, 3])]
    normal_high = df1[df1['血压级别'] == 4]
    
    print(f"高血压组人数: {len(high_bp)} (目标: 34)")
    print(f"- 1级高血压: {len(df1[df1['血压级别'] == 1])} (目标: 24)")
    print(f"- 2级高血压: {len(df1[df1['血压级别'] == 2])} (目标: 9)")
    print(f"- 3级高血压: {len(df1[df1['血压级别'] == 3])} (目标: 1)")
    print(f"血压正常高值组人数: {len(normal_high)} (目标: 15)")
    
    # 验证第二组
    print("\n第二组数据验证:")
    print(f"总人数: {len(df2)}")
    
    # 年龄分布
    age_mean = df2['年龄'].mean()
    age_std = df2['年龄'].std()
    print(f"年龄分布: {age_mean:.2f}±{age_std:.2f} (目标: 66.36±{np.sqrt(3.03):.2f})")
    
    # 血压级别分布
    high_bp = df2[df2['血压级别'].isin([1, 2, 3])]
    normal_high = df2[df2['血压级别'] == 4]
    
    print(f"高血压组人数: {len(high_bp)} (目标: 33)")
    print(f"- 1级高血压: {len(df2[df2['血压级别'] == 1])} (目标: 23)")
    print(f"- 2级高血压: {len(df2[df2['血压级别'] == 2])} (目标: 8)")
    print(f"- 3级高血压: {len(df2[df2['血压级别'] == 3])} (目标: 2)")
    print(f"血压正常高值组人数: {len(normal_high)} (目标: 16)")

if __name__ == "__main__":
    verify_data()
