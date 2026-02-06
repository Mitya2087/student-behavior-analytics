import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

input_file = 'data_clean.csv'
df = pd.read_csv(input_file)

sns.set_theme(style="whitegrid")

col_tutors = 'По каким предметам ты взял репета?' 

df_clean = df.dropna(subset=[col_tutors]).copy()

def clean_split(text):
    if pd.isna(text): return []
    return [x.strip() for x in text.split(',')]

df_clean['subjects_list'] = df_clean[col_tutors].apply(clean_split)

df_exploded = df_clean.explode('subjects_list')

counts = df_exploded['subjects_list'].value_counts().reset_index()
counts.columns = ['Предмет', 'Количество']

plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=counts,
    x='Предмет',
    y='Количество',
    palette='viridis',
    hue='Предмет',
    legend=False
)

plt.title('Топ предметов: каких репетиторов берут чаще всего?', fontsize=14, fontweight='bold')
plt.xlabel('Предмет', fontsize=12)
plt.ylabel('Количество учеников', fontsize=12)
plt.xticks(rotation=45)

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.tight_layout()
plt.savefig('popular_tutors_overall.png', dpi=300)
print("Сохранен график: popular_tutors_overall.png")
plt.close()


dummies = df_clean[col_tutors].str.get_dummies(sep=', ')

co_occurrence = dummies.T.dot(dummies)

np.fill_diagonal(co_occurrence.values, 0)

plt.figure(figsize=(12, 10))
sns.heatmap(
    co_occurrence,
    annot=True,
    fmt='d',
    cmap='Reds',
    linewidths=1,
    linecolor='white'
)

plt.title('Матрица связей: какие предметы берут вместе?', fontsize=14, fontweight='bold')
plt.xlabel('Предмет А', fontsize=12)
plt.ylabel('Предмет Б', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('tutors_connections_heatmap.png', dpi=300)
print("Сохранен график: tutors_connections_heatmap.png")
plt.close()