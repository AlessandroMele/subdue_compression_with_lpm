import argparse
import source.compression_with_lpm as lpm_comp
import source.log_conversion as log_conv
import source.lpm_detection as lpm_det

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Subdue compression with Local Process Model")

    # RECOGNITION PARAMETERS

    parser.add_argument("--LPMs_dir", type=str, default="./testing/LPMPaymentRequest/",
                        help="path to lpms (.pnml format)")
    
    parser.add_argument("--raw_log_file", default="./testing/RequestForPayment.xes", type=str,
                        help="path to raw xes format log file")
   
    parser.add_argument("--processed_log_file", default="./testing/PaymentRequest_completeLPMs_Aggregated.csv", type=str,
                        help="path to location store and name of the output file in csv format")
    
    parser.add_argument('--Min_prefix_size', default=2, type=float)
    parser.add_argument('--Max_prefix_size', default=36, type=float)
    
    ##########

    # CONVERSION FROM csv TO xes PARAMETERS
    parser.add_argument('--xes_converted', default="./testing/PaymentRequest_completeLPMs_Aggregated.xes", type=str,
                        help="path to location store and name the converted file from csv to xes format")
    ##########
                    
    # COMPRESSION PARAMETERS
        
    parser.add_argument('--out_xes_file', default="./testing/PaymentRequest_completeLPMs_compressed.xes", type=str,
                        help="path to location store and name of the compressed output file in xes format")

    parser.add_argument('--limit', default=1, type=int,
                        help = "number of iteration of the compression module, for future developments")

    parser.add_argument('--prefix', default="testLaura_", type=str,
                        help = "template filename of lpm")

    parser.add_argument('--suffix', default="pnml", type=str,
                        help = "extension of lpm")

    args = parser.parse_args()
    
    ##########

    # RECOGNITION MODULE
    Min_prefix_size = args.Min_prefix_size
    Max_prefix_size = args.Max_prefix_size
    event_log_address = args.raw_log_file
    output_address_name_file = args.processed_log_file
    LPMs_folder_name = args.LPMs_dir

    lpm_det.lpm_detection(Min_prefix_size, Max_prefix_size, event_log_address, output_address_name_file, LPMs_folder_name)
    
    ##########

    # CONVERSION FROM csv TO xes MODULE
    xes_converted = args.xes_converted
    
    log_conv.from_csv_to_xes(output_address_name_file, xes_converted)
    
    ##########

    # COMPRESSION MODULE
    out_xes = args.out_xes_file
    limit = args.limit
    prefix = args.prefix
    suffix = args.suffix

    lpm_comp.compression(xes_converted, LPMs_folder_name, limit, out_xes, prefix, suffix)
    
    ##########

    # PRESENTAZIONE
    """
    python3 subdue_extended.py --xes_converted=testing_presentazione/test_input/test_esempio_7.xes --LPMs_dir=./testing_presentazione/test_input/LPMs/ --out_xes_file=testing_presentazione/test_output/output.xes --prefix=lpm --suffix=apnml
    """
