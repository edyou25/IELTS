import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np
import os
from collections import Counter

def read_scores_csv(filename):
    """读取分数CSV文件"""
    scores_dict = {}
    try:
        df = pd.read_csv(filename, encoding='utf-8')
        
        # 假设CSV文件有列：编号, 听力, 阅读
        test_ids = df['ID'].tolist()
        listening_scores = df['Listening'].tolist()
        reading_scores = df['Reading'].tolist()
        
        scores_dict = {
            'test_ids': test_ids,
            'listening': listening_scores,
            'reading': reading_scores
        }
        
        print(f"✅ Successfully loaded {len(test_ids)} records from {filename}")
        return scores_dict
        
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return None

def calculate_mode(scores):
    """计算众数"""
    valid_scores = [s for s in scores if s is not None and not pd.isna(s)]
    if not valid_scores:
        return None
    
    # 使用Counter统计频率
    counter = Counter(valid_scores)
    max_count = max(counter.values())
    modes = [k for k, v in counter.items() if v == max_count]
    
    # 如果所有值都只出现一次，返回None
    if max_count == 1 and len(modes) == len(valid_scores):
        return None
    
    return modes[0] if len(modes) == 1 else modes

def main():
    # 设置文件路径
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv")
    csv_file = os.path.join(input_dir, 'scores.csv')
    
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return
    
    # 读取CSV数据
    csv_dict = read_scores_csv(csv_file)
    
    if csv_dict is None:
        print("❌ Failed to load data from CSV")
        return
    
    # 提取数据
    test_ids = csv_dict['test_ids']
    listening_scores = csv_dict['listening']
    reading_scores = csv_dict['reading']
    
    # 计算统计数据
    def calculate_stats(scores, name):
        # 移除None值和NaN值
        valid_scores = [s for s in scores if s is not None and not pd.isna(s)]
        
        if not valid_scores:
            return f"No valid {name} scores"
        
        mode_value = calculate_mode(scores)
        
        stats = {
            'count': len(valid_scores),
            'mean': np.mean(valid_scores),
            'median': np.median(valid_scores),
            'mode': mode_value,
            'std': np.std(valid_scores),
            'min': np.min(valid_scores),
            'max': np.max(valid_scores),
            'range': np.max(valid_scores) - np.min(valid_scores)
        }
        
        return stats
    
    # 计算统计信息
    listening_stats = calculate_stats(listening_scores, "Listening")
    reading_stats = calculate_stats(reading_scores, "Reading")
    
    # 打印统计信息
    print("\n" + "="*60)
    print("📊 IELTS SCORES ANALYSIS")
    print("="*60)
    
    if isinstance(listening_stats, dict):
        print("\n🎧 LISTENING STATISTICS:")
        print(f"   📈 Count: {listening_stats['count']} tests")
        print(f"   📊 Mean: {listening_stats['mean']:.2f}")
        print(f"   📊 Median: {listening_stats['median']:.2f}")
        print(f"   📊 Mode: {listening_stats['mode']}")
        print(f"   📊 Std Dev: {listening_stats['std']:.2f}")
        print(f"   📊 Min: {listening_stats['min']:.1f}")
        print(f"   📊 Max: {listening_stats['max']:.1f}")
        print(f"   📊 Range: {listening_stats['range']:.1f}")
    
    if isinstance(reading_stats, dict):
        print("\n📖 READING STATISTICS:")
        print(f"   📈 Count: {reading_stats['count']} tests")
        print(f"   📊 Mean: {reading_stats['mean']:.2f}")
        print(f"   📊 Median: {reading_stats['median']:.2f}")
        print(f"   📊 Mode: {reading_stats['mode']}")
        print(f"   📊 Std Dev: {reading_stats['std']:.2f}")
        print(f"   📊 Min: {reading_stats['min']:.1f}")
        print(f"   📊 Max: {reading_stats['max']:.1f}")
        print(f"   📊 Range: {reading_stats['range']:.1f}")
    
    # 创建图表
    fig = go.Figure()
    
    # 添加听力分数线
    fig.add_trace(go.Scatter(
        x=test_ids, 
        y=listening_scores, 
        mode='lines+markers', 
        name='Listening',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))
    
    # 添加阅读分数线
    fig.add_trace(go.Scatter(
        x=test_ids, 
        y=reading_scores, 
        mode='lines+markers', 
        name='Reading',
        line=dict(color='red', width=2),
        marker=dict(size=8)
    ))
    
    # 添加统计线条
    x_range = [test_ids[0], test_ids[-1]]
    
    # 听力统计线
    if isinstance(listening_stats, dict):
        # 平均数
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['mean'], listening_stats['mean']],
            mode='lines',
            name=f'Listening Mean ({listening_stats["mean"]:.2f})',
            line=dict(color='lightblue', width=2, dash='solid'),
            opacity=0.7
        ))
        
        # 中位数
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['median'], listening_stats['median']],
            mode='lines',
            name=f'Listening Median ({listening_stats["median"]:.2f})',
            line=dict(color='blue', width=2, dash='dash'),
            opacity=0.7
        ))
        
        # 众数（如果存在）
        if listening_stats['mode'] is not None:
            mode_val = listening_stats['mode'] if isinstance(listening_stats['mode'], (int, float)) else listening_stats['mode'][0]
            fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'Listening Mode ({mode_val})',
                line=dict(color='darkblue', width=2, dash='dot'),
                opacity=0.7
            ))
    
    # 阅读统计线
    if isinstance(reading_stats, dict):
        # 平均数
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['mean'], reading_stats['mean']],
            mode='lines',
            name=f'Reading Mean ({reading_stats["mean"]:.2f})',
            line=dict(color='lightcoral', width=2, dash='solid'),
            opacity=0.7
        ))
        
        # 中位数
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['median'], reading_stats['median']],
            mode='lines',
            name=f'Reading Median ({reading_stats["median"]:.2f})',
            line=dict(color='red', width=2, dash='dash'),
            opacity=0.7
        ))
        
        # 众数（如果存在）
        if reading_stats['mode'] is not None:
            mode_val = reading_stats['mode'] if isinstance(reading_stats['mode'], (int, float)) else reading_stats['mode'][0]
            fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'Reading Mode ({mode_val})',
                line=dict(color='darkred', width=2, dash='dot'),
                opacity=0.7
            ))
    
    # 添加6.5分数线（IELTS重要分界线）
    fig.add_trace(go.Scatter(
        x=x_range,
        y=[6.5, 6.5],
        mode='lines',
        name='Target Line (6.5)',
        line=dict(color='green', width=3, dash='dashdot'),
        opacity=0.8
    ))
    
    # 更新布局
    fig.update_layout(
        title='IELTS Scores Analysis with Statistical Lines',
        xaxis_title='Test ID',
        yaxis_title='Score',
        legend_title='Legend',
        yaxis=dict(range=[0, 9.5]),  # IELTS分数范围
        width=1200,
        height=700,
        template='plotly_white',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    # 添加注释
    fig.add_annotation(
        x=test_ids[-1],
        y=6.5,
        text="Target Score",
        showarrow=True,
        arrowhead=2,
        arrowcolor="green",
        font=dict(color="green", size=12)
    )
    
    # # 保存文件
    # output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # # 保存为HTML
    # html_path = os.path.join(output_dir, 'ielts_scores_analysis.html')
    # fig.write_html(html_path)
    # print(f"\n✅ Plot saved as HTML: {html_path}")
    
    # # 保存为JSON
    # json_path = os.path.join(output_dir, 'ielts_scores_analysis.json')
    # fig.write_json(json_path)
    # print(f"✅ Plot saved as JSON: {json_path}")
    
    # # 尝试保存为PNG
    # try:
    #     png_path = os.path.join(output_dir, 'ielts_scores_analysis.png')
    #     fig.write_image(png_path, width=1200, height=700)
    #     print(f"✅ Plot saved as PNG: {png_path}")
    # except Exception as e:
    #     print(f"⚠️ PNG export failed: {e}")
    #     print("💡 To export PNG, install kaleido: pip install kaleido")
    
    # 在浏览器中显示
    fig.show()
    
    print("="*60)

if __name__ == "__main__":
    main()