from collections import Counter
import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
def process_dataframe(df):
    """
    处理DataFrame的函数
    1. 做去空处理
    2. 若ask列的值为"无"则用title覆盖
    """
    original_rows = len(df)
    df_cleaned = df
    none_count_before = (df_cleaned['ask'] == "无").sum()
    mask = df_cleaned['ask'] == "无"
    df_cleaned.loc[mask, 'ask'] = df_cleaned.loc[mask, 'title']
    none_count_after = (df_cleaned['ask'] == "无").sum()
    
    print("=== 处理结果统计 ===")
    print(f"原始数据行数: {original_rows}")
    print(f"替换'无'值数量: {none_count_before}")
    print(f"替换后剩余'无'值数量: {none_count_after}")
    print(f"最终有效数据行数: {len(df_cleaned)}")
    
    return df_cleaned

df = pd.read_csv('肿瘤科5-10000.csv', encoding='GB18030')
df= process_dataframe(df)
department_counts = Counter(df['department'])
total_count = len(df)

print("科室分布统计分析：")
print(f"总记录数：{total_count}")
print("\n前二十个占比最多的科室类别：")
print("-" * 40)

results = []
for department, count in department_counts.most_common():
    percentage = (count / total_count) * 100
    results.append((department, count, percentage))


for i, (department, count, percentage) in enumerate(results[:50], 1):
    print(f"{i:2d}. {department:<6} - 出现次数：{count:2d} - 占比：{percentage:6.2f}%")

# 设置抽样阈值
threshold = 1000
balanced_dfs = []

# 对每个类目进行处理
for department, count in department_counts.items():
    department_data = df[df['department'] == department]
    
    if count > threshold:
        sampled_data = department_data.sample(n=threshold, random_state=42)  # random_state确保结果可复现
        balanced_dfs.append(sampled_data)
    else:
        balanced_dfs.append(department_data)


balanced_df = pd.concat(balanced_dfs, ignore_index=True)


# 输出处理后的统计信息
print("\n处理后的数据分布统计：")
print(f"总记录数：{len(balanced_df)}")
print("\n各科室类别分布：")
balanced_counts = Counter(balanced_df['department'])
for department, count in balanced_counts.most_common():
    percentage = (count / len(balanced_df)) * 100
#     print(f"{department}: 记录数={count}, 占比={percentage:.2f}%")

formatted_data = balanced_df[['ask', 'answer']].rename(
    columns={'ask': 'input', 'answer': 'output'}
)


formatted_data['instruction'] = "现在你是一个肿瘤学科医生，请根据患者的问题给出实际的医疗建议："
formatted_data = formatted_data[['instruction', 'input', 'output']]

train_df, temp_df = train_test_split(formatted_data, test_size=0.2, random_state=42)

val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

output_dir = 'final_data'
os.makedirs(output_dir, exist_ok=True)

# 保存训练集
train_path = os.path.join(output_dir, 'train.json')
with open(train_path, 'w', encoding='utf-8') as f:
    json.dump(train_df.to_dict('records'), f, ensure_ascii=False, indent=4)

# 保存验证集
val_path = os.path.join(output_dir, 'validation.json')
with open(val_path, 'w', encoding='utf-8') as f:
    json.dump(val_df.to_dict('records'), f, ensure_ascii=False, indent=4)

# 保存测试集
test_path = os.path.join(output_dir, 'test.json')
with open(test_path, 'w', encoding='utf-8') as f:
    json.dump(test_df.to_dict('records'), f, ensure_ascii=False, indent=4)

# 输出划分结果
print(f"数据划分完成，已保存至 {output_dir} 文件夹")
print(f"训练集: {len(train_df)} 条数据 ({len(train_df)/len(formatted_data)*100:.2f}%)")
print(f"验证集: {len(val_df)} 条数据 ({len(val_df)/len(formatted_data)*100:.2f}%)")
print(f"测试集: {len(test_df)} 条数据 ({len(test_df)/len(formatted_data)*100:.2f}%)")

