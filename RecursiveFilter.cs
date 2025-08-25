using System;
using System.Collections.Generic;
using System.Linq;

class RecursiveFilter
{
    // 递归过滤，去掉超出均值 ±k*std 的数据，直到所有数据都落在范围内。
    public static FilterResult RecursiveFilterFunc(List<double> data, double k)
    {
        var removed = new List<double>();
        var current = new List<double>(data);
        while (true)
        {
            double mean = current.Average();
            double std = Std(current, mean);
            var filtered = current.Where(x => x >= mean - k * std && x <= mean + k * std).ToList();
            if (filtered.Count == current.Count)
                return new FilterResult(filtered, mean, std, removed);
            foreach (var x in current)
            {
                if (x < mean - k * std || x > mean + k * std)
                    removed.Add(x);
            }
            current = filtered;
        }
    }

    public static double Std(List<double> data, double mean)
    {
        double variance = data.Select(x => (x - mean) * (x - mean)).Average();
        return Math.Sqrt(variance);
    }

    public static void PrintFilterResult(FilterResult result, double k)
    {
        Console.WriteLine("最终保留数据: " + string.Join(", ", result.Filtered));
        Console.WriteLine("最终平均值 = {0:F2}", result.Mean);
        Console.WriteLine("最终标准差 = {0:F2}", result.Std);
        Console.WriteLine("{0}倍标准差上下线: [{1:F2}, {2:F2}]", k, result.Mean - k * result.Std, result.Mean + k * result.Std);
        Console.WriteLine("被过滤掉的异常值: " + string.Join(", ", result.Removed));
    }

    static void Main(string[] args)
    {
        var volumes = new List<double> { 190, 191, 181, 119, 166, 90, 123, 131, 356, 1057 };
        double k = 2.0;
        var result = RecursiveFilterFunc(volumes, k);
        PrintFilterResult(result, k);
    }

    public class FilterResult
    {
        public List<double> Filtered;
        public double Mean;
        public double Std;
        public List<double> Removed;
        public FilterResult(List<double> filtered, double mean, double std, List<double> removed)
        {
            Filtered = filtered;
            Mean = mean;
            Std = std;
            Removed = removed;
        }
    }
}
