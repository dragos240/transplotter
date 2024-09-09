from typing import Tuple, Dict
from calendar import monthrange, month_name

from matplotlib.figure import Axes
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

x_coords = []
y_coords = []


def draw_month_header(year: int,
                      month: int,
                      ax: Axes,
                      x: float, y: float):
    color = "black"
    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    month_name = month_names[month-1]
    month_label = f"{month_name} {year}"
    ax.text(x, y, month_label, color=color, va="center")


def draw_days_header(ax: Axes,
                     x: float, y: float):
    color = "black"
    x_offset_rate = 1
    for weekday in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        ax.text(x, y, weekday, ha="center", va="center", color=color)
        x += x_offset_rate


def draw_day_text(ax: Axes,
                  day: int,
                  x: float, y: float):
    color = "black"
    x_coords.append(x)
    y_coords.append(y)
    text = ax.text(x, y, day, ha="center", va="center", color=color)


def draw_calendar(ax: Axes,
                  year: int,
                  month: int):
    weekday, num_days = monthrange(year, month)

    # adjust by 0.5 to set text at the ceter of grid square
    x_start = 1 - 0.5
    y_start = 5 + 0.5
    x_offset_rate = 1
    y_offset = -1

    draw_month_header(year, month, ax, x_start, y_start + 2)
    draw_days_header(ax, x_start, y_start + 1)

    y = y_start

    for day in range(1, num_days + 1):
        x = x_start + weekday * x_offset_rate

        draw_day_text(ax, day, x, y)
        weekday = (weekday + 1) % 7
        if weekday == 0:
            y += y_offset


def plot(yearmonth: Tuple[int, int],
         transactions: Dict[int, float]):
    year, month = yearmonth
    fig: plt.FigureBase = plt.figure()
    ax: Axes = fig.add_subplot()
    ax.axis([0, 7, 0, 7])

    draw_calendar(ax, year, month)
    plot = ax.plot(x_coords, y_coords, 'o', color="#00000000")

    cursor = mplcursors.cursor(plot, hover=True)

    @cursor.connect("add")
    def _(sel: mplcursors.Selection):
        sel.annotation.set(text=f"${transactions[sel.index]:.2f}")

    plt.show()


def generate_days_grid(yearmonth: Tuple[int, int],
                       transactions: Dict[int, float]) -> np.ndarray:
    DAYS_IN_WEEK = 7
    year, month = yearmonth
    week_start_day, num_days = monthrange(year, month)
    week_start_day = (week_start_day + 1) % 7  # Adjust to start on Sunday

    # Calculate the number of weeks needed
    num_weeks = (num_days + week_start_day + DAYS_IN_WEEK - 1) // DAYS_IN_WEEK

    # Create a 2D numpy array for weeks, initialized with NaN
    weeks = np.full((num_weeks, DAYS_IN_WEEK), np.nan)

    # Fill the array with transaction totals
    day_index = 0
    for week in range(num_weeks):
        for day in range(DAYS_IN_WEEK):
            if week == 0 and day < week_start_day:
                continue
            if day_index < num_days:
                weeks[week, day] = transactions.get(day_index, 0)
                day_index += 1

    return weeks


def create_expenses_heatmap(yearmonth: Tuple[int, int],
                            transactions: Dict[int, float]):
    year, month = yearmonth

    data = generate_days_grid(yearmonth, transactions)

    ax: Axes
    _, ax = plt.subplots()  # type: ignore

    # Create the heatmap
    heatmap = ax.imshow(data, cmap='coolwarm', interpolation='nearest')

    # Create a label for each data point on the heatmap
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # Continue if type is NaN
            if np.isnan(data[i, j]):
                continue
            ax.text(j, i, f'{data[i, j]:.2f}',
                    ha='center', va='center', color='black')

    # Add color bar to represent income/expense
    plt.colorbar(heatmap, label='Amount')

    # Add labels for days of the week
    plt.xticks(np.arange(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.yticks(np.arange(6), ['Week 1', 'Week 2',
               'Week 3', 'Week 4', 'Week 5', 'Week 6'])

    plt.tight_layout()

    # Add title
    plt.title(
        f'Expenses and Income Heatmap for {month_name[month]} {year}')

    # Show the plot
    plt.show()
