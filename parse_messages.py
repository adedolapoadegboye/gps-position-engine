from pyrtcm import RTCMReader
from utils import DEBUG

### ========== RTCM MESSAGE PARSING ========== ###

def parse_rtcm_messages(stream, buffer_size=1024):
    """
    Parses RTCM messages (1019 for ephemeris, 1074 for pseudoranges),
    limiting the read buffer to a fixed size.
    Returns a list of (raw_data, parsed_data) tuples with error handling.
    """
    try:
        rtr = RTCMReader(stream)
        messages = []
        bytes_read = 0  # Track bytes read

        while bytes_read < buffer_size:
            try:
                raw_data, parsed_data = next(rtr)  # Read next RTCM message
                bytes_read += len(raw_data)  # Update bytes read count

                if parsed_data is None:
                    print("⚠ No valid RTCM message found, continuing...") if DEBUG else None
                    continue

                print(f"📥 Received RTCM Message: {parsed_data.identity}") if DEBUG else None # Debugging

                if parsed_data.identity == '1019':
                    eph_data = parse_ephemeris_1019(parsed_data)
                    messages.append((raw_data, eph_data))
                    print(f"✅ Ephemeris 1019 parsed: {eph_data}") if DEBUG else None # Debugging

                elif parsed_data.identity == '1074':
                    pr_data = parse_msm4_1074(parsed_data)
                    messages.append((raw_data, pr_data))
                    print(f"✅ Pseudorange 1074 parsed: {pr_data}") if DEBUG else None # Debugging

            except StopIteration:
                print("🔄 No more RTCM data available.") if DEBUG else None
                break  # Stop looping when there are no more messages

            except Exception as e:
                print(f"❌ Error parsing RTCM message: {e}") if DEBUG else None
                break  # Prevent infinite loop if error occurs

        print("🔚 Buffer limit reached, returning parsed messages.") if DEBUG else None
        return messages if messages else None

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        return None

def parse_ephemeris_1019(parsed_data):
    """ Extracts satellite ephemeris data (1019) from RTCM message. """
    try:
        return {field: getattr(parsed_data, field) for field in parsed_data.__dict__.keys() if field.startswith('DF')}
    except AttributeError as e:
        print(f"❌ Error parsing ephemeris data: {e}")
        return {}


def parse_msm4_1074(parsed_data):
    """ Extracts pseudorange data from MSM4 message (1074). """
    try:
        return {field: getattr(parsed_data, field) for field in parsed_data.__dict__.keys() if field.startswith('DF')}
    except AttributeError as e:
        print(f"❌ Error parsing MSM4 data: {e}")
        return {}
