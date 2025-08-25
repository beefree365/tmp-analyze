import java.util.*;
import java.util.stream.Collectors;

public class RecursiveFilter {
    /**
     * 递归过滤，去掉超出均值 ±k*std 的数据，直到所有数据都落在范围内。
     * 返回过滤后数据、均值、标准差、被过滤掉的异常值
     */
    public static FilterResult recursiveFilter(List<Double> data, double k) {
        List<Double> removed = new ArrayList<>();
        List<Double> current = new ArrayList<>(data);
        while (true) {
            double mean = mean(current);
            double std = std(current, mean);
            List<Double> filtered = current.stream()
                    .filter(x -> x >= mean - k * std && x <= mean + k * std)
                    .collect(Collectors.toList());
            if (filtered.size() == current.size()) {
                return new FilterResult(filtered, mean, std, removed);
            }
            for (double x : current) {
                if (x < mean - k * std || x > mean + k * std) {
                    removed.add(x);
                }
            }
            current = filtered;
        }
    }

    public static double mean(List<Double> data) {
        return data.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
    }

    public static double std(List<Double> data, double mean) {
        double variance = data.stream().mapToDouble(x -> (x - mean) * (x - mean)).average().orElse(0.0);
        return Math.sqrt(variance);
    }

    public static void printFilterResult(FilterResult result, double k) {
        System.out.println("最终保留数据: " + result.filtered);
        System.out.printf("最终平均值 = %.2f\n", result.mean);
        System.out.printf("最终标准差 = %.2f\n", result.std);
        System.out.printf("%.0f倍标准差上下线: [%.2f, %.2f]\n", k, result.mean - k * result.std, result.mean + k * result.std);
        System.out.println("被过滤掉的异常值: " + result.removed);
    }

    public static void main(String[] args) {
        List<Double> volumes = Arrays.asList(190.0, 191.0, 181.0, 119.0, 166.0, 90.0, 123.0, 131.0, 356.0, 1057.0);
        double k = 2.0;
        FilterResult result = recursiveFilter(volumes, k);
        printFilterResult(result, k);
        // 如需绘图，可导出数据用Python等工具绘制
    }

    static class FilterResult {
        List<Double> filtered;
        double mean;
        double std;
        List<Double> removed;
        FilterResult(List<Double> filtered, double mean, double std, List<Double> removed) {
            this.filtered = filtered;
            this.mean = mean;
            this.std = std;
            this.removed = removed;
        }
    }
}
