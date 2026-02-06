import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

input_file = 'data_clean.csv'
df = pd.read_csv(input_file)

custom_palette = {'Лицей БГУ': '#1f77b4', 'Школа': '#ff7f0e'}
sns.set_theme(style="whitegrid")

col_school = 'Где вы учитесь?'
col_thought = 'Когда ты впервые задумался о том чтобы пойти на курсы/взять репета?'
col_action = 'Когда ты по итогу записался на курсы / взял репета?'

time_mapping = {
    'Первая половина 10го класса': 1,
    'Вторая половина 10го класса': 2,
    'Первая половина 11го класса': 3,
    'Вторая половина 11го класса': 4,
    'Интенсив': 5
}

df_lag = df.copy()

df_lag['thought_num'] = df_lag[col_thought].map(time_mapping)
df_lag['action_num'] = df_lag[col_action].map(time_mapping)

df_lag = df_lag.dropna(subset=['thought_num', 'action_num'])

df_lag['lag'] = df_lag['action_num'] - df_lag['thought_num']

df_lag.loc[df_lag['lag'] < 0, 'lag'] = 0

def categorize_lag(x):
    if x == 0:
        return 'Сразу (в том же полугодии)'
    elif x == 1:
        return 'Думал полгода'
    elif x == 2:
        return 'Думал год'
    else:
        return 'Думал больше года'

df_lag['wait_time'] = df_lag['lag'].apply(categorize_lag)

order_wait = ['Сразу (в том же полугодии)', 'Думал полгода', 'Думал год', 'Думал больше года']

counts = df_lag.groupby([col_school, 'wait_time']).size().reset_index(name='count')
total = df_lag.groupby(col_school).size().reset_index(name='total')
data_plot = pd.merge(counts, total, on=col_school)
data_plot['percent'] = (data_plot['count'] / data_plot['total']) * 100

plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=data_plot, 
    x='wait_time', 
    y='percent', 
    hue=col_school, 
    palette=custom_palette,
    order=order_wait
)

plt.title('Сколько времени от "Задумался" до "Записался"?', fontsize=14, fontweight='bold')
plt.xlabel('Время принятия решения (Lag Time)', fontsize=12)
plt.ylabel('Процент учеников (%)', fontsize=12)
plt.legend(title='Учебное заведение')

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', padding=3)

plt.tight_layout()
plt.savefig('3_decision_window_bar.png', dpi=300)
print("Сохранен график: 3_decision_window_bar.png")
plt.close()

pivot_table = pd.crosstab(
    df_lag[col_thought], 
    df_lag[col_action], 
    normalize='index'
) * 100

ordered_labels = [
    'Первая половина 10го класса', 
    'Вторая половина 10го класса', 
    'Первая половина 11го класса', 
    'Вторая половина 11го класса',
    'Интенсив',
    'Я считаю что сдам своими силами'
]

existing_labels_idx = [x for x in ordered_labels if x in pivot_table.index]
existing_labels_col = [x for x in ordered_labels if x in pivot_table.columns]

pivot_table = pivot_table.loc[existing_labels_idx, existing_labels_col]

plt.figure(figsize=(10, 8))
sns.heatmap(
    pivot_table, 
    annot=True, 
    fmt=".1f", 
    cmap="YlGnBu", 
    cbar_kws={'label': 'Процент перехода (%)'}
)

plt.title('Когда задумался vs Когда купил', fontsize=14, fontweight='bold')
plt.xlabel('Когда по факту записался', fontsize=12)
plt.ylabel('Когда впервые задумался', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('3_decision_window_heatmap.png', dpi=300)
print("Сохранен график: 3_decision_window_heatmap.png")
plt.close()