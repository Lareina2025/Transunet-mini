import os
import numpy as np
from collections import defaultdict
import random
import shutil

def load_npz_file(file_path):
    """加载NPZ格式文件"""
    data = np.load(file_path)
    return data['image'], data['label']

def is_valid_slice(label_slice, organ_indices):
    """检查切片是否包含至少一个目标器官"""
    return np.any(np.isin(label_slice, list(organ_indices.values())))

def collect_samples(data_dir, num_samples=300):
    """
    从NPZ格式数据集中收集样本切片
    :param data_dir: 包含NPZ文件的目录
    :param num_samples: 要选择的样本数量
    :return: 选中的样本列表，每个元素是(npz文件路径, 切片索引)元组
    """
    # 定义器官对应的标签索引（Synapse标准）
    organ_indices = {
        'aorta': 1,
        'gallbladder': 2,
        'spleen': 3,
        'left_kidney': 4,
        'right_kidney': 5,
        'liver': 6,
        'pancreas': 7,
        'stomach': 8
    }
    
    # 获取所有NPZ文件
    npz_files = [f for f in os.listdir(data_dir) if f.endswith('.npz')]
    
    # 准备数据结构
    organ_slices = defaultdict(list)
    all_valid_slices = []
    
    # 遍历所有NPZ文件
    for file_name in npz_files:
        file_path = os.path.join(data_dir, file_name)
        try:
            _, label = load_npz_file(file_path)
            
            # 检查是否包含至少一个器官
            if is_valid_slice(label, organ_indices):
                # 记录包含的器官
                present_organs = [
                    org for org, idx in organ_indices.items() 
                    if idx in label
                ]
                
                # 添加到全局列表
                all_valid_slices.append((file_path, file_name, 0))  # 添加原始文件名
                
                # 按器官分类
                for org in present_organs:
                    organ_slices[org].append((file_path, file_name, 0))
                    
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue
    
    print(f"Found {len(all_valid_slices)} valid slices in total.")
    
    # 平衡采样逻辑
    selected_samples = set()
    num_organs = len(organ_indices)
    samples_per_organ = max(1, num_samples // (2 * num_organs))
    
    # 第一阶段：器官平衡采样
    for org in organ_indices:
        if not organ_slices[org]:
            print(f"Warning: No slices found for {org}")
            continue
            
        available = [s for s in organ_slices[org] if s not in selected_samples]
        if not available:
            continue
            
        samples_to_take = min(samples_per_organ, len(available))
        selected_samples.update(random.sample(available, samples_to_take))
    
    # 第二阶段：补充剩余样本
    remaining = num_samples - len(selected_samples)
    if remaining > 0:
        available = [s for s in all_valid_slices if s not in selected_samples]
        if available:
            selected_samples.update(random.sample(available, min(remaining, len(available))))
    
    selected_samples = list(selected_samples)[:num_samples]
    
    # 验证分布
    dist = defaultdict(int)
    for sample in selected_samples:
        file_path, _, _ = sample
        _, label = load_npz_file(file_path)
        for org, idx in organ_indices.items():
            if idx in label:
                dist[org] += 1
    
    print("\n器官分布统计:")
    for org, count in dist.items():
        print(f"{org}: {count} slices")
    
    return selected_samples

def copy_selected_samples(selected_samples, output_dir):
    """自动复制选中的样本到指定目录，保留原始文件名"""
    os.makedirs(output_dir, exist_ok=True)
    
    for src_path, original_name, _ in selected_samples:
        dst_path = os.path.join(output_dir, original_name)
        
        # 处理文件名冲突
        counter = 1
        while os.path.exists(dst_path):
            name, ext = os.path.splitext(original_name)
            dst_path = os.path.join(output_dir, f"{name}_{counter}{ext}")
            counter += 1
        
        shutil.copy2(src_path, dst_path)
    
    print(f"\n已自动复制 {len(selected_samples)} 个样本到 {output_dir}，保留原始文件名")

if __name__ == "__main__":
    # 修改为有写入权限的目录
    base_dir = r"E:\PyProjects\Transunet\data\Synapse"
    data_dir = os.path.join(base_dir, "train_npz")
    output_dir = r"F:\selected_300_samples"
    csv_path = os.path.join(base_dir, "selected_samples.csv")
    
    try:
        samples = collect_samples(data_dir, 300)
        
        # 保存结果
        with open(csv_path, "w") as f:
            f.write("original_name,file_path,slice_index\n")
            for path, name, idx in samples:
                f.write(f"{name},{path},{idx}\n")
        
        print(f"\n成功选取 {len(samples)} 个样本，结果已保存。")
        copy_selected_samples(samples, output_dir)
        
    except PermissionError:
        print("\n权限错误解决方案:")
        print(f"1. 确保你有写入 {base_dir} 的权限")
        print("2. 尝试以管理员身份运行程序")
        print("3. 或者将输出路径改为你有写入权限的目录")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        print("建议检查:")
        print("1. 数据路径是否正确")
        print("2. NPZ文件格式是否一致")
        print("3. 磁盘空间是否充足")
    
