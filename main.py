import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

mu = 0  # Mean
sigma = 1.4  # Standard deviation
n = 147  # Number of samples

# Generate a list of random numbers
frequency_list = np.random.normal(mu, sigma, n)

sns.displot(frequency_list)

plt.show()

def plot_freq_polygon(freq_list):
    # Create a list of x values
    x = list(range(1, len(freq_list) + 1))

    # Build a frequency polygon
    plt.plot(x, freq_list, marker='o', linestyle='-')

    # Set the x-axis and y-axis labels
    plt.xlabel('Frequency number')
    plt.ylabel('Frequency')
    plt.title('Frequency polygon')

    # Show the plot
    plt.show()

# Example usage
plot_freq_polygon(frequency_list)

def calculate_statistics(freq_list):
    # Calculate the mean
    mean = np.sum(freq_list) / len(freq_list)

    # Calculate the median
    sorted_list = freq_list.sort()
    n = len(freq_list)

    if n % 2 == 0: 
        median = (sorted_list[n // 2 - 1] + sorted_list[n // 2]) / 2
    else: 
        median = sorted_list[n // 2]

    # Calculate the mode
    min_value = np.min(freq_list)
    counts = np.bincount(freq_list - min_value + 1).tolist()
    mode = np.argmax(counts) + min_value - 1

    # Calculate the variance
    variance = np.sum((freq_list - mean) ** 2) / (len(freq_list) - 1)

    # Calculate the standard deviation
    stdev = np.sqrt(variance)

    # Show the results
    print("MEAN:", mean)
    print("MEDIAN:", median)
    print("MODE:", mode)
    print("VARIANCE:", variance)
    print("STANDARD DEVIATION:", stdev)

# Example usage
calculate_statistics(frequency_list)

def plot_boxplot(freq_list):
    # Build a boxplot
    plt.boxplot(freq_list)

    # Set the x-axis and y-axis labels
    plt.xlabel('Frequency')
    plt.ylabel('Value')
    plt.title('Boxplot')

    # Show the plot
    plt.show()

def plot_pareto(freq_list):
    # Sort the frequencies in descending order
    freq_list.sort()
    freq_list[:] = freq_list[::-1]

    # Calculate the cumulative sum
    cum_sum = [sum(freq_list[:i+1]) for i in range(len(freq_list))]

    # Calculate the total sum
    total_sum = sum(freq_list)

    # Calculate the cumulative percentage
    cum_percentage = [cum / total_sum * 100 for cum in cum_sum]

    # Build a Pareto chart
    fig, ax1 = plt.subplots()

    ax1.bar(range(len(freq_list)), freq_list, align='center')
    ax1.set_xlabel('Frequency number')
    ax1.set_ylabel('Frequency')

    ax2 = ax1.twinx()
    ax2.plot(range(len(freq_list)), cum_percentage, color='r', marker='o')
    ax2.set_ylabel('Cumulative %')

    plt.title('Pareto chart')
    plt.show()

def plot_pie_chart(freq_list):
    # Build a pie chart
    plt.pie(freq_list, labels=range(1, len(freq_list)+1), autopct='%1.1f%%')

    # Set the title
    plt.title('Pie chart')

    # Show the plot
    plt.show()

# Example usage

plot_boxplot(frequency_list)
plot_pareto(frequency_list)
plot_pie_chart(frequency_list)