import korean_financial_minute_data_miner.market.creon.connection as creon_connection
import korean_financial_minute_data_miner.run.first_entry as run_first_entry
import korean_financial_minute_data_miner.util.time as util_time
import korean_financial_minute_data_miner.upload.history as upload_history
import korean_financial_minute_data_miner.upload.upload as upload_upload
import korean_financial_minute_data_miner.util.logging as logging
import time
import config


def run_daily_routine(dryrun):
    dt_str = util_time.get_today_str_tz()
    if upload_history.did_upload_today():
        logging.info("daily routine for {dt_str} is already done".format(dt_str=dt_str))
        return

    logging.info("starting the daily routine's ingestion for {dt_str}".format(dt_str=dt_str))
    if not dryrun:
        date_v = util_time.get_date_v_now()
        df = run_first_entry.get_first_entries_df(date_v, force_ingest=False)
        logging.info(df.head())
        logging.info(df.tail())
        logging.info("uploading for {dt_str}".format(dt_str=dt_str))
        upload_upload.upload(dt_str)

    upload_history.on_upload()
    logging.info("daily routine for {dt_str} is done".format(dt_str=dt_str))

if __name__ == '__main__':
    if not creon_connection.init_creon():
        logging.errror('creon is not initialized properly')
        exit(1)

    cfg = config.load('config.kr.yaml')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--forcerun", action="store_true", help="forcerun runs the cycle once")
    parser.add_argument("-d", "--dryrun", action="store_true", help="dryrun executes no real buy/sell trades")
    args = parser.parse_args()


    while True:
        dt_str = util_time.get_today_str_tz()
        logging.info("checking if the daily routine is to begin for {dt_str}.".format(dt_str=dt_str))
        t_ingestion_start = config.get_day_data_ingest_start(cfg)
        t = util_time.get_now_tz()
        dt_seconds = util_time.time_diff_seconds(t_ingestion_start, t)
        if dt_seconds > 0 and not args.forcerun:
            if dt_seconds > 1 * 3600:
                time.sleep(30 * 60)
            elif dt_seconds < 60:
                time.sleep(2)
            else:
                time.sleep(30)
            continue

        run_daily_routine(args.dryrun)

        if args.forcerun and not args.dryrun:
            break

        if not args.forcerun:
            logging.info("sleeping for the next iteration for {dt_str}".format(dt_str=dt_str))
            time.sleep(30 * 60)
