import rosbag
from itertools import izip, islice

def merge_left_right_bags(iter1, iter2):
    cnt = 0
    for i, j in izip(iter1, iter2):
        cnt += 1
        if cnt == 1:
            ret1 = i
            ret3 = j
        if cnt == 2:
            ret2 = i
            ret4 = j
        if cnt == 4:
            cnt = 0
            yield {"left_camera_info":ret1, "left_image_raw":ret2, "right_camera_info":ret3, "right_image_raw":ret4}

def get_bags_with_start_stamp(bag_file_path, start_stamp, start_topic):
    bags = rosbag.Bag(bag_file_path).read_messages()
    start_index = 0
    for bag in bags:
        # print str(bag.timestamp)
        if (str(bag.timestamp).startswith(start_stamp)) & (bag.topic == start_topic):
            print "Start Point Found: " + start_topic
            break
        start_index += 1
    bags = islice(rosbag.Bag(bag_file_path).read_messages(), start_index, None)
    print "Get the camera data from " + start_stamp
    return bags

def synchronize_two_cameras(bag_file_path, left_start_stamp, right_start_stamp):
    left_bags = get_bags_with_start_stamp(bag_file_path, left_start_stamp, "/stereo/left/camera_info")
    right_bags = get_bags_with_start_stamp(bag_file_path, right_start_stamp, "/stereo/right/camera_info")

    bags = merge_left_right_bags(left_bags, right_bags)
    return bags

def synchronize_four_cameras(kyle_bag_file_path, kyle_left_start_stamp, kyle_right_start_stamp,
                                melody_bag_file_path, melody_left_start_stamp, melody_right_start_stamp):
    kyle_cameras = synchronize_two_cameras(kyle_bag_file_path, kyle_left_start_stamp, kyle_right_start_stamp)
    melody_cameras = synchronize_two_cameras(melody_bag_file_path, melody_left_start_stamp, melody_right_start_stamp)
    for i, j in izip(kyle_cameras, melody_cameras):
        yield {"kyle_cameras":i, "melody_cameras":j}

if __name__ == "__main__":
    kyle_bag_file_path = './rosbag_files/calibration_kyle.bag'
    kyle_left_start_stamp = "15193252432"
    kyle_right_start_stamp = "15193252431"

    melody_bag_file_path = './rosbag_files/calibration_melody.bag'
    melody_left_start_stamp = "15193252431"
    melody_right_start_stamp = "15193252431"

    four_cameras = synchronize_four_cameras(kyle_bag_file_path, kyle_left_start_stamp, kyle_right_start_stamp,
                                            melody_bag_file_path, melody_left_start_stamp, melody_right_start_stamp)

    for frame in four_cameras:
        print frame["kyle_cameras"]["left_camera_info"].timestamp
        print frame["melody_cameras"]["right_image_raw"].timestamp
        break
