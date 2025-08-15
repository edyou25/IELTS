import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import numpy as np
import os
from collections import Counter

def read_scores_csv(filename):
    """读取分数CSV文件"""
    scores_dict = {}
    try:
        df = pd.read_csv(filename, encoding='utf-8')
        
        # 假设CSV文件有列：编号, 听力, 阅读, 类型
        test_ids = df['ID'].tolist()
        listening_scores = df['Listening'].tolist()
        reading_scores = df['Reading'].tolist()
        score_types = df['Type'].tolist() if 'Type' in df.columns else ['practice'] * len(test_ids)
        
        scores_dict = {
            'test_ids': test_ids,
            'listening': listening_scores,
            'reading': reading_scores,
            'types': score_types
        }
        
        # 统计不同类型的分数
        practice_count = score_types.count('practice')
        real_count = score_types.count('real_exam')
        
        print(f"✅ Successfully loaded {len(test_ids)} records from {filename}")
        print(f"   📝 Practice tests: {practice_count}")
        print(f"   🎯 Real exams: {real_count}")
        return scores_dict
        
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return None

def linear_fit_and_predict(x_data, y_data, prediction_steps=3):
    """
    线性拟合数据并进行预测
    x_data: x轴数据
    y_data: y轴数据  
    prediction_steps: 预测未来几个点
    """
    # 移除None值和NaN值
    valid_indices = [i for i, y in enumerate(y_data) if y is not None and not pd.isna(y)]
    if len(valid_indices) < 2:  # 至少需要2个点进行线性拟合
        return None, None, None
    
    x_valid = [x_data[i] for i in valid_indices]
    y_valid = [y_data[i] for i in valid_indices]
    
    # 转换为numpy数组
    x_array = np.array(x_valid)
    y_array = np.array(y_valid)
    
    # 线性拟合 (y = ax + b)
    coeffs = np.polyfit(x_array, y_array, 1)  # 1次多项式 = 线性
    slope, intercept = coeffs
    
    # 生成拟合线的x值
    x_fit = np.linspace(x_array.min(), x_array.max(), 100)
    y_fit = slope * x_fit + intercept
    
    # 预测未来的点
    x_future = np.arange(x_array.max() + 1, x_array.max() + 1 + prediction_steps)
    x_future = np.arange(x_array.max(), x_array.max() + prediction_steps*.1, 0.1)

    y_future = slope * x_future + intercept
    
    # 确保预测值在合理范围内（0-9分）
    y_future = np.clip(y_future, 0, 9)
    
    # 计算拟合质量 (R²)
    y_pred = slope * x_array + intercept
    ss_res = np.sum((y_array - y_pred) ** 2)
    ss_tot = np.sum((y_array - np.mean(y_array)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    x_future = np.arange(x_array.max() + 1, x_array.max() + 1 + prediction_steps)
    
    return (x_fit, y_fit), (x_future, y_future), {'slope': slope, 'intercept': intercept, 'r_squared': r_squared}

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
    score_types = csv_dict['types']
    
    # 分离练习分数和真实考试分数
    practice_indices = [i for i, t in enumerate(score_types) if t == 'practice']
    real_indices = [i for i, t in enumerate(score_types) if t == 'real_exam']
    
    practice_ids = [test_ids[i] for i in practice_indices]
    practice_listening = [listening_scores[i] for i in practice_indices]
    practice_reading = [reading_scores[i] for i in practice_indices]
    
    real_ids = [test_ids[i] for i in real_indices] if real_indices else []
    real_listening = [listening_scores[i] for i in real_indices] if real_indices else []
    real_reading = [reading_scores[i] for i in real_indices] if real_indices else []
    
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
    
    # 计算统计信息（仅基于练习分数）
    practice_listening_stats = calculate_stats(practice_listening, "Practice Listening")
    practice_reading_stats = calculate_stats(practice_reading, "Practice Reading")
    
    # 计算所有分数的统计（包括真实考试）
    listening_stats = calculate_stats(listening_scores, "All Listening")
    reading_stats = calculate_stats(reading_scores, "All Reading")
    
    # 打印统计信息
    print("\n" + "="*60)
    print("📊 IELTS SCORES ANALYSIS")
    print("="*60)
    
    # 打印真实考试成绩
    if real_indices:
        print("\n🎯 REAL EXAM RESULTS:")
        for i, idx in enumerate(real_indices):
            print(f"   Test {test_ids[idx]}: Listening {listening_scores[idx]}, Reading {reading_scores[idx]}")
    
    print(f"\n📊 PRACTICE STATISTICS (Based on {len(practice_indices)} practice tests):")
    
    if isinstance(practice_listening_stats, dict):
        print("\n🎧 LISTENING STATISTICS:")
        print(f"   📈 Count: {practice_listening_stats['count']} tests")
        print(f"   📊 Mean: {practice_listening_stats['mean']:.2f}")
        print(f"   📊 Median: {practice_listening_stats['median']:.2f}")
        print(f"   📊 Mode: {practice_listening_stats['mode']}")
        print(f"   📊 Std Dev: {practice_listening_stats['std']:.2f}")
        print(f"   📊 Min: {practice_listening_stats['min']:.1f}")
        print(f"   📊 Max: {practice_listening_stats['max']:.1f}")
        print(f"   📊 Range: {practice_listening_stats['range']:.1f}")
    
    if isinstance(practice_reading_stats, dict):
        print("\n📖 READING STATISTICS:")
        print(f"   📈 Count: {practice_reading_stats['count']} tests")
        print(f"   📊 Mean: {practice_reading_stats['mean']:.2f}")
        print(f"   📊 Median: {practice_reading_stats['median']:.2f}")
        print(f"   📊 Mode: {practice_reading_stats['mode']}")
        print(f"   📊 Std Dev: {practice_reading_stats['std']:.2f}")
        print(f"   📊 Min: {practice_reading_stats['min']:.1f}")
        print(f"   📊 Max: {practice_reading_stats['max']:.1f}")
        print(f"   📊 Range: {practice_reading_stats['range']:.1f}")
    
    # 计算线性拟合和预测（基于练习分数）
    listening_fit_data = linear_fit_and_predict(practice_ids, practice_listening, prediction_steps=3)
    reading_fit_data = linear_fit_and_predict(practice_ids, practice_reading, prediction_steps=3)
    
    # 打印拟合信息
    if listening_fit_data[2] is not None:
        fit_info = listening_fit_data[2]
        print(f"\n🎧 LISTENING LINEAR FIT:")
        print(f"   📈 Slope: {fit_info['slope']:.3f} points/test")
        print(f"   📊 R² (fit quality): {fit_info['r_squared']:.3f}")
        trend = "improving" if fit_info['slope'] > 0 else "declining" if fit_info['slope'] < 0 else "stable"
        print(f"   📈 Trend: {trend}")
    
    if reading_fit_data[2] is not None:
        fit_info = reading_fit_data[2]
        print(f"\n📖 READING LINEAR FIT:")
        print(f"   📈 Slope: {fit_info['slope']:.3f} points/test")
        print(f"   📊 R² (fit quality): {fit_info['r_squared']:.3f}")
        trend = "improving" if fit_info['slope'] > 0 else "declining" if fit_info['slope'] < 0 else "stable"
        print(f"   📈 Trend: {trend}")

    # 创建subplot布局：2行2列，第一行跨2列，第二行2列
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Combined Analysis', '🎧 Listening Analysis', '📖 Reading Analysis'),
        specs=[[{"colspan": 2}, None],
               [{"colspan": 1}, {"colspan": 1}]],
        horizontal_spacing=0.15,
        vertical_spacing=0.20
    )
    
    # 添加统计线条的x范围
    x_range = [test_ids[0], test_ids[-1]]
    
    # ============= 第一行：综合分析（跨3列） =============
    # 添加练习听力分数线
    if practice_indices:
        fig.add_trace(go.Scatter(
            x=practice_ids, 
            y=practice_listening, 
            mode='lines+markers', 
            name='Listening (Practice)',
            line=dict(color='blue', width=3),
            marker=dict(size=8, color='blue'),
            showlegend=True,
            legendgroup="main"
        ), row=1, col=1)
    
    # 添加练习阅读分数线
    if practice_indices:
        fig.add_trace(go.Scatter(
            x=practice_ids, 
            y=practice_reading, 
            mode='lines+markers', 
            name='Reading (Practice)',
            line=dict(color='red', width=3),
            marker=dict(size=8, color='red'),
            showlegend=True,
            legendgroup="main"
        ), row=1, col=1)
    
    # 添加真实考试听力分数
    if real_indices:
        fig.add_trace(go.Scatter(
            x=real_ids, 
            y=real_listening, 
            mode='markers', 
            name='Listening (Real Exam)',
            marker=dict(size=15, color='blue', symbol='star', line=dict(width=2, color='darkblue')),
            showlegend=True,
            legendgroup="main"
        ), row=1, col=1)
    
    # 添加真实考试阅读分数
    if real_indices:
        fig.add_trace(go.Scatter(
            x=real_ids, 
            y=real_reading, 
            mode='markers', 
            name='Reading (Real Exam)',
            marker=dict(size=15, color='red', symbol='star', line=dict(width=2, color='darkred')),
            showlegend=True,
            legendgroup="main"
        ), row=1, col=1)
    
    # 听力统计线（综合图，默认隐藏）
    if isinstance(listening_stats, dict):
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['mean'], listening_stats['mean']],
            mode='lines',
            name=f'L-Mean ({listening_stats["mean"]:.2f})',
            line=dict(color='lightblue', width=2, dash='solid'),
            opacity=0.7,
            showlegend=True,
            visible='legendonly',  # 默认隐藏
            legendgroup="main"
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['median'], listening_stats['median']],
            mode='lines',
            name=f'L-Median ({listening_stats["median"]:.2f})',
            line=dict(color='blue', width=2, dash='dash'),
            opacity=0.7,
            showlegend=True,
            visible='legendonly',  # 默认隐藏
            legendgroup="main"
        ), row=1, col=1)
        
        if listening_stats['mode'] is not None:
            mode_val = listening_stats['mode'] if isinstance(listening_stats['mode'], (int, float)) else listening_stats['mode'][0]
            fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'L-Mode ({mode_val})',
                line=dict(color='darkblue', width=2, dash='dot'),
                opacity=0.7,
                showlegend=True,
                visible='legendonly',  # 默认隐藏
                legendgroup="main"
            ), row=1, col=1)
    
    # 阅读统计线（综合图，默认隐藏）
    if isinstance(reading_stats, dict):
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['mean'], reading_stats['mean']],
            mode='lines',
            name=f'R-Mean ({reading_stats["mean"]:.2f})',
            line=dict(color='lightcoral', width=2, dash='solid'),
            opacity=0.7,
            showlegend=True,
            visible='legendonly',  # 默认隐藏
            legendgroup="main"
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['median'], reading_stats['median']],
            mode='lines',
            name=f'R-Median ({reading_stats["median"]:.2f})',
            line=dict(color='red', width=2, dash='dash'),
            opacity=0.7,
            showlegend=True,
            visible='legendonly',  # 默认隐藏
            legendgroup="main"
        ), row=1, col=1)
        
        if reading_stats['mode'] is not None:
            mode_val = reading_stats['mode'] if isinstance(reading_stats['mode'], (int, float)) else reading_stats['mode'][0]
            fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'R-Mode ({mode_val})',
                line=dict(color='darkred', width=2, dash='dot'),
                opacity=0.7,
                showlegend=True,
                visible='legendonly',  # 默认隐藏
                legendgroup="main"
            ), row=1, col=1)
    
    # 目标线（综合图）
    fig.add_trace(go.Scatter(
        x=x_range,
        y=[6.5, 6.5],
        mode='lines',
        name='Target (6.5)',
        line=dict(color='green', width=3, dash='dashdot'),
        opacity=0.8,
        showlegend=True,
        legendgroup="main"
    ), row=1, col=1)
    
    # 添加线性拟合线（综合图，默认隐藏）
    if listening_fit_data[0] is not None:
        fit_x, fit_y = listening_fit_data[0]
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=fit_y,
            mode='lines',
            name=f'L-Trend (R²={listening_fit_data[2]["r_squared"]:.3f})',
            line=dict(color='darkblue', width=2, dash='longdash'),
            opacity=0.6,
            showlegend=True,
            visible='legendonly',  # 默认隐藏
            legendgroup="main"
        ), row=1, col=1)
        
        # 添加听力预测点
        if listening_fit_data[1] is not None:
            future_x, future_y = listening_fit_data[1]
            fig.add_trace(go.Scatter(
                x=future_x,
                y=future_y,
                mode='markers',
                name='L-Prediction',
                marker=dict(color='blue', size=10, symbol='diamond'),
                showlegend=True,
                visible='legendonly',  # 默认隐藏
                legendgroup="main"
            ), row=1, col=1)
    
    if reading_fit_data[0] is not None:
        fit_x, fit_y = reading_fit_data[0]
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=fit_y,
            mode='lines',
            name=f'R-Trend (R²={reading_fit_data[2]["r_squared"]:.3f})',
            line=dict(color='darkred', width=2, dash='longdash'),
            opacity=0.6,
            showlegend=True,
            visible='legendonly',  # 默认隐藏
            legendgroup="main"
        ), row=1, col=1)
        
        # 添加阅读预测点
        if reading_fit_data[1] is not None:
            future_x, future_y = reading_fit_data[1]
            fig.add_trace(go.Scatter(
                x=future_x,
                y=future_y,
                mode='markers',
                name='R-Prediction',
                marker=dict(color='red', size=10, symbol='diamond'),
                showlegend=True,
                visible='legendonly',  # 默认隐藏
                legendgroup="main"
            ), row=1, col=1)

    # ============= 第二行第一列：听力详细分析 =============
    # 练习听力分数线
    if practice_indices:
        fig.add_trace(go.Scatter(
            x=practice_ids, 
            y=practice_listening, 
            mode='lines+markers', 
            name='Practice Scores',
            line=dict(color='blue', width=3),
            marker=dict(size=8, color='blue'),
            showlegend=True,
            legendgroup="listening"
        ), row=2, col=1)
    
    # 真实考试听力分数
    if real_indices:
        fig.add_trace(go.Scatter(
            x=real_ids, 
            y=real_listening, 
            mode='markers', 
            name='Real Exam',
            marker=dict(size=15, color='gold', symbol='star', line=dict(width=2, color='darkblue')),
            showlegend=True,
            legendgroup="listening"
        ), row=2, col=1)
    
    # 听力统计线（默认显示）
    if isinstance(listening_stats, dict):
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['mean'], listening_stats['mean']],
            mode='lines',
            name=f'Mean ({listening_stats["mean"]:.2f})',
            line=dict(color='lightblue', width=2, dash='solid'),
            opacity=0.8,
            showlegend=True,
            legendgroup="listening"
        ), row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['median'], listening_stats['median']],
            mode='lines',
            name=f'Median ({listening_stats["median"]:.2f})',
            line=dict(color='darkblue', width=2, dash='dash'),
            opacity=0.8,
            showlegend=True,
            legendgroup="listening"
        ), row=2, col=1)
        
        if listening_stats['mode'] is not None:
            mode_val = listening_stats['mode'] if isinstance(listening_stats['mode'], (int, float)) else listening_stats['mode'][0]
            fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'Mode ({mode_val})',
                line=dict(color='navy', width=2, dash='dot'),
                opacity=0.8,
                showlegend=True,
                legendgroup="listening"
            ), row=2, col=1)
    
    # 目标线（听力图）
    fig.add_trace(go.Scatter(
        x=x_range,
        y=[6.5, 6.5],
        mode='lines',
        name='Target (6.5)',
        line=dict(color='green', width=3, dash='dashdot'),
        opacity=0.9,
        showlegend=True,
        legendgroup="listening"
    ), row=2, col=1)
    
    # 添加听力拟合线和预测
    if listening_fit_data[0] is not None:
        fit_x, fit_y = listening_fit_data[0]
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=fit_y,
            mode='lines',
            name=f'Trend Fit (R²={listening_fit_data[2]["r_squared"]:.3f})',
            line=dict(color='darkblue', width=2, dash='longdash'),
            opacity=0.8,
            showlegend=True,
            legendgroup="listening"
        ), row=2, col=1)
        
        # 添加预测点和连接线
        if listening_fit_data[1] is not None:
            future_x, future_y = listening_fit_data[1]
            fig.add_trace(go.Scatter(
                x=future_x,
                y=future_y,
                mode='markers+lines',
                name='Prediction',
                line=dict(color='purple', width=2, dash='dot'),
                marker=dict(color='purple', size=12, symbol='diamond'),
                showlegend=True,
                legendgroup="listening"
            ), row=2, col=1)
            
            # 添加预测值注释
            for i, (px, py) in enumerate(zip(future_x, future_y)):
                fig.add_annotation(
                    x=px, y=py + 0.3,
                    text=f"{py:.1f}",
                    showarrow=False,
                    font=dict(color="purple", size=10),
                    row=2, col=1
                )

    # ============= 第二行第二列：阅读详细分析 =============
    # 练习阅读分数线
    if practice_indices:
        fig.add_trace(go.Scatter(
            x=practice_ids, 
            y=practice_reading, 
            mode='lines+markers', 
            name='Practice Scores',
            line=dict(color='red', width=3),
            marker=dict(size=8, color='red'),
            showlegend=True,
            legendgroup="reading"
        ), row=2, col=2)
    
    # 真实考试阅读分数
    if real_indices:
        fig.add_trace(go.Scatter(
            x=real_ids, 
            y=real_reading, 
            mode='markers', 
            name='Real Exam',
            marker=dict(size=15, color='gold', symbol='star', line=dict(width=2, color='darkred')),
            showlegend=True,
            legendgroup="reading"
        ), row=2, col=2)
    
    # 阅读统计线（默认显示）
    if isinstance(reading_stats, dict):
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['mean'], reading_stats['mean']],
            mode='lines',
            name=f'Mean ({reading_stats["mean"]:.2f})',
            line=dict(color='lightcoral', width=2, dash='solid'),
            opacity=0.8,
            showlegend=True,
            legendgroup="reading"
        ), row=2, col=2)
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['median'], reading_stats['median']],
            mode='lines',
            name=f'Median ({reading_stats["median"]:.2f})',
            line=dict(color='darkred', width=2, dash='dash'),
            opacity=0.8,
            showlegend=True,
            legendgroup="reading"
        ), row=2, col=2)
        
        if reading_stats['mode'] is not None:
            mode_val = reading_stats['mode'] if isinstance(reading_stats['mode'], (int, float)) else reading_stats['mode'][0]
            fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'Mode ({mode_val})',
                line=dict(color='maroon', width=2, dash='dot'),
                opacity=0.8,
                showlegend=True,
                legendgroup="reading"
            ), row=2, col=2)
    
    # 目标线（阅读图）
    fig.add_trace(go.Scatter(
        x=x_range,
        y=[6.5, 6.5],
        mode='lines',
        name='Target (6.5)',
        line=dict(color='green', width=3, dash='dashdot'),
        opacity=0.9,
        showlegend=True,
        legendgroup="reading"
    ), row=2, col=2)
    
    # 添加阅读拟合线和预测
    if reading_fit_data[0] is not None:
        fit_x, fit_y = reading_fit_data[0]
        fig.add_trace(go.Scatter(
            x=fit_x,
            y=fit_y,
            mode='lines',
            name=f'Trend Fit (R²={reading_fit_data[2]["r_squared"]:.3f})',
            line=dict(color='darkred', width=2, dash='longdash'),
            opacity=0.8,
            showlegend=True,
            legendgroup="reading"
        ), row=2, col=2)
        
        # 添加预测点和连接线
        if reading_fit_data[1] is not None:
            future_x, future_y = reading_fit_data[1]
            fig.add_trace(go.Scatter(
                x=future_x,
                y=future_y,
                mode='markers+lines',
                name='Prediction',
                line=dict(color='orange', width=2, dash='dot'),
                marker=dict(color='orange', size=12, symbol='diamond'),
                showlegend=True,
                legendgroup="reading"
            ), row=2, col=2)
            
            # 添加预测值注释
            for i, (px, py) in enumerate(zip(future_x, future_y)):
                fig.add_annotation(
                    x=px, y=py + 0.3,
                    text=f"{py:.1f}",
                    showarrow=False,
                    font=dict(color="orange", size=10),
                    row=2, col=2
                )

    # 更新布局
    fig.update_layout(
        title='IELTS Scores Analysis Dashboard - Combined & Individual Analysis',
        width=1600,
        height=900,
        template='plotly_white',
        # 分组图例设置
        legend=dict(
            groupclick="toggleitem",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        ),
        legend2=dict(
            groupclick="toggleitem",
            orientation="v",
            x=0.48,
            y=0.45,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="blue",
            borderwidth=1
        ),
        legend3=dict(
            groupclick="toggleitem",
            orientation="v",
            x=1.02,
            y=0.45,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="red",
            borderwidth=1
        )
    )
    
    # 设置每个子图的y轴范围和标签
    fig.update_yaxes(range=[0, 9.5], title_text="Score", row=1, col=1)
    fig.update_yaxes(range=[0, 9.5], title_text="Listening Score", row=2, col=1)
    fig.update_yaxes(range=[0, 9.5], title_text="Reading Score", row=2, col=2)
    
    # 设置x轴标签
    fig.update_xaxes(title_text="Test ID", row=1, col=1)
    fig.update_xaxes(title_text="Test ID", row=2, col=1)
    fig.update_xaxes(title_text="Test ID", row=2, col=2)
    
    # 保存为HTML文件
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成单独的子图HTML文件
    # 听力分析子图
    listening_fig = go.Figure()
    if practice_indices:
        listening_fig.add_trace(go.Scatter(
            x=practice_ids, 
            y=practice_listening, 
            mode='lines+markers', 
            name='Practice Scores',
            line=dict(color='blue', width=3),
            marker=dict(size=8, color='blue')
        ))
    if real_indices:
        listening_fig.add_trace(go.Scatter(
            x=real_ids, 
            y=real_listening, 
            mode='markers', 
            name='Real Exam',
            marker=dict(size=15, color='gold', symbol='star', line=dict(width=2, color='darkblue'))
        ))
    
    # 添加听力统计线（默认隐藏）
    if isinstance(listening_stats, dict):
        listening_fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['mean'], listening_stats['mean']],
            mode='lines',
            name=f'Mean ({listening_stats["mean"]:.2f})',
            line=dict(color='lightblue', width=2, dash='solid'),
            opacity=0.8,
            visible='legendonly'  # 默认隐藏
        ))
        
        listening_fig.add_trace(go.Scatter(
            x=x_range,
            y=[listening_stats['median'], listening_stats['median']],
            mode='lines',
            name=f'Median ({listening_stats["median"]:.2f})',
            line=dict(color='darkblue', width=2, dash='dash'),
            opacity=0.8,
            visible='legendonly'  # 默认隐藏
        ))
        
        if listening_stats['mode'] is not None:
            mode_val = listening_stats['mode'] if isinstance(listening_stats['mode'], (int, float)) else listening_stats['mode'][0]
            listening_fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'Mode ({mode_val})',
                line=dict(color='navy', width=2, dash='dot'),
                opacity=0.8,
                visible='legendonly'  # 默认隐藏
            ))
    
    listening_fig.add_trace(go.Scatter(
        x=x_range,
        y=[6.5, 6.5],
        mode='lines',
        name='Target (6.5)',
        line=dict(color='green', width=3, dash='dashdot')
    ))
    
    if listening_fit_data[0] is not None:
        fit_x, fit_y = listening_fit_data[0]
        listening_fig.add_trace(go.Scatter(
            x=fit_x, y=fit_y, mode='lines',
            name=f'Trend (R²={listening_fit_data[2]["r_squared"]:.3f})',
            line=dict(color='darkblue', width=2, dash='longdash')
        ))
        
        if listening_fit_data[1] is not None:
            future_x, future_y = listening_fit_data[1]
            listening_fig.add_trace(go.Scatter(
                x=future_x, y=future_y, mode='markers+lines',
                name='Prediction',
                line=dict(color='purple', width=2, dash='dot'),
                marker=dict(color='purple', size=12, symbol='diamond')
            ))
            
            # 添加预测值注释
            for i, (px, py) in enumerate(zip(future_x, future_y)):
                listening_fig.add_annotation(
                    x=px, y=py + 0.3,
                    text=f"{py:.1f}",
                    showarrow=False,
                    font=dict(color="purple", size=10)
                )
    
    listening_fig.update_layout(
        title='🎧 IELTS Listening Scores Analysis',
        xaxis_title='Test ID',
        yaxis_title='Listening Score',
        yaxis=dict(range=[0, 9.5]),
        template='plotly_white',
        height=500,
        legend=dict(
            groupclick="toggleitem",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top"
        )
    )
    
    listening_html = os.path.join(output_dir, 'listening_scores.html')
    listening_fig.write_html(listening_html, include_plotlyjs='cdn', div_id="listening-chart")
    
    # 阅读分析子图
    reading_fig = go.Figure()
    if practice_indices:
        reading_fig.add_trace(go.Scatter(
            x=practice_ids, 
            y=practice_reading, 
            mode='lines+markers', 
            name='Practice Scores',
            line=dict(color='red', width=3),
            marker=dict(size=8, color='red')
        ))
    if real_indices:
        reading_fig.add_trace(go.Scatter(
            x=real_ids, 
            y=real_reading, 
            mode='markers', 
            name='Real Exam',
            marker=dict(size=15, color='gold', symbol='star', line=dict(width=2, color='darkred'))
        ))
    
    # 添加阅读统计线（默认隐藏）
    if isinstance(reading_stats, dict):
        reading_fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['mean'], reading_stats['mean']],
            mode='lines',
            name=f'Mean ({reading_stats["mean"]:.2f})',
            line=dict(color='lightcoral', width=2, dash='solid'),
            opacity=0.8,
            visible='legendonly'  # 默认隐藏
        ))
        
        reading_fig.add_trace(go.Scatter(
            x=x_range,
            y=[reading_stats['median'], reading_stats['median']],
            mode='lines',
            name=f'Median ({reading_stats["median"]:.2f})',
            line=dict(color='darkred', width=2, dash='dash'),
            opacity=0.8,
            visible='legendonly'  # 默认隐藏
        ))
        
        if reading_stats['mode'] is not None:
            mode_val = reading_stats['mode'] if isinstance(reading_stats['mode'], (int, float)) else reading_stats['mode'][0]
            reading_fig.add_trace(go.Scatter(
                x=x_range,
                y=[mode_val, mode_val],
                mode='lines',
                name=f'Mode ({mode_val})',
                line=dict(color='maroon', width=2, dash='dot'),
                opacity=0.8,
                visible='legendonly'  # 默认隐藏
            ))
    
    reading_fig.add_trace(go.Scatter(
        x=x_range,
        y=[6.5, 6.5],
        mode='lines',
        name='Target (6.5)',
        line=dict(color='green', width=3, dash='dashdot')
    ))
    
    if reading_fit_data[0] is not None:
        fit_x, fit_y = reading_fit_data[0]
        reading_fig.add_trace(go.Scatter(
            x=fit_x, y=fit_y, mode='lines',
            name=f'Trend (R²={reading_fit_data[2]["r_squared"]:.3f})',
            line=dict(color='darkred', width=2, dash='longdash')
        ))
        
        if reading_fit_data[1] is not None:
            future_x, future_y = reading_fit_data[1]
            reading_fig.add_trace(go.Scatter(
                x=future_x, y=future_y, mode='markers+lines',
                name='Prediction',
                line=dict(color='orange', width=2, dash='dot'),
                marker=dict(color='orange', size=12, symbol='diamond')
            ))
            
            # 添加预测值注释
            for i, (px, py) in enumerate(zip(future_x, future_y)):
                reading_fig.add_annotation(
                    x=px, y=py + 0.3,
                    text=f"{py:.1f}",
                    showarrow=False,
                    font=dict(color="orange", size=10)
                )
    
    reading_fig.update_layout(
        title='📖 IELTS Reading Scores Analysis',
        xaxis_title='Test ID',
        yaxis_title='Reading Score',
        yaxis=dict(range=[0, 9.5]),
        template='plotly_white',
        height=500,
        legend=dict(
            groupclick="toggleitem",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top"
        )
    )
    
    reading_html = os.path.join(output_dir, 'reading_scores.html')
    reading_fig.write_html(reading_html, include_plotlyjs='cdn', div_id="reading-chart")
    
    # 显示图表
    fig.show()
    
    print("="*60)
    print("📊 Generated individual score charts:")
    print("   💡 Click legend items to show/hide traces")
    print("   📈 Trend lines show linear fitting with R² values")
    print("   🔮 Diamond markers show predicted future scores")
    print(f"   🎧 Listening chart: {listening_html}")
    print(f"   📖 Reading chart: {reading_html}")
    
    # 打印预测结果
    if listening_fit_data[1] is not None:
        future_x, future_y = listening_fit_data[1]
        print(f"\n🎧 LISTENING PREDICTIONS:")
        for i, (test_id, score) in enumerate(zip(future_x, future_y)):
            print(f"   Test {int(test_id)}: {score:.1f}")
    
    if reading_fit_data[1] is not None:
        future_x, future_y = reading_fit_data[1]
        print(f"\n📖 READING PREDICTIONS:")
        for i, (test_id, score) in enumerate(zip(future_x, future_y)):
            print(f"   Test {int(test_id)}: {score:.1f}")

if __name__ == "__main__":
    main()