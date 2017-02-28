from db_scripts.data_utils import resample_df, filter_df_by_dates
from db_scripts.get_server_data import get_table_for_variable
from flood_data.db_scripts.focus_intersection import all_flood_dates


def number_of_flood_dates_over_threshold(threshold=3.2, units="feet"):
    tide_df = get_table_for_variable('tide')
    tide_df = resample_df(tide_df, 'max')
    tide_df = filter_df_by_dates(tide_df, all_flood_dates)
    above_thresh = tide_df[tide_df.Value > 3.2]
    msg = "For {} out of {} total flood events, the tide level exceeded the threshold of {} {}"
    msg = msg.format(
        len(above_thresh.index),
        len(tide_df.index),
        threshold,
        units
    )

    print msg
    return above_thresh


def main():
    number_of_flood_dates_over_threshold()


if __name__ == "__main__":
    main()
