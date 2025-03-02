import time
import numpy as np
from math import pi

# Import local functions
from utils import DEBUG, SPEED_OF_LIGHT, OMEGA_E
from gps_receiver import GPSReceiver
from parse_messages import parse_rtcm_messages
from process_parsed_message import process_parsed_message
from format_ephemeris import format_ephemeris
from format_pseudorange import format_pseudorange
from format_receiver_tow import format_receiver_tow
from estimate_satellite_clock_bias import estimate_satellite_clock_bias
from get_satellite_position import get_satellite_position
from estimate_position import estimate_position
from WGStoEllipsoid import WGStoEllipsoid


### ========== MAIN PROCESSING LOOP ========== ###
def main():
    user_position_array = []
    HDOP_array = []
    VDOP_array =[]
    rcvr_clock_bias_array = []
    pr_data_local = {}
    eph_data_global = {}
    epoch = 0
    xu, b = np.array([0, 0, 0]), 0

    try:
        gps_receiver = GPSReceiver(serial_port='/dev/tty.usbserial-147120')  # Change to your port

        while True:
            parsed_messages = parse_rtcm_messages(gps_receiver.ser)
            pr_data, eph_data = process_parsed_message(parsed_messages, eph_data_global, pr_data_local, epoch)

            print(pr_data) if DEBUG else None
            print(eph_data) if DEBUG else None

            formatted_eph_data = format_ephemeris(eph_data)
            print(f"EPH: {formatted_eph_data}")

            formatted_pr_data = format_pseudorange(pr_data)
            print(f"PR: {formatted_pr_data}")

            receiver_tow = format_receiver_tow(pr_data)
            print(f"Receiver TOW: {receiver_tow}")

            if formatted_pr_data.keys() == formatted_eph_data.keys() and len(formatted_eph_data) > 4:
                # If all satellites with pseudorange values have corresponding EPH data and more than 4 satellites are visible
                numSV = len(formatted_eph_data)
                formatted_corrected_pseudorange_data = {}

                for sv_id, pseudorange in formatted_pr_data.items():
                    # Estimate satellite clock bias for each satellite
                    sat_clk_bias = estimate_satellite_clock_bias(receiver_tow, formatted_eph_data[sv_id])

                    # Apply correction
                    corrected_pseudorange = pseudorange + (SPEED_OF_LIGHT * sat_clk_bias)
                    formatted_corrected_pseudorange_data[sv_id] = corrected_pseudorange

                print(f"Sat CLK Corrected PR: {formatted_corrected_pseudorange_data}")

                dx = np.array([100, 100, 100])  # 1D array
                ds_ = np.array([100, 100, 100])  # 1D array
                db = 100

                while np.linalg.norm(dx) > 0.1 and abs(db) > 1:
                    Xs = np.empty((0, 3))  # Initialize empty (0,3) NumPy array
                    pr = np.array([])  # Initialize as empty NumPy array

                    for svid, pseudorange in formatted_corrected_pseudorange_data.items():
                        cpr = pseudorange - b

                        # Convert `pr` into a NumPy array while keeping shape consistent
                        pr = np.append(pr, cpr)  # Append corrected pseudorange values

                        tau = cpr / SPEED_OF_LIGHT
                        satellite_tow = receiver_tow - tau

                        # Get satellite position
                        ds_ = get_satellite_position(formatted_eph_data[svid], satellite_tow)
                        print(f"Satellite {svid} ECEF Position: {ds_}")
                        theta = OMEGA_E * tau
                        print(f"Satellite {svid} theta: {theta}") if DEBUG else None

                        # Stack `ds_` properly into `Xs`
                        Xs = np.vstack((Xs, ds_))

                    print(f"Xs Shape: {Xs.shape}, pr Shape: {pr.shape}") if DEBUG else None
                    print(f"Xs: {Xs}")
                    print(f"pr: {pr}")

                    xu = np.array(xu, dtype=np.float64)
                    b = float(b)

                    x_, b_, norm_dp, G = estimate_position(Xs, pr, numSV, xu, b, 3)

                    dx = x_ - xu
                    db = b_ - b
                    xu = x_
                    b = b_
                    print(f"xu: {xu}")
                    print(f"norm_dp: {norm_dp}")
                    print(f"G: {G}")


                lambda_, phi, h = WGStoEllipsoid(xu[0], xu[1], xu[2])
                latitude = (phi * 180) / pi
                longitude = (lambda_ * 180) / pi
                print(f"Longitude: {longitude}")
                print(f"Latitude: {latitude}")
            epoch += 1
            time.sleep(1)  # Process every 2 seconds
    except Exception as e:
        print(f"❌ Critical Error: {e}")
    return None


if __name__ == "__main__":
    main()

