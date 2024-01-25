import argparse

def main():

    parser = argparse.ArgumentParser(prog = "bs",
                                     description = "Booking System article demo package.")
    
    parser.add_argument("integers", metavar = "N", type = int, nargs = "+",
                        help = "an integer for the accumulator")
    
    parser.add_argument("-greet", action = "store_const", const = True,
                        default = False, dest = "greet", 
                        help = "Greet Message fron Booking System Team.")
    

    parser.add_argument("--sum", dest = "accumulate", action = "store_const", 
                        const = sum, default = max,
                        help = "sum the integers (default: find the max)")
    

    args = parser.parse_args()


    if args.greet():
        print("Welcome to Booking System !")

        if args.accumulate == max:
            print("The Computation Done is Maximum")
        else:
            print("The Computation Done is Summation")
        print("And Here's your result:", end =" ")

    print(args.accumulate(args.integers))