import argparse
import source.compression_with_lpm as lpm_comp
import source.log_conversion as log_conv
import source.lpm_detection as lpm_det

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LPM Feature Generating")

    # RECOGNITION
    parser.add_argument("--LPMs_dir", type=str, default="./testing/LPMPaymentRequest",
                        help="path to lpms (.pnml format)")
    parser.add_argument("--raw_log_file", default="./testing/RequestForPayment.xes", type=str,
                        help="path to raw xes format log file")
    parser.add_argument("--processed_log_file", default="./testing/PaymentRequest_completeLPMs_Aggregated.csv", type=str,
                        help="path to location store and name of the output file in csv format")
    parser.add_argument('--Min_prefix_size', default=2, type=float)
    parser.add_argument('--Max_prefix_size', default=36, type=float)

    # CONVERSION FROM csv TO xes
    parser.add_argument('--csv_path', default="./testing/PaymentRequest_completeLPMs_Aggregated.csv", type=str, help="")
    parser.add_argument('--xes_converted', default="./testing/PaymentRequest_completeLPMs_Aggregated.xes", type=str, help="")

    # COMPRESSION
    parser.add_argument('--input_lpms', default="./testing/LPMPaymentRequest/", type=str, help="")
    parser.add_argument('--out_xes_file', default="./testing/test_output/out.xes", type=str, help="")
    parser.add_argument('--limit', default=1, type=int)
    
    args = parser.parse_args()

    ##########
    # RECOGNITION
    Min_prefix_size = args.Min_prefix_size
    Max_prefix_size = args.Max_prefix_size
    event_log_address = args.raw_log_file
    output_address_name_file = args.processed_log_file
    LPMs_folder_name = args.LPMs_dir

    lpm_det.lpm_detection(Min_prefix_size, Max_prefix_size, event_log_address, output_address_name_file, LPMs_folder_name)
    ##########

    ##########
    # CONVERSION FROM csv TO xes
    csv_path = args.csv_path
    xes_converted = args.xes_converted
    
    log_conv.conversion(csv_path, xes_converted)
    ##########

    ##########
    # COMPRESSION
    input_lpms = args.input_lpms
    out_xes = args.out_xes_file
    limit = args.limit
    
    lpm_comp.subdue_extended(xes_converted, input_lpms, limit, out_xes)
    ##########