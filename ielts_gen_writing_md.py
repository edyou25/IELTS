import re
import os

mode = "改进"

def extract_improved_essays(file_path):
    """从markdown文件中提取Task1和Task2的改进后文章"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return
    
    # 提取Task 1改进后的句子
    task1_improved = []
    task2_improved = []
    
    # 分割内容为Task 1和Task 2部分
    parts = content.split('### Task 2')
    task1_part = parts[0] if len(parts) > 0 else ""
    task2_part = parts[1] if len(parts) > 1 else ""
    
    # 提取Task 1的改进句子
    print("TASK 1")
    
    # 找到所有"改进："后的内容
    if mode == "改进":
        task1_improvements = re.findall(r'改进：([^改进]+?)(?=原句：|改进点：|### Task 2|$)', task1_part, re.DOTALL)
    else :
        # 原句
        task1_improvements = re.findall(r'原句：([^改进]+?)(?=改进：|改进点：|### Task 2|$)', task1_part, re.DOTALL)
    task1_essay = []
    for improvement in task1_improvements:
        sentence = improvement.strip()
        if sentence and not sentence.startswith('改进点：'):
            task1_essay.append(sentence)
    
    # 组合Task 1文章
    if task1_essay:
        print("\n".join(task1_essay))

    print("TASK 2")
    
    # 提取Task 2的改进句子
    if mode == "改进":
        task2_improvements = re.findall(r'改进：([^改进]+?)(?=原句：|改进点：|$)', task2_part, re.DOTALL)
    else:
        # 原句
        task2_improvements = re.findall(r'原句：([^改进]+?)(?=改进：|改进点：|$)', task2_part, re.DOTALL)
    
    task2_essay = []
    for improvement in task2_improvements:
        sentence = improvement.strip()
        if sentence and not sentence.startswith('改进点：') and not sentence.startswith('（'):
            task2_essay.append(sentence)
    
    # 组合Task 2文章
    if task2_essay:
        print("\n".join(task2_essay))

def main():
    filename = "18-1.md"
    file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")
    file_path = os.path.join(file_dir, filename)
    extract_improved_essays(file_path)

if __name__ == "__main__":
    main()
