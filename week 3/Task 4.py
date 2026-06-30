def convert_f_to_c(f_temp):
    return (f_temp - 32) * (5.0 / 9.0)

def convert_c_to_f(c_temp):
    return (c_temp * 1.8) + 32

mode = input("Convert F to C or C to F? (fc/cf): ").strip().lower()

if mode == "fc":
    val_f = float(input("Enter temperature in Fahrenheit: "))
    print(f"Celsius: {convert_f_to_c(val_f):.2f}")
elif mode == "cf":
    val_c = float(input("Enter temperature in Celsius: "))
    print(f"Fahrenheit: {convert_c_to_f(val_c):.2f}")
else:
    print("Invalid choice!")