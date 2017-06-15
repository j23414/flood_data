from hr_db_scripts.main_db_script import get_db_table_as_df
from db_scripts.main_db_script import db_filename, fig_dir
import matplotlib.pyplot as plt
import numpy as np


def plot_results(df, true_col, pred_col, set_name, model_name):
    max_val = df.max().max()*1.05
    df = df[df[true_col] > 0]
    ax = df.plot.scatter(true_col, pred_col, xlim=(0, max_val), ylim=(0, max_val),
                                 xticks=np.arange(0, max_val, 20), yticks=np.arange(0, max_val, 20)
                                 )
    rmse = (((df.iloc[:, 0] - df.iloc[:, 1])**2).mean())**0.5
    mae = (abs(df.iloc[:, 0] - df.iloc[:, 1])).mean()
    ax.text(max_val/2., max_val*0.9, 'RMSE: {}'.format(round(rmse, 2)), ha='center')
    ax.text(max_val/2., max_val*0.8, 'MAE: {}'.format(round(mae, 2)), ha='center')
    ax.plot((0, 1000), (0, 1000), ls="--", c="0.3")
    ax.set_xlabel('True')
    ax.set_ylabel('Predicted')
    ax.set_title('Reported flood occurrences: {} {}'.format(model_name, set_name))
    ax.set_aspect('equal', adjustable='box-forced')
    plt.savefig('{}results_{}_{}'.format(fig_dir, model_name, set_name), dpi=300)

model_type = 'poisson'
df_tst_res = get_db_table_as_df('{}_count_mod_res_test'.format(model_type), dbfilename=db_filename)
plot_results(df_tst_res, 'all_tst', 'all_pred_tst', 'testing', model_type)
df_trn_res = get_db_table_as_df('{}_count_mod_res_train'.format(model_type), dbfilename=db_filename)
plot_results(df_trn_res, 'all_trn', 'all_pred_trn', 'training', model_type)
