import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

input_file = 'data_clean.csv'
df = pd.read_csv(input_file)

custom_palette = {'Лицей БГУ': '#1f77b4', 'Школа': '#ff7f0e'}
sns.set_theme(style="whitegrid")

col_school = 'Где вы учитесь?'
col_score = 'На какой балл по экзу ты реально рассчитываешь?'
col_time = 'Когда ты по итогу записался на курсы / взял репета?'
col_subjects = 'Какие предметы вы планируете сдавать?'

def save_plot(filename, title, xlabel, ylabel):
    plt.title(title, fontsize=16, pad=20, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Сохранено: {filename}")
    plt.close()

def prepare_percent_data(df, col, group_col, order=None):
    counts = df.groupby([group_col, col]).size().reset_index(name='count')
    
    total = df.groupby(group_col).size().reset_index(name='total')
    
    data = pd.merge(counts, total, on=group_col)
    data['percent'] = (data['count'] / data['total']) * 100
    
    if order:
        data[col] = pd.Categorical(data[col], categories=order, ordered=True)
        data = data.sort_values(col)
        
    return data

order_score = ['90+', '80-90', '70-80', 'До 70']
data_score = prepare_percent_data(df, col_score, col_school, order_score)

plt.figure(figsize=(10, 6))
ax = sns.barplot(data=data_score, x=col_score, y='percent', hue=col_school, palette=custom_palette)

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', padding=3)

save_plot('1_ambitions.png', 'Ожидаемые баллы (Амбиции)', 'Баллы', 'Процент опрошенных (%)')


time_map = {
    'Первая половина 10го класса': '10 класс (перв. пол)',
    'Вторая половина 10го класса': '10 класс (втор. пол)',
    'Первая половина 11го класса': '11 класс (перв. пол)',
    'Вторая половина 11го класса': '11 класс (втор. пол)',
    'Интенсив': 'Интенсив перед экзами',
    'Сам': 'Самостоятельно'
}
df[col_time] = df[col_time].fillna('Сам')
df['time_group'] = df[col_time].map(time_map)
order_time = ['10 класс (перв. пол)', '10 класс (втор. пол)', '11 класс (перв. пол)', '11 класс (втор. пол)', 'Интенсив перед экзами', 'Самостоятельно']

data_time = prepare_percent_data(df, 'time_group', col_school, order_time)

plt.figure(figsize=(13, 7))
ax = sns.barplot(data=data_time, x='time_group', y='percent', hue=col_school, palette=custom_palette)
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', padding=3)

save_plot('2_preparation_start.png', 'Время когда взяли репетитора', '', 'Процент опрошенных (%)')
