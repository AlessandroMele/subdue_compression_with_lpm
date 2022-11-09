import argparse
import source.compression_with_lpm as lpm_comp
import source.log_conversion as log_conv
import source.lpm_detection as lpm_det

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Subdue compression with Local Process Model")

    # RECOGNITION PARAMETERS
    parser.add_argument("--lpms_dir",
    default="./testing/LPMPaymentRequest/LPMs/",
    type=str,
    help="path to lpms (pnml or apnml format)")

    parser.add_argument("--raw_log_file",
    default="./testing/LPMPaymentRequest/RequestForPayment.xes",
    type=str,
    help="path to raw xes format log file")

    parser.add_argument("--processed_log_file",
    default="./testing/LPMPaymentRequest/RequestForPayment_completeLPMs_aggregated.csv",
    type=str,
    help="path to location store and name of the output file in csv format")

    parser.add_argument('--min_prefix_size',
    default=2,
    type=float)

    parser.add_argument('--max_prefix_size',
    default=36,
    type=float)
    ##########

    # CONVERSION FROM csv TO xes PARAMETERS
    parser.add_argument('--xes_converted',
    default="./testing/LPMPaymentRequest/RequestForPayment_completeLPMs_converted.xes",
    type=str,
    help="path to location store and name the converted file from csv to xes format")
    ##########
                    
    # COMPRESSION PARAMETERS
    parser.add_argument('--xes_compressed',
    default="./testing/LPMPaymentRequest/RequestForPayment_completeLPMs_compressed.xes",
    type=str,
    help="path to location store and name of the compressed output file in xes format")
    
    parser.add_argument('--limit',
    default=1,
    type=int,
    help = "number of iteration of the compression module (for further developments)")

    parser.add_argument('--prefix',
    default="testLaura_",
    type=str,
    help = "template filename of lpm")

    parser.add_argument('--suffix',
    default="pnml",
    type=str,
    help = "extension of lpm")

    args = parser.parse_args()
    ##########

    # RECOGNITION MODULE
    min_prefix_size = args.min_prefix_size
    max_prefix_size = args.max_prefix_size
    event_log_address = args.raw_log_file
    output_address_name_file = args.processed_log_file
    lpms_folder_name = args.lpms_dir
    ##########

    # CONVERSION FROM csv TO xes MODULE
    xes_converted = args.xes_converted
    ##########

    # COMPRESSION MODULE
    xes_compressed = args.xes_compressed
    limit = args.limit
    prefix = args.prefix
    suffix = args.suffix
    ##########

    iteration = 0
    while(iteration<limit):
        if(iteration != 0):
            event_log_address = xes_compressed
        
        # for testing only compression module
        # lpm_det.lpm_detection(min_prefix_size, max_prefix_size, event_log_address, output_address_name_file, lpms_folder_name)
        # log_conv.from_csv_to_xes(output_address_name_file, xes_converted)
        
        lpm_comp.compression(xes_converted, lpms_folder_name, xes_compressed, prefix, suffix, iteration)
        iteration += 1

    # TEST LPMPaymentRequest
    """
    python3 subdue_extended.py --lpms_dir=./testing/LPMPaymentRequest/LPMs/ --raw_log_file=./testing/LPMPaymentRequest/RequestForPayment.xes --processed_log_file=./testing/LPMPaymentRequest/RequestForPayment_completeLPMs_aggregated.csv --xes_converted=./testing/LPMPaymentRequest/RequestForPayment_completeLPMs_converted.xes --xes_compressed=./testing/LPMPaymentRequest/RequestForPayment_completeLPMs_compressed.xes --prefix=testLaura_ --suffix=pnml
    """
    ##########

    # TEST BPI12_w
    """
    python3 subdue_extended.py --lpms_dir=./testing/BPI12_w/LPMs/ --raw_log_file=./testing/BPI12_w/BPI12_w.xes --processed_log_file=./testing/BPI12_w/BPI12_w_completeLPMs_aggregated.csv --xes_converted=./testing/BPI12_w/BPI12_w_completeLPMs_converted.xes --xes_compressed=./testing/BPI12_w/BPI12_w_completeLPMs_compressed.xes --prefix=testLaura_ --suffix=pnml
    """
    ##########

    # PRESENTAZIONE
    """
    python3 subdue_extended.py --lpms_dir=./testing/Presentazione/LPMs/ --xes_converted=./testing/Presentazione/test_7.xes --xes_compressed=./testing/Presentazione/test_7_compressed.xes --prefix=lpm --suffix=apnml
    """