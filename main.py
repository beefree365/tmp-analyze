
import numpy as np
import matplotlib.pyplot as plt

def recursive_filter(data, k=2):
    """
    递归过滤，去掉超出均值 ±k*std 的数据，直到所有数据都落在范围内。
    返回：过滤后数据、均值、标准差、被过滤掉的异常值
    """
    removed = []
    while True:
        mean_val = data.mean()
        std_val = data.std(ddof=0)
        mask = (data >= mean_val - k*std_val) & (data <= mean_val + k*std_val)
        if mask.all():
            return data, mean_val, std_val, np.array(removed)
        removed.extend(data[~mask])
        data = data[mask]

def print_filter_result(final_volumes, final_mean, final_std, removed_outliers, k=2):
    print("最终保留数据:", final_volumes)
    print(f"最终平均值 = {final_mean:.2f}")
    print(f"最终标准差 = {final_std:.2f}")
    print(f"{k}倍标准差上下线: [{final_mean - k*final_std:.2f}, {final_mean + k*final_std:.2f}]")
    print("被过滤掉的异常值:", removed_outliers)

def plot_volumes(final_volumes, final_mean, final_std, filename="output.png"):
    x = np.arange(len(final_volumes))
    plt.figure(figsize=(10,6))
    plt.plot(x, final_volumes, marker='o', label="Final Volumes")
    plt.axhline(final_mean, color='green', linestyle='--', label=f"Mean = {final_mean:.1f}")
    for i in range(1, 4):
        plt.axhline(final_mean + i*final_std, color='red', linestyle=':', label=f"+{i}σ = {final_mean + i*final_std:.1f}")
        plt.axhline(final_mean - i*final_std, color='blue', linestyle=':', label=f"-{i}σ = {final_mean - i*final_std:.1f}")
    plt.title("Recursive Filtered Volumes (All within ±2σ)")
    plt.xlabel("Index (Final)")
    plt.ylabel("Volume")
    plt.legend(loc="upper left", bbox_to_anchor=(1,1))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)

def main():
    # 初始数据
    volumes = np.array([190, 191, 181, 119, 166, 90, 123, 131, 356, 1057])
    k = 2
    final_volumes, final_mean, final_std, removed_outliers = recursive_filter(volumes, k=k)
    print_filter_result(final_volumes, final_mean, final_std, removed_outliers, k=k)
    plot_volumes(final_volumes, final_mean, final_std, filename="output.png")

if __name__ == "__main__":
    main()
