import sys
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from scipy import stats

OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)

def convert_weekday(weekday):
    return weekday.date().weekday()
def convert_year(date):
    return date.date().isocalendar().year
def convert_week(date):
    return date.date().isocalendar().week

def main():
    counts = pd.read_json(sys.argv[1], convert_dates=['date'],lines=True)
    counts = counts[(counts['date'] > '2011-12-31') & (counts['date'] < '2014-01-01')]
    counts = counts[counts['subreddit'] == 'canada']
    counts['weekend'] = counts['date'].apply(convert_weekday)
    
    weekends = counts[counts['weekend'] > 4].copy()
    weekdays = counts[counts['weekend'] < 5].copy()
    weekdays['log'] = np.log(weekdays['comment_count'])
    weekends['log'] = np.log(weekends['comment_count'])
    
    day = weekdays.copy()
    day['year'] = day['date'].apply(convert_year)
    # day[''] = day['week'] * 100
    day['week'] = day['date'].apply(convert_week)
    day = day.drop(['date', 'subreddit'], axis=1)
    day = day.groupby(by=['week', 'year']).mean()
    
    end = weekends.copy()
    end['year'] = end['date'].apply(convert_year)
    # end['week'] = end['week'] * 100
    end['week'] = end['date'].apply(convert_week)
    end = end.drop(['date', 'subreddit'], axis=1)
    end = end.groupby(by=['week', 'year']).mean()
    
    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=stats.ttest_ind(weekdays['comment_count'], weekends['comment_count']).pvalue,
        initial_weekday_normality_p=stats.normaltest(weekdays['comment_count']).pvalue,
        initial_weekend_normality_p=stats.normaltest(weekends['comment_count']).pvalue,
        initial_levene_p=stats.levene(weekends['comment_count'], weekdays['comment_count']).pvalue,
        transformed_weekday_normality_p=stats.normaltest(weekdays['log']).pvalue,
        transformed_weekend_normality_p=stats.normaltest(weekends['log']).pvalue,
        transformed_levene_p=stats.levene(weekends['log'], weekdays['log']).pvalue,
        weekly_weekday_normality_p=stats.normaltest(day['comment_count']).pvalue,
        weekly_weekend_normality_p=stats.normaltest(end['comment_count']).pvalue,
        weekly_levene_p=stats.levene(end['comment_count'], day['comment_count']).pvalue,
        weekly_ttest_p=stats.ttest_ind(day['comment_count'], end['comment_count']).pvalue,
        utest_p=stats.mannwhitneyu(weekends['comment_count'], weekdays['comment_count']).pvalue,
    ))
    
if __name__ == '__main__':
    main()