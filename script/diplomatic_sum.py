#!python

import pandas as pd
import sys
import calendar

def get_action_word(word, number, sentence = False):
    if word == 'phone':
        word += " call"
    if sentence:
        if 'Beijing' in word:
            word = word.replace('visit', 'guest')
        elif 'abroad' in word:
            word = 'foreign activity'
    if number == 1:
        return word
    if 'visit' in word or 'guest' in word or 'foreign activity' in word:
        return word.replace('visit', 'visits').replace('guest', 'guests').replace('foreign activity', 'foreign activities')
    else:
        return word + 's'

diplomatic_activities = '../_data/diplomatic_activities.csv'

dip_ac_df = pd.read_csv(diplomatic_activities, header=0, parse_dates = ['date'])

month = int(sys.argv[1])
year = int(sys.argv[2])

df_filtered = dip_ac_df[(dip_ac_df['date'].dt.month == month) \
                        & (dip_ac_df['date'].dt.year == year) ]

df_filtered = df_filtered.sort_values(by=['format', 'date'])

df_filtered['Count'] = df_filtered.groupby('format').cumcount() + 1

df_count = df_filtered.pop('Count')

df_filtered.insert(0,'Count', df_count)

df_filtered.to_csv('../_data/diplomatic_{}_{}.csv'.format(year,month), index=False, date_format='%Y %b %d')

format_dict = df_filtered['format'].value_counts().to_dict()
verb_dict = {'letter': 'replied',
             'message': 'sent',
             'phone': 'made',
             'video': 'made',
             'visit in Beijing': 'met',
             'visit abroad': 'made'}

with open(f'../video_materials/content_{year}_{month}.txt', 'w') as cf:
    cf.write(f'In {calendar.month_name[month]} of {year}, Xi Jinping had {df_filtered.shape[0]} diplomatic activities.\n')
    cf.write(f'\nThese diplomatic activities involved {df_filtered["country"].nunique()} countries and organizations: \n')
    cf.write(f'{(", ").join(df_filtered["country"].unique().tolist()) }\n')

    cf.write(f'\nXi Jinping\'s diplomatic activities in {calendar.month_name[month]} of {year} includes ')
    for k, v in format_dict.items():
        cf.write(f'{v} {get_action_word(k, v)} ')
    cf.write('.\n')
    for k, v in format_dict.items():
        cf.write(f'\nYou {verb_dict[k]} {v} {get_action_word(k,v, True)}:\n')
        df_filtered_format = df_filtered[df_filtered['format'] == k]
        for index, row in df_filtered_format.iterrows():
            cf.write(f'{row["Count"]} On {row["date"].strftime("%Y %B %d")}, To {row["country"]} {row["counterparty"]} for {row["message"]} \n')
        
