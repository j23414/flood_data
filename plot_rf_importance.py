from hr_db_scripts.main_db_script import get_db_table_as_df
from db_scripts.main_db_script import db_filename, fig_dir
import matplotlib.pyplot as plt
import numpy as np



impo_df = get_db_table_as_df('rf_count_feat_impo', dbfilename=db_filename)
impo_df.set_index('row_names', inplace=True)
ax = impo_df.mean(1).sort_values(ascending=False).plot.bar()
ax.set_xlabel('Variable')
ax.set_ylabel('Increase in MSE with permutations (%)')
ax.set_title('Variable importance from RF')
plt.tight_layout()
plt.savefig('{}_count_model_var_impo'.format(fig_dir), dpi=300)
plt.show()
