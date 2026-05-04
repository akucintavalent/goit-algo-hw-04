from timeit import timeit
import numpy as np
from collections import namedtuple
from collections.abc import Callable
import matplotlib.pyplot as plt
from functools import cache


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    return merge(merge_sort(left_half), merge_sort(right_half))


def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged


def insertion_sort(lst):
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and key < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst


tim_sort = sorted

SortTimes = namedtuple(
    "SortTimes", ["size", "merge_time", "insertion_time", "tim_time"]
)


def gather_times(data_generator: Callable[[int], list[float]]):
    times: list[SortTimes] = []

    for size in range(100, 10001, 100):
        average_merge_time = 0
        average_insertion_time = 0
        average_tim_time = 0

        for _ in range(5):  # Run each size 5 times for better averaging
            arr = data_generator(size)

            merge_arr_copy = arr.copy()
            insertion_arr_copy = arr.copy()
            tim_arr_copy = arr.copy()

            merge_time = timeit(lambda: merge_sort(merge_arr_copy), number=1)
            insertion_time = timeit(
                lambda: insertion_sort(insertion_arr_copy), number=1
            )
            tim_time = timeit(lambda: tim_sort(tim_arr_copy), number=1)

            average_merge_time += merge_time
            average_insertion_time += insertion_time
            average_tim_time += tim_time

        average_merge_time /= 5
        average_insertion_time /= 5
        average_tim_time /= 5

        times.append(
            SortTimes(
                size, average_merge_time, average_insertion_time, average_tim_time
            )
        )

    return times


@cache
def gather_times_for_random_data():
    return gather_times(lambda size: list(np.random.rand(size)))


@cache
def gather_times_for_sorted_data():
    return gather_times(lambda size: list(range(size)))


@cache
def gather_times_for_reverse_sorted_data():
    return gather_times(lambda size: list(range(size, 0, -1)))


def draw_plot(ax: plt.Axes, times: list[SortTimes], title: str):
    sizes = [t.size for t in times]
    merge_times = [t.merge_time for t in times]
    insertion_times = [t.insertion_time for t in times]
    tim_times = [t.tim_time for t in times]

    ax.plot(sizes, merge_times, label="Merge sort")
    ax.plot(sizes, insertion_times, label="Insertion sort")
    ax.plot(sizes, tim_times, label="Timsort (Python built-in)")

    ax.set_title(title)
    ax.set_xlabel("Size")
    ax.set_ylabel("Time (s)")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.4)


def draw_plots():
    random_times = gather_times_for_random_data()
    sorted_times = gather_times_for_sorted_data()
    reverse_sorted_times = gather_times_for_reverse_sorted_data()

    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharex=True, sharey=True)
    fig.suptitle("Sorting algorithms comparison", fontsize=14)

    draw_plot(axes[0], random_times, "Random data")
    draw_plot(axes[1], sorted_times, "Sorted data")
    draw_plot(axes[2], reverse_sorted_times, "Reverse sorted data")

    # Single legend for the whole figure
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False)

    fig.tight_layout(rect=(0, 0.07, 1, 0.95))
    plt.show()


def quadratic_correlation_coefficient(times: list[SortTimes]):
    sizes = np.array([t.size for t in times])
    merge_times = np.array([t.merge_time for t in times])
    insertion_times = np.array([t.insertion_time for t in times])
    tim_times = np.array([t.tim_time for t in times])

    merge_corr = np.corrcoef(sizes**2, merge_times)[0, 1]
    insertion_corr = np.corrcoef(sizes**2, insertion_times)[0, 1]
    tim_corr = np.corrcoef(sizes**2, tim_times)[0, 1]

    return merge_corr, insertion_corr, tim_corr


def linear_logarithmic_correlation_coefficient(times: list[SortTimes]):
    sizes = np.array([t.size for t in times])
    merge_times = np.array([t.merge_time for t in times])
    insertion_times = np.array([t.insertion_time for t in times])
    tim_times = np.array([t.tim_time for t in times])

    merge_corr = np.corrcoef(sizes * np.log(sizes), merge_times)[0, 1]
    insertion_corr = np.corrcoef(sizes * np.log(sizes), insertion_times)[0, 1]
    tim_corr = np.corrcoef(sizes * np.log(sizes), tim_times)[0, 1]

    return merge_corr, insertion_corr, tim_corr


def print_correlation_results(times: list[SortTimes]):
    merge_quad_corr, insertion_quad_corr, tim_quad_corr = (
        quadratic_correlation_coefficient(times)
    )
    merge_log_corr, insertion_log_corr, tim_log_corr = (
        linear_logarithmic_correlation_coefficient(times)
    )

    print("Quadratic Correlation Coefficients:")
    print(f"Merge sort: {merge_quad_corr:.4f}")
    print(f"Insertion sort: {insertion_quad_corr:.4f}")
    print(f"Timsort: {tim_quad_corr:.4f}\n")

    print("Linear-Logarithmic Correlation Coefficients:")
    print(f"Merge sort: {merge_log_corr:.4f}")
    print(f"Insertion sort: {insertion_log_corr:.4f}")
    print(f"Timsort: {tim_log_corr:.4f}")


if __name__ == "__main__":
    random_times = gather_times_for_random_data()
    print("Correlation results for random data:")
    print_correlation_results(random_times)

    sorted_times = gather_times_for_sorted_data()
    print("\nCorrelation results for sorted data:")
    print_correlation_results(sorted_times)

    reverse_sorted_times = gather_times_for_reverse_sorted_data()
    print("\nCorrelation results for reverse sorted data:")
    print_correlation_results(reverse_sorted_times)

    draw_plots()
