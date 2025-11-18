from datetime import datetime

def calculate_checksum(record):
    """
    Calculate the checksum for a given Intel HEX record.
    """
    # Convert the record to bytes
    record_bytes = bytes.fromhex(record[1:])
    
    # Calculate the sum of the bytes
    checksum = sum(record_bytes)
    
    # Take the two's complement of the least significant byte
    checksum = ((~checksum + 1) & 0xFF)
    
    return f"{checksum:02X}"

def zeropad_hexfile(input_file, output_file, start_address, end_address):
    """
    Zeropad a hexfile with all memory locations in range and calculate checksums.
    Each line should be of length 0x10.
    """
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Dictionary to store the data at each address
    memory = {}
    
    # Parse the input file and store data in memory dictionary
    for line in lines:
        if line.startswith(':'):
            byte_count = int(line[1:3], 16)
            address = int(line[3:7], 16)
            record_type = int(line[7:9], 16)
            data = line[9:9 + 2 * byte_count]
            checksum = line[9 + 2 * byte_count:11 + 2 * byte_count]
            
            if record_type == 0:  # Data record
                for i in range(byte_count):
                    memory[address + i] = data[2 * i:2 * i + 2]
    
    # Zeropad the memory and write to output file
    with open(output_file, 'w') as outfile:
        address = start_address
        while address <= end_address:
            data_bytes = []
            for i in range(0x10):
                if address + i in memory:
                    data_bytes.append(memory[address + i])
                else:
                    data_bytes.append("00")
            
            record_data = ''.join(data_bytes)
            record = f":10{address:04X}00{record_data}"
            checksum = calculate_checksum(record)
            outfile.write(f"{record}{checksum}\n")
            
            address += 0x10
        
        # Write End Of File (EOF) record
        outfile.write(":00000001FF\n")

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Example usage
input_file = "D:\code\e41-rc1\DefaultBuild\R7F123FGG3AFB_V05.hex"
output_file = f"output_{current_datetime}.hex"
#output_file = "output.hex"
start_address = 0x5020
end_address = 0x80D0

zeropad_hexfile(input_file, output_file, start_address, end_address)
