from utils import DEBUG

def process_parsed_message(parsed_messages = None, eph_data_global = None, pr_data_local = None, epoch = None):
    if parsed_messages is not None:
        print(f"\n========== EPOCH {epoch + 1} ==========\n")
        for raw_data, parsed_data in parsed_messages:
            print(f"📝 Saving Raw Message: {raw_data}") if DEBUG else None
            print(f"📝 Saving Parsed Message: {parsed_data}") if DEBUG else None

            if isinstance(parsed_data, dict):
                # ✅ Safely access DF002 and ensure it's a string
                if str(parsed_data.get('DF002', "")) == "1019":
                    sat_id = parsed_data.get('DF009', None)  # Extract satellite ID

                    if sat_id and sat_id not in eph_data_global:
                        eph_data_global[sat_id] = parsed_data
                        print(f"✅ New Ephemeris Data Stored for Satellite {sat_id}") if DEBUG else None
                    elif sat_id and eph_data_global.get(sat_id) != parsed_data:
                        eph_data_global[sat_id] = parsed_data
                        print(f"🔄 Updated Ephemeris Data for Satellite {sat_id}") if DEBUG else None

                if str(parsed_data.get('DF002', "")) == "1074":
                    pr_data_local = parsed_data  # Store for per-second updates
                    print(f"📡 Pseudorange Data Added for EPOCH {epoch + 1}") if DEBUG else None
        return pr_data_local, eph_data_global
    else:
        return None, None
