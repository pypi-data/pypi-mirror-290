
# pylint: disable=line-too-long

from copy import deepcopy

def provider_preproc_single_ticker_bulk(records_origin_short_ref, original_records, preproc_descr=None):

    """
    Preprocesses the original records for a single ticker by applying provider-specific transformations.
    This function deep-copies the original records and applies preprocessing steps based on the data source. 
    For example, it can rename the date column to a standard format and document the changes in a description list.
    """

    if preproc_descr is None:
        preproc_descr = []

    copied_original_records = deepcopy(original_records)
    date_col_name=None  # Initialize date_col_name

    if records_origin_short_ref == "eodhd_eod":
        date_col_name = "date"
        for record in copied_original_records:
            # Directly rename the key within the record
            record['date_id'] = record.pop(date_col_name)
        preproc_descr.append(f"--Renamed '{date_col_name}' to 'date_id' --")
        return copied_original_records, preproc_descr, date_col_name

    raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")


def common_preproc_market_single_ticker_bulk(records_input, preproc_descr=None):

    """
    Applies common preprocessing steps to market data for a single ticker.

    This function processes the input records by rounding the prices to 2 decimal places 
    (3 decimals if the price is less than or equal to 1) and updates the preprocessing description list.
    """
    
    processed_data = []
    if preproc_descr is None:
        preproc_descr = []

    ##############################################################
    ########## Define processing helpers #######################

    ################ Round values to save space ###########
    def round_value(value):
        return round(value, 3 if value <= 1 else 2)

    #############################################
    ########## Apply #############################
    for entry in records_input:
        processed_entry = entry.copy()
        # Apply rounding to the numeric fields
        for key in ['open', 'high', 'low', 'close', 'adjusted_close']:
            value = processed_entry.get(key)
            if value is not None:
                processed_entry[key] = round_value(float(value))
        processed_data.append(processed_entry)

    preproc_descr.append("--Rounded prices to 2 decimals (to 3 decimals if price <=1)--")


    return processed_data, preproc_descr
