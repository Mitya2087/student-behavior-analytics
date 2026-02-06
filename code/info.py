import pandas as pd


input_file = 'data_clean.csv'
df = pd.read_csv(input_file)

col_school = 'Где вы учитесь?'
col_thought = 'Когда ты впервые задумался о том чтобы пойти на курсы/взять репета?'

order_thought = [
    'Первая половина 10го класса',
    'Вторая половина 10го класса',
    'Первая половина 11го класса',
    'Вторая половина 11го класса',
    'Я считаю что сдам своими силами'
]

if 'Не указано' in df[col_thought].unique():
    order_thought.append('Не указано')

def format_stats(subset, total_count):
    counts = subset[col_thought].value_counts()
    counts = counts.reindex(order_thought, fill_value=0)
    
    result = []
    for category in order_thought:
        count = counts[category]
        if total_count > 0:
            percent = (count / total_count) * 100
        else:
            percent = 0
        result.append(f"{percent:.1f}% ({count})")
    return result

total_lyceum = len(df[df[col_school] == 'Лицей БГУ'])
total_school = len(df[df[col_school] == 'Школа'])
total_all = len(df)

stats_lyceum = format_stats(df[df[col_school] == 'Лицей БГУ'], total_lyceum)
stats_school = format_stats(df[df[col_school] == 'Школа'], total_school)
stats_all = format_stats(df, total_all)

result_df = pd.DataFrame({
    'Период': order_thought,
    'Лицей БГУ': stats_lyceum,
    'Школа': stats_school,
    'ВСЕГО': stats_all
})

print(f"Всего опрошено: {total_all} человек (Лицей: {total_lyceum}, Школа: {total_school})")
print("-" * 80)
print(result_df.to_string(index=False))
print("-" * 80)