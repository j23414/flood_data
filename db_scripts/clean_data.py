from get_server_data import get_table_for_variable, fig_dir
import numpy as np
import matplotlib.pyplot as plt


def account_for_elev(df, elev_threshold=10):
    cleaned = np.where(df['Value'] > elev_threshold, np.nan, df['Value'])
    df['cleaned'] = cleaned
    return df


def run_hampel_filter(df, col, k, threshold=2):
    df['rolling_median'] = df[col].rolling(k).median()
    df['rolling_std'] = df[col].rolling(k).std()
    df['num_sigma'] = abs(df[col]-df['rolling_median'])/df['rolling_std']
    df['filtered'] = np.where(df['num_sigma'] > threshold, df['rolling_median'], df[col])
    return df[['ValueID', 'Value', 'VariableID', 'SiteID', 'filtered']]


def main():
    df = get_table_for_variable(6)
    df_cleaned = account_for_elev(df)
    df_filtered = run_hampel_filter(df_cleaned, 'cleaned', 30, threshold=3)

    ax = df['Value'].plot()
    # ax = df_filtered['filtered'].plot()
    ax.set_ylabel('Shallow Well_NAVD 88 (ft)')
    ax.set_title('Raw data at MMPS-170')
    plt.savefig("{}{}.png".format(fig_dir, "raw_shallow_well"), dpi=300)


if __name__ == "__main__":
    main()
