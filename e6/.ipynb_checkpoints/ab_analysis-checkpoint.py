import sys
import pandas as pd
from scipy.stats import chi2_contingency, mannwhitneyu

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    data = pd.read_json(sys.argv[1], orient='records', lines=True)
    
    inst = data[data['is_instructor'] == True]
    
    new_stud = data[data['uid'] % 2 == 1]
    old_stud = data[data['uid'] % 2 == 0]
    
    new_inst = inst[inst['uid'] % 2 == 1]
    old_inst = inst[inst['uid'] % 2 == 0]
    
    chi2, u_ch2, dof, expected = chi2_contingency([[len(new_stud[new_stud['search_count'] > 0].index), len(new_stud[new_stud['search_count'] == 0].index)], [len(old_stud[old_stud['search_count'] > 0].index), len(old_stud[old_stud['search_count'] == 0].index)]])
    
    chi2, i_ch2, dof, expected = chi2_contingency([[len(new_inst[new_inst['search_count'] > 0].index), len(new_inst[new_inst['search_count'] == 0].index)], [len(old_inst[old_inst['search_count'] > 0].index), len(old_inst[old_inst['search_count'] == 0].index)]])

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=u_ch2,
        more_searches_p=mannwhitneyu(new_stud['search_count'], old_stud['search_count']).pvalue,
        more_instr_p=i_ch2,
        more_instr_searches_p=mannwhitneyu(new_inst['search_count'], old_inst['search_count']).pvalue,
    ))


if __name__ == '__main__':
    main()